"""
SMS API Service - FastAPI Application
RESTful API để gửi SMS qua nhiều dịch vụ khác nhau
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator
import logging
from typing import Optional
import config
from smsvip_loader import get_loader

# Setup logging
logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SMS API Service",
    description="RESTful API để gửi SMS OTP qua nhiều dịch vụ khác nhau",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class SMSRequest(BaseModel):
    phone: str = Field(..., description="Số điện thoại nhận SMS (10-11 số)")
    amount: int = Field(default=10, ge=1, le=2000, description="Số lượng dịch vụ gửi SMS (1-2000)")
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        # Remove spaces and special characters
        phone = ''.join(filter(str.isdigit, v))
        
        # Check length
        if len(phone) < 10 or len(phone) > 11:
            raise ValueError('Số điện thoại phải có 10-11 số')
        
        # Check if starts with 0
        if not phone.startswith('0'):
            raise ValueError('Số điện thoại phải bắt đầu bằng số 0')
        
        return phone


class SingleServiceRequest(BaseModel):
    phone: str = Field(..., description="Số điện thoại nhận SMS (10-11 số)")
    service_name: str = Field(..., description="Tên dịch vụ cụ thể (vd: momo, viettel, vieon)")
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        # Remove spaces and special characters
        phone = ''.join(filter(str.isdigit, v))
        
        # Check length
        if len(phone) < 10 or len(phone) > 11:
            raise ValueError('Số điện thoại phải có 10-11 số')
        
        # Check if starts with 0
        if not phone.startswith('0'):
            raise ValueError('Số điện thoại phải bắt đầu bằng số 0')
        
        return phone


# Initialize service loader on startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting SMS API Service...")
    loader = get_loader()
    logger.info(f"Loaded {loader.get_service_count()} SMS services")


# Root endpoint
@app.get("/", tags=["Info"])
async def root():
    """Get API information"""
    loader = get_loader()
    return {
        "name": "SMS API Service",
        "version": "1.0.0",
        "description": "RESTful API để gửi SMS OTP qua nhiều dịch vụ Việt Nam",
        "total_services": loader.get_service_count(),
        "endpoints": {
            "send_batch": "POST /api/sms/send - Gửi SMS qua nhiều dịch vụ",
            "send_single": "POST /api/sms/single - Gửi SMS qua 1 dịch vụ cụ thể",
            "list_services": "GET /api/sms/services - Danh sách dịch vụ",
            "health": "GET /health - Health check",
            "docs": "GET /docs - Swagger UI",
        }
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    loader = get_loader()
    return {
        "status": "healthy",
        "services_loaded": loader.get_service_count()
    }


# List available services
@app.get("/api/sms/services", tags=["SMS"])
async def list_services():
    """
    Lấy danh sách tất cả các dịch vụ SMS có sẵn
    """
    try:
        loader = get_loader()
        services = loader.get_available_services()
        
        return {
            "status": "success",
            "total": len(services),
            "services": sorted(services)[:50]  # Return first 50 unique service names
        }
    except Exception as e:
        logger.error(f"Error listing services: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing services: {str(e)}"
        )


# Send SMS via multiple services (Auto spam)
@app.post("/api/sms/send", tags=["SMS"])
async def send_sms_batch(request: SMSRequest):
    """
    Gửi SMS OTP qua nhiều dịch vụ ngẫu nhiên
    
    - **phone**: Số điện thoại nhận SMS (10-11 số, bắt đầu bằng 0)
    - **amount**: Số lượng dịch vụ gửi SMS (mặc định 10, tối đa 100)
    
    API sẽ tự động chọn ngẫu nhiên N dịch vụ và gửi SMS song song
    """
    try:
        logger.info(f"Sending SMS to {request.phone} via {request.amount} services")
        
        loader = get_loader()
        results = loader.send_sms_batch(request.phone, request.amount)
        
        return {
            "status": "completed",
            "message": f"Đã gửi SMS qua {results['success_count']}/{results['total_services']} dịch vụ",
            "data": results
        }
        
    except Exception as e:
        logger.error(f"Error sending batch SMS: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending SMS: {str(e)}"
        )


# Spam via GET Link (Run directly in browser)
@app.get("/api/spam", tags=["SMS"])
async def spam_get(phone: str, amount: int = 100):
    """
    Spam SMS trực tiếp qua đường dẫn trình duyệt (GET Method)
    
    Cách dùng: truy cập URL
    /api/spam?phone=0865526740&amount=1000
    """
    try:
        # Validate phone basic
        if not phone.startswith('0') or len(phone) < 10:
             return {"status": "error", "message": "So dien thoai khong hop le"}
             
        # Limit amount
        if amount > 2000: amount = 2000
        
        loader = get_loader()
        # Chay background task hoac doi ket qua
        # O day ta doi luon vi user muon thay ket qua
        results = loader.send_sms_batch(phone, amount)
        
        return {
            "status": "completed",
            "message": f"SPAM SUCCESS: {results['success_count']}/{results['total_services']} services -> {phone}",
            "details": results
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Send SMS via specific service
@app.post("/api/sms/single", tags=["SMS"])
async def send_sms_single(request: SingleServiceRequest):
    """
    Gửi SMS OTP qua một dịch vụ cụ thể
    
    - **phone**: Số điện thoại nhận SMS (10-11 số, bắt đầu bằng 0)
    - **service_name**: Tên dịch vụ (vd: momo, viettel, vieon, tiki, fpt, ...)
    
    Sử dụng GET /api/sms/services để xem danh sách dịch vụ có sẵn
    """
    try:
        logger.info(f"Sending SMS to {request.phone} via {request.service_name}")
        
        loader = get_loader()
        result = loader.send_sms_single(request.phone, request.service_name)
        
        if result.get("status") == "error":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result.get("error")
            )
        
        return {
            "status": "success",
            "message": f"Đã gửi SMS qua dịch vụ {request.service_name}",
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending single SMS: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending SMS: {str(e)}"
        )


# Custom exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "message": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEBUG_MODE
    )
