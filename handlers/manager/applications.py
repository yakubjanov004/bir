"""
Manager Applications Module - Complete Inline Keyboard Implementation
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

logger = logging.getLogger(__name__)

# ================== MOCK DATA ==================
MOCK_APPLICATIONS_DATA = {
    "applications": [
        {
            "id": "APP-2024-001",
            "type": "connection",
            "customer": "Alisher Karimov",
            "phone": "+998901234567",
            "address": "Toshkent, Chorsu",
            "tariff": "100 Mbps - 89,000 UZS",
            "status": "new",
            "priority": "high",
            "created": datetime.now() - timedelta(hours=2),
            "technician": None,
            "notes": "Mijoz tezkor ulanish so'ramoqda"
        },
        {
            "id": "APP-2024-002",
            "type": "technical",
            "customer": "Malika Azizova",
            "phone": "+998901234568",
            "address": "Toshkent, Yunusabad",
            "tariff": "200 Mbps - 149,000 UZS",
            "status": "in_progress",
            "priority": "medium",
            "created": datetime.now() - timedelta(hours=5),
            "technician": "Ahmad Toshmatov",
            "notes": "Internet sekin ishlayapti"
        },
        {
            "id": "APP-2024-003",
            "type": "change",
            "customer": "Jamshid Rahimov",
            "phone": "+998901234569",
            "address": "Toshkent, Sergeli",
            "tariff": "500 Mbps - 299,000 UZS",
            "status": "completed",
            "priority": "low",
            "created": datetime.now() - timedelta(days=1),
            "technician": "Jasur Rahimov",
            "notes": "Tarif o'zgartirildi"
        },
        {
            "id": "APP-2024-004",
            "type": "disconnect",
            "customer": "Dilnoza Saidova",
            "phone": "+998901234570",
            "address": "Toshkent, Mirzo Ulug'bek",
            "tariff": "100 Mbps - 89,000 UZS",
            "status": "pending",
            "priority": "urgent",
            "created": datetime.now() - timedelta(minutes=30),
            "technician": None,
            "notes": "Ko'chib o'tish sababli uzish"
        },
        {
            "id": "APP-2024-005",
            "type": "payment",
            "customer": "Rustam Xolmatov",
            "phone": "+998901234571",
            "address": "Toshkent, Chilonzor",
            "tariff": "1 Gbps - 499,000 UZS",
            "status": "new",
            "priority": "high",
            "created": datetime.now() - timedelta(minutes=15),
            "technician": None,
            "notes": "To'lov muammosi"
        }
    ],
    "statistics": {
        "total": 156,
        "new": 22,
        "in_progress": 45,
        "pending": 34,
        "completed": 55,
        "cancelled": 0,
        "today": 8,
        "this_week": 34,
        "this_month": 156
    },
    "technicians": [
        {"id": 1, "name": "Ahmad Toshmatov", "active": 3, "completed": 12},
        {"id": 2, "name": "Jasur Rahimov", "active": 5, "completed": 8},
        {"id": 3, "name": "Dilfuza Abdullayeva", "active": 2, "completed": 15},
        {"id": 4, "name": "Rustam Karimov", "active": 4, "completed": 10}
    ]
}

# ================== STATES ==================
class ApplicationStates(StatesGroup):
    menu = State()
    viewing_list = State()
    viewing_detail = State()
    creating = State()
    editing = State()
    assigning = State()
    filtering = State()

# ================== KEYBOARDS ==================
def get_applications_menu_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Get applications menu keyboard"""
    stats = MOCK_APPLICATIONS_DATA["statistics"]
    
    if lang == "uz":
        buttons = [
            [
                InlineKeyboardButton(
                    text=f"📋 Barcha ({stats['total']})",
                    callback_data="apps:all"
                ),
                InlineKeyboardButton(
                    text=f"🆕 Yangi ({stats['new']})",
                    callback_data="apps:new"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"🔄 Jarayonda ({stats['in_progress']})",
                    callback_data="apps:in_progress"
                ),
                InlineKeyboardButton(
                    text=f"⏳ Kutilmoqda ({stats['pending']})",
                    callback_data="apps:pending"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"✅ Bajarilgan ({stats['completed']})",
                    callback_data="apps:completed"
                ),
                InlineKeyboardButton(
                    text="➕ Yangi ariza",
                    callback_data="apps:create"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Qidirish",
                    callback_data="apps:search"
                ),
                InlineKeyboardButton(
                    text="📊 Statistika",
                    callback_data="apps:stats"
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
                    text=f"📋 Все ({stats['total']})",
                    callback_data="apps:all"
                ),
                InlineKeyboardButton(
                    text=f"🆕 Новые ({stats['new']})",
                    callback_data="apps:new"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"🔄 В процессе ({stats['in_progress']})",
                    callback_data="apps:in_progress"
                ),
                InlineKeyboardButton(
                    text=f"⏳ В ожидании ({stats['pending']})",
                    callback_data="apps:pending"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"✅ Выполненные ({stats['completed']})",
                    callback_data="apps:completed"
                ),
                InlineKeyboardButton(
                    text="➕ Новая заявка",
                    callback_data="apps:create"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Поиск",
                    callback_data="apps:search"
                ),
                InlineKeyboardButton(
                    text="📊 Статистика",
                    callback_data="apps:stats"
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

def get_application_detail_keyboard(app_id: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """Get application detail keyboard"""
    
    if lang == "uz":
        buttons = [
            [
                InlineKeyboardButton(
                    text="✏️ Tahrirlash",
                    callback_data=f"apps:edit:{app_id}"
                ),
                InlineKeyboardButton(
                    text="👨‍🔧 Texnik tayinlash",
                    callback_data=f"apps:assign:{app_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Status o'zgartirish",
                    callback_data=f"apps:status:{app_id}"
                ),
                InlineKeyboardButton(
                    text="📝 Izoh qo'shish",
                    callback_data=f"apps:note:{app_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📱 Mijoz bilan bog'lanish",
                    callback_data=f"apps:contact:{app_id}"
                ),
                InlineKeyboardButton(
                    text="🗑 O'chirish",
                    callback_data=f"apps:delete:{app_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="apps:back_to_list"
                )
            ]
        ]
    else:  # ru
        buttons = [
            [
                InlineKeyboardButton(
                    text="✏️ Редактировать",
                    callback_data=f"apps:edit:{app_id}"
                ),
                InlineKeyboardButton(
                    text="👨‍🔧 Назначить техника",
                    callback_data=f"apps:assign:{app_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Изменить статус",
                    callback_data=f"apps:status:{app_id}"
                ),
                InlineKeyboardButton(
                    text="📝 Добавить заметку",
                    callback_data=f"apps:note:{app_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📱 Связаться с клиентом",
                    callback_data=f"apps:contact:{app_id}"
                ),
                InlineKeyboardButton(
                    text="🗑 Удалить",
                    callback_data=f"apps:delete:{app_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="apps:back_to_list"
                )
            ]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_type_emoji(app_type: str) -> str:
    """Get application type emoji"""
    return {
        "connection": "🔌",
        "technical": "🔧",
        "change": "🔄",
        "disconnect": "🔚",
        "payment": "💰"
    }.get(app_type, "📋")

def get_status_emoji(status: str) -> str:
    """Get status emoji"""
    return {
        "new": "🆕",
        "in_progress": "🔄",
        "pending": "⏳",
        "completed": "✅",
        "cancelled": "❌"
    }.get(status, "❓")

def get_priority_emoji(priority: str) -> str:
    """Get priority emoji"""
    return {
        "urgent": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢"
    }.get(priority, "⚪")

def format_time_ago(dt: datetime, lang: str = "uz") -> str:
    """Format time ago"""
    now = datetime.now()
    diff = now - dt
    
    if lang == "uz":
        if diff.days > 0:
            return f"{diff.days} kun oldin"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} soat oldin"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} daqiqa oldin"
        else:
            return "hozirgina"
    else:
        if diff.days > 0:
            return f"{diff.days} дней назад"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} часов назад"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} минут назад"
        else:
            return "только что"

# ================== HANDLERS ==================
async def show_applications_menu(callback: CallbackQuery, state: FSMContext):
    """Show applications menu"""
    
    data = await state.get_data()
    lang = data.get("language", "uz")
    stats = MOCK_APPLICATIONS_DATA["statistics"]
    
    if lang == "uz":
        text = f"""
📋 <b>ARIZALAR BOSHQARUVI</b>

📊 <b>Statistika:</b>
├ 📁 Jami arizalar: {stats['total']}
├ 🆕 Yangi: {stats['new']}
├ 🔄 Jarayonda: {stats['in_progress']}
├ ⏳ Kutilmoqda: {stats['pending']}
├ ✅ Bajarilgan: {stats['completed']}
└ ❌ Bekor qilingan: {stats['cancelled']}

📅 <b>Vaqt bo'yicha:</b>
├ 📅 Bugun: {stats['today']}
├ 📆 Bu hafta: {stats['this_week']}
└ 📅 Bu oy: {stats['this_month']}

<b>Qaysi arizalarni ko'rmoqchisiz?</b>
        """
    else:
        text = f"""
📋 <b>УПРАВЛЕНИЕ ЗАЯВКАМИ</b>

📊 <b>Статистика:</b>
├ 📁 Всего заявок: {stats['total']}
├ 🆕 Новые: {stats['new']}
├ 🔄 В процессе: {stats['in_progress']}
├ ⏳ В ожидании: {stats['pending']}
├ ✅ Выполненные: {stats['completed']}
└ ❌ Отмененные: {stats['cancelled']}

📅 <b>По времени:</b>
├ 📅 Сегодня: {stats['today']}
├ 📆 На этой неделе: {stats['this_week']}
└ 📅 В этом месяце: {stats['this_month']}

<b>Какие заявки показать?</b>
        """
    
    await callback.message.edit_text(
        text,
        reply_markup=get_applications_menu_keyboard(lang),
        parse_mode="HTML"
    )
    
    await state.set_state(ApplicationStates.menu)

def get_manager_applications_router() -> Router:
    """Get complete applications router with inline keyboards"""
    router = Router()
    
    @router.callback_query(F.data.startswith("apps:"))
    async def handle_applications_callbacks(callback: CallbackQuery, state: FSMContext):
        """Handle all applications callbacks"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        action_parts = callback.data.split(":")
        action = action_parts[1]
        
        if action == "all":
            await show_applications_list(callback, state, filter_type="all")
        elif action == "new":
            await show_applications_list(callback, state, filter_type="new")
        elif action == "in_progress":
            await show_applications_list(callback, state, filter_type="in_progress")
        elif action == "pending":
            await show_applications_list(callback, state, filter_type="pending")
        elif action == "completed":
            await show_applications_list(callback, state, filter_type="completed")
        elif action == "create":
            await start_create_application(callback, state)
        elif action == "search":
            await show_search_menu(callback, state)
        elif action == "stats":
            await show_statistics(callback, state)
        elif action == "back_to_list":
            await show_applications_menu(callback, state)
        elif action == "view":
            app_id = action_parts[2]
            await show_application_detail(callback, state, app_id)
        elif action == "edit":
            app_id = action_parts[2]
            await edit_application(callback, state, app_id)
        elif action == "assign":
            app_id = action_parts[2]
            await assign_technician(callback, state, app_id)
        elif action == "status":
            app_id = action_parts[2]
            await change_status(callback, state, app_id)
        elif action == "note":
            app_id = action_parts[2]
            await add_note(callback, state, app_id)
        elif action == "contact":
            app_id = action_parts[2]
            await contact_customer(callback, state, app_id)
        elif action == "delete":
            app_id = action_parts[2]
            await delete_application(callback, state, app_id)
        
        await callback.answer()
    
    async def show_applications_list(callback: CallbackQuery, state: FSMContext, filter_type: str = "all"):
        """Show filtered applications list"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        # Filter applications
        applications = MOCK_APPLICATIONS_DATA["applications"]
        if filter_type != "all":
            applications = [app for app in applications if app["status"] == filter_type]
        
        if not applications:
            text = "Arizalar topilmadi" if lang == "uz" else "Заявки не найдены"
            await callback.message.edit_text(
                f"❌ <b>{text}</b>",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text="⬅️ Orqaga" if lang == "uz" else "⬅️ Назад",
                        callback_data="apps:back_to_list"
                    )]
                ]),
                parse_mode="HTML"
            )
            return
        
        # Build applications list
        if lang == "uz":
            text = f"📋 <b>ARIZALAR RO'YXATI</b>\n\n"
            
            for app in applications[:10]:  # Show first 10
                text += f"""
{get_type_emoji(app['type'])} #{app['id']}
👤 {app['customer']}
📱 {app['phone']}
📍 {app['address']}
{get_priority_emoji(app['priority'])} {get_status_emoji(app['status'])} {format_time_ago(app['created'], lang)}
                """
        else:
            text = f"📋 <b>СПИСОК ЗАЯВОК</b>\n\n"
            
            for app in applications[:10]:
                text += f"""
{get_type_emoji(app['type'])} #{app['id']}
👤 {app['customer']}
📱 {app['phone']}
📍 {app['address']}
{get_priority_emoji(app['priority'])} {get_status_emoji(app['status'])} {format_time_ago(app['created'], lang)}
                """
        
        # Create inline buttons for each application
        buttons = []
        for app in applications[:5]:  # Show first 5 as buttons
            buttons.append([
                InlineKeyboardButton(
                    text=f"{get_type_emoji(app['type'])} {app['id']} - {app['customer']}",
                    callback_data=f"apps:view:{app['id']}"
                )
            ])
        
        buttons.append([
            InlineKeyboardButton(
                text="⬅️ Orqaga" if lang == "uz" else "⬅️ Назад",
                callback_data="apps:back_to_list"
            )
        ])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        
        await state.set_state(ApplicationStates.viewing_list)
    
    async def show_application_detail(callback: CallbackQuery, state: FSMContext, app_id: str):
        """Show application details"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        # Find application
        app = None
        for application in MOCK_APPLICATIONS_DATA["applications"]:
            if application["id"] == app_id:
                app = application
                break
        
        if not app:
            await callback.answer("Ariza topilmadi!" if lang == "uz" else "Заявка не найдена!")
            return
        
        if lang == "uz":
            text = f"""
