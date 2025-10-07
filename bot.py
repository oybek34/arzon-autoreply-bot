import asyncio
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

import os

TOKEN = os.getenv("TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running successfully!"

async def start(update, context):
    await update.message.reply_text("Привет! Бот запущен и готов отвечать 😊")

async def echo(update, context):
    await update.message.reply_text(update.message.text)

async def run_bot():
    tg_app = ApplicationBuilder().token(TOKEN).build()
    tg_app.add_handler(CommandHandler("start", start))
    tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🤖 Bot started polling...")
    await tg_app.initialize()
    await tg_app.start()
    await tg_app.updater.start_polling()
    await asyncio.Event().wait()  # Держим бота запущенным бесконечно

if __name__ == "__main__":
    import threading

    # Запускаем Telegram-бот в отдельном потоке
    threading.Thread(target=lambda: asyncio.run(run_bot()), daemon=True).start()

    # Запускаем Flask-сервер для Render
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
