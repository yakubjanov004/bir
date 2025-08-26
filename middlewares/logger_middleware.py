from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Union
import logging
import traceback

logger = logging.getLogger(__name__)

class LoggerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        try:
            user = event.from_user
            event_type = "Message" if isinstance(event, Message) else "Callback"
            event_content = event.text if isinstance(event, Message) else event.data
            
            logger.info(f"[{user.id}] {user.full_name} → {event_type}: {event_content}")
            
            # Handler natijasini qaytarish
            result = await handler(event, data)
            
            logger.info(f"[{user.id}] Handler completed successfully")
            return result
            
        except Exception as e:
            user = event.from_user
            logger.error(f"[{user.id}] Handler error: {str(e)}", exc_info=True)
            logger.error(f"[{user.id}] Error details: {traceback.format_exc()}")
            raise 