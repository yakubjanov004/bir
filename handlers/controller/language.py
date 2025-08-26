"""
Controller Language Handler - Mock Data Implementation

Bu modul controller uchun til o'zgartirish funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import controllers_main_menu
from states.controller_states import ControllerSettingsStates
from filters.role_filter import RoleFilter
import logging

logger = logging.getLogger(__name__)

# Mock data storage
mock_users = {
    123456789: {
        'id': 1,
        'telegram_id': 123456789,
        'role': 'controller',
        'language': 'uz',
        'full_name': 'Test Controller',
        'phone_number': '+998901234567',
        'region': 'toshkent'
    }
}

# Mock controller dashboard statistics
mock_controller_stats = {
    'pending_assignment': 5,
    'active_work': 12,
    'completed_today': 8,
    'active_technicians': 15
}

# Mock utility classes
class MockAuditLogger:
    """Mock audit logger"""
    async def log_action(self, user_id: int, action: str, details: dict = None, entity_type: str = None, entity_id: str = None, region: str = None):
        """Mock log action"""
        logger.info(f"Mock: User {user_id} performed action: {action}")
        if details:
            logger.info(f"Mock: Details: {details}")

# Initialize mock instances
audit_logger = MockAuditLogger()

# Mock functions
async def get_user_by_telegram_id(region: str, telegram_id: int):
    """Mock get user by telegram ID"""
    logger.info(f"Mock: Getting user by telegram ID {telegram_id} in region {region}")
    return mock_users.get(telegram_id)

async def get_user_region(telegram_id: int):
    """Mock get user region"""
    user = mock_users.get(telegram_id)
    return user.get('region') if user else None

async def update_user_language(region: str, user_id: int, language: str):
    """Mock update user language"""
    logger.info(f"Mock: Updating user {user_id} language to {language} in region {region}")
    
    # Find and update the user
    for user in mock_users.values():
        if user['id'] == user_id:
            user['language'] = language
            return True
    return False

async def get_controller_dashboard_stats(region: str):
    """Mock get controller dashboard statistics"""
    logger.info(f"Mock: Getting controller dashboard stats for region {region}")
    return mock_controller_stats

def get_controller_language_router():
    """Get controller language router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Изменить язык"]))
    async def show_language_options(message: Message, state: FSMContext):
        """Show language selection as reply keyboard"""
        user_id = message.from_user.id
        
        try:
            # Get user region
            region = await get_user_region(user_id)
            if not region:
                await message.answer("❌ Region aniqlanmadi")
                return
            
            user = await get_user_by_telegram_id(region, user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda ruxsat yo'q.")
                return
            
            current_lang = user.get('language', 'uz')
            
            lang_kb = ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton("🇺🇿 O'zbek tili")],
                    [KeyboardButton("🇷🇺 Русский язык")],
                    [KeyboardButton("🔙 Orqaga" if current_lang == 'uz' else "🔙 Назад")],
                ],
                resize_keyboard=True
            )
            
            if current_lang == 'uz':
                text = "Tilni tanlang:"
            else:
                text = "Выберите язык:"
            
            await message.answer(text, reply_markup=lang_kb)
            await state.set_state(ControllerSettingsStates.selecting_language)
            
        except Exception as e:
            logger.error(f"Error in show_language_options: {e}")
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text.in_(["🇺🇿 O'zbek tili"]), ControllerSettingsStates.selecting_language)
    async def set_uzbek_language(message: Message, state: FSMContext):
        """O'zbek tilini o'rnatish"""
        user_id = message.from_user.id
        
        try:
            # Get user region
            region = await get_user_region(user_id)
            if not region:
                await message.answer("❌ Region aniqlanmadi")
                return
            
            user = await get_user_by_telegram_id(region, user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            # Update language in mock data
            success = await update_user_language(region, user['id'], 'uz')
            
            if success:
                text = """✅ <b>Til muvaffaqiyatli o'zgartirildi!</b>

Hozir siz O'zbek tilidan foydalanmoqdasiz 🇺🇿

Bosh menyuga qaytish uchun tugmani bosing."""
                
                # Get updated statistics from mock data
                stats = await get_controller_dashboard_stats(region)
                
                welcome_text = (
                    "🎛️ <b>Nazoratchi paneli</b>\n\n"
                    "📊 <b>Tizim holati:</b>\n"
                    f"• Tayinlash kutilmoqda: {stats.get('pending_assignment', 0)}\n"
                    f"• Faol ishlar: {stats.get('active_work', 0)}\n"
                    f"• Bugun bajarilgan: {stats.get('completed_today', 0)}\n"
                    f"• Faol texniklar: {stats.get('active_technicians', 0)}\n\n"
                    "Kerakli bo'limni tanlang:"
                )
                
                await message.answer(text, parse_mode='HTML')
                await message.answer(
                    welcome_text,
                    reply_markup=controllers_main_menu('uz'),
                    parse_mode='HTML'
                )
                await state.clear()
                await state.set_state(ControllerSettingsStates.main_menu)
                
                # Log action
                await audit_logger.log_action(
                    user_id=user_id,
                    action='DATA_UPDATED',
                    details={'field': 'language', 'old_value': user.get('language'), 'new_value': 'uz'},
                    entity_type='user',
                    entity_id=user['id'],
                    region=region
                )
                
                logger.info(f"Controller {user['id']} changed language to Uzbek")
            else:
                text = "❌ Tilni o'zgartirishda xatolik yuz berdi."
                await message.answer(text)
            
        except Exception as e:
            logger.error(f"Error in set_uzbek_language: {e}")
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text.in_(["🇷🇺 Русский язык"]), ControllerSettingsStates.selecting_language)
    async def set_russian_language(message: Message, state: FSMContext):
        """Rus tilini o'rnatish"""
        user_id = message.from_user.id
        
        try:
            # Get user region
            region = await get_user_region(user_id)
            if not region:
                await message.answer("❌ Регион не определен")
                return
            
            user = await get_user_by_telegram_id(region, user_id)
            if not user or user['role'] != 'controller':
                await message.answer("У вас нет прав контроллера.")
                return
            
            # Update language in mock data
            success = await update_user_language(region, user['id'], 'ru')
            
            if success:
                text = """✅ <b>Язык успешно изменен!</b>

Теперь вы используете русский язык 🇷🇺

Нажмите кнопку для возврата в главное меню."""
                
                # Get updated statistics from mock data
                stats = await get_controller_dashboard_stats(region)
                
                welcome_text = (
                    "🎛️ <b>Панель контроллера</b>\n\n"
                    "📊 <b>Состояние системы:</b>\n"
                    f"• Ожидает назначения: {stats.get('pending_assignment', 0)}\n"
                    f"• Активные работы: {stats.get('active_work', 0)}\n"
                    f"• Выполнено сегодня: {stats.get('completed_today', 0)}\n"
                    f"• Активные техники: {stats.get('active_technicians', 0)}\n\n"
                    "Выберите нужный раздел:"
                )
                
                await message.answer(text, parse_mode='HTML')
                await message.answer(
                    welcome_text,
                    reply_markup=controllers_main_menu('ru'),
                    parse_mode='HTML'
                )
                await state.clear()
                await state.set_state(ControllerSettingsStates.main_menu)
                
                # Log action
                await audit_logger.log_action(
                    user_id=user_id,
                    action='DATA_UPDATED',
                    details={'field': 'language', 'old_value': user.get('language'), 'new_value': 'ru'},
                    entity_type='user',
                    entity_id=user['id'],
                    region=region
                )
                
                logger.info(f"Controller {user['id']} changed language to Russian")
            else:
                text = "❌ Ошибка при изменении языка."
                await message.answer(text)
            
        except Exception as e:
            logger.error(f"Error in set_russian_language: {e}")
            await message.answer("Произошла ошибка")

    @router.message(F.text.in_(["🔙 Orqaga", "🔙 Назад"]))
    async def back_from_language(message: Message, state: FSMContext):
        """Til menyusidan orqaga qaytish"""
        user_id = message.from_user.id
        
        try:
            # Get user region
            region = await get_user_region(user_id)
            if not region:
                await message.answer("❌ Region aniqlanmadi / Регион не определен")
                return
            
            user = await get_user_by_telegram_id(region, user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q. / У вас нет прав контроллера.")
                return
            
            lang = user.get('language', 'uz')
            await state.clear()
            await state.set_state(ControllerSettingsStates.main_menu)
            
            # Get statistics from mock data
            stats = await get_controller_dashboard_stats(region)
            
            if lang == 'uz':
                welcome_text = (
                    "🎛️ <b>Nazoratchi paneli</b>\n\n"
                    "📊 <b>Tizim holati:</b>\n"
                    f"• Tayinlash kutilmoqda: {stats.get('pending_assignment', 0)}\n"
                    f"• Faol ishlar: {stats.get('active_work', 0)}\n"
                    f"• Bugun bajarilgan: {stats.get('completed_today', 0)}\n"
                    f"• Faol texniklar: {stats.get('active_technicians', 0)}\n\n"
                    "Kerakli bo'limni tanlang:"
                )
            else:
                welcome_text = (
                    "🎛️ <b>Панель контроллера</b>\n\n"
                    "📊 <b>Состояние системы:</b>\n"
                    f"• Ожидает назначения: {stats.get('pending_assignment', 0)}\n"
                    f"• Активные работы: {stats.get('active_work', 0)}\n"
                    f"• Выполнено сегодня: {stats.get('completed_today', 0)}\n"
                    f"• Активные техники: {stats.get('active_technicians', 0)}\n\n"
                    "Выберите нужный раздел:"
                )
            
            await message.answer(
                welcome_text,
                reply_markup=controllers_main_menu(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            logger.error(f"Error in back_from_language: {e}")
            await message.answer("Xatolik yuz berdi / Произошла ошибка")

    return router
