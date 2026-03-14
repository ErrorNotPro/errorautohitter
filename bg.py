import io
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from rembg import remove
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)

# --- CONFIGURATION ---
API_TOKEN = '8233339248:AAGsB-4sJyeHsHliL6jXAucsr864g7wOXkI'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.reply("Hi! Send me any photo, and I'll remove the background in seconds. ⚡")

@dp.message(types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    # Send a "processing" hint to the user
    status_msg = await message.answer("Processing... ⏳")
    
    try:
        # 1. Download photo to memory
        photo_io = io.BytesIO()
        file = await bot.get_file(message.photo[-1].file_id)
        await bot.download_file(file.file_path, photo_io)
        photo_io.seek(0)

        # 2. Run background removal in a separate thread to keep the bot responsive
        loop = asyncio.get_event_loop()
        output_io = await loop.run_in_executor(None, process_image, photo_io)

        # 3. Send the processed image back as a document (to preserve transparency)
        output_file = types.BufferedInputFile(output_io.getvalue(), filename="no_bg.png")
        await message.answer_document(output_file, caption="Done! ✅")
        
        # Clean up status message
        await status_msg.delete()

    except Exception as e:
        logging.error(f"Error: {e}")
        await status_msg.edit_text("Oops! Something went wrong while processing.")

def process_image(input_io):
    """Function to handle the heavy lifting of BG removal."""
    input_image = Image.open(input_io)
    # The 'remove' function handles the AI mask generation
    output_image = remove(input_image)
    
    output_io = io.BytesIO()
    output_image.save(output_io, format='PNG')
    output_io.seek(0)
    return output_io

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")