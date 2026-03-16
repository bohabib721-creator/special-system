import telebot
import google.generativeai as genai
import os
import http.server
import socketserver
import threading

# المفاتيح (تأكد من عدم وجود مسافات)
TELEGRAM_TOKEN = "8772903016:AAHAjzCH2iQ5mDH3OGVEsGE8LCPB9Zc0iXM"
GEMINI_API_KEY = "AIzaSyDO-EHfb083eyuC04B8r1duQY556sshUs8"

# سيرفر وهمي بسيط جداً
def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = http.server.HTTPServer(('', port), http.server.SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# إعدادات Gemini
genai.configure(api_key=GEMINI_API_KEY)
# استخدمنا موديل 1.5-flash لأنه الأكثر مرونة حالياً
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # محاولة طلب الرد
        response = model.generate_content(message.text)
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "تم الاتصال بجوجل ولكن لم يتم إنشاء نص. جرب سؤالاً آخر.")
    except Exception as e:
        # هذه الرسالة هي الأهم، انسخها لي إذا ظهرت
        error_detail = str(e)
        bot.reply_to(message, f"❌ خطأ تقني محدد: {error_detail}")

print("جاري الفحص والتشغيل...")
bot.infinity_polling()
