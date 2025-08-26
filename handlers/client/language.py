"""
Client Language Handler - Database Integrated

This module handles client language selection functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import get_language_keyboard, get_main_menu_keyboard
from states.client_states import LanguageStates
from filters.role_filter import RoleFilter

# Mock database functions to replace database imports
async def get_user_by_telegram_id_redis(telegram_id: int):
    """Mock user data from Redis"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'client',
        'language': 'uz',
        'full_name': 'Test Client',
        'phone_number': '+998901234567',
        'region': 'toshkent'
    }

async def get_db_pool(region: str):
    """Mock database pool"""
    print(f"Mock: Getting database pool for region {region}")
    return MockPool()

class MockPool:
    """Mock database pool"""
    async def acquire(self):
        return MockConnection()
    
    async def close(self):
        print("Mock: Closing database pool")

class MockConnection:
    """Mock database connection"""
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def fetchval(self, query: str, *args):
        """Mock fetchval - always return success"""
        print(f"Mock: Executing query: {query} with args: {args}")
        return 1  # Return user ID to indicate success

async def update_user_language(pool, telegram_id: int, language: str) -> bool:
    """Mock update user language in database"""
    try:
        print(f"Mock: Updating language for user {telegram_id} to {language}")
        # Simulate database update
        return True
        
    except Exception as e:
        print(f"Error updating user language: {e}")
        return False

# Mock audit logger
class AuditLogger:
    async def log_action(self, user_id: int, action: str, details: dict):
        """Mock audit logging"""
        print(f"Mock Audit Log: User {user_id} performed {action} with details {details}")

audit_logger = AuditLogger()

def get_client_language_router():
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🌐 Til o'zgartirish", "🌐 Изменить язык"]))
    async def client_language_handler(message: Message, state: FSMContext):
        """Client language handler"""
        try:
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return
            
            lang = user.get('language', 'uz')
            
            language_text = (
                "Tilni tanlang:"
                if lang == 'uz' else
                "Выберите язык:"
            )
            
            sent_message = await message.answer(
                text=language_text,
                reply_markup=get_language_keyboard()
            )
            
            # Save region in state for database operations
            region = user.get('region', 'toshkent').lower()
            await state.update_data(user_region=region)
            await state.set_state(LanguageStates.selecting_language)
            
        except Exception as e:
            print(f"Error in client_language_handler: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("lang_"))
    async def handle_language_selection(callback: CallbackQuery, state: FSMContext):
        """Handle language selection"""
        try:
            await callback.answer()
            
            selected_lang = callback.data.split("_")[1]
            
            # Get user and region from state
            user = await get_user_by_telegram_id_redis(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
                
            state_data = await state.get_data()
            region = state_data.get('user_region', user.get('region', 'toshkent')).lower()
            
            # Get database pool
            pool = await get_db_pool(region)
            
            # Update user language in database
            success = await update_user_language(pool, callback.from_user.id, selected_lang)
            
            if success:
                success_text = (
                    f"✅ Til muvaffaqiyatli o'zgartirildi: {'O\'zbekcha' if selected_lang == 'uz' else 'Русский'}"
                    if selected_lang == 'uz' else
                    f"✅ Язык успешно изменен: {'O\'zbekcha' if selected_lang == 'uz' else 'Русский'}"
                )
                
                # Show success message without keyboard first
                await callback.message.edit_text(text=success_text)
                
                # Then send main menu with reply keyboard
                menu_text = (
                    "Quyidagi menyudan kerakli bo'limni tanlang."
                    if selected_lang == 'uz' else
                    "Выберите нужный раздел из меню ниже."
                )
                
                await callback.message.answer(
                    text=menu_text,
                    reply_markup=get_main_menu_keyboard(selected_lang)
                )
                
                # Log action
                await audit_logger.log_action(
                    user_id=user['id'],
                    action="change_language",
                    details={"old_language": user.get('language', 'uz'), "new_language": selected_lang}
                )
                
                await state.clear()
            else:
                error_text = (
                    "❌ Til o'zgartirishda xatolik yuz berdi."
                    if user.get('language', 'uz') == 'uz' else
                    "❌ Ошибка при изменении языка."
                )
                
                await callback.message.edit_text(error_text)
                
        except Exception as e:
            print(f"Error in handle_language_selection: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "cancel_language")
    async def cancel_language_selection(callback: CallbackQuery, state: FSMContext):
        """Cancel language selection"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id_redis(callback.from_user.id)
            lang = user.get('language', 'uz') if user else 'uz'
            
            cancel_text = (
                "❌ Til tanlash bekor qilindi."
                if lang == 'uz' else
                "❌ Выбор языка отменен."
            )
            
            # Edit message to show cancellation
            await callback.message.edit_text(cancel_text)
            
            # Send main menu
            menu_text = (
                "Quyidagi menyudan kerakli bo'limni tanlang."
                if lang == 'uz' else
                "Выберите нужный раздел из меню ниже."
            )
            
            await callback.message.answer(
                text=menu_text,
                reply_markup=get_main_menu_keyboard(lang)
            )
            
            await state.clear()
            
        except Exception as e:
            print(f"Error in cancel_language_selection: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
