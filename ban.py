import smtplib
import getpass
import time
import re
import os
import random
import requests
from itertools import cycle
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import Fore, Style, init

init(autoreset=True)

# ===== Tool login =====
tool_username = "admin"
tool_password = "admins"

# ===== Your personal Gmail credentials =====
gmail_accounts = [
    {"email": "managerhimself032@gmail.com", "password": "inagtgypnpyweleu"},
    {"email": "arsheeqarsheeqq@gmail.com", "password": "pkkqfactxwkpvzgc"},
    {"email": "unknownhimself6@gmail.com", "password": "uupfjdufriwrdgop"},
    {"email": "cryptolord25ss@gmail.com", "password": "lczszqjxovvbuxco"},
    {"email": "himselfdev759@gmail.com", "password": "fpwncioanqohseix"},
]

# rotate accounts automatically
account_cycle = cycle(gmail_accounts)

# ===== WhatsApp Business API credentials =====
ACCESS_TOKEN = "EAAJgi17vyDYBPTGf8m4LNp0xFdUozhBKS6PTnrElQdSZCIRZCnuLFmBigzRvB4ZCUI8EBNuNZCFZBfG5e11ehZBujToi9S6zYQ3HSmDZBPNQHZBFFrd3ntSZAl6lRZAOa86mOZCp60VaaCMhgUN6s68EEvYSEJXlaIk9iiB7xe1rlZBKbEVf7YiIADUZA0kHuO9nr0QZDZD"
PHONE_NUMBER_ID = "669101662914614"

