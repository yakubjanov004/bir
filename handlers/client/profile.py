"""
Client Profile Handler - Database Integrated

This module handles client profile functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.client_buttons import (
    get_client_profile_menu,
    get_edit_profile_keyboard,
    get_client_profile_reply_keyboard,
    get_main_menu_keyboard,
)
from states.client_states import ProfileStates
from filters.role_filter import RoleFilter
from utils.logger import get_logger
from datetime import datetime

# Mock database functions to replace database imports
# Global mock storage for demonstration
mock_user_data = {}

async def get_user_by_telegram_id_redis(telegram_id: int):
    """Mock user data from Redis"""
    # Initialize mock data if not exists
    if telegram_id not in mock_user_data:
        mock_user_data[telegram_id] = {
            'id': 1,
            'telegram_id': telegram_id,
            'role': 'client',
            'language': 'uz',
            'full_name': 'Test Client',
            'phone_number': '+998901234567',
            'phone': '+998901234567',
            'address': 'Toshkent shahri, Chilanzor tumani, 15-uy',
            'region': 'toshkent',
            'created_at': '2024-01-01 10:00:00'
        }
    
    return mock_user_data[telegram_id]

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
    
    async def fetchrow(self, query: str, *args):
        """Mock fetchrow - return mock user profile"""
        print(f"Mock: Executing profile query: {query} with args: {args}")
        return {
            'id': 1,
            'telegram_id': args[0] if args else 123456789,
            'full_name': 'Test Client',
            'username': 'testuser',
            'phone': '+998901234567',
            'role': 'client',
            'language': 'uz',
            'is_active': True,
            'address': 'Toshkent shahri, Chilanzor tumani, 15-uy',
            'created_at': '2024-01-01 10:00:00',
            'updated_at': '2024-01-15 10:00:00'
        }
    
    async def fetchval(self, query: str, *args):
        """Mock fetchval - return mock update result"""
        print(f"Mock: Executing update query: {query} with args: {args}")
        return 1  # Return user ID to indicate success

async def get_user_profile_from_db(pool, telegram_id: int):
    """Mock get user profile from database"""
    try:
        print(f"Mock: Getting user profile for {telegram_id}")
        
        # Get data from mock storage
        user_data = mock_user_data.get(telegram_id, {})
        
        # Mock user profile data with current values
        profile = {
            'id': user_data.get('id', 1),
            'telegram_id': telegram_id,
            'full_name': user_data.get('full_name', 'Test Client'),
            'username': user_data.get('username', 'testuser'),
            'phone': user_data.get('phone', '+998901234567'),
            'role': user_data.get('role', 'client'),
            'language': user_data.get('language', 'uz'),
            'is_active': user_data.get('is_active', True),
            'address': user_data.get('address', 'Toshkent shahri, Chilanzor tumani, 15-uy'),
            'created_at': user_data.get('created_at', '2024-01-01 10:00:00'),
            'updated_at': user_data.get('updated_at', '2024-01-15 10:00:00')
        }
        
        return profile
        
    except Exception as e:
        print(f"Error getting user profile: {e}")
        return None

async def update_user_profile(pool, telegram_id: int, field: str, value: str):
    """Mock update user profile in database"""
    try:
        print(f"Mock: Updating user {telegram_id} {field} to {value}")
        
        # Update mock storage
        if telegram_id not in mock_user_data:
            mock_user_data[telegram_id] = {}
        
        # Update the specific field based on the database field name
        if field == 'full_name':
            mock_user_data[telegram_id]['full_name'] = value
        elif field == 'phone':
            mock_user_data[telegram_id]['phone'] = value
            mock_user_data[telegram_id]['phone_number'] = value
        elif field == 'address':
            mock_user_data[telegram_id]['address'] = value
        
        # Update timestamp
        from datetime import datetime
        mock_user_data[telegram_id]['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"Mock: Successfully updated {field} to {value} for user {telegram_id}")
        print(f"Mock: Current user data: {mock_user_data[telegram_id]}")
        
        return True
        
    except Exception as e:
        print(f"Error updating user profile: {e}")
        return False

async def get_user_statistics(pool, user_id: int):
    """Mock get user statistics from database"""
    try:
        print(f"Mock: Getting statistics for user {user_id}")
        
        # Mock statistics data
        stats = {
            'active_orders': 2,
            'completed_orders': 3,
            'total_orders': 5,
            'last_order_date': '2024-01-15 10:30:00'
        }
        
        return stats
        
    except Exception as e:
        print(f"Error getting user statistics: {e}")
        return {
            'active_orders': 0,
            'completed_orders': 0,
            'total_orders': 0,
            'last_order_date': None
        }

# Mock audit logger
class AuditLogger:
    async def log_action(self, user_id: int, action: str, details: dict):
        """Mock audit logging"""
        print(f"Mock Audit Log: User {user_id} performed {action} with details {details}")

audit_logger = AuditLogger()

# Initialize logger
logger = get_logger(__name__)

async def show_updated_profile(message: Message, user: dict, lang: str):
    """Show updated profile information"""
    try:
        # Get region from user
        region = user.get('region', 'toshkent')
        if region:
            region = region.lower()
        else:
            region = 'toshkent'
        
        pool = await get_db_pool(region)
        
        # Get updated profile from database
        profile = await get_user_profile_from_db(pool, message.from_user.id)
        if not profile:
            return
        
        # Get statistics
        stats = await get_user_statistics(pool, profile['id'])
        
        # Format dates
        created_date = profile.get('created_at')
        if created_date:
            if isinstance(created_date, str):
                created_date = datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S')
            formatted_date = created_date.strftime('%d.%m.%Y')
        else:
            formatted_date = 'Noma\'lum'
        
        # Format last order date
        last_order = stats.get('last_order_date') if stats else None
        if last_order:
            if isinstance(last_order, str):
                last_order = datetime.strptime(last_order, '%Y-%m-%d %H:%M:%S')
            last_order_text = last_order.strftime('%d.%m.%Y %H:%M')
        else:
            last_order_text = 'Yo\'q'
        
        if lang == 'uz':
            profile_text = (
                "🔄 <b>Yangilangan profil ma'lumotlari:</b>\n\n"
                f"📱 <b>Telegram ID:</b> {profile.get('telegram_id', 'Noma\'lum')}\n"
                f"👤 <b>F.I.O:</b> {profile.get('full_name', 'Kiritilmagan')}\n"
                f"📞 <b>Telefon:</b> {profile.get('phone', 'Kiritilmagan')}\n"
                f"📍 <b>Manzil:</b> {profile.get('address', 'Kiritilmagan')}\n"
                f"🌐 <b>Til:</b> {'O\'zbek' if lang == 'uz' else 'Русский'}\n"
                f"📅 <b>Ro'yxatdan o'tgan:</b> {formatted_date}\n"
                f"🕒 <b>Oxirgi yangilangan:</b> {profile.get('updated_at', 'Noma\'lum')}\n\n"
                f"📊 <b>Statistika:</b>\n"
                f"• Faol buyurtmalar: {stats.get('active_orders', 0) if stats else 0}\n"
                f"• Bajarilgan buyurtmalar: {stats.get('completed_orders', 0) if stats else 0}\n"
                f"• Jami buyurtmalar: {stats.get('total_orders', 0) if stats else 0}\n"
                f"• Oxirgi buyurtma: {last_order_text}"
            )
        else:
            profile_text = (
                "🔄 <b>Обновленные данные профиля:</b>\n\n"
                f"📱 <b>Telegram ID:</b> {profile.get('telegram_id', 'Неизвестно')}\n"
                f"👤 <b>Ф.И.О:</b> {profile.get('full_name', 'Не указано')}\n"
                f"📞 <b>Телефон:</b> {profile.get('phone', 'Не указано')}\n"
                f"📍 <b>Адрес:</b> {profile.get('address', 'Не указано')}\n"
                f"🌐 <b>Язык:</b> {'Узбекский' if lang == 'uz' else 'Русский'}\n"
                f"📅 <b>Дата регистрации:</b> {formatted_date}\n"
                f"🕒 <b>Последнее обновление:</b> {profile.get('updated_at', 'Неизвестно')}\n\n"
                f"📊 <b>Статистика:</b>\n"
                f"• Активные заказы: {stats.get('active_orders', 0) if stats else 0}\n"
                f"• Выполненные заказы: {stats.get('completed_orders', 0) if stats else 0}\n"
                f"• Всего заказов: {stats.get('total_orders', 0) if stats else 0}\n"
                f"• Последний заказ: {last_order_text}"
            )
        
        await message.answer(
            text=profile_text,
            parse_mode='HTML'
        )
        
    except Exception as e:
        logger.error(f"Error in show_updated_profile: {e}")

def get_client_profile_router():
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(['👤 Kabinet', '👤 Кабинет']))
    async def client_profile_handler(message: Message, state: FSMContext):
        """Cabinet entry with reply keyboard"""
        try:
            # Get user from Redis cache
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return

            lang = user.get('language', 'uz')
            region = user.get('region', 'toshkent')
            if region:
                region = region.lower()
            else:
                region = 'toshkent'
            
            # Save region in state
            await state.update_data(user_region=region)
            
            profile_text = (
                "👤 Kabinet. Amalni tanlang." if lang == 'uz' else "👤 Кабинет. Выберите действие."
            )

            await message.answer(
                text=profile_text,
                reply_markup=get_client_profile_reply_keyboard(lang)
            )

            await state.set_state(ProfileStates.profile_menu)
            
            # Log action
            await audit_logger.log_action(
                user_id=user['id'],
                action="open_cabinet",
                details={}
            )
            
        except Exception as e:
            logger.error(f"Error in client_profile_handler: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(F.text.in_(["👁️ Ma'lumotlarni ko'rish", "👁️ Просмотр информации"]))
    async def view_profile(message: Message, state: FSMContext):
        """View profile information"""
        try:
            # Get user from Redis cache first
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return
            
            # Get region from state or user
            state_data = await state.get_data()
            region = state_data.get('user_region', user.get('region', 'toshkent'))
            if region:
                region = region.lower()
            else:
                region = 'toshkent'
            pool = await get_db_pool(region)
            
            # Get full profile from database
            profile = await get_user_profile_from_db(pool, message.from_user.id)
            if not profile:
                await message.answer("Profil ma'lumotlari topilmadi.")
                return
            
            # Get statistics
            stats = await get_user_statistics(pool, profile['id'])
            
            lang = profile.get('language', 'uz')
            
            # Format dates
            created_date = profile.get('created_at')
            if created_date:
                if isinstance(created_date, str):
                    created_date = datetime.strptime(created_date, '%Y-%m-%d %H:%M:%S')
                formatted_date = created_date.strftime('%d.%m.%Y')
            else:
                formatted_date = 'Noma\'lum'
            
            # Format last order date
            last_order = stats.get('last_order_date') if stats else None
            if last_order:
                if isinstance(last_order, str):
                    last_order = datetime.strptime(last_order, '%Y-%m-%d %H:%M:%S')
                last_order_text = last_order.strftime('%d.%m.%Y %H:%M')
            else:
                last_order_text = 'Yo\'q'
            
            if lang == 'uz':
                profile_text = (
                    "👤 <b>Mening ma'lumotlarim</b>\n\n"
                    f"📱 <b>Telegram ID:</b> {profile.get('telegram_id', 'Noma\'lum')}\n"
                    f"👤 <b>F.I.O:</b> {profile.get('full_name', 'Kiritilmagan')}\n"
                    f"📞 <b>Telefon:</b> {profile.get('phone', 'Kiritilmagan')}\n"
                    f"📍 <b>Manzil:</b> {profile.get('address', 'Kiritilmagan')}\n"
                    f"🌐 <b>Til:</b> {'O\'zbek' if lang == 'uz' else 'Русский'}\n"
                    f"📅 <b>Ro'yxatdan o'tgan:</b> {formatted_date}\n\n"
                    f"📊 <b>Statistika:</b>\n"
                    f"• Faol buyurtmalar: {stats.get('active_orders', 0) if stats else 0}\n"
                    f"• Bajarilgan buyurtmalar: {stats.get('completed_orders', 0) if stats else 0}\n"
                    f"• Jami buyurtmalar: {stats.get('total_orders', 0) if stats else 0}\n"
                    f"• Oxirgi buyurtma: {last_order_text}"
                )
            else:
                profile_text = (
                    "👤 <b>Мои данные</b>\n\n"
                    f"📱 <b>Telegram ID:</b> {profile.get('telegram_id', 'Неизвестно')}\n"
                    f"👤 <b>Ф.И.О:</b> {profile.get('full_name', 'Не указано')}\n"
                    f"📞 <b>Телефон:</b> {profile.get('phone', 'Не указано')}\n"
                    f"📍 <b>Адрес:</b> {profile.get('address', 'Не указано')}\n"
                    f"🌐 <b>Язык:</b> {'Узбекский' if lang == 'uz' else 'Русский'}\n"
                    f"📅 <b>Дата регистрации:</b> {formatted_date}\n\n"
                    f"📊 <b>Статистика:</b>\n"
                    f"• Активные заказы: {stats.get('active_orders', 0) if stats else 0}\n"
                    f"• Выполненные заказы: {stats.get('completed_orders', 0) if stats else 0}\n"
                    f"• Всего заказов: {stats.get('total_orders', 0) if stats else 0}\n"
                    f"• Последний заказ: {last_order_text}"
                )

            await message.answer(
                text=profile_text,
                parse_mode='HTML',
            )
            
        except Exception as e:
            logger.error(f"Error in view_profile: {e}")
            await message.answer("❌ Xatolik yuz berdi.")

    @router.message(F.text.in_(["✏️ Ma'lumotlarni tahrirlash", "✏️ Редактировать данные"]))
    async def edit_profile_menu(message: Message, state: FSMContext):
        """Show edit profile menu"""
        try:
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return

            lang = user.get('language', 'uz')
            
            if lang == 'uz':
                text = "✏️ Qaysi ma'lumotni tahrirlashni xohlaysiz?"
            else:
                text = "✏️ Какую информацию вы хотите редактировать?"

            await message.answer(
                text=text,
                reply_markup=get_edit_profile_keyboard(lang)
            )
            
            await state.set_state(ProfileStates.editing)
            
        except Exception as e:
            logger.error(f"Error in edit_profile_menu: {e}")
            await message.answer("❌ Xatolik yuz berdi.")

    @router.callback_query(F.data.startswith("edit_"))
    async def handle_edit_profile(callback: CallbackQuery, state: FSMContext):
        """Handle profile edit callbacks"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id_redis(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi.", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            field = callback.data.split("edit_")[1]  # Extract field name from edit_*
            
            # Save field to edit in state
            await state.update_data(editing_field=field)
            
            # Get prompt text based on field
            prompts = {
                'name': {
                    'uz': "👤 Yangi F.I.O ni kiriting:",
                    'ru': "👤 Введите новое Ф.И.О:"
                },
                'address': {
                    'uz': "📍 Yangi manzilni kiriting:",
                    'ru': "📍 Введите новый адрес:"
                }
            }
            
            prompt_text = prompts.get(field, {}).get(lang, "Ma'lumot kiriting:")
            
            await callback.message.answer(prompt_text)
            await state.set_state(ProfileStates.waiting_for_input)
            
        except Exception as e:
            logger.error(f"Error in handle_edit_profile: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(ProfileStates.waiting_for_input)
    async def process_profile_edit(message: Message, state: FSMContext):
        """Process profile edit input"""
        try:
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            if not user:
                await message.answer("Foydalanuvchi topilmadi.")
                return
            
            lang = user.get('language', 'uz')
            state_data = await state.get_data()
            field = state_data.get('editing_field')
            region = state_data.get('user_region', user.get('region', 'toshkent')).lower()
            
            if not field:
                await message.answer("Xatolik: tahrirlash maydoni topilmadi.")
                return
            
            # Get database pool
            pool = await get_db_pool(region)
            
            # Map field names
            field_map = {
                'name': 'full_name',
                'phone': 'phone',
                'address': 'address'
            }
            
            db_field = field_map.get(field)
            
            # Validate input based on field
            new_value = message.text.strip()
            
            if field == 'name':
                # Basic name validation
                if not new_value or len(new_value) < 2:
                    error_text = (
                        "❌ Ism juda qisqa. Kamida 2 ta harf bo'lishi kerak."
                        if lang == 'uz' else
                        "❌ Имя слишком короткое. Должно быть минимум 2 символа."
                    )
                    await message.answer(error_text)
                    return
                if len(new_value) > 100:
                    error_text = (
                        "❌ Ism juda uzun. 100 ta harfdan kam bo'lishi kerak."
                        if lang == 'uz' else
                        "❌ Имя слишком длинное. Должно быть меньше 100 символов."
                    )
                    await message.answer(error_text)
                    return
            
            if field == 'phone':
                # Basic phone validation
                if not new_value.startswith('+998') or len(new_value) != 13:
                    error_text = (
                        "❌ Noto'g'ri telefon formati. +998 bilan boshlanishi kerak."
                        if lang == 'uz' else
                        "❌ Неверный формат телефона. Должен начинаться с +998."
                    )
                    await message.answer(error_text)
                    return
            
            # Update in database
            success = await update_user_profile(pool, message.from_user.id, db_field, new_value)
            
            if success:
                success_text = (
                    "✅ Ma'lumot muvaffaqiyatli yangilandi!"
                    if lang == 'uz' else
                    "✅ Данные успешно обновлены!"
                )
                
                # Log action
                await audit_logger.log_action(
                    user_id=user['id'],
                    action="update_profile",
                    details={"field": field, "new_value": new_value}
                )
                
                # Show updated profile
                await show_updated_profile(message, user, lang)
            else:
                success_text = (
                    "❌ Ma'lumotni yangilashda xatolik."
                    if lang == 'uz' else
                    "❌ Ошибка при обновлении данных."
                )
            
            await message.answer(
                success_text,
                reply_markup=get_client_profile_reply_keyboard(lang)
            )
            
            await state.set_state(ProfileStates.profile_menu)
            
        except Exception as e:
            logger.error(f"Error in process_profile_edit: {e}")
            await message.answer("❌ Xatolik yuz berdi.")

    @router.message(F.text.in_(["🔙 Orqaga", "🔙 Назад"]), ProfileStates.profile_menu)
    async def back_to_main_menu(message: Message, state: FSMContext):
        """Return to main menu"""
        try:
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            lang = user.get('language', 'uz') if user else 'uz'
            
            back_text = (
                "Asosiy menyuga qaytdingiz." if lang == 'uz' else "Вы вернулись в главное меню."
            )
            
            await message.answer(
                text=back_text,
                reply_markup=get_main_menu_keyboard(lang)
            )
            
            await state.clear()
            
        except Exception as e:
            logger.error(f"Error in back_to_main_menu: {e}")
            await message.answer("❌ Xatolik yuz berdi.")


    return router
