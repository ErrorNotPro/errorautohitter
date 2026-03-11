from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

router = Router()

ALLOWED_GROUP = -1002190350051
OWNER_ID = 6181269269

def check_access(msg: Message) -> bool:
    if msg.chat.id == ALLOWED_GROUP:
        return True
    if msg.chat.type == "private" and msg.from_user.id == OWNER_ID:
        return True
    return False

@router.message(Command("start"))
async def start_handler(msg: Message):
    if not check_access(msg):
        await msg.answer(
            "<blockquote><code>𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱 ❌</code></blockquote>\n\n"
            "<blockquote>「❃」 𝗝𝗼𝗶𝗻 𝘁𝗼 𝘂𝘀𝗲 : <code>@botlogsaai</code></blockquote>",
            parse_mode=ParseMode.HTML
        )
        return
    
    welcome = (
        "<blockquote><code>𝗧𝗼𝗼𝗹𝘀 ⚡</code></blockquote>\n\n"
        "<blockquote>「❃」 𝗖𝗵𝗲𝗰𝗸𝗼𝘂𝘁 𝗣𝗮𝗿𝘀𝗲𝗿\n"
        "    • <code>/co url</code> - Parse Stripe Checkout\n"
        "    • <code>/co url cc|mm|yy|cvv</code> - Charge Card</blockquote>\n\n"
        "<blockquote>「❃」 𝗦𝘂𝗽𝗽𝗼𝗿𝘁𝗲𝗱 𝗨𝗥𝗟𝘀\n"
        "    • <code>checkout.stripe.com</code>\n"
        "    • <code>buy.stripe.com</code></blockquote>\n\n"
        "<blockquote>「❃」 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 : <code>@victus_xd</code></blockquote>"
    )
    await msg.answer(welcome, parse_mode=ParseMode.HTML)

@router.message(Command("help"))
async def help_handler(msg: Message):
    if not check_access(msg):
        await msg.answer(
            "<blockquote><code>𝗔𝗰𝗰𝗲𝘀𝘀 𝗗𝗲𝗻𝗶𝗲𝗱 ❌</code></blockquote>\n\n"
            "<blockquote>「❃」 𝗝𝗼𝗶𝗻 𝘁𝗼 𝘂𝘀𝗲 : <code>@proscraperbot</code></blockquote>",
            parse_mode=ParseMode.HTML
        )
        return
    
    help_text = (
        "<blockquote><code>𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀 📋</code></blockquote>\n\n"
        "<blockquote>「❃」 <code>/start</code> - Show welcome message\n"
        "「❃」 <code>/help</code> - Show this help\n"
        "「❃」 <code>/co url</code> - Parse checkout info\n"
        "「❃」 <code>/co url cards</code> - Charge cards</blockquote>\n\n"
        "<blockquote>「❃」 𝗖𝗮𝗿𝗱 𝗙𝗼𝗿𝗺𝗮𝘁 : <code>cc|mm|yy|cvv</code>\n"
        "「❃」 𝗘𝘅𝗮𝗺𝗽𝗹𝗲 : <code>4242424242424242|12|25|123</code></blockquote>"
    )
    await msg.answer(help_text, parse_mode=ParseMode.HTML)
