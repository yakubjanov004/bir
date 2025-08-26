"""
Manager Staff Activity Handler - Mock Data Version

Bu modul manager uchun xodimlar faoliyatini kuzatish funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, database kerak emas.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime, date, timedelta
import logging
import json
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Mock data for staff members
MOCK_STAFF = [
    {
        'id': 1,
        'full_name': 'Aziz Karimov',
        'role': 'junior_manager',
        'status': 'online',
        'region': 'toshkent',
        'last_seen': datetime.now() - timedelta(minutes=5),
        'total_tasks': 45,
        'completed_tasks': 38,
        'in_progress': 7,
        'cancelled': 0,
        'success_rate': 84.4,
        'avg_completion_hours': 2.3,
        'completed_today': 3,
        'workload': 'medium'
    },
    {
        'id': 2,
        'full_name': 'Malika Yusupova',
        'role': 'junior_manager',
        'status': 'online',
        'region': 'toshkent',
        'last_seen': datetime.now() - timedelta(minutes=2),
        'total_tasks': 52,
        'completed_tasks': 47,
        'in_progress': 5,
        'cancelled': 0,
        'success_rate': 90.4,
        'avg_completion_hours': 1.8,
        'completed_today': 4,
        'workload': 'high'
    },
    {
        'id': 3,
        'full_name': 'Jasur Toshmatov',
        'role': 'technician',
        'status': 'busy',
        'region': 'toshkent',
        'last_seen': datetime.now() - timedelta(minutes=1),
        'total_tasks': 38,
        'completed_tasks': 35,
        'in_progress': 3,
        'cancelled': 0,
        'success_rate': 92.1,
        'avg_completion_hours': 1.5,
        'completed_today': 2,
        'workload': 'medium'
    },
    {
        'id': 4,
        'full_name': 'Dilfuza Rahimova',
        'role': 'technician',
        'status': 'online',
        'region': 'toshkent',
        'last_seen': datetime.now() - timedelta(minutes=3),
        'total_tasks': 41,
        'completed_tasks': 36,
        'in_progress': 5,
        'cancelled': 0,
        'success_rate': 87.8,
        'avg_completion_hours': 2.1,
        'completed_today': 3,
        'workload': 'low'
    },
    {
        'id': 5,
        'full_name': 'Rustam Alimov',
        'role': 'junior_manager',
        'status': 'offline',
        'region': 'toshkent',
        'last_seen': datetime.now() - timedelta(hours=2),
        'total_tasks': 28,
        'completed_tasks': 25,
        'in_progress': 3,
        'cancelled': 0,
        'success_rate': 89.3,
        'avg_completion_hours': 2.8,
        'completed_today': 1,
        'workload': 'low'
    }
]

# Mock data for staff performance history
MOCK_PERFORMANCE_HISTORY = {
    1: [  # Aziz Karimov
        {'date': '2024-01-15', 'completed': 3, 'total': 3, 'hours_worked': 8.5},
        {'date': '2024-01-14', 'completed': 4, 'total': 4, 'hours_worked': 9.0},
        {'date': '2024-01-13', 'completed': 2, 'total': 3, 'hours_worked': 7.5},
        {'date': '2024-01-12', 'completed': 5, 'total': 5, 'hours_worked': 8.0},
        {'date': '2024-01-11', 'completed': 3, 'total': 4, 'hours_worked': 8.5}
    ],
    2: [  # Malika Yusupova
        {'date': '2024-01-15', 'completed': 4, 'total': 4, 'hours_worked': 9.0},
        {'date': '2024-01-14', 'completed': 5, 'total': 5, 'hours_worked': 9.5},
        {'date': '2024-01-13', 'completed': 3, 'total': 3, 'hours_worked': 8.0},
        {'date': '2024-01-12', 'completed': 4, 'total': 4, 'hours_worked': 8.5},
        {'date': '2024-01-11', 'completed': 6, 'total': 6, 'hours_worked': 9.0}
    ],
    3: [  # Jasur Toshmatov
        {'date': '2024-01-15', 'completed': 2, 'total': 2, 'hours_worked': 8.0},
        {'date': '2024-01-14', 'completed': 3, 'total': 3, 'hours_worked': 8.5},
        {'date': '2024-01-13', 'completed': 4, 'total': 4, 'hours_worked': 9.0},
        {'date': '2024-01-12', 'completed': 2, 'total': 2, 'hours_worked': 7.5},
        {'date': '2024-01-11', 'completed': 3, 'total': 3, 'hours_worked': 8.0}
    ]
}

def get_staff_performance_mock(staff_id: int, period_days: int = 7) -> Dict[str, Any]:
    """Get staff performance from mock data"""
    try:
        staff = next((s for s in MOCK_STAFF if s['id'] == staff_id), None)
        if not staff:
            return {}
        
        # Get performance history
        history = MOCK_PERFORMANCE_HISTORY.get(staff_id, [])
        
        # Calculate period metrics
        period_history = history[:period_days] if len(history) >= period_days else history
        
        total_completed = sum(day['completed'] for day in period_history)
        total_hours = sum(day['hours_worked'] for day in period_history)
        avg_daily_completed = round(total_completed / len(period_history), 1) if period_history else 0
        avg_daily_hours = round(total_hours / len(period_history), 1) if period_history else 0
        
        return {
            'staff_info': staff,
            'period_metrics': {
                'total_completed': total_completed,
                'total_hours': total_hours,
                'avg_daily_completed': avg_daily_completed,
                'avg_daily_hours': avg_daily_hours,
                'period_days': len(period_history)
            },
            'daily_history': period_history
        }
        
    except Exception as e:
        logger.error(f"Error getting mock staff performance: {e}")
        return {}

def get_online_staff_mock(region: str = 'toshkent') -> List[Dict[str, Any]]:
    """Get online staff from mock data"""
    try:
        online_staff = [s for s in MOCK_STAFF if s['status'] == 'online' and s['region'] == region]
        return online_staff
    except Exception as e:
        logger.error(f"Error getting mock online staff: {e}")
        return []

def get_staff_workload_mock(region: str = 'toshkent') -> Dict[str, Any]:
    """Get staff workload from mock data"""
    try:
        staff_in_region = [s for s in MOCK_STAFF if s['region'] == region]
        
        workload_stats = {
            'low': len([s for s in staff_in_region if s['workload'] == 'low']),
            'medium': len([s for s in staff_in_region if s['workload'] == 'medium']),
            'high': len([s for s in staff_in_region if s['workload'] == 'high']),
            'total': len(staff_in_region)
        }
        
        return workload_stats
    except Exception as e:
        logger.error(f"Error getting mock staff workload: {e}")
        return {'low': 0, 'medium': 0, 'high': 0, 'total': 0}

def get_manager_staff_activity_router():
    """Router for staff activity monitoring with mock data"""
    router = Router()
    
    @router.message(F.text.in_(["👥 Xodimlar faoliyati", "👥 Активность сотрудников"]))
    async def show_staff_activity_menu(message: Message, state: FSMContext):
        """Show staff activity monitoring menu"""
        try:
            # Mock user info
            mock_user = {
                'id': message.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Get staff data
            online_staff = get_online_staff_mock('toshkent')
            workload_stats = get_staff_workload_mock('toshkent')
            
            if lang == 'uz':
                text = f"""👥 <b>Xodimlar faoliyati</b>

