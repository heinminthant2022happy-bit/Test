import sys, time, os, requests, hashlib, base64
from datetime import datetime

# ၁။ engine.so စစ်ဆေးခြင်း
try:
    import engine
except ImportError:
    print("\033[0;31m[!] Error: engine.so missing.\033[00m")
    sys.exit(1)

# Configuration (သင့်ရဲ့ GitHub Raw Link ကို ပြင်ရန်)
DB_URL = "https://raw.githubusercontent.com/heinminthant2022happy-bit/Test/refs/heads/main/database.txt"
LOCAL_DB = ".sys_auth.bin"

def get_device_id():
    # Android ID တောင်းရခက်ရင် ဖုန်းရဲ့ ပိုင်ရှင်အမည် သို့မဟုတ် hardware info နဲ့ အစားထိုးခြင်း
    try:
        # ပထမနည်းလမ်း- android_id ကို လှမ်းတောင်းမယ်
        import subprocess
        aid = subprocess.check_output("settings get secure android_id", shell=True).decode().strip()
    except:
        # ဒုတိယနည်းလမ်း- အပေါ်ကမရရင် Termux user ID ကို ယူမယ်
        aid = os.popen("whoami").read().strip() + "-001"
    
    unique_id = "TRB-" + hashlib.md5(aid.encode()).hexdigest()[:12].upper()
    return unique_id
    

def encrypt_data(data):
    return base64.b64encode(data.encode()).decode()

def decrypt_data(data):
    try: return base64.b64decode(data.encode()).decode()
    except: return ""

def check_online():
    try:
        r = requests.get(DB_URL, timeout=5)
        return r.text.splitlines() if r.status_code == 200 else None
    except:
        return None

def main_auth():
    os.system('clear')
    my_id = get_device_id()
    print(f"\033[0;36mDevice ID: {my_id}\033[00m")
    
    db_data = check_online()
    
    # Offline Check (ဖုန်းထဲက ဖိုင်ကိုစစ်ခြင်း)
    if os.path.exists(LOCAL_DB):
        with open(LOCAL_DB, "r") as f:
            saved = decrypt_data(f.read()).split("|")
            if len(saved) == 3:
                s_id, s_key, s_date = saved
                expire_dt = datetime.strptime(s_date, "%Y-%m-%d")
                
                # အကယ်၍ Online ရရင် GitHub နဲ့ တိုက်စစ်မယ်
                if db_data:
                    found = False
                    for line in db_data:
                        if f"{my_id}|{s_key}|{s_date}" == line:
                            found = True; break
                    if not found:
                        os.remove(LOCAL_DB)
                        print("\033[0;31m[!] Key Revoked or Changed by Admin.\033[00m")
                        time.sleep(2); return False

                # သက်တမ်းစစ်ခြင်း
                if expire_dt > datetime.now():
                    print(f"\033[0;32m[+] Welcome Back! Expire: {s_date}\033[00m")
                    return True
                else:
                    print("\033[0;31m[!] Key Expired.\033[00m")
                    os.remove(LOCAL_DB)

    # Key အသစ်တောင်းခြင်း
    if not db_data:
        print("\033[0;31m[!] No Internet Connection for First Login.\033[00m")
        return False

    u_key = input("\033[0;33mEnter Key: \033[00m").strip()
    for line in db_data:
        parts = line.split("|")
        if len(parts) == 3 and parts[0] == my_id and parts[1] == u_key:
            if datetime.strptime(parts[2], "%Y-%m-%d") > datetime.now():
                with open(LOCAL_DB, "w") as f:
                    f.write(encrypt_data(line))
                print("\033[0;32m[+] Login Successful!\033[00m")
                return True
    
    print("\033[0;31m[!] Invalid Key or Device ID.\033[00m")
    return False

if __name__ == "__main__":
    if main_auth():
        engine.run_script()
        