📋 <b>ARIZA TAFSILOTLARI</b>

🆔 <b>ID:</b> #{app['id']}
{get_type_emoji(app['type'])} <b>Turi:</b> {app['type']}
👤 <b>Mijoz:</b> {app['customer']}
📱 <b>Telefon:</b> {app['phone']}
📍 <b>Manzil:</b> {app['address']}
💰 <b>Tarif:</b> {app['tariff']}

{get_priority_emoji(app['priority'])} <b>Muhimlik:</b> {app['priority']}
{get_status_emoji(app['status'])} <b>Status:</b> {app['status']}
⏰ <b>Yaratilgan:</b> {app['created'].strftime('%Y-%m-%d %H:%M')}

👨‍🔧 <b>Texnik:</b> {app['technician'] or 'Tayinlanmagan'}

📝 <b>Izohlar:</b>
{app['notes']}

<b>Qanday amal bajarasiz?</b>
            """
        else:
            text = f"""
📋 <b>ДЕТАЛИ ЗАЯВКИ</b>

🆔 <b>ID:</b> #{app['id']}
{get_type_emoji(app['type'])} <b>Тип:</b> {app['type']}
👤 <b>Клиент:</b> {app['customer']}
📱 <b>Телефон:</b> {app['phone']}
📍 <b>Адрес:</b> {app['address']}
💰 <b>Тариф:</b> {app['tariff']}

