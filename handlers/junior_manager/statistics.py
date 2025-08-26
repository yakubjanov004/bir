"""
Junior Manager Statistics - Mock Data Implementation

Bu modul junior manager uchun statistika funksionalligini o'z ichiga oladi.
Faqat o'z statistikasini ko'rsatadi. Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter
from keyboards.junior_manager_buttons import (
    get_statistics_keyboard,
    get_detailed_statistics_keyboard,
    get_junior_manager_main_menu
)
from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
import logging

logger = logging.getLogger(__name__)

# Mock data storage
mock_users = {
    123456789: {
        'id': 1,
        'telegram_id': 123456789,
        'role': 'junior_manager',
        'language': 'uz',
        'full_name': 'Test Junior Manager',
        'phone_number': '+998901234567',
        'region': 'toshkent'
    }
}

# Mock service requests for statistics calculation
mock_service_requests = {
    'REQ001001': {
        'id': 'REQ001001',
        'workflow_type': 'connection_request',
        'current_status': 'completed',
        'priority': 'high',
        'description': 'Internet ulanish arizasi - yangi uy uchun',
        'location': 'Toshkent shahri, Chilanzor tumani, 15-uy',
        'contact_info': {
            'full_name': 'Alisher Karimov',
            'phone': '+998901234567'
        },
        'created_at': datetime.now() - timedelta(days=2),
        'updated_at': datetime.now() - timedelta(hours=12),
        'assigned_to': 1,
        'assigned_role': 'junior_manager',
        'staff_creator_id': 1,
        'current_assignee_id': 1
    },
    'REQ001002': {
        'id': 'REQ001002',
        'workflow_type': 'technical_service',
        'current_status': 'in_progress',
        'priority': 'medium',
        'description': 'TV signal muammosi - kanallar ko\'rinmayapti',
        'location': 'Toshkent shahri, Sergeli tumani, 25-uy',
        'contact_info': {
            'full_name': 'Dilfuza Rahimova',
            'phone': '+998901234568'
        },
        'created_at': datetime.now() - timedelta(days=5),
        'updated_at': datetime.now() - timedelta(hours=3),
        'assigned_to': 1,
        'assigned_role': 'junior_manager',
        'staff_creator_id': 1,
        'current_assignee_id': 1
    },
    'REQ001003': {
        'id': 'REQ001003',
        'workflow_type': 'technical_service',
        'current_status': 'assigned_to_controller',
        'priority': 'urgent',
        'description': 'Internet tezligi juda past',
        'location': 'Toshkent shahri, Yakkasaroy tumani, 8-uy',
        'contact_info': {
            'full_name': 'Jamshid Toshmatov',
            'phone': '+998901234569'
        },
        'created_at': datetime.now() - timedelta(days=1),
        'updated_at': datetime.now() - timedelta(hours=6),
        'assigned_to': 1,
        'assigned_role': 'junior_manager',
        'staff_creator_id': 1,
        'current_assignee_id': 1
    },
    'REQ001004': {
        'id': 'REQ001004',
        'workflow_type': 'connection_request',
        'current_status': 'created',
        'priority': 'normal',
        'description': 'Yangi uy uchun internet va TV xizmati',
        'location': 'Toshkent shahri, Yunusabad tumani, 42-uy',
        'contact_info': {
            'full_name': 'Malika Yusupova',
            'phone': '+998901234570'
        },
        'created_at': datetime.now() - timedelta(days=8),
        'updated_at': datetime.now() - timedelta(days=8),
        'assigned_to': 1,
        'assigned_role': 'junior_manager',
        'staff_creator_id': 1,
        'current_assignee_id': 1
    },
    'REQ001005': {
        'id': 'REQ001005',
        'workflow_type': 'call_center_direct',
        'current_status': 'completed',
        'priority': 'low',
        'description': 'TV kanal qo\'shish arizasi',
        'location': 'Toshkent shahri, Chorsu tumani, 18-uy',
        'contact_info': {
            'full_name': 'Aziz Karimov',
            'phone': '+998901234571'
        },
        'created_at': datetime.now() - timedelta(days=10),
        'updated_at': datetime.now() - timedelta(days=8),
        'assigned_to': 1,
        'assigned_role': 'junior_manager',
        'staff_creator_id': 1,
        'current_assignee_id': 1
    },
    'REQ001006': {
        'id': 'REQ001006',
        'workflow_type': 'technical_service',
        'current_status': 'cancelled',
        'priority': 'high',
        'description': 'Internet uzilishi muammosi',
        'location': 'Toshkent shahri, Shayxontohur tumani, 33-uy',
        'contact_info': {
            'full_name': 'Rustam Azimov',
            'phone': '+998901234572'
        },
        'created_at': datetime.now() - timedelta(days=15),
        'updated_at': datetime.now() - timedelta(days=14),
        'assigned_to': 1,
        'assigned_role': 'junior_manager',
        'staff_creator_id': 1,
        'current_assignee_id': 1
    }
}

# Mock statistics data
mock_statistics = {
    1: {  # user_id
        'created_applications': 6,
        'transferred_to_controller': 2,
        'completed_applications': 2,
        'cancelled_applications': 1,
        'avg_processing_hours': 24.5,
        'success_rate': 66.7
    }
}

# Mock utility classes
class MockAuditLogger:
    """Mock audit logger"""
    async def log_statistics_view(self, user_id: int, stats_type: str, region: str = None):
        """Mock log statistics view"""
        logger.info(f"Mock: Junior Manager {user_id} viewed {stats_type} statistics")
        if region:
            logger.info(f"Mock: Region: {region}")

# Initialize mock instances
audit_logger = MockAuditLogger()

# Mock functions to replace database calls
async def get_user_by_telegram_id(user_id: int):
    """Mock get user by telegram ID"""
    return mock_users.get(user_id)

async def get_junior_manager_statistics(region: str, user_id: int, start_date: date, end_date: date):
    """Mock get junior manager statistics"""
    try:
        user_stats = mock_statistics.get(user_id, {})
        return {
            'created_applications': user_stats.get('created_applications', 0),
            'transferred_to_controller': user_stats.get('transferred_to_controller', 0),
            'completed_applications': user_stats.get('completed_applications', 0),
            'cancelled_applications': user_stats.get('cancelled_applications', 0)
        }
    except Exception as e:
        logger.error(f"Mock: Error getting junior manager statistics: {e}")
        return {}

async def get_employee_performance(region: str, user_id: int):
    """Mock get employee performance"""
    try:
        user_stats = mock_statistics.get(user_id, {})
        return {
            'avg_processing_hours': user_stats.get('avg_processing_hours', 0),
            'success_rate': user_stats.get('success_rate', 0)
        }
    except Exception as e:
        logger.error(f"Mock: Error getting employee performance: {e}")
        return {}

async def get_daily_statistics(region: str, user_id: int, days: int = 7):
    """Mock get daily statistics"""
    try:
        # Generate mock daily stats
        daily_stats = []
        for i in range(days):
            day = date.today() - timedelta(days=i)
            count = 0
            for req in mock_service_requests.values():
                if req.get('assigned_to') == user_id:
                    created_at = req.get('created_at')
                    if created_at:
                        if isinstance(created_at, str):
                            req_date = datetime.fromisoformat(created_at.replace('Z', '+00:00')).date()
                        else:
                            req_date = created_at.date()
                        
                        if req_date == day:
                            count += 1
            
            daily_stats.append({
                'date': day,
                'count': count
            })
        
        return daily_stats
    except Exception as e:
        logger.error(f"Mock: Error getting daily statistics: {e}")
        return []

async def get_junior_manager_requests(region: str, manager_id: int):
    """Mock get junior manager requests"""
    try:
        requests = [req for req in mock_service_requests.values() 
                   if req.get('assigned_to') == manager_id and 
                   req.get('assigned_role') == 'junior_manager']
        return requests
    except Exception as e:
        logger.error(f"Mock: Error getting junior manager requests: {e}")
        return []

async def get_service_requests_by_assignee(region: str, assignee_id: int):
    """Mock get service requests by assignee"""
    try:
        requests = [req for req in mock_service_requests.values() 
                   if req.get('assigned_to') == assignee_id]
        return requests
    except Exception as e:
        logger.error(f"Mock: Error getting service requests by assignee: {e}")
        return []

async def get_user_lang(user_id: int):
    """Mock get user language"""
    user = await get_user_by_telegram_id(user_id)
    return user.get('language', 'uz') if user else 'uz'

async def format_date(date_obj, lang: str = 'uz'):
    """Mock format date"""
    try:
        if isinstance(date_obj, str):
            return date_obj[:16]
        elif isinstance(date_obj, datetime):
            return date_obj.strftime('%d.%m.%Y %H:%M')
        else:
            return str(date_obj)
    except Exception as e:
        logger.error(f"Mock: Error formatting date: {e}")
        return str(date_obj)

# Create router
router = Router(name="junior_manager_statistics")

# Apply role filter to all handlers
router.message.filter(RoleFilter(role="junior_manager"))
router.callback_query.filter(RoleFilter(role="junior_manager"))


async def calculate_junior_manager_stats(user_id: int, region: str) -> Dict[str, Any]:
    """Calculate comprehensive statistics for junior manager"""
    try:
        # Date ranges
        today = date.today()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Get statistics from mock data
        stats = await get_junior_manager_statistics(region, user_id, month_ago, today)
        
        # Get all applications for detailed analysis
        created_apps = await get_junior_manager_requests(region, user_id)
        assigned_apps = await get_service_requests_by_assignee(region, user_id)
        
        # Combine applications
        all_apps = created_apps + assigned_apps
        seen_ids = set()
        unique_apps = []
        for app in all_apps:
            if app['id'] not in seen_ids:
                seen_ids.add(app['id'])
                unique_apps.append(app)
        
        # Count by status
        status_counts = {
            'pending': 0,
            'in_progress': 0,
            'completed': 0,
            'cancelled': 0,
            'total': len(unique_apps)
        }
        
        # Count by priority
        priority_counts = {
            'low': 0,
            'medium': 0,
            'high': 0,
            'urgent': 0
        }
        
        # Count by type
        type_counts = {}
        
        # Process each application
        total_processing_time = 0
        completed_count = 0
        
        for app in unique_apps:
            # Status counting
            status = app.get('current_status', 'pending')
            if status in ['created', 'assigned_to_junior_manager']:
                status_counts['pending'] += 1
            elif status in ['assigned_to_controller', 'assigned_to_technician', 'in_progress']:
                status_counts['in_progress'] += 1
            elif status in ['completed', 'resolved']:
                status_counts['completed'] += 1
                completed_count += 1
                
                # Calculate processing time for completed apps
                if app.get('created_at') and app.get('updated_at'):
                    created = app['created_at']
                    updated = app['updated_at']
                    if isinstance(created, str):
                        created = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    if isinstance(updated, str):
                        updated = datetime.fromisoformat(updated.replace('Z', '+00:00'))
                    
                    processing_time = (updated - created).total_seconds() / 3600  # hours
                    total_processing_time += processing_time
                    
            elif status == 'cancelled':
                status_counts['cancelled'] += 1
            
            # Priority counting
            priority = app.get('priority', 'medium')
            if priority in priority_counts:
                priority_counts[priority] += 1
            
            # Type counting
            app_type = app.get('workflow_type', 'unknown')
            type_counts[app_type] = type_counts.get(app_type, 0) + 1
        
        # Calculate averages and rates
        avg_processing_time = 0
        if completed_count > 0:
            avg_processing_time = total_processing_time / completed_count
            
        success_rate = 0
        if status_counts['total'] > 0:
            success_rate = (status_counts['completed'] / status_counts['total']) * 100
        
        # Get weekly statistics
        weekly_stats = await get_daily_statistics(region, user_id, 7)
        
        # Get top services
        top_services = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_applications': status_counts['total'],
            'pending_applications': status_counts['pending'],
            'in_progress_applications': status_counts['in_progress'],
            'completed_applications': status_counts['completed'],
            'cancelled_applications': status_counts['cancelled'],
            'created_by_me': stats.get('created_applications', 0),
            'transferred_to_controller': stats.get('transferred_to_controller', 0),
            'avg_processing_hours': round(avg_processing_time, 1),
            'success_rate': round(success_rate, 1),
            'priority_counts': priority_counts,
            'weekly_stats': weekly_stats,
            'top_services': top_services
        }
        
    except Exception as e:
        logger.error(f"Error calculating junior manager stats: {str(e)}")
        return {
            'total_applications': 0,
            'pending_applications': 0,
            'in_progress_applications': 0,
            'completed_applications': 0,
            'cancelled_applications': 0,
            'created_by_me': 0,
            'transferred_to_controller': 0,
            'avg_processing_hours': 0,
            'success_rate': 0,
            'priority_counts': {'low': 0, 'medium': 0, 'high': 0, 'urgent': 0},
            'weekly_stats': [],
            'top_services': []
        }


@router.message(F.text.in_(["📊 Statistika", "📊 Статистика"]))
async def view_statistics(message: Message, state: FSMContext):
    """Junior manager view own statistics handler"""
    user_id = message.from_user.id
    
    try:
        # Get user data
        user = await get_user_by_telegram_id(user_id)
        if not user:
            await message.answer("❌ Foydalanuvchi topilmadi.")
            return
        
        # Verify role
        if user.get('role') != 'junior_manager':
            await message.answer("⛔ Sizda bu bo'limga kirish ruxsati yo'q.")
            return
        
        # Get language and region
        lang = await get_user_lang(user_id) or user.get('language', 'uz')
        region = user.get('region')
        
        if not region:
            await message.answer("❌ Region tanlanmagan!")
            return
        
        # Get junior manager's own statistics
        stats = await calculate_junior_manager_stats(user.get('id'), region)
        
        # Log the action
        await audit_logger.log_statistics_view(user_id, 'overview', region)
        
        # Format statistics text
        if lang == 'uz':
            statistics_text = (
                f"📊 <b>Sizning statistikangiz</b>\n\n"
                f"📈 <b>Asosiy ko'rsatkichlar:</b>\n"
                f"• Jami arizalar: {stats['total_applications']}\n"
                f"• Kutilmoqda: {stats['pending_applications']}\n"
                f"• Jarayonda: {stats['in_progress_applications']}\n"
                f"• Bajarilgan: {stats['completed_applications']}\n"
                f"• Bekor qilingan: {stats['cancelled_applications']}\n\n"
                f"📋 <b>Sizning faoliyatingiz:</b>\n"
                f"• Yaratilgan arizalar: {stats['created_by_me']}\n"
                f"• Controller'ga yuborilgan: {stats['transferred_to_controller']}\n\n"
                f"⏰ <b>O'rtacha ishlov berish:</b> {stats['avg_processing_hours']} soat\n"
                f"📈 <b>Muvaffaqiyat darajasi:</b> {stats['success_rate']}%\n\n"
                "Batafsil statistikani ko'rish uchun tugmani bosing:"
            )
        else:
            statistics_text = (
                f"📊 <b>Ваша статистика</b>\n\n"
                f"📈 <b>Основные показатели:</b>\n"
                f"• Всего заявок: {stats['total_applications']}\n"
                f"• Ожидающие: {stats['pending_applications']}\n"
                f"• В процессе: {stats['in_progress_applications']}\n"
                f"• Завершенные: {stats['completed_applications']}\n"
                f"• Отмененные: {stats['cancelled_applications']}\n\n"
                f"📋 <b>Ваша активность:</b>\n"
                f"• Созданные заявки: {stats['created_by_me']}\n"
                f"• Отправлено контроллеру: {stats['transferred_to_controller']}\n\n"
                f"⏰ <b>Среднее время обработки:</b> {stats['avg_processing_hours']} часов\n"
                f"📈 <b>Уровень успеха:</b> {stats['success_rate']}%\n\n"
                "Нажмите кнопку для просмотра подробной статистики:"
            )
        
        # Save stats to state for detailed view
        await state.update_data(
            statistics=stats,
            language=lang,
            region=region
        )
        
        await message.answer(
            text=statistics_text,
            reply_markup=get_statistics_keyboard(lang),
            parse_mode='HTML'
        )
        
        logger.info(f"Junior Manager {user_id} viewed own statistics")
        
    except Exception as e:
        logger.error(f"Error in view_statistics: {str(e)}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")


@router.callback_query(F.data == "view_detailed_statistics")
async def view_detailed_statistics(callback: CallbackQuery, state: FSMContext):
    """View detailed statistics (only own statistics)"""
    try:
        await callback.answer()
        
        # Get state data
        data = await state.get_data()
        stats = data.get('statistics')
        lang = data.get('language', 'uz')
        
        if not stats:
            # Recalculate if not in state
            user = await get_user_by_telegram_id(callback.from_user.id)
            if user and user.get('region'):
                stats = await calculate_junior_manager_stats(user.get('id'), user.get('region'))
            else:
                await callback.answer("❌ Ma'lumot topilmadi", show_alert=True)
                return
        
        # Log the action
        await audit_logger.log_statistics_view(callback.from_user.id, 'detailed', data.get('region'))
        
        # Format detailed statistics
        if lang == 'uz':
            detailed_stats_text = (
                "📊 <b>Batafsil statistika</b>\n\n"
                "📅 <b>Haftalik ko'rsatkichlar:</b>\n"
            )
            
            # Add weekly stats
            for stat in stats.get('weekly_stats', [])[:7]:
                date_str = stat['date'].strftime('%d.%m')
                detailed_stats_text += f"• {date_str}: {stat['count']} ta ariza\n"
            
            detailed_stats_text += "\n⚡ <b>Muhimlik bo'yicha:</b>\n"
            priority_counts = stats.get('priority_counts', {})
            detailed_stats_text += f"• 🔴 Shoshilinch: {priority_counts.get('urgent', 0)}\n"
            detailed_stats_text += f"• 🟠 Yuqori: {priority_counts.get('high', 0)}\n"
            detailed_stats_text += f"• 🟡 O'rta: {priority_counts.get('medium', 0)}\n"
            detailed_stats_text += f"• 🟢 Past: {priority_counts.get('low', 0)}\n"
            
            detailed_stats_text += "\n🏆 <b>Eng ko'p xizmat turlari:</b>\n"
            
            # Add top services
            service_names = {
                'connection_request': 'Internet ulanish',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Call Center',
                'staff_created': 'Xodim yaratgan',
                'unknown': 'Boshqa'
            }
            
            for i, (service_type, count) in enumerate(stats.get('top_services', []), 1):
                service_name = service_names.get(service_type, service_type)
                detailed_stats_text += f"{i}. {service_name}: {count} ta\n"
            
            detailed_stats_text += (
                f"\n📈 <b>Umumiy tahlil:</b>\n"
                f"• O'rtacha kunlik: {stats.get('total_applications', 0) // 30} ta ariza\n"
                f"• Muvaffaqiyat darajasi: {stats.get('success_rate', 0)}%\n"
                f"• O'rtacha ishlov berish: {stats.get('avg_processing_hours', 0)} soat"
            )
        else:
            detailed_stats_text = (
                "📊 <b>Подробная статистика</b>\n\n"
                "📅 <b>Недельные показатели:</b>\n"
            )
            
            # Add weekly stats
            for stat in stats.get('weekly_stats', [])[:7]:
                date_str = stat['date'].strftime('%d.%m')
                detailed_stats_text += f"• {date_str}: {stat['count']} заявок\n"
            
            detailed_stats_text += "\n⚡ <b>По приоритету:</b>\n"
            priority_counts = stats.get('priority_counts', {})
            detailed_stats_text += f"• 🔴 Срочный: {priority_counts.get('urgent', 0)}\n"
            detailed_stats_text += f"• 🟠 Высокий: {priority_counts.get('high', 0)}\n"
            detailed_stats_text += f"• 🟡 Средний: {priority_counts.get('medium', 0)}\n"
            detailed_stats_text += f"• 🟢 Низкий: {priority_counts.get('low', 0)}\n"
            
            detailed_stats_text += "\n🏆 <b>Топ типов услуг:</b>\n"
            
            # Add top services
            service_names = {
                'connection_request': 'Подключение интернета',
                'technical_service': 'Техническое обслуживание',
                'call_center_direct': 'Call Center',
                'staff_created': 'Создано сотрудником',
                'unknown': 'Другое'
            }
            
            for i, (service_type, count) in enumerate(stats.get('top_services', []), 1):
                service_name = service_names.get(service_type, service_type)
                detailed_stats_text += f"{i}. {service_name}: {count} шт\n"
            
            detailed_stats_text += (
                f"\n📈 <b>Общий анализ:</b>\n"
                f"• Среднее в день: {stats.get('total_applications', 0) // 30} заявок\n"
                f"• Уровень успеха: {stats.get('success_rate', 0)}%\n"
                f"• Среднее время обработки: {stats.get('avg_processing_hours', 0)} часов"
            )
        
        keyboard = get_detailed_statistics_keyboard(lang)
        
        await callback.message.edit_text(
            detailed_stats_text, 
            reply_markup=keyboard, 
            parse_mode='HTML'
        )
        
        logger.info(f"Junior Manager {callback.from_user.id} viewed detailed statistics")
        
    except Exception as e:
        logger.error(f"Error in view_detailed_statistics: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data == "back_to_statistics")
async def back_to_statistics(callback: CallbackQuery, state: FSMContext):
    """Back to statistics menu"""
    try:
        await callback.answer()
        
        # Get state data
        data = await state.get_data()
        stats = data.get('statistics')
        lang = data.get('language', 'uz')
        
        if not stats:
            # Recalculate if not in state
            user = await get_user_by_telegram_id(callback.from_user.id)
            if user and user.get('region'):
                stats = await calculate_junior_manager_stats(user.get('id'), user.get('region'))
                lang = await get_user_lang(callback.from_user.id) or 'uz'
            else:
                await callback.answer("❌ Ma'lumot topilmadi", show_alert=True)
                return
        
        # Format statistics text
        if lang == 'uz':
            statistics_text = (
                f"📊 <b>Sizning statistikangiz</b>\n\n"
                f"📈 <b>Asosiy ko'rsatkichlar:</b>\n"
                f"• Jami arizalar: {stats['total_applications']}\n"
                f"• Kutilmoqda: {stats['pending_applications']}\n"
                f"• Jarayonda: {stats['in_progress_applications']}\n"
                f"• Bajarilgan: {stats['completed_applications']}\n"
                f"• Bekor qilingan: {stats['cancelled_applications']}\n\n"
                f"📋 <b>Sizning faoliyatingiz:</b>\n"
                f"• Yaratilgan arizalar: {stats['created_by_me']}\n"
                f"• Controller'ga yuborilgan: {stats['transferred_to_controller']}\n\n"
                f"⏰ <b>O'rtacha ishlov berish:</b> {stats['avg_processing_hours']} soat\n"
                f"📈 <b>Muvaffaqiyat darajasi:</b> {stats['success_rate']}%\n\n"
                "Batafsil statistikani ko'rish uchun tugmani bosing:"
            )
        else:
            statistics_text = (
                f"📊 <b>Ваша статистика</b>\n\n"
                f"📈 <b>Основные показатели:</b>\n"
                f"• Всего заявок: {stats['total_applications']}\n"
                f"• Ожидающие: {stats['pending_applications']}\n"
                f"• В процессе: {stats['in_progress_applications']}\n"
                f"• Завершенные: {stats['completed_applications']}\n"
                f"• Отмененные: {stats['cancelled_applications']}\n\n"
                f"📋 <b>Ваша активность:</b>\n"
                f"• Созданные заявки: {stats['created_by_me']}\n"
                f"• Отправлено контроллеру: {stats['transferred_to_controller']}\n\n"
                f"⏰ <b>Среднее время обработки:</b> {stats['avg_processing_hours']} часов\n"
                f"📈 <b>Уровень успеха:</b> {stats['success_rate']}%\n\n"
                "Нажмите кнопку для просмотра подробной статистики:"
            )
        
        await callback.message.edit_text(
            text=statistics_text,
            reply_markup=get_statistics_keyboard(lang),
            parse_mode='HTML'
        )
        
    except Exception as e:
        logger.error(f"Error in back_to_statistics: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data == "jm_close_menu")
async def close_statistics(callback: CallbackQuery, state: FSMContext):
    """Close statistics and return to main menu"""
    try:
        await callback.answer()
        
        lang = await get_user_lang(callback.from_user.id) or 'uz'
        
        await callback.message.edit_text(
            "📊 Statistika yopildi" if lang == 'uz' else "📊 Статистика закрыта"
        )
        
        await callback.message.answer(
            "Asosiy menyu" if lang == 'uz' else "Главное меню",
            reply_markup=get_junior_manager_main_menu(lang)
        )
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error in close_statistics: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
