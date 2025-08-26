"""
Manager Language Handler - Mock Data Version

Bu modul manager uchun til o'zgartirish funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, database kerak emas.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
import logging

from keyboards.manager_buttons import get_manager_main_keyboard
from states.manager_states import ManagerMainMenuStates

logger = logging.getLogger(__name__)

# Mock user data for language management
MOCK_USERS = {
    123456789: {  # Example user ID
        'id': 123456789,
        'full_name': 'Manager User',
        'role': 'manager',
        'language': 'uz',
        'region': 'toshkent'
    }
}

def get_user_language_mock(user_id: int) -> str:
    """Get user language from mock data"""
    user = MOCK_USERS.get(user_id, {})
    return user.get('language', 'uz')

def update_user_language_mock(user_id: int, new_language: str) -> bool:
    """Update user language in mock data"""
    try:
        if user_id in MOCK_USERS:
            MOCK_USERS[user_id]['language'] = new_language
            return True
        else:
            # Create new user if doesn't exist
            MOCK_USERS[user_id] = {
                'id': user_id,
                'full_name': 'Manager User',
                'role': 'manager',
                'language': new_language,
                'region': 'toshkent'
            }
            return True
    except Exception as e:
        logger.error(f"Error updating mock user language: {e}")
        return False

def get_manager_language_router():
    """Get manager language router with mock data"""
    router = Router()
    
    @router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Изменить язык"]))
    async def change_manager_language(message: Message, state: FSMContext):
        """Manager language change handler"""
        try:
            # Get user language from mock data
            current_lang = get_user_language_mock(message.from_user.id)
            
            # Create language selection keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🇺🇿 O'zbekcha" + (" ✅" if current_lang == 'uz' else ""),
                        callback_data="manager_lang_uz"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🇷🇺 Русский" + (" ✅" if current_lang == 'ru' else ""),
                        callback_data="manager_lang_ru"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔙 Orqaga" if current_lang == 'uz' else "🔙 Назад",
                        callback_data="manager_lang_back"
                    )
                ]
            ])
            
            if current_lang == 'uz':
                lang_text = """🌐 <b>Tilni tanlang</b>

Joriy til: 🇺🇿 O'zbekcha

Kerakli tilni tanlang:"""
            else:
                lang_text = """🌐 <b>Выберите язык</b>

Текущий язык: 🇷🇺 Русский

Выберите нужный язык:"""
            
            sent_message = await message.answer(
                text=lang_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            await state.update_data(last_message_id=sent_message.message_id)
            
        except Exception as e:
            logger.error(f"Error in change_manager_language: {str(e)}")
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("manager_lang_"))
    async def handle_language_selection(callback: CallbackQuery, state: FSMContext):
        """Handle language selection"""
        try:
            await callback.answer()
            
            # Extract language code
            lang_code = callback.data.replace("manager_lang_", "")
            
            if lang_code == "back":
                # Go back to main menu
                await state.clear()
                
                # Get current language
                current_lang = get_user_language_mock(callback.from_user.id)
                
                # Import and show main keyboard
                keyboard = get_manager_main_keyboard(current_lang)
                
                if current_lang == 'uz':
                    text = "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:"
                else:
                    text = "🏠 <b>Главное меню</b>\n\nВыберите нужный раздел:"
                
                await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                return
            
            # Update user language
            success = update_user_language_mock(callback.from_user.id, lang_code)
            
            if success:
                # Language names
                lang_names = {
                    'uz': '🇺🇿 O\'zbekcha',
                    'ru': '🇷🇺 Русский'
                }
                
                # Success messages
                success_messages = {
                    'uz': f"""✅ <b>Til muvaffaqiyatli o'zgartirildi!</b>

🌐 Yangi til: {lang_names[lang_code]}

Endi bot siz bilan {lang_names[lang_code]} tilida ishlaydi.

🏠 Asosiy menyuga qaytish uchun tugmani bosing:""",
                    'ru': f"""✅ <b>Язык успешно изменен!</b>

🌐 Новый язык: {lang_names[lang_code]}

Теперь бот работает с вами на {lang_names[lang_code]} языке.

🏠 Нажмите кнопку для возврата в главное меню:"""
                }
                
                # Create success keyboard
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(
                        text="🏠 Asosiy menyu" if lang_code == 'uz' else "🏠 Главное меню",
                        callback_data="manager_lang_back"
                    )
                ]])
                
                await callback.message.edit_text(
                    text=success_messages[lang_code],
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )
                
                # Update state
                await state.update_data(language=lang_code)
                
            else:
                # Error message
                error_messages = {
                    'uz': "❌ Til o'zgartirishda xatolik yuz berdi",
                    'ru': "❌ Произошла ошибка при изменении языка"
                }
                
                current_lang = get_user_language_mock(callback.from_user.id)
                error_text = error_messages.get(current_lang, error_messages['uz'])
                
                await callback.answer(error_text, show_alert=True)
            
        except Exception as e:
            logger.error(f"Error in handle_language_selection: {str(e)}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "manager_lang_back")
    async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
        """Go back to main menu"""
        try:
            await callback.answer()
            
            # Clear state
            await state.clear()
            
            # Get current language
            current_lang = get_user_language_mock(callback.from_user.id)
            
            # Import and show main keyboard
            keyboard = get_manager_main_keyboard(current_lang)
            
            if current_lang == 'uz':
                text = "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:"
            else:
                text = "🏠 <b>Главное меню</b>\n\nВыберите нужный раздел:"
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error going back to main menu: {str(e)}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    return router
