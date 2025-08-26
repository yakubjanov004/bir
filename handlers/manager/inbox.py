"""
Manager Inbox Module - Complete Inline Keyboard Implementation
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
import asyncio

logger = logging.getLogger(__name__)

# ================== MOCK DATA ==================
MOCK_INBOX_DATA = {
    "messages": [
        {
            "id": "12345",
            "from": "Alisher Karimov",
            "phone": "+998901234567",
            "subject": "Ulanish arizasi",
            "message": "Internet ulash kerak. Manzil: Toshkent, Chorsu, 100 Mbps tarif",
            "priority": "urgent",
            "status": "new",
            "time": datetime.now() - timedelta(hours=2),
            "type": "connection",
            "address": "Toshkent, Chorsu",
            "tariff": "100 Mbps - 89,000 UZS"
        },
        {
            "id": "12344",
            "from": "Malika Azizova",
            "phone": "+998901234568",
            "subject": "Texnik xizmat",
            "message": "Internet sekin ishlayapti, tekshirish kerak",
            "priority": "medium",
            "status": "pending",
            "time": datetime.now() - timedelta(hours=1),
            "type": "technical",
            "address": "Toshkent, Yunusabad",
            "tariff": "200 Mbps - 149,000 UZS"
        },
        {
            "id": "12343",
            "from": "Jamshid Rahimov",
            "phone": "+998901234569",
            "subject": "Tarif o'zgartirish",
            "message": "100 Mbps dan 200 Mbps ga o'tkazish",
            "priority": "low",
            "status": "resolved",
            "time": datetime.now() - timedelta(minutes=30),
            "type": "change",
            "address": "Toshkent, Sergeli",
            "tariff": "500 Mbps - 299,000 UZS"
        },
        {
            "id": "12342",
            "from": "Dilnoza Saidova",
            "phone": "+998901234570",
            "subject": "Yangi ulanish",
            "message": "Ofisga internet kerak, 1 Gbps tarif",
            "priority": "high",
            "status": "new",
            "time": datetime.now() - timedelta(minutes=15),
            "type": "connection",
            "address": "Toshkent, Mirzo Ulug'bek",
            "tariff": "1 Gbps - 499,000 UZS"
        },
        {
            "id": "12341",
            "from": "Rustam Xolmatov",
            "phone": "+998901234571",
            "subject": "To'lov muammosi",
            "message": "To'lov o'tmadi, yordam kerak",
            "priority": "urgent",
            "status": "in_progress",
            "time": datetime.now() - timedelta(minutes=5),
            "type": "payment",
            "address": "Toshkent, Chilonzor",
            "tariff": "100 Mbps - 89,000 UZS"
        }
    ],
    "statistics": {
        "total": 45,
        "unread": 12,
        "urgent": 3,
        "pending": 7,
        "resolved": 25,
        "in_progress": 8
    },
    "junior_managers": [
        {"id": 11, "name": "Ahmad Toshmatov", "active_tasks": 3},
        {"id": 12, "name": "Malika Karimova", "active_tasks": 2},
        {"id": 13, "name": "Jasur Rahimov", "active_tasks": 5},
        {"id": 14, "name": "Dilfuza Abdullayeva", "active_tasks": 1}
    ]
}

# ================== STATES ==================
class ManagerInboxStates(StatesGroup):
    inbox_menu = State()
    viewing_messages = State()
    viewing_message_detail = State()
    replying_message = State()
    filtering = State()
    assigning_junior = State()
    searching = State()

# ================== KEYBOARDS ==================
def get_inbox_menu_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Get inbox menu keyboard"""
    stats = MOCK_INBOX_DATA["statistics"]
    
    if lang == "uz":
        buttons = [
            [
                InlineKeyboardButton(
                    text=f"📋 Hammasi ({stats['total']})", 
                    callback_data="inbox:all"
                ),
                InlineKeyboardButton(
                    text=f"🆕 Yangi ({stats['unread']})", 
                    callback_data="inbox:new"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"🔴 Shoshilinch ({stats['urgent']})", 
                    callback_data="inbox:urgent"
                ),
                InlineKeyboardButton(
                    text=f"⏳ Kutilmoqda ({stats['pending']})", 
                    callback_data="inbox:pending"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"🔄 Jarayonda ({stats['in_progress']})", 
                    callback_data="inbox:in_progress"
                ),
                InlineKeyboardButton(
                    text=f"✅ Hal qilingan ({stats['resolved']})", 
                    callback_data="inbox:resolved"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Qidirish", 
                    callback_data="inbox:search"
                ),
                InlineKeyboardButton(
                    text="📊 Statistika", 
                    callback_data="inbox:stats"
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
                    callback_data="inbox:all"
                ),
                InlineKeyboardButton(
                    text=f"🆕 Новые ({stats['unread']})", 
                    callback_data="inbox:new"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"🔴 Срочные ({stats['urgent']})", 
                    callback_data="inbox:urgent"
                ),
                InlineKeyboardButton(
                    text=f"⏳ В ожидании ({stats['pending']})", 
                    callback_data="inbox:pending"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"🔄 В процессе ({stats['in_progress']})", 
                    callback_data="inbox:in_progress"
                ),
                InlineKeyboardButton(
                    text=f"✅ Решенные ({stats['resolved']})", 
                    callback_data="inbox:resolved"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔍 Поиск", 
                    callback_data="inbox:search"
                ),
                InlineKeyboardButton(
                    text="📊 Статистика", 
                    callback_data="inbox:stats"
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

def get_message_navigation_keyboard(current_index: int, total: int, message_id: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """Get message navigation keyboard with junior manager assignment"""
    
    buttons = []
    
    # Navigation row
    nav_row = []
    if current_index > 0:
        nav_row.append(InlineKeyboardButton(
            text="⬅️ Oldingi" if lang == "uz" else "⬅️ Предыдущий",
            callback_data=f"inbox:prev:{current_index}"
        ))
    
    nav_row.append(InlineKeyboardButton(
        text=f"{current_index + 1}/{total}",
        callback_data="inbox:page_info"
    ))
    
    if current_index < total - 1:
        nav_row.append(InlineKeyboardButton(
            text="Keyingi ➡️" if lang == "uz" else "Следующий ➡️",
            callback_data=f"inbox:next:{current_index}"
        ))
    
    if nav_row:
        buttons.append(nav_row)
    
    # Action buttons
    if lang == "uz":
        buttons.extend([
            [
                InlineKeyboardButton(
                    text="👨‍💼 Kichik menejerga yuborish",
                    callback_data=f"inbox:assign_junior:{message_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 Javob berish",
                    callback_data=f"inbox:reply:{message_id}"
                ),
                InlineKeyboardButton(
                    text="✅ Hal qilindi",
                    callback_data=f"inbox:resolve:{message_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Batafsil",
                    callback_data=f"inbox:detail:{message_id}"
                ),
                InlineKeyboardButton(
                    text="🔄 Status",
                    callback_data=f"inbox:status:{message_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="inbox:back_to_list"
                )
            ]
        ])
    else:
        buttons.extend([
            [
                InlineKeyboardButton(
                    text="👨‍💼 Отправить младшему менеджеру",
                    callback_data=f"inbox:assign_junior:{message_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 Ответить",
                    callback_data=f"inbox:reply:{message_id}"
                ),
                InlineKeyboardButton(
                    text="✅ Решено",
                    callback_data=f"inbox:resolve:{message_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Подробнее",
                    callback_data=f"inbox:detail:{message_id}"
                ),
                InlineKeyboardButton(
                    text="🔄 Статус",
                    callback_data=f"inbox:status:{message_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="inbox:back_to_list"
                )
            ]
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_junior_managers_keyboard(message_id: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """Get junior managers selection keyboard"""
    
    buttons = []
    
    for jm in MOCK_INBOX_DATA["junior_managers"]:
        text = f"👤 {jm['name']} (Faol: {jm['active_tasks']})" if lang == "uz" else f"👤 {jm['name']} (Активных: {jm['active_tasks']})"
        buttons.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"inbox:confirm_junior:{message_id}:{jm['id']}"
            )
        ])
    
    buttons.append([
        InlineKeyboardButton(
            text="❌ Bekor qilish" if lang == "uz" else "❌ Отмена",
            callback_data=f"inbox:cancel_junior:{message_id}"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def format_time_ago(dt: datetime, lang: str = "uz") -> str:
    """Format time ago string"""
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
    else:  # ru
        if diff.days > 0:
            return f"{diff.days} дней назад"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600} часов назад"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60} минут назад"
        else:
            return "только что"

def get_priority_emoji(priority: str) -> str:
    """Get priority emoji"""
    return {
        "urgent": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🟢"
    }.get(priority, "⚪")

def get_status_emoji(status: str) -> str:
    """Get status emoji"""
    return {
        "new": "🆕",
        "pending": "⏳",
        "in_progress": "🔄",
        "resolved": "✅",
        "closed": "🔒"
    }.get(status, "❓")

# ================== HANDLERS ==================
async def show_inbox_menu(callback: CallbackQuery, state: FSMContext):
    """Show inbox menu"""
    
    data = await state.get_data()
    lang = data.get("language", "uz")
    stats = MOCK_INBOX_DATA["statistics"]
    
    if lang == "uz":
        text = f"""
📥 <b>KELGAN XABARLAR</b>

📊 <b>Statistika:</b>
├ 📬 Jami xabarlar: {stats['total']}
├ 🆕 Yangi: {stats['unread']}
├ 🔴 Shoshilinch: {stats['urgent']}
├ ⏳ Kutilmoqda: {stats['pending']}
├ 🔄 Jarayonda: {stats['in_progress']}
└ ✅ Hal qilingan: {stats['resolved']}

<b>Qaysi xabarlarni ko'rmoqchisiz?</b>
        """
    else:
        text = f"""
📥 <b>ВХОДЯЩИЕ СООБЩЕНИЯ</b>

📊 <b>Статистика:</b>
├ 📬 Всего сообщений: {stats['total']}
├ 🆕 Новые: {stats['unread']}
├ 🔴 Срочные: {stats['urgent']}
├ ⏳ В ожидании: {stats['pending']}
├ 🔄 В процессе: {stats['in_progress']}
└ ✅ Решенные: {stats['resolved']}

<b>Какие сообщения показать?</b>
        """
    
    await callback.message.edit_text(
        text,
        reply_markup=get_inbox_menu_keyboard(lang),
        parse_mode="HTML"
    )
    
    await state.set_state(ManagerInboxStates.inbox_menu)

def get_manager_inbox_router_min() -> Router:
    """Get complete manager inbox router with inline keyboards"""
    router = Router()
    
    @router.callback_query(F.data.startswith("inbox:"))
    async def handle_inbox_callbacks(callback: CallbackQuery, state: FSMContext):
        """Handle all inbox callbacks"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        action_parts = callback.data.split(":")
        action = action_parts[1]
        
        # Handle different actions
        if action == "all":
            await show_messages_list(callback, state, filter_type="all")
        elif action == "new":
            await show_messages_list(callback, state, filter_type="new")
        elif action == "urgent":
            await show_messages_list(callback, state, filter_type="urgent")
        elif action == "pending":
            await show_messages_list(callback, state, filter_type="pending")
        elif action == "in_progress":
            await show_messages_list(callback, state, filter_type="in_progress")
        elif action == "resolved":
            await show_messages_list(callback, state, filter_type="resolved")
        elif action == "search":
            await show_search_menu(callback, state)
        elif action == "stats":
            await show_inbox_statistics(callback, state)
        elif action == "back_to_list":
            await show_inbox_menu(callback, state)
        elif action == "prev":
            current_index = int(action_parts[2])
            await navigate_message(callback, state, current_index - 1)
        elif action == "next":
            current_index = int(action_parts[2])
            await navigate_message(callback, state, current_index + 1)
        elif action == "assign_junior":
            message_id = action_parts[2]
            await show_junior_managers_list(callback, state, message_id)
        elif action == "confirm_junior":
            message_id = action_parts[2]
            junior_id = action_parts[3]
            await assign_to_junior_manager(callback, state, message_id, junior_id)
        elif action == "cancel_junior":
            message_id = action_parts[2]
            await cancel_junior_assignment(callback, state, message_id)
        elif action == "reply":
            message_id = action_parts[2]
            await start_reply_process(callback, state, message_id)
        elif action == "resolve":
            message_id = action_parts[2]
            await resolve_message(callback, state, message_id)
        elif action == "detail":
            message_id = action_parts[2]
            await show_message_detail(callback, state, message_id)
        elif action == "status":
            message_id = action_parts[2]
            await change_message_status(callback, state, message_id)
        elif action == "page_info":
            await callback.answer()
            return
        
        if action != "page_info":
            await callback.answer()
    
    async def show_messages_list(callback: CallbackQuery, state: FSMContext, filter_type: str = "all"):
        """Show filtered messages list"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        # Filter messages based on type
        messages = MOCK_INBOX_DATA["messages"]
        if filter_type == "new":
            messages = [m for m in messages if m["status"] == "new"]
        elif filter_type == "urgent":
            messages = [m for m in messages if m["priority"] == "urgent"]
        elif filter_type == "pending":
            messages = [m for m in messages if m["status"] == "pending"]
        elif filter_type == "in_progress":
            messages = [m for m in messages if m["status"] == "in_progress"]
        elif filter_type == "resolved":
            messages = [m for m in messages if m["status"] == "resolved"]
        
        if not messages:
            text = "Xabarlar topilmadi" if lang == "uz" else "Сообщения не найдены"
            await callback.message.edit_text(
                f"❌ <b>{text}</b>",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text="⬅️ Orqaga" if lang == "uz" else "⬅️ Назад",
                        callback_data="inbox:back_to_list"
                    )]
                ]),
                parse_mode="HTML"
            )
            return
        
        # Show first message
        await state.update_data(current_messages=messages, current_index=0)
        await navigate_message(callback, state, 0)
    
    async def navigate_message(callback: CallbackQuery, state: FSMContext, index: int):
        """Navigate through messages"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        messages = data.get("current_messages", MOCK_INBOX_DATA["messages"])
        
        if index < 0 or index >= len(messages):
            await callback.answer("Xabar mavjud emas" if lang == "uz" else "Сообщение не существует")
            return
        
        message = messages[index]
        
        # Format message display
        if lang == "uz":
            text = f"""
📧 <b>ARIZA #{message['id']}</b>

🆔 ID: #{message['id']}
💰 Tarif: {message['tariff']}
👤 Mijoz: {message['from']}
📱 Telefon: {message['phone']}
📍 Manzil: {message['address']}
⏰ Yaratilgan: {format_time_ago(message['time'], lang)}

{get_priority_emoji(message['priority'])} Muhimlik: {message['priority']}
{get_status_emoji(message['status'])} Status: {message['status']}

📝 <b>Xabar:</b>
{message['message']}
            """
        else:
            text = f"""
📧 <b>ЗАЯВКА #{message['id']}</b>

🆔 ID: #{message['id']}
💰 Тариф: {message['tariff']}
👤 Клиент: {message['from']}
📱 Телефон: {message['phone']}
📍 Адрес: {message['address']}
⏰ Создано: {format_time_ago(message['time'], lang)}

{get_priority_emoji(message['priority'])} Приоритет: {message['priority']}
{get_status_emoji(message['status'])} Статус: {message['status']}

📝 <b>Сообщение:</b>
{message['message']}
            """
        
        keyboard = get_message_navigation_keyboard(index, len(messages), message['id'], lang)
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        
        await state.update_data(current_index=index)
    
    async def show_junior_managers_list(callback: CallbackQuery, state: FSMContext, message_id: str):
        """Show junior managers list for assignment"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        if lang == "uz":
            text = f"""
👨‍💼 <b>KICHIK MENEJER TANLASH</b>

Ariza #{message_id} uchun kichik menejerni tanlang:

📊 Faol vazifalar soni ko'rsatilgan
            """
        else:
            text = f"""
👨‍💼 <b>ВЫБОР МЛАДШЕГО МЕНЕДЖЕРА</b>

Выберите младшего менеджера для заявки #{message_id}:

📊 Показано количество активных задач
            """
        
        keyboard = get_junior_managers_keyboard(message_id, lang)
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        
        await state.set_state(ManagerInboxStates.assigning_junior)
    
    async def assign_to_junior_manager(callback: CallbackQuery, state: FSMContext, message_id: str, junior_id: str):
        """Assign message to junior manager"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        # Find junior manager name
        junior_name = None
        for jm in MOCK_INBOX_DATA["junior_managers"]:
            if str(jm['id']) == junior_id:
                junior_name = jm['name']
                jm['active_tasks'] += 1
                break
        
        if lang == "uz":
            text = f"""
✅ <b>MUVAFFAQIYATLI YUBORILDI!</b>

Ariza #{message_id}
Kichik menejerga yuborildi: {junior_name}
Vaqt: {datetime.now().strftime('%H:%M')}

Keyingi arizaga o'tish...
            """
        else:
            text = f"""
✅ <b>УСПЕШНО ОТПРАВЛЕНО!</b>

Заявка #{message_id}
Отправлена младшему менеджеру: {junior_name}
Время: {datetime.now().strftime('%H:%M')}

Переход к следующей заявке...
            """
        
        await callback.message.edit_text(
            text,
            parse_mode="HTML"
        )
        
        # Auto-navigate to next message after 2 seconds
        await asyncio.sleep(2)
        
        # Navigate to next message
        current_index = data.get("current_index", 0)
        messages = data.get("current_messages", MOCK_INBOX_DATA["messages"])
        
        if current_index < len(messages) - 1:
            await navigate_message(callback, state, current_index + 1)
        else:
            await show_inbox_menu(callback, state)
    
    async def cancel_junior_assignment(callback: CallbackQuery, state: FSMContext, message_id: str):
        """Cancel junior manager assignment"""
        
        data = await state.get_data()
        current_index = data.get("current_index", 0)
        await navigate_message(callback, state, current_index)
    
    async def show_message_detail(callback: CallbackQuery, state: FSMContext, message_id: str):
        """Show detailed message information"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        # Find message
        message = None
        for msg in MOCK_INBOX_DATA["messages"]:
            if msg["id"] == message_id:
                message = msg
                break
        
        if not message:
            await callback.answer("Xabar topilmadi!" if lang == "uz" else "Сообщение не найдено!")
            return
        
        if lang == "uz":
            text = f"""
📊 <b>BATAFSIL MA'LUMOT</b>

🆔 Ariza ID: #{message['id']}
📌 Turi: {message['type']}
👤 Mijoz: {message['from']}
📱 Telefon: {message['phone']}
📍 Manzil: {message['address']}
💰 Tarif: {message['tariff']}

⏰ Yaratilgan: {message['time'].strftime('%Y-%m-%d %H:%M')}
{get_priority_emoji(message['priority'])} Muhimlik: {message['priority']}
{get_status_emoji(message['status'])} Status: {message['status']}

📝 <b>To'liq xabar:</b>
{message['message']}

📈 <b>Tarix:</b>
• Yaratilgan: {message['time'].strftime('%H:%M')}
• Ko'rilgan: {datetime.now().strftime('%H:%M')}
            """
        else:
            text = f"""
📊 <b>ПОДРОБНАЯ ИНФОРМАЦИЯ</b>

🆔 ID заявки: #{message['id']}
📌 Тип: {message['type']}
👤 Клиент: {message['from']}
📱 Телефон: {message['phone']}
📍 Адрес: {message['address']}
💰 Тариф: {message['tariff']}

⏰ Создано: {message['time'].strftime('%Y-%m-%d %H:%M')}
{get_priority_emoji(message['priority'])} Приоритет: {message['priority']}
{get_status_emoji(message['status'])} Статус: {message['status']}

📝 <b>Полное сообщение:</b>
{message['message']}

📈 <b>История:</b>
• Создано: {message['time'].strftime('%H:%M')}
• Просмотрено: {datetime.now().strftime('%H:%M')}
            """
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga" if lang == "uz" else "⬅️ Назад",
                    callback_data=f"inbox:back_to_message"
                )
            ]
        ])
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    
    async def show_inbox_statistics(callback: CallbackQuery, state: FSMContext):
        """Show inbox statistics"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        stats = MOCK_INBOX_DATA["statistics"]
        
        if lang == "uz":
            text = f"""
