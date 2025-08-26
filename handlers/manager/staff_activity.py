"""
Manager Staff Activity Module - Complete Inline Keyboard Implementation  
Author: Telegram Bot Development Team
Date: 2024
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import logging
import random

logger = logging.getLogger(__name__)

# ================== MOCK DATA ==================
MOCK_STAFF_DATA = {
    "technicians": [
        {
            "id": 1,
            "name": "Ahmad Toshmatov",
            "role": "Senior Texnik",
            "status": "online",
            "current_task": "APP-2024-001",
            "location": "Toshkent, Chorsu",
            "completed_today": 5,
            "active_tasks": 3,
            "rating": 4.8,
            "phone": "+998901234567",
            "last_seen": datetime.now() - timedelta(minutes=5)
        },
        {
            "id": 2,
            "name": "Jasur Rahimov",
            "role": "Texnik",
            "status": "busy",
            "current_task": "APP-2024-002",
            "location": "Toshkent, Yunusabad",
            "completed_today": 3,
            "active_tasks": 5,
            "rating": 4.5,
            "phone": "+998901234568",
            "last_seen": datetime.now() - timedelta(minutes=15)
        },
        {
            "id": 3,
            "name": "Dilfuza Abdullayeva",
            "role": "Texnik",
            "status": "break",
            "current_task": None,
            "location": "Toshkent, Sergeli",
            "completed_today": 4,
            "active_tasks": 2,
            "rating": 4.9,
            "phone": "+998901234569",
            "last_seen": datetime.now() - timedelta(minutes=30)
        },
        {
            "id": 4,
            "name": "Rustam Karimov",
            "role": "Junior Texnik",
            "status": "offline",
            "current_task": None,
            "location": "Toshkent, Mirzo Ulug'bek",
            "completed_today": 2,
            "active_tasks": 1,
            "rating": 4.3,
            "phone": "+998901234570",
            "last_seen": datetime.now() - timedelta(hours=2)
        }
    ],
    "call_center": [
        {
            "id": 5,
            "name": "Malika Karimova",
            "role": "Call Center Operator",
            "status": "online",
            "calls_today": 45,
            "active_call": True,
            "avg_call_time": "3:45",
            "rating": 4.7,
            "phone": "+998901234571",
            "last_seen": datetime.now()
        },
        {
            "id": 6,
            "name": "Dilnoza Saidova",
            "role": "Senior Operator",
            "status": "online",
            "calls_today": 52,
            "active_call": False,
            "avg_call_time": "4:12",
            "rating": 4.9,
            "phone": "+998901234572",
            "last_seen": datetime.now() - timedelta(minutes=2)
        }
    ],
    "junior_managers": [
        {
            "id": 7,
            "name": "Aziz Xolmatov",
            "role": "Junior Manager",
            "status": "online",
            "tasks_assigned": 12,
            "tasks_completed": 8,
            "active_tasks": 4,
            "rating": 4.6,
            "phone": "+998901234573",
            "last_seen": datetime.now() - timedelta(minutes=10)
        },
        {
            "id": 8,
            "name": "Shoxrux Rahimov",
            "role": "Junior Manager",
            "status": "busy",
            "tasks_assigned": 15,
            "tasks_completed": 10,
            "active_tasks": 5,
            "rating": 4.4,
            "phone": "+998901234574",
            "last_seen": datetime.now() - timedelta(minutes=20)
        }
    ],
    "statistics": {
        "total_staff": 25,
        "online": 18,
        "busy": 5,
        "break": 2,
        "offline": 4,
        "technicians_total": 15,
        "call_center_total": 6,
        "junior_managers_total": 4,
        "avg_rating": 4.6,
        "tasks_today": 156,
        "tasks_completed": 89,
        "calls_today": 234,
        "avg_response_time": "15 min"
    }
}

# ================== STATES ==================
class StaffActivityStates(StatesGroup):
    menu = State()
    viewing_list = State()
    viewing_detail = State()
    viewing_performance = State()
    viewing_statistics = State()

# ================== KEYBOARDS ==================
def get_staff_menu_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Get staff activity menu keyboard"""
    stats = MOCK_STAFF_DATA["statistics"]
    
    if lang == "uz":
        buttons = [
            [
                InlineKeyboardButton(
                    text=f"👥 Barcha xodimlar ({stats['total_staff']})",
                    callback_data="staff:all"
                ),
                InlineKeyboardButton(
                    text=f"🟢 Online ({stats['online']})",
                    callback_data="staff:online"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"👨‍🔧 Texniklar ({stats['technicians_total']})",
                    callback_data="staff:technicians"
                ),
                InlineKeyboardButton(
                    text=f"📞 Call center ({stats['call_center_total']})",
                    callback_data="staff:call_center"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"👨‍💼 Junior menejerlar ({stats['junior_managers_total']})",
                    callback_data="staff:junior_managers"
                ),
                InlineKeyboardButton(
                    text="📊 Statistika",
                    callback_data="staff:statistics"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📈 Performance",
                    callback_data="staff:performance"
                ),
                InlineKeyboardButton(
                    text="📋 Hisobotlar",
                    callback_data="staff:reports"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="manager:back_to_menu"
                )
            ]
        ]
    else:  # ru
        buttons = [
            [
                InlineKeyboardButton(
                    text=f"👥 Все сотрудники ({stats['total_staff']})",
                    callback_data="staff:all"
                ),
                InlineKeyboardButton(
                    text=f"🟢 Онлайн ({stats['online']})",
                    callback_data="staff:online"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"👨‍🔧 Техники ({stats['technicians_total']})",
                    callback_data="staff:technicians"
                ),
                InlineKeyboardButton(
                    text=f"📞 Колл-центр ({stats['call_center_total']})",
                    callback_data="staff:call_center"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"👨‍💼 Младшие менеджеры ({stats['junior_managers_total']})",
                    callback_data="staff:junior_managers"
                ),
                InlineKeyboardButton(
                    text="📊 Статистика",
                    callback_data="staff:statistics"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📈 Производительность",
                    callback_data="staff:performance"
                ),
                InlineKeyboardButton(
                    text="📋 Отчеты",
                    callback_data="staff:reports"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="manager:back_to_menu"
                )
            ]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_staff_detail_keyboard(staff_id: int, lang: str = "uz") -> InlineKeyboardMarkup:
    """Get staff detail keyboard"""
    
    if lang == "uz":
        buttons = [
            [
                InlineKeyboardButton(
                    text="📱 Bog'lanish",
                    callback_data=f"staff:contact:{staff_id}"
                ),
                InlineKeyboardButton(
                    text="📊 Performance",
                    callback_data=f"staff:perf:{staff_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Vazifalar",
                    callback_data=f"staff:tasks:{staff_id}"
                ),
                InlineKeyboardButton(
                    text="📈 Statistika",
                    callback_data=f"staff:stats:{staff_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📝 Izoh qo'shish",
                    callback_data=f"staff:note:{staff_id}"
                ),
                InlineKeyboardButton(
                    text="⚠️ Ogohlantirish",
                    callback_data=f"staff:warn:{staff_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="staff:back_to_list"
                )
            ]
        ]
    else:  # ru
        buttons = [
            [
                InlineKeyboardButton(
                    text="📱 Связаться",
                    callback_data=f"staff:contact:{staff_id}"
                ),
                InlineKeyboardButton(
                    text="📊 Производительность",
                    callback_data=f"staff:perf:{staff_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Задачи",
                    callback_data=f"staff:tasks:{staff_id}"
                ),
                InlineKeyboardButton(
                    text="📈 Статистика",
                    callback_data=f"staff:stats:{staff_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📝 Добавить заметку",
                    callback_data=f"staff:note:{staff_id}"
                ),
                InlineKeyboardButton(
                    text="⚠️ Предупреждение",
                    callback_data=f"staff:warn:{staff_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="staff:back_to_list"
                )
            ]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_status_emoji(status: str) -> str:
    """Get status emoji"""
    return {
        "online": "🟢",
        "busy": "🔴",
        "break": "🟡",
        "offline": "⚫"
    }.get(status, "⚪")

def format_last_seen(last_seen: datetime, lang: str = "uz") -> str:
    """Format last seen time"""
    now = datetime.now()
    diff = now - last_seen
    
    if lang == "uz":
        if diff.seconds < 60:
            return "Hozirgina"
        elif diff.seconds < 3600:
            return f"{diff.seconds // 60} daqiqa oldin"
        elif diff.seconds < 86400:
            return f"{diff.seconds // 3600} soat oldin"
        else:
            return f"{diff.days} kun oldin"
    else:
        if diff.seconds < 60:
            return "Только что"
        elif diff.seconds < 3600:
            return f"{diff.seconds // 60} минут назад"
        elif diff.seconds < 86400:
            return f"{diff.seconds // 3600} часов назад"
        else:
            return f"{diff.days} дней назад"

# ================== HANDLERS ==================
async def show_staff_menu(callback: CallbackQuery, state: FSMContext):
    """Show staff activity menu"""
    
    data = await state.get_data()
    lang = data.get("language", "uz")
    stats = MOCK_STAFF_DATA["statistics"]
    
    if lang == "uz":
        text = f"""
👥 <b>XODIMLAR FAOLIYATI</b>

📊 <b>Umumiy statistika:</b>
├ 👥 Jami xodimlar: {stats['total_staff']}
├ 🟢 Online: {stats['online']}
├ 🔴 Band: {stats['busy']}
├ 🟡 Tanaffus: {stats['break']}
└ ⚫ Offline: {stats['offline']}

📈 <b>Bugungi ko'rsatkichlar:</b>
├ 📋 Vazifalar: {stats['tasks_today']}
├ ✅ Bajarilgan: {stats['tasks_completed']}
├ 📞 Qo'ng'iroqlar: {stats['calls_today']}
├ ⏱️ O'rtacha javob: {stats['avg_response_time']}
└ ⭐ O'rtacha reyting: {stats['avg_rating']}

<b>Qaysi xodimlarni ko'rmoqchisiz?</b>
        """
    else:
        text = f"""
👥 <b>АКТИВНОСТЬ СОТРУДНИКОВ</b>

📊 <b>Общая статистика:</b>
├ 👥 Всего сотрудников: {stats['total_staff']}
├ 🟢 Онлайн: {stats['online']}
├ 🔴 Заняты: {stats['busy']}
├ 🟡 Перерыв: {stats['break']}
└ ⚫ Оффлайн: {stats['offline']}

📈 <b>Сегодняшние показатели:</b>
├ 📋 Задачи: {stats['tasks_today']}
├ ✅ Выполнено: {stats['tasks_completed']}
├ 📞 Звонки: {stats['calls_today']}
├ ⏱️ Среднее время ответа: {stats['avg_response_time']}
└ ⭐ Средний рейтинг: {stats['avg_rating']}

<b>Каких сотрудников показать?</b>
        """
    
    await callback.message.edit_text(
        text,
        reply_markup=get_staff_menu_keyboard(lang),
        parse_mode="HTML"
    )
    
    await state.set_state(StaffActivityStates.menu)

def get_manager_staff_activity_router() -> Router:
    """Get complete staff activity router with inline keyboards"""
    router = Router()
    
    @router.callback_query(F.data.startswith("staff:"))
    async def handle_staff_callbacks(callback: CallbackQuery, state: FSMContext):
        """Handle all staff callbacks"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        action_parts = callback.data.split(":")
        action = action_parts[1]
        
        if action == "all":
            await show_all_staff(callback, state)
        elif action == "online":
            await show_online_staff(callback, state)
        elif action == "technicians":
            await show_technicians(callback, state)
        elif action == "call_center":
            await show_call_center(callback, state)
        elif action == "junior_managers":
            await show_junior_managers(callback, state)
        elif action == "statistics":
            await show_statistics(callback, state)
        elif action == "performance":
            await show_performance(callback, state)
        elif action == "reports":
            await show_reports(callback, state)
        elif action == "back_to_list":
            await show_staff_menu(callback, state)
        elif action == "view":
            staff_id = int(action_parts[2])
            await show_staff_detail(callback, state, staff_id)
        elif action == "contact":
            staff_id = int(action_parts[2])
            await contact_staff(callback, state, staff_id)
        elif action == "perf":
            staff_id = int(action_parts[2])
            await show_staff_performance(callback, state, staff_id)
        elif action == "tasks":
            staff_id = int(action_parts[2])
            await show_staff_tasks(callback, state, staff_id)
        elif action == "stats":
            staff_id = int(action_parts[2])
            await show_staff_stats(callback, state, staff_id)
        elif action == "note":
            staff_id = int(action_parts[2])
            await add_note(callback, state, staff_id)
        elif action == "warn":
            staff_id = int(action_parts[2])
            await warn_staff(callback, state, staff_id)
        
        await callback.answer()
    
    async def show_technicians(callback: CallbackQuery, state: FSMContext):
        """Show technicians list"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        technicians = MOCK_STAFF_DATA["technicians"]
        
        if lang == "uz":
            text = "👨‍🔧 <b>TEXNIKLAR RO'YXATI</b>\n\n"
            
            for tech in technicians:
                text += f"""
{get_status_emoji(tech['status'])} <b>{tech['name']}</b>
├ 📍 {tech['location']}
├ 📋 Faol: {tech['active_tasks']} | Bajarilgan: {tech['completed_today']}
├ ⭐ Reyting: {tech['rating']}
└ 👁️ {format_last_seen(tech['last_seen'], lang)}
                """
        else:
            text = "👨‍🔧 <b>СПИСОК ТЕХНИКОВ</b>\n\n"
            
            for tech in technicians:
                text += f"""
{get_status_emoji(tech['status'])} <b>{tech['name']}</b>
├ 📍 {tech['location']}
├ 📋 Активных: {tech['active_tasks']} | Выполнено: {tech['completed_today']}
├ ⭐ Рейтинг: {tech['rating']}
└ 👁️ {format_last_seen(tech['last_seen'], lang)}
                """
        
        # Create inline buttons for each technician
        buttons = []
        for tech in technicians:
            buttons.append([
                InlineKeyboardButton(
                    text=f"{get_status_emoji(tech['status'])} {tech['name']} ({tech['active_tasks']} vazifa)",
                    callback_data=f"staff:view:{tech['id']}"
                )
            ])
        
        buttons.append([
            InlineKeyboardButton(
                text="⬅️ Orqaga" if lang == "uz" else "⬅️ Назад",
                callback_data="staff:back_to_list"
            )
        ])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        
        await state.set_state(StaffActivityStates.viewing_list)
    
    async def show_call_center(callback: CallbackQuery, state: FSMContext):
        """Show call center staff"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        operators = MOCK_STAFF_DATA["call_center"]
        
        if lang == "uz":
            text = "📞 <b>CALL CENTER XODIMLARI</b>\n\n"
            
            for op in operators:
                text += f"""
{get_status_emoji(op['status'])} <b>{op['name']}</b>
├ 💼 {op['role']}
├ 📞 Bugun: {op['calls_today']} qo'ng'iroq
├ ⏱️ O'rtacha: {op['avg_call_time']}
├ ⭐ Reyting: {op['rating']}
└ 📱 {'Faol qo'ng'iroqda' if op['active_call'] else 'Tayyor'}
                """
        else:
            text = "📞 <b>СОТРУДНИКИ КОЛЛ-ЦЕНТРА</b>\n\n"
            
            for op in operators:
                text += f"""
{get_status_emoji(op['status'])} <b>{op['name']}</b>
├ 💼 {op['role']}
├ 📞 Сегодня: {op['calls_today']} звонков
├ ⏱️ Среднее: {op['avg_call_time']}
├ ⭐ Рейтинг: {op['rating']}
└ 📱 {'На звонке' if op['active_call'] else 'Готов'}
                """
        
        # Create inline buttons
        buttons = []
        for op in operators:
            buttons.append([
                InlineKeyboardButton(
                    text=f"{get_status_emoji(op['status'])} {op['name']} ({op['calls_today']} qo'ng'iroq)",
                    callback_data=f"staff:view:{op['id']}"
                )
            ])
        
        buttons.append([
            InlineKeyboardButton(
                text="⬅️ Orqaga" if lang == "uz" else "⬅️ Назад",
                callback_data="staff:back_to_list"
            )
        ])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    
    async def show_junior_managers(callback: CallbackQuery, state: FSMContext):
        """Show junior managers list"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        junior_managers = MOCK_STAFF_DATA["junior_managers"]
        
        if lang == "uz":
            text = "👨‍💼 <b>KICHIK MENEJERLAR</b>\n\n"
            
            for jm in junior_managers:
                text += f"""
{get_status_emoji(jm['status'])} <b>{jm['name']}</b>
├ 📋 Tayinlangan: {jm['tasks_assigned']}
├ ✅ Bajarilgan: {jm['tasks_completed']}
├ 🔄 Faol: {jm['active_tasks']}
├ ⭐ Reyting: {jm['rating']}
└ 👁️ {format_last_seen(jm['last_seen'], lang)}
                """
        else:
            text = "👨‍💼 <b>МЛАДШИЕ МЕНЕДЖЕРЫ</b>\n\n"
            
            for jm in junior_managers:
                text += f"""
{get_status_emoji(jm['status'])} <b>{jm['name']}</b>
├ 📋 Назначено: {jm['tasks_assigned']}
├ ✅ Выполнено: {jm['tasks_completed']}
├ 🔄 Активных: {jm['active_tasks']}
├ ⭐ Рейтинг: {jm['rating']}
└ 👁️ {format_last_seen(jm['last_seen'], lang)}
                """
        
        # Create inline buttons
        buttons = []
        for jm in junior_managers:
            buttons.append([
                InlineKeyboardButton(
                    text=f"{get_status_emoji(jm['status'])} {jm['name']} ({jm['active_tasks']} faol)",
                    callback_data=f"staff:view:{jm['id']}"
                )
            ])
        
        buttons.append([
            InlineKeyboardButton(
                text="⬅️ Orqaga" if lang == "uz" else "⬅️ Назад",
                callback_data="staff:back_to_list"
            )
        ])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    
    async def show_staff_detail(callback: CallbackQuery, state: FSMContext, staff_id: int):
        """Show staff member details"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        # Find staff member
        staff = None
        for tech in MOCK_STAFF_DATA["technicians"]:
            if tech["id"] == staff_id:
                staff = tech
                break
        
        if not staff:
            for op in MOCK_STAFF_DATA["call_center"]:
                if op["id"] == staff_id:
                    staff = op
                    break
        
        if not staff:
            for jm in MOCK_STAFF_DATA["junior_managers"]:
                if jm["id"] == staff_id:
                    staff = jm
                    break
        
        if not staff:
            await callback.answer("Xodim topilmadi!" if lang == "uz" else "Сотрудник не найден!")
            return
        
        if lang == "uz":
            text = f"""
👤 <b>XODIM TAFSILOTLARI</b>

👤 <b>Ism:</b> {staff['name']}
💼 <b>Lavozim:</b> {staff['role']}
📱 <b>Telefon:</b> {staff['phone']}
{get_status_emoji(staff['status'])} <b>Status:</b> {staff['status']}
⭐ <b>Reyting:</b> {staff['rating']}
👁️ <b>Oxirgi faollik:</b> {format_last_seen(staff['last_seen'], lang)}

📊 <b>Bugungi ko'rsatkichlar:</b>
"""
            
            if 'completed_today' in staff:
                text += f"""├ ✅ Bajarilgan: {staff['completed_today']}
├ 🔄 Faol vazifalar: {staff['active_tasks']}
├ 📍 Joylashuv: {staff.get('location', 'Noma\'lum')}
└ 📋 Joriy vazifa: {staff.get('current_task', 'Yo\'q')}"""
            elif 'calls_today' in staff:
                text += f"""├ 📞 Qo'ng'iroqlar: {staff['calls_today']}
├ ⏱️ O'rtacha vaqt: {staff['avg_call_time']}
└ 📱 Status: {'Faol qo'ng'iroqda' if staff.get('active_call') else 'Tayyor'}"""
            else:
                text += f"""├ 📋 Tayinlangan: {staff['tasks_assigned']}
├ ✅ Bajarilgan: {staff['tasks_completed']}
└ 🔄 Faol: {staff['active_tasks']}"""
        else:
            text = f"""
👤 <b>ДЕТАЛИ СОТРУДНИКА</b>

👤 <b>Имя:</b> {staff['name']}
💼 <b>Должность:</b> {staff['role']}
📱 <b>Телефон:</b> {staff['phone']}
{get_status_emoji(staff['status'])} <b>Статус:</b> {staff['status']}
⭐ <b>Рейтинг:</b> {staff['rating']}
👁️ <b>Последняя активность:</b> {format_last_seen(staff['last_seen'], lang)}

📊 <b>Сегодняшние показатели:</b>
"""
            
            if 'completed_today' in staff:
                text += f"""├ ✅ Выполнено: {staff['completed_today']}
├ 🔄 Активные задачи: {staff['active_tasks']}
├ 📍 Местоположение: {staff.get('location', 'Неизвестно')}
└ 📋 Текущая задача: {staff.get('current_task', 'Нет')}"""
            elif 'calls_today' in staff:
                text += f"""├ 📞 Звонки: {staff['calls_today']}
├ ⏱️ Среднее время: {staff['avg_call_time']}
└ 📱 Статус: {'На звонке' if staff.get('active_call') else 'Готов'}"""
            else:
                text += f"""├ 📋 Назначено: {staff['tasks_assigned']}
├ ✅ Выполнено: {staff['tasks_completed']}
└ 🔄 Активных: {staff['active_tasks']}"""
        
        await callback.message.edit_text(
            text,
            reply_markup=get_staff_detail_keyboard(staff_id, lang),
            parse_mode="HTML"
        )
        
        await state.set_state(StaffActivityStates.viewing_detail)
    
    async def show_statistics(callback: CallbackQuery, state: FSMContext):
        """Show staff statistics"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        stats = MOCK_STAFF_DATA["statistics"]
        
        # Calculate additional stats
        efficiency = (stats['tasks_completed'] * 100) // stats['tasks_today'] if stats['tasks_today'] > 0 else 0
        online_percent = (stats['online'] * 100) // stats['total_staff'] if stats['total_staff'] > 0 else 0
        
        if lang == "uz":
            text = f"""
📊 <b>XODIMLAR STATISTIKASI</b>

👥 <b>Xodimlar taqsimoti:</b>
├ 👨‍🔧 Texniklar: {stats['technicians_total']}
├ 📞 Call center: {stats['call_center_total']}
└ 👨‍💼 Junior menejerlar: {stats['junior_managers_total']}

📈 <b>Faollik ko'rsatkichlari:</b>
├ 🟢 Online: {stats['online']} ({online_percent}%)
├ 🔴 Band: {stats['busy']}
├ 🟡 Tanaffus: {stats['break']}
└ ⚫ Offline: {stats['offline']}

📋 <b>Vazifalar statistikasi:</b>
├ 📁 Jami vazifalar: {stats['tasks_today']}
├ ✅ Bajarilgan: {stats['tasks_completed']}
├ 📊 Samaradorlik: {efficiency}%
└ ⏱️ O'rtacha vaqt: {stats['avg_response_time']}

📞 <b>Call center statistikasi:</b>
├ 📞 Jami qo'ng'iroqlar: {stats['calls_today']}
├ ⏱️ O'rtacha davomiylik: 4:23
├ 📈 Konversiya: 67%
└ ⭐ Mijoz qoniqishi: 92%

⭐ <b>Umumiy reyting:</b> {stats['avg_rating']}
            """
        else:
            text = f"""
📊 <b>СТАТИСТИКА СОТРУДНИКОВ</b>

👥 <b>Распределение сотрудников:</b>
├ 👨‍🔧 Техники: {stats['technicians_total']}
├ 📞 Колл-центр: {stats['call_center_total']}
└ 👨‍💼 Младшие менеджеры: {stats['junior_managers_total']}

📈 <b>Показатели активности:</b>
├ 🟢 Онлайн: {stats['online']} ({online_percent}%)
├ 🔴 Заняты: {stats['busy']}
├ 🟡 Перерыв: {stats['break']}
└ ⚫ Оффлайн: {stats['offline']}

📋 <b>Статистика задач:</b>
├ 📁 Всего задач: {stats['tasks_today']}
├ ✅ Выполнено: {stats['tasks_completed']}
├ 📊 Эффективность: {efficiency}%
└ ⏱️ Среднее время: {stats['avg_response_time']}

📞 <b>Статистика колл-центра:</b>
├ 📞 Всего звонков: {stats['calls_today']}
├ ⏱️ Средняя продолжительность: 4:23
├ 📈 Конверсия: 67%
└ ⭐ Удовлетворенность клиентов: 92%

⭐ <b>Общий рейтинг:</b> {stats['avg_rating']}
            """
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📤 Export" if lang == "uz" else "📤 Экспорт",
                    callback_data="staff:export_stats"
                ),
                InlineKeyboardButton(
                    text="🔄 Yangilash" if lang == "uz" else "🔄 Обновить",
                    callback_data="staff:refresh_stats"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga" if lang == "uz" else "⬅️ Назад",
                    callback_data="staff:back_to_list"
                )
            ]
        ])
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    
    # Stub functions
    async def show_all_staff(callback: CallbackQuery, state: FSMContext):
        await show_technicians(callback, state)  # Show technicians as example
    
    async def show_online_staff(callback: CallbackQuery, state: FSMContext):
        await show_technicians(callback, state)  # Show technicians as example
    
    async def show_performance(callback: CallbackQuery, state: FSMContext):
        await callback.answer("📈 Performance ko'rsatkichlari")
    
    async def show_reports(callback: CallbackQuery, state: FSMContext):
        await callback.answer("📋 Hisobotlar")
    
    async def contact_staff(callback: CallbackQuery, state: FSMContext, staff_id: int):
        await callback.answer(f"📱 Xodim bilan bog'lanish: {staff_id}")
    
    async def show_staff_performance(callback: CallbackQuery, state: FSMContext, staff_id: int):
        await callback.answer(f"📊 Xodim performance: {staff_id}")
    
    async def show_staff_tasks(callback: CallbackQuery, state: FSMContext, staff_id: int):
        await callback.answer(f"📋 Xodim vazifalari: {staff_id}")
    
    async def show_staff_stats(callback: CallbackQuery, state: FSMContext, staff_id: int):
        await callback.answer(f"📈 Xodim statistikasi: {staff_id}")
    
    async def add_note(callback: CallbackQuery, state: FSMContext, staff_id: int):
        await callback.answer(f"📝 Izoh qo'shish: {staff_id}")
    
    async def warn_staff(callback: CallbackQuery, state: FSMContext, staff_id: int):
        await callback.answer(f"⚠️ Ogohlantirish: {staff_id}")
    
    return router
