"""
Manager Main Menu Module - Complete Inline Keyboard Implementation
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
MOCK_MANAGER_DATA = {
    "manager_info": {
        "id": 1,
        "name": "Alisher Karimov",
        "role": "Senior Manager",
        "department": "Operations",
        "permissions": ["view_all", "edit_all", "assign_technicians", "export_data"],
        "active_since": "2023-01-15",
        "rating": 4.8
    },
    "statistics": {
        "total_applications": 156,
        "completed": 89,
        "active": 45,
        "new": 22,
        "cancelled": 0,
        "today": 8,
        "this_week": 34,
        "this_month": 156
    },
    "inbox": {
        "unread": 12,
        "total": 45,
        "urgent": 3,
        "pending_reply": 7
    },
    "staff": {
        "total": 25,
        "active": 18,
        "on_break": 3,
        "offline": 4,
        "technicians": 15,
        "call_center": 10
    }
}

# ================== STATES ==================
class ManagerMainStates(StatesGroup):
    main_menu = State()
    waiting_action = State()

# ================== KEYBOARDS ==================
def get_main_menu_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Get main menu inline keyboard for manager"""
    
    if lang == "uz":
        buttons = [
            [
                InlineKeyboardButton(text="📥 Inbox (12)", callback_data="manager:inbox"),
                InlineKeyboardButton(text="📋 Arizalar", callback_data="manager:applications")
            ],
            [
                InlineKeyboardButton(text="🔌 Ulanish arizasi", callback_data="manager:connection"),
                InlineKeyboardButton(text="🔧 Texnik xizmat", callback_data="manager:technical")
            ],
            [
                InlineKeyboardButton(text="🕐 Real monitoring", callback_data="manager:realtime"),
                InlineKeyboardButton(text="📊 Statistika", callback_data="manager:statistics")
            ],
            [
                InlineKeyboardButton(text="👥 Xodimlar", callback_data="manager:staff"),
                InlineKeyboardButton(text="🔄 Status", callback_data="manager:status")
            ],
            [
                InlineKeyboardButton(text="📤 Export", callback_data="manager:export"),
                InlineKeyboardButton(text="🌐 Til", callback_data="manager:language")
            ]
        ]
    else:  # ru
        buttons = [
            [
                InlineKeyboardButton(text="📥 Входящие (12)", callback_data="manager:inbox"),
                InlineKeyboardButton(text="📋 Заявки", callback_data="manager:applications")
            ],
            [
                InlineKeyboardButton(text="🔌 Подключение", callback_data="manager:connection"),
                InlineKeyboardButton(text="🔧 Тех. обслуживание", callback_data="manager:technical")
            ],
            [
                InlineKeyboardButton(text="🕐 Мониторинг", callback_data="manager:realtime"),
                InlineKeyboardButton(text="📊 Статистика", callback_data="manager:statistics")
            ],
            [
                InlineKeyboardButton(text="👥 Сотрудники", callback_data="manager:staff"),
                InlineKeyboardButton(text="🔄 Статус", callback_data="manager:status")
            ],
            [
                InlineKeyboardButton(text="📤 Экспорт", callback_data="manager:export"),
                InlineKeyboardButton(text="🌐 Язык", callback_data="manager:language")
            ]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_back_button(lang: str = "uz") -> InlineKeyboardMarkup:
    """Get back button keyboard"""
    text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text, callback_data="manager:back_to_menu")]
    ])

# ================== ROUTER ==================
def get_manager_main_menu_router() -> Router:
    """Get manager main menu router"""
    router = Router()
    
    # ================== HANDLERS ==================
    
    @router.message(Command("manager"))
    async def cmd_manager_start(message: Message, state: FSMContext):
        """Manager panel start command"""
        
        # Get manager info from mock data
        manager = MOCK_MANAGER_DATA["manager_info"]
        stats = MOCK_MANAGER_DATA["statistics"]
        inbox = MOCK_MANAGER_DATA["inbox"]
        
        # Build welcome message
        welcome_text = f"""
🔐 <b>Xush kelibsiz, {manager['name']}!</b>

👤 <b>Sizning ma'lumotlaringiz:</b>
├ 💼 Lavozim: {manager['role']}
├ 🏢 Bo'lim: {manager['department']}
├ ⭐ Reyting: {manager['rating']}/5
└ 📅 Faol: {manager['active_since']}

📊 <b>Bugungi statistika:</b>
├ 📥 Yangi xabarlar: {inbox['unread']}
├ 🆕 Yangi arizalar: {stats['new']}
├ ⏳ Faol arizalar: {stats['active']}
├ ✅ Bajarilgan: {stats['completed']}
└ 👥 Faol xodimlar: {MOCK_MANAGER_DATA['staff']['active']}/{MOCK_MANAGER_DATA['staff']['total']}

<b>Quyidagi bo'limlardan birini tanlang:</b>
        """
        
        # Send welcome message with main menu
        await message.answer(
            welcome_text,
            reply_markup=get_main_menu_keyboard("uz"),
            parse_mode="HTML"
        )
        
        # Set state
        await state.set_state(ManagerMainStates.main_menu)
        await state.update_data(language="uz", manager_id=manager['id'])
    
    @router.callback_query(F.data == "manager:back_to_menu")
    async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
        """Back to main menu handler"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        # Get updated statistics
        stats = MOCK_MANAGER_DATA["statistics"]
        inbox = MOCK_MANAGER_DATA["inbox"]
        
        if lang == "uz":
            text = f"""
