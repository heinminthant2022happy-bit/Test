import sys, time, os, requests, hashlib, base64
from datetime import datetime

# --- CONFIGURATION ---
DB_URL = "https://raw.githubusercontent.com/heinminthant2022happy-bit/Test/main/database.txt?v=" + str(time.time())

def get_fixed_id():
    # engine.so က တောင်းနေတဲ့ 10277user ဆိုတဲ့ ID ထွက်လာအောင် လုပ်ပေးခြင်း
    return "10277user"

def create_bypass(key_val):
    # engine.so က လိုချင်နိုင်တဲ့ token ဖိုင်ကို အတင်းဆောက်ပေးမယ်
    files = [".access_token", "key.txt"]
    for f_name in files:
        with open(f_name, "w") as f:
            f.write(key_val)

def check_online():
    try:
        r = requests.get(DB_URL, headers={'Cache-Control': 'no-cache'}, timeout=5)
        return r.text.splitlines() if r.status_code == 200 else None
    except: return None

def main_auth():
    os.system('clear')
    my_id = get_fixed_id()
    print(f"\033[0;36m[!] System ID: {my_id}\033[00m")
    
    db_data = check_online()
    if not db_data:
        print("No Internet Connection."); return False

    u_key = input("\033[0;33mEnter Access Key: \033[00m").strip()
    
    for line in db_data:
        if f"{my_id}|{u_key}" in line:
            # အောင်မြင်တာနဲ့ engine အတွက် bypass လုပ်မယ်
            create_bypass(u_key)
            print("\033[0;32m[+] Bypass Successful!\033[00m")
            return True
            
    print("\033[0;31m[!] Invalid Key.\033[00m")
    return False

if __name__ == "__main__":
    try:
        import engine
        if main_auth():
            time.sleep(1)
            engine.run_script()
    except ImportError:
        print("engine.so missing.")
        
