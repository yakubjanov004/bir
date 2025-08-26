"""
Controller Technicians Activity - Mock Data Implementation

Shows technicians' activity for controller role with filters and per-technician detailed view.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter
from datetime import datetime, timedelta
from typing import List, Dict, Any
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

# Mock technicians data
mock_technicians = [
    {
        'id': 1,
        'full_name': 'Ahmad Karimov',
        'phone': '+998901234567',
        'region': 'toshkent',
        'is_active': True,
        'specialization': 'Internet',
        'rating': 4.8,
        'experience_years': 3
    },
    {
        'id': 2,
        'full_name': 'Malika Toshmatova',
        'phone': '+998901234568',
        'region': 'toshkent',
        'is_active': True,
        'specialization': 'TV',
        'rating': 4.6,
        'experience_years': 2
    },
    {
        'id': 3,
        'full_name': 'Jasur Rahimov',
        'phone': '+998901234569',
        'region': 'toshkent',
        'is_active': True,
        'specialization': 'Combo',
        'rating': 4.9,
        'experience_years': 4
    },
    {
        'id': 4,
        'full_name': 'Dilfuza Abdullayeva',
        'phone': '+998901234570',
        'region': 'toshkent',
        'is_active': True,
        'specialization': 'Internet',
        'rating': 4.7,
        'experience_years': 2
    },
    {
        'id': 5,
        'full_name': 'Rustam Azimov',
        'phone': '+998901234571',
        'region': 'toshkent',
        'is_active': False,
        'specialization': 'TV',
        'rating': 4.5,
        'experience_years': 1
    }
]

# Mock technician workload data
mock_technician_workload = {
    1: {
        'assigned_count': 3,
        'in_progress_count': 2,
        'completed_today': 5,
        'avg_completion_hours': 2.5,
        'total_orders': 45,
        'success_rate': 95
    },
    2: {
        'assigned_count': 1,
        'in_progress_count': 1,
        'completed_today': 3,
        'avg_completion_hours': 3.2,
        'total_orders': 32,
        'success_rate': 88
    },
    3: {
        'assigned_count': 4,
        'in_progress_count': 3,
        'completed_today': 7,
        'avg_completion_hours': 2.1,
        'total_orders': 67,
        'success_rate': 97
    },
    4: {
        'assigned_count': 0,
        'in_progress_count': 0,
        'completed_today': 2,
        'avg_completion_hours': 2.8,
        'total_orders': 28,
        'success_rate': 92
    },
    5: {
        'assigned_count': 0,
        'in_progress_count': 0,
        'completed_today': 0,
        'avg_completion_hours': 0,
        'total_orders': 0,
        'success_rate': 0
    }
}

# Mock functions
async def get_user_by_telegram_id(region: str, telegram_id: int):
    """Mock get user by telegram ID"""
    return mock_users.get(telegram_id, {
        'id': 999,
        'telegram_id': telegram_id,
        'role': 'controller',
        'region': region,
        'full_name': 'Unknown User'
    })

async def get_available_technicians(region: str):
    """Mock get available technicians"""
    return [tech for tech in mock_technicians if tech['region'] == region and tech['is_active']]

async def get_technician_workload(region: str):
    """Mock get technician workload"""
    techs = []
    for tech in mock_technicians:
        if tech['region'] == region:
            workload = mock_technician_workload.get(tech['id'], {})
            techs.append({
                'id': tech['id'],
                'full_name': tech['full_name'],
                'phone': tech['phone'],
                'assigned_count': workload.get('assigned_count', 0),
                'in_progress_count': workload.get('in_progress_count', 0),
                'completed_today': workload.get('completed_today', 0),
                'avg_completion_hours': workload.get('avg_completion_hours', 0),
                'total_orders': workload.get('total_orders', 0),
                'success_rate': workload.get('success_rate', 0)
            })
    return techs

async def get_technician_performance(region: str, technician_id: int):
    """Mock get technician performance"""
    tech = next((t for t in mock_technicians if t['id'] == technician_id), None)
    if not tech:
        return {}
    
    workload = mock_technician_workload.get(technician_id, {})
    return {
        'technician_name': tech['full_name'],
        'phone': tech['phone'],
        'active_orders': workload.get('assigned_count', 0) + workload.get('in_progress_count', 0),
        'completed_today': workload.get('completed_today', 0),
        'avg_completion_hours': workload.get('avg_completion_hours', 0),
        'total_orders': workload.get('total_orders', 0),
        'success_rate': workload.get('success_rate', 0),
        'specialization': tech['specialization'],
        'rating': tech['rating'],
        'experience_years': tech['experience_years']
    }

# Mock audit logger
class MockAuditLogger:
    """Mock audit logger"""
    async def log_action(self, user_id: int, action: str, details: dict = None, region: str = None):
        """Mock log action"""
        logger.info(f"Mock audit log: User {user_id} performed {action}")
        if details:
            logger.info(f"Mock: Details: {details}")
        if region:
            logger.info(f"Mock: Region: {region}")

audit_logger = MockAuditLogger()

# Mock user region function
async def get_user_region(user_id: int):
    """Mock get user region"""
    user = mock_users.get(user_id, {})
    return user.get('region', 'toshkent')

def get_controller_technicians_router():
    router = Router()

    role_filter = RoleFilter('controller')
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    # Helpers
    def _filter_techs(techs: List[Dict[str, Any]], flt: str) -> List[Dict[str, Any]]:
        if flt == 'all':
            return techs
        if flt == 'online':
            # Filter by active orders (technicians with active work are considered online)
            return [t for t in techs if (t.get('assigned_count', 0) > 0 or t.get('in_progress_count', 0) > 0)]
        if flt == 'busy':
            return [t for t in techs if (t.get('assigned_count', 0) + t.get('in_progress_count', 0)) > 0]
        return techs

    def _tech_detail_keyboard(flt: str, index: int, total: int) -> InlineKeyboardMarkup:
        rows = []
        nav = []
        if index > 0:
            nav.append(InlineKeyboardButton(text='⬅️ Oldingi', callback_data=f'ctrl_tech_nav_prev_{flt}_{index-1}'))
        nav.append(InlineKeyboardButton(text=f"{index+1}/{total}", callback_data='noop'))
        if index < total - 1:
            nav.append(InlineKeyboardButton(text='Keyingi ➡️', callback_data=f'ctrl_tech_nav_next_{flt}_{index+1}'))
        if nav:
            rows.append(nav)
        rows.append([
            InlineKeyboardButton(text='📋 Hammasi', callback_data='ctrl_tech_filter_all'),
            InlineKeyboardButton(text='🟢 Faol', callback_data='ctrl_tech_filter_online'),
            InlineKeyboardButton(text='📋 Band', callback_data='ctrl_tech_filter_busy'),
        ])
        rows.append([
            InlineKeyboardButton(text='🔄 Yangilash', callback_data=f'ctrl_tech_refresh_detail_{flt}_{index}'),
            InlineKeyboardButton(text='⬅️ Orqaga', callback_data='controllers_back'),
        ])
        return InlineKeyboardMarkup(inline_keyboard=rows)

    async def _render_tech_detail(message_or_callback, region: str, flt: str = 'all', index: int = 0):
        try:
            # Get technicians workload from mock data
            techs = await get_technician_workload(region)
            
            if not techs:
                # If no workload data, get available technicians
                available_techs = await get_available_technicians(region)
                techs = []
                for tech in available_techs:
                    # Get performance data for each technician
                    perf = await get_technician_performance(region, tech['id'])
                    techs.append({
                        'id': tech['id'],
                        'full_name': tech.get('full_name', 'Noma\'lum'),
                        'phone': tech.get('phone', 'N/A'),
                        'assigned_count': perf.get('active_orders', 0),
                        'in_progress_count': 0,
                        'completed_today': perf.get('completed_today', 0),
                        'avg_completion_hours': perf.get('avg_completion_hours', 0)
                    })
            
            filtered = _filter_techs(techs, flt)
            total = len(filtered)
            
            if total == 0:
                text = "👥 <b>Texniklar faoliyati</b>\n\nHozircha ma'lumot yo'q"
                kb = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='📋 Hammasi', callback_data='ctrl_tech_filter_all'),
                     InlineKeyboardButton(text='🟢 Faol', callback_data='ctrl_tech_filter_online'),
                     InlineKeyboardButton(text='📋 Band', callback_data='ctrl_tech_filter_busy')],
                    [InlineKeyboardButton(text='⬅️ Orqaga', callback_data='controllers_back')]
                ])
                if isinstance(message_or_callback, Message):
                    await message_or_callback.answer(text, reply_markup=kb, parse_mode='HTML')
                else:
                    await message_or_callback.message.edit_text(text, reply_markup=kb, parse_mode='HTML')
                return
            
            index = max(0, min(index, total - 1))
            t = filtered[index]
            
            # Get detailed performance for selected technician
            perf = await get_technician_performance(region, t['id'])
            
            # Determine status
            total_active = t.get('assigned_count', 0) + t.get('in_progress_count', 0)
            if total_active == 0:
                emoji_status = '🟡 Bo\'sh'
            elif total_active <= 2:
                emoji_status = '🟢 Faol'
            else:
                emoji_status = '🔴 Band'
            
            # Calculate success rate (if completed_today > 0)
            completed = t.get('completed_today', 0)
            success_rate = 100 if completed > 0 else 0  # Simplified for now
            
            text = (
                "👥 <b>Texniklar faoliyati</b>\n\n"
                f"👨‍🔧 <b>F.I.O.:</b> {t.get('full_name', perf.get('technician_name', 'Noma\'lum'))}\n"
                f"📞 <b>Telefon:</b> {t.get('phone', perf.get('phone', 'N/A'))}\n"
                f"📌 <b>Status:</b> {emoji_status}\n"
                f"🧾 <b>Bugun bajarilgan:</b> {completed} ta\n"
                f"📦 <b>Tayinlangan:</b> {t.get('assigned_count', 0)} ta\n"
                f"🔧 <b>Jarayonda:</b> {t.get('in_progress_count', 0)} ta\n"
                f"📈 <b>Muvaffaqiyat:</b> {success_rate}%\n"
                f"⏱ <b>O'rtacha bajarish vaqti:</b> {perf.get('avg_completion_hours', 0):.1f} soat\n"
                f"🗓 <b>Jami faol ishlar:</b> {total_active} ta\n"
                f"\n📊 <b>#{index+1}/{total}</b>"
            )
            
            kb = _tech_detail_keyboard(flt, index, total)
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=kb, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=kb, parse_mode='HTML')
                
        except Exception as e:
            logger.error(f"Error in _render_tech_detail: {e}")
            error_text = "❌ Ma'lumotlarni yuklashda xatolik"
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(error_text)
            else:
                await message_or_callback.message.edit_text(error_text)

    # Entry: reply button
    @router.message(F.text.in_(["👥 Xodimlar faoliyati", "👥 Активность сотрудников"]))
    async def technicians_activity(message: Message, state: FSMContext):
        try:
            # Get user region
            region = await get_user_region(message.from_user.id)
            if not region:
                await message.answer("❌ Region aniqlanmadi")
                return
            
            user = await get_user_by_telegram_id(region, message.from_user.id)
            if not user or user.get('role') != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            # Log action
            await audit_logger.log_action(
                user_id=message.from_user.id,
                action='CONTROLLER_ACTION',
                details={'action': 'viewed_technicians_activity'},
                region=region
            )
            
            await _render_tech_detail(message, region, flt='all', index=0)
            
        except Exception as e:
            logger.error(f"Error in technicians_activity: {e}")
            await message.answer("❌ Xatolik yuz berdi")

    # Filters
    @router.callback_query(F.data == 'ctrl_tech_filter_all')
    async def tech_filter_all(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            # Get user region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            await _render_tech_detail(callback, region, flt='all', index=0)
            
        except Exception as e:
            logger.error(f"Error in tech_filter_all: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == 'ctrl_tech_filter_online')
    async def tech_filter_online(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            # Get user region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            await _render_tech_detail(callback, region, flt='online', index=0)
            
        except Exception as e:
            logger.error(f"Error in tech_filter_online: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == 'ctrl_tech_filter_busy')
    async def tech_filter_busy(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            # Get user region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            await _render_tech_detail(callback, region, flt='busy', index=0)
            
        except Exception as e:
            logger.error(f"Error in tech_filter_busy: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    # Navigation
    @router.callback_query(lambda c: c.data.startswith('ctrl_tech_nav_prev_'))
    async def tech_nav_prev(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            # Get user region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            parts = callback.data.split('_')
            flt = parts[4]
            index = parts[5]
            await _render_tech_detail(callback, region, flt=flt, index=int(index))
            
        except Exception as e:
            logger.error(f"Error in tech_nav_prev: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(lambda c: c.data.startswith('ctrl_tech_nav_next_'))
    async def tech_nav_next(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            
            # Get user region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            parts = callback.data.split('_')
            flt = parts[4]
            index = parts[5]
            await _render_tech_detail(callback, region, flt=flt, index=int(index))
            
        except Exception as e:
            logger.error(f"Error in tech_nav_next: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(lambda c: c.data.startswith('ctrl_tech_refresh_detail_'))
    async def tech_refresh_detail(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer("🔄 Yangilanmoqda...")
            
            # Get user region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            parts = callback.data.split('_')
            flt = parts[4]
            index = parts[5]
            
            # Log refresh action
            await audit_logger.log_action(
                user_id=callback.from_user.id,
                action='CONTROLLER_ACTION',
                details={'action': 'refreshed_technician_data', 'filter': flt, 'index': index},
                region=region
            )
            
            await _render_tech_detail(callback, region, flt=flt, index=int(index))
            
        except Exception as e:
            logger.error(f"Error in tech_refresh_detail: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router