📊 <b>Joriy holat:</b>
• Online xodimlar: {len(online_staff)}
• Jami xodimlar: {workload_stats['total']}

📈 <b>Ish yuki:</b>
• Past: {workload_stats['low']}
• O'rtacha: {workload_stats['medium']}
• Yuqori: {workload_stats['high']}

Quyidagi bo'limlardan birini tanlang:"""
            else:
                text = f"""👥 <b>Активность сотрудников</b>

📊 <b>Текущее состояние:</b>
• Онлайн сотрудники: {len(online_staff)}
• Всего сотрудников: {workload_stats['total']}

📈 <b>Рабочая нагрузка:</b>
• Низкая: {workload_stats['low']}
• Средняя: {workload_stats['medium']}
• Высокая: {workload_stats['high']}

Выберите один из следующих разделов:"""
            
            # Create staff activity keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="🟢 Online xodimlar" if lang == 'uz' else "🟢 Онлайн сотрудники",
                    callback_data="mgr_staff_online"
                )],
                [InlineKeyboardButton(
                    text="📊 Ish natijalari" if lang == 'uz' else "📊 Результаты работы",
                    callback_data="mgr_staff_performance"
                )],
                [InlineKeyboardButton(
                    text="📈 Ish yuki" if lang == 'uz' else "📈 Рабочая нагрузка",
                    callback_data="mgr_staff_workload"
                )],
                [InlineKeyboardButton(
                    text="👨‍💼 Kichik menejerlar" if lang == 'uz' else "👨‍💼 Младшие менеджеры",
                    callback_data="mgr_junior_managers"
                )],
                [InlineKeyboardButton(
                    text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                    callback_data="mgr_back_to_main"
                )]
            ])
            
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error showing staff activity menu: {e}")
            await message.answer("❌ Xatolik yuz berdi")
    
    @router.callback_query(F.data == "mgr_staff_online")
    async def show_online_staff(callback: CallbackQuery, state: FSMContext):
        """Show online staff"""
        try:
            await callback.answer()
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Get online staff
            online_staff = get_online_staff_mock('toshkent')
            
            if not online_staff:
                if lang == 'uz':
                    text = "📭 Online xodimlar topilmadi"
                else:
                    text = "📭 Онлайн сотрудники не найдены"
                
                await callback.message.edit_text(text)
                return
            
            # Show first online staff
            await state.update_data(
                online_staff=online_staff,
                current_index=0
            )
            
            await display_online_staff(callback.message, online_staff[0], 0, len(online_staff), lang)
            
        except Exception as e:
            logger.error(f"Error showing online staff: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_staff_performance")
    async def show_staff_performance(callback: CallbackQuery, state: FSMContext):
        """Show staff performance"""
        try:
            await callback.answer()
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Get all staff for performance view
            all_staff = [s for s in MOCK_STAFF if s['region'] == 'toshkent']
            
            if not all_staff:
                if lang == 'uz':
                    text = "📭 Xodimlar topilmadi"
                else:
                    text = "📭 Сотрудники не найдены"
                
                await callback.message.edit_text(text)
                return
            
            # Show first staff performance
            await state.update_data(
                all_staff=all_staff,
                current_index=0
            )
            
            await display_staff_performance(callback.message, all_staff[0], 0, len(all_staff), lang)
            
        except Exception as e:
            logger.error(f"Error showing staff performance: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_staff_workload")
    async def show_staff_workload(callback: CallbackQuery, state: FSMContext):
        """Show staff workload"""
        try:
            await callback.answer()
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Get workload stats
            workload_stats = get_staff_workload_mock('toshkent')
            
            if lang == 'uz':
                text = f"""📈 <b>Xodimlar ish yuki</b>

📊 <b>Joriy holat:</b>
• Jami xodimlar: {workload_stats['total']}

📈 <b>Ish yuki taqsimoti:</b>
• 🟢 Past: {workload_stats['low']} xodim
• 🟡 O'rtacha: {workload_stats['medium']} xodim
• 🔴 Yuqori: {workload_stats['high']} xodim

📊 <b>Foizlar:</b>
• Past: {round(workload_stats['low'] / workload_stats['total'] * 100, 1)}%
• O'rtacha: {round(workload_stats['medium'] / workload_stats['total'] * 100, 1)}%
• Yuqori: {round(workload_stats['high'] / workload_stats['total'] * 100, 1)}%"""
            else:
                text = f"""📈 <b>Рабочая нагрузка сотрудников</b>

📊 <b>Текущее состояние:</b>
• Всего сотрудников: {workload_stats['total']}

📈 <b>Распределение нагрузки:</b>
• 🟢 Низкая: {workload_stats['low']} сотрудников
• 🟡 Средняя: {workload_stats['medium']} сотрудников
• 🔴 Высокая: {workload_stats['high']} сотрудников

📊 <b>Проценты:</b>
• Низкая: {round(workload_stats['low'] / workload_stats['total'] * 100, 1)}%
• Средняя: {round(workload_stats['medium'] / workload_stats['total'] * 100, 1)}%
• Высокая: {round(workload_stats['high'] / workload_stats['total'] * 100, 1)}%"""
            
            # Create back keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                    callback_data="mgr_staff_activity"
                )
            ]])
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error showing staff workload: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_junior_managers")
    async def show_junior_managers(callback: CallbackQuery, state: FSMContext):
        """Show junior managers"""
        try:
            await callback.answer()
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Get junior managers
            junior_managers = [s for s in MOCK_STAFF if s['role'] == 'junior_manager' and s['region'] == 'toshkent']
            
            if not junior_managers:
                if lang == 'uz':
                    text = "👨‍💼 Kichik menejerlar topilmadi"
                else:
                    text = "👨‍💼 Младшие менеджеры не найдены"
                
                await callback.message.edit_text(text)
                return
            
            # Show first junior manager
            await state.update_data(
                junior_managers=junior_managers,
                current_index=0
            )
            
            await display_junior_manager(callback.message, junior_managers[0], 0, len(junior_managers), lang)
            
        except Exception as e:
            logger.error(f"Error showing junior managers: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_staff_activity")
    async def back_to_staff_activity(callback: CallbackQuery, state: FSMContext):
        """Go back to staff activity menu"""
        try:
            await callback.answer()
            
            # Clear state
            await state.clear()
            
            # Show staff activity menu again
            await show_staff_activity_menu(callback.message, state)
            
        except Exception as e:
            logger.error(f"Error going back to staff activity: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_back_to_main")
    async def back_to_main(callback: CallbackQuery, state: FSMContext):
        """Go back to main menu"""
        try:
            await callback.answer()
            
            # Clear state
            await state.clear()
            
            # Import and show main keyboard
            from keyboards.manager_buttons import get_manager_main_keyboard
            keyboard = get_manager_main_keyboard('uz')  # Default to Uzbek
            
            text = "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:"
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error going back to main: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    return router

