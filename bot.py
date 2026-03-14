import io
import asyncio
import time
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from rembg import remove, new_session

# --- CONFIG ---
API_TOKEN = '8233339248:AAGsB-4sJyeHsHliL6jXAucsr864g7wOXkI'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Pre-loading the session once globally to keep it in RAM
# 'u2netp' is the "Fast" version of the u2net model
session = new_session("u2netp")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("🚀 **High-Speed BG Remover Active!**\nSend a photo for 1-3 second processing.")

@dp.message(F.photo)
async def on_photo(message: types.Message):
    start_time = time.time()
    status = await message.answer("⚡ *Processing...*", parse_mode="Markdown")
    
    try:
        # 1. Download to memory
        photo_bytes = io.BytesIO()
        file = await bot.get_file(message.photo[-1].file_id)
        await bot.download_file(file.file_path, photo_bytes)
        
        # 2. Process background (Running in thread pool to keep bot alive)
        loop = asyncio.get_event_loop()
        input_data = photo_bytes.getvalue()
        output_data = await loop.run_in_executor(None, lambda: remove(input_data, session=session))

        # 3. Calculate speed
        end_time = round(time.time() - start_time, 2)

        # 4. Upload result
        final_file = types.BufferedInputFile(output_data, filename="no_bg.png")
        await message.answer_document(
            final_file, 
            caption=f"✅ **Done in {end_time}s**", 
            parse_mode="Markdown"
        )
        
        await status.delete()

    except Exception as e:
        await status.edit_text(f"❌ **Error:** {str(e)}")

async def main():
    print("Bot is live and pre-loaded!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
