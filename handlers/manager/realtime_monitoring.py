"""
Menejer uchun real vaqtda kuzatish handleri - Mock Data Version

Bu modul menejer rolida real vaqtda kuzatish funksiyalarini ta'minlaydi.
Mock data bilan ishlaydi, test qilish uchun.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from filters.role_filter import RoleFilter
from keyboards.manager_buttons import (
    get_manager_realtime_keyboard,
    get_realtime_navigation_keyboard,
    get_realtime_refresh_keyboard
)
import logging
import json
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Mock data for testing
MOCK_APPLICATIONS = [
    {
        'id': 'REQ001',
        'client_id': 101,
        'client_name': 'Aziz Karimov',
        'workflow_type': 'connection_request',
        'current_status': 'in_progress',
        'current_assignee_id': 201,
        'current_role_actor_name': 'Technician 1',
        'current_role_actor_role': 'technician',
        'created_at': '2024-01-15 10:30:00',
        'updated_at': '2024-01-15 14:20:00',
        'location': 'Toshkent, Chilonzor',
        'priority': 'high',
        'description': 'Internet ulanish muammosi',
        'state_data': '{"tariff": "Premium", "connection_type": "B2C"}'
    },
    {
        'id': 'REQ002',
        'client_id': 102,
        'client_name': 'Malika Yusupova',
        'workflow_type': 'technical_service',
        'current_status': 'assigned',
        'current_assignee_id': 202,
        'current_role_actor_name': 'Manager 1',
        'current_role_actor_role': 'manager',
        'created_at': '2024-01-14 14:20:00',
        'updated_at': '2024-01-15 09:15:00',
        'location': 'Toshkent, Sergeli',
        'priority': 'normal',
        'description': 'Televizor signal muammosi',
        'state_data': '{}'
    },
    {
        'id': 'REQ003',
        'client_id': 103,
        'client_name': 'Jasur Toshmatov',
        'workflow_type': 'call_center_direct',
        'current_status': 'pending',
        'current_assignee_id': 203,
        'current_role_actor_name': 'Call Center 1',
        'current_role_actor_role': 'call_center',
        'created_at': '2024-01-13 09:15:00',
        'updated_at': '2024-01-15 11:30:00',
        'location': 'Toshkent, Yakkasaroy',
        'priority': 'urgent',
        'description': 'Telefon xizmati',
        'state_data': '{}'
    },
    {
        'id': 'REQ004',
        'client_id': 104,
        'client_name': 'Dilfuza Rahimova',
        'workflow_type': 'connection_request',
        'current_status': 'completed',
        'current_assignee_id': 204,
        'current_role_actor_name': 'Technician 2',
        'current_role_actor_role': 'technician',
        'created_at': '2024-01-12 16:45:00',
        'updated_at': '2024-01-15 10:00:00',
        'location': 'Toshkent, Shayxontohur',
        'priority': 'low',
        'description': 'Internet tezligi past',
        'state_data': '{"tariff": "Standard", "connection_type": "B2C"}'
    },
    {
        'id': 'REQ005',
        'client_id': 105,
        'client_name': 'Rustam Alimov',
        'workflow_type': 'technical_service',
        'current_status': 'in_progress',
        'current_assignee_id': 205,
        'current_role_actor_name': 'Technician 3',
        'current_role_actor_role': 'technician',
        'created_at': '2024-01-11 11:30:00',
        'updated_at': '2024-01-15 13:45:00',
        'location': 'Toshkent, Uchtepa',
        'priority': 'high',
        'description': 'Kabellar almashtirildi',
        'state_data': '{}'
    }
]

MOCK_USERS = {
    201: {'full_name': 'Technician 1', 'role': 'technician'},
    202: {'full_name': 'Manager 1', 'role': 'manager'},
    203: {'full_name': 'Call Center 1', 'role': 'call_center'},
    204: {'full_name': 'Technician 2', 'role': 'technician'},
    205: {'full_name': 'Technician 3', 'role': 'technician'}
}

# Mock workflow history data
MOCK_WORKFLOW_HISTORY = {
    'REQ001': {
        'client_name': 'Aziz Karimov',
        'workflow_type': 'connection_request',
        'current_status': 'in_progress',
        'total_steps': 4,
        'total_duration_hours': 3,
        'total_duration_minutes': 50,
        'workflow_steps': [
            {'step': 1, 'role': 'client', 'actor': 'Aziz Karimov', 'arrived': '10:30', 'left': '10:45', 'duration': '15 daqiqa', 'is_current': False},
            {'step': 2, 'role': 'controller', 'actor': 'Controller 1', 'arrived': '10:45', 'left': '11:15', 'duration': '30 daqiqa', 'is_current': False},
            {'step': 3, 'role': 'manager', 'actor': 'Manager 1', 'arrived': '11:15', 'left': '13:00', 'duration': '1s 45d', 'is_current': False},
            {'step': 4, 'role': 'technician', 'actor': 'Technician 1', 'arrived': '13:00', 'left': None, 'duration': '1s 20d', 'is_current': True}
        ]
    },
    'REQ002': {
        'client_name': 'Malika Yusupova',
        'workflow_type': 'technical_service',
        'current_status': 'assigned',
        'total_steps': 3,
        'total_duration_hours': 1,
        'total_duration_minutes': 30,
        'workflow_steps': [
            {'step': 1, 'role': 'client', 'actor': 'Malika Yusupova', 'arrived': '14:20', 'left': '14:35', 'duration': '15 daqiqa', 'is_current': False},
            {'step': 2, 'role': 'call_center', 'actor': 'Call Center 1', 'arrived': '14:35', 'left': '15:00', 'duration': '25 daqiqa', 'is_current': False},
            {'step': 3, 'role': 'manager', 'actor': 'Manager 1', 'arrived': '15:00', 'left': None, 'duration': '0 daqiqa', 'is_current': True}
        ]
    }
}

def calculate_time_duration(start_time: datetime, end_time: datetime = None) -> str:
    """Calculate time duration between start and end time"""
    if end_time is None:
        end_time = datetime.now()
    
    duration = end_time - start_time
    total_seconds = int(duration.total_seconds())
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}s {minutes}d"
    else:
        return f"{minutes} daqiqa"

def get_priority_emoji(priority: str) -> str:
    """Get priority emoji based on priority level"""
    priority_emojis = {
        'urgent': '🔴',
        'high': '🟠', 
        'normal': '🟡',
        'low': '🟢'
    }
    return priority_emojis.get(priority, '⚪')

def get_status_emoji(duration_minutes: int) -> str:
    """Get status emoji based on duration"""
    if duration_minutes <= 30:
        return '🟢'
    elif duration_minutes <= 60:
        return '🟡'
    else:
        return '🔴'

# Mock functions for database operations
async def get_user_by_telegram_id(telegram_id: int) -> Dict:
    """Mock function to find user by telegram ID"""
    return {
        'id': telegram_id,
        'full_name': f'Manager {telegram_id}',
        'language': 'uz',
        'role': 'manager'
    }

async def get_user(region: str, user_id: int) -> Dict:
    """Mock function to get user by ID"""
    return MOCK_USERS.get(user_id, {'full_name': 'Unknown', 'role': 'unknown'})

async def get_manager_applications(region: str, manager_id: int = None, status_filter: str = None, limit: int = 100, offset: int = 0) -> List[Dict]:
    """Mock function to get manager applications"""
    return MOCK_APPLICATIONS[:limit]

async def get_request_workflow_summary(request_id: str) -> Dict:
    """Mock function to get workflow summary"""
    return MOCK_WORKFLOW_HISTORY.get(request_id, {
        'client_name': 'Unknown',
        'workflow_type': 'unknown',
        'current_status': 'unknown',
        'total_steps': 0,
        'total_duration_hours': 0,
        'total_duration_minutes': 0,
        'workflow_steps': []
    })

# Mock realtime dashboard function
async def get_manager_realtime_dashboard(region: str, manager_id: int = None):
    """Get manager realtime dashboard from mock data"""
    try:
        now = datetime.now()
        
        # Filter active applications
        active_requests = []
        urgent_count = 0
        normal_count = 0
        low_count = 0
        
        for app in MOCK_APPLICATIONS:
            if app.get('current_status') not in ['completed', 'cancelled']:
                # Calculate durations
                created_at = datetime.strptime(app.get('created_at', ''), '%Y-%m-%d %H:%M:%S')
                updated_at = datetime.strptime(app.get('updated_at', ''), '%Y-%m-%d %H:%M:%S')
                
                total_duration = (now - created_at).total_seconds() / 60
                current_role_duration = (now - updated_at).total_seconds() / 60
                
                # Get assignee info
                assignee_name = app.get('current_role_actor_name', 'Tayinlanmagan')
                assignee_role = app.get('current_role_actor_role', 'unknown')
                
                # Prepare request data
                request_data = {
                    'id': app.get('id', ''),
                    'client_name': app.get('client_name', 'Unknown'),
                    'workflow_type': app.get('workflow_type', 'unknown'),
                    'status': app.get('current_status', 'unknown'),
                    'current_role_actor_name': assignee_name,
                    'current_role_actor_role': assignee_role,
                    'start_time': created_at,
                    'current_role_start_time': updated_at,
                    'current_duration_text': calculate_time_duration(updated_at, now),
                    'created_at': created_at.strftime('%Y-%m-%d %H:%M'),
                    'location': app.get('location', ''),
                    'workflow_steps': 4,  # Mock value
                    'total_duration_text': calculate_time_duration(created_at, now),
                    'status_emoji': get_status_emoji(int(total_duration)),
                    'priority': app.get('priority', 'normal'),
                    'duration_minutes': int(total_duration),
                    'current_role_minutes': int(current_role_duration),
                    'realtime': {
                        'current_role_duration_minutes': int(current_role_duration),
                        'total_duration_minutes': int(total_duration),
                        'estimated_completion': (now + timedelta(minutes=30)).strftime('%H:%M')
                    }
                }
                
                active_requests.append(request_data)
                
                # Count by priority
                if app.get('priority') == 'high' or total_duration > 120:
                    urgent_count += 1
                elif app.get('priority') == 'normal':
                    normal_count += 1
                else:
                    low_count += 1
        
        return {
            'total_active_requests': len(active_requests),
            'urgent_requests': urgent_count,
            'normal_requests': normal_count,
            'low_priority_requests': low_count,
            'requests': active_requests
        }
        
    except Exception as e:
        logger.error(f"Error getting realtime dashboard: {e}")
        return {
            'total_active_requests': 0,
            'urgent_requests': 0,
            'normal_requests': 0,
            'low_priority_requests': 0,
            'requests': []
        }

async def get_manager_detailed_requests(region: str, manager_id: int = None):
    """Get detailed requests for manager monitoring from mock data"""
    try:
        # Return mock applications with additional calculated fields
        detailed_requests = []
        now = datetime.now()
        
        for app in MOCK_APPLICATIONS:
            if app.get('current_status') not in ['completed', 'cancelled']:
                created_at = datetime.strptime(app.get('created_at', ''), '%Y-%m-%d %H:%M:%S')
                updated_at = datetime.strptime(app.get('updated_at', ''), '%Y-%m-%d %H:%M:%S')
                
                total_duration = (now - created_at).total_seconds() / 60
                current_role_duration = (now - updated_at).total_seconds() / 60
                
                detailed_request = {
                    **app,
                    'current_duration_text': calculate_time_duration(updated_at, now),
                    'total_duration_text': calculate_time_duration(created_at, now),
                    'status_emoji': get_status_emoji(int(total_duration)),
                    'duration_minutes': int(total_duration),
                    'current_role_minutes': int(current_role_duration),
                    'workflow_steps': 4  # Mock value
                }
                detailed_requests.append(detailed_request)
        
        return {'requests': detailed_requests}
    except Exception as e:
        logger.error(f"Error getting detailed requests: {e}")
        return {'requests': []}

async def calculate_time_duration(time_diff):
    """Calculate time duration from timedelta"""
    if not time_diff:
        return "0 daqiqa"
    
    if isinstance(time_diff, timedelta):
        total_seconds = int(time_diff.total_seconds())
    else:
        total_seconds = int(time_diff)
    
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    
    parts = []
    if days > 0:
        parts.append(f"{days} kun")
    if hours > 0:
        parts.append(f"{hours} soat")
    if minutes > 0:
        parts.append(f"{minutes} daqiqa")
    
    return " ".join(parts) if parts else "0 daqiqa"

def get_manager_realtime_monitoring_router():
    router = Router()
    
    # Apply role filter - both manager and junior_manager can access
    role_filter = RoleFilter(["manager", "junior_manager"])
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🕐 Real vaqtda kuzatish"]), flags={"block": False})
    async def show_realtime_dashboard(message: Message, state: FSMContext):
        """Manager realtime monitoring handler"""
        try:
            # Use hardcoded values for now
            user_region = 'toshkent'
            
            user = await get_user_by_telegram_id(user_region, message.from_user.id)
            if not user or user['role'] != 'manager':
                error_text = "Sizda ruxsat yo'q."
                await message.answer(error_text)
                return

            # Use hardcoded values for now
            lang = 'uz'
            
            try:
                # Dashboard ma'lumotlarini olish
                dashboard_data = await get_manager_realtime_dashboard(user_region, user['id'])
                
                if "error" in dashboard_data:
                    error_text = "Ma'lumotlarni olishda xatolik"
                    await message.answer(error_text)
                    return
                
                # Xabar formatlash
                dashboard_text = f"""