async def display_online_staff(message: Message, staff: dict, current_index: int, total_count: int, lang: str):
    """Display online staff details"""
    try:
        # Status emoji
        status_emoji = {
            'online': '🟢',
            'busy': '🟡',
            'offline': '⚫'
        }.get(staff['status'], '⚪')
        
        # Role emoji
        role_emoji = {
            'junior_manager': '👨‍💼',
            'technician': '🔧',
            'controller': '🎛️'
        }.get(staff['role'], '👤')
        
        # Workload emoji
        workload_emoji = {
            'low': '🟢',
            'medium': '🟡',
            'high': '🔴'
        }.get(staff['workload'], '⚪')
        
        # Format text
        if lang == 'uz':
            text = f"""👤 <b>Xodim ma'lumotlari {current_index + 1}/{total_count}</b>

{status_emoji} <b>Status:</b> {staff['status']}
{role_emoji} <b>Lavozim:</b> {staff['role']}
{workload_emoji} <b>Ish yuki:</b> {staff['workload']}

🆔 <b>ID:</b> {staff['id']}
👤 <b>Nomi:</b> {staff['full_name']}
📍 <b>Hudud:</b> {staff['region']}
⏰ <b>Oxirgi ko'rinish:</b> {staff['last_seen'].strftime('%H:%M')}

📊 <b>Ish natijalari (7 kun):</b>
• Jami vazifalar: {staff['total_tasks']}
• Bajarilgan: {staff['completed_tasks']}
• Jarayonda: {staff['in_progress']}
• Muvaffaqiyat: {staff['success_rate']}%
• O'rtacha vaqt: {staff['avg_completion_hours']} soat
• Bugun bajarilgan: {staff['completed_today']}"""
        else:
            text = f"""👤 <b>Информация о сотруднике {current_index + 1}/{total_count}</b>

{status_emoji} <b>Статус:</b> {staff['status']}
{role_emoji} <b>Должность:</b> {staff['role']}
{workload_emoji} <b>Нагрузка:</b> {staff['workload']}

🆔 <b>ID:</b> {staff['id']}
👤 <b>Имя:</b> {staff['full_name']}
📍 <b>Регион:</b> {staff['region']}
⏰ <b>Последний раз:</b> {staff['last_seen'].strftime('%H:%M')}

📊 <b>Результаты работы (7 дней):</b>
• Всего задач: {staff['total_tasks']}
• Выполнено: {staff['completed_tasks']}
• В процессе: {staff['in_progress']}
• Успешность: {staff['success_rate']}%
• Среднее время: {staff['avg_completion_hours']} часов
• Выполнено сегодня: {staff['completed_today']}"""
        
        # Create navigation keyboard
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущий",
                    callback_data="mgr_staff_prev"
                ),
                InlineKeyboardButton(
                    text="Keyingi ➡️" if lang == 'uz' else "Следующий ➡️",
                    callback_data="mgr_staff_next"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                    callback_data="mgr_staff_activity"
                )
            ]
        ])
        
        await message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Error displaying online staff: {e}")
        await message.answer("❌ Xatolik yuz berdi")

