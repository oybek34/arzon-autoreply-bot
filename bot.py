import os
import asyncio
import pytz
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from flask import Flask

# Фейковый сервер, чтобы Render не завершал процесс
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is running ✅"

# Запуск Flask-сервера
def run_web():
    app_web.run(host="0.0.0.0", port=10000)

# Telegram токен
TOKEN = os.getenv("TOKEN")

# Часовой пояс Ташкент
tz = pytz.timezone("Asia/Tashkent")

async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now(tz)
    hour = now.hour

    if 10 <= hour < 21:
        reply_text = (
            "👋 Assalomu Aleykum Hurmatli mijoz 😊, "
            "Siz Arzon.Gadjet ga murojaat qildingiz, sizga tez orada javob beramiz 💬\n"
            "➖➖➖\n"
            "👋 Здравствуйте! Спасибо за сообщение 😊\n"
            "Мы сейчас на связи и ответим вам в ближайшее время 💬"
        )
    else:
        reply_text = (
            "👋 Assalomu Aleykum Hurmatli mijoz 😊, "
            "Siz Arzon.Gadjet ga murojaat qildingiz, Afsus bizning ish vaqtimiz tugadi 😮‍💨,\n"
            "⏰ Soat 10:00 dan 21:00 gacha aloqadamiz. Agar savolingiz bo'lsa qoldiring biz albatta javob beramiz 😊\n"
            "➖➖➖\n"
            "🌙 Добрый вечер!\n"
            "Наш график: с 10:00 до 21:00 🕙\n"
            "Сейчас мы уже не работаем, но обязательно ответим вам утром 💬"
        )

    await update.message.reply_text(reply_text)

async def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, auto_reply))
    print("🤖 Bot started successfully!")
    await app.run_polling()

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_web).start()
    asyncio.run(run_bot())
