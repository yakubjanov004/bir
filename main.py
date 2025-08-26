"""
Telegram Bot - Manager Panel
Soddalashtirilgan versiya
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Import handlers
from handlers.applications import get_manager_applications_router
from handlers.inbox import get_manager_inbox_router
from handlers.connection_order import get_manager_connection_order_router
from handlers.technician_order import get_manager_technician_order_router
from handlers.realtime_monitoring import get_manager_realtime_monitoring_router
from handlers.staff_activity import get_manager_staff_activity_router
from handlers.status_management import get_manager_status_management_router
from handlers.export import get_manager_export_router
from handlers.language import get_manager_language_router
from handlers.filters import get_manager_filters_router

# Import keyboards
from keyboards.manager_buttons import get_manager_main_keyboard

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token - .env faylidan o'qish yoki to'g'ridan-to'g'ri yozish
BOT_TOKEN = "7591107647:AAEF1v90SSoi1gJBxhvrzGIzCvUvw9-t0Kg"  # Bu yerga o'zingizning bot tokenini yozing

# Bot va dispatcher yaratish
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Start command handler"""
    welcome_text = f"""<b>Xush kelibsiz, {message.from_user.first_name or 'Manager'}!</b>

Bu manager panel orqali siz:
• Arizalarni ko'rishingiz mumkin
• Inbox xabarlarini boshqarishingiz mumkin
• Yangi ulanish arizalarini yaratishingiz mumkin
• Texnik xizmat arizalarini yaratishingiz mumkin
• Real vaqtda monitoring qilishingiz mumkin
• Xodimlar faoliyatini kuzatishingiz mumkin

Boshlash uchun quyidagi tugmalardan birini bosing:"""

    keyboard = get_manager_main_keyboard("uz")  # O'zbek tilida keyboard
    await message.answer(welcome_text, reply_markup=keyboard, parse_mode='HTML')

async def main():
    """Asosiy funksiya"""
    logger.info("Bot ishga tushmoqda...")
    
    # Routers ro'yxatini to'g'ri tartibda qo'shish
    # Har bir router o'zining aniq matnli buyrug'iga ega bo'lishi kerak
    dp.include_routers(
        get_manager_applications_router(),
        get_manager_inbox_router(),
        get_manager_connection_order_router(),
        get_manager_technician_order_router(),
        get_manager_realtime_monitoring_router(),
        get_manager_staff_activity_router(),
        get_manager_status_management_router(),
        get_manager_export_router(),
        get_manager_language_router(),
        get_manager_filters_router()
    )
    
    # Bot ishga tushirish
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