async def display_staff_performance(message: Message, staff: dict, current_index: int, total_count: int, lang: str):
    """Display staff performance details"""
    try:
        # Get performance data
        performance = get_staff_performance_mock(staff['id'])
        
        # Status emoji
        status_emoji = {
            'online': '🟢',
            'busy': '🟡',
            'offline': '⚫'
        }.get(staff['status'], '⚪')
        
        # Role emoji
        role_emoji = {
            'junior_manager': '👨‍💼',
            'technician': '🔧',
            'controller': '🎛️'
        }.get(staff['role'], '👤')
        
        # Format text
        if lang == 'uz':
            text = f"""📊 <b>Xodim ish natijalari {current_index + 1}/{total_count}</b>

{status_emoji} <b>Status:</b> {staff['status']}
{role_emoji} <b>Lavozim:</b> {staff['role']}

👤 <b>Nomi:</b> {staff['full_name']}
📍 <b>Hudud:</b> {staff['region']}

📈 <b>Umumiy natijalar (7 kun):</b>
• Jami vazifalar: {staff['total_tasks']}
• Bajarilgan: {staff['completed_tasks']}
• Jarayonda: {staff['in_progress']}
• Muvaffaqiyat: {staff['success_rate']}%
• O'rtacha vaqt: {staff['avg_completion_hours']} soat
• Bugun bajarilgan: {staff['completed_today']}

📅 <b>Kunlik natijalar:</b>
• O'rtacha kunlik: {performance.get('period_metrics', {}).get('avg_daily_completed', 0)} vazifa
• O'rtacha kunlik soat: {performance.get('period_metrics', {}).get('avg_daily_hours', 0)} soat"""
        else:
            text = f"""📊 <b>Результаты работы сотрудника {current_index + 1}/{total_count}</b>

{status_emoji} <b>Статус:</b> {staff['status']}
{role_emoji} <b>Должность:</b> {staff['role']}

👤 <b>Имя:</b> {staff['full_name']}
📍 <b>Регион:</b> {staff['region']}

📈 <b>Общие результаты (7 дней):</b>
• Всего задач: {staff['total_tasks']}
• Выполнено: {staff['completed_tasks']}
• В процессе: {staff['in_progress']}
• Успешность: {staff['success_rate']}%
• Среднее время: {staff['avg_completion_hours']} часов
• Выполнено сегодня: {staff['completed_today']}

📅 <b>Ежедневные результаты:</b>
• Среднее за день: {performance.get('period_metrics', {}).get('avg_daily_completed', 0)} задач
• Среднее за день часов: {performance.get('period_metrics', {}).get('avg_daily_hours', 0)} часов"""
        
        # Create navigation keyboard
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущий",
                    callback_data="mgr_perf_prev"
                ),
                InlineKeyboardButton(
                    text="Keyingi ➡️" if lang == 'uz' else "Следующий ➡️",
                    callback_data="mgr_perf_next"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                    callback_data="mgr_staff_activity"
                )
            ]
        ])
        
        await message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Error displaying staff performance: {e}")
        await message.answer("❌ Xatolik yuz berdi")

