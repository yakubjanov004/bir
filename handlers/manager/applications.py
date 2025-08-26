"""
Applications Main Router - Mock Data Implementation

Bu modul barcha applications sub-routerlarini birlashtiradi va 
qo'shimcha umumiy funksionallikni ta'minlaydi.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter
import logging

logger = logging.getLogger(__name__)

# Mock data storage
mock_application_stats = {
    'total': 25,
    'completed': 18,
    'active': 5,
    'new': 2,
    'cancelled': 0,
    'today': 3,
    'this_week': 12
}

mock_recent_applications = [
    {
        'id': 'req_001_2024_01_15',
        'current_status': 'in_progress',
        'workflow_type': 'connection_request',
        'priority': 'high'
    },
    {
        'id': 'req_002_2024_01_16',
        'current_status': 'created',
        'workflow_type': 'technical_service',
        'priority': 'normal'
    },
    {
        'id': 'req_003_2024_01_17',
        'current_status': 'completed',
        'workflow_type': 'call_center_direct',
        'priority': 'low'
    },
    {
        'id': 'req_004_2024_01_18',
        'current_status': 'created',
        'workflow_type': 'connection_request',
        'priority': 'urgent'
    },
    {
        'id': 'req_005_2024_01_19',
        'current_status': 'in_progress',
        'workflow_type': 'technical_service',
        'priority': 'high'
    }
]

mock_tracker_stats = {
    'total': 25,
    'completed': 18,
    'completion_rate': 72,
    'avg_rating': 4.6
}

# Mock functions
async def get_user_by_telegram_id(region: str, user_id: int):
    """Mock get user by telegram ID"""
    return {
        'id': 1,
        'telegram_id': user_id,
        'role': 'manager',
        'language': 'uz',
        'full_name': 'Test Manager',
        'phone_number': '+998901234567'
    }

async def get_application_statistics(region: str, manager_id: int = None):
    """Mock get application statistics"""
    return mock_application_stats

async def get_manager_applications(region: str, manager_id: int = None, limit: int = 10):
    """Mock get manager applications"""
    return mock_recent_applications[:limit]

class MockApplicationTracker:
    """Mock application tracker"""
    async def get_statistics(self):
        """Mock get statistics"""
        return mock_tracker_stats

class MockAuditLogger:
    """Mock audit logger"""
    async def log_manager_action(self, manager_id: int, action: str, details: dict = None):
        """Mock log manager action"""
        logger.info(f"Mock: Manager {manager_id} performed action: {action}")
        if details:
            logger.info(f"Mock: Details: {details}")

# Initialize mock instances
application_tracker = MockApplicationTracker()
audit_logger = MockAuditLogger()

def get_manager_applications_router():
    """Main applications router that combines all sub-routers"""
    router = Router()
    
    # Apply role filter to entire router - both manager and junior_manager can access
    role_filter = RoleFilter(["manager", "junior_manager"])
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    # NOTE: Sub-routers are included in handlers/manager/__init__.py
    # Do not include them here to avoid duplicate inclusion
    
    # Add main applications command handler
    @router.message(F.text.in_(["📋 Arizalarni ko'rish", "📋 Все заявки"]), flags={"block": False})
    async def show_applications_menu(message: Message, state: FSMContext):
        """Show applications main menu with statistics using mock data"""
        try:
            user_id = message.from_user.id
            
            # Get user info
            user = await get_user_by_telegram_id('toshkent', user_id)
            if not user:
                await message.answer("❌ Foydalanuvchi topilmadi")
                return
            
            lang = user.get('language', 'uz')
            
            # Get applications statistics from mock data
            stats = await get_application_statistics('toshkent', manager_id=user.get('id'))
            
            # Format statistics message
            if lang == 'uz':
                text = f"""📊 <b>Arizalar statistikasi</b>

📁 Jami arizalar: {stats.get('total', 0)}
✅ Bajarilgan: {stats.get('completed', 0)}
⏳ Faol: {stats.get('active', 0)}
🆕 Yangi: {stats.get('new', 0)}
❌ Bekor qilingan: {stats.get('cancelled', 0)}

📅 Bugun: {stats.get('today', 0)}
📆 Bu hafta: {stats.get('this_week', 0)}

