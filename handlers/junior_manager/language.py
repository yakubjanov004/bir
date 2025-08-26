"""
Junior Manager Language Handler - Mock Data Implementation

Bu modul junior manager uchun til o'zgartirish funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.junior_manager_buttons import (
    get_language_keyboard,
    get_junior_manager_main_menu
)
from states.junior_manager_states import JuniorManagerLanguageStates
from filters.role_filter import RoleFilter
import logging

logger = logging.getLogger(__name__)

# Mock data storage
mock_users = {
    123456789: {
        'id': 1,
        'telegram_id': 123456789,
        'role': 'junior_manager',
        'language': 'uz',
        'full_name': 'Test Junior Manager',
        'phone_number': '+998901234567',
        'region': 'toshkent'
    }
}

# Mock language settings
mock_language_settings = {
    123456789: {
        'user_id': 1,
        'language': 'uz',
        'region': 'toshkent',
        'updated_at': '2024-01-15 10:00:00'
    }
}

# Mock utility classes
class MockAuditLogger:
    """Mock audit logger"""
    async def log_language_change(self, user_id: int, old_lang: str, new_lang: str, region: str = None):
        """Mock log language change"""
        logger.info(f"Mock: Junior Manager {user_id} changed language from {old_lang} to {new_lang}")
        if region:
            logger.info(f"Mock: Region: {region}")

# Initialize mock instances
audit_logger = MockAuditLogger()

# Mock functions to replace database calls
async def get_user_by_telegram_id(user_id: int):
    """Mock get user by telegram ID"""
    return mock_users.get(user_id)

async def update_user_language(user_id: int, new_language: str):
    """Mock update user language"""
    try:
        if user_id in mock_users:
            mock_users[user_id]['language'] = new_language
            
            # Update language settings
            if user_id in mock_language_settings:
                mock_language_settings[user_id]['language'] = new_language
                mock_language_settings[user_id]['updated_at'] = '2024-01-15 10:00:00'
            else:
                mock_language_settings[user_id] = {
                    'user_id': mock_users[user_id]['id'],
                    'language': new_language,
                    'region': mock_users[user_id].get('region', 'toshkent'),
                    'updated_at': '2024-01-15 10:00:00'
                }
            
            logger.info(f"Mock: Updated language for user {user_id} to {new_language}")
            return True
        return False
    except Exception as e:
        logger.error(f"Mock: Error updating user language: {e}")
        return False

async def update_user_in_db(region_code: str, user_id: int, updates: dict):
    """Mock update user in database"""
    try:
        # Find user by ID in mock data
        for user in mock_users.values():
            if user.get('id') == user_id:
                user.update(updates)
                logger.info(f"Mock: Updated user {user_id} in regional DB with {updates}")
                return True
        return False
    except Exception as e:
        logger.error(f"Mock: Error updating user in regional DB: {e}")
        return False

async def get_user_lang(user_id: int):
    """Mock get user language"""
    user = await get_user_by_telegram_id(user_id)
    return user.get('language', 'uz') if user else 'uz'

async def get_text(key: str, lang: str = 'uz'):
    """Mock get text by key and language"""
    # Simple mock text function
    texts = {
        'uz': {
            'user_not_found': 'Foydalanuvchi topilmadi',
            'access_denied': 'Sizda bu bo\'limga kirish ruxsati yo\'q',
            'language_changed': 'Til muvaffaqiyatli o\'zgartirildi',
            'language_already_set': 'Til allaqachon o\'zbek tilida',
            'error_occurred': 'Xatolik yuz berdi'
        },
        'ru': {
            'user_not_found': 'Пользователь не найден',
            'access_denied': 'У вас нет доступа к этому разделу',
            'language_changed': 'Язык успешно изменен',
            'language_already_set': 'Язык уже русский',
            'error_occurred': 'Произошла ошибка'
        }
    }
    return texts.get(lang, {}).get(key, key)

# Create router
router = Router(name="junior_manager_language")

# Apply role filter to all handlers
router.message.filter(RoleFilter(role="junior_manager"))
router.callback_query.filter(RoleFilter(role="junior_manager"))


@router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Изменить язык"]))
async def change_language(message: Message, state: FSMContext):
    """Handle language change request"""
    user_id = message.from_user.id
    
    try:
        # Get user data
        user = await get_user_by_telegram_id(user_id)
        if not user:
            await message.answer("❌ Foydalanuvchi topilmadi.")
            return
        
        # Verify role
        if user.get('role') != 'junior_manager':
            await message.answer("⛔ Sizda bu bo'limga kirish ruxsati yo'q.")
            return
        
        # Get current language
        current_lang = await get_user_lang(user_id) or user.get('language', 'uz')
        
        # Prepare message text
        if current_lang == 'uz':
            text = (
                "🌐 <b>Tilni o'zgartirish</b>\n\n"
                "Kerakli tilni tanlang:\n\n"
                f"Joriy til: {'🇺🇿 O\'zbekcha' if current_lang == 'uz' else '🇷🇺 Русский'}"
            )
        else:
            text = (
                "🌐 <b>Изменить язык</b></n\n"
                "Выберите нужный язык:\n\n"
                f"Текущий язык: {'🇺🇿 Узбекский' if current_lang == 'uz' else '🇷🇺 Русский'}"
            )
        
        # Set state
        await state.set_state(JuniorManagerLanguageStates.selecting_language)
        await state.update_data(
            current_language=current_lang,
            user_id=user.get('id'),
            region=user.get('region')
        )
        
        await message.answer(
            text,
            reply_markup=get_language_keyboard(current_lang),
            parse_mode='HTML'
        )
        
        logger.info(f"Junior Manager {user_id} opened language settings")
        
    except Exception as e:
        logger.error(f"Error in change_language: {str(e)}")
        await message.answer("❌ Xatolik yuz berdi")


@router.callback_query(F.data.in_(["jm_lang_uz", "jm_lang_ru"]))
async def handle_language_selection(callback: CallbackQuery, state: FSMContext):
    """Handle language selection"""
    user_id = callback.from_user.id
    
    try:
        await callback.answer()
        
        # Get new language from callback data
        new_lang = "uz" if callback.data == "jm_lang_uz" else "ru"
        
        # Get state data
        data = await state.get_data()
        current_lang = data.get('current_language', 'uz')
        
        # Check if language is actually changing
        if new_lang == current_lang:
            if new_lang == 'uz':
                text = "ℹ️ Til allaqachon o'zbek tilida"
            else:
                text = "ℹ️ Язык уже русский"
            
            await callback.answer(text, show_alert=True)
            return
        
        # Update language in mock data
        success = await update_user_language(user_id, new_lang)
        
        if success:
            # Also update in regional database if region is available
            region = data.get('region')
            if region:
                try:
                    await update_user_in_db(
                        region_code=region,
                        user_id=data.get('user_id'),
                        updates={'language': new_lang}
                    )
                except Exception as e:
                    logger.error(f"Error updating language in regional DB: {str(e)}")
            
            # Log the action
            await audit_logger.log_language_change(
                user_id=user_id,
                old_lang=current_lang,
                new_lang=new_lang,
                region=region
            )
            
            # Prepare success message
            if new_lang == 'uz':
                success_text = (
                    "✅ <b>Til muvaffaqiyatli o'zgartirildi!</b>\n\n"
                    "Endi bot o'zbek tilida ishlaydi.\n"
                    "Barcha xabarlar va tugmalar o'zbek tilida ko'rsatiladi."
                )
                button_text = "Asosiy menyuga qaytish"
            else:
                success_text = (
                    "✅ <b>Язык успешно изменен!</b>\n\n"
                    "Теперь бот работает на русском языке.\n"
                    "Все сообщения и кнопки будут отображаться на русском языке."
                )
                button_text = "Вернуться в главное меню"
            
            # Edit message with success text
            await callback.message.edit_text(
                success_text,
                parse_mode='HTML'
            )
            
            # Send main menu with new language
            await callback.message.answer(
                button_text,
                reply_markup=get_junior_manager_main_menu(new_lang)
            )
            
            # Clear state
            await state.clear()
            
            logger.info(f"Junior Manager {user_id} changed language from {current_lang} to {new_lang}")
            
        else:
            error_text = "❌ Tilni o'zgartirishda xatolik" if current_lang == 'uz' else "❌ Ошибка при изменении языка"
            await callback.answer(error_text, show_alert=True)
        
    except Exception as e:
        logger.error(f"Error in handle_language_selection: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data == "jm_cancel_language")
async def cancel_language_change(callback: CallbackQuery, state: FSMContext):
    """Cancel language change"""
    try:
        await callback.answer()
        
        # Get current language
        lang = await get_user_lang(callback.from_user.id) or 'uz'
        
        if lang == 'uz':
            text = "❌ Til o'zgartirish bekor qilindi"
        else:
            text = "❌ Изменение языка отменено"
        
        await callback.message.edit_text(text)
        
        # Send main menu
        await callback.message.answer(
            "Asosiy menyu" if lang == 'uz' else "Главное меню",
            reply_markup=get_junior_manager_main_menu(lang)
        )
        
        # Clear state
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error in cancel_language_change: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)