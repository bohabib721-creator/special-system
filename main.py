import telebot
import google.generativeai as genai
import os
import http.server
import socketserver
import threading

# المفاتيح
TELEGRAM_TOKEN = "8772903016:AAHAjzCH2iQ5mDH3OGVEsGE8LCPB9Zc0iXM"
GEMINI_API_KEY = "AIzaSyDO-EHfb083eyuC04B8r1duQY556sshUs8"

# سيرفر وهمي
def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# إعداد Gemini - تغيير الموديل لنسخة أكثر توافقاً
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.0-pro') # جربنا 1.0 pro لأنه مستقر جداً
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # محاولة توليد المحتوى
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # إذا فشل، سنخبرك بالخطأ التقني الدقيق
        bot.reply_to(message, f"الخطأ هو: {str(e)[:100]}")

print("انطلاق البوت...")
bot.infinity_polling()
