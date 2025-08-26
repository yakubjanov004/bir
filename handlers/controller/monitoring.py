"""
Controller Monitoring - Mock Data Implementation

This module handles controller monitoring functionality with mock data.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.controllers_buttons import get_monitoring_keyboard, get_controller_back_keyboard, get_monitoring_detailed_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
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

# Mock controller requests data
mock_controller_requests = [
    {
        'id': 'REQ001',
        'current_status': 'pending_assignment',
        'created_at': datetime.now() - timedelta(hours=2),
        'updated_at': datetime.now() - timedelta(hours=2)
    },
    {
        'id': 'REQ002',
        'current_status': 'assigned_to_technician',
        'created_at': datetime.now() - timedelta(hours=4),
        'updated_at': datetime.now() - timedelta(hours=1)
    },
    {
        'id': 'REQ003',
        'current_status': 'work_in_progress',
        'created_at': datetime.now() - timedelta(hours=6),
        'updated_at': datetime.now() - timedelta(hours=2)
    },
    {
        'id': 'REQ004',
        'current_status': 'completed',
        'created_at': datetime.now() - timedelta(hours=8),
        'updated_at': datetime.now() - timedelta(hours=1)
    },
    {
        'id': 'REQ005',
        'current_status': 'completed',
        'created_at': datetime.now() - timedelta(hours=10),
        'updated_at': datetime.now() - timedelta(hours=30, minutes=30)
    },
    {
        'id': 'REQ006',
        'current_status': 'cancelled',
        'created_at': datetime.now() - timedelta(hours=12),
        'updated_at': datetime.now() - timedelta(hours=11)
    },
    {
        'id': 'REQ007',
        'current_status': 'pending_assignment',
        'created_at': datetime.now() - timedelta(hours=1),
        'updated_at': datetime.now() - timedelta(hours=1)
    },
    {
        'id': 'REQ008',
        'current_status': 'assigned_to_technician',
        'created_at': datetime.now() - timedelta(hours=3),
        'updated_at': datetime.now() - timedelta(hours=2)
    }
]

# Mock technician workload data
mock_technician_workload = [
    {
        'id': 2001,
        'assigned_count': 3,
        'in_progress_count': 2,
        'completed_today': 1
    },
    {
        'id': 2002,
        'assigned_count': 2,
        'in_progress_count': 1,
        'completed_today': 1
    },
    {
        'id': 2003,
        'assigned_count': 1,
        'in_progress_count': 1,
        'completed_today': 0
    },
    {
        'id': 2004,
        'assigned_count': 0,
        'in_progress_count': 0,
        'completed_today': 0
    },
    {
        'id': 2005,
        'assigned_count': 2,
        'in_progress_count': 1,
        'completed_today': 1
    }
]

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

async def get_monitoring_data(region: str, controller_id: int) -> Dict[str, Any]:
    """Get monitoring data from mock data"""
    try:
        logger.info(f"Mock: Getting monitoring data for controller {controller_id} in region {region}")
        
        # Calculate statistics from mock data
        total_applications = len(mock_controller_requests)
        pending = len([r for r in mock_controller_requests if r.get('current_status') == 'pending_assignment'])
        in_progress = len([r for r in mock_controller_requests if r.get('current_status') in ['assigned_to_technician', 'work_in_progress']])
        completed = len([r for r in mock_controller_requests if r.get('current_status') == 'completed'])
        cancelled = len([r for r in mock_controller_requests if r.get('current_status') == 'cancelled'])
        
        # Calculate today's stats
        today = datetime.now().date()
        today_applications = len([r for r in mock_controller_requests 
                                 if r.get('created_at') and 
                                 r.get('created_at').date() == today])
        
        today_completed = len([r for r in mock_controller_requests 
                             if r.get('current_status') == 'completed' and
                             r.get('updated_at') and
                             r.get('updated_at').date() == today])
        
        # Calculate weekly stats
        week_ago = datetime.now() - timedelta(days=7)
        weekly_applications = len([r for r in mock_controller_requests 
                                  if r.get('created_at') and 
                                  r.get('created_at') > week_ago])
        
        weekly_completed = len([r for r in mock_controller_requests 
                              if r.get('current_status') == 'completed' and
                              r.get('updated_at') and
                              r.get('updated_at') > week_ago])
        
        # Calculate technician stats
        active_technicians = len([t for t in mock_technician_workload if t.get('assigned_count', 0) > 0])
        total_technicians = len(mock_technician_workload)
        
        # Calculate average response time (simplified)
        avg_response_hours = 2.5  # Mock default value
        success_rate = (completed / max(total_applications, 1)) * 100
        
        return {
            'total_applications': total_applications,
            'pending': pending,
            'in_progress': in_progress,
            'completed': completed,
            'cancelled': cancelled,
            'active_technicians': active_technicians,
            'total_technicians': total_technicians,
            'avg_response_time': f'{avg_response_hours:.1f} soat',
            'success_rate': f'{success_rate:.1f}%',
            'today_applications': today_applications,
            'today_completed': today_completed,
            'weekly_applications': weekly_applications,
            'weekly_completed': weekly_completed,
            'pending_assignment': pending,
            'active_work': in_progress,
            'completed_today': today_completed
        }
        
    except Exception as e:
        logger.error(f"Error getting monitoring data: {e}")
        return {
            'total_applications': 0,
            'pending': 0,
            'in_progress': 0,
            'completed': 0,
            'cancelled': 0,
            'active_technicians': 0,
            'total_technicians': 0,
            'avg_response_time': 'N/A',
            'success_rate': '0%',
            'today_applications': 0,
            'today_completed': 0,
            'weekly_applications': 0,
            'weekly_completed': 0
        }

async def get_system_status(region: str) -> Dict[str, Any]:
    """Get system status from mock data"""
    try:
        logger.info(f"Mock: Getting system status for region {region}")
        
        # Mock system status data
        db_status = 'healthy'
        last_backup = datetime.now() - timedelta(hours=1)
        uptime = 99.9
        
        return {
            'system_status': 'online',
            'database_status': db_status,
            'api_status': 'operational',
            'notification_status': 'active',
            'last_backup': last_backup.strftime('%Y-%m-%d %H:%M'),
            'uptime': f'{uptime:.1f}%'
        }
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return {
            'system_status': 'error',
            'database_status': 'unknown',
            'api_status': 'unknown',
            'notification_status': 'unknown',
            'last_backup': 'N/A',
            'uptime': 'N/A'
        }

def get_controller_monitoring_router():
    """Router for monitoring functionality"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📊 Monitoring", "📊 Мониторинг"]))
    async def view_monitoring(message: Message, state: FSMContext):
        """Controller view monitoring handler"""
        try:
            # Get region
            region = await get_user_region(message.from_user.id)
            if not region:
                await message.answer("❌ Region aniqlanmadi")
                return
            
            user = await get_user_by_telegram_id(region, message.from_user.id)
            if not user or user['role'] != 'controller':
                return
            
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Get monitoring data from mock data
            monitoring_data = await get_monitoring_data(region, controller_id)
            
            # Log action
            await audit_logger.log_action(
                user_id=message.from_user.id,
                action='CONTROLLER_ACTION',
                details={'action': 'viewed_monitoring'},
                region=region
            )
            
            if lang == 'uz':
                monitoring_text = (
                    "📊 <b>Monitoring - To'liq ma'lumot</b>\n\n"
                    "📈 <b>Umumiy statistika:</b>\n"
                    f"• Jami arizalar: {monitoring_data['total_applications']}\n"
                    f"• Kutilmoqda: {monitoring_data['pending']}\n"
                    f"• Jarayonda: {monitoring_data['in_progress']}\n"
                    f"• Bajarilgan: {monitoring_data['completed']}\n"
                    f"• Bekor qilingan: {monitoring_data['cancelled']}\n\n"
                    f"👨‍🔧 <b>Texniklar:</b> {monitoring_data['active_technicians']}/{monitoring_data['total_technicians']}\n"
                    f"⏰ <b>O'rtacha javob vaqti:</b> {monitoring_data['avg_response_time']}\n"
                    f"📈 <b>Muvaffaqiyat darajasi:</b> {monitoring_data['success_rate']}\n\n"
                    "Quyidagi bo'limlardan birini tanlang:"
                )
            else:
                monitoring_text = (
                    "📊 <b>Мониторинг - Полная информация</b>\n\n"
                    "📈 <b>Общая статистика:</b>\n"
                    f"• Всего заявок: {monitoring_data['total_applications']}\n"
                    f"• Ожидающие: {monitoring_data['pending']}\n"
                    f"• В процессе: {monitoring_data['in_progress']}\n"
                    f"• Завершенные: {monitoring_data['completed']}\n"
                    f"• Отмененные: {monitoring_data['cancelled']}\n\n"
                    f"👨‍🔧 <b>Техники:</b> {monitoring_data['active_technicians']}/{monitoring_data['total_technicians']}\n"
                    f"⏰ <b>Среднее время ответа:</b> {monitoring_data['avg_response_time']}\n"
                    f"📈 <b>Уровень успеха:</b> {monitoring_data['success_rate']}\n\n"
                    "Выберите один из разделов ниже:"
                )
            
            sent_message = await message.answer(
                text=monitoring_text,
                reply_markup=get_monitoring_keyboard(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            logger.error(f"Error in view_monitoring: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "view_detailed_statistics")
    async def view_detailed_statistics(callback: CallbackQuery, state: FSMContext):
        """View detailed statistics"""
        try:
            await callback.answer()
            
            # Get region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Get detailed monitoring data from mock data
            monitoring_data = await get_monitoring_data(region, controller_id)
            
            # Calculate percentages
            today_percentage = (monitoring_data['today_completed'] / max(monitoring_data['today_applications'], 1)) * 100
            weekly_percentage = (monitoring_data['weekly_completed'] / max(monitoring_data['weekly_applications'], 1)) * 100
            
            if lang == 'uz':
                stats_text = (
                    "📊 <b>Batafsil statistika - To'liq ma'lumot</b>\n\n"
                    "📅 <b>Bugungi ko'rsatkichlar:</b>\n"
                    f"• Yangi arizalar: {monitoring_data['today_applications']}\n"
                    f"• Bajarilgan: {monitoring_data['today_completed']}\n"
                    f"• Bajarish foizi: {today_percentage:.1f}%\n\n"
                    "📅 <b>Haftalik ko'rsatkichlar:</b>\n"
                    f"• Jami arizalar: {monitoring_data['weekly_applications']}\n"
                    f"• Bajarilgan: {monitoring_data['weekly_completed']}\n"
                    f"• Bajarish foizi: {weekly_percentage:.1f}%\n\n"
                    "📈 <b>Umumiy ko'rsatkichlar:</b>\n"
                    f"• Jami arizalar: {monitoring_data['total_applications']}\n"
                    f"• Bajarilgan: {monitoring_data['completed']}\n"
                    f"• Muvaffaqiyat darajasi: {monitoring_data['success_rate']}\n"
                    f"• O'rtacha javob vaqti: {monitoring_data['avg_response_time']}"
                )
            else:
                stats_text = (
                    "📊 <b>Подробная статистика - Полная информация</b>\n\n"
                    "📅 <b>Сегодняшние показатели:</b>\n"
                    f"• Новые заявки: {monitoring_data['today_applications']}\n"
                    f"• Выполнено: {monitoring_data['today_completed']}\n"
                    f"• Процент выполнения: {today_percentage:.1f}%\n\n"
                    "📅 <b>Недельные показатели:</b>\n"
                    f"• Всего заявок: {monitoring_data['weekly_applications']}\n"
                    f"• Выполнено: {monitoring_data['weekly_completed']}\n"
                    f"• Процент выполнения: {weekly_percentage:.1f}%\n\n"
                    "📈 <b>Общие показатели:</b>\n"
                    f"• Всего заявок: {monitoring_data['total_applications']}\n"
                    f"• Выполнено: {monitoring_data['completed']}\n"
                    f"• Уровень успеха: {monitoring_data['success_rate']}\n"
                    f"• Среднее время ответа: {monitoring_data['avg_response_time']}"
                )
            
            keyboard = get_monitoring_detailed_keyboard(lang)
            
            await callback.message.edit_text(stats_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in view_detailed_statistics: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "view_system_status")
    async def view_system_status(callback: CallbackQuery, state: FSMContext):
        """View system status"""
        try:
            await callback.answer()
            
            # Get region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get system status from mock data
            system_data = await get_system_status(region)
            
            # Log action
            await audit_logger.log_action(
                user_id=callback.from_user.id,
                action='CONTROLLER_ACTION',
                details={'action': 'viewed_system_status'},
                region=region
            )
            
            # Format status emojis
            status_emoji = {
                'online': '🟢',
                'operational': '🟢',
                'active': '🟢',
                'healthy': '🟢',
                'error': '🔴',
                'unknown': '🟡'
            }
            
            if lang == 'uz':
                status_text = (
                    "🖥️ <b>Tizim holati</b>\n\n"
                    f"{status_emoji.get(system_data['system_status'], '🟡')} <b>Tizim:</b> {system_data['system_status']}\n"
                    f"{status_emoji.get(system_data['database_status'], '🟡')} <b>Ma'lumotlar bazasi:</b> {system_data['database_status']}\n"
                    f"{status_emoji.get(system_data['api_status'], '🟡')} <b>API:</b> {system_data['api_status']}\n"
                    f"{status_emoji.get(system_data['notification_status'], '🟡')} <b>Bildirishnomalar:</b> {system_data['notification_status']}\n\n"
                    f"💾 <b>Oxirgi backup:</b> {system_data['last_backup']}\n"
                    f"⏱️ <b>Uptime:</b> {system_data['uptime']}"
                )
            else:
                status_text = (
                    "🖥️ <b>Состояние системы</b>\n\n"
                    f"{status_emoji.get(system_data['system_status'], '🟡')} <b>Система:</b> {system_data['system_status']}\n"
                    f"{status_emoji.get(system_data['database_status'], '🟡')} <b>База данных:</b> {system_data['database_status']}\n"
                    f"{status_emoji.get(system_data['api_status'], '🟡')} <b>API:</b> {system_data['api_status']}\n"
                    f"{status_emoji.get(system_data['notification_status'], '🟡')} <b>Уведомления:</b> {system_data['notification_status']}\n\n"
                    f"💾 <b>Последний backup:</b> {system_data['last_backup']}\n"
                    f"⏱️ <b>Uptime:</b> {system_data['uptime']}"
                )
            
            keyboard = get_controller_back_keyboard(lang)
            
            await callback.message.edit_text(status_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in view_system_status: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "refresh_monitoring")
    async def refresh_monitoring(callback: CallbackQuery, state: FSMContext):
        """Refresh monitoring data"""
        try:
            await callback.answer("🔄 Yangilanmoqda...")
            
            # Get region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Get fresh monitoring data from mock data
            monitoring_data = await get_monitoring_data(region, controller_id)
            
            if lang == 'uz':
                monitoring_text = (
                    "📊 <b>Monitoring - To'liq ma'lumot</b> 🔄\n\n"
                    "📈 <b>Umumiy statistika:</b>\n"
                    f"• Jami arizalar: {monitoring_data['total_applications']}\n"
                    f"• Kutilmoqda: {monitoring_data['pending']}\n"
                    f"• Jarayonda: {monitoring_data['in_progress']}\n"
                    f"• Bajarilgan: {monitoring_data['completed']}\n"
                    f"• Bekor qilingan: {monitoring_data['cancelled']}\n\n"
                    f"👨‍🔧 <b>Texniklar:</b> {monitoring_data['active_technicians']}/{monitoring_data['total_technicians']}\n"
                    f"⏰ <b>O'rtacha javob vaqti:</b> {monitoring_data['avg_response_time']}\n"
                    f"📈 <b>Muvaffaqiyat darajasi:</b> {monitoring_data['success_rate']}\n\n"
                    f"🕐 Yangilandi: {datetime.now().strftime('%H:%M:%S')}"
                )
            else:
                monitoring_text = (
                    "📊 <b>Мониторинг - Полная информация</b> 🔄\n\n"
                    "📈 <b>Общая статистика:</b>\n"
                    f"• Всего заявок: {monitoring_data['total_applications']}\n"
                    f"• Ожидающие: {monitoring_data['pending']}\n"
                    f"• В процессе: {monitoring_data['in_progress']}\n"
                    f"• Завершенные: {monitoring_data['completed']}\n"
                    f"• Отмененные: {monitoring_data['cancelled']}\n\n"
                    f"👨‍🔧 <b>Техники:</b> {monitoring_data['active_technicians']}/{monitoring_data['total_technicians']}\n"
                    f"⏰ <b>Среднее время ответа:</b> {monitoring_data['avg_response_time']}\n"
                    f"📈 <b>Уровень успеха:</b> {monitoring_data['success_rate']}\n\n"
                    f"🕐 Обновлено: {datetime.now().strftime('%H:%M:%S')}"
                )
            
            keyboard = get_monitoring_keyboard(lang)
            
            await callback.message.edit_text(monitoring_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in refresh_monitoring: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_monitoring")
    async def back_to_monitoring(callback: CallbackQuery, state: FSMContext):
        """Back to main monitoring menu"""
        try:
            await callback.answer()
            
            # Get region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Get monitoring data from mock data
            monitoring_data = await get_monitoring_data(region, controller_id)
            
            if lang == 'uz':
                monitoring_text = (
                    "📊 <b>Monitoring - To'liq ma'lumot</b>\n\n"
                    "📈 <b>Umumiy statistika:</b>\n"
                    f"• Jami arizalar: {monitoring_data['total_applications']}\n"
                    f"• Kutilmoqda: {monitoring_data['pending']}\n"
                    f"• Jarayonda: {monitoring_data['in_progress']}\n"
                    f"• Bajarilgan: {monitoring_data['completed']}\n"
                    f"• Bekor qilingan: {monitoring_data['cancelled']}\n\n"
                    f"👨‍🔧 <b>Texniklar:</b> {monitoring_data['active_technicians']}/{monitoring_data['total_technicians']}\n"
                    f"⏰ <b>O'rtacha javob vaqti:</b> {monitoring_data['avg_response_time']}\n"
                    f"📈 <b>Muvaffaqiyat darajasi:</b> {monitoring_data['success_rate']}\n\n"
                    "Quyidagi bo'limlardan birini tanlang:"
                )
            else:
                monitoring_text = (
                    "📊 <b>Мониторинг - Полная информация</b>\n\n"
                    "📈 <b>Общая статистика:</b>\n"
                    f"• Всего заявок: {monitoring_data['total_applications']}\n"
                    f"• Ожидающие: {monitoring_data['pending']}\n"
                    f"• В процессе: {monitoring_data['in_progress']}\n"
                    f"• Завершенные: {monitoring_data['completed']}\n"
                    f"• Отмененные: {monitoring_data['cancelled']}\n\n"
                    f"👨‍🔧 <b>Техники:</b> {monitoring_data['active_technicians']}/{monitoring_data['total_technicians']}\n"
                    f"⏰ <b>Среднее время ответа:</b> {monitoring_data['avg_response_time']}\n"
                    f"📈 <b>Уровень успеха:</b> {monitoring_data['success_rate']}\n\n"
                    "Выберите один из разделов ниже:"
                )
            
            keyboard = get_monitoring_keyboard(lang)
            
            await callback.message.edit_text(monitoring_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in back_to_monitoring: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router