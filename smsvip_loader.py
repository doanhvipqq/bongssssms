"""
SMS Service Loader Module
Dynamically loads and manages SMS service functions from multiple smsvip files
"""

import importlib
import inspect
import random
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Callable, Tuple
import config

# Setup logging
logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)
logger = logging.getLogger(__name__)


class SMSServiceLoader:
    def __init__(self):
        self.services: Dict[str, Callable] = {}
        self.service_names: List[str] = []
        self.executor = ThreadPoolExecutor(max_workers=config.MAX_WORKERS)
        
    def load_all_services(self) -> Dict[str, Callable]:
        """Load all SMS service functions from configured files"""
        logger.info("Loading SMS services...")
        
        for service_file in config.SERVICE_FILES:
            try:
                # Import module dynamically - Always use 'services' package
                module_name = f"services.{service_file}"
                module = importlib.import_module(module_name)
                
                # Get all functions from module
                functions = inspect.getmembers(module, inspect.isfunction)
                
                # Filter functions (assuming SMS functions take 'phone' parameter)
                for func_name, func in functions:
                    # Skip private functions
                    if func_name.startswith('_'):
                        continue
                    
                    # Check if function has 'phone' parameter
                    sig = inspect.signature(func)
                    if 'phone' in sig.parameters or 'sdt' in sig.parameters:
                        # Create unique key: servicefile_functionname
                        service_key = f"{service_file}_{func_name}"
                        self.services[service_key] = func
                        self.service_names.append(func_name)
                
                logger.info(f"Loaded {len([f for f in functions if not f[0].startswith('_')])} functions from {service_file}")
                
            except Exception as e:
                logger.error(f"Error loading {service_file}: {str(e)}")
                continue
        
        logger.info(f"Total services loaded: {len(self.services)}")
        return self.services
    
    def get_available_services(self) -> List[str]:
        """Get list of available service names"""
        return list(set(self.service_names))
    
    def get_random_services(self, amount: int) -> List[Tuple[str, Callable]]:
        """Get random services for sending SMS"""
        if amount > len(self.services):
            amount = len(self.services)
        
        selected = random.sample(list(self.services.items()), amount)
        return selected
    
    def _call_service(self, service_name: str, service_func: Callable, phone: str) -> Dict:
        """Call a single SMS service function"""
        try:
            # Try calling with 'phone' parameter
            sig = inspect.signature(service_func)
            if 'phone' in sig.parameters:
                result = service_func(phone=phone)
            elif 'sdt' in sig.parameters:
                result = service_func(sdt=phone)
            else:
                # Try positional argument
                result = service_func(phone)
            
            return {
                "service": service_name,
                "status": "success",
                "result": result if result else "SMS sent"
            }
        except Exception as e:
            logger.error(f"Error calling {service_name}: {str(e)}")
            return {
                "service": service_name,
                "status": "error",
                "error": str(e)
            }
    
    def send_sms_batch(self, phone: str, amount: int) -> Dict:
        """Send SMS via multiple services concurrently"""
        selected_services = self.get_random_services(amount)
        
        results = {
            "phone": phone,
            "requested": amount,
            "total_services": len(selected_services),
            "results": []
        }
        
        # Execute services concurrently
        futures = {}
        for service_name, service_func in selected_services:
            future = self.executor.submit(self._call_service, service_name, service_func, phone)
            futures[future] = service_name
        
        # Collect results
        success_count = 0
        error_count = 0
        
        for future in as_completed(futures, timeout=config.REQUEST_TIMEOUT):
            try:
                result = future.result()
                results["results"].append(result)
                
                if result["status"] == "success":
                    success_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                error_count += 1
                results["results"].append({
                    "service": futures[future],
                    "status": "error",
                    "error": f"Timeout or execution error: {str(e)}"
                })
        
        results["success_count"] = success_count
        results["error_count"] = error_count
        
        return results
    
    def send_sms_single(self, phone: str, service_name: str) -> Dict:
        """Send SMS via a specific service"""
        # Find service by name
        matching_services = [(k, v) for k, v in self.services.items() if service_name.lower() in k.lower()]
        
        if not matching_services:
            return {
                "status": "error",
                "error": f"Service '{service_name}' not found"
            }
        
        # Use first matching service
        service_key, service_func = matching_services[0]
        return self._call_service(service_key, service_func, phone)
    
    def get_service_count(self) -> int:
        """Get total number of loaded services"""
        return len(self.services)


# Global instance
_loader = None

def get_loader() -> SMSServiceLoader:
    """Get or create global SMS service loader instance"""
    global _loader
    if _loader is None:
        _loader = SMSServiceLoader()
        _loader.load_all_services()
    return _loader