🕐 <b>Real vaqtda kuzatish</b>

📊 <b>Joriy holat:</b>
• Faol zayavkalar: {dashboard_data.get('total_active_requests', 0)}
• Shoshilinch: {dashboard_data.get('urgent_requests', 0)}
• Normal: {dashboard_data.get('normal_requests', 0)}

⏰ <b>Yangilangan:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""
                
                # Klaviatura
                keyboard = get_manager_realtime_keyboard(lang)

                await message.answer(dashboard_text, reply_markup=keyboard, parse_mode='HTML')

            except Exception as e:
                print(f"Error in realtime dashboard: {e}")
                error_text = "Dashboard ko'rsatishda xatolik"
                await message.answer(error_text)
                
        except Exception as e:
            print(f"Error in show_realtime_dashboard: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.callback_query(F.data == "mgr_realtime_requests")
    async def show_realtime_requests(callback: CallbackQuery, state: FSMContext):
        """Real vaqtda zayavkalar ro'yxatini ko'rsatish"""
        try:
            # Use hardcoded values for now
            user_region = 'toshkent'
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return

            # Use hardcoded values for now
            lang = 'uz'
            
            try:
                # Batafsil zayavkalar ma'lumotlarini olish
                detailed_data = await get_manager_detailed_requests(user['id'])
                
                if "error" in detailed_data:
                    await callback.answer("Xatolik yuz berdi", show_alert=True)
                    return
                
                requests = detailed_data.get('requests', [])
                total_count = len(requests)
                
                if not requests:
                    no_requests_text = "Faol zayavkalar yo'q"
                    await callback.answer(no_requests_text, show_alert=True)
                    return
                
                # Foydalanuvchi state'da joriy zayavka indeksini saqlash
                current_index = await state.get_data()
                current_index = current_index.get('current_request_index', 0)
                
                # Indeksni cheklash
                if current_index >= len(requests):
                    current_index = 0
                elif current_index < 0:
                    current_index = len(requests) - 1
                
                # Joriy zayavka ma'lumotlari
                current_request = requests[current_index]
                
                # Zayavka ma'lumotlarini formatlash
                request_text = f"""
📋 <b>Zayavka #{current_index + 1} / {total_count}</b>

{current_request['status_emoji']} <b>{current_request['client_name']}</b>
   📋 ID: {current_request['id'][:8]}...
   🏷️ Turi: {current_request['workflow_type']}
   📊 Status: {current_request['status']}
   👤 Joriy: {current_request['current_role_actor_name']} ({current_request['current_role_actor_role']})
   ⏰ Joriy rolda: {current_request['current_duration_text']}
   📅 Yaratilgan: {current_request['created_at']}
   📍 Manzil: {current_request['location']}

📊 <b>Umumiy ma'lumot:</b>
   • Jami qadamlar: {current_request['workflow_steps']}
   • Umumiy vaqt: {current_request['total_duration_text']}
"""
                
                # Navigatsiya tugmalari
                keyboard_buttons = []
                
                # Agar 1tadan ko'p zayavka bo'lsa, navigatsiya tugmalarini qo'shish
                if total_count > 1:
                    keyboard_buttons.append([
                        InlineKeyboardButton(
                            text="◀️ Oldingi",
                            callback_data="mgr_prev_request"
                        ),
                        InlineKeyboardButton(
                            text=f"{current_index + 1}/{total_count}",
                            callback_data="mgr_request_info"
                        ),
                        InlineKeyboardButton(
                            text="Keyingi ▶️",
                            callback_data="mgr_next_request"
                        )
                    ])
                else:
                    # Agar faqat 1ta zayavka bo'lsa, faqat raqamni ko'rsatish
                    keyboard_buttons.append([
                        InlineKeyboardButton(
                            text=f"1/1",
                            callback_data="mgr_request_info"
                        )
                    ])
                
                # Orqaga qaytish tugmasi har doim
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="⬅️ Orqaga",
                        callback_data="mgr_back_to_realtime"
                    )
                ])
                
                keyboard = get_realtime_navigation_keyboard(lang='uz')
                
                # State'da joriy indeksni saqlash
                await state.update_data(current_request_index=current_index)
                
                try:
                    await callback.message.edit_text(request_text, reply_markup=keyboard, parse_mode='HTML')
                except Exception as e:
                    if "message is not modified" in str(e):
                        # Xabar o'zgartirilmagan bo'lsa, faqat answer qilish
                        await callback.answer()
                    else:
                        # Boshqa xatolik bo'lsa, qayta urinish
                        await callback.message.edit_text(request_text, reply_markup=keyboard, parse_mode='HTML')
                
                await callback.answer()
                
            except Exception as e:
                print(f"Error showing detailed requests: {e}")
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            print(f"Error in show_realtime_requests: {str(e)}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_prev_request")
    async def show_previous_request(callback: CallbackQuery, state: FSMContext):
        """Oldingi zayavkani ko'rsatish"""
        # Use hardcoded values for now
        user_region = 'toshkent'
        
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        current_index = data.get('current_request_index', 0)
        
        # Oldingi indeksga o'tish
        await state.update_data(current_request_index=current_index - 1)
        
        # Zayavkani qayta ko'rsatish
        try:
            await show_realtime_requests(callback, state)
        except Exception as e:
            print(f"Error showing previous request: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_next_request")
    async def show_next_request(callback: CallbackQuery, state: FSMContext):
        """Keyingi zayavkani ko'rsatish"""
        # Use hardcoded values for now
        user_region = 'toshkent'
        
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        current_index = data.get('current_request_index', 0)
        
        # Keyingi indeksga o'tish
        await state.update_data(current_request_index=current_index + 1)
        
        # Zayavkani qayta ko'rsatish
        try:
            await show_realtime_requests(callback, state)
        except Exception as e:
            print(f"Error showing next request: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_realtime_urgent")
    async def show_urgent_requests(callback: CallbackQuery, state: FSMContext):
        """Shoshilinch zayavkalarni ko'rsatish"""
        # Use hardcoded values for now
        user_region = 'toshkent'
        
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # Use hardcoded values for now
        lang = 'uz'
        
        try:
            dashboard_data = await get_manager_realtime_dashboard(user_region, user['id'])
            
            if "error" in dashboard_data:
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                return
            
            requests = dashboard_data.get('requests', [])
            urgent_requests = []
            
            # Shoshilinch zayavkalarni filtrlash
            for request in requests:
                # Try both nested and direct field access for backwards compatibility
                duration = request.get('realtime', {}).get('current_role_duration_minutes', 0)
                if duration == 0:  # If nested structure doesn't have duration, try direct field
                    duration = request.get('current_role_minutes', 0)
                if duration > 60:  # 1 soatdan ko'p
                    urgent_requests.append(request)
            
            if not urgent_requests:
                no_urgent_text = "Shoshilinch zayavkalar yo'q"
                await callback.answer(no_urgent_text, show_alert=True)
                return
            
            # Foydalanuvchi state'da joriy zayavka indeksini saqlash
            data = await state.get_data()
            current_index = data.get('current_urgent_index', 0)
            
            # Indeksni cheklash
            if current_index >= len(urgent_requests):
                current_index = 0
            elif current_index < 0:
                current_index = len(urgent_requests) - 1
            
            # Joriy zayavka ma'lumotlari
            current_request = urgent_requests[current_index]
            duration_minutes = current_request.get('current_role_minutes', 0)
            total_duration = current_request.get('total_duration_text', 'Noma\'lum')
            current_role_duration = current_request.get('current_duration_text', 'Noma\'lum')
            
            # Zayavka ma'lumotlarini formatlash
            urgent_text = f"""
🚨 <b>Shoshilinch zayavka</b>

{get_status_emoji(duration_minutes)} <b>{current_request.get('client_name', 'Noma\'lum')}</b>
   ⏰ Joriy rolda: {current_role_duration}
   ⏰ Umumiy vaqt: {total_duration}
   📋 ID: {current_request.get('id', '')[:8]}...
   👤 Joriy: {current_request.get('current_role_actor_name', 'Noma\'lum')} ({current_request.get('current_role_actor_role', 'Noma\'lum')})
   📍 Manzil: {current_request.get('location', 'Manzil ko\'rsatilmagan')}
   📅 Yaratilgan: {current_request.get('created_at', 'Noma\'lum')}
   🏷️ Turi: {current_request.get('workflow_type', 'Noma\'lum')}
"""
            
            # Navigatsiya tugmalari
            keyboard_buttons = []
            
            # Agar 1tadan ko'p shoshilinch zayavka bo'lsa, navigatsiya tugmalarini qo'shish
            if len(urgent_requests) > 1:
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="◀️ Oldingi",
                        callback_data="mgr_prev_urgent"
                    ),
                    InlineKeyboardButton(
                        text="Keyingi ▶️",
                        callback_data="mgr_next_urgent"
                    )
                ])
            
            # Orqaga qaytish tugmasi har doim
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="mgr_back_to_realtime"
                )
            ])
            
            keyboard = get_realtime_navigation_keyboard(lang='uz')
            
            # State'da joriy indeksni saqlash
            await state.update_data(current_urgent_index=current_index)
            
            try:
                await callback.message.edit_text(urgent_text, reply_markup=keyboard, parse_mode='HTML')
            except Exception as e:
                if "message is not modified" in str(e):
                    await callback.answer()
                else:
                    await callback.message.edit_text(urgent_text, reply_markup=keyboard, parse_mode='HTML')
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error showing urgent requests: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_time_tracking")
    async def show_time_tracking(callback: CallbackQuery, state: FSMContext):
        """Zayavka vaqt kuzatish ko'rsatish"""
        # Use hardcoded values for now
        user_region = 'toshkent'
        
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # Use hardcoded values for now
        lang = 'uz'
        
        try:
            # Dashboard ma'lumotlarini olish
            dashboard_data = await get_manager_realtime_dashboard(user_region, user['id'])
            
            if "error" in dashboard_data:
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                return
            
            requests = dashboard_data.get('requests', [])
            
            if not requests:
                no_requests_text = "Faol zayavkalar yo'q"
                await callback.answer(no_requests_text, show_alert=True)
                return
            
            # Foydalanuvchi state'da joriy zayavka indeksini saqlash
            data = await state.get_data()
            current_index = data.get('current_time_index', 0)
            
            # Indeksni cheklash
            if current_index >= len(requests):
                current_index = 0
            elif current_index < 0:
                current_index = len(requests) - 1
            
            # Joriy zayavka ma'lumotlari
            current_request = requests[current_index]
            request_id = current_request.get('id')
            
            # Zayavka ma'lumotlarini formatlash
            client_name = current_request.get('client_name', 'Noma\'lum')
            total_duration = current_request.get('total_duration_text', 'Noma\'lum')
            current_role_duration = current_request.get('current_duration_text', 'Noma\'lum')
            current_role = current_request.get('current_role_actor_role', 'Noma\'lum')
            current_actor = current_request.get('current_role_actor_name', 'Noma\'lum')
            duration_minutes = current_request.get('current_role_minutes', 0)
            
            # Status belgisini aniqlash
            status_emoji = get_status_emoji(duration_minutes)
            priority_emoji = get_priority_emoji(current_request.get('priority', 'normal'))
            
            time_text = f"""
⏰ <b>Vaqt kuzatish #{current_index + 1} / {len(requests)}</b>

{status_emoji} <b>{client_name}</b>
   {priority_emoji} {current_request.get('workflow_type', 'Noma\'lum')}
   ⏰ Umumiy vaqt: {total_duration}
   🔄 Joriy rol: {current_role} ({current_role_duration})
   👤 Joriy: {current_actor}
   📋 ID: {request_id[:8]}...

📊 <b>Vaqt tahlili:</b>
   • Joriy rolda: {duration_minutes} daqiqa
   • Status: {current_request.get('status', 'Noma\'lum')}
   • Priority: {current_request.get('priority', 'Noma\'lum')}
"""
            
            # Navigatsiya tugmalari
            keyboard_buttons = []
            
            # Agar 1tadan ko'p zayavka bo'lsa, navigatsiya tugmalarini qo'shish
            if len(requests) > 1:
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="◀️ Oldingi",
                        callback_data="mgr_prev_time"
                    ),
                    InlineKeyboardButton(
                        text="Keyingi ▶️",
                        callback_data="mgr_next_time"
                    )
                ])
            
            # Orqaga qaytish tugmasi har doim
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="mgr_back_to_realtime"
                )
            ])
            
            keyboard = get_realtime_navigation_keyboard(lang='uz')
            
            # State'da joriy indeksni saqlash
            await state.update_data(current_time_index=current_index)
            
            try:
                await callback.message.edit_text(time_text, reply_markup=keyboard, parse_mode='HTML')
            except Exception as e:
                if "message is not modified" in str(e):
                    await callback.answer()
                else:
                    await callback.message.edit_text(time_text, reply_markup=keyboard, parse_mode='HTML')
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error showing time tracking: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_workflow_history")
    async def show_workflow_history(callback: CallbackQuery, state: FSMContext):
        """Zayavka workflow tarixini ko'rsatish"""
        # Use hardcoded values for now
        user_region = 'toshkent'
        
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # Use hardcoded values for now
        lang = 'uz'
        
        try:
            # Dashboard ma'lumotlarini olish
            dashboard_data = await get_manager_realtime_dashboard(user_region, user['id'])
            
            if "error" in dashboard_data:
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                return
            
            requests = dashboard_data.get('requests', [])
            
            if not requests:
                no_requests_text = "Faol zayavkalar yo'q"
                await callback.answer(no_requests_text, show_alert=True)
                return
            
            # Foydalanuvchi state'da joriy zayavka indeksini saqlash
            data = await state.get_data()
            current_index = data.get('current_workflow_index', 0)
            
            # Indeksni cheklash
            if current_index >= len(requests):
                current_index = 0
            elif current_index < 0:
                current_index = len(requests) - 1
            
            # Joriy zayavka ma'lumotlari
            current_request = requests[current_index]
            request_id = current_request.get('id')
            workflow_summary = await get_request_workflow_summary(request_id)
            
            if "error" in workflow_summary:
                await callback.answer("Zayavka ma'lumotlarini olishda xatolik", show_alert=True)
                return
            
            # Zayavka ma'lumotlarini formatlash
            client_name = workflow_summary.get('client_name', 'Noma\'lum')
            workflow_type = workflow_summary.get('workflow_type', 'Noma\'lum')
            current_status = workflow_summary.get('current_status', 'Noma\'lum')
            total_steps = workflow_summary.get('total_steps', 0)
            total_hours = workflow_summary.get('total_duration_hours', 0)
            total_minutes = workflow_summary.get('total_duration_minutes', 0)
            
            # Zayavka turini formatlash
            workflow_type_text = {
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Qo\'ng\'iroq markazi'
            }.get(workflow_type, workflow_type)
            
            # Status belgisini aniqlash
            status_emoji = "🟢" if current_status == 'completed' else "🟡" if current_status == 'in_progress' else "🔴"
            
            history_text = f"""
📊 <b>Workflow tarix #{current_index + 1} / {len(requests)}</b>

{status_emoji} <b>{client_name}</b>
   🏷️ Turi: {workflow_type_text}
   📊 Status: {current_status}
   📋 Qadamlar: {total_steps}
   ⏰ Umumiy: {total_hours}s {total_minutes}d
   📋 ID: {request_id[:8]}...

📋 <b>Workflow qadamlar:</b>
"""
            
            # Har bir qadam uchun
            for step in workflow_summary.get('workflow_steps', [])[:5]:
                step_num = step['step']
                role = step['role']
                actor = step['actor']
                arrived = step['arrived']
                left = step['left']
                duration = step['duration']
                is_current = step['is_current']
                
                # Rol belgilarini aniqlash
                role_emoji = {
                    'client': '👤',
                    'controller': '🎛️',
                    'manager': '👨‍💼',
                    'junior_manager': '👨‍💼',
                    'technician': '🔧',
                    'call_center': '📞',
                    'warehouse': '📦'
                }.get(role.lower(), '👤')
                
                current_mark = " 🔄" if is_current else ""
                
                # Vaqt formatlash
                if arrived and left:
                    time_info = f"📅 {arrived} → {left}"
                elif arrived:
                    time_info = f"📅 {arrived} → hali tugamagan"
                else:
                    time_info = "📅 Vaqt ma'lum emas"
                
                history_text += (
                    f"   {step_num}. {role_emoji} {role} ({actor})\n"
                    f"      {time_info}\n"
                    f"      ⏰ {duration}{current_mark}\n\n"
                )
            
            # Navigatsiya tugmalari
            keyboard_buttons = []
            
            # Agar 1tadan ko'p zayavka bo'lsa, navigatsiya tugmalarini qo'shish
            if len(requests) > 1:
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="◀️ Oldingi",
                        callback_data="mgr_prev_workflow"
                    ),
                    InlineKeyboardButton(
                        text="Keyingi ▶️",
                        callback_data="mgr_next_workflow"
                    )
                ])
            
            # Orqaga qaytish tugmasi har doim
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="mgr_back_to_realtime"
                )
            ])
            
            keyboard = get_realtime_navigation_keyboard(lang='uz')
            
            # State'da joriy indeksni saqlash
            await state.update_data(current_workflow_index=current_index)
            
            try:
                await callback.message.edit_text(history_text, reply_markup=keyboard, parse_mode='HTML')
            except Exception as e:
                if "message is not modified" in str(e):
                    await callback.answer()
                else:
                    await callback.message.edit_text(history_text, reply_markup=keyboard, parse_mode='HTML')
            
            await callback.answer()
            
        except Exception as e:
            print(f"Error showing workflow history: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_back_to_realtime")
    async def back_to_realtime_dashboard(callback: CallbackQuery, state: FSMContext):
        """Asosiy realtime dashboardga qaytish"""
        # Use hardcoded values for now
        user_region = 'toshkent'
        
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # Use hardcoded values for now
        lang = 'uz'
        
        try:
            dashboard_data = await get_manager_realtime_dashboard(user_region, user['id'])
            
            if "error" in dashboard_data:
                await callback.answer("Xatolik yuz berdi", show_alert=True)
                return
            
            # Asosiy dashboard xabari
            dashboard_text = f"""
🕐 <b>Real vaqtda kuzatish</b>

📊 <b>Joriy holat:</b>
• Faol zayavkalar: {dashboard_data.get('total_active_requests', 0)}
• Shoshilinch: {dashboard_data.get('urgent_requests', 0)}
• Normal: {dashboard_data.get('normal_requests', 0)}

⏰ <b>Yangilangan:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""
            
            # Klaviatura
            keyboard = get_manager_realtime_keyboard(lang)

            await callback.message.edit_text(dashboard_text, reply_markup=keyboard, parse_mode='HTML')
            await callback.answer()
            
        except Exception as e:
            print(f"Error going back to realtime dashboard: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    # Navigation handlers for different sections
    @router.callback_query(F.data.startswith("mgr_prev_"))
    async def show_previous_item(callback: CallbackQuery, state: FSMContext):
        """Oldingi elementni ko'rsatish"""
        # Use hardcoded values for now
        user_region = 'toshkent'
        
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        item_type = callback.data.replace("mgr_prev_", "")
        
        if item_type == "request":
            current_index = data.get('current_request_index', 0)
            await state.update_data(current_request_index=current_index - 1)
            await show_realtime_requests(callback, state)
        elif item_type == "urgent":
            current_index = data.get('current_urgent_index', 0)
            await state.update_data(current_urgent_index=current_index - 1)
            await show_urgent_requests(callback, state)
        elif item_type == "time":
            current_index = data.get('current_time_index', 0)
            await state.update_data(current_time_index=current_index - 1)
            await show_time_tracking(callback, state)
        elif item_type == "workflow":
            current_index = data.get('current_workflow_index', 0)
            await state.update_data(current_workflow_index=current_index - 1)
            await show_workflow_history(callback, state)

    @router.callback_query(F.data.startswith("mgr_next_"))
    async def show_next_item(callback: CallbackQuery, state: FSMContext):
        """Keyingi elementni ko'rsatish"""
        # Use hardcoded values for now
        user_region = 'toshkent'
        
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user['role'] != 'manager':
            await callback.answer("Ruxsat yo'q!", show_alert=True)
            return

        # State'dan joriy indeksni olish
        data = await state.get_data()
        item_type = callback.data.replace("mgr_next_", "")
        
        if item_type == "request":
            current_index = data.get('current_request_index', 0)
            await state.update_data(current_request_index=current_index + 1)
            await show_realtime_requests(callback, state)
        elif item_type == "urgent":
            current_index = data.get('current_urgent_index', 0)
            await state.update_data(current_urgent_index=current_index + 1)
            await show_urgent_requests(callback, state)
        elif item_type == "time":
            current_index = data.get('current_time_index', 0)
            await state.update_data(current_time_index=current_index + 1)
            await show_time_tracking(callback, state)
        elif item_type == "workflow":
            current_index = data.get('current_workflow_index', 0)
            await state.update_data(current_workflow_index=current_index + 1)
            await show_workflow_history(callback, state)

    @router.callback_query(F.data.startswith("mgr_request_info"))
    async def show_request_info(callback: CallbackQuery, state: FSMContext):
        """Zayavka haqida ma'lumot"""
        await callback.answer("Bu zayavka haqida ma'lumot", show_alert=True)

    return router