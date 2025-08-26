"""
Applications List Handler - Mock Data Implementation

Bu modul manager uchun arizalar ro'yxati va navigatsiya funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_manager_view_applications_keyboard, get_manager_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime
from filters.role_filter import RoleFilter
import logging

logger = logging.getLogger(__name__)

# Mock data storage
mock_applications = [
    {
        'id': 'req_001_2024_01_15',
        'workflow_type': 'connection_request',
        'current_status': 'in_progress',
        'role_current': 'manager',
        'contact_info': {
            'full_name': 'Aziz Karimov',
            'phone': '+998901234567'
        },
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'description': 'Internet ulanish arizasi - yangi uy uchun internet xizmatini ulashish kerak',
        'location': 'Tashkent, Chorsu tumani, 15-uy',
        'priority': 'high',
        'estimated_time': '2-3 kun',
        'technician': 'Ahmad Karimov',
        'region': 'Toshkent shahri',
        'address': 'Chorsu tumani, 15-uy',
        'client_id': 123456789
    },
    {
        'id': 'req_002_2024_01_16',
        'workflow_type': 'technical_service',
        'current_status': 'created',
        'role_current': 'manager',
        'contact_info': {
            'full_name': 'Malika Toshmatova',
            'phone': '+998901234568'
        },
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'description': 'TV signal muammosi - TV kanallar ko\'rinmayapti, signal zaif',
        'location': 'Tashkent, Yunusabad tumani, 25-uy',
        'priority': 'normal',
        'estimated_time': '1-2 kun',
        'technician': 'Bekzod Azimov',
        'region': 'Toshkent shahri',
        'address': 'Yunusobod tumani, 25-uy',
        'client_id': 123456790
    },
    {
        'id': 'req_003_2024_01_17',
        'workflow_type': 'call_center_direct',
        'current_status': 'completed',
        'role_current': 'manager',
        'contact_info': {
            'full_name': 'Jahongir Azimov',
            'phone': '+998901234569'
        },
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'description': 'Qo\'ng\'iroq markazi arizasi - mijoz xizmat sifatini yaxshilash haqida',
        'location': 'Tashkent, Sergeli tumani, 8-uy',
        'priority': 'low',
        'estimated_time': '1 kun',
        'technician': 'Karim Karimov',
        'region': 'Toshkent shahri',
        'address': 'Sergeli tumani, 8-uy',
        'client_id': 123456791
    },
    {
        'id': 'req_004_2024_01_18',
        'workflow_type': 'connection_request',
        'current_status': 'created',
        'role_current': 'manager',
        'contact_info': {
            'full_name': 'Umar Toshmatov',
            'phone': '+998901234570'
        },
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'description': 'Yangi internet paketini qo\'shish - 100 Mbit/s tezlikda',
        'location': 'Tashkent, Chilanzor tumani, 30-uy',
        'priority': 'urgent',
        'estimated_time': '1 kun',
        'technician': 'Malik Toshmatov',
        'region': 'Toshkent shahri',
        'address': 'Chilanzor tumani, 30-uy',
        'client_id': 123456792
    }
]

mock_users = {
    1: {
        'id': 1,
        'telegram_id': 123456789,
        'role': 'manager',
        'language': 'uz',
        'full_name': 'Test Manager',
        'phone_number': '+998901234567'
    }
}

# Mock functions
async def find_user_by_telegram_id(telegram_id: int):
    """Mock find user by telegram ID"""
    for user in mock_users.values():
        if user.get('telegram_id') == telegram_id:
            return user
    return None

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    user = await find_user_by_telegram_id(telegram_id)
    return user.get('language', 'uz') if user else 'uz'

# Mock workflow access control
class MockWorkflowAccessControl:
    """Mock workflow access control"""
    async def get_filtered_requests_for_role(self, user_id: int, user_role: str, region: str = 'toshkent'):
        """Mock get filtered requests for role"""
        try:
            # Return mock applications filtered by role
            if user_role == 'manager':
                # Manager uchun barcha arizalarni qaytarish (role_current'ga qaramasdan)
                return mock_applications
            else:
                return mock_applications
        except Exception as e:
            logger.error(f"Mock: Error getting applications: {e}")
            return []

def get_manager_applications_list_router():
    """Router for applications list with mock data"""
    router = Router()
    
    # Apply role filter - both manager and junior_manager can access
    role_filter = RoleFilter(["manager", "junior_manager"])
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.message(F.text.in_(["📋 Arizalar ro'yxati"]), flags={"block": False})
    async def show_applications_list(message: Message, state: FSMContext):
        """Show applications list using mock data"""
        try:
            # Get user
            user = await find_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("❌ Foydalanuvchi topilmadi")
                return
            
            # Get region from state or default
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Get mock applications
            access_control = MockWorkflowAccessControl()
            applications = await access_control.get_filtered_requests_for_role(
                user_id=user['id'],
                user_role='manager',
                region=region
            )
            
            if not applications:
                text = "📭 Arizalar topilmadi"
                keyboard = get_manager_back_keyboard(lang=user.get('language', 'uz'))
                await message.answer(text, reply_markup=keyboard)
                return
            
            # Update state with applications
            await state.update_data(
                applications=applications,
                current_index=0,
                region=region
            )
            
            # Display first application
            await display_application_list(message, state, applications, 0, user)
            
        except Exception as e:
            logger.error(f"Error in show_applications_list: {e}")
            await message.answer("Xatolik yuz berdi")
    
    @router.callback_query(F.data.startswith("list_"))
    async def handle_list_action(callback: CallbackQuery, state: FSMContext):
        """Handle list actions using mock data"""
        try:
            await callback.answer()
            
            # Extract action and data
            action_data = callback.data.replace("list_", "")
            parts = action_data.split("_")
            action = parts[0]
            
            # Get user
            user = await find_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Get applications from state
            state_data = await state.get_data()
            applications = state_data.get('applications', [])
            current_index = state_data.get('current_index', 0)
            
            if not applications or current_index >= len(applications):
                await callback.answer("Arizalar topilmadi", show_alert=True)
                return
            
            if action == "next":
                # Go to next application
                if current_index < len(applications) - 1:
                    new_index = current_index + 1
                    await state.update_data(current_index=new_index)
                    await display_application_list(callback.message, state, applications, new_index, user)
                else:
                    await callback.answer("Oxirgi ariza", show_alert=True)
                    
            elif action == "prev":
                # Go to previous application
                if current_index > 0:
                    new_index = current_index - 1
                    await state.update_data(current_index=new_index)
                    await display_application_list(callback.message, state, applications, new_index, user)
                else:
                    await callback.answer("Birinchi ariza", show_alert=True)
                    
            elif action == "view":
                # View application details
                await show_application_details(callback, state, applications[current_index], user)
                
            else:
                await callback.answer("Noma'lum amal", show_alert=True)
                
        except Exception as e:
            logger.error(f"Error in handle_list_action: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    async def display_application_list(event, state: FSMContext, applications: List[Dict], index: int, user: Dict):
        """Display application in list format using mock data"""
        try:
            app = applications[index]
            
            # Get client info
            client_name = 'Unknown'
            client_phone = 'N/A'
            if app.get('contact_info'):
                client_name = app['contact_info'].get('full_name', 'Unknown')
                client_phone = app['contact_info'].get('phone', 'N/A')
            
            # Format workflow type
            workflow_type_names = {
                'connection_request': '🔌 Ulanish arizasi',
                'technical_service': '🔧 Texnik xizmat',
                'call_center_direct': '📞 Qo\'ng\'iroq markazi'
            }
            
            workflow_type = workflow_type_names.get(app.get('workflow_type'), f"📋 {app.get('workflow_type', 'Ariza')}")
            
            # Format status
            status_names = {
                'created': '🆕 Yaratilgan',
                'in_progress': '⏳ Jarayonda',
                'completed': '✅ Tugallangan',
                'cancelled': '❌ Bekor qilingan'
            }
            
            status = status_names.get(app.get('current_status'), f"📋 {app.get('current_status', 'Noma\'lum')}")
            
            # Format priority
            priority_emoji = {
                'low': '🔵',
                'normal': '🟢',
                'high': '🔴',
                'urgent': '🚨'
            }.get(app.get('priority'), '🟢')
            
            # Format date
            created_date = app.get('created_at')
            if hasattr(created_date, 'strftime'):
                created_date = created_date.strftime('%d.%m.%Y %H:%M')
            else:
                created_date = str(created_date)
            
            # Create text
            text = (
                f"📋 <b>Ariza #{index + 1} / {len(applications)}</b>\n\n"
                f"{workflow_type}\n"
                f"{status}\n"
                f"{priority_emoji} <b>Muhimlik:</b> {app.get('priority', 'normal').title()}\n\n"
                f"👤 <b>Mijoz:</b> {client_name}\n"
                f"📞 <b>Telefon:</b> {client_phone}\n"
                f"📍 <b>Manzil:</b> {app.get('location', 'N/A')}\n"
                f"📅 <b>Yaratilgan:</b> {created_date}\n"
                f"📝 <b>Tavsif:</b> {app.get('description', 'Tavsif yo\'q')[:80]}{'...' if app.get('description') and len(app.get('description', '')) > 80 else ''}\n\n"
                f"🆔 <b>ID:</b> {app.get('id', 'N/A')}"
            )
            
            # Create navigation keyboard
            keyboard = get_manager_view_applications_keyboard(
                has_prev=index > 0,
                has_next=index < len(applications) - 1,
                app_id=app.get('id'),
                lang=user.get('language', 'uz')
            )
            
            if hasattr(event, 'edit_text'):
                await event.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await event.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in display_application_list: {e}")
            if hasattr(event, 'answer'):
                await event.answer("Xatolik yuz berdi")
    
    async def show_application_details(callback: CallbackQuery, state: FSMContext, app: Dict, user: Dict):
        """Show detailed application information using mock data"""
        try:
            # Get client info
            client_name = 'Unknown'
            client_phone = 'N/A'
            if app.get('contact_info'):
                client_name = app['contact_info'].get('full_name', 'Unknown')
                client_phone = app['contact_info'].get('phone', 'N/A')
            
            # Format workflow type
            workflow_type_names = {
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Qo\'ng\'iroq markazi'
            }
            
            workflow_type = workflow_type_names.get(app.get('workflow_type'), app.get('workflow_type', 'Ariza'))
            
            # Format status
            status_names = {
                'created': 'Yaratilgan',
                'in_progress': 'Jarayonda',
                'completed': 'Tugallangan',
                'cancelled': 'Bekor qilingan'
            }
            
            status = status_names.get(app.get('current_status'), app.get('current_status', 'Noma\'lum'))
            
            # Format priority
            priority_names = {
                'low': 'Past',
                'normal': 'O\'rtacha',
                'high': 'Yuqori',
                'urgent': 'Shoshilinch'
            }
            
            priority = priority_names.get(app.get('priority'), app.get('priority', 'normal').title())
            
            # Format date
            created_date = app.get('created_at')
            if hasattr(created_date, 'strftime'):
                created_date = created_date.strftime('%d.%m.%Y %H:%M')
            else:
                created_date = str(created_date)
            
            # Create detailed text
            text = (
                f"📋 <b>Ariza tafsilotlari</b>\n\n"
                f"🆔 <b>ID:</b> {app.get('id', 'N/A')}\n"
                f"📝 <b>Tur:</b> {workflow_type}\n"
                f"📊 <b>Holat:</b> {status}\n"
                f"🔴 <b>Muhimlik:</b> {priority}\n\n"
                f"👤 <b>Mijoz ma'lumotlari:</b>\n"
                f"• Nomi: {client_name}\n"
                f"• Telefon: {client_phone}\n"
                f"• Manzil: {app.get('location', 'N/A')}\n\n"
                f"📅 <b>Vaqt ma'lumotlari:</b>\n"
                f"• Yaratilgan: {created_date}\n"
                f"• Taxminiy muddat: {app.get('estimated_time', 'N/A')}\n\n"
                f"📝 <b>Tavsif:</b>\n{app.get('description', 'Tavsif yo\'q')}\n\n"
                f"🔧 <b>Texnik ma'lumotlar:</b>\n"
                f"• Texnik: {app.get('technician', 'N/A')}\n"
                f"• Hudud: {app.get('region', 'N/A')}\n"
                f"• To'liq manzil: {app.get('address', 'N/A')}"
            )
            
            # Create back button
            keyboard = get_manager_back_keyboard(lang=user.get('language', 'uz'))
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in show_application_details: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "back_to_applications")
    async def back_to_applications(callback: CallbackQuery, state: FSMContext):
        """Go back to applications list"""
        try:
            await callback.answer()
            
            # Get user
            user = await find_user_by_telegram_id(callback.from_user.id)
            if not user:
                return
            
            # Get applications from state
            state_data = await state.get_data()
            applications = state_data.get('applications', [])
            current_index = state_data.get('current_index', 0)
            
            if applications:
                await display_application_list(callback.message, state, applications, current_index, user)
            else:
                # If no applications, show empty message
                text = "📭 Arizalar topilmadi"
                keyboard = get_manager_back_keyboard(lang=user.get('language', 'uz'))
                await callback.message.edit_text(text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in back_to_applications: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "back_to_main")
    async def back_to_main(callback: CallbackQuery, state: FSMContext):
        """Go back to main menu"""
        try:
            await callback.answer()
            
            # Get user
            user = await find_user_by_telegram_id(callback.from_user.id)
            if not user:
                return
            
            # Clear applications from state
            await state.update_data(applications=None, current_index=None)
            
            # Import and show main keyboard
            from keyboards.manager_buttons import get_manager_main_keyboard
            keyboard = get_manager_main_keyboard(lang=user.get('language', 'uz'))
            text = "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:"
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in back_to_main: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    # Additional mock handlers for backward compatibility
    @router.message(F.text.in_(["📋 Hammasini ko'rish"]), flags={"block": False})
    async def view_all_applications(message: Message, state: FSMContext):
        """Manager view all applications handler"""
        try:
            user = await find_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            lang = user.get('language', 'uz')
            
            # Use mock workflow access control to get filtered requests for manager role
            access_control = MockWorkflowAccessControl()
            applications = await access_control.get_filtered_requests_for_role(message.from_user.id, 'manager')
            
            if not applications:
                await message.answer("Hozircha arizalar yo'q.")
                return
            
            # Show first application
            await show_application_details(message, applications[0], applications, 0)
            
        except Exception as e:
            logger.error(f"Error in view_all_applications: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def show_application_details(message_or_callback, application, applications, index):
        """Show application details with navigation"""
        try:
            # Format workflow type
            workflow_type_emoji = {
                'connection_request': '🔌',
                'technical_service': '🔧',
                'call_center_direct': '📞'
            }.get(application['workflow_type'], '📄')
            
            workflow_type_text = {
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Call Center'
            }.get(application['workflow_type'], 'Boshqa')
            
            # Format status
            status_emoji = {
                'in_progress': '🟡',
                'created': '🟠',
                'completed': '🟢',
                'cancelled': '🔴'
            }.get(application['current_status'], '⚪')
            
            status_text = {
                'in_progress': 'Jarayonda',
                'created': 'Yaratilgan',
                'completed': 'Bajarilgan',
                'cancelled': 'Bekor qilingan'
            }.get(application['current_status'], 'Noma\'lum')
            
            # Format priority
            priority_emoji = {
                'high': '🔴',
                'normal': '🟡',
                'low': '🟢'
            }.get(application.get('priority', 'normal'), '🟡')
            
            priority_text = {
                'high': 'Yuqori',
                'normal': 'O\'rtacha',
                'low': 'Past'
            }.get(application.get('priority', 'normal'), 'O\'rtacha')
            
            # Format dates
            created_date = application['created_at'].strftime('%d.%m.%Y %H:%M')
            updated_date = application['updated_at'].strftime('%d.%m.%Y %H:%M')
            
            # To'liq ma'lumot
            text = (
                f"{workflow_type_emoji} <b>{workflow_type_text} - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"📅 <b>Yaratilgan:</b> {created_date}\n"
                f"🔄 <b>Yangilangan:</b> {updated_date}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"🏛️ <b>Hudud:</b> {application.get('region', 'Noma\'lum')}\n"
                f"🏠 <b>Manzil:</b> {application.get('address', 'Noma\'lum')}\n"
                f"📝 <b>Tavsif:</b> {application['description']}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"👨‍🔧 <b>Texnik:</b> {application.get('technician', 'Tayinlanmagan')}\n"
                f"⏰ <b>Taxminiy vaqt:</b> {application.get('estimated_time', 'Noma\'lum')}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n\n"
                f"📊 <b>Ariza #{index + 1} / {len(applications)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_applications_navigation_keyboard(index, len(applications))
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            logger.error(f"Error in show_application_details: {e}")
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_prev_application")
    async def show_previous_application(callback: CallbackQuery, state: FSMContext):
        """Show previous application"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            access_control = MockWorkflowAccessControl()
            applications = await access_control.get_filtered_requests_for_role(callback.from_user.id, 'manager')
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu birinchi ariza")
                
        except Exception as e:
            logger.error(f"Error in show_previous_application: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_next_application")
    async def show_next_application(callback: CallbackQuery, state: FSMContext):
        """Show next application"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            access_control = MockWorkflowAccessControl()
            applications = await access_control.get_filtered_requests_for_role(callback.from_user.id, 'manager')
            
            if current_index < len(applications) - 1:
                new_index = current_index + 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu oxirgi ariza")
                
        except Exception as e:
            logger.error(f"Error in show_next_application: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_view_all_applications")
    async def view_all_applications_callback(callback: CallbackQuery, state: FSMContext):
        """View all applications from callback"""
        try:
            await callback.answer()
            
            user = await find_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            access_control = MockWorkflowAccessControl()
            applications = await access_control.get_filtered_requests_for_role(callback.from_user.id, 'manager')
            
            if not applications:
                await callback.message.edit_text("Hozircha arizalar yo'q.")
                return
            
            # Reset index to 0
            await state.update_data(current_app_index=0)
            await show_application_details(callback, applications[0], applications, 0)
            
        except Exception as e:
            logger.error(f"Error in view_all_applications_callback: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "mgr_view_active_applications")
    async def view_active_applications_callback(callback: CallbackQuery, state: FSMContext):
        """View active applications from callback"""
        try:
            await callback.answer()
            
            user = await find_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            access_control = MockWorkflowAccessControl()
            all_applications = await access_control.get_filtered_requests_for_role(callback.from_user.id, 'manager')
            
            # Filter active applications
            active_applications = [app for app in all_applications if app.get('current_status') in ['created', 'in_progress']]
            
            if not active_applications:
                await callback.message.edit_text("Hozircha faol arizalar yo'q.")
                return
            
            # Reset index to 0
            await state.update_data(current_app_index=0)
            await show_application_details(callback, active_applications[0], active_applications, 0)
            
        except Exception as e:
            logger.error(f"Error in view_active_applications_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_view_completed_applications")
    async def view_completed_applications_callback(callback: CallbackQuery, state: FSMContext):
        """View completed applications from callback"""
        try:
            await callback.answer()
            
            user = await find_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                return
            
            access_control = MockWorkflowAccessControl()
            all_applications = await access_control.get_filtered_requests_for_role(callback.from_user.id, 'manager')
            
            # Filter completed applications
            completed_applications = [app for app in all_applications if app.get('current_status') == 'completed']
            
            if not completed_applications:
                await callback.message.edit_text("Hozircha bajarilgan arizalar yo'q.")
                return
            
            # Reset index to 0
            await state.update_data(current_app_index=0)
            await show_application_details(callback, completed_applications[0], completed_applications, 0)
            
        except Exception as e:
            logger.error(f"Error in view_completed_applications_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router

def get_applications_navigation_keyboard(current_index: int, total_applications: int):
    """Create navigation keyboard for applications"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="mgr_prev_application"
        ))
    
    # Next button
    if current_index < total_applications - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="mgr_next_application"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 