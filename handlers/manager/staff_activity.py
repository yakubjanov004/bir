"""
Manager Staff Activity Handler - Complete Implementation

This module provides complete staff activity monitoring functionality for Manager role,
allowing managers to view online staff, performance, workload, attendance, and junior manager work.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime, date, timedelta
from filters.role_filter import RoleFilter
import logging
import json
from typing import List, Dict, Any, Optional


async def get_user_by_telegram_id(region: str, telegram_id: int) -> Optional[dict]:
    """
    Mock function to get user info by telegram_id for a given region.
    In a real implementation, this would query the database.
    """
    # Example mock data for demonstration
    mock_users = [
        {
            "id": 201,
            "telegram_id": 123456789,
            "role": "manager",
            "region": "toshkent",
            "full_name": "Manager 1",
            "language": "uz"
        },
        {
            "id": 202,
            "telegram_id": 987654321,
            "role": "junior_manager",
            "region": "toshkent",
            "full_name": "Junior Manager 1",
            "language": "uz"
        },
        {
            "id": 203,
            "telegram_id": 555555555,
            "role": "technician",
            "region": "toshkent",
            "full_name": "Technician 1",
            "language": "uz"
        }
    ]
    for user in mock_users:
        if user["telegram_id"] == telegram_id and user["region"] == region:
            return user
    return None

logger = logging.getLogger(__name__)

# Calculate staff performance metrics
async def calculate_staff_performance(region: str, staff_id: int, period_days: int = 7) -> Dict[str, Any]:
    """Calculate performance metrics for a staff member"""
    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        
        # Get applications assigned to this staff
        applications = await get_manager_applications(
            region=region,
            manager_id=staff_id,
            limit=100,
            offset=0
        )
        
        # Calculate metrics
        total_tasks = len(applications)
        completed_tasks = sum(1 for app in applications if app.get('current_status') == 'completed')
        in_progress = sum(1 for app in applications if app.get('current_status') in ['in_progress', 'assigned'])
        cancelled = sum(1 for app in applications if app.get('current_status') == 'cancelled')
        
        # Calculate completion rate
        success_rate = round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
        
        # Calculate average completion time (in hours)
        completion_times = []
        for app in applications:
            if app.get('current_status') == 'completed' and app.get('created_at') and app.get('updated_at'):
                created = app['created_at']
                updated = app['updated_at']
                if isinstance(created, str):
                    created = datetime.fromisoformat(created.replace('Z', '+00:00'))
                if isinstance(updated, str):
                    updated = datetime.fromisoformat(updated.replace('Z', '+00:00'))
                hours = (updated - created).total_seconds() / 3600
                completion_times.append(hours)
        
        avg_completion_hours = round(sum(completion_times) / len(completion_times), 1) if completion_times else 0
        
        # Group by task type
        tasks_by_type = {}
        for app in applications:
            task_type = app.get('workflow_type', 'other')
            tasks_by_type[task_type] = tasks_by_type.get(task_type, 0) + 1
        
        # Today's metrics
        today = datetime.now().date()
        completed_today = sum(1 for app in applications 
                             if app.get('current_status') == 'completed' 
                             and app.get('updated_at')
                             and (datetime.fromisoformat(str(app['updated_at']).replace('Z', '+00:00')).date() == today if isinstance(app['updated_at'], str) else app['updated_at'].date() == today))
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress': in_progress,
            'cancelled': cancelled,
            'success_rate': success_rate,
            'avg_completion_hours': avg_completion_hours,
            'tasks_by_type': tasks_by_type,
            'completed_today': completed_today,
            'period_days': period_days
        }
        
    except Exception as e:
        logger.error(f"Error calculating staff performance: {e}")
        return {
            'total_tasks': 0,
            'completed_tasks': 0,
            'in_progress': 0,
            'cancelled': 0,
            'success_rate': 0,
            'avg_completion_hours': 0,
            'tasks_by_type': {},
            'completed_today': 0,
            'period_days': period_days
        }

# Get online staff members
async def get_online_staff(region: str) -> List[Dict[str, Any]]:
    """Get currently online staff members"""
    try:
        online_staff = []
        
        # Get all staff by roles
        for role in ['technician', 'controller', 'junior_manager', 'call_center']:
            staff_members = await get_staff_by_role(region, role)
            
            for staff in staff_members:
                # Check if online (last activity within 5 minutes)
                if staff.get('last_activity'):
                    last_activity = staff['last_activity']
                    if isinstance(last_activity, str):
                        last_activity = datetime.fromisoformat(last_activity.replace('Z', '+00:00'))
                    
                    if (datetime.now() - last_activity).total_seconds() < 300:  # 5 minutes
                        staff['is_online'] = True
                        staff['role_display'] = get_role_display(role)
                        online_staff.append(staff)
        
        return online_staff
        
    except Exception as e:
        logger.error(f"Error getting online staff: {e}")
        return []

# Get role display name
def get_role_display(role: str) -> str:
    """Get display name for role"""
    role_map = {
        'technician': '👨‍🔧 Texnik',
        'controller': '👮 Nazoratchi',
        'junior_manager': '👨‍💼 Kichik menejer',
        'call_center': '☎️ Call Center',
        'manager': '👨‍💼 Menejer',
        'admin': '👨‍💻 Admin'
    }
    return role_map.get(role, role)

# Calculate workload distribution
async def calculate_workload_distribution(region: str) -> Dict[str, Any]:
    """Calculate workload distribution across staff"""
    try:
        workload = {}
        
        # Get all active applications
        all_applications = await get_manager_applications(
            region=region,
            status_filter='in_progress',
            limit=200,
            offset=0
        )
        
        # Group by assignee
        for app in all_applications:
            assignee_id = app.get('current_assignee_id')
            if assignee_id:
                if assignee_id not in workload:
                    workload[assignee_id] = {
                        'total': 0,
                        'high_priority': 0,
                        'medium_priority': 0,
                        'low_priority': 0
                    }
                
                workload[assignee_id]['total'] += 1
                priority = app.get('priority', 'medium')
                workload[assignee_id][f'{priority}_priority'] += 1
        
        # Get staff info for each assignee
        result = []
        for staff_id, load in workload.items():
            staff_info = await get_user(region, staff_id)
            if staff_info:
                result.append({
                    'staff_id': staff_id,
                    'full_name': staff_info.get('full_name', 'Unknown'),
                    'role': staff_info.get('role', 'unknown'),
                    'workload': load
                })
        
        # Sort by total workload
        result.sort(key=lambda x: x['workload']['total'], reverse=True)
        
        return {
            'distribution': result,
            'total_active': sum(w['workload']['total'] for w in result),
            'staff_count': len(result)
        }
        
    except Exception as e:
        logger.error(f"Error calculating workload distribution: {e}")
        return {'distribution': [], 'total_active': 0, 'staff_count': 0}


def get_manager_staff_activity_router():
    """Get router for manager staff activity handlers"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text == "👥 Xodimlar faoliyati")
    async def show_staff_activity_menu(message: Message, state: FSMContext):
        """Manager staff activity handler"""
        try:
            # Get user data from state
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Get manager info
            manager = await get_user_by_telegram_id(region, message.from_user.id)
            if not manager:
                await message.answer("❌ Manager topilmadi")
                return
            
            # Get online staff count
            online_staff = await get_online_staff(region)
            online_count = len(online_staff)
            
            # Get workload summary
            workload = await calculate_workload_distribution(region)
            
            activity_text = (
                f"👥 <b>Xodimlar faoliyati</b>\n\n"
                f"🟢 Online xodimlar: {online_count} ta\n"
                f"📋 Aktiv vazifalar: {workload['total_active']} ta\n"
                f"👷 Ishlayotgan xodimlar: {workload['staff_count']} ta\n\n"
                f"Quyidagi bo'limlardan birini tanlang:"
            )
            
            keyboard = _create_staff_activity_keyboard()
            await message.answer(activity_text, reply_markup=keyboard, parse_mode='HTML')
            
            # Save region to state for callbacks
            await state.update_data(region=region, manager_id=manager.get('id'))
            
            # Log action
            await audit_logger.log_manager_action(
                manager_id=manager.get('id'),
                action='view_staff_activity',
                details={'online_count': online_count, 'active_tasks': workload['total_active']}
            )
            
        except Exception as e:
            logger.error(f"Error showing staff activity menu: {e}")
            await message.answer("❌ Xatolik yuz berdi")

    # Inline callbacks for staff activity sections
    @router.callback_query(F.data == "staff_performance")
    async def cb_staff_performance(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await show_staff_performance(callback.message, state)

    @router.callback_query(F.data == "staff_workload")
    async def cb_staff_workload(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await show_staff_workload(callback.message, state)

    @router.callback_query(F.data == "staff_user_detail")
    async def cb_staff_user_detail(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.update_data(staff_user_index=0)
        await show_staff_user_detail(callback, state)

    @router.callback_query(F.data == "staff_user_prev")
    async def cb_staff_user_prev(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        idx = max(0, int(data.get('staff_user_index', 0)) - 1)
        await state.update_data(staff_user_index=idx)
        await show_staff_user_detail(callback, state)

    @router.callback_query(F.data == "staff_user_next")
    async def cb_staff_user_next(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        idx = int(data.get('staff_user_index', 0)) + 1
        await state.update_data(staff_user_index=idx)
        await show_staff_user_detail(callback, state)

    @router.callback_query(F.data == "staff_back")
    async def cb_staff_back(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        from keyboards.manager_buttons import get_manager_main_keyboard
        await callback.message.edit_text("Asosiy menyu:")
        await callback.message.answer("Asosiy menyu:", reply_markup=get_manager_main_keyboard())

    async def show_staff_performance(message, state: FSMContext):
        """Show staff performance statistics"""
        try:
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Get all staff members
            performance_data = []
            
            for role in ['technician', 'controller', 'junior_manager', 'call_center']:
                staff_members = await get_staff_by_role(region, role)
                
                for staff in staff_members[:3]:  # Limit to top 3 per role
                    # Calculate performance for each staff
                    perf = await calculate_staff_performance(region, staff.get('id'), period_days=7)
                    
                    performance_data.append({
                        'full_name': staff.get('full_name', 'Unknown'),
                        'role': get_role_display(role),
                        'completed_tasks': perf['completed_tasks'],
                        'total_tasks': perf['total_tasks'],
                        'success_rate': perf['success_rate'],
                        'avg_hours': perf['avg_completion_hours']
                    })
            
            # Sort by success rate
            performance_data.sort(key=lambda x: x['success_rate'], reverse=True)
            
            text = "📊 <b>Xodimlar samaradorligi (7 kunlik)</b>\n\n"
            
            for i, s in enumerate(performance_data[:10], 1):  # Show top 10
                emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "👤"
                text += (
                    f"{emoji} <b>{s['full_name']}</b> ({s['role']})\n"
                    f"   ✅ Bajarilgan: {s['completed_tasks']}/{s['total_tasks']} "
                    f"({s['success_rate']}%)\n"
                    f"   ⏱️ O'rtacha: {s['avg_hours']} soat\n\n"
                )
            
            if not performance_data:
                text += "📭 Ma'lumot topilmadi"
            
            await message.answer(text, parse_mode='HTML')
            
            # Log action
            await audit_logger.log_manager_action(
                manager_id=state_data.get('manager_id'),
                action='view_staff_performance',
                details={'staff_count': len(performance_data)}
            )
            
        except Exception as e:
            logger.error(f"Error showing staff performance: {e}")
            await message.answer("❌ Xatolik yuz berdi")

    async def show_staff_workload(message, state: FSMContext):
        """Show staff workload statistics"""
        try:
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Get workload distribution
            workload_data = await calculate_workload_distribution(region)
            
            text = "📋 <b>Xodimlar ish yuki</b>\n\n"
            
            if workload_data['distribution']:
                # Group by priority
                high_load = [s for s in workload_data['distribution'] if s['workload']['total'] >= 10]
                medium_load = [s for s in workload_data['distribution'] if 5 <= s['workload']['total'] < 10]
                low_load = [s for s in workload_data['distribution'] if s['workload']['total'] < 5]
                
                if high_load:
                    text += "🔴 <b>Yuqori yuklanish:</b>\n"
                    for s in high_load[:5]:
                        text += (
                            f"👤 {s['full_name']} ({get_role_display(s['role'])})\n"
                            f"   📋 Jami: {s['workload']['total']} ta\n"
                            f"   🔥 Yuqori: {s['workload']['high_priority']}, "
                            f"⚡ O'rta: {s['workload']['medium_priority']}, "
                            f"💤 Past: {s['workload']['low_priority']}\n\n"
                        )
                
                if medium_load:
                    text += "🟡 <b>O'rtacha yuklanish:</b>\n"
                    for s in medium_load[:5]:
                        text += (
                            f"👤 {s['full_name']}: {s['workload']['total']} ta vazifa\n"
                        )
                    text += "\n"
                
                if low_load:
                    text += "🟢 <b>Past yuklanish:</b>\n"
                    for s in low_load[:5]:
                        text += (
                            f"👤 {s['full_name']}: {s['workload']['total']} ta vazifa\n"
                        )
                
                text += (
                    f"\n📊 <b>Umumiy statistika:</b>\n"
                    f"├ Jami aktiv vazifalar: {workload_data['total_active']} ta\n"
                    f"├ Ishlayotgan xodimlar: {workload_data['staff_count']} ta\n"
                    f"└ O'rtacha yuklanish: {round(workload_data['total_active'] / workload_data['staff_count'], 1) if workload_data['staff_count'] > 0 else 0} ta\n"
                )
            else:
                text += "📭 Hozircha aktiv vazifalar yo'q"
            
            await message.answer(text, parse_mode='HTML')
            
            # Log action
            await audit_logger.log_manager_action(
                manager_id=state_data.get('manager_id'),
                action='view_staff_workload',
                details={'total_active': workload_data['total_active'], 'staff_count': workload_data['staff_count']}
            )
            
        except Exception as e:
            logger.error(f"Error showing staff workload: {e}")
            await message.answer("❌ Xatolik yuz berdi")

    async def show_staff_user_detail(message_or_callback, state: FSMContext):
        """Per-employee detailed card with navigation"""
        try:
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Get all staff members
            staff_list = []
            for role in ['technician', 'controller', 'junior_manager', 'call_center']:
                staff_members = await get_staff_by_role(region, role)
                
                for staff in staff_members[:5]:  # Limit per role
                    # Calculate detailed performance
                    perf_7days = await calculate_staff_performance(region, staff.get('id'), period_days=7)
                    perf_1day = await calculate_staff_performance(region, staff.get('id'), period_days=1)
                    
                    staff_detail = {
                        'id': staff.get('id'),
                        'full_name': staff.get('full_name', 'Unknown'),
                        'role': role,
                        'phone': staff.get('phone', 'N/A'),
                        'completed_today': perf_1day['completed_today'],
                        'in_progress': perf_7days['in_progress'],
                        'cancelled': perf_7days['cancelled'],
                        'success_rate': perf_7days['success_rate'],
                        'avg_completion_hours': perf_7days['avg_completion_hours'],
                        'tasks_by_type': perf_7days['tasks_by_type'],
                        'last_7_days_completed': perf_7days['completed_tasks'],
                        'last_7_days_total': perf_7days['total_tasks'],
                        'is_online': False
                    }
                    
                    # Check if online
                    if staff.get('last_activity'):
                        last_activity = staff['last_activity']
                        if isinstance(last_activity, str):
                            last_activity = datetime.fromisoformat(last_activity.replace('Z', '+00:00'))
                        
                        if (datetime.now() - last_activity).total_seconds() < 300:  # 5 minutes
                            staff_detail['is_online'] = True
                    
                    staff_list.append(staff_detail)
            
            if not staff_list:
                await message_or_callback.answer("📭 Xodimlar topilmadi")
                return
            idx = max(0, min(int(state_data.get('staff_user_index', 0)), len(staff_list) - 1))
            s = staff_list[idx]
            
            # Format task types
            by_type_lines = "\n".join([f"   • {k}: {v} ta" for k, v in s['tasks_by_type'].items()]) if s['tasks_by_type'] else "   • Ma'lumot yo'q"
            
            # Online status
            online_status = "🟢 Online" if s.get('is_online') else "⚫ Offline"
            
            text = (
                f"👤 <b>{s['full_name']}</b> — {get_role_display(s['role'])} {online_status}\n"
                f"📱 Telefon: {s.get('phone', 'N/A')}\n\n"
                f"📊 <b>Bugungi faoliyat:</b>\n"
                f"├ ✅ Bajarilgan: {s['completed_today']} ta\n"
                f"├ ⏳ Jarayonda: {s['in_progress']} ta\n"
                f"└ ❌ Bekor qilingan: {s['cancelled']} ta\n\n"
                f"📈 <b>Samaradorlik ko'rsatkichlari:</b>\n"
                f"├ Muvaffaqiyat darajasi: {s['success_rate']}%\n"
                f"├ O'rtacha bajarish vaqti: {s['avg_completion_hours']} soat\n"
                f"└ Umumiy samaradorlik: {'Yuqori' if s['success_rate'] >= 90 else 'O\'rta' if s['success_rate'] >= 70 else 'Past'}\n\n"
                f"🗂 <b>Ish turlari bo'yicha taqsimot:</b>\n{by_type_lines}\n\n"
                f"📅 <b>Haftalik statistika:</b>\n"
                f"├ Bajarilgan: {s['last_7_days_completed']} ta\n"
                f"├ Jami vazifalar: {s['last_7_days_total']} ta\n"
                f"└ O'rtacha vaqt: {s['avg_completion_hours']} soat\n\n"
                f"📊 <b>Xodim #{idx+1}/{len(staff_list)}</b>"
            )
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text='⬅️ Oldingi', callback_data='staff_user_prev') if idx > 0 else InlineKeyboardButton(text=f'{idx+1}/{len(staff_list)}', callback_data='noop'),
                    InlineKeyboardButton(text='Keyingi ➡️', callback_data='staff_user_next') if idx < len(staff_list)-1 else InlineKeyboardButton(text=f'{idx+1}/{len(staff_list)}', callback_data='noop')
                ],
                [InlineKeyboardButton(text='⬅️ Orqaga', callback_data='staff_back')]
            ])
            
            if isinstance(message_or_callback, CallbackQuery):
                try:
                    await message_or_callback.message.edit_text(text, reply_markup=kb, parse_mode='HTML')
                except Exception:
                    await message_or_callback.message.answer(text, reply_markup=kb, parse_mode='HTML')
            else:
                await message_or_callback.answer(text, reply_markup=kb, parse_mode='HTML')
            
            # Log action
            await audit_logger.log_manager_action(
                manager_id=state_data.get('manager_id'),
                action='view_staff_detail',
                details={'staff_id': s.get('id'), 'staff_name': s['full_name']}
            )
            
        except Exception as e:
            logger.error(f"Error showing staff detail: {e}")
            if isinstance(message_or_callback, CallbackQuery):
                await message_or_callback.answer("❌ Xatolik yuz berdi", show_alert=True)
            else:
                await message_or_callback.answer("❌ Xatolik yuz berdi")

    return router


def _create_staff_activity_keyboard():
    """Create keyboard for staff activity menu (updated)"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Samaradorlik", callback_data="staff_performance"),
            InlineKeyboardButton(text="📋 Ish yuki", callback_data="staff_workload"),
        ],
        [
            InlineKeyboardButton(text="👤 Xodimlar kesimi", callback_data="staff_user_detail"),
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="staff_back")
        ],
    ])