{get_priority_emoji(app['priority'])} <b>Приоритет:</b> {app['priority']}
{get_status_emoji(app['status'])} <b>Статус:</b> {app['status']}
⏰ <b>Создано:</b> {app['created'].strftime('%Y-%m-%d %H:%M')}

👨‍🔧 <b>Техник:</b> {app['technician'] or 'Не назначен'}

📝 <b>Заметки:</b>
{app['notes']}

<b>Какое действие выполнить?</b>
            """
        
        await callback.message.edit_text(
            text,
            reply_markup=get_application_detail_keyboard(app_id, lang),
            parse_mode="HTML"
        )
        
        await state.set_state(ApplicationStates.viewing_detail)
    
    async def assign_technician(callback: CallbackQuery, state: FSMContext, app_id: str):
        """Assign technician to application"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        if lang == "uz":
            text = f"""
👨‍🔧 <b>TEXNIK TAYINLASH</b>

Ariza #{app_id} uchun texnik tanlang:
            """
        else:
            text = f"""
👨‍🔧 <b>НАЗНАЧИТЬ ТЕХНИКА</b>

Выберите техника для заявки #{app_id}:
            """
        
        buttons = []
        for tech in MOCK_APPLICATIONS_DATA["technicians"]:
            tech_text = f"👤 {tech['name']} (Faol: {tech['active']})" if lang == "uz" else f"👤 {tech['name']} (Активных: {tech['active']})"
            buttons.append([
                InlineKeyboardButton(
                    text=tech_text,
                    callback_data=f"assign:confirm:{app_id}:{tech['id']}"
                )
            ])
        
        buttons.append([
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == "uz" else "❌ Отмена",
                callback_data=f"apps:view:{app_id}"
            )
        ])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        
        await state.set_state(ApplicationStates.assigning)
    
    async def show_statistics(callback: CallbackQuery, state: FSMContext):
        """Show applications statistics"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        stats = MOCK_APPLICATIONS_DATA["statistics"]
        
        # Calculate percentages
        new_percent = (stats['new'] * 100) // stats['total'] if stats['total'] > 0 else 0
        progress_percent = (stats['in_progress'] * 100) // stats['total'] if stats['total'] > 0 else 0
        completed_percent = (stats['completed'] * 100) // stats['total'] if stats['total'] > 0 else 0
        
        if lang == "uz":
            text = f"""
