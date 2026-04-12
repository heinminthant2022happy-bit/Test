import sys
import time
import os

# ၁။ engine.so ဖိုင်ရှိမရှိ စစ်ဆေးခြင်း
try:
    import engine
except ImportError:
    print("\033[0;31m[!] Error: engine.so ဖိုင်ကို မတွေ့ပါ။\033[00m")
    sys.exit(1)

# ၂။ သင်ကိုယ်တိုင် သတ်မှတ်ပေးမယ့် Access Keys များ
# ဒီနေရာမှာ သင်ပေးချင်တဲ့ Key တွေကို စာရင်းသွင်းထားပါ
ALLOWED_KEYS = ["ALADDIN-VIP-01", "HAPPY-BIT-99", "TEST-KEY"]

def check_license():
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\033[0;36m" + "="*45)
    print("   🚀 Aladdin Starlink Bypass - Admin Panel 🚀")
    print("="*45 + "\033[00m")
    
    # ဖုန်းရဲ့ Device ID ကို ထုတ်ပြခြင်း (User ဆီက Key တောင်းဖို့အတွက်)
    try:
        device_id = engine.get_system_key()
        print(f"\033[0;32m[*] Your Device ID: {device_id}\033[00m")
    except:
        pass

    print("-" * 45)
    user_key = input("\033[0;33m[?] Enter Access Key: \033[00m").strip()
    
    if user_key in ALLOWED_KEYS:
        print("\033[0;32m[+] Access Granted! Welcome.\033[00m")
        time.sleep(1.5)
        return True
    else:
        print("\033[0;31m[!] Invalid Key! ဆက်သွယ်ရန် - @Aladdin_Help_Bot\033[00m")
        time.sleep(2)
        return False

def main():
    try:
        # သင်ကိုယ်တိုင်လုပ်ထားတဲ့ License Check အရင်အောင်မြင်ရမယ်
        if check_license():
            # အောင်မြင်မှ .so ထဲက မူရင်း logic ကို run မယ်
            engine.run_script()
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\033[0;31m[!] Program ကို အသုံးပြုသူမှ ရပ်ဆိုင်းလိုက်ပါသည်။\033[00m")
        sys.exit(0)
        
    except Exception as e:
        # Error တက်ရင် ၁၀ စက္ကန့်နေရင် ပြန်စတင်မယ်
        print(f"\n\033[0;31m[!] Error: {e}\033[00m")
        print("\033[0;33m[*] ၁၀ စက္ကန့်အကြာတွင် အလိုအလျောက် ပြန်လည်စတင်ပါမည်...\033[00m")
        time.sleep(10)
        main()

if __name__ == "__main__":
    main()
  
