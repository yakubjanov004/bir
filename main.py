"""
Main Application - Alfa Connect Bot

This is the main entry point for the Alfa Connect Telegram bot.
"""

import asyncio
import traceback
import sys
import logging
from loader import start_bot

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

if __name__ == "__main__":
    print("🚀 Starting Alfa Connect Bot...")
    print("📋 Loading configuration...")
    print("🔧 Setting up handlers...")
    
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
        logger.info("Bot stopped by user")
    except ImportError as e:
        logger.error(f"Import Error: {e}", exc_info=True)
        print(f"❌ Import Error: {e}")
        print(f"📁 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"🔍 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
    except NameError as e:
        logger.error(f"Name Error: {e}", exc_info=True)
        print(f"❌ Name Error: {e}")
        print(f"📁 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"🔍 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
    except Exception as e:
        logger.error(f"Error running bot: {e}", exc_info=True)
        print(f"❌ Error running bot: {e}")
        print(f"📁 Error type: {type(e).__name__}")
        print(f"🔍 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
        print(f"📄 Line number: {e.__traceback__.tb_lineno}")
        traceback.print_exc()
        sys.exit(1)