📊 <b>ARIZALAR STATISTIKASI</b>

📈 <b>Umumiy ko'rsatkichlar:</b>
├ 📁 Jami: {stats['total']}
├ 🆕 Yangi: {stats['new']} ({new_percent}%)
├ 🔄 Jarayonda: {stats['in_progress']} ({progress_percent}%)
├ ⏳ Kutilmoqda: {stats['pending']}
├ ✅ Bajarilgan: {stats['completed']} ({completed_percent}%)
└ ❌ Bekor qilingan: {stats['cancelled']}

📅 <b>Vaqt bo'yicha tahlil:</b>
├ 📅 Bugun: {stats['today']}
├ 📆 Bu hafta: {stats['this_week']}
├ 📅 Bu oy: {stats['this_month']}
└ 📊 O'rtacha kunlik: {stats['this_month'] // 30}

⏰ <b>Samaradorlik:</b>
├ Yangi arizalarni qabul qilish: 15 daqiqa
├ Texnik tayinlash: 30 daqiqa
├ Hal qilish: 2-4 soat
└ Mijoz qoniqishi: 92%
            """
        else:
            text = f"""
📊 <b>СТАТИСТИКА ЗАЯВОК</b>

📈 <b>Общие показатели:</b>
├ 📁 Всего: {stats['total']}
├ 🆕 Новые: {stats['new']} ({new_percent}%)
├ 🔄 В процессе: {stats['in_progress']} ({progress_percent}%)
├ ⏳ В ожидании: {stats['pending']}
├ ✅ Выполнено: {stats['completed']} ({completed_percent}%)
└ ❌ Отменено: {stats['cancelled']}

