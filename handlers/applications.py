"""
Applications Main Router - Mock Data Version

Bu modul barcha applications sub-routerlarini birlashtiradi va 
qo'shimcha umumiy funksionallikni ta'minlaydi.
Mock data bilan ishlaydi, database kerak emas.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging

logger = logging.getLogger(__name__)

# Mock data for applications
MOCK_APPLICATIONS = [
    {
        'id': 'APP001',
        'client_name': 'Aziz Karimov',
        'address': 'Toshkent, Chilonzor tumani',
        'status': 'new',
        'created_date': '2024-01-15',
        'priority': 'normal',
        'type': 'connection'
    },
    {
        'id': 'APP002',
        'client_name': 'Malika Yusupova',
        'address': 'Toshkent, Sergeli tumani',
        'status': 'active',
        'created_date': '2024-01-14',
        'priority': 'high',
        'type': 'technical'
    },
    {
        'id': 'APP003',
        'client_name': 'Jasur Toshmatov',
        'address': 'Toshkent, Yashnobod tumani',
        'status': 'completed',
        'created_date': '2024-01-13',
        'priority': 'normal',
        'type': 'connection'
    },
    {
        'id': 'APP004',
        'client_name': 'Dilfuza Rahimova',
        'address': 'Toshkent, Mirabad tumani',
        'status': 'active',
        'created_date': '2024-01-12',
        'priority': 'urgent',
        'type': 'technical'
    },
    {
        'id': 'APP005',
        'client_name': 'Rustam Alimov',
        'address': 'Toshkent, Shayxontohur tumani',
        'status': 'completed',
        'created_date': '2024-01-11',
        'priority': 'low',
        'type': 'connection'
    }
]

# Mock statistics
MOCK_STATISTICS = {
    'total': 156,
    'completed': 89,
    'active': 45,
    'new': 22,
    'cancelled': 8,
    'today': 5,
    'this_week': 23
}

def get_manager_applications_router():
    """Main applications router that combines all sub-routers"""
    router = Router()
    
    # Import and include all sub-routers
    from handlers.applications_list import get_manager_applications_list_router
    from handlers.applications_search import get_manager_applications_search_router
    from handlers.applications_actions import get_manager_applications_actions_router
    from handlers.applications_callbacks import get_manager_applications_callbacks_router
    
    # Include all sub-routers
    router.include_router(get_manager_applications_list_router())
    router.include_router(get_manager_applications_search_router())
    router.include_router(get_manager_applications_actions_router())
    router.include_router(get_manager_applications_callbacks_router())
    
    # Add main applications command handler
    @router.message(F.text.in_(["📋 Arizalarni ko'rish", "📋 Все заявки"]))
    async def show_applications_menu(message: Message, state: FSMContext):
        """Show applications main menu with statistics"""
        try:
            user_id = message.from_user.id
            
            # Mock user info
            mock_user = {
                'id': user_id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Get applications statistics from mock data
            stats = MOCK_STATISTICS
            
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
            
            # Get keyboard
            from keyboards.manager_buttons import get_manager_view_applications_keyboard
            keyboard = get_manager_view_applications_keyboard(lang)
            
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error showing applications menu: {e}")
            await message.answer("❌ Xatolik yuz berdi")
    
    # Add quick stats command
    @router.message(F.text.in_(["📊 Statistika", "📊 Статистика"]))
    async def show_quick_stats(message: Message, state: FSMContext):
        """Show quick applications statistics"""
        try:
            user_id = message.from_user.id
            
            # Mock user info
            mock_user = {
                'id': user_id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Get recent applications from mock data
            recent_apps = MOCK_APPLICATIONS[:5]
            
            # Get statistics from mock data
            stats = MOCK_STATISTICS
            
            # Calculate completion rate
            completion_rate = round((stats.get('completed', 0) / stats.get('total', 1)) * 100, 1)
            avg_rating = 4.2  # Mock average rating
            
            # Format message
            if lang == 'uz':
                text = f"""📊 <b>Tezkor statistika</b>

📈 Umumiy ko'rsatkichlar:
• Jami: {stats.get('total', 0)}
• Bajarilgan: {stats.get('completed', 0)} ({completion_rate}%)
• O'rtacha baho: ⭐ {avg_rating}

📝 Oxirgi arizalar: {len(recent_apps)}"""
                
                if recent_apps:
                    text += "\n\n<b>Oxirgi 5 ta ariza:</b>\n"
                    for i, app in enumerate(recent_apps[:5], 1):
                        text += f"{i}. {app.get('id', 'N/A')} - {app.get('status', 'N/A')}\n"
            else:
                text = f"""📊 <b>Быстрая статистика</b>

📈 Общие показатели:
• Всего: {stats.get('total', 0)}
• Выполнено: {stats.get('completed', 0)} ({completion_rate}%)
• Средняя оценка: ⭐ {avg_rating}

📝 Последние заявки: {len(recent_apps)}"""
                
                if recent_apps:
                    text += "\n\n<b>Последние 5 заявок:</b>\n"
                    for i, app in enumerate(recent_apps[:5], 1):
                        text += f"{i}. {app.get('id', 'N/A')} - {app.get('status', 'N/A')}\n"
            
            await message.answer(text, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error showing quick stats: {e}")
            await message.answer("❌ Xatolik yuz berdi")

    return router