Qaysi arizalarni ko'rmoqchisiz?"""
            else:
                text = f"""📊 <b>Статистика заявок</b>

📁 Всего заявок: {stats.get('total', 0)}
✅ Выполнено: {stats.get('completed', 0)}
⏳ Активные: {stats.get('active', 0)}
🆕 Новые: {stats.get('new', 0)}
❌ Отменено: {stats.get('cancelled', 0)}

📅 Сегодня: {stats.get('today', 0)}
📆 На этой неделе: {stats.get('this_week', 0)}

Какие заявки вы хотите посмотреть?"""
            
            # Get keyboard - to'g'ri callback data'lar bilan
            from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            
            # Create custom keyboard with correct callback data
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📋 Hammasi", callback_data="mgr_view_all_applications")],
                [InlineKeyboardButton(text="⏳ Faol", callback_data="mgr_view_active_applications")],
                [InlineKeyboardButton(text="✅ Bajarilgan", callback_data="mgr_view_completed_applications")],
                [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu")]
            ])
            
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
            # Log action using mock audit logger
            await audit_logger.log_manager_action(
                manager_id=user.get('id'),
                action='view_applications_menu',
                details={'statistics': stats}
            )
            
        except Exception as e:
            logger.error(f"Error showing applications menu: {e}")
            await message.answer("❌ Xatolik yuz berdi")
    
    # Add quick stats command
    @router.message(F.text.in_(["📊 Statistika", "📊 Статистика"]), flags={"block": False})
    async def show_quick_stats(message: Message, state: FSMContext):
        """Show quick applications statistics using mock data"""
        try:
            user_id = message.from_user.id
            
            # Get user info
            user = await get_user_by_telegram_id('toshkent', user_id)
            if not user:
                await message.answer("❌ Foydalanuvchi topilmadi")
                return
            
            lang = user.get('language', 'uz')
            
            # Get recent applications from mock data
            recent_apps = await get_manager_applications(
                'toshkent',
                manager_id=user.get('id'),
                limit=5
            )
            
            # Get statistics from mock tracker
            stats = await application_tracker.get_statistics()
            
            # Format message
            if lang == 'uz':
                text = f"""📊 <b>Tezkor statistika</b>

📈 Umumiy ko'rsatkichlar:
• Jami: {stats.get('total', 0)}
• Bajarilgan: {stats.get('completed', 0)} ({stats.get('completion_rate', 0)}%)
• O'rtacha baho: ⭐ {stats.get('avg_rating', 0)}

📝 Oxirgi arizalar: {len(recent_apps)}"""
                
                if recent_apps:
                    text += "\n\n<b>Oxirgi 5 ta ariza:</b>\n"
                    for i, app in enumerate(recent_apps[:5], 1):
                        status_emoji = {
                            'created': '🆕',
                            'in_progress': '⏳',
                            'completed': '✅',
                            'cancelled': '❌'
                        }.get(app.get('current_status'), '📋')
                        
                        priority_emoji = {
                            'low': '🔵',
                            'normal': '🟢',
                            'high': '🔴',
                            'urgent': '🚨'
                        }.get(app.get('priority'), '🟢')
                        
                        text += f"{i}. {status_emoji} {app.get('id', 'N/A')} - {priority_emoji} {app.get('current_status', 'N/A')}\n"
            else:
                text = f"""📊 <b>Быстрая статистика</b>

📈 Общие показатели:
• Всего: {stats.get('total', 0)}
• Выполнено: {stats.get('completed', 0)} ({stats.get('completion_rate', 0)}%)
• Средняя оценка: ⭐ {stats.get('avg_rating', 0)}

📝 Последние заявки: {len(recent_apps)}"""
                
                if recent_apps:
                    text += "\n\n<b>Последние 5 заявок:</b>\n"
                    for i, app in enumerate(recent_apps[:5], 1):
                        status_emoji = {
                            'created': '🆕',
                            'in_progress': '⏳',
                            'completed': '✅',
                            'cancelled': '❌'
                        }.get(app.get('current_status'), '📋')
                        
                        priority_emoji = {
                            'low': '🔵',
                            'normal': '🟢',
                            'high': '🔴',
                            'urgent': '🚨'
                        }.get(app.get('priority'), '🟢')
                        
                        text += f"{i}. {status_emoji} {app.get('id', 'N/A')} - {priority_emoji} {app.get('current_status', 'N/A')}\n"
            
            await message.answer(text, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error showing quick stats: {e}")
            await message.answer("❌ Xatolik yuz berdi")

    return router