async def display_junior_manager(message: Message, staff: dict, current_index: int, total_count: int, lang: str):
    """Display junior manager details"""
    try:
        # Status emoji
        status_emoji = {
            'online': '🟢',
            'busy': '🟡',
            'offline': '⚫'
        }.get(staff['status'], '⚪')
        
        # Workload emoji
        workload_emoji = {
            'low': '🟢',
            'medium': '🟡',
            'high': '🔴'
        }.get(staff['workload'], '⚪')
        
        # Format text
        if lang == 'uz':
            text = f"""👨‍💼 <b>Kichik menejer ma'lumotlari {current_index + 1}/{total_count}</b>

{status_emoji} <b>Status:</b> {staff['status']}
{workload_emoji} <b>Ish yuki:</b> {staff['workload']}

👤 <b>Nomi:</b> {staff['full_name']}
📍 <b>Hudud:</b> {staff['region']}
⏰ <b>Oxirgi ko'rinish:</b> {staff['last_seen'].strftime('%H:%M')}

📊 <b>Ish natijalari (7 kun):</b>
• Jami vazifalar: {staff['total_tasks']}
• Bajarilgan: {staff['completed_tasks']}
• Jarayonda: {staff['in_progress']}
• Muvaffaqiyat: {staff['success_rate']}%
• O'rtacha vaqt: {staff['avg_completion_hours']} soat
• Bugun bajarilgan: {staff['completed_today']}

💼 <b>Menejer sifatida:</b>
• Kichik menejer lavozimida ishlaydi
• Arizalarni boshqaradi va texniklarga yuboradi
• Mijozlar bilan bog'lanishda yordam beradi"""
        else:
            text = f"""👨‍💼 <b>Информация о младшем менеджере {current_index + 1}/{total_count}</b>

{status_emoji} <b>Статус:</b> {staff['status']}
{workload_emoji} <b>Нагрузка:</b> {staff['workload']}

👤 <b>Имя:</b> {staff['full_name']}
📍 <b>Регион:</b> {staff['region']}
⏰ <b>Последний раз:</b> {staff['last_seen'].strftime('%H:%M')}

📊 <b>Результаты работы (7 дней):</b>
• Всего задач: {staff['total_tasks']}
• Выполнено: {staff['completed_tasks']}
• В процессе: {staff['in_progress']}
• Успешность: {staff['success_rate']}%
• Среднее время: {staff['avg_completion_hours']} часов
• Выполнено сегодня: {staff['completed_today']}

💼 <b>Как менеджер:</b>
• Работает в должности младшего менеджера
• Управляет заявками и направляет техникам
• Помогает в общении с клиентами"""
        
        # Create navigation keyboard
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущий",
                    callback_data="mgr_jm_prev"
                ),
                InlineKeyboardButton(
                    text="Keyingi ➡️" if lang == 'uz' else "Следующий ➡️",
                    callback_data="mgr_jm_next"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                    callback_data="mgr_staff_activity"
                )
            ]
        ])
        
        await message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Error displaying junior manager: {e}")
        await message.answer("❌ Xatolik yuz berdi")
