from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler

app = Flask(__name__)

BOT_TOKEN = "8637448255:AAGna6cWyBvrk3FrtfPKQob_tD607Y4MTMs"
CHANNEL_ID = "techpro_km"

async def start(update, context):
    user_id = update.effective_user.id
    member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
    if member.status in ["member", "administrator", "creator"]:
        keyboard = [
            [InlineKeyboardButton("🎵 WebApp ochish", web_app={"url": "https://yourproject.up.railway.app"})]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "✅ A'zolik tasdiqlandi! Endi WebApp’ni ochishingiz mumkin:",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("❌ Avval kanalga obuna bo‘ling: @your_channel")

# Yangi Application API
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))

# Webhook rejimi
application.run_webhook(
    listen="0.0.0.0",
    port=8080,
    url_path=BOT_TOKEN,
    webhook_url=f"https://yourproject.up.railway.app/{BOT_TOKEN}"
)

# Flask WebApp
@app.route("/")
def index():
    return "MUSIQA_TECH_BOT WebApp ishlayapti!"

