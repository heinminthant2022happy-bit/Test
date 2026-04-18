import sys, time, os, requests, hashlib, base64
from datetime import datetime

# --- CONFIGURATION ---
DB_URL = "https://raw.githubusercontent.com/heinminthant2022happy-bit/Test/main/database.txt?v=" + str(time.time())
LOCAL_DB = ".sys_auth.bin"

def get_fixed_id():
    try:
        aid = os.popen("whoami").read().strip()
        if not aid: aid = "default_user"
    except:
        aid = "user_backup"
    unique_id = "TRB-" + hashlib.md5(aid.encode()).hexdigest()[:12].upper()
    return unique_id

# --- ENGINE BYPASS LOGIC ---
def create_engine_bypass(key):
    # engine.so က လိုချင်နိုင်တဲ့ ဖိုင်နာမည်များ (ဒါတွေကို အလိုအလျောက် ဆောက်ပေးမယ်)
    bypass_files = [".access_token", "key.txt", ".key.bin", "access.txt"]
    for filename in bypass_files:
        try:
            with open(filename, "w") as f:
                f.write(key)
        except:
            pass

def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(data):
    try: return base64.b64decode(data.encode()).decode()
    except: return ""

def check_online():
    try:
        headers = {'Cache-Control': 'no-cache', 'Pragma': 'no-cache'}
        r = requests.get(DB_URL, headers=headers, timeout=5)
        return r.text.splitlines() if r.status_code == 200 else None
    except:
        return None

def main_auth():
    os.system('clear')
    my_id = get_fixed_id()
    print(f"\033[0;36mDevice ID: {my_id}\033[00m")
    
    db_data = check_online()
    
    # ၁။ Offline Check
    if os.path.exists(LOCAL_DB):
        with open(LOCAL_DB, "r") as f:
            saved = decrypt_data(f.read()).split("|")
            if len(saved) == 3:
                s_id, s_key, s_date = saved
                if s_id == my_id:
                    expire_dt = datetime.strptime(s_date, "%Y-%m-%d")
                    if db_data:
                        found = False
                        for line in db_data:
                            if f"{my_id}|{s_key}|{s_date}" == line:
                                found = True; break
                        if not found:
                            os.remove(LOCAL_DB)
                            return False
                    
                    if expire_dt > datetime.now():
                        # Auto Login ဖြစ်တဲ့အချိန်မှာလည်း Bypass ဖိုင်ကို ပြန်ဆောက်ပေးမယ်
                        create_engine_bypass(s_key)
                        print(f"\033[0;32m[+] Access Verified! Expire: {s_date}\033[00m")
                        return True

    # ၂။ Key အသစ်တောင်းခြင်း
    if not db_data:
        print("\033[0;31m[!] No Internet Connection.\033[00m")
        return False

    u_key = input("\033[0;33mEnter Access Key: \033[00m").strip()
    for line in db_data:
        parts = line.split("|")
        if len(parts) == 3 and parts[0] == my_id and parts[1] == u_key:
            if datetime.strptime(parts[2], "%Y-%m-%d") > datetime.now():
                with open(LOCAL_DB, "w") as f:
                    f.write(encrypt_data(line))
                # Key မှန်တာနဲ့ Bypass ဖိုင်ကို ဆောက်မယ်
                create_engine_bypass(u_key)
                print("\033[0;32m[+] Access Granted!\033[00m")
                time.sleep(1)
                return True
    
    print(f"\033[0;31m[!] Invalid Key for ID: {my_id}\033[00m")
    return False

if __name__ == "__main__":
    try:
        import engine
        if main_auth():
            # engine.so ကို မ run ခင် 0.5 စက္ကန့် ခဏစောင့်မယ် (ဖိုင်ဆောက်တာ သေချာစေရန်)
            time.sleep(0.5)
            engine.run_script()
    except ImportError:
        print("engine.so missing.")

