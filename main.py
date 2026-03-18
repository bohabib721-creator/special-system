import telebot
import google.generativeai as genai
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# --- الإعدادات النهائية ---
# التوكن والمفتاح النرويجي الجديد
TELEGRAM_TOKEN = "8772903016:AAHAjzCH2iQ5mDH3OGVEsGE8LCPB9Zc0iXM"
GEMINI_API_KEY = "AIzaSyCWAvbKY86oLY4UNGvDg2sPVOIbX6MtOvI"

# 1. نظام الحفاظ على استمرارية السيرفر (Port 8080)
def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('', port), SimpleHTTPRequestHandler)
    print(f"Health check server started on port {port}")
    server.serve_forever()

threading.Thread(target=run_health_check, daemon=True).start()

# 2. إعداد ذكاء جوجل (Gemini 1.5 Flash)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. إعداد بوت تليجرام
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = "مرحباً يا كريم! 🌟\nالبوت الآن يعمل بنجاح باستخدام المفتاح الجديد.\nأنا جاهز لمساعدتك في دروس الباكالوريا أو أي سؤال آخر. أرسل سؤالك الآن!"
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_chat(message):
    try:
        # إظهار أن البوت "يكتب الآن" ليعطي لمسة احترافية
        bot.send_chat_action(message.chat.id, 'typing')
        
        # طلب الرد من Gemini
        response = model.generate_content(message.text)
        
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "⚠️ استلمت الطلب ولكن لم أستطع صياغة رد مناسب. حاول مرة أخرى.")
            
    except Exception as e:
        print(f"Error occurred: {e}")
        bot.reply_to(message, "⚠️ عذراً، هناك ضغط على الخدمة حالياً. سأحاول مجدداً بعد قليل.")

# 4. تشغيل البوت مع خاصية عدم التوقف (Infinity Polling)
if __name__ == "__main__":
    print("البوت انطلق بنجاح... اذهب لتليجرام وجربه!")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