📊 <b>INBOX STATISTIKASI</b>

📈 <b>Umumiy ko'rsatkichlar:</b>
├ 📬 Jami: {stats['total']}
├ 🆕 Yangi: {stats['unread']} ({stats['unread']*100//stats['total']}%)
├ 🔴 Shoshilinch: {stats['urgent']} ({stats['urgent']*100//stats['total']}%)
├ ⏳ Kutilmoqda: {stats['pending']} ({stats['pending']*100//stats['total']}%)
├ 🔄 Jarayonda: {stats['in_progress']} ({stats['in_progress']*100//stats['total']}%)
└ ✅ Hal qilingan: {stats['resolved']} ({stats['resolved']*100//stats['total']}%)

📊 <b>Bugungi faollik:</b>
├ 📥 Kelgan: 12
├ 📤 Javob berilgan: 8
├ ✅ Yopilgan: 5
└ 👨‍💼 Yuborilgan: 3

⏰ <b>O'rtacha vaqt:</b>
├ Javob berish: 15 daqiqa
├ Hal qilish: 2 soat
└ Yopish: 4 soat
            """
        else:
            text = f"""
📊 <b>СТАТИСТИКА ВХОДЯЩИХ</b>

📈 <b>Общие показатели:</b>
├ 📬 Всего: {stats['total']}
├ 🆕 Новые: {stats['unread']} ({stats['unread']*100//stats['total']}%)
├ 🔴 Срочные: {stats['urgent']} ({stats['urgent']*100//stats['total']}%)
├ ⏳ В ожидании: {stats['pending']} ({stats['pending']*100//stats['total']}%)
├ 🔄 В процессе: {stats['in_progress']} ({stats['in_progress']*100//stats['total']}%)
└ ✅ Решенные: {stats['resolved']} ({stats['resolved']*100//stats['total']}%)

📊 <b>Сегодняшняя активность:</b>
├ 📥 Получено: 12
├ 📤 Отвечено: 8
├ ✅ Закрыто: 5
└ 👨‍💼 Отправлено: 3

⏰ <b>Среднее время:</b>
├ Ответ: 15 минут
├ Решение: 2 часа
└ Закрытие: 4 часа
            """
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📤 Export" if lang == "uz" else "📤 Экспорт",
                    callback_data="inbox:export_stats"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga" if lang == "uz" else "⬅️ Назад",
                    callback_data="inbox:back_to_list"
                )
            ]
        ])
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    
    async def show_search_menu(callback: CallbackQuery, state: FSMContext):
        """Show search menu"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        if lang == "uz":
            text = """
🔍 <b>XABAR QIDIRISH</b>

Qanday qidirmoqchisiz?
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🆔 ID bo'yicha", callback_data="search:by_id"),
                    InlineKeyboardButton(text="👤 Ism bo'yicha", callback_data="search:by_name")
                ],
                [
                    InlineKeyboardButton(text="📱 Telefon bo'yicha", callback_data="search:by_phone"),
                    InlineKeyboardButton(text="📅 Sana bo'yicha", callback_data="search:by_date")
                ],
                [
                    InlineKeyboardButton(text="⬅️ Orqaga", callback_data="inbox:back_to_list")
                ]
            ])
        else:
            text = """
🔍 <b>ПОИСК СООБЩЕНИЙ</b>

Как искать?
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🆔 По ID", callback_data="search:by_id"),
                    InlineKeyboardButton(text="👤 По имени", callback_data="search:by_name")
                ],
                [
                    InlineKeyboardButton(text="📱 По телефону", callback_data="search:by_phone"),
                    InlineKeyboardButton(text="📅 По дате", callback_data="search:by_date")
                ],
                [
                    InlineKeyboardButton(text="⬅️ Назад", callback_data="inbox:back_to_list")
                ]
            ])
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        
        await state.set_state(ManagerInboxStates.searching)
    
    async def start_reply_process(callback: CallbackQuery, state: FSMContext, message_id: str):
        """Start reply process"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        if lang == "uz":
            text = f"""
💬 <b>XABARGA JAVOB BERISH</b>

Ariza ID: #{message_id}

Javobingizni yozing va yuboring:
            """
        else:
            text = f"""
💬 <b>ОТВЕТ НА СООБЩЕНИЕ</b>

ID заявки: #{message_id}

Напишите ваш ответ и отправьте:
            """
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == "uz" else "❌ Отмена",
                callback_data=f"inbox:cancel_reply:{message_id}"
            )]
        ])
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        
        await state.set_state(ManagerInboxStates.replying_message)
        await state.update_data(replying_to=message_id)
    
    async def resolve_message(callback: CallbackQuery, state: FSMContext, message_id: str):
        """Mark message as resolved"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        # Update message status
        for msg in MOCK_INBOX_DATA["messages"]:
            if msg["id"] == message_id:
                msg["status"] = "resolved"
                break
        
        # Update statistics
        MOCK_INBOX_DATA["statistics"]["resolved"] += 1
        MOCK_INBOX_DATA["statistics"]["pending"] -= 1
        
        if lang == "uz":
            await callback.answer("✅ Ariza hal qilindi!", show_alert=True)
        else:
            await callback.answer("✅ Заявка решена!", show_alert=True)
        
        # Navigate to next message
        current_index = data.get("current_index", 0)
        messages = data.get("current_messages", MOCK_INBOX_DATA["messages"])
        
        if current_index < len(messages) - 1:
            await navigate_message(callback, state, current_index + 1)
        else:
            await show_inbox_menu(callback, state)
    
    async def change_message_status(callback: CallbackQuery, state: FSMContext, message_id: str):
        """Change message status"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        
        if lang == "uz":
            text = f"""
🔄 <b>STATUS O'ZGARTIRISH</b>

Ariza #{message_id} uchun yangi statusni tanlang:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🆕 Yangi", callback_data=f"status:new:{message_id}"),
                    InlineKeyboardButton(text="⏳ Kutilmoqda", callback_data=f"status:pending:{message_id}")
                ],
                [
                    InlineKeyboardButton(text="🔄 Jarayonda", callback_data=f"status:in_progress:{message_id}"),
                    InlineKeyboardButton(text="✅ Hal qilingan", callback_data=f"status:resolved:{message_id}")
                ],
                [
                    InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"inbox:cancel_status:{message_id}")
                ]
            ])
        else:
            text = f"""
🔄 <b>ИЗМЕНЕНИЕ СТАТУСА</b>

Выберите новый статус для заявки #{message_id}:
            """
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🆕 Новый", callback_data=f"status:new:{message_id}"),
                    InlineKeyboardButton(text="⏳ В ожидании", callback_data=f"status:pending:{message_id}")
                ],
                [
                    InlineKeyboardButton(text="🔄 В процессе", callback_data=f"status:in_progress:{message_id}"),
                    InlineKeyboardButton(text="✅ Решено", callback_data=f"status:resolved:{message_id}")
                ],
                [
                    InlineKeyboardButton(text="❌ Отмена", callback_data=f"inbox:cancel_status:{message_id}")
                ]
            ])
        
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    
    @router.message(ManagerInboxStates.replying_message)
    async def process_reply(message: Message, state: FSMContext):
        """Process reply message"""
        
        data = await state.get_data()
        lang = data.get("language", "uz")
        message_id = data.get("replying_to")
        
        if lang == "uz":
            text = f"""
✅ <b>JAVOB YUBORILDI!</b>

Ariza ID: #{message_id}
Javob: {message.text}
Vaqt: {datetime.now().strftime('%H:%M')}

Mijoz tez orada javobingizni oladi.
            """
        else:
            text = f"""
✅ <b>ОТВЕТ ОТПРАВЛЕН!</b>

ID заявки: #{message_id}
Ответ: {message.text}
Время: {datetime.now().strftime('%H:%M')}

Клиент скоро получит ваш ответ.
            """
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📥 Inbox'ga qaytish" if lang == "uz" else "📥 Вернуться во входящие",
                    callback_data="manager:inbox"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 Asosiy menyu" if lang == "uz" else "🏠 Главное меню",
                    callback_data="manager:back_to_menu"
                )
            ]
        ])
        
        await message.answer(
            text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        
        await state.set_state(ManagerInboxStates.inbox_menu)
    
    return router
