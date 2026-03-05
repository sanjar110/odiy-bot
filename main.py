import os
import asyncio
import logging
import yt_dlp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
    CallbackQuery,
)

# ================== CONFIG ==================
TOKEN = "8637448255:AAGna6cWyBvrk3FrtfPKQob_tD607Y4MTMs"
CHANNEL = "@techpro_km"
# ============================================

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

search_cache = {}  # vaqtinchalik saqlash

# ================== SUB CHECK ==================
async def check_subscription(user_id: int) -> bool:
    try:
        chat = await bot.get_chat(CHANNEL)
        member = await bot.get_chat_member(chat.id, user_id)
        return member.status in ("member", "administrator", "creator")
    except:
        return False


def sub_keyboard():
    if str(CHANNEL).startswith("@"):
        url = f"https://t.me/{CHANNEL.replace('@','')}"
    else:
        url = "https://t.me/"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url=url)],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]
        ]
    )

# ================== START ==================
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    if not await check_subscription(message.from_user.id):
        await message.answer(
            "❗ Avval kanalga obuna bo‘ling.",
            reply_markup=sub_keyboard()
        )
        return

    await message.answer("🎵 Artist yoki qo‘shiq nomini yozing.")

# ================== SEARCH ==================
def search_youtube(query: str):
    ydl_opts = {"quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch10:{query}", download=False)
        return info["entries"]

@dp.message()
async def search_handler(message: types.Message):
    if not await check_subscription(message.from_user.id):
        await message.answer(
            "❗ Avval kanalga obuna bo‘ling.",
            reply_markup=sub_keyboard()
        )
        return

    msg = await message.answer("🔎 Qidirilmoqda...")

    try:
        results = search_youtube(message.text)

        if not results:
            await msg.edit_text("❌ Hech narsa topilmadi.")
            return

        search_cache[message.from_user.id] = results

        buttons = []
        for i, video in enumerate(results):
            title = video["title"][:40]
            buttons.append(
                [InlineKeyboardButton(
                    text=f"{i+1}. {title}",
                    callback_data=f"dl_{i}"
                )]
            )

        kb = InlineKeyboardMarkup(inline_keyboard=buttons)

        await msg.edit_text("🎧 Top 10 natija:", reply_markup=kb)

    except Exception as e:
        print(e)
        await msg.edit_text("❌ Xatolik yuz berdi.")

# ================== DOWNLOAD ==================
def download_audio(url: str):
    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return os.path.splitext(filename)[0] + ".mp3"


# ================== CALLBACK DOWNLOAD ==================
@dp.callback_query(F.data.startswith("dl_"))
async def download_callback(callback: CallbackQuery):
    index = int(callback.data.split("_")[1])

    results = search_cache.get(callback.from_user.id)

    if not results:
        await callback.answer("❌ Vaqt tugadi. Qayta qidiring.", show_alert=True)
        return

    video = results[index]
    url = video["webpage_url"]

    await callback.message.edit_text("⬇ Yuklanmoqda...")

    try:
        file_path = download_audio(url)

        await callback.message.answer_audio(
            FSInputFile(file_path),
            caption="✅ Yuklab olindi"
        )

        os.remove(file_path)

    except Exception as e:
        print(e)
        await callback.message.answer("❌ Yuklashda xatolik.")

# ================== RUN ==================
async def main():
    me = await bot.get_me()
    print(f"🚀 Bot ishga tushdi: @{me.username}")
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
