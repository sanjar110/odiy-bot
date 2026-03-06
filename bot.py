from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler

app = Flask(__name__)

BOT_TOKEN = "8637448255:AAGna6cWyBvrk3FrtfPKQob_tD607Y4MTMs"
CHANNEL_ID = "techpro_km"

def start(update, context):
    user_id = update.effective_user.id
    member = context.bot.get_chat_member(CHANNEL_ID, user_id)
    if member.status in ["member", "administrator", "creator"]:
        # WebApp tugmasi
        keyboard = [
            [InlineKeyboardButton("🎵 WebApp ochish", web_app={"url": "https://yourproject.up.railway.app"})]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("✅ A'zolik tasdiqlandi! Endi WebApp’ni ochishingiz mumkin:", reply_markup=reply_markup)
    else:
        update.message.reply_text("❌ Avval kanalga obuna bo‘ling: @your_channel")

# Botni ishga tushirish
updater = Updater(BOT_TOKEN)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()

# Flask WebApp
@app.route("/")
def index():
    return "MUSIQA_TECH_BOT WebApp ishlayapti!"
