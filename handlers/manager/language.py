"""
Manager Language Handler - Mock Data Implementation

Bu modul manager uchun til o'zgartirish funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter
import logging

from keyboards.manager_buttons import get_manager_main_keyboard
from states.manager_states import ManagerMainMenuStates

logger = logging.getLogger(__name__)

# Mock data storage
mock_users = {
    1: {
        'id': 1,
        'telegram_id': 123456789,
        'role': 'manager',
        'language': 'uz',
        'full_name': 'Test Manager',
        'phone_number': '+998901234567',
        'region': 'toshkent'
    }
}

# Mock application statistics
mock_statistics = {
    'total_requests': 15,
    'created_count': 8,
    'in_progress_count': 4,
    'completed_count': 3,
    'cancelled_count': 0
}

# Mock utility classes
class MockAuditLogger:
    """Mock audit logger"""
    async def log_manager_action(self, manager_id: int, action: str, details: dict = None):
        """Mock log manager action"""
        logger.info(f"Mock: Manager {manager_id} performed action: {action}")
        if details:
            logger.info(f"Mock: Details: {details}")

# Initialize mock instances
audit_logger = MockAuditLogger()

# Mock functions
async def get_user_by_telegram_id(region: str, user_id: int):
    """Mock get user by telegram ID"""
    for user in mock_users.values():
        if user.get('telegram_id') == user_id:
            return user
    return None

async def update_user_language(region: str, user_id: int, language: str):
    """Mock update user language"""
    logger.info(f"Mock: Updating user {user_id} language to {language} in region {region}")
    # Update mock user data
    for user in mock_users.values():
        if user.get('id') == user_id:
            user['language'] = language
            break
    return True

async def update_user_activity(region: str, user_id: int):
    """Mock update user activity"""
    logger.info(f"Mock: Updating user {user_id} activity in region {region}")
    return True

async def get_application_statistics(region: str, user_id: int):
    """Mock get application statistics"""
    logger.info(f"Mock: Getting statistics for user {user_id} in region {region}")
    return mock_statistics

def get_manager_language_router():
    """Get manager language router with mock data"""
    router = Router()
    
    # Apply role filter - both manager and junior_manager can access
    role_filter = RoleFilter(["manager", "junior_manager"])
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Изменить язык"]), flags={"block": False})
    async def change_manager_language(message: Message, state: FSMContext):
        """Manager language change handler"""
        try:
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Get user from mock data
            user = await get_user_by_telegram_id(region, message.from_user.id)
            if not user or user['role'] not in ['manager', 'junior_manager']:
                await message.answer("❌ Sizda ruxsat yo'q")
                return
            
            current_lang = user.get('language', 'uz')
            
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
                        text="🔙 Orqaga / Назад",
                        callback_data="manager_back_to_main"
                    )
                ]
            ])
            
            if current_lang == 'uz':
                lang_text = (
                    "🌐 <b>Tilni tanlang</b>\n\n"
                    f"Joriy til: {'O\'zbekcha' if current_lang == 'uz' else 'Русский'}\n\n"
                    "Quyidagi tugmalardan birini tanlang:"
                )
            else:
                lang_text = (
                    "🌐 <b>Выберите язык</b>\n\n"
                    f"Текущий язык: {'O\'zbekcha' if current_lang == 'uz' else 'Русский'}\n\n"
                    "Выберите одну из кнопок ниже:"
                )
            
            await message.answer(
                text=lang_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Log language menu access using mock audit logger
            await audit_logger.log_manager_action(
                manager_id=user['id'],
                action='access_language_menu',
                details={'current_language': current_lang, 'region': region}
            )
            
        except Exception as e:
            logger.error(f"Error in change_manager_language: {str(e)}")
            await message.answer("❌ Xatolik yuz berdi / Произошла ошибка")

    @router.callback_query(F.data.startswith("manager_lang_"))
    async def set_manager_language(callback: CallbackQuery, state: FSMContext):
        """Set manager language"""
        try:
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Get user from mock data
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            if not user or user['role'] not in ['manager', 'junior_manager']:
                await callback.answer("❌ Xatolik: Foydalanuvchi ma'lumotlari topilmadi.", show_alert=True)
                return
            
            selected_lang = callback.data.split('_')[-1]
            
            # Update user language using mock function
            success = await update_user_language(region, user['id'], selected_lang)
            
            if not success:
                await callback.answer("❌ Tilni o'zgartirishda xatolik", show_alert=True)
                return
            
            # Update state
            await state.update_data(lang=selected_lang)
            
            # Create success message
            if selected_lang == 'uz':
                success_text = (
                    "✅ <b>Til muvaffaqiyatli o'zgartirildi!</b>\n\n"
                    "🌐 Joriy til: O'zbekcha\n\n"
                    "Endi barcha xabarlar o'zbek tilida ko'rsatiladi."
                )
                button_text = "🏠 Asosiy menyu"
            else:
                success_text = (
                    "✅ <b>Язык успешно изменен!</b>\n\n"
                    "🌐 Текущий язык: Русский\n\n"
                    "Теперь все сообщения будут отображаться на русском языке."
                )
                button_text = "🏠 Главное меню"
            
            # Create inline keyboard for back to main menu
            back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=button_text, callback_data="manager_back_to_main")]
            ])
            
            # Edit message with success and inline keyboard
            await callback.message.edit_text(
                text=success_text,
                reply_markup=back_keyboard,
                parse_mode='HTML'
            )
            
            # Log language change using mock audit logger
            await audit_logger.log_manager_action(
                manager_id=user['id'],
                action='change_language',
                details={
                    'from_language': user.get('language', 'uz'),
                    'to_language': selected_lang,
                    'region': region
                }
            )
            
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error in set_manager_language: {str(e)}")
            await callback.answer("❌ Xatolik yuz berdi / Произошла ошибка", show_alert=True)

    @router.callback_query(F.data == "manager_back_to_main")
    async def manager_back_to_main_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to main menu button"""
        try:
            await callback.answer()
            
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Get user from mock data
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            if not user or user['role'] not in ['manager', 'junior_manager']:
                return
            
            # Update user activity using mock function
            await update_user_activity(region, user['id'])
            
            lang = user.get('language', 'uz')
            
            # Get statistics for display using mock function
            stats = await get_application_statistics(region, user['id'])
            
            # Prepare main menu text with statistics
            if lang == 'uz':
                main_menu_text = (
                    f"👨‍💼 <b>Manager paneli</b>\n\n"
                    f"Assalomu alaykum, {user.get('full_name', 'Manager')}!\n\n"
                    f"📊 <b>Bugungi statistika:</b>\n"
                    f"• Jami arizalar: {stats.get('total_requests', 0)}\n"
                    f"• Yangi: {stats.get('created_count', 0)}\n"
                    f"• Jarayonda: {stats.get('in_progress_count', 0)}\n"
                    f"• Tugallangan: {stats.get('completed_count', 0)}\n\n"
                    f"Quyidagi menyudan kerakli bo'limni tanlang:"
                )
            else:
                main_menu_text = (
                    f"👨‍💼 <b>Панель менеджера</b>\n\n"
                    f"Здравствуйте, {user.get('full_name', 'Менеджер')}!\n\n"
                    f"📊 <b>Статистика за сегодня:</b>\n"
                    f"• Всего заявок: {stats.get('total_requests', 0)}\n"
                    f"• Новых: {stats.get('created_count', 0)}\n"
                    f"• В процессе: {stats.get('in_progress_count', 0)}\n"
                    f"• Завершено: {stats.get('completed_count', 0)}\n\n"
                    f"Выберите нужный раздел из меню:"
                )
            
            # Send new message with main menu keyboard
            await callback.message.answer(
                text=main_menu_text,
                reply_markup=get_manager_main_keyboard(lang),
                parse_mode='HTML'
            )
            
            # Delete the previous message
            await callback.message.delete()
            
            # Set state to main menu
            await state.set_state(ManagerMainMenuStates.main_menu)
            
        except Exception as e:
            logger.error(f"Error in manager_back_to_main_handler: {str(e)}")
            await callback.answer("❌ Xatolik yuz berdi / Произошла ошибка", show_alert=True)

    return router
