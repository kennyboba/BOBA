import os
import random
from random import choice
import requests
from user_agent import generate_user_agent
from hashlib import md5
from bs4 import BeautifulSoup
import base64
import secrets
import time
import string
import uuid
from datetime import datetime
import json
import asyncio

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    from cfonts import render
except ImportError:
    os.system("pip install python-telegram-bot==20.7 requests pyfiglet cfonts")
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

b = random.randint(5,208)
bo = f'\x1b[38;5;{b}m'
ED = '\x1b[38;5;208m'
BLUE = '\033[94m'
Z = '\033[1;31m' 
YELLOW = '\033[1;33m' 
J = '\033[2;36m'
N = '\033[1;37m'

def banner():
    print(f'''{J}
    
    
⚊⚊⚊⚊⚊⚊⚊⚊⚊⚊⚊⚊⚊⚊
İNSTAGRAM RESET TOOL BOT
⚊⚊⚊⚊⚊⚊⚊⚊⚊⚊⚊⚊⚊⚊
    
{J} 
''')

banner()

# Bot token from input
BOT_TOKEN = "8337686593:AAEcjEoxMRmg3VzbuUQUedG1KqKrEuxqkIE"

def generate_device_info():
    ANDROID_ID = f"android-{''.join(random.choices(string.hexdigits.lower(), k=16))}"
    USER_AGENT = f"Instagram 394.0.0.46.81 Android ({random.choice(['28/9','29/10','30/11','31/12'])}; {random.choice(['240dpi','320dpi','480dpi'])}; {random.choice(['720x1280','1080x1920','1440x2560'])}; {random.choice(['samsung','xiaomi','huawei','oneplus','google'])}; {random.choice(['SM-G975F','Mi-9T','P30-Pro','ONEPLUS-A6003','Pixel-4'])}; intel; en_US; {random.randint(100000000,999999999)})"
    WATERFALL_ID = str(uuid.uuid4())
    timestamp = int(datetime.now().timestamp())
    nums = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    PASSWORD = f'#PWD_INSTAGRAM:0:{timestamp}:Kennyboba@{nums}'
    return ANDROID_ID, USER_AGENT, WATERFALL_ID, PASSWORD

def acer(mid="", user_agent=""):
    return {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Bloks-Version-Id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
        "X-Mid": mid,
        "User-Agent": user_agent,
        "Content-Length": "9481"
    }

def id_user(user_id):
    try:
        url = f"https://i.instagram.com/api/v1/users/{user_id}/info/"
        headers = {
            "User-Agent": "Instagram 219.0.0.12.117 Android"
        }
        r = requests.get(url, headers=headers)
        try:
            username = r.json()["user"]["username"]
            return username
        except:
            return None
    except:
        return None        
    