📅 <b>Анализ по времени:</b>
├ 📅 Сегодня: {stats['today']}
├ 📆 На этой неделе: {stats['this_week']}
├ 📅 В этом месяце: {stats['this_month']}
└ 📊 Среднее в день: {stats['this_month'] // 30}

⏰ <b>Эффективность:</b>
├ Прием новых заявок: 15 минут
├ Назначение техника: 30 минут
├ Решение: 2-4 часа
└ Удовлетворенность клиентов: 92%
            """
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📤 Export" if lang == "uz" else "📤 Экспорт",
                    callback_data="apps:export_stats"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga" if lang == "uz" else "⬅️ Назад",
                    callback_data="apps:back_to_list"
                )
            ]
        ])
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    
    # Stub functions for other actions
    async def start_create_application(callback: CallbackQuery, state: FSMContext):
        await callback.answer("➕ Yangi ariza yaratish")
    
    async def show_search_menu(callback: CallbackQuery, state: FSMContext):
        await callback.answer("🔍 Qidiruv")
    
    async def edit_application(callback: CallbackQuery, state: FSMContext, app_id: str):
        await callback.answer(f"✏️ Tahrirlash: {app_id}")
    
    async def change_status(callback: CallbackQuery, state: FSMContext, app_id: str):
        await callback.answer(f"🔄 Status o'zgartirish: {app_id}")
    
    async def add_note(callback: CallbackQuery, state: FSMContext, app_id: str):
        await callback.answer(f"📝 Izoh qo'shish: {app_id}")
    
    async def contact_customer(callback: CallbackQuery, state: FSMContext, app_id: str):
        await callback.answer(f"📱 Mijoz bilan bog'lanish: {app_id}")
    
    async def delete_application(callback: CallbackQuery, state: FSMContext, app_id: str):
        await callback.answer(f"🗑 O'chirish: {app_id}")
    
    return router