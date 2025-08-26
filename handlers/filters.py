"""
Manager Filters Handler - Mock Data Integration

This module handles manager filters functionality using mock data.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_manager_filters_keyboard, get_manager_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
import json

logger = logging.getLogger(__name__)

# Mock data for applications
MOCK_APPLICATIONS = [
    {
        'id': 'APP001',
        'workflow_type': 'connection_request',
        'current_status': 'created',
        'client_id': 'CL001',
        'contact_info': '{"full_name": "Aziz Karimov", "phone": "+998901234567"}',
        'created_at': '2024-01-15T10:30:00Z',
        'description': 'Internet ulanish arizasi',
        'location': 'Toshkent sh., Chilonzor t., 15-uy',
        'priority': 'high',
        'region': 'toshkent'
    },
    {
        'id': 'APP002',
        'workflow_type': 'technical_service',
        'current_status': 'in_progress',
        'client_id': 'CL002',
        'contact_info': '{"full_name": "Malika Yusupova", "phone": "+998901234568"}',
        'created_at': '2024-01-14T14:20:00Z',
        'description': 'Internet tezligi past',
        'location': 'Toshkent sh., Sergeli t., 25-uy',
        'priority': 'normal',
        'region': 'toshkent'
    },
    {
        'id': 'APP003',
        'workflow_type': 'call_center_direct',
        'current_status': 'completed',
        'client_id': 'CL003',
        'contact_info': '{"full_name": "Jasur Toshmatov", "phone": "+998901234569"}',
        'created_at': '2024-01-13T09:15:00Z',
        'description': 'Hisob ma\'lumotlari haqida savol',
        'location': 'Toshkent sh., Yashnobod t., 8-uy',
        'priority': 'low',
        'region': 'toshkent'
    },
    {
        'id': 'APP004',
        'workflow_type': 'connection_request',
        'current_status': 'pending',
        'client_id': 'CL004',
        'contact_info': '{"full_name": "Dilfuza Rahimova", "phone": "+998901234570"}',
        'created_at': '2024-01-12T16:45:00Z',
        'description': 'Yangi uy uchun internet',
        'location': 'Toshkent sh., Uchtepa t., 12-uy',
        'priority': 'high',
        'region': 'toshkent'
    },
    {
        'id': 'APP005',
        'workflow_type': 'technical_service',
        'current_status': 'cancelled',
        'client_id': 'CL005',
        'contact_info': '{"full_name": "Rustam Azimov", "phone": "+998901234571"}',
        'created_at': '2024-01-11T11:30:00Z',
        'description': 'Modem aloqasi yo\'q',
        'location': 'Toshkent sh., Shayxontohur t., 30-uy',
        'priority': 'normal',
        'region': 'toshkent'
    }
]

# Mock data for users
MOCK_USERS = {
    'CL001': {'full_name': 'Aziz Karimov', 'phone': '+998901234567'},
    'CL002': {'full_name': 'Malika Yusupova', 'phone': '+998901234568'},
    'CL003': {'full_name': 'Jasur Toshmatov', 'phone': '+998901234569'},
    'CL004': {'full_name': 'Dilfuza Rahimova', 'phone': '+998901234570'},
    'CL005': {'full_name': 'Rustam Azimov', 'phone': '+998901234571'}
}

async def get_filtered_applications_mock(region: str, filters: dict):
    """Get filtered applications from mock data"""
    try:
        # Extract filter parameters
        status_filter = filters.get('status')
        priority_filter = filters.get('priority')
        date_from = filters.get('date_from')
        date_to = filters.get('date_to')
        workflow_type = filters.get('workflow_type')
        search_term = filters.get('search_term')
        
        # Start with all applications
        applications = MOCK_APPLICATIONS.copy()
        
        # Apply filters
        filtered = []
        for app in applications:
            # Region filter (already filtered by mock data)
            if app.get('region') != region:
                continue
            
            # Status filter
            if status_filter and app.get('current_status') != status_filter:
                continue
            
            # Priority filter
            if priority_filter and app.get('priority') != priority_filter:
                continue
            
            # Date filter
            if date_from or date_to:
                created_at = app.get('created_at')
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                
                if date_from and created_at < date_from:
                    continue
                if date_to and created_at > date_to:
                    continue
            
            # Workflow type filter
            if workflow_type and app.get('workflow_type') != workflow_type:
                continue
            
            # Search term filter
            if search_term:
                search_lower = search_term.lower()
                app_text = f"{app.get('description', '')} {app.get('location', '')}".lower()
                if search_lower not in app_text:
                    continue
            
            # Get client info
            client_name = 'Unknown'
            client_phone = 'N/A'
            if app.get('client_id'):
                client = MOCK_USERS.get(app['client_id'], {})
                if client:
                    client_name = client.get('full_name', 'Unknown')
                    client_phone = client.get('phone', 'N/A')
            
            # Parse contact info if exists
            contact_info = {}
            if app.get('contact_info'):
                try:
                    contact_info = json.loads(app['contact_info']) if isinstance(app['contact_info'], str) else app['contact_info']
                except:
                    contact_info = {}
            
            # Format application data
            app_data = {
                'id': app.get('id', ''),
                'workflow_type': app.get('workflow_type', 'unknown'),
                'current_status': app.get('current_status', 'unknown'),
                'contact_info': {
                    'full_name': contact_info.get('full_name', client_name),
                    'phone': contact_info.get('phone', client_phone)
                },
                'created_at': app.get('created_at', datetime.now()),
                'description': app.get('description', 'Tavsif yo\'q'),
                'location': app.get('location', 'Manzil ko\'rsatilmagan'),
                'priority': app.get('priority', 'normal'),
                'region': region
            }
            
            filtered.append(app_data)
        
        return filtered
        
    except Exception as e:
        logger.error(f"Error getting filtered applications: {e}")
        return []

def get_manager_filters_router():
    """Router for filters functionality"""
    router = Router()

    @router.message(F.text.in_(["🔍 Filtrlar", "🔍 Фильтрация"]))
    async def view_filters(message: Message, state: FSMContext):
        """Manager view filters handler"""
        try:
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Save to state for later use
            await state.update_data(region=region, manager_id=message.from_user.id)
            
            # Default language
            lang = 'uz'
            
            filters_text = (
                "🔍 <b>Filtrlash - To'liq ma'lumot</b>\n\n"
                "📋 <b>Mavjud filtrlash turlari:</b>\n"
                "• Hudud bo'yicha\n"
                "• Holat bo'yicha\n"
                "• Sana bo'yicha\n"
                "• Ustuvorlik bo'yicha\n"
                "• Ariza turi bo'yicha\n\n"
                "Quyidagi filtrlardan birini tanlang:"
            )
            
            sent_message = await message.answer(
                text=filters_text,
                reply_markup=get_manager_filters_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "filter_by_region")
    async def filter_by_region(callback: CallbackQuery, state: FSMContext):
        """Filter by region"""
        try:
            await callback.answer()
            
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Filter by current region
            filters = {}  # Region is already filtered by mock data
            applications = await get_filtered_applications_mock(region, filters)
            
            if not applications:
                no_results_text = "📭 Bu hududda arizalar topilmadi."
                
                await callback.message.edit_text(
                    text=no_results_text,
                    reply_markup=get_manager_back_keyboard('uz')
                )
                return
            
            # Show first application
            await show_filtered_application(callback, applications[0], applications, 0)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "filter_by_status")
    async def filter_by_status(callback: CallbackQuery, state: FSMContext):
        """Filter by status"""
        try:
            await callback.answer()
            
            # Show status selection keyboard
            status_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🆕 Yangi", callback_data="filter_status_created"),
                    InlineKeyboardButton(text="👤 Tayinlangan", callback_data="filter_status_assigned")
                ],
                [
                    InlineKeyboardButton(text="⏳ Jarayonda", callback_data="filter_status_in_progress"),
                    InlineKeyboardButton(text="⏸️ Kutilmoqda", callback_data="filter_status_pending")
                ],
                [
                    InlineKeyboardButton(text="✅ Bajarilgan", callback_data="filter_status_completed"),
                    InlineKeyboardButton(text="❌ Bekor qilingan", callback_data="filter_status_cancelled")
                ],
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_filters")]
            ])
            
            await callback.message.edit_text(
                "📊 Qaysi status bo'yicha filtrlash kerak?",
                reply_markup=status_keyboard
            )
            
        except Exception as e:
            logger.error(f"Error in filter_by_status: {e}")
            await callback.answer("❌ Xatolik yuz berdi")
    
    @router.callback_query(F.data.startswith("filter_status_"))
    async def apply_status_filter(callback: CallbackQuery, state: FSMContext):
        """Apply status filter"""
        try:
            await callback.answer()
            
            # Get status from callback data
            status = callback.data.replace("filter_status_", "")
            
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Apply filter
            filters = {'status': status}
            applications = await get_filtered_applications_mock(region, filters)
            
            if not applications:
                no_results_text = f"📭 '{status}' holatida arizalar topilmadi."
                
                await callback.message.edit_text(
                    text=no_results_text,
                    reply_markup=get_manager_back_keyboard('uz')
                )
                return
            
            # Save filter results to state
            await state.update_data(filtered_applications=applications, current_filter_index=0)
            
            # Show first application
            await show_filtered_application(callback, applications[0], applications, 0)
            
        except Exception as e:
            logger.error(f"Error applying status filter: {e}")
            await callback.answer("❌ Xatolik yuz berdi")

    async def show_filtered_application(callback, application, applications, index):
        """Show filtered application details"""
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
            
            # Format date
            created_date = application['created_at']
            if isinstance(created_date, str):
                try:
                    created_date = datetime.fromisoformat(created_date.replace('Z', '+00:00'))
                except:
                    created_date = datetime.now()
            
            created_date_str = created_date.strftime('%d.%m.%Y %H:%M') if hasattr(created_date, 'strftime') else str(created_date)
            
            # To'liq ma'lumot
            text = (
                f"{workflow_type_emoji} <b>{workflow_type_text} - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"📅 <b>Sana:</b> {created_date_str}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"🏛️ <b>Hudud:</b> {application.get('region', 'Noma\'lum')}\n"
                f"🏠 <b>Manzil:</b> {application.get('location', 'Noma\'lum')}\n"
                f"📝 <b>Tavsif:</b> {application['description']}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n\n"
                f"📊 <b>Ariza #{index + 1} / {len(applications)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_filtered_applications_navigation_keyboard(index, len(applications))
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "filter_by_priority")
    async def filter_by_priority(callback: CallbackQuery, state: FSMContext):
        """Filter by priority"""
        try:
            await callback.answer()
            
            # Show priority selection keyboard
            priority_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔴 Yuqori", callback_data="filter_priority_high"),
                    InlineKeyboardButton(text="🟡 O'rtacha", callback_data="filter_priority_normal"),
                    InlineKeyboardButton(text="🟢 Past", callback_data="filter_priority_low")
                ],
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_filters")]
            ])
            
            await callback.message.edit_text(
                "⚡ Qaysi ustuvorlik bo'yicha filtrlash kerak?",
                reply_markup=priority_keyboard
            )
            
        except Exception as e:
            logger.error(f"Error in filter_by_priority: {e}")
            await callback.answer("❌ Xatolik yuz berdi")
    
    @router.callback_query(F.data.startswith("filter_priority_"))
    async def apply_priority_filter(callback: CallbackQuery, state: FSMContext):
        """Apply priority filter"""
        try:
            await callback.answer()
            
            # Get priority from callback data
            priority = callback.data.replace("filter_priority_", "")
            
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Apply filter
            filters = {'priority': priority}
            applications = await get_filtered_applications_mock(region, filters)
            
            if not applications:
                priority_text = {'high': 'Yuqori', 'normal': "O'rtacha", 'low': 'Past'}.get(priority, priority)
                no_results_text = f"📭 '{priority_text}' ustuvorlikdagi arizalar topilmadi."
                
                await callback.message.edit_text(
                    text=no_results_text,
                    reply_markup=get_manager_back_keyboard('uz')
                )
                return
            
            # Save filter results to state
            await state.update_data(filtered_applications=applications, current_filter_index=0)
            
            # Show first application
            await show_filtered_application(callback, applications[0], applications, 0)
            
        except Exception as e:
            logger.error(f"Error applying priority filter: {e}")
            await callback.answer("❌ Xatolik yuz berdi")
    
    @router.callback_query(F.data == "filter_by_date")
    async def filter_by_date(callback: CallbackQuery, state: FSMContext):
        """Filter by date"""
        try:
            await callback.answer()
            
            # Show date range selection keyboard
            date_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📅 Bugun", callback_data="filter_date_today")],
                [InlineKeyboardButton(text="📅 Kecha", callback_data="filter_date_yesterday")],
                [InlineKeyboardButton(text="📅 Oxirgi 7 kun", callback_data="filter_date_week")],
                [InlineKeyboardButton(text="📅 Oxirgi 30 kun", callback_data="filter_date_month")],
                [InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_filters")]
            ])
            
            await callback.message.edit_text(
                "📅 Qaysi vaqt oralig'i bo'yicha filtrlash kerak?",
                reply_markup=date_keyboard
            )
            
        except Exception as e:
            logger.error(f"Error in filter_by_date: {e}")
            await callback.answer("❌ Xatolik yuz berdi")
    
    @router.callback_query(F.data.startswith("filter_date_"))
    async def apply_date_filter(callback: CallbackQuery, state: FSMContext):
        """Apply date filter"""
        try:
            await callback.answer()
            
            # Get date range from callback data
            date_range = callback.data.replace("filter_date_", "")
            
            # Calculate date range
            now = datetime.now()
            date_from = None
            date_to = now
            
            if date_range == "today":
                date_from = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif date_range == "yesterday":
                date_from = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                date_to = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif date_range == "week":
                date_from = now - timedelta(days=7)
            elif date_range == "month":
                date_from = now - timedelta(days=30)
            
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Apply filter
            filters = {'date_from': date_from, 'date_to': date_to}
            applications = await get_filtered_applications_mock(region, filters)
            
            if not applications:
                date_text = {
                    'today': 'Bugun',
                    'yesterday': 'Kecha',
                    'week': 'Oxirgi 7 kun',
                    'month': 'Oxirgi 30 kun'
                }.get(date_range, date_range)
                no_results_text = f"📭 {date_text} ichida arizalar topilmadi."
                
                await callback.message.edit_text(
                    text=no_results_text,
                    reply_markup=get_manager_back_keyboard('uz')
                )
                return
            
            # Save filter results to state
            await state.update_data(filtered_applications=applications, current_filter_index=0)
            
            # Show first application
            await show_filtered_application(callback, applications[0], applications, 0)
            
        except Exception as e:
            logger.error(f"Error applying date filter: {e}")
            await callback.answer("❌ Xatolik yuz berdi")
    
    return router

def get_filtered_applications_navigation_keyboard(current_index: int, total_applications: int):
    """Create navigation keyboard for filtered applications"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="prev_filtered_app"
        ))
    
    # Next button
    if current_index < total_applications - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="next_filtered_app"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