# ===== WhatsApp support emails (expanded list) =====
support_emails = [
    "support@support.whatsapp.com",
    "appeals@support.whatsapp.com",
    "android_web@support.whatsapp.com",
    "ios_web@support.whatsapp.com",
    "webclient_web@support.whatsapp.com",
    "1483635209301664@support.whatsapp.com",
    "support@whatsapp.com",
    "businesscomplaints@support.whatsapp.com",
    "abuse@support.whatsapp.com",
    "security@support.whatsapp.com"
] * 11  # send multiple copies

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def typewriter(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

def check_whatsapp_number(phone):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/contacts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "blocking": "wait",
        "contacts": [phone],
        "force_check": True
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
    except Exception as e:
        print(Fore.RED + f"\n⚠️ Request failed: {e}\n")
        return

    if response.status_code == 200:
        data = response.json()
        for contact in data.get("contacts", []):
            status = contact.get("status", "unknown")
            wa_id = contact.get("wa_id", "N/A")
            print(Fore.GREEN + f"\n✅ Number: {wa_id} is {str(status).upper()} on WhatsApp.\n")
        if not data.get("contacts"):
            print(Fore.RED + "\n❌ Number is not registered on WhatsApp.\n")
    else:
        print(Fore.RED + "\n⚠️ Failed to check number.\n")
        try:
            print(response.text)
        except Exception:
            pass

# ===== Email Sender Helper =====
def send_email(subject, body, max_emails=None):
    """
    Sends the given subject/body to every address in support_emails using rotating gmail_accounts.
    Returns (success_count, fail_count)
    """
    success = 0
    fail = 0

    # pick next account from cycle
    account = next(account_cycle)
    your_email = account["email"]
    your_app_password = account["password"]

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(your_email, your_app_password)
    except Exception as e:
        print(Fore.RED + f"\n❌ SMTP login failed for {your_email}: {e}\n")
        return (0, len(support_emails))

    total = len(support_emails) if max_emails is None else min(len(support_emails), max_emails)
    for i, email in enumerate(support_emails[:total], 1):
        try:
            msg = MIMEMultipart()
            msg['From'] = your_email
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server.send_message(msg)
            success += 1
            print(Fore.GREEN + f"   [{i}/{total}] Sent to {email} ✅")
            time.sleep(0.2)
        except Exception as e:
            fail += 1
            print(Fore.RED + f"   [{i}/{total}] Failed to send to {email}: {e}")
            time.sleep(0.2)

    try:
        server.quit()
    except Exception:
        pass

    return (success, fail)

# ===== Login screen =====
while True:
    banner_color = random.choice([Fore.GREEN, Fore.CYAN, Fore.MAGENTA])
    print(banner_color + "📲 Welcome to WhatsApp Unban Tool")

    # Banner art
    print(banner_color + r'''
⠛⠛⣿⣿⣿⣿⣿⡷⢶⣦⣶⣶⣤⣤⣤⣀⠀⠀⠀
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀
⠀⠀⠀⠉⠉⠉⠙⠻⣿⣿⠿⠿⠛⠛⠛⠻⣿⣿⣇⠀
⠀⠀⢤⣀⣀⣀⠀⠀⢸⣷⡄⠀⣁⣀⣤⣴⣿⣿⣿⣆
⠀⠀⠀⠀⠹⠏⠀⠀⠀⣿⣧⠀⠹⣿⣿⣿⣿⣿⡿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠿⠇⢀⣼⣿⣿⠛⢯⡿⡟
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠦⠴⢿⢿⣿⡿⠷⠀⣿⠀
⠀⠀⠀⠀⠀⠀⠀⠙⣷⣶⣶⣤⣤⣤⣤⣤⣶⣦⠃⠀
⠀⠀⠀⠀⠀⠀⠀⢐⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⠟
''')

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    username = input("👤 Enter Username: ")
    password = getpass.getpass("🔒 Enter Password: ")

    if username == tool_username and password == tool_password:
        print(Fore.GREEN + "\n✅ Login successful!")

        # Banner art (on successful login)
        print(banner_color + r'''
⠛⠛⣿⣿⣿⣿⣿⡷⢶⣦⣶⣶⣤⣤⣤⣀⠀⠀⠀
⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀
⠀⠀⠀⠉⠉⠉⠙⠻⣿⣿⠿⠿⠛⠛⠛⠻⣿⣿⣇⠀
⠀⠀⢤⣀⣀⣀⠀⠀⢸⣷⡄⠀⣁⣀⣤⣴⣿⣿⣿⣆
⠀⠀⠀⠀⠹⠏⠀⠀⠀⣿⣧⠀⠹⣿⣿⣿⣿⣿⡿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠿⠇⢀⣼⣿⣿⠛⢯⡿⡟
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠦⠴⢿⢿⣿⡿⠷⠀⣿⠀
⠀⠀⠀⠀⠀⠀⠀⠙⣷⣶⣶⣤⣤⣤⣤⣤⣶⣦⠃⠀
⠀⠀⠀⠀⠀⠀⠀⢐⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⠟
''')
        typewriter(Fore.YELLOW + "This tool was made by Crypto Lord alone.\n", delay=0.06)
        break
    else:
        print(Fore.RED + "\n❌ Incorrect credentials, try again...")
        time.sleep(2)

# ===== Main Menu =====
while True:
    clear()
    menu_color = random.choice([Fore.BLUE, Fore.YELLOW, Fore.CYAN])
    print(menu_color + "🛠️ WhatsApp Tool - Main Menu")
    print(menu_color + r'''
⠀⠀⠀    ⣠⣶⣶⣶⣶
⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣴⣶⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣧
⠀⠀⠀⠀⣼⣿⣿⣿⡿⣿⣿⣆⠀⠀⠀⠀⠀⠀⣠⣴⣶⣤⡀⠀
⠀⠀⠀⢰⣿⣿⣿⣿⠃⠈⢻⣿⣦⠀⠀⠀⠀⣸⣿⣿⣿⣿⣷⠀
⠀⠀⠀⠘⣿⣿⣿⡏⣴⣿⣷⣝⢿⣷⢀⠀⢀⣿⣿⣿⣿⡿⠋⠀
⠀⠀⠀⠀⢿⣿⣿⡇⢻⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⣿⣇⢸⣿⣿⡟⠙⠛⠻⣿⣿⣿⣿⡇⠀⠀⠀⠀
⣴⣿⣿⣿⣿⣿⣿⣿⣠⣿⣿⡇⠀⠀⠀⠉⠛⣽⣿⣇⣀⣀⣀⠀
⠙⠻⠿⠿⠿⠿⠿⠟⠿⠿⠿⠇⠀⠀⠀⠀⠀⠻⠿⠿⠛⠛⠛
''')
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(menu_color + " [1] 📩 Unban Temporary")
    print(menu_color + " [2] 🚫 Unban Permanent")
    print(menu_color + " [3] 🔍 Check WhatsApp Number Status")
    print(menu_color + " [4] ⚠️ Report Fraud/Scam Number")
    print(menu_color + " [5] 💀 Report Hard (Strong Fraud Report)")
    print(menu_color + " [0] ❌ Exit")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    choice = input(Fore.CYAN + "\n📥 Select an option: ").strip()

    if choice in ["1", "2"]:
        unban_type = "Temporary" if choice == "1" else "Permanent"
        clear()
        print(menu_color + f"🔄 Unban {unban_type} Selected\n")

        while True:
            phone = input("📞 Enter WhatsApp number with country code (e.g., +2348123456789): ").strip()
            if re.match(r"^\+\d{10,15}$", phone):
                break
            else:
                print(Fore.RED + "❌ Invalid format! Only numbers allowed with country code starting with +.")
                time.sleep(1)

        print(f"\n📝 Sending {unban_type} unban request for {phone}...")
        time.sleep(1)

        if unban_type == "Temporary":
            subject = "Humble Request for Temporary Lift of WhatsApp Account Ban"
            body = f"""

Dear WhatsApp Appeals Team,

I hope this message finds you well.

I am writing with deep respect and concern regarding the ban placed on my WhatsApp account associated with the phone number {phone}. I understand the importance of maintaining a safe and positive community, and I fully support your efforts.

However, I kindly believe this ban may have resulted from a misunderstanding or an unintentional error. WhatsApp is essential for my daily communication with family, friends, and work, and I am sincerely committed to following all community guidelines moving forward.

Phone Number: {phone}
WhatsApp Version: 2.25.21.82

I humbly request that you consider temporarily lifting the ban on my account to allow me the opportunity to demonstrate responsible use and compliance with your policies. If any issues remain, I would be grateful for guidance so I can fully address them.

Thank you very much for your understanding and consideration. I deeply appreciate your time and support.

With sincere gratitude.
"""
        else:
            subject = "Humble Request for Reconsideration Permanent Unban of WhatsApp Number Due to Violation"
            body = f"""
            
Dear WhatsApp  Team,

I hope you are doing well.

I am reaching out with a heavy heart regarding the permanent ban on my WhatsApp account linked to the phone number {phone}. I was deeply saddened to learn about this restriction and genuinely believe there might have been a misunderstanding or an unintentional mistake on my part. I acknowledge the mistake and sincerely apologize for any inconvenience caused. I assure you that I understand the importance of adhering to the platform's guidelines and am committed to using WhatsApp responsibly in the future. I kindly ask for your understanding and consideration in granting me a second chance to regain access to my account. 
Phone Number: {phone}
WhatsApp is incredibly important to me—it connects me with my loved ones, friends, and colleagues daily. I truly respect the rules and community guidelines set forth by your team, and if I have unknowingly violated any, I sincerely apologize. Please know that it was never my intention to cause any harm or disruption. 
I humbly ask for your kindness and understanding in reviewing my case. If given the chance, I commit to strictly adhering to all policies moving forward and ensuring that my usage aligns fully with your standards.
Thank you very much for your time, patience, and consideration. I would be extremely grateful for the opportunity to regain access to my account.
With sincere gratitude.
"""

        # Use the helper to send emails (rotates accounts automatically)
        success, fail = send_email(subject, body)
        total_sent = success
        if total_sent > 0:
            print(Fore.GREEN + f"\n🎉 SUCCESS: {unban_type} unban request submitted to {total_sent} addresses.")
            print("📡 Stay active while WhatsApp reviews your request.\n")
        else:
            print(Fore.RED + "\n❌ Failed to send unban request. Check SMTP credentials and network.\n")

        input(Fore.CYAN + "\n🔁 Press Enter to return to menu...")

    elif choice == "3":
        clear()
        print(menu_color + "🔍 Check WhatsApp Number Status\n")
        phone = input("📞 Enter the WhatsApp number (e.g., +2348123456789): ")
        print("\n⏳ Checking number...")
        time.sleep(1.5)
        check_whatsapp_number(phone)
        input(Fore.CYAN + "\n🔁 Press Enter to return to menu...")

    elif choice == "4":
        target = input("📞 Enter fraud/scam number: ").strip()
        confirm = input(f"⚠️ Are you sure to report {target}? (y/n): ").lower()
        if confirm == "y":
            print(Fore.YELLOW + "🚨 Reporting in progress please wait...")
            subject = f"Report Fraud Number {target}"
            body = f"""Dear WhatsApp Support,  
I want to report this number: {target}.  
This number is involved in scam/fraudulent activities.  
Please investigate and take action."""
            success, fail = send_email(subject, body)
            if success > 0:
                print(Fore.GREEN + f"\n✅ Report done successful on target {target}.\nCheck after 2/3 min, if not banned try again.")
            else:
                print(Fore.RED + "\n❌ Failed to send report. Check credentials/network.")
        input(Fore.CYAN + "\n🔁 Press Enter to return to menu...")

    elif choice == "5":
        target = input("📞 Enter fraud/scam number: ").strip()
        confirm = input(f"⚠️ Confirm HARD REPORT on {target}? (y/n): ").lower()
        if confirm == "y":
            print(Fore.RED + "💀 Sending strong fraud report...")
            subject = f"URGENT: Strong Fraud Report {target}"
            body = f"""Dear WhatsApp Support Team,  

This number {target} is being used for **serious abuse, fraud, impersonation, and criminal scam operations**.  
This account is extremely dangerous and poses a **major threat to user safety and security**.  

It is **repeatedly violating your Terms of Service and community standards**.  
Leaving this number active will only allow it to deceive and harm more victims.  

This is a **critical abuse report**. The account linked to +{target} is involved in **extreme misconduct, harassment, impersonation, and fraud**, actively spreading harmful and criminal activity.  
The user is **deceiving people by falsely claiming to be the son of Mark Zuckerberg** in order to scam and trick victims into believing false promises and fraudulent schemes.  
This is a **clear case of impersonation and severe abuse**.  

Failure to act immediately allows this dangerous number to continue targeting innocent users.  

Details:  
• Fraudster’s Number: +{target}  
• Description: This number is impersonating, scamming, and deceiving people by pretending to be Mark Zuckerberg’s son, using false claims to defraud victims.  
• Evidence: (Screenshots, chat logs, or proof can be attached if needed.)  

I **demand immediate and permanent suspension** of this account to protect WhatsApp users.  
Your urgent action is required — **do not delay**.  

Thank you for your quick response and support.  

Sincerely,  
A concerned user"""
            success, fail = send_email(subject, body)
            if success > 0:
                print(Fore.GREEN + f"\n✅ HARD REPORT sent successful on target {target}.\nCheck after 2/3 min, retry if needed.")
            else:
                print(Fore.RED + "\n❌ Failed to send HARD REPORT. Check credentials/network.")
    elif choice == "0":
        print(Fore.YELLOW + "\n👋 Goodbye!")
        break

    else:
        print(Fore.RED + "\n❌ Invalid choice.")
        time.sleep(2)