def purna(reset_link):
    try:
        ANDROID_ID, USER_AGENT, WATERFALL_ID, PASSWORD = generate_device_info()
        
        if "uidb36=" not in reset_link or "token=" not in reset_link:
            return {"success": False, "error": "Invalid reset link format"}
        
        uidb36 = reset_link.split("uidb36=")[1].split("&token=")[0]
        token = reset_link.split("&token=")[1].split(":")[0]

        url = "https://i.instagram.com/api/v1/accounts/password_reset/"
        data = {
            "source": "one_click_login_email",
            "uidb36": uidb36,
            "device_id": ANDROID_ID,
            "token": token,
            "waterfall_id": WATERFALL_ID
        }
        r = requests.post(url, headers=acer(user_agent=USER_AGENT), data=data)
        
        if "user_id" not in r.text:
            return {"success": False, "error": "Invalid or expired reset link"}

        mid = r.headers.get("Ig-Set-X-Mid")
        resp_json = r.json()
        user_id = resp_json.get("user_id")
        cni = resp_json.get("cni")
        nonce_code = resp_json.get("nonce_code")
        challenge_context = resp_json.get("challenge_context")

        url2 = "https://i.instagram.com/api/v1/bloks/apps/com.instagram.challenge.navigation.take_challenge/"
        data2 = {
            "user_id": str(user_id),
            "cni": str(cni),
            "nonce_code": str(nonce_code),
            "bk_client_context": '{"bloks_version":"e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd","styles_id":"instagram"}',
            "challenge_context": str(challenge_context),
            "bloks_versioning_id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
            "get_challenge": "true"
        }
        r2 = requests.post(url2, headers=acer(mid, USER_AGENT), data=data2).text
        
        challenge_context_final = r2.replace('\\', '').split(f'(bk.action.i64.Const, {cni}), "')[1].split('", (bk.action.bool.Const, false)))')[0]

        data3 = {
            "is_caa": "False",
            "source": "",
            "uidb36": "",
            "error_state": {"type_name":"str","index":0,"state_id":1048583541},
            "afv": "",
            "cni": str(cni),
            "token": "",
            "has_follow_up_screens": "0",
            "bk_client_context": {"bloks_version":"e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd","styles_id":"instagram"},
            "challenge_context": challenge_context_final,
            "bloks_versioning_id": "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd",
            "enc_new_password1": PASSWORD,
            "enc_new_password2": PASSWORD
        }
        
        requests.post(url2, headers=acer(mid, USER_AGENT), data=data3)
        new_password = PASSWORD.split(":")[-1]
        
        username = id_user(user_id)
        
        return {
            "success": True,
            "password": new_password,
            "username": username if username else "Unknown",
            "user_id": user_id
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# Telegram Bot Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = """
🤖 *Instagram Password Reset Bot*

Send me an Instagram password reset link and I'll reset the password for you!

*New Password Format:* `Kennyboba@XXXX` (where X is random numbers)

*How to use:*
Simply send me the reset link you received via email

*Example:*
`https://www.instagram.com/accounts/password/reset/?uidb36=...&token=...`

*Note:* Link must be valid and not expired
"""
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_msg = """
*Commands:*
/start - Start the bot
/help - Show this help message

*How to get a reset link:*
1. Go to Instagram login page
2. Click "Forgot password"
3. Enter the username/email
4. Check your email for the reset link
5. Copy the full link and send it here
"""
    await update.message.reply_text(help_msg, parse_mode='Markdown')

async def handle_reset_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    reset_link = update.message.text.strip()
    
    # Validate if it looks like an Instagram reset link
    if "instagram.com" not in reset_link or "password/reset" not in reset_link:
        await update.message.reply_text("❌ Please send a valid Instagram password reset link")
        return
    
    processing_msg = await update.message.reply_text("🔄 Processing your reset link... This may take a few seconds...")
    
    # Process the reset link
    result = purna(reset_link)
    
    if result.get("success"):
        success_msg = f"""
✅ *Password Reset Successful!*

📱 *Username:* {result['username']}
🔑 *New Password:* `{result['password']}`
🆔 *User ID:* {result['user_id']}

⚠️ *Important:* 
• Use this password to login to Instagram
• Change the password after login for security
• Keep this password safe

💡 *Tip:* Use the new password to login at instagram.com
"""
        await processing_msg.edit_text(success_msg, parse_mode='Markdown')
    else:
        error_msg = f"""
❌ *Password Reset Failed!*

Error: {result.get('error', 'Unknown error occurred')}

Possible reasons:
• Link has expired
• Link is invalid
• Link has already been used
• Instagram is blocking the request

Please try with a fresh reset link.
"""
        await processing_msg.edit_text(error_msg, parse_mode='Markdown')

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Error: {context.error}")
    if update and update.message:
        await update.message.reply_text("❌ An error occurred. Please try again later.")

def main():
    print("🤖 Starting Instagram Reset Bot...")
    print(f"Bot Token: {BOT_TOKEN[:10]}...")
    
    # Create application with specific version
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reset_link))
    application.add_error_handler(error_handler)
    
    print("✅ Bot is running! Press Ctrl+C to stop.")
    print("📱 Find your bot on Telegram and send /start")
    print(f"🤖 Bot username: @your_bot_username")
    
    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    # First, reinstall the correct version
    os.system("pip uninstall python-telegram-bot -y")
    os.system("pip install python-telegram-bot==20.7")
    
    # Wait a moment for installation
    time.sleep(2)
    
    # Run the main function
    main()