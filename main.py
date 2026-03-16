import telebot
import google.generativeai as genai
import os
import http.server
import socketserver
import threading

# المفاتيح الخاصة بك - تأكد أنها صحيحة 100%
TELEGRAM_TOKEN = "8772903016:AAHAjzCH2iQ5mDH3OGVEsGE8LCPB9Zc0iXM"
GEMINI_API_KEY = "AIzaSyDO-EHfb083eyuC04B8r1duQY556sshUs8"

# سيرفر وهمي صغير جداً لإرضاء Render
def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# إعدادات Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # محاولة طلب الرد من الذكاء الاصطناعي
        response = model.generate_content(message.text)
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "⚠️ تم الاتصال بجوجل ولكن لم يتم إنشاء نص.")
    except Exception as e:
        # هنا البوت سيكتب لك الخطأ "بالحرف الواحد"
        error_info = str(e)
        bot.reply_to(message, f"❌ كود الخطأ الحقيقي هو: \n{error_info}")

print("جاري تشغيل نظام التشخيص...")
bot.infinity_polling
