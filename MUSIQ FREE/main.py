import os
import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

search_results = {}

# Kanal klaviaturasi
def sub_keyboard():

    if str(CHANNEL).startswith("@"):
        link = f"https://t.me/{CHANNEL[1:]}"
    else:
        link = CHANNEL

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga obuna", url=link)],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]
        ]
    )

    return keyboard


# Obuna tekshirish
async def check_sub(user_id):

    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member","administrator","creator"]
    except:
        return False


# START
@dp.message(CommandStart())
async def start_handler(message: types.Message):

    if not await check_sub(message.from_user.id):
        await message.answer(
            "❗ Botdan foydalanish uchun kanalga obuna bo‘ling",
            reply_markup=sub_keyboard()
        )
        return

    await message.answer(
        "🎧 Qo‘shiq nomi yoki artist yozing"
    )


# Obuna tekshirish tugmasi
@dp.callback_query(F.data == "check_sub")
async def check_handler(callback: types.CallbackQuery):

    if await check_sub(callback.from_user.id):
        await callback.message.edit_text("✅ Obuna tasdiqlandi\n\n🎧 Qo‘shiq nomi yozing")
    else:
        await callback.answer("❌ Avval kanalga obuna bo‘ling", show_alert=True)


# Qidiruv
@dp.message()
async def search_handler(message: types.Message):

    if not await check_sub(message.from_user.id):
        await message.answer(
            "❗ Kanalga obuna bo‘ling",
            reply_markup=sub_keyboard()
        )
        return

    query = message.text

    await message.answer("🔎 Qidirilmoqda...")

    ydl_opts = {
        'quiet': True,
        'extract_flat': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch10:{query}", download=False)

    results = info['entries']

    search_results[message.from_user.id] = results

    kb = InlineKeyboardBuilder()

    for i, video in enumerate(results):
        kb.button(
            text=f"{i+1}. {video['title'][:40]}",
            callback_data=f"music_{i}"
        )

    kb.adjust(1)

    await message.answer(
        "🎵 Topilgan qo‘shiqlar:",
        reply_markup=kb.as_markup()
    )


# Qo‘shiq tanlash
@dp.callback_query(F.data.startswith("music_"))
async def music_handler(callback: types.CallbackQuery):

    index = int(callback.data.split("_")[1])

    video = search_results[callback.from_user.id][index]

    url = f"https://youtube.com/watch?v={video['id']}"

    await callback.message.answer("⬇️ Yuklanmoqda...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    for file in os.listdir():
        if file.startswith("music"):
            await bot.send_audio(
                callback.from_user.id,
                audio=types.FSInputFile(file),
                title=video['title']
            )
            os.remove(file)
            break


# Botni ishga tushirish
async def main():
    print("🚀 Bot ishga tushdi")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())