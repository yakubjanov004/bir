"""
Manager Status Management Handler - Mock Data Version

This module provides complete status management functionality for Manager role,
allowing managers to change application statuses according to workflow.
Mock data bilan ishlaydi, test qilish uchun.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime
import logging
import json
from typing import List, Dict, Any, Optional

from keyboards.manager_buttons import (
    get_status_keyboard, 
    get_manager_main_keyboard,
    get_status_management_keyboard,
    get_status_navigation_keyboard,
    get_status_confirmation_keyboard
)
from states.manager_states import ManagerStatusStates
from filters.role_filter import RoleFilter

logger = logging.getLogger(__name__)

# Mock data for testing
MOCK_APPLICATIONS = [
    {
        'id': 1,
        'client_id': 101,
        'client_name': 'Aziz Karimov',
        'client_phone': '+998901234567',
        'location': 'Toshkent, Chilonzor',
        'current_status': 'created',
        'created_at': '2024-01-15 10:30:00',
        'description': 'Internet ulanish muammosi'
    },
    {
        'id': 2,
        'client_id': 102,
        'client_name': 'Malika Yusupova',
        'client_phone': '+998901234568',
        'location': 'Toshkent, Sergeli',
        'current_status': 'assigned',
        'created_at': '2024-01-14 14:20:00',
        'description': 'Televizor signal muammosi'
    },
    {
        'id': 3,
        'client_id': 103,
        'client_name': 'Jasur Toshmatov',
        'client_phone': '+998901234569',
        'location': 'Toshkent, Yakkasaroy',
        'current_status': 'in_progress',
        'created_at': '2024-01-13 09:15:00',
        'description': 'Telefon xizmati'
    },
    {
        'id': 4,
        'client_id': 104,
        'client_name': 'Dilfuza Rahimova',
        'client_phone': '+998901234570',
        'location': 'Toshkent, Shayxontohur',
        'current_status': 'pending',
        'created_at': '2024-01-12 16:45:00',
        'description': 'Internet tezligi past'
    },
    {
        'id': 5,
        'client_id': 105,
        'client_name': 'Rustam Alimov',
        'client_phone': '+998901234571',
        'location': 'Toshkent, Uchtepa',
        'current_status': 'completed',
        'created_at': '2024-01-11 11:30:00',
        'description': 'Kabellar almashtirildi'
    }
]

MOCK_USERS = {
    101: {'full_name': 'Aziz Karimov', 'phone': '+998901234567'},
    102: {'full_name': 'Malika Yusupova', 'phone': '+998901234568'},
    103: {'full_name': 'Jasur Toshmatov', 'phone': '+998901234569'},
    104: {'full_name': 'Dilfuza Rahimova', 'phone': '+998901234570'},
    105: {'full_name': 'Rustam Alimov', 'phone': '+998901234571'}
}

# Status workflow configuration
STATUS_WORKFLOW = {
    'created': ['assigned', 'cancelled'],
    'assigned': ['in_progress', 'transferred', 'cancelled'],
    'in_progress': ['completed', 'pending', 'cancelled'],
    'pending': ['in_progress', 'cancelled'],
    'completed': [],  # Terminal state
    'cancelled': ['created'],  # Can reopen
    'transferred': ['assigned', 'in_progress'],
}

# Status display names
STATUS_DISPLAY = {
    'uz': {
        'created': '🆕 Yangi',
        'assigned': '👤 Tayinlangan',
        'in_progress': '⏳ Jarayonda',
        'pending': '⏸️ Kutilmoqda',
        'completed': '✅ Bajarilgan',
        'cancelled': '❌ Bekor qilingan',
        'transferred': '↔️ O\'tkazilgan'
    },
    'ru': {
        'created': '🆕 Новая',
        'assigned': '👤 Назначена',
        'in_progress': '⏳ В процессе',
        'pending': '⏸️ Ожидание',
        'completed': '✅ Выполнена',
        'cancelled': '❌ Отменена',
        'transferred': '↔️ Передана'
    }
}

# Mock functions for database operations
async def find_user_by_telegram_id(telegram_id: int) -> Dict:
    """Mock function to find user by telegram ID"""
    return {
        'id': telegram_id,
        'full_name': f'Manager {telegram_id}',
        'language': 'uz',
        'role': 'manager'
    }

async def get_manager_applications(region_code: str, manager_id: int, limit: int = 50) -> List[Dict]:
    """Mock function to get manager applications"""
    return MOCK_APPLICATIONS[:limit]

async def get_application_statistics(region: str, manager_id: int = None) -> Dict[str, Any]:
    """Mock function to get application statistics"""
    # Count applications by status
    status_counts = {}
    for app in MOCK_APPLICATIONS:
        status = app['current_status']
        status_counts[f'{status}_count'] = status_counts.get(f'{status}_count', 0) + 1
    
    return status_counts

async def update_application_status_with_history(request_id: int, new_status: str, updated_by: int, comments: str) -> bool:
    """Mock function to update application status"""
    # Find and update application
    for app in MOCK_APPLICATIONS:
        if app['id'] == request_id:
            app['current_status'] = new_status
            app['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            app['updated_by'] = updated_by
            app['comments'] = comments
            return True
    return False

async def audit_logger_log_action(user_id: int, action: str, target_id: int, details: str):
    """Mock function for audit logging"""
    logger.info(f"Mock Audit Log: User {user_id} performed {action} on {target_id}: {details}")

# Calculate status change statistics
async def calculate_status_statistics(region: str, manager_id: int = None) -> Dict[str, Any]:
    """Calculate statistics for status changes using mock data"""
    try:
        stats = await get_application_statistics(region, manager_id)
        
        # Group by status
        status_counts = {}
        for status in ['created', 'assigned', 'in_progress', 'pending', 'completed', 'cancelled']:
            status_counts[status] = stats.get(f'{status}_count', 0)
        
        # Calculate percentages
        total = sum(status_counts.values())
        if total > 0:
            for status in status_counts:
                status_counts[f'{status}_percent'] = round((status_counts[status] / total) * 100, 1)
        
        return {
            'total': total,
            'status_counts': status_counts,
            'last_updated': datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error calculating status statistics: {e}")
        return {
            'total': 0,
            'status_counts': {},
            'last_updated': datetime.now()
        }

def get_manager_status_management_router():
    """Router for status management with mock data"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.message(F.text.in_(["📊 Status boshqaruvi"]))
    async def show_status_management(message: Message, state: FSMContext):
        """Show status management menu using mock data"""
        try:
            # Get user
            user = await find_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("❌ Foydalanuvchi topilmadi")
                return
            
            # Get region from state or default
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Update state
            await state.update_data(status_region=region)
            
            # Show status management keyboard
            keyboard = get_status_management_keyboard(lang=user.get('language', 'uz'))
            text = (
                f"📊 <b>Status boshqaruvi</b>\n\n"
                f"📍 Hudud: {region.title()}\n\n"
                f"Kerakli amalni tanlang:"
            )
            
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in show_status_management: {e}")
            await message.answer("Xatolik yuz berdi")
    
    @router.callback_query(F.data == "view_status_statistics")
    async def view_status_statistics(callback: CallbackQuery, state: FSMContext):
        """View status statistics using mock data"""
        try:
            await callback.answer()
            
            # Get user
            user = await find_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('status_region', 'toshkent')
            
            # Calculate statistics from mock data
            stats = await calculate_status_statistics(region, user.get('id'))
            
            if not stats or stats['total'] == 0:
                text = "📊 <b>Status statistikasi</b>\n\n❌ Ma'lumotlar topilmadi"
                keyboard = get_manager_back_keyboard(lang=user.get('language', 'uz'))
                await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                return
            
            # Format statistics
            lang = user.get('language', 'uz')
            status_names = STATUS_DISPLAY.get(lang, STATUS_DISPLAY['uz'])
            
            text = f"📊 <b>Status statistikasi</b>\n\n📍 Hudud: {region.title()}\n\n"
            
            for status, count in stats['status_counts'].items():
                if not status.endswith('_percent'):
                    percent = stats['status_counts'].get(f'{status}_percent', 0)
                    emoji = status_names.get(status, '📋')
                    text += f"{emoji} {status.title()}: {count} ({percent}%)\n"
            
            text += f"\n📈 Jami: {stats['total']}\n"
            text += f"🕐 Yangilangan: {stats['last_updated'].strftime('%d.%m.%Y %H:%M')}"
            
            # Create back button
            keyboard = get_manager_back_keyboard(lang=user.get('language', 'uz'))
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in view_status_statistics: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "change_application_status")
    async def change_application_status(callback: CallbackQuery, state: FSMContext):
        """Change application status using mock data"""
        try:
            await callback.answer()
            
            # Get user
            user = await find_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('status_region', 'toshkent')
            
            # Get applications from mock data
            applications = await get_manager_applications(
                region_code=region,
                manager_id=user.get('id'),
                limit=50
            )
            
            if not applications:
                text = "📭 Arizalar topilmadi"
                keyboard = get_manager_back_keyboard(lang=user.get('language', 'uz'))
                await callback.message.edit_text(text, reply_markup=keyboard)
                return
            
            # Update state with applications
            await state.update_data(
                status_applications=applications,
                current_status_index=0,
                status_region=region
            )
            
            # Display first application for status change
            await display_application_for_status_change(callback, state, applications, 0, user)
            
        except Exception as e:
            logger.error(f"Error in change_application_status: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    async def display_application_for_status_change(callback: CallbackQuery, state: FSMContext, applications: List[Dict], index: int, user: Dict):
        """Display application for status change using mock data"""
        try:
            app = applications[index]
            
            # Get client info from mock data
            client_name = app.get('client_name', 'Unknown')
            client_phone = app.get('client_phone', 'N/A')
            
            # Get current status
            current_status = app.get('current_status', 'created')
            
            # Get available next statuses
            next_statuses = STATUS_WORKFLOW.get(current_status, [])
            
            # Format status names
            lang = user.get('language', 'uz')
            status_names = STATUS_DISPLAY.get(lang, STATUS_DISPLAY['uz'])
            
            current_status_display = status_names.get(current_status, current_status)
            
            # Create text
            text = (
                f"📊 <b>Status o'zgartirish</b>\n\n"
                f"📝 Ariza ID: {app.get('id', 'N/A')}\n"
                f"👤 Mijoz: {client_name}\n"
                f"📞 Telefon: {client_phone}\n"
                f"📍 Manzil: {app.get('location', 'N/A')}\n"
                f"📋 Hozirgi status: {current_status_display}\n\n"
                f"🔄 Yangi statusni tanlang:"
            )
            
            # Create status selection keyboard
            keyboard = create_status_selection_keyboard(next_statuses, lang)
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in display_application_for_status_change: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    def create_status_selection_keyboard(statuses: List[str], lang: str = 'uz') -> InlineKeyboardMarkup:
        """Create keyboard for status selection"""
        keyboard = []
        
        # Status buttons
        for status in statuses:
            status_names = STATUS_DISPLAY.get(lang, STATUS_DISPLAY['uz'])
            status_display = status_names.get(status, status.title())
            
            keyboard.append([InlineKeyboardButton(
                text=status_display,
                callback_data=f"status_select_{status}"
            )])
        
        # Navigation buttons
        keyboard.append([
            InlineKeyboardButton(text="⬅️ Oldingi", callback_data="status_prev"),
            InlineKeyboardButton(text="Keyingi ➡️", callback_data="status_next")
        ])
        
        # Back button
        keyboard.append([InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="status_back"
        )])
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    @router.callback_query(F.data.startswith("status_select_"))
    async def select_new_status(callback: CallbackQuery, state: FSMContext):
        """Select new status for application using mock data"""
        try:
            await callback.answer()
            
            # Extract new status
            new_status = callback.data.replace("status_select_", "")
            
            # Get user
            user = await find_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Get application from state
            state_data = await state.get_data()
            applications = state_data.get('status_applications', [])
            current_index = state_data.get('current_status_index', 0)
            
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi", show_alert=True)
                return
            
            app = applications[current_index]
            
            # Update state with selected status
            await state.update_data(
                selected_status=new_status,
                current_application_id=app.get('id')
            )
            
            # Show confirmation
            await show_status_change_confirmation(callback, state, app, new_status, user)
            
        except Exception as e:
            logger.error(f"Error in select_new_status: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    async def show_status_change_confirmation(callback: CallbackQuery, state: FSMContext, app: Dict, new_status: str, user: Dict):
        """Show confirmation for status change using mock data"""
        try:
            # Get client info
            client_name = app.get('client_name', 'Unknown')
            
            # Format status names
            lang = user.get('language', 'uz')
            status_names = STATUS_DISPLAY.get(lang, STATUS_DISPLAY['uz'])
            
            current_status_display = status_names.get(app.get('current_status', 'created'), 'created')
            new_status_display = status_names.get(new_status, new_status)
            
            # Create confirmation text
            text = (
                f"✅ <b>Status o'zgartirish tasdiqlash</b>\n\n"
                f"📝 Ariza ID: {app.get('id', 'N/A')}\n"
                f"👤 Mijoz: {client_name}\n"
                f"🔄 Status: {current_status_display} → {new_status_display}\n\n"
                f"Bu o'zgarishni tasdiqlaysizmi?"
            )
            
            # Create confirmation keyboard
            keyboard = get_status_confirmation_keyboard(
                app_id=app.get('id'),
                new_status=new_status,
                lang=lang
            )
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in show_status_change_confirmation: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("status_confirm_"))
    async def confirm_status_change(callback: CallbackQuery, state: FSMContext):
        """Confirm status change using mock data"""
        try:
            await callback.answer()
            
            # Extract data
            parts = callback.data.replace("status_confirm_", "").split("_")
            app_id = int(parts[0])
            new_status = parts[1]
            
            # Get user
            user = await find_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Update application status in mock data
            success = await update_application_status_with_history(
                request_id=app_id,
                new_status=new_status,
                updated_by=user['id'],
                comments=f"Status changed to {new_status} by manager {user.get('full_name', 'N/A')}"
            )
            
            if success:
                # Log the status change
                await audit_logger_log_action(
                    user_id=user['id'],
                    action='change_status',
                    target_id=app_id,
                    details=f"Status changed to {new_status}"
                )
                
                # Format status name
                lang = user.get('language', 'uz')
                status_names = STATUS_DISPLAY.get(lang, STATUS_DISPLAY['uz'])
                new_status_display = status_names.get(new_status, new_status)
                
                text = (
                    f"✅ <b>Status muvaffaqiyatli o'zgartirildi!</b>\n\n"
                    f"📝 Ariza ID: {app_id}\n"
                    f"🔄 Yangi status: {new_status_display}\n"
                    f"👨‍💼 O'zgartiruvchi: {user.get('full_name', 'N/A')}\n\n"
                    f"Status muvaffaqiyatli yangilandi."
                )
                
                # Create back button
                keyboard = get_manager_back_keyboard(lang=lang)
                
                await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
                # Clear state
                await state.clear()
                
            else:
                await callback.answer("Status o'zgartirishda xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            logger.error(f"Error in confirm_status_change: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("status_"))
    async def handle_status_navigation(callback: CallbackQuery, state: FSMContext):
        """Handle status navigation using mock data"""
        try:
            await callback.answer()
            
            # Extract action
            action = callback.data.replace("status_", "")
            
            # Get user
            user = await find_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Get applications from state
            state_data = await state.get_data()
            applications = state_data.get('status_applications', [])
            current_index = state_data.get('current_status_index', 0)
            
            if action == "prev":
                # Go to previous application
                if current_index > 0:
                    new_index = current_index - 1
                    await state.update_data(current_status_index=new_index)
                    await display_application_for_status_change(callback, state, applications, new_index, user)
                else:
                    await callback.answer("Birinchi ariza", show_alert=True)
                    
            elif action == "next":
                # Go to next application
                if current_index < len(applications) - 1:
                    new_index = current_index + 1
                    await state.update_data(current_status_index=new_index)
                    await display_application_for_status_change(callback, state, applications, new_index, user)
                else:
                    await callback.answer("Oxirgi ariza", show_alert=True)
                    
            elif action == "back":
                # Go back to status management menu
                await state.clear()
                await show_status_management(callback.message, state)
                
            else:
                await callback.answer("Noma'lum amal", show_alert=True)
                
        except Exception as e:
            logger.error(f"Error in handle_status_navigation: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "back_to_status")
    async def back_to_status(callback: CallbackQuery, state: FSMContext):
        """Go back to status management menu"""
        try:
            await callback.answer()
            
            # Get user
            user = await find_user_by_telegram_id(callback.from_user.id)
            if not user:
                return
            
            # Clear status state
            await state.update_data(
                status_applications=None,
                current_status_index=None,
                selected_status=None
            )
            
            # Show status management menu
            await show_status_management(callback.message, state)
            
        except Exception as e:
            logger.error(f"Error in back_to_status: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    return router