🏠 <b>ASOSIY MENYU</b>

📊 <b>Tezkor statistika:</b>
├ 📥 Yangi xabarlar: {inbox['unread']}
├ 🆕 Yangi arizalar: {stats['new']}
├ ⏳ Faol arizalar: {stats['active']}
└ 👥 Faol xodimlar: {MOCK_MANAGER_DATA['staff']['active']}

<b>Bo'limni tanlang:</b>
            """
        else:
            text = f"""
🏠 <b>ГЛАВНОЕ МЕНЮ</b>

📊 <b>Быстрая статистика:</b>
├ 📥 Новые сообщения: {inbox['unread']}
├ 🆕 Новые заявки: {stats['new']}
├ ⏳ Активные заявки: {stats['active']}
└ 👥 Активные сотрудники: {MOCK_MANAGER_DATA['staff']['active']}

<b>Выберите раздел:</b>
            """
        
        await callback.message.edit_text(
            text,
            reply_markup=get_main_menu_keyboard(lang),
            parse_mode="HTML"
        )
        
        await state.set_state(ManagerMainStates.main_menu)
        await callback.answer()
    
    @router.callback_query(F.data.startswith("manager:"))
    async def handle_menu_selection(callback: CallbackQuery, state: FSMContext):
        """Handle main menu selections"""
        
        action = callback.data.split(":")[1]
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        # Handle different menu selections
        if action == "inbox":
            from .inbox import show_inbox_menu
            await show_inbox_menu(callback, state)
            
        elif action == "applications":
            from .applications import show_applications_menu
            await show_applications_menu(callback, state)
            
        elif action == "connection":
            from .connection_order import show_connection_order_menu
            await show_connection_order_menu(callback, state)
            
        elif action == "technical":
            from .technician_order import show_technical_service_menu
            await show_technical_service_menu(callback, state)
            
        elif action == "realtime":
            from .realtime_monitoring import show_realtime_menu
            await show_realtime_menu(callback, state)
            
        elif action == "statistics":
            await show_statistics_menu(callback, state)
            
        elif action == "staff":
            from .staff_activity import show_staff_menu
            await show_staff_menu(callback, state)
            
        elif action == "status":
            from .status_management import show_status_menu
            await show_status_menu(callback, state)
            
        elif action == "export":
            from .export import show_export_menu
            await show_export_menu(callback, state)
            
        elif action == "language":
            from .language import show_language_menu
            await show_language_menu(callback, state)
        
        await callback.answer()
    
    async def show_statistics_menu(callback: CallbackQuery, state: FSMContext):
        """Show statistics menu"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        stats = MOCK_MANAGER_DATA["statistics"]
        
        if lang == "uz":
            text = f"""
📊 <b>STATISTIKA VA TAHLIL</b>

📈 <b>Umumiy ko'rsatkichlar:</b>
├ 📁 Jami arizalar: {stats['total_applications']}
├ ✅ Bajarilgan: {stats['completed']}
├ ⏳ Faol: {stats['active']}
├ 🆕 Yangi: {stats['new']}
└ ❌ Bekor qilingan: {stats['cancelled']}

📅 <b>Vaqt bo'yicha:</b>
├ 📅 Bugun: {stats['today']}
├ 📆 Bu hafta: {stats['this_week']}
└ 📅 Bu oy: {stats['this_month']}

<b>Qaysi statistikani ko'rmoqchisiz?</b>
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="📊 Umumiy", callback_data="stats:general"),
                    InlineKeyboardButton(text="📈 Grafik", callback_data="stats:chart")
                ],
                [
                    InlineKeyboardButton(text="👥 Xodimlar", callback_data="stats:staff"),
                    InlineKeyboardButton(text="💰 Moliyaviy", callback_data="stats:financial")
                ],
                [
                    InlineKeyboardButton(text="📅 Kunlik", callback_data="stats:daily"),
                    InlineKeyboardButton(text="📆 Haftalik", callback_data="stats:weekly")
                ],
                [
                    InlineKeyboardButton(text="📤 Export", callback_data="stats:export"),
                    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="manager:back_to_menu")
                ]
            ])
        else:
            text = f"""
📊 <b>СТАТИСТИКА И АНАЛИЗ</b>

📈 <b>Общие показатели:</b>
├ 📁 Всего заявок: {stats['total_applications']}
├ ✅ Выполнено: {stats['completed']}
├ ⏳ Активные: {stats['active']}
├ 🆕 Новые: {stats['new']}
└ ❌ Отменено: {stats['cancelled']}

📅 <b>По времени:</b>
├ 📅 Сегодня: {stats['today']}
├ 📆 На этой неделе: {stats['this_week']}
└ 📅 В этом месяце: {stats['this_month']}

<b>Какую статистику показать?</b>
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="📊 Общая", callback_data="stats:general"),
                    InlineKeyboardButton(text="📈 График", callback_data="stats:chart")
                ],
                [
                    InlineKeyboardButton(text="👥 Сотрудники", callback_data="stats:staff"),
                    InlineKeyboardButton(text="💰 Финансы", callback_data="stats:financial")
                ],
                [
                    InlineKeyboardButton(text="📅 Ежедневно", callback_data="stats:daily"),
                    InlineKeyboardButton(text="📆 Еженедельно", callback_data="stats:weekly")
                ],
                [
                    InlineKeyboardButton(text="📤 Экспорт", callback_data="stats:export"),
                    InlineKeyboardButton(text="⬅️ Назад", callback_data="manager:back_to_menu")
                ]
            ])
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    
    return router