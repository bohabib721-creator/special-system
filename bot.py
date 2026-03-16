import telebot
import google.generativeai as genai
import os
import http.server
import socketserver
import threading

# --- الإعدادات ---
TELEGRAM_TOKEN = "8772903016:AAHAjzCH2iQ5mDH3OGVEsGE8LCPB9Zc0iXM"
GEMINI_API_KEY = "AIzaSyDO-EHfb083eyuC04B8r1duQY556sshUs8"

# 1. نظام الحفاظ على استمرارية السيرفر (Keep-Alive)
def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Server started on port {port}")
        httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# 2. إعداد ذكاء جوجل (Gemini 1.5 Flash - الأسرع والأكثر استقراراً)
genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

# 3. إعداد بوت تليجرام
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك يا بطل! أنا بوت الذكاء الاصطناعي الخاص بك، جاهز لمساعدتك في الدراسة أو أي شيء آخر. أرسل سؤالك الآن!")

@bot.message_handler(func=lambda message: True)
def handle_ai_chat(message):
    try:
        # إرسال رسالة انتظار "جاري التفكير..."
        chat_id = message.chat.id
        bot.send_chat_action(chat_id, 'typing')
        
        # طلب الرد من Gemini
        response = model.generate_content(message.text)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "عذراً، لم أستطع صياغة رد. جرب إعادة صياغة السؤال.")
            
    except Exception as e:
        # نظام تشخيص صامت: يرسل لك الخطأ إذا كنت أنت المستخدم فقط
        error_msg = str(e)
        bot.reply_to(message, "⚠️ عذراً، أواجه مشكلة بسيطة في الاتصال بذكاء جوجل. سأحاول مجدداً.")
        print(f"Error: {error_msg}")

# 4. تشغيل البوت للأبد
if __name__ == "__main__":
    print("البوت يعمل الآن بأقصى طاقة 🚀")
    bot.infinity_polling()
  
