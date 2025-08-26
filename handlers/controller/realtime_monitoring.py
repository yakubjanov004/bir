"""
Controller Real-time Monitoring Handler
Manages real-time monitoring for controller with mock data implementation
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from filters.role_filter import RoleFilter
from keyboards.controllers_buttons import (
    get_realtime_monitoring_keyboard,
    get_realtime_refresh_keyboard
)
import logging
import random

logger = logging.getLogger(__name__)

# Mock data storage
mock_controller_stats = {
    'active_work': 15,
    'pending_assignment': 8,
    'completed_today': 23,
    'total_technicians': 12,
    'available_technicians': 5,
    'busy_technicians': 7
}

mock_technician_workload = [
    {
        'id': 1,
        'full_name': 'Sardor Rahimov',
        'phone': '+998901234567',
        'assigned_count': 3,
        'in_progress_count': 1,
        'completed_today': 5
    },
    {
        'id': 2,
        'full_name': 'Jasur Karimov',
        'phone': '+998901234568',
        'assigned_count': 2,
        'in_progress_count': 0,
        'completed_today': 3
    },
    {
        'id': 3,
        'full_name': 'Sherzod Toshmatov',
        'phone': '+998901234569',
        'assigned_count': 0,
        'in_progress_count': 0,
        'completed_today': 0
    },
    {
        'id': 4,
        'full_name': 'Dilshod Yuldashev',
        'phone': '+998901234570',
        'assigned_count': 4,
        'in_progress_count': 2,
        'completed_today': 7
    },
    {
        'id': 5,
        'full_name': 'Rustam Abdullayev',
        'phone': '+998901234571',
        'assigned_count': 1,
        'in_progress_count': 1,
        'completed_today': 2
    }
]

mock_controller_requests = [
    {
        'id': 'req_001_2024_01_15',
        'client_name': 'Aziz Ergashev',
        'workflow_type': 'connection_request',
        'current_status': 'assigned_to_technician',
        'technician_name': 'Sardor Rahimov',
        'current_assignee_role': 'technician',
        'created_at': datetime.now() - timedelta(hours=2),
        'location': 'Toshkent shahri, Chilonzor tumani',
        'priority': 'urgent'
    },
    {
        'id': 'req_002_2024_01_16',
        'client_name': 'Bobur Hasanov',
        'workflow_type': 'technical_service',
        'current_status': 'work_in_progress',
        'technician_name': 'Jasur Karimov',
        'current_assignee_role': 'technician',
        'created_at': datetime.now() - timedelta(hours=1),
        'location': 'Toshkent shahri, Sergeli tumani',
        'priority': 'high'
    },
    {
        'id': 'req_003_2024_01_17',
        'client_name': 'Farrux Rahmonov',
        'workflow_type': 'connection_request',
        'current_status': 'pending_assignment',
        'technician_name': 'Tayinlanmagan',
        'current_assignee_role': 'controller',
        'created_at': datetime.now() - timedelta(minutes=30),
        'location': 'Toshkent shahri, Yashnobod tumani',
        'priority': 'normal'
    },
    {
        'id': 'req_004_2024_01_18',
        'client_name': 'Shohruh Mirzayev',
        'workflow_type': 'technical_service',
        'current_status': 'assigned_to_technician',
        'technician_name': 'Dilshod Yuldashev',
        'current_assignee_role': 'technician',
        'created_at': datetime.now() - timedelta(hours=3),
        'location': 'Toshkent shahri, Uchtepa tumani',
        'priority': 'high'
    },
    {
        'id': 'req_005_2024_01_19',
        'client_name': 'Umid Qodirov',
        'workflow_type': 'connection_request',
        'current_status': 'pending_assignment',
        'technician_name': 'Tayinlanmagan',
        'current_assignee_role': 'controller',
        'created_at': datetime.now() - timedelta(minutes=45),
        'location': 'Toshkent shahri, Shayxontohur tumani',
        'priority': 'low'
    }
]

# Mock functions
async def get_user_by_telegram_id(region: str, user_id: int):
    """Mock get user by telegram ID"""
    return {
        'id': 1,
        'telegram_id': user_id,
        'role': 'controller',
        'language': 'uz',
        'full_name': 'Test Controller',
        'phone_number': '+998901234567'
    }

async def get_available_technicians(region: str):
    """Mock get available technicians"""
    return [tech for tech in mock_technician_workload if tech.get('assigned_count', 0) == 0]

async def get_controller_monitoring_stats(region: str):
    """Mock get controller monitoring stats"""
    return mock_controller_stats

async def get_controller_requests(region: str, controller_id: int):
    """Mock get controller requests"""
    return mock_controller_requests

async def get_controller_dashboard_stats(region: str):
    """Mock get controller dashboard stats"""
    return mock_controller_stats

async def get_technician_workload(region: str):
    """Mock get technician workload"""
    return mock_technician_workload

async def get_service_request(region: str, request_id: str):
    """Mock get service request"""
    for req in mock_controller_requests:
        if req['id'] == request_id:
            return req
    return None

async def get_requests_by_status(region: str, status: str):
    """Mock get requests by status"""
    return [req for req in mock_controller_requests if req.get('current_status') == status]

# Mock audit logger
class MockAuditLogger:
    """Mock audit logger"""
    async def log_action(self, user_id: int, action: str, details: dict = None, region: str = None):
        """Mock log action"""
        logger.info(f"Mock: User {user_id} performed action: {action}")
        if details:
            logger.info(f"Mock: Details: {details}")

# Mock realtime updater
class MockRealtimeUpdater:
    """Mock realtime updater"""
    async def update_data(self):
        """Mock update data"""
        logger.info("Mock: Realtime data updated")

# Mock loader function
async def get_user_region(user_id: int):
    """Mock get user region"""
    return 'toshkent'

# Initialize mock objects
audit_logger = MockAuditLogger()
realtime_updater = MockRealtimeUpdater()

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
        'medium': '🟡',
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

async def get_realtime_data(region: str, controller_id: int) -> Dict[str, Any]:
    """Get real-time data from mock data"""
    try:
        # Get dashboard statistics
        stats = await get_controller_dashboard_stats(region)
        
        # Get controller's active requests
        controller_requests = await get_controller_requests(region, controller_id)
        
        # Get technician workload
        tech_workload = await get_technician_workload(region)
        
        # Get available technicians
        available_techs = await get_available_technicians(region)
        
        # Calculate statistics
        active_technicians = len([t for t in tech_workload if t.get('assigned_count', 0) > 0])
        total_technicians = len(tech_workload)
        available_technicians = len([t for t in tech_workload if t.get('assigned_count', 0) == 0])
        busy_technicians = total_technicians - available_technicians
        
        # Get urgent requests
        urgent_requests = []
        for req in controller_requests:
            if req.get('priority') == 'urgent' or req.get('priority') == 'high':
                created_at = req.get('created_at')
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at)
                
                # Calculate current role minutes
                current_role_minutes = 0
                if created_at:
                    current_role_minutes = int((datetime.now() - created_at).total_seconds() / 60)
                
                urgent_requests.append({
                    'id': req.get('id'),
                    'client_name': req.get('client_name', 'Noma\'lum'),
                    'workflow_type': req.get('workflow_type', 'unknown'),
                    'status': req.get('current_status'),
                    'current_role_actor_name': req.get('technician_name', 'Tayinlanmagan'),
                    'current_role_actor_role': req.get('current_assignee_role', 'controller'),
                    'start_time': created_at,
                    'current_role_start_time': created_at,
                    'created_at': created_at.strftime('%Y-%m-%d %H:%M') if created_at else 'N/A',
                    'location': req.get('location', 'Noma\'lum'),
                    'priority': req.get('priority', 'normal'),
                    'total_duration': calculate_time_duration(created_at) if created_at else 'N/A',
                    'current_role_duration': calculate_time_duration(created_at) if created_at else 'N/A',
                    'current_role_minutes': current_role_minutes
                })
        
        # Get normal requests
        normal_requests = []
        for req in controller_requests:
            if req.get('priority') not in ['urgent', 'high']:
                created_at = req.get('created_at')
                if isinstance(created_at, str):
                    created_at = datetime.fromisoformat(created_at)
                
                # Calculate current role minutes
                current_role_minutes = 0
                if created_at:
                    current_role_minutes = int((datetime.now() - created_at).total_seconds() / 60)
                
                normal_requests.append({
                    'id': req.get('id'),
                    'client_name': req.get('client_name', 'Noma\'lum'),
                    'workflow_type': req.get('workflow_type', 'unknown'),
                    'status': req.get('current_status'),
                    'current_role_actor_name': req.get('technician_name', 'Tayinlanmagan'),
                    'current_role_actor_role': req.get('current_assignee_role', 'controller'),
                    'start_time': created_at,
                    'current_role_start_time': created_at,
                    'created_at': created_at.strftime('%Y-%m-%d %H:%M') if created_at else 'N/A',
                    'location': req.get('location', 'Noma\'lum'),
                    'priority': req.get('priority', 'normal'),
                    'total_duration': calculate_time_duration(created_at) if created_at else 'N/A',
                    'current_role_duration': calculate_time_duration(created_at) if created_at else 'N/A',
                    'current_role_minutes': current_role_minutes
                })
        
        # Get active technicians list
        active_technicians_list = []
        for tech in tech_workload:
            if tech.get('assigned_count', 0) > 0 or tech.get('in_progress_count', 0) > 0:
                active_technicians_list.append({
                    'id': tech.get('id'),
                    'name': tech.get('full_name', 'Noma\'lum'),
                    'phone': tech.get('phone', 'N/A'),
                    'current_orders': tech.get('assigned_count', 0) + tech.get('in_progress_count', 0),
                    'completed_today': tech.get('completed_today', 0),
                    'status': 'active' if tech.get('in_progress_count', 0) > 0 else 'assigned',
                    'last_activity': datetime.now().strftime('%H:%M')
                })
        
        return {
            'active_orders': stats.get('active_work', 0),
            'pending_orders': stats.get('pending_assignment', 0),
            'completed_today': stats.get('completed_today', 0),
            'active_technicians': active_technicians,
            'total_technicians': total_technicians,
            'avg_response_time': '1.5 soat',  # Can be calculated from actual data
            'system_status': 'online',
            'system_uptime': '99.9%',
            'active_applications': len(controller_requests),
            'pending_applications': len([r for r in controller_requests if r.get('current_status') == 'pending_assignment']),
            'in_progress_applications': len([r for r in controller_requests if r.get('current_status') in ['assigned_to_technician', 'work_in_progress']]),
            'completed_applications': stats.get('completed_today', 0),
            'available_technicians': available_technicians,
            'busy_technicians': busy_technicians,
            'urgent_requests': urgent_requests[:5],  # Limit to 5 urgent requests
            'normal_requests': normal_requests[:10],  # Limit to 10 normal requests
            'active_technicians_list': active_technicians_list,
            'last_update': datetime.now().strftime('%H:%M:%S'),
            'performance_metrics': {
                'satisfaction_score': '4.6/5.0',
                'active_sessions': 15,
                'completion_rate': '78.5%',
                'response_time_avg': '1.5 soat',
                'avg_response_time': '1.5 soat',
                'avg_completion_time': '4.2 soat',
                'satisfaction_rate': '92.5%',
                'system_uptime': '99.9%'
            },
            'system_overview': {
                'total_requests': 45,
                'active_requests': 15,
                'completed_today': 23,
                'pending_requests': 8,
                'urgent_requests': 3
            },
            'technician_status': {
                'total_technicians': 12,
                'available_technicians': 5,
                'busy_technicians': 7,
                'offline_technicians': 0,
                'avg_workload': '2.3'
            },
            'recent_activities': [
                {
                    'type': 'new_application',
                    'description': 'Yangi ariza yaratildi',
                    'user': 'Aziz Ergashev',
                    'priority': 'urgent',
                    'time': datetime.now() - timedelta(minutes=15)
                },
                {
                    'type': 'technician_assigned',
                    'description': 'Texnik tayinlandi',
                    'user': 'Sardor Rahimov',
                    'priority': 'high',
                    'time': datetime.now() - timedelta(minutes=30)
                },
                {
                    'type': 'application_completed',
                    'description': 'Ariza bajarildi',
                    'user': 'Jasur Karimov',
                    'priority': 'normal',
                    'time': datetime.now() - timedelta(hours=1)
                }
            ],
            'system_alerts': [
                {
                    'type': 'warning',
                    'message': '3 ta shoshilinch ariza kutilmoqda',
                    'time': datetime.now() - timedelta(minutes=10)
                },
                {
                    'type': 'info',
                    'message': 'Tizim yangilandi',
                    'time': datetime.now() - timedelta(hours=2)
                }
            ],
            'urgent_requests_with_time': urgent_requests
        }
        
    except Exception as e:
        logger.error(f"Error getting realtime data: {e}")
        return {
            'active_orders': 0,
            'pending_orders': 0,
            'completed_today': 0,
            'active_technicians': 0,
            'total_technicians': 0,
            'avg_response_time': 'N/A',
            'system_status': 'error',
            'system_uptime': 'N/A',
            'active_applications': 0,
            'pending_applications': 0,
            'in_progress_applications': 0,
            'completed_applications': 0,
            'available_technicians': 0,
            'busy_technicians': 0,
            'urgent_requests': [],
            'normal_requests': [],
            'active_technicians_list': [],
            'last_update': datetime.now().strftime('%H:%M:%S'),
            'performance_metrics': {
                'satisfaction_score': 'N/A',
                'active_sessions': 0,
                'completion_rate': 'N/A',
                'response_time_avg': 'N/A',
                'avg_response_time': 'N/A',
                'avg_completion_time': 'N/A',
                'satisfaction_rate': 'N/A',
                'system_uptime': 'N/A'
            },
            'system_overview': {
                'total_requests': 0,
                'active_requests': 0,
                'completed_today': 0,
                'pending_requests': 0,
                'urgent_requests': 0
            },
            'technician_status': {
                'total_technicians': 0,
                'available_technicians': 0,
                'busy_technicians': 0,
                'offline_technicians': 0,
                'avg_workload': '0'
            },
            'recent_activities': [],
            'system_alerts': [],
            'urgent_requests_with_time': []
        }

async def format_monitoring_message(data: Dict[str, Any], lang: str = 'uz') -> str:
    """Format monitoring message based on data and language"""
    if lang == 'uz':
        message = f"""
