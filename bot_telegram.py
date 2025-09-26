

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from datetime import datetime
from inference import predict, load_model

import gc
gc.collect()

from auth import get_auth

dict_auth = get_auth()
TELEGRAM_TOKEN, HF_TOKEN = dict_auth['tl_token'], dict_auth["hf_token"]
os.makedirs("pictures", exist_ok=True)

pipe = load_model()
default_message = "👋 Send me a description of character and the style. I'll generate an image! Styles examples: Makoto Shinkai, Hatsune Miku, Akira anime, Pop art anime, Shounen manga, Manga sketch"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(default_message)

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text(f"🎨 Generating image for: {prompt}")
    # Generate image
    image = predict(pipe, prompt) 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join("pictures", f"output_{timestamp}.png")
    image.save(file_path)
    await update.message.reply_photo(photo=open(file_path, "rb"))
    await update.message.reply_text(default_message)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    