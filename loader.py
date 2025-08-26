"""
Bot Loader - Complete Implementation

This module sets up the Telegram bot with environment variables
and role-based routing system.
"""

import os
import asyncio
import traceback
import sys
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

# Logger sozlash - batafsil
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Terminal uchun
        logging.FileHandler('testbot_errors.log', encoding='utf-8'),  # Xatoliklar uchun
        logging.FileHandler('testbot_activity.log', encoding='utf-8')  # Faollik uchun
    ]
)
logger = logging.getLogger(__name__)

# Qo'shimcha logger'lar
activity_logger = logging.getLogger('activity')
activity_logger.setLevel(logging.INFO)
activity_handler = logging.FileHandler('testbot_activity.log', encoding='utf-8')
activity_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
activity_handler.setFormatter(activity_formatter)
activity_logger.addHandler(activity_handler)

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip()]
BOT_ID = int(os.getenv('BOT_ID', 0))
ZAYAVKA_GROUP_ID = int(os.getenv('ZAYAVKA_GROUP_ID', 0))

# Database configuration (for future use)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'alfaconnect_db')

# Role IDs
MANAGER_ID = int(os.getenv('MANAGER_ID', 0)) if os.getenv('MANAGER_ID') else None
CLIENT_ID = int(os.getenv('CLIENT_ID', 0)) if os.getenv('CLIENT_ID') else None
JUNIOR_MANAGER_ID = int(os.getenv('JUNIOR_MANAGER_ID', 0)) if os.getenv('JUNIOR_MANAGER_ID') else None
CONTROLLER_ID = int(os.getenv('CONTROLLER_ID', 0)) if os.getenv('CONTROLLER_ID') else None
TECHNICIAN_ID = int(os.getenv('TECHNICIAN_ID', 0)) if os.getenv('TECHNICIAN_ID') else None
WAREHOUSE_ID = int(os.getenv('WAREHOUSE_ID', 0)) if os.getenv('WAREHOUSE_ID') else None
CALL_CENTER_SUPERVISOR_ID = int(os.getenv('CALL_CENTER_SUPERVISOR_ID', 0)) if os.getenv('CALL_CENTER_SUPERVISOR_ID') else None
CALL_CENTER_ID = int(os.getenv('CALL_CENTER_ID', 0)) if os.getenv('CALL_CENTER_ID') else None

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Middleware'larni qo'shish
from middlewares.logger_middleware import LoggerMiddleware
from middlewares.error_middleware import ErrorMiddleware

dp.message.middleware(LoggerMiddleware())
dp.callback_query.middleware(LoggerMiddleware())
dp.message.middleware(ErrorMiddleware())
dp.callback_query.middleware(ErrorMiddleware())

# Role mapping
ROLE_MAPPING = {
    MANAGER_ID: 'manager',
    CLIENT_ID: 'client',
    JUNIOR_MANAGER_ID: 'junior_manager',
    CONTROLLER_ID: 'controller',
    TECHNICIAN_ID: 'technician',
    WAREHOUSE_ID: 'warehouse',
    CALL_CENTER_SUPERVISOR_ID: 'call_center_supervisor',
    CALL_CENTER_ID: 'call_center'
}

def get_user_role(user_id: int) -> str:
    """Get user role based on user ID"""
    if user_id in ADMIN_IDS:
        return 'admin'
    
    for role_id, role_name in ROLE_MAPPING.items():
        if role_id and user_id == role_id:
            return role_name
    
    # Default role for testing
    return 'client'

# Global bot instance for use in handlers
def get_bot():
    return bot

def get_dp():
    return dp

async def setup_bot():
    """Setup bot with all handlers"""
    try:
        # Import and setup handlers
        from handlers import setup_handlers
        setup_handlers(dp)
        
        print("✅ Bot setup completed successfully")
        print(f"🤖 Bot ID: {BOT_ID}")
        print(f"👥 Admin IDs: {ADMIN_IDS}")
        print(f"📋 Role mapping: {ROLE_MAPPING}")
        
    except ImportError as e:
        logger.error(f"Import Error in setup_bot: {e}", exc_info=True)
        print(f"❌ Import Error in setup_bot: {e}")
        print(f"📁 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"🔍 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
        raise
    except NameError as e:
        logger.error(f"Name Error in setup_bot: {e}", exc_info=True)
        print(f"❌ Name Error in setup_bot: {e}")
        print(f"📁 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"🔍 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
        raise
    except Exception as e:
        logger.error(f"Error setting up bot: {e}", exc_info=True)
        print(f"❌ Error setting up bot: {e}")
        print(f"📁 Error type: {type(e).__name__}")
        print(f"🔍 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"📄 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
        raise

async def start_bot():
    """Start the bot"""
    try:
        await setup_bot()
        print("🚀 Starting bot...")
        await dp.start_polling(bot)
    except ImportError as e:
        logger.error(f"Import Error in start_bot: {e}", exc_info=True)
        print(f"❌ Import Error in start_bot: {e}")
        print(f"📁 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"🔍 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
        raise
    except NameError as e:
        logger.error(f"Name Error in start_bot: {e}", exc_info=True)
        print(f"❌ Name Error in start_bot: {e}")
        print(f"📁 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"🔍 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
        raise
    except Exception as e:
        logger.error(f"Error starting bot: {e}", exc_info=True)
        print(f"❌ Error starting bot: {e}")
        print(f"📁 Error type: {type(e).__name__}")
        print(f"🔍 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"📄 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
        raise

if __name__ == "__main__":
    asyncio.run(start_bot())