🔴 <b>REAL-VAQT MONITORING</b> 🔴

📊 <b>Umumiy statistika:</b>
├ 📦 Faol buyurtmalar: <b>{data['active_orders']}</b>
├ ⏳ Kutilayotgan: <b>{data['pending_orders']}</b>
├ ✅ Bugun bajarilgan: <b>{data['completed_today']}</b>
└ ⏱ O'rtacha javob vaqti: <b>{data['avg_response_time']}</b>

👥 <b>Texniklar holati:</b>
├ 🟢 Faol: <b>{data['active_technicians']}/{data['total_technicians']}</b>
├ 🔧 Band: <b>{data['busy_technicians']}</b>
└ ⏸ Bo'sh: <b>{data['available_technicians']}</b>

📋 <b>Arizalar holati:</b>
├ 📝 Jami faol: <b>{data['active_applications']}</b>
├ ⏳ Kutilmoqda: <b>{data['pending_applications']}</b>
├ 🔄 Jarayonda: <b>{data['in_progress_applications']}</b>
└ ✅ Bajarilgan: <b>{data['completed_applications']}</b>

🔄 <b>Oxirgi yangilanish:</b> {data['last_update']}
"""
    else:
        message = f"""
🔴 <b>МОНИТОРИНГ В РЕАЛЬНОМ ВРЕМЕНИ</b> 🔴

