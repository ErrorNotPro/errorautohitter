import io
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from rembg import remove, new_session

# Log everything to the Railway console
logging.basicConfig(level=logging.INFO)

API_TOKEN = '8233339248:AAGsB-4sJyeHsHliL6jXAucsr864g7wOXkI'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
session = new_session("u2netp")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("🚀 Bot is Online! Send a photo now.")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    logging.info("📸 Photo received! Starting process...")
    status = await message.answer("⚡ Processing...")
    
    try:
        # Step 1: Download
        logging.info("Downloading photo from Telegram...")
        photo_bytes = io.BytesIO()
        file = await bot.get_file(message.photo[-1].file_id)
        await bot.download_file(file.file_path, photo_bytes)
        
        # Step 2: Process
        logging.info("Removing background (AI running)...")
        loop = asyncio.get_event_loop()
        input_data = photo_bytes.getvalue()
        # This is the line that usually crashes if RAM is low or libraries are missing
        output_data = await loop.run_in_executor(None, lambda: remove(input_data, session=session))

        # Step 3: Send
        logging.info("Sending result back to user...")
        final_file = types.BufferedInputFile(output_data, filename="no_bg.png")
        await message.answer_document(final_file, caption="✅ Background Removed!")
        await status.delete()
        logging.info("✅ Task Complete!")

    except Exception as e:
        logging.error(f"❌ CRASHED: {str(e)}")
        await message.answer(f"⚠️ Error: {str(e)}")

async def main():
    logging.info("Bot is starting up...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
