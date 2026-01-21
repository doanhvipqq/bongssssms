import sys
import os

# Gia lap moi truong Vercel
print("Testing Vercel Entry Point...")

try:
    from api.index import app
    print("✅ Load api/index.py SUCCESS")
    
    from smsvip_loader import get_loader
    loader = get_loader()
    print(f"✅ Loaded {loader.get_service_count()} services")
    
except Exception as e:
    print(f"❌ FAIL: {e}")
    import traceback
    traceback.print_exc()
