from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Union
import logging
import traceback

logger = logging.getLogger(__name__)

class ErrorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            user = event.from_user
            error_msg = f"[{user.id}] {user.full_name} - Error in handler: {str(e)}"
            
            # Terminalga chiqarish
            print(f"❌ {error_msg}")
            print(f"📁 Error type: {type(e).__name__}")
            print(f"🔍 Error location: {e.__traceback__.tb_frame.f_code.co_filename}")
            print(f"📄 Line number: {e.__traceback__.tb_lineno}")
            print(f"📋 Full traceback:")
            traceback.print_exc()
            
            # Logger orqali yozish
            logger.error(error_msg, exc_info=True)
            logger.error(f"[{user.id}] Full traceback: {traceback.format_exc()}")
            
            # Foydalanuvchiga xabar yuborish
            try:
                if isinstance(event, Message):
                    await event.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
                elif isinstance(event, CallbackQuery):
                    await event.answer("❌ Xatolik yuz berdi", show_alert=True)
            except Exception as callback_error:
                logger.error(f"[{user.id}] Error sending error message: {callback_error}")
            
            raise 