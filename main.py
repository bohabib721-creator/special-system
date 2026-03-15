import telebot
import google.generativeai as genai
import os

# --- إعدادات البوت ---
# ملاحظة: سنستخدم متغيرات البيئة لزيادة الأمان
CHROME_TOKEN = os.getenv("TELEGRAM_TOKEN") 
GEMINI_API_KEY = os.getenv("GEMINI_KEY")

# إعداد الذكاء الاصطناعي 🧠
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(CHROME_TOKEN)

# الرد على كلمات الشكر ⚪️
@bot.message_handler(func=lambda message: any(word in message.text.lower() for word in ['شكرا', 'صحيت', 'يعطيك الصحة']))
def handle_thanks(message):
    bot.reply_to(message, "العفو يا غالي! أنا كريم، مدريدي متعصب ⚪️ وفي الخدمة دائماً!")

# الرد العام باستخدام Gemini 🤖
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "أهلاً! تأكد من ضبط المفاتيح بشكل صحيح.")

print("البوت يعمل الآن...")
bot.infinity_polling()
