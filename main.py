import telebot
import google.generativeai as genai
import os
import http.server
import socketserver
import threading

# المفاتيح الخاصة بك
TELEGRAM_TOKEN = "8772903016:AAHAjzCH2iQ5mDH3OGVEsGE8LCPB9Zc0iXM"
GEMINI_API_KEY = "AIzaSyDO-EHfb083eyuC04B8r1duQY556sshUs8"

# سيرفر وهمي لإبقاء Render يعمل
def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# إعداد Gemini ببروتوكول أكثر مرونة
genai.configure(api_key=GEMINI_API_KEY)
# استخدمنا 1.5-flash لأنها تدعم مناطق جغرافية أوسع من النسخ القديمة
model = genai.GenerativeModel('gemini-1.5-flash') 
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # طلب الرد من جوجل
        response = model.generate_content(message.text)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "جوجل استلمت الرسالة لكنها لم توفر رداً نصياً، جرب جملة أخرى.")
            
    except Exception as e:
        # هنا البوت سيكتب لك سبب المشكلة بالضبط
        error_msg = str(e)
        if "location" in error_msg.lower():
            bot.reply_to(message, "⚠️ جوجل ترفض السيرفر بسبب الموقع الجغرافي. سأحاول إصلاح ذلك.")
        else:
            bot.reply_to(message, f"⚠️ الخطأ التقني هو: {error_msg[:100]}")

print("البوت ينطلق الآن...")
bot.infinity_polling()