📊 <b>Общая статистика:</b>
├ 📦 Активные заказы: <b>{data['active_orders']}</b>
├ ⏳ В ожидании: <b>{data['pending_orders']}</b>
├ ✅ Выполнено сегодня: <b>{data['completed_today']}</b>
└ ⏱ Среднее время ответа: <b>{data['avg_response_time']}</b>

👥 <b>Состояние техников:</b>
├ 🟢 Активные: <b>{data['active_technicians']}/{data['total_technicians']}</b>
├ 🔧 Занятые: <b>{data['busy_technicians']}</b>
└ ⏸ Свободные: <b>{data['available_technicians']}</b>

📋 <b>Состояние заявок:</b>
├ 📝 Всего активных: <b>{data['active_applications']}</b>
├ ⏳ Ожидают: <b>{data['pending_applications']}</b>
├ 🔄 В процессе: <b>{data['in_progress_applications']}</b>
└ ✅ Выполнено: <b>{data['completed_applications']}</b>

🔄 <b>Последнее обновление:</b> {data['last_update']}
"""
    return message

async def format_urgent_requests_message(data: Dict[str, Any], lang: str = 'uz') -> str:
    """Format urgent requests message"""
    urgent_requests = data.get('urgent_requests', [])
    
    if not urgent_requests:
        if lang == 'uz':
            return "🟢 <b>Shoshilinch arizalar yo'q</b>"
        else:
            return "🟢 <b>Нет срочных заявок</b>"
    
    if lang == 'uz':
        message = "🔴 <b>SHOSHILINCH ARIZALAR</b> 🔴\n\n"
        for i, req in enumerate(urgent_requests, 1):
            priority_emoji = get_priority_emoji(req['priority'])
            message += f"""
{i}. {priority_emoji} <b>Ariza #{req['id']}</b>
├ 👤 Mijoz: {req['client_name']}
├ 📍 Manzil: {req['location']}
├ ⏱ Davomiyligi: {req['total_duration']}
├ 👷 Mas'ul: {req['current_role_actor_name']}
└ 📌 Status: {req['status']}
"""
    else:
        message = "🔴 <b>СРОЧНЫЕ ЗАЯВКИ</b> 🔴\n\n"
        for i, req in enumerate(urgent_requests, 1):
            priority_emoji = get_priority_emoji(req['priority'])
            message += f"""
{i}. {priority_emoji} <b>Заявка #{req['id']}</b>
├ 👤 Клиент: {req['client_name']}
├ 📍 Адрес: {req['location']}
├ ⏱ Длительность: {req['total_duration']}
├ 👷 Ответственный: {req['current_role_actor_name']}
└ 📌 Статус: {req['status']}
"""
    
    return message

async def format_technicians_activity_message(data: Dict[str, Any], lang: str = 'uz') -> str:
    """Format technicians activity message"""
    technicians = data.get('active_technicians_list', [])
    
    if not technicians:
        if lang == 'uz':
            return "📊 <b>Faol texniklar yo'q</b>"
        else:
            return "📊 <b>Нет активных техников</b>"
    
    if lang == 'uz':
        message = "👥 <b>TEXNIKLAR FAOLIYATI</b> 👥\n\n"
        for i, tech in enumerate(technicians, 1):
            status_emoji = '🟢' if tech['status'] == 'active' else '🟡'
            message += f"""
{i}. {status_emoji} <b>{tech['name']}</b>
├ 📞 Tel: {tech['phone']}
├ 📦 Joriy ishlar: {tech['current_orders']}
├ ✅ Bugun bajarilgan: {tech['completed_today']}
└ 🕐 Oxirgi faollik: {tech['last_activity']}
"""
    else:
        message = "👥 <b>АКТИВНОСТЬ ТЕХНИКОВ</b> 👥\n\n"
        for i, tech in enumerate(technicians, 1):
            status_emoji = '🟢' if tech['status'] == 'active' else '🟡'
            message += f"""
{i}. {status_emoji} <b>{tech['name']}</b>
├ 📞 Тел: {tech['phone']}
├ 📦 Текущие работы: {tech['current_orders']}
├ ✅ Выполнено сегодня: {tech['completed_today']}
└ 🕐 Последняя активность: {tech['last_activity']}
"""
    
    return message

def get_realtime_monitoring_router():
    """Get controller real-time monitoring router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🕐 Real vaqtda kuzatish", "📡 Мониторинг в реальном времени"]))
    async def view_realtime_monitoring(message: Message, state: FSMContext):
        """Handle real-time monitoring view"""
        user_id = message.from_user.id
        
        try:
            region = await get_user_region(user_id)
            if not region:
                await message.answer("❌ Region aniqlanmadi")
                return
                
            user = await get_user_by_telegram_id(region, user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            controller_id = user['id']
            realtime_data = await get_realtime_data(region, controller_id)
            
            # Log action
            await audit_logger.log_action(
                user_id=user_id,
                action='controller_action',
                details={'action': 'viewed_realtime_monitoring'},
                region=region
            )
            
            monitoring_text = await format_monitoring_message(realtime_data, lang)
            
            # Manager-like keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=("📋 Zayavkalar ro'yxati" if lang=='uz' else "📋 Список заявок"), callback_data="ctrl_realtime_requests")],
                [InlineKeyboardButton(text=("🚨 Shoshilinch zayavkalar" if lang=='uz' else "🚨 Срочные заявки"), callback_data="ctrl_realtime_urgent")],
                [InlineKeyboardButton(text=("⏰ Vaqt kuzatish" if lang=='uz' else "⏰ Отслеживание времени"), callback_data="ctrl_time_tracking")],
                [InlineKeyboardButton(text=("🔄 Yangilash" if lang=='uz' else "🔄 Обновить"), callback_data="ctrl_refresh_realtime")],
            ])
            
            await message.answer(
                monitoring_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in view_realtime_monitoring: {str(e)}")
            error_text = "Xatolik yuz berdi"
            await message.answer(error_text)

    @router.callback_query(F.data == "ctrl_realtime_status")
    async def view_live_status(callback: CallbackQuery, state: FSMContext):
        """View live system status"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Sizning hududingiz topilmadi. Iltimos, boshqaruvchi bilan bog'laning.")
                return
            
            controller_id = user['id']
            realtime_data = await get_realtime_data(region, controller_id)
            
            status_text = (
                "🟢 <b>Jonli tizim holati</b>\n\n"
                "📊 <b>Umumiy ma'lumot:</b>\n"
                f"• Jami arizalar: {realtime_data['active_applications'] + realtime_data['completed_applications']}\n"
                f"• Faol arizalar: {realtime_data['active_applications']}\n"
                f"• Bugun bajarilgan: {realtime_data['completed_applications']}\n\n"
                f"👨‍🔧 <b>Texniklar holati:</b>\n"
                f"• Jami texniklar: {realtime_data['total_technicians']}\n"
                f"• Mavjud texniklar: {realtime_data['available_technicians']}\n"
                f"• Band texniklar: {realtime_data['busy_technicians']}\n\n"
                f"📈 <b>Samaradorlik:</b>\n"
                f"• O'rtacha javob vaqti: {realtime_data['avg_response_time']}\n"
                f"• Tizim ishlashi: {realtime_data['system_uptime']}\n"
                f"• Mijozlar mamnuniyati: {realtime_data['performance_metrics']['satisfaction_score']}\n\n"
                f"⏰ <b>Yangilangan:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            )
            
            keyboard = get_realtime_refresh_keyboard(lang)
            
            await callback.message.edit_text(status_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_realtime_activities")
    async def view_recent_activities(callback: CallbackQuery, state: FSMContext):
        """View recent activities"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Sizning hududingiz topilmadi. Iltimos, boshqaruvchi bilan bog'laning.")
                return
            
            controller_id = user['id']
            realtime_data = await get_realtime_data(region, controller_id)
            
            activities_text = (
                "📋 <b>So'nggi faolliklar</b>\n\n"
            )
            
            # Add recent activities
            for i, activity in enumerate(realtime_data['recent_activities'], 1):
                priority_emoji = get_priority_emoji(activity.get('priority', 'normal'))
                
                activity_type_emoji = {
                    'new_application': '📝',
                    'technician_assigned': '👨‍🔧',
                    'application_completed': '✅',
                    'application_cancelled': '❌',
                    'order_created': '📋',
                    'order_assigned': '👨‍🔧',
                    'order_completed': '✅',
                    'application_urgent': '🚨'
                }.get(activity['type'], '📄')
                
                time_diff = datetime.now() - activity['time']
                if time_diff.total_seconds() < 3600:  # Less than 1 hour
                    time_text = f"{int(time_diff.total_seconds() // 60)} daqiqa oldin"
                elif time_diff.total_seconds() < 86400:  # Less than 1 day
                    time_text = f"{int(time_diff.total_seconds() // 3600)} soat oldin"
                else:
                    time_text = f"{int(time_diff.total_seconds() // 86400)} kun oldin"
                
                activities_text += (
                    f"{i}. {activity_type_emoji} {activity['description']}\n"
                    f"   {priority_emoji} {activity['user']} - {time_text}\n\n"
                )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔄 Yangilash", callback_data="ctrl_refresh_activities"),
                    InlineKeyboardButton(text="📊 Batafsil", callback_data="ctrl_detailed_activities")
                ],
                [
                    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="ctrl_back_to_realtime")
                ]
            ])
            
            await callback.message.edit_text(activities_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_realtime_alerts")
    async def view_system_alerts(callback: CallbackQuery, state: FSMContext):
        """View system alerts"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Sizning hududingiz topilmadi. Iltimos, boshqaruvchi bilan bog'laning.")
                return
            
            controller_id = user['id']
            realtime_data = await get_realtime_data(region, controller_id)
            
            alerts_text = (
                "🚨 <b>Tizim ogohlantirishlari</b>\n\n"
            )
            
            if realtime_data.get('system_alerts'):
                for i, alert in enumerate(realtime_data['system_alerts'], 1):
                    alert_emoji = {
                        'warning': '⚠️',
                        'error': '❌',
                        'info': 'ℹ️',
                        'success': '✅'
                    }.get(alert['type'], '📢')
                    
                    time_diff = datetime.now() - alert['time']
                    if time_diff.total_seconds() < 3600:
                        time_text = f"{int(time_diff.total_seconds() // 60)} daqiqa oldin"
                    else:
                        time_text = f"{int(time_diff.total_seconds() // 3600)} soat oldin"
                    
                    alerts_text += (
                        f"{i}. {alert_emoji} {alert['message']}\n"
                        f"   ⏰ {time_text}\n\n"
                    )
            else:
                alerts_text += "✅ Hozircha ogohlantirishlar yo'q\n\n"
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔄 Yangilash", callback_data="ctrl_refresh_alerts"),
                    InlineKeyboardButton(text="📊 Batafsil", callback_data="ctrl_detailed_alerts")
                ],
                [
                    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="ctrl_back_to_realtime")
                ]
            ])
            
            await callback.message.edit_text(alerts_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_realtime_performance")
    async def view_performance_metrics(callback: CallbackQuery, state: FSMContext):
        """View performance metrics"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Sizning hududingiz topilmadi. Iltimos, boshqaruvchi bilan bog'laning.")
                return
            
            controller_id = user['id']
            realtime_data = await get_realtime_data(region, controller_id)
            
            performance_text = (
                "📈 <b>Samaradorlik ko'rsatkichlari</b>\n\n"
                "⏰ <b>Vaqt ko'rsatkichlari:</b>\n"
                f"• O'rtacha javob vaqti: {realtime_data['avg_response_time']}\n"
                f"• Tizim ishlashi: {realtime_data['system_uptime']}\n\n"
                "📊 <b>Bajarish ko'rsatkichlari:</b>\n"
                f"• Mijozlar mamnuniyati: {realtime_data['performance_metrics']['satisfaction_score']}\n"
                f"• Faol sessiyalar: {realtime_data['performance_metrics']['active_sessions']}\n"
                f"• Bajarish darajasi: {realtime_data['performance_metrics']['completion_rate']}\n\n"
                "👨‍🔧 <b>Texniklar samaradorligi:</b>\n"
                f"• Faol texniklar: {realtime_data['active_technicians']}/{realtime_data['total_technicians']}\n"
                f"• O'rtacha ish yuki: {realtime_data['performance_metrics']['response_time_avg']}\n\n"
                f"⏰ <b>Yangilangan:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔄 Yangilash", callback_data="ctrl_refresh_performance"),
                    InlineKeyboardButton(text="📊 Batafsil", callback_data="ctrl_detailed_performance")
                ],
                [
                    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="ctrl_back_to_realtime")
                ]
            ])
            
            await callback.message.edit_text(performance_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    
    @router.callback_query(F.data == "ctrl_back_to_realtime")
    async def back_to_realtime_monitoring(callback: CallbackQuery, state: FSMContext):
        """Back to real-time monitoring menu"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Sizning hududingiz topilmadi. Iltimos, boshqaruvchi bilan bog'laning.")
                return
            
            controller_id = user['id']
            
            # Get realtime data
            realtime_data = await get_realtime_data(region, controller_id)
            
            monitoring_text = await format_monitoring_message(realtime_data, lang)
            
            keyboard = get_realtime_monitoring_keyboard(lang)
            
            await callback.message.edit_text(
                text=monitoring_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    # Simple refresh for entry dashboard
    @router.callback_query(F.data == "ctrl_refresh_realtime")
    async def realtime_refresh(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            # Reuse entry rendering
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Sizning hududingiz topilmadi. Iltimos, boshqaruvchi bilan bog'laning.")
                return
            
            controller_id = user['id']
            realtime_data = await get_realtime_data(region, controller_id)
            monitoring_text = await format_monitoring_message(realtime_data, lang)
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=("📋 Zayavkalar ro'yxati" if lang=='uz' else "📋 Список заявок"), callback_data="ctrl_realtime_requests")],
                [InlineKeyboardButton(text=("🚨 Shoshilinch zayavkalar" if lang=='uz' else "🚨 Срочные заявки"), callback_data="ctrl_realtime_urgent")],
                [InlineKeyboardButton(text=("⏰ Vaqt kuzatish" if lang=='uz' else "⏰ Отслеживание времени"), callback_data="ctrl_time_tracking")],
                [InlineKeyboardButton(text=("🔄 Yangilash" if lang=='uz' else "🔄 Обновить"), callback_data="ctrl_refresh_realtime")],
            ])
            await callback.message.edit_text(monitoring_text, reply_markup=keyboard, parse_mode='HTML')
        except Exception:
            await callback.answer("❌ Xatolik yuz berdi")

    # Refresh handlers
    @router.callback_query(F.data.startswith("ctrl_refresh_"))
    async def refresh_realtime_data(callback: CallbackQuery, state: FSMContext):
        """Refresh real-time data"""
        try:
            await callback.answer("🔄 Yangilandi")
            
            # Determine which section to refresh based on callback data
            refresh_type = callback.data.replace("ctrl_refresh_", "")
            
            if refresh_type == "status":
                await view_live_status(callback, state)
            elif refresh_type == "activities":
                await view_recent_activities(callback, state)
            elif refresh_type == "alerts":
                await view_system_alerts(callback, state)
            elif refresh_type == "performance":
                await view_performance_metrics(callback, state)
            
        except Exception as e:
            await callback.answer("❌ Yangilashda xatolik")

    # Detailed view handlers
    @router.callback_query(F.data.startswith("ctrl_detailed_"))
    async def view_detailed_data(callback: CallbackQuery, state: FSMContext):
        """View detailed data"""
        try:
            await callback.answer()
            
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Sizning hududingiz topilmadi. Iltimos, boshqaruvchi bilan bog'laning.")
                return
            
            controller_id = user['id']
            detailed_data = await get_realtime_data(region, controller_id)
            
            detail_type = callback.data.replace("ctrl_detailed_", "")
            
            if detail_type == "status":
                detailed_text = (
                    "📊 <b>Batafsil tizim holati</b>\n\n"
                    "📈 <b>Umumiy ko'rsatkichlar:</b>\n"
                    f"• Jami arizalar: {detailed_data['system_overview']['total_requests']}\n"
                    f"• Faol arizalar: {detailed_data['system_overview']['active_requests']}\n"
                    f"• Bugun bajarilgan: {detailed_data['system_overview']['completed_today']}\n"
                    f"• Kutilmoqda: {detailed_data['system_overview']['pending_requests']}\n"
                    f"• Shoshilinch: {detailed_data['system_overview']['urgent_requests']}\n\n"
                    "👨‍🔧 <b>Texniklar holati:</b>\n"
                    f"• Jami texniklar: {detailed_data['technician_status']['total_technicians']}\n"
                    f"• Mavjud texniklar: {detailed_data['technician_status']['available_technicians']}\n"
                    f"• Band texniklar: {detailed_data['technician_status']['busy_technicians']}\n"
                    f"• Oflayn texniklar: {detailed_data['technician_status']['offline_technicians']}\n"
                    f"• O'rtacha ish yuki: {detailed_data['technician_status']['avg_workload']}\n\n"
                    "📈 <b>Samaradorlik:</b>\n"
                    f"• O'rtacha javob vaqti: {detailed_data['performance_metrics']['avg_response_time']}\n"
                    f"• O'rtacha bajarish vaqti: {detailed_data['performance_metrics']['avg_completion_time']}\n"
                    f"• Mijozlar mamnuniyati: {detailed_data['performance_metrics']['satisfaction_rate']}\n"
                    f"• Tizim ishlashi: {detailed_data['performance_metrics']['system_uptime']}"
                )
            elif detail_type == "alerts":
                detailed_text = (
                    "🚨 <b>Shoshilinch zayavkalar</b>\n\n"
                )
                
                for i, request in enumerate(detailed_data['urgent_requests_with_time'], 1):
                    priority_emoji = get_priority_emoji(request['priority'])
                    status_emoji = get_status_emoji(request['current_role_minutes'])
                    
                    detailed_text += (
                        f"{i}. {status_emoji} <b>{request['client_name']}</b>\n"
                        f"   {priority_emoji} {request['workflow_type']}\n"
                        f"   👤 {request['current_role_actor_name']} ({request['current_role_actor_role']})\n"
                        f"   ⏰ Umumiy vaqt: {request['total_duration']}\n"
                        f"   🔄 Joriy rolda: {request['current_role_duration']}\n"
                        f"   📍 {request['location']}\n\n"
                    )
            else:
                detailed_text = "📊 Batafsil ma'lumotlar ko'rsatilmoqda..."
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="ctrl_back_to_realtime")
                ]
            ])
            
            await callback.message.edit_text(detailed_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    # ===== Manager-like controllers: Requests list (1-by-1) =====
    @router.callback_query(F.data == "ctrl_realtime_requests")
    async def ctrl_realtime_requests(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Sizning hududingiz topilmadi. Iltimos, boshqaruvchi bilan bog'laning.")
                return
            
            controller_id = user['id']
            detailed = await get_realtime_data(region, controller_id)
            requests = detailed.get('urgent_requests', [])
            if not requests:
                await callback.answer("Faol zayavkalar yo'q", show_alert=True)
                return
            data = await state.get_data()
            idx = data.get('ctrl_req_idx', 0)
            if idx < 0 or idx >= len(requests):
                idx = 0
            req = requests[idx]
            status_emo = get_status_emoji(req.get('current_role_minutes', 0))
            text = (
                f"📋 <b>Zayavka #{idx+1} / {len(requests)}</b>\n\n"
                f"{status_emo} <b>{req.get('client_name','-')}</b>\n"
                f"   🏷️ Turi: {req.get('workflow_type','-')}\n"
                f"   👤 Joriy: {req.get('current_role_actor_name','-')} ({req.get('current_role_actor_role','-')})\n"
                f"   ⏰ Joriy rolda: {req.get('current_role_duration','-')}\n"
                f"   ⏰ Umumiy: {req.get('total_duration','-')}\n"
                f"   📍 Manzil: {req.get('location','-')}\n"
            )
            kb_rows = []
            if len(requests) > 1:
                kb_rows.append([
                    InlineKeyboardButton(text=("◀️ Oldingi" if lang=='uz' else "◀️ Предыдущая"), callback_data="ctrl_prev_request"),
                    InlineKeyboardButton(text=f"{idx+1}/{len(requests)}", callback_data="noop"),
                    InlineKeyboardButton(text=("Keyingi ▶️" if lang=='uz' else "Следующая ▶️"), callback_data="ctrl_next_request"),
                ])
            kb_rows.append([InlineKeyboardButton(text=("⬅️ Orqaga" if lang=='uz' else "⬅️ Назад"), callback_data="ctrl_back_to_realtime")])
            await state.update_data(ctrl_req_idx=idx)
            await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb_rows), parse_mode='HTML')
        except Exception:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_prev_request")
    async def ctrl_prev_request(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        idx = max(0, data.get('ctrl_req_idx', 0) - 1)
        await state.update_data(ctrl_req_idx=idx)
        await ctrl_realtime_requests(callback, state)

    @router.callback_query(F.data == "ctrl_next_request")
    async def ctrl_next_request(callback: CallbackQuery, state: FSMContext):
        region = await get_user_region(callback.from_user.id)
        if not region:
            await callback.answer("Sizning hududingiz topilmadi. Iltimos, boshqaruvchi bilan bog'laning.")
            return
        
        controller_id = await get_user_by_telegram_id(callback.from_user.id)['id']
        detailed = await get_realtime_data(region, controller_id)
        total = len(detailed.get('urgent_requests', []))
        data = await state.get_data()
        idx = min(total-1, data.get('ctrl_req_idx', 0) + 1)
        await state.update_data(ctrl_req_idx=idx)
        await ctrl_realtime_requests(callback, state)

    # ===== Urgent list (1-by-1) =====
    @router.callback_query(F.data == "ctrl_realtime_urgent")
    async def ctrl_realtime_urgent(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Sizning hududingiz topilmadi. Iltimos, boshqaruvchi bilan bog'laning.")
                return
            
            controller_id = user['id']
            rt = await get_realtime_data(region, controller_id)
            urgent = rt.get('urgent_requests', [])
            if not urgent:
                await callback.answer("Shoshilinch zayavkalar yo'q", show_alert=True)
                return
            data = await state.get_data()
            idx = data.get('ctrl_urgent_idx', 0)
            if idx < 0 or idx >= len(urgent):
                idx = 0
            req = urgent[idx]
            duration = req.get('current_role_duration', '-')
            text = (
                f"🚨 <b>Shoshilinch zayavka</b>\n\n"
                f"🔴 <b>{req.get('client_name','-')}</b>\n"
                f"   ⏰ {duration}\n"
                f"   👤 Joriy: {req.get('current_role_actor_name','-')} ({req.get('current_role_actor_role','-')})\n"
                f"   📍 Manzil: {req.get('location','-')}\n"
                f"   📅 Yaratilgan: {req.get('created_at','-')}\n"
            )
            rows = []
            if len(urgent) > 1:
                rows.append([
                    InlineKeyboardButton(text=("◀️ Oldingi" if lang=='uz' else "◀️ Предыдущая"), callback_data="ctrl_prev_urgent"),
                    InlineKeyboardButton(text=("Keyingi ▶️" if lang=='uz' else "Следующая ▶️"), callback_data="ctrl_next_urgent"),
                ])
            rows.append([InlineKeyboardButton(text=("⬅️ Orqaga" if lang=='uz' else "⬅️ Назад"), callback_data="ctrl_back_to_realtime")])
            await state.update_data(ctrl_urgent_idx=idx)
            await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=rows), parse_mode='HTML')
        except Exception:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_prev_urgent")
    async def ctrl_prev_urgent(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        idx = max(0, data.get('ctrl_urgent_idx', 0) - 1)
        await state.update_data(ctrl_urgent_idx=idx)
        await ctrl_realtime_urgent(callback, state)

    @router.callback_query(F.data == "ctrl_next_urgent")
    async def ctrl_next_urgent(callback: CallbackQuery, state: FSMContext):
        region = await get_user_region(callback.from_user.id)
        if not region:
            await callback.answer("Sizning hududingiz topilmadi. Iltimos, boshqaruvchi bilan bog'laning.")
            return
        
        controller_id = await get_user_by_telegram_id(callback.from_user.id)['id']
        rt = await get_realtime_data(region, controller_id)
        total = len(rt.get('urgent_requests', []))
        data = await state.get_data()
        idx = min(total-1, data.get('ctrl_urgent_idx', 0) + 1)
        await state.update_data(ctrl_urgent_idx=idx)
        await ctrl_realtime_urgent(callback, state)

    # ===== Time tracking (1-by-1) =====
    @router.callback_query(F.data == "ctrl_time_tracking")
    async def ctrl_time_tracking(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            user = await get_user_by_telegram_id(callback.from_user.id)
            lang = user.get('language', 'uz')
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Sizning hududingiz topilmadi. Iltimos, boshqaruvchi bilan bog'laning.")
                return
            
            controller_id = user['id']
            detailed = await get_realtime_data(region, controller_id)
            reqs = detailed.get('urgent_requests_with_time', [])
            if not reqs:
                await callback.answer("Faol zayavkalar yo'q", show_alert=True)
                return
            data = await state.get_data()
            idx = data.get('ctrl_time_idx', 0)
            if idx < 0 or idx >= len(reqs):
                idx = 0
            req = reqs[idx]
            total = req.get('total_duration', '-')
            current = req.get('current_role_duration', '-')
            cur_min = req.get('current_role_minutes', 0)
            status_emo = get_status_emoji(cur_min)
            text = (
                f"⏰ <b>Vaqt kuzatish #{idx+1} / {len(reqs)}</b>\n\n"
                f"{status_emo} <b>{req.get('client_name','-')}</b>\n"
                f"   ⏰ Umumiy: {total}\n"
                f"   🔄 Joriy rol: {req.get('current_role_actor_role','-')} ({current})\n"
            )
            rows = []
            if len(reqs) > 1:
                rows.append([
                    InlineKeyboardButton(text=("◀️ Oldingi" if lang=='uz' else "◀️ Предыдущая"), callback_data="ctrl_prev_time"),
                    InlineKeyboardButton(text=("Keyingi ▶️" if lang=='uz' else "Следующая ▶️"), callback_data="ctrl_next_time"),
                ])
            rows.append([InlineKeyboardButton(text=("⬅️ Orqaga" if lang=='uz' else "⬅️ Назад"), callback_data="ctrl_back_to_realtime")])
            await state.update_data(ctrl_time_idx=idx)
            await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=rows), parse_mode='HTML')
        except Exception:
            await callback.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_prev_time")
    async def ctrl_prev_time(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        idx = max(0, data.get('ctrl_time_idx', 0) - 1)
        await state.update_data(ctrl_time_idx=idx)
        await ctrl_time_tracking(callback, state)

    @router.callback_query(F.data == "ctrl_next_time")
    async def ctrl_next_time(callback: CallbackQuery, state: FSMContext):
        region = await get_user_region(callback.from_user.id)
        if not region:
            await callback.answer("Sizning hududingiz topilmadi. Iltimos, boshqaruvchi bilan bog'laning.")
            return
        
        controller_id = await get_user_by_telegram_id(callback.from_user.id)['id']
        detailed = await get_realtime_data(region, controller_id)
        total = len(detailed.get('urgent_requests_with_time', []))
        data = await state.get_data()
        idx = min(total-1, data.get('ctrl_time_idx', 0) + 1)
        await state.update_data(ctrl_time_idx=idx)
        await ctrl_time_tracking(callback, state)

    return router 