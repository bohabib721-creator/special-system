import telebot
import google.generativeai as genai
import os
import http.server
import socketserver
import threading

# المفاتيح الرسمية الخاصة بك يا كريم
TELEGRAM_TOKEN = "8772903016:AAHAjzCH2iQ5mDH3OGVEsGE8LCPB9Zc0iXM"
GEMINI_API_KEY = "AIzaSyDO-EHfb083eyuC04B8r1duQY556sshUs8"

# تشغيل سيرفر وهمي لتجاوز قيود موقع Render
def run_dummy_server():
    try:
        port = int(os.environ.get("PORT", 8080))
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", port), handler) as httpd:
            httpd.serve_forever()
    except Exception:
        pass

threading.Thread(target=run_dummy_server, daemon=True).start()

# إعداد ذكاء Gemini (استخدام نسخة Flash الأسرع)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # إرسال الرسالة لذكاء جوجل وتلقي الرد
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # البوت سيخبرك بالخطأ الحقيقي إذا فشل الاتصال بجوجل
        bot.reply_to(message, f"⚠️ عذراً كريم، حدث خطأ: {str(e)[:100]}")

print("جاري تشغيل البوت...")
bot.infinity_polling()
