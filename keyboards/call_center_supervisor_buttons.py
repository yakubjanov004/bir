from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Any
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_call_center_supervisor_main_keyboard(lang="uz"):
    """Call center supervisor main keyboard - returns main menu keyboard"""
    return get_call_center_supervisor_main_menu(lang)

def get_call_center_supervisor_main_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Main menu keyboard for call center supervisor"""
    inbox = "📥 Inbox"
    orders = "📝 Buyurtmalar" if lang == 'uz' else "📝 Заказы"
    staff_management = "👥 Xodimlar boshqaruvi" if lang == 'uz' else "👥 Управление персоналом"
    create_connection = "🔌 Ulanish arizasi yaratish" if lang == 'uz' else "🔌 Создать заявку на подключение"
    create_technical = "🔧 Texnik xizmat yaratish" if lang == 'uz' else "🔧 Создать техническую заявку"
    workflow_management = "⚙️ Workflow boshqaruvi" if lang == 'uz' else "⚙️ Управление процессами"
    statistics = "📊 Statistikalar" if lang == 'uz' else "📊 Статистика"
    export = "📤 Export" if lang == 'uz' else "📤 Экспорт"
    feedback = "⭐️ Fikr-mulohaza" if lang == 'uz' else "⭐️ Обратная связь"
    change_lang = "🌐 Tilni o'zgartirish" if lang == 'uz' else "🌐 Изменить язык"
    main_menu = "🏠 Bosh menyu" if lang == 'uz' else "🏠 Главное меню"
    
    keyboard = [
        [KeyboardButton(text=inbox)],
        [KeyboardButton(text=orders)],
        [KeyboardButton(text=staff_management)],
        [KeyboardButton(text=create_connection), KeyboardButton(text=create_technical)],
        [KeyboardButton(text=workflow_management)],
        [KeyboardButton(text=statistics), KeyboardButton(text=export)],
        [KeyboardButton(text=feedback)],
        [KeyboardButton(text=change_lang)],
        [KeyboardButton(text=main_menu)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_quick_actions_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Quick actions menu for call center supervisor"""
    new_orders = "🆕 Yangi buyurtmalar" if lang == 'uz' else "🆕 Новые заказы"
    urgent_tasks = "🚨 Shoshilinch vazifalar" if lang == 'uz' else "🚨 Срочные задачи"
    staff_status = "👥 Xodimlar holati" if lang == 'uz' else "👥 Статус персонала"
    daily_report = "📊 Kunlik hisobot" if lang == 'uz' else "📊 Дневной отчет"
    notifications = "🔔 Bildirishnomalar" if lang == 'uz' else "🔔 Уведомления"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=new_orders), KeyboardButton(text=urgent_tasks)],
        [KeyboardButton(text=staff_status), KeyboardButton(text=daily_report)],
        [KeyboardButton(text=notifications)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_staff_management_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Staff management inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="👥 Xodimlar ro'yxati" if lang == 'uz' else "👥 Список персонала",
                callback_data="ccs_staff_list"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Xodimlar statistikasi" if lang == 'uz' else "📊 Статистика персонала",
                callback_data="ccs_staff_stats"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Vazifalar tayinlash" if lang == 'uz' else "📋 Назначить задачи",
                callback_data="ccs_assign_tasks"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔄 Buyurtmalarni qayta tayinlash" if lang == 'uz' else "🔄 Переназначить заказы",
                callback_data="ccs_reassign_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_order_management_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Order management inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📋 Yangi buyurtmalar" if lang == 'uz' else "📋 Новые заказы",
                callback_data="ccs_new_orders"
            ),
            InlineKeyboardButton(
                text="⏳ Jarayondagi" if lang == 'uz' else "⏳ В процессе",
                callback_data="ccs_in_progress_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные",
                callback_data="ccs_completed_orders"
            ),
            InlineKeyboardButton(
                text="❌ Bekor qilingan" if lang == 'uz' else "❌ Отмененные",
                callback_data="ccs_cancelled_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔴 Muammoli" if lang == 'uz' else "🔴 Проблемные",
                callback_data="ccs_problem_orders"
            ),
            InlineKeyboardButton(
                text="⬆️ Yuqoriga ko'tarilgan" if lang == 'uz' else "⬆️ Эскалированные",
                callback_data="ccs_escalated_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔍 Qidirish" if lang == 'uz' else "🔍 Поиск",
                callback_data="ccs_search_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_client_search_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Client search method selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📱 Telefon" if lang == 'uz' else "📱 Телефон",
                callback_data="ccs_client_search_phone"
            ),
            InlineKeyboardButton(
                text="👤 Ism" if lang == 'uz' else "👤 Имя",
                callback_data="ccs_client_search_name"
            )
        ],
        [
            InlineKeyboardButton(
                text="🆔 ID" if lang == 'uz' else "🆔 ID",
                callback_data="ccs_client_search_id"
            ),
            InlineKeyboardButton(
                text="➕ Yangi mijoz" if lang == 'uz' else "➕ Новый клиент",
                callback_data="ccs_client_search_new"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="ccs_cancel_application_creation"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_type_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Application type selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔌 Ulanish arizasi" if lang == 'uz' else "🔌 Заявка на подключение",
                callback_data="ccs_app_type_connection"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔧 Texnik xizmat" if lang == 'uz' else "🔧 Техническое обслуживание",
                callback_data="ccs_app_type_technical"
            )
        ],
        [
            InlineKeyboardButton(
                text="📞 Qo'ng'iroq markazi" if lang == 'uz' else "📞 Колл-центр",
                callback_data="ccs_app_type_call_center"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="ccs_cancel_application_creation"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_order_action_menu(order_id: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Order action menu for supervisor"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="👤 Tayinlash" if lang == 'uz' else "👤 Назначить",
                callback_data=f"ccs_assign_order_{order_id}"
            ),
            InlineKeyboardButton(
                text="📝 Tahrirlash" if lang == 'uz' else "📝 Редактировать",
                callback_data=f"ccs_edit_order_{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬆️ Yuqoriga ko'tarish" if lang == 'uz' else "⬆️ Эскалировать",
                callback_data=f"ccs_escalate_order_{order_id}"
            ),
            InlineKeyboardButton(
                text="🔄 Status o'zgartirish" if lang == 'uz' else "🔄 Изменить статус",
                callback_data=f"ccs_change_status_{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Batafsil" if lang == 'uz' else "📋 Подробности",
                callback_data=f"ccs_order_details_{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_operator_selection_keyboard(operators: List[Dict[str, Any]], order_id: int) -> InlineKeyboardMarkup:
    """Creates a keyboard to select an operator for assignment."""
    builder = InlineKeyboardBuilder()
    for operator in operators:
        button_text = f"{operator['full_name']}"
        callback_data = f"assign_operator:{order_id}:{operator['id']}"
        builder.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    
    builder.adjust(2)  # Adjust to show 2 operators per row
    builder.row(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"view_order:{order_id}:0"))
    return builder.as_markup()


def get_staff_assignment_menu(operators: list, order_id: int, lang: str = 'uz'):
    """Alias for get_operator_selection_keyboard for backward compatibility."""
    return get_operator_selection_keyboard(operators, order_id)


def get_status_change_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Status change selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🆕 Yangi" if lang == 'uz' else "🆕 Новый",
                callback_data="ccs_status_new"
            ),
            InlineKeyboardButton(
                text="⏳ Jarayonda" if lang == 'uz' else "⏳ В процессе",
                callback_data="ccs_status_in_progress"
            )
        ],
        [
            InlineKeyboardButton(
                text="⏸️ To'xtatilgan" if lang == 'uz' else "⏸️ Приостановлен",
                callback_data="ccs_status_on_hold"
            ),
            InlineKeyboardButton(
                text="✅ Bajarilgan" if lang == 'uz' else "✅ Выполнен",
                callback_data="ccs_status_completed"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilingan" if lang == 'uz' else "❌ Отменен",
                callback_data="ccs_status_cancelled"
            ),
            InlineKeyboardButton(
                text="🔴 Muammo" if lang == 'uz' else "🔴 Проблема",
                callback_data="ccs_status_issue"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="ccs_cancel_status_change"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_inbox_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Inbox management inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📋 Yangi arizalar" if lang == 'uz' else "📋 Новые заявки",
                callback_data="ccs_inbox_new"
            ),
            InlineKeyboardButton(
                text="🔴 Muammoli" if lang == 'uz' else "🔴 Проблемные",
                callback_data="ccs_inbox_issues"
            )
        ],
        [
            InlineKeyboardButton(
                text="⏳ Kutilayotgan" if lang == 'uz' else "⏳ Ожидающие",
                callback_data="ccs_inbox_pending"
            ),
            InlineKeyboardButton(
                text="⬆️ Yuqoriga ko'tarilgan" if lang == 'uz' else "⬆️ Эскалированные",
                callback_data="ccs_inbox_escalated"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔄 Yangilash" if lang == 'uz' else "🔄 Обновить",
                callback_data="ccs_inbox_refresh"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_statistics_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Statistics menu inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📊 Bugungi statistika" if lang == 'uz' else "📊 Статистика за сегодня",
                callback_data="ccs_stats_daily"
            )
        ],
        [
            InlineKeyboardButton(
                text="📈 Haftalik hisobot" if lang == 'uz' else "📈 Недельный отчет",
                callback_data="ccs_stats_weekly"
            )
        ],
        [
            InlineKeyboardButton(
                text="📉 Oylik hisobot" if lang == 'uz' else "📉 Месячный отчет",
                callback_data="ccs_stats_monthly"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Xodimlar samaradorligi" if lang == 'uz' else "👥 Эффективность персонала",
                callback_data="ccs_stats_staff_performance"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Buyurtmalar tahlili" if lang == 'uz' else "📋 Анализ заказов",
                callback_data="ccs_stats_orders_analysis"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_order_list_keyboard(orders: List[Dict[str, Any]], page: int = 0, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Generate keyboard for order list with pagination"""
    keyboard = []
    
    # Show orders (5 per page)
    start_idx = page * 5
    end_idx = min(start_idx + 5, len(orders))
    
    for i in range(start_idx, end_idx):
        order = orders[i]
        status_emoji = _get_status_emoji(order['status'])
        text = f"{status_emoji} #{order['id']} - {order.get('client_name', 'N/A')[:20]}"
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"ccs_view_order_{order['id']}"
            )
        ])
    
    # Pagination buttons
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущая",
                callback_data=f"ccs_orders_page_{page-1}"
            )
        )
    
    if end_idx < len(orders):
        nav_buttons.append(
            InlineKeyboardButton(
                text="Keyingi ➡️" if lang == 'uz' else "Следующая ➡️",
                callback_data=f"ccs_orders_page_{page+1}"
            )
        )
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Close button
    keyboard.append([
        InlineKeyboardButton(
            text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
            callback_data="ccs_close_menu"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_staff_list_keyboard(staff_list: List[Dict[str, Any]], lang: str = 'uz') -> InlineKeyboardMarkup:
    """Generate keyboard for staff list"""
    keyboard = []
    
    for staff in staff_list[:10]:  # Limit to 10 staff members
        status_emoji = "✅" if staff.get('is_active', True) else "❌"
        role_emoji = "📞" if staff['role'] == 'call_center' else "🔧"
        
        text = f"{status_emoji} {role_emoji} {staff['full_name']}"
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"ccs_view_staff_{staff['id']}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
            callback_data="ccs_close_menu"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_client_selection_keyboard(clients: List[Dict[str, Any]], lang: str = 'uz') -> InlineKeyboardMarkup:
    """Generate keyboard for client selection"""
    keyboard = []
    
    for client in clients[:8]:  # Limit to 8 clients
        text = f"👤 {client['full_name']} - {client.get('phone', 'N/A')}"
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"ccs_select_client_{client['id']}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            text="🔍 Boshqa qidirish" if lang == 'uz' else "🔍 Другой поиск",
            callback_data="ccs_search_again"
        )
    ])
    
    keyboard.append([
        InlineKeyboardButton(
            text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
            callback_data="ccs_cancel_application_creation"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_priority_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Application priority selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔴 Yuqori" if lang == 'uz' else "🔴 Высокий",
                callback_data="ccs_priority_high"
            ),
            InlineKeyboardButton(
                text="🟡 O'rta" if lang == 'uz' else "🟡 Средний",
                callback_data="ccs_priority_medium"
            )
        ],
        [
            InlineKeyboardButton(
                text="🟢 Past" if lang == 'uz' else "🟢 Низкий",
                callback_data="ccs_priority_low"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="ccs_cancel_application_creation"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_back_to_inbox_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    """Creates a keyboard with a button to go back to the inbox."""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="⬅️ Orqaga", callback_data=f"back_to_inbox:{page}"))
    return builder.as_markup()


def get_application_confirmation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Application confirmation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="✅ Tasdiqlash" if lang == 'uz' else "✅ Подтвердить",
                callback_data="ccs_confirm_application"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Tahrirlash" if lang == 'uz' else "📝 Редактировать",
                callback_data="ccs_edit_application"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="ccs_cancel_application_creation"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_order_search_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Order search options keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🆔 ID bo'yicha" if lang == 'uz' else "🆔 По ID",
                callback_data="ccs_search_by_id"
            ),
            InlineKeyboardButton(
                text="👤 Mijoz bo'yicha" if lang == 'uz' else "👤 По клиенту",
                callback_data="ccs_search_by_client"
            )
        ],
        [
            InlineKeyboardButton(
                text="📅 Sana bo'yicha" if lang == 'uz' else "📅 По дате",
                callback_data="ccs_search_by_date"
            ),
            InlineKeyboardButton(
                text="📊 Status bo'yicha" if lang == 'uz' else "📊 По статусу",
                callback_data="ccs_search_by_status"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="ccs_cancel_search"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_feedback_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Feedback options keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📝 Fikr yozish" if lang == 'uz' else "📝 Написать отзыв",
                callback_data="ccs_write_feedback"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Fikrlarni ko'rish" if lang == 'uz' else "📊 Просмотр отзывов",
                callback_data="ccs_view_feedback"
            )
        ],
        [
            InlineKeyboardButton(
                text="⭐ Baholash" if lang == 'uz' else "⭐ Оценить",
                callback_data="ccs_rate_service"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Language selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🇺🇿 O'zbekcha",
                callback_data="ccs_lang_uz"
            ),
            InlineKeyboardButton(
                text="🇷🇺 Русский",
                callback_data="ccs_lang_ru"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data="ccs_cancel_lang_change"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_workflow_management_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Workflow management menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📊 Jarayon monitoringi" if lang == 'uz' else "📊 Мониторинг процессов",
                callback_data="ccs_workflow_monitoring"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔧 Workflow optimizatsiyasi" if lang == 'uz' else "🔧 Оптимизация процессов",
                callback_data="ccs_workflow_optimization"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Jamoa koordinatsiyasi" if lang == 'uz' else "👥 Координация команды",
                callback_data="ccs_workflow_coordination"
            )
        ],
        [
            InlineKeyboardButton(
                text="📈 Workflow analitikasi" if lang == 'uz' else "📈 Аналитика процессов",
                callback_data="ccs_workflow_analytics"
            )
        ],
        [
            InlineKeyboardButton(
                text="🤖 Avtomatlashtirish" if lang == 'uz' else "🤖 Автоматизация",
                callback_data="ccs_workflow_automation"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_process_monitoring_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Process monitoring menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📊 Real vaqt monitoring" if lang == 'uz' else "📊 Мониторинг в реальном времени",
                callback_data="ccs_monitor_realtime"
            )
        ],
        [
            InlineKeyboardButton(
                text="🚧 Bottleneck tahlili" if lang == 'uz' else "🚧 Анализ узких мест",
                callback_data="ccs_monitor_bottlenecks"
            )
        ],
        [
            InlineKeyboardButton(
                text="📈 Samaradorlik monitoring" if lang == 'uz' else "📈 Мониторинг эффективности",
                callback_data="ccs_monitor_performance"
            )
        ],
        [
            InlineKeyboardButton(
                text="🚨 Workflow ogohlantirishlari" if lang == 'uz' else "🚨 Предупреждения процессов",
                callback_data="ccs_monitor_alerts"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
                callback_data="ccs_workflow_monitoring"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_workflow_optimization_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Workflow optimization menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="⚖️ Ish yukini taqsimlash" if lang == 'uz' else "⚖️ Распределение нагрузки",
                callback_data="ccs_optimize_load"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎯 Muhimlik optimizatsiyasi" if lang == 'uz' else "🎯 Оптимизация приоритетов",
                callback_data="ccs_optimize_priority"
            )
        ],
        [
            InlineKeyboardButton(
                text="📦 Resurs taqsimoti" if lang == 'uz' else "📦 Распределение ресурсов",
                callback_data="ccs_optimize_resources"
            )
        ],
        [
            InlineKeyboardButton(
                text="📅 Jadval optimizatsiyasi" if lang == 'uz' else "📅 Оптимизация расписания",
                callback_data="ccs_optimize_schedule"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
                callback_data="ccs_workflow_optimization"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_team_coordination_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Team coordination menu keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📋 Vazifa taqsimoti" if lang == 'uz' else "📋 Распределение задач",
                callback_data="ccs_coord_tasks"
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Muloqot optimizatsiyasi" if lang == 'uz' else "💬 Оптимизация коммуникации",
                callback_data="ccs_coord_communication"
            )
        ],
        [
            InlineKeyboardButton(
                text="🤝 Jamoaviy ishlash" if lang == 'uz' else "🤝 Командная работа",
                callback_data="ccs_coord_teamwork"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Jamoa samaradorligi" if lang == 'uz' else "📊 Эффективность команды",
                callback_data="ccs_coord_efficiency"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
                callback_data="ccs_workflow_coordination"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_advanced_staff_management_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Advanced staff management inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="👥 Xodimlar ro'yxati" if lang == 'uz' else "👥 Список персонала",
                callback_data="ccs_staff_list"
            ),
            InlineKeyboardButton(
                text="📊 Samaradorlik" if lang == 'uz' else "📊 Производительность",
                callback_data="ccs_staff_performance"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Vazifalar tayinlash" if lang == 'uz' else "📋 Назначить задачи",
                callback_data="ccs_assign_tasks"
            ),
            InlineKeyboardButton(
                text="🔄 Qayta tayinlash" if lang == 'uz' else "🔄 Переназначить",
                callback_data="ccs_reassign_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚖️ Ish yukini taqsimlash" if lang == 'uz' else "⚖️ Распределение нагрузки",
                callback_data="ccs_workload_balance"
            )
        ],
        [
            InlineKeyboardButton(
                text="📈 Xodim tahlili" if lang == 'uz' else "📈 Анализ сотрудников",
                callback_data="ccs_staff_analytics"
            ),
            InlineKeyboardButton(
                text="🎯 KPI ko'rsatkichlari" if lang == 'uz' else "🎯 KPI показатели",
                callback_data="ccs_staff_kpi"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔔 Xodim bildirishnomalari" if lang == 'uz' else "🔔 Уведомления персонала",
                callback_data="ccs_staff_notifications"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_advanced_order_management_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Advanced order management inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📋 Yangi" if lang == 'uz' else "📋 Новые",
                callback_data="ccs_new_orders"
            ),
            InlineKeyboardButton(
                text="⏳ Jarayonda" if lang == 'uz' else "⏳ В процессе",
                callback_data="ccs_in_progress_orders"
            ),
            InlineKeyboardButton(
                text="✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные",
                callback_data="ccs_completed_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔴 Muammoli" if lang == 'uz' else "🔴 Проблемные",
                callback_data="ccs_problem_orders"
            ),
            InlineKeyboardButton(
                text="⬆️ Eskalatsiya" if lang == 'uz' else "⬆️ Эскалация",
                callback_data="ccs_escalated_orders"
            ),
            InlineKeyboardButton(
                text="❌ Bekor qilingan" if lang == 'uz' else "❌ Отмененные",
                callback_data="ccs_cancelled_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="🚨 Shoshilinch" if lang == 'uz' else "🚨 Срочные",
                callback_data="ccs_urgent_orders"
            ),
            InlineKeyboardButton(
                text="⏰ Kechikkan" if lang == 'uz' else "⏰ Просроченные",
                callback_data="ccs_overdue_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔍 Qidirish" if lang == 'uz' else "🔍 Поиск",
                callback_data="ccs_search_orders"
            ),
            InlineKeyboardButton(
                text="📊 Tahlil" if lang == 'uz' else "📊 Анализ",
                callback_data="ccs_orders_analytics"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔄 Yangilash" if lang == 'uz' else "🔄 Обновить",
                callback_data="ccs_refresh_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_priority_management_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Priority management keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔴 Yuqori muhimlik" if lang == 'uz' else "🔴 Высокий приоритет",
                callback_data="ccs_priority_high_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="🟡 O'rta muhimlik" if lang == 'uz' else "🟡 Средний приоритет",
                callback_data="ccs_priority_medium_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="🟢 Past muhimlik" if lang == 'uz' else "🟢 Низкий приоритет",
                callback_data="ccs_priority_low_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎯 Muhimlikni o'zgartirish" if lang == 'uz' else "🎯 Изменить приоритет",
                callback_data="ccs_change_priority"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_notification_management_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Notification management keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔔 Yangi bildirishnomalar" if lang == 'uz' else "🔔 Новые уведомления",
                callback_data="ccs_new_notifications"
            )
        ],
        [
            InlineKeyboardButton(
                text="📨 Xodimga xabar yuborish" if lang == 'uz' else "📨 Отправить сообщение сотруднику",
                callback_data="ccs_send_staff_message"
            )
        ],
        [
            InlineKeyboardButton(
                text="📢 Umumiy e'lon" if lang == 'uz' else "📢 Общее объявление",
                callback_data="ccs_broadcast_message"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚠️ Ogohlantirish yuborish" if lang == 'uz' else "⚠️ Отправить предупреждение",
                callback_data="ccs_send_warning"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Bildirishnomalar tarixi" if lang == 'uz' else "📋 История уведомлений",
                callback_data="ccs_notifications_history"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_analytics_dashboard_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Analytics dashboard keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📊 Bugungi hisobot" if lang == 'uz' else "📊 Сегодняшний отчет",
                callback_data="ccs_analytics_today"
            ),
            InlineKeyboardButton(
                text="📈 Haftalik trend" if lang == 'uz' else "📈 Недельный тренд",
                callback_data="ccs_analytics_weekly"
            )
        ],
        [
            InlineKeyboardButton(
                text="📉 Oylik tahlil" if lang == 'uz' else "📉 Месячный анализ",
                callback_data="ccs_analytics_monthly"
            ),
            InlineKeyboardButton(
                text="🎯 KPI dashboard" if lang == 'uz' else "🎯 KPI панель",
                callback_data="ccs_analytics_kpi"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Jamoa samaradorligi" if lang == 'uz' else "👥 Эффективность команды",
                callback_data="ccs_analytics_team"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔍 Batafsil tahlil" if lang == 'uz' else "🔍 Детальный анализ",
                callback_data="ccs_analytics_detailed"
            ),
            InlineKeyboardButton(
                text="📋 Hisobot eksport" if lang == 'uz' else "📋 Экспорт отчета",
                callback_data="ccs_analytics_export"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_client_management_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Client management keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="👤 Mijoz qidirish" if lang == 'uz' else "👤 Поиск клиента",
                callback_data="ccs_client_search"
            ),
            InlineKeyboardButton(
                text="➕ Yangi mijoz" if lang == 'uz' else "➕ Новый клиент",
                callback_data="ccs_client_new"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Mijoz tarixi" if lang == 'uz' else "📋 История клиента",
                callback_data="ccs_client_history"
            ),
            InlineKeyboardButton(
                text="📞 Qo'ng'iroqlar tarixi" if lang == 'uz' else "📞 История звонков",
                callback_data="ccs_client_calls"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Mijoz ma'lumotlari" if lang == 'uz' else "📝 Данные клиента",
                callback_data="ccs_client_info"
            ),
            InlineKeyboardButton(
                text="⭐ Mijoz baholari" if lang == 'uz' else "⭐ Оценки клиента",
                callback_data="ccs_client_ratings"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_quick_filters_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Quick filters keyboard for orders"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🕐 Bugun yaratilgan" if lang == 'uz' else "🕐 Созданные сегодня",
                callback_data="ccs_filter_today"
            )
        ],
        [
            InlineKeyboardButton(
                text="🚨 Shoshilinch" if lang == 'uz' else "🚨 Срочные",
                callback_data="ccs_filter_urgent"
            ),
            InlineKeyboardButton(
                text="⏰ Kechikkan" if lang == 'uz' else "⏰ Просроченные",
                callback_data="ccs_filter_overdue"
            )
        ],
        [
            InlineKeyboardButton(
                text="👤 Tayinlanmagan" if lang == 'uz' else "👤 Неназначенные",
                callback_data="ccs_filter_unassigned"
            ),
            InlineKeyboardButton(
                text="🔄 Qayta ishlash" if lang == 'uz' else "🔄 На доработке",
                callback_data="ccs_filter_rework"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔍 Barchasi" if lang == 'uz' else "🔍 Все",
                callback_data="ccs_filter_all"
            ),
            InlineKeyboardButton(
                text="🗂️ Filtrlarni tozalash" if lang == 'uz' else "🗂️ Очистить фильтры",
                callback_data="ccs_filter_clear"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_bulk_actions_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Bulk actions keyboard for multiple orders"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="👥 Ommaviy tayinlash" if lang == 'uz' else "👥 Массовое назначение",
                callback_data="ccs_bulk_assign"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔄 Status o'zgartirish" if lang == 'uz' else "🔄 Изменить статус",
                callback_data="ccs_bulk_status"
            ),
            InlineKeyboardButton(
                text="🎯 Muhimlik o'zgartirish" if lang == 'uz' else "🎯 Изменить приоритет",
                callback_data="ccs_bulk_priority"
            )
        ],
        [
            InlineKeyboardButton(
                text="📨 Ommaviy xabar" if lang == 'uz' else "📨 Массовое сообщение",
                callback_data="ccs_bulk_message"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Hisobot yaratish" if lang == 'uz' else "📋 Создать отчет",
                callback_data="ccs_bulk_report"
            ),
            InlineKeyboardButton(
                text="📤 Eksport qilish" if lang == 'uz' else "📤 Экспортировать",
                callback_data="ccs_bulk_export"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_supervisor_settings_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Supervisor settings keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔔 Bildirishnoma sozlamalari" if lang == 'uz' else "🔔 Настройки уведомлений",
                callback_data="ccs_settings_notifications"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Dashboard sozlamalari" if lang == 'uz' else "📊 Настройки панели",
                callback_data="ccs_settings_dashboard"
            )
        ],
        [
            InlineKeyboardButton(
                text="⏰ Ish vaqti sozlamalari" if lang == 'uz' else "⏰ Настройки рабочего времени",
                callback_data="ccs_settings_worktime"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎯 KPI sozlamalari" if lang == 'uz' else "🎯 Настройки KPI",
                callback_data="ccs_settings_kpi"
            )
        ],
        [
            InlineKeyboardButton(
                text="🌐 Til sozlamalari" if lang == 'uz' else "🌐 Языковые настройки",
                callback_data="ccs_settings_language"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_order_details_actions_keyboard(order_id: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Detailed order actions keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="👤 Tayinlash" if lang == 'uz' else "👤 Назначить",
                callback_data=f"ccs_assign_order_{order_id}"
            ),
            InlineKeyboardButton(
                text="🔄 Status" if lang == 'uz' else "🔄 Статус",
                callback_data=f"ccs_change_status_{order_id}"
            ),
            InlineKeyboardButton(
                text="🎯 Muhimlik" if lang == 'uz' else "🎯 Приоритет",
                callback_data=f"ccs_change_priority_{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Tahrirlash" if lang == 'uz' else "📝 Редактировать",
                callback_data=f"ccs_edit_order_{order_id}"
            ),
            InlineKeyboardButton(
                text="💬 Izoh qo'shish" if lang == 'uz' else "💬 Добавить комментарий",
                callback_data=f"ccs_add_comment_{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬆️ Eskalatsiya" if lang == 'uz' else "⬆️ Эскалация",
                callback_data=f"ccs_escalate_order_{order_id}"
            ),
            InlineKeyboardButton(
                text="📞 Mijozga qo'ng'iroq" if lang == 'uz' else "📞 Позвонить клиенту",
                callback_data=f"ccs_call_client_{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Tarix" if lang == 'uz' else "📋 История",
                callback_data=f"ccs_order_history_{order_id}"
            ),
            InlineKeyboardButton(
                text="📄 Hisobot" if lang == 'uz' else "📄 Отчет",
                callback_data=f"ccs_order_report_{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
                callback_data="ccs_back_to_orders"
            ),
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_supervisor_dashboard_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Dashboard menu for call center supervisor"""
    overview = "📊 Umumiy ko'rinish" if lang == 'uz' else "📊 Обзор"
    today_tasks = "📋 Bugungi vazifalar" if lang == 'uz' else "📋 Задачи на сегодня"
    team_status = "👥 Jamoa holati" if lang == 'uz' else "👥 Статус команды"
    urgent_items = "🚨 Shoshilinch" if lang == 'uz' else "🚨 Срочные"
    performance = "📈 Samaradorlik" if lang == 'uz' else "📈 Производительность"
    reports = "📄 Hisobotlar" if lang == 'uz' else "📄 Отчеты"
    settings = "⚙️ Sozlamalar" if lang == 'uz' else "⚙️ Настройки"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=overview)],
        [KeyboardButton(text=today_tasks), KeyboardButton(text=team_status)],
        [KeyboardButton(text=urgent_items), KeyboardButton(text=performance)],
        [KeyboardButton(text=reports), KeyboardButton(text=settings)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_staff_actions_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Staff actions menu for call center supervisor"""
    view_staff = "👥 Xodimlarni ko'rish" if lang == 'uz' else "👥 Просмотр персонала"
    assign_tasks = "📋 Vazifa berish" if lang == 'uz' else "📋 Назначить задачу"
    performance_review = "📊 Samaradorlik baholash" if lang == 'uz' else "📊 Оценка производительности"
    send_message = "💬 Xabar yuborish" if lang == 'uz' else "💬 Отправить сообщение"
    schedule_meeting = "📅 Uchrashuv belgilash" if lang == 'uz' else "📅 Назначить встречу"
    training = "🎓 O'qitish" if lang == 'uz' else "🎓 Обучение"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=view_staff), KeyboardButton(text=assign_tasks)],
        [KeyboardButton(text=performance_review), KeyboardButton(text=send_message)],
        [KeyboardButton(text=schedule_meeting), KeyboardButton(text=training)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_orders_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Orders menu for call center supervisor"""
    my_orders = "📋 Mening buyurtmalarim" if lang == 'uz' else "📋 Мои заказы"
    new_orders = "🆕 Yangi buyurtmalar" if lang == 'uz' else "🆕 Новые заказы"
    in_progress = "⏳ Jarayondagi" if lang == 'uz' else "⏳ В процессе"
    completed = "✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные"
    pending_review = "👁️ Ko'rib chiqilmoqda" if lang == 'uz' else "👁️ На рассмотрении"
    search_orders = "🔍 Buyurtma qidirish" if lang == 'uz' else "🔍 Поиск заказов"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=my_orders), KeyboardButton(text=new_orders)],
        [KeyboardButton(text=in_progress), KeyboardButton(text=completed)],
        [KeyboardButton(text=pending_review), KeyboardButton(text=search_orders)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_order_actions_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Order actions menu for call center supervisor"""
    new_orders = "🆕 Yangi buyurtmalar" if lang == 'uz' else "🆕 Новые заказы"
    assign_orders = "👤 Buyurtma tayinlash" if lang == 'uz' else "👤 Назначить заказ"
    track_progress = "📈 Jarayonni kuzatish" if lang == 'uz' else "📈 Отслеживание прогресса"
    escalate = "⬆️ Yuqoriga ko'tarish" if lang == 'uz' else "⬆️ Эскалация"
    quality_check = "✅ Sifat nazorati" if lang == 'uz' else "✅ Контроль качества"
    reports = "📊 Hisobotlar" if lang == 'uz' else "📊 Отчеты"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=new_orders), KeyboardButton(text=assign_orders)],
        [KeyboardButton(text=track_progress), KeyboardButton(text=escalate)],
        [KeyboardButton(text=quality_check), KeyboardButton(text=reports)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_client_service_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Client service menu for call center supervisor"""
    search_client = "🔍 Mijoz qidirish" if lang == 'uz' else "🔍 Поиск клиента"
    client_history = "📋 Mijoz tarixi" if lang == 'uz' else "📋 История клиента"
    create_request = "➕ Ariza yaratish" if lang == 'uz' else "➕ Создать заявку"
    follow_up = "📞 Kuzatuv qo'ng'iroqi" if lang == 'uz' else "📞 Контрольный звонок"
    complaints = "⚠️ Shikoyatlar" if lang == 'uz' else "⚠️ Жалобы"
    feedback = "⭐ Fikr-mulohaza" if lang == 'uz' else "⭐ Обратная связь"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=search_client), KeyboardButton(text=client_history)],
        [KeyboardButton(text=create_request), KeyboardButton(text=follow_up)],
        [KeyboardButton(text=complaints), KeyboardButton(text=feedback)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_analytics_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Analytics menu for call center supervisor"""
    daily_stats = "📊 Kunlik statistika" if lang == 'uz' else "📊 Дневная статистика"
    weekly_report = "📈 Haftalik hisobot" if lang == 'uz' else "📈 Недельный отчет"
    monthly_analysis = "📉 Oylik tahlil" if lang == 'uz' else "📉 Месячный анализ"
    team_performance = "👥 Jamoa samaradorligi" if lang == 'uz' else "👥 Производительность команды"
    kpi_dashboard = "🎯 KPI dashboard" if lang == 'uz' else "🎯 KPI панель"
    export_data = "📤 Ma'lumot eksport" if lang == 'uz' else "📤 Экспорт данных"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=daily_stats), KeyboardButton(text=weekly_report)],
        [KeyboardButton(text=monthly_analysis), KeyboardButton(text=team_performance)],
        [KeyboardButton(text=kpi_dashboard), KeyboardButton(text=export_data)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_workflow_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Workflow menu for call center supervisor"""
    process_monitor = "📊 Jarayon monitoring" if lang == 'uz' else "📊 Мониторинг процессов"
    optimize_workflow = "🔧 Workflow optimallashtirish" if lang == 'uz' else "🔧 Оптимизация процессов"
    team_coordination = "👥 Jamoa koordinatsiyasi" if lang == 'uz' else "👥 Координация команды"
    automation = "🤖 Avtomatlashtirish" if lang == 'uz' else "🤖 Автоматизация"
    bottleneck_analysis = "🚧 Bottleneck tahlili" if lang == 'uz' else "🚧 Анализ узких мест"
    efficiency_metrics = "📈 Samaradorlik ko'rsatkichlari" if lang == 'uz' else "📈 Метрики эффективности"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=process_monitor), KeyboardButton(text=optimize_workflow)],
        [KeyboardButton(text=team_coordination), KeyboardButton(text=automation)],
        [KeyboardButton(text=bottleneck_analysis), KeyboardButton(text=efficiency_metrics)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_communication_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Communication menu for call center supervisor"""
    send_announcement = "📢 E'lon yuborish" if lang == 'uz' else "📢 Отправить объявление"
    team_message = "💬 Jamoa xabari" if lang == 'uz' else "💬 Сообщение команде"
    individual_message = "👤 Shaxsiy xabar" if lang == 'uz' else "👤 Личное сообщение"
    urgent_alert = "🚨 Shoshilinch ogohlantirish" if lang == 'uz' else "🚨 Срочное предупреждение"
    meeting_schedule = "📅 Yig'ilish rejasi" if lang == 'uz' else "📅 Расписание встреч"
    notifications = "🔔 Bildirishnomalar" if lang == 'uz' else "🔔 Уведомления"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=send_announcement), KeyboardButton(text=team_message)],
        [KeyboardButton(text=individual_message), KeyboardButton(text=urgent_alert)],
        [KeyboardButton(text=meeting_schedule), KeyboardButton(text=notifications)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_quality_control_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Quality control menu for call center supervisor"""
    quality_check = "✅ Sifat nazorati" if lang == 'uz' else "✅ Контроль качества"
    call_monitoring = "📞 Qo'ng'iroq monitoring" if lang == 'uz' else "📞 Мониторинг звонков"
    performance_audit = "📊 Samaradorlik auditi" if lang == 'uz' else "📊 Аудит производительности"
    training_needs = "🎓 O'qitish ehtiyojlari" if lang == 'uz' else "🎓 Потребности в обучении"
    feedback_review = "⭐ Fikr-mulohaza ko'rib chiqish" if lang == 'uz' else "⭐ Обзор обратной связи"
    improvement_plan = "📈 Yaxshilash rejasi" if lang == 'uz' else "📈 План улучшений"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=quality_check), KeyboardButton(text=call_monitoring)],
        [KeyboardButton(text=performance_audit), KeyboardButton(text=training_needs)],
        [KeyboardButton(text=feedback_review), KeyboardButton(text=improvement_plan)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_emergency_actions_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Emergency actions menu for call center supervisor"""
    urgent_escalation = "🚨 Shoshilinch eskalatsiya" if lang == 'uz' else "🚨 Срочная эскалация"
    emergency_assignment = "⚡ Favqulodda tayinlash" if lang == 'uz' else "⚡ Экстренное назначение"
    crisis_management = "🆘 Inqiroz boshqaruvi" if lang == 'uz' else "🆘 Управление кризисом"
    priority_override = "🎯 Muhimlikni bekor qilish" if lang == 'uz' else "🎯 Переопределение приоритета"
    emergency_broadcast = "📢 Favqulodda e'lon" if lang == 'uz' else "📢 Экстренное объявление"
    incident_report = "📋 Hodisa hisoboti" if lang == 'uz' else "📋 Отчет об инциденте"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=urgent_escalation), KeyboardButton(text=emergency_assignment)],
        [KeyboardButton(text=crisis_management), KeyboardButton(text=priority_override)],
        [KeyboardButton(text=emergency_broadcast), KeyboardButton(text=incident_report)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_supervisor_tools_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Supervisor tools menu"""
    bulk_operations = "📦 Ommaviy amallar" if lang == 'uz' else "📦 Массовые операции"
    data_export = "📤 Ma'lumot eksport" if lang == 'uz' else "📤 Экспорт данных"
    system_health = "🔧 Tizim salomatligi" if lang == 'uz' else "🔧 Состояние системы"
    backup_restore = "💾 Zaxira nusxa" if lang == 'uz' else "💾 Резервная копия"
    user_management = "👥 Foydalanuvchi boshqaruvi" if lang == 'uz' else "👥 Управление пользователями"
    system_logs = "📋 Tizim jurnallari" if lang == 'uz' else "📋 Системные журналы"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=bulk_operations), KeyboardButton(text=data_export)],
        [KeyboardButton(text=system_health), KeyboardButton(text=backup_restore)],
        [KeyboardButton(text=user_management), KeyboardButton(text=system_logs)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_training_management_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Training management menu"""
    training_schedule = "📅 O'qitish jadvali" if lang == 'uz' else "📅 Расписание обучения"
    skill_assessment = "🎯 Ko'nikma baholash" if lang == 'uz' else "🎯 Оценка навыков"
    training_materials = "📚 O'quv materiallari" if lang == 'uz' else "📚 Учебные материалы"
    certification = "🏆 Sertifikatlashtirish" if lang == 'uz' else "🏆 Сертификация"
    progress_tracking = "📈 Taraqqiyot kuzatuvi" if lang == 'uz' else "📈 Отслеживание прогресса"
    training_feedback = "⭐ O'qitish fikri" if lang == 'uz' else "⭐ Отзывы об обучении"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=training_schedule), KeyboardButton(text=skill_assessment)],
        [KeyboardButton(text=training_materials), KeyboardButton(text=certification)],
        [KeyboardButton(text=progress_tracking), KeyboardButton(text=training_feedback)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Additional inline keyboards for enhanced functionality

def get_real_time_monitoring_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Real-time monitoring keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📊 Jonli dashboard" if lang == 'uz' else "📊 Живая панель",
                callback_data="ccs_live_dashboard"
            ),
            InlineKeyboardButton(
                text="📈 Real vaqt metrikalar" if lang == 'uz' else "📈 Метрики в реальном времени",
                callback_data="ccs_realtime_metrics"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Xodimlar faolligi" if lang == 'uz' else "👥 Активность персонала",
                callback_data="ccs_staff_activity"
            ),
            InlineKeyboardButton(
                text="📞 Qo'ng'iroqlar oqimi" if lang == 'uz' else "📞 Поток звонков",
                callback_data="ccs_call_flow"
            )
        ],
        [
            InlineKeyboardButton(
                text="🚨 Tezkor ogohlantirishlar" if lang == 'uz' else "🚨 Быстрые предупреждения",
                callback_data="ccs_quick_alerts"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔄 Yangilash" if lang == 'uz' else "🔄 Обновить",
                callback_data="ccs_refresh_monitoring"
            ),
            InlineKeyboardButton(
                text="⚙️ Sozlamalar" if lang == 'uz' else "⚙️ Настройки",
                callback_data="ccs_monitoring_settings"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_advanced_search_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Advanced search keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔍 Oddiy qidirish" if lang == 'uz' else "🔍 Простой поиск",
                callback_data="ccs_simple_search"
            ),
            InlineKeyboardButton(
                text="🔎 Kengaytirilgan qidirish" if lang == 'uz' else "🔎 Расширенный поиск",
                callback_data="ccs_advanced_search"
            )
        ],
        [
            InlineKeyboardButton(
                text="📅 Sana oralig'i" if lang == 'uz' else "📅 Диапазон дат",
                callback_data="ccs_date_range_search"
            ),
            InlineKeyboardButton(
                text="👤 Xodim bo'yicha" if lang == 'uz' else "👤 По сотруднику",
                callback_data="ccs_staff_search"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Status bo'yicha" if lang == 'uz' else "📊 По статусу",
                callback_data="ccs_status_search"
            ),
            InlineKeyboardButton(
                text="🎯 Muhimlik bo'yicha" if lang == 'uz' else "🎯 По приоритету",
                callback_data="ccs_priority_search"
            )
        ],
        [
            InlineKeyboardButton(
                text="🏷️ Teglar bo'yicha" if lang == 'uz' else "🏷️ По тегам",
                callback_data="ccs_tag_search"
            ),
            InlineKeyboardButton(
                text="📝 Matn bo'yicha" if lang == 'uz' else "📝 По тексту",
                callback_data="ccs_text_search"
            )
        ],
        [
            InlineKeyboardButton(
                text="💾 Saqlangan qidiruvlar" if lang == 'uz' else "💾 Сохраненные поиски",
                callback_data="ccs_saved_searches"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_escalation_management_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Escalation management keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="⬆️ Yangi eskalatsiya" if lang == 'uz' else "⬆️ Новая эскалация",
                callback_data="ccs_new_escalation"
            ),
            InlineKeyboardButton(
                text="📋 Eskalatsiya tarixi" if lang == 'uz' else "📋 История эскалаций",
                callback_data="ccs_escalation_history"
            )
        ],
        [
            InlineKeyboardButton(
                text="🚨 Shoshilinch eskalatsiya" if lang == 'uz' else "🚨 Срочная эскалация",
                callback_data="ccs_urgent_escalation"
            ),
            InlineKeyboardButton(
                text="📊 Eskalatsiya statistikasi" if lang == 'uz' else "📊 Статистика эскалаций",
                callback_data="ccs_escalation_stats"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Eskalatsiya jamoasi" if lang == 'uz' else "👥 Команда эскалации",
                callback_data="ccs_escalation_team"
            ),
            InlineKeyboardButton(
                text="⚙️ Eskalatsiya qoidalari" if lang == 'uz' else "⚙️ Правила эскалации",
                callback_data="ccs_escalation_rules"
            )
        ],
        [
            InlineKeyboardButton(
                text="📈 Tahlil va hisobot" if lang == 'uz' else "📈 Анализ и отчеты",
                callback_data="ccs_escalation_analysis"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_performance_dashboard_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Performance dashboard keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📊 Umumiy ko'rsatkichlar" if lang == 'uz' else "📊 Общие показатели",
                callback_data="ccs_overall_metrics"
            ),
            InlineKeyboardButton(
                text="👤 Individual samaradorlik" if lang == 'uz' else "👤 Индивидуальная производительность",
                callback_data="ccs_individual_performance"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Jamoa samaradorligi" if lang == 'uz' else "👥 Производительность команды",
                callback_data="ccs_team_performance"
            ),
            InlineKeyboardButton(
                text="📈 Trend tahlili" if lang == 'uz' else "📈 Анализ трендов",
                callback_data="ccs_trend_analysis"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎯 KPI monitoring" if lang == 'uz' else "🎯 Мониторинг KPI",
                callback_data="ccs_kpi_monitoring"
            ),
            InlineKeyboardButton(
                text="📋 Samaradorlik hisoboti" if lang == 'uz' else "📋 Отчет о производительности",
                callback_data="ccs_performance_report"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚠️ Samaradorlik ogohlantirishlari" if lang == 'uz' else "⚠️ Предупреждения о производительности",
                callback_data="ccs_performance_alerts"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔄 Yangilash" if lang == 'uz' else "🔄 Обновить",
                callback_data="ccs_refresh_performance"
            ),
            InlineKeyboardButton(
                text="📤 Eksport" if lang == 'uz' else "📤 Экспорт",
                callback_data="ccs_export_performance"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_language_selection_inline_menu() -> InlineKeyboardMarkup:
    """Language selection inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🇺🇿 O'zbekcha",
                callback_data="ccs_lang_uz"
            ),
            InlineKeyboardButton(
                text="🇷🇺 Русский",
                callback_data="ccs_lang_ru"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data="ccs_cancel_lang_change"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_supervisor_inbox_keyboard(lang='uz'):
    """Generate inbox keyboard for supervisor with locale support"""
    new_messages_text = "🆕 Yangi xabarlar" if lang == "uz" else "🆕 Новые сообщения"
    read_messages_text = "✅ O'qilgan xabarlar" if lang == "uz" else "✅ Прочитанные сообщения"
    urgent_messages_text = "🚨 Shoshilinch xabarlar" if lang == "uz" else "🚨 Срочные сообщения"
    all_messages_text = "📋 Barcha xabarlar" if lang == "uz" else "📋 Все сообщения"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=new_messages_text, callback_data="ccs_inbox_new"),
            InlineKeyboardButton(text=read_messages_text, callback_data="ccs_inbox_read")
        ],
        [
            InlineKeyboardButton(text=urgent_messages_text, callback_data="ccs_inbox_urgent"),
            InlineKeyboardButton(text=all_messages_text, callback_data="ccs_inbox_all")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_ccs_main")
        ]
    ])
    return keyboard

def get_supervisor_back_keyboard(lang='uz'):
    """Supervisor back keyboard"""
    back_text = "🏠 Asosiy menyu" if lang == "uz" else "🏠 Главное меню"
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=back_text)]],
        resize_keyboard=True
    )

# New centralized keyboard functions for call center supervisor module
def get_supervisor_operator_assignment_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Supervisor operator assignment keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="✅ Ha, yuborish" if lang == 'uz' else "✅ Да, отправить",
                callback_data="supervisor_confirm_assign"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="supervisor_back_to_application"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_supervisor_back_to_inbox_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Supervisor back to inbox keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📥 Inbox'ga qaytish" if lang == 'uz' else "📥 Вернуться в inbox",
                callback_data="supervisor_back_to_inbox"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_supervisor_export_types_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Supervisor export types keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📑 Buyurtmalar" if lang == 'uz' else "📑 Заказы",
                callback_data="ccs_export_main_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Statistika" if lang == 'uz' else "📊 Статистика",
                callback_data="ccs_export_main_statistics"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Xodimlar" if lang == 'uz' else "👥 Сотрудники",
                callback_data="ccs_export_main_users"
            )
        ],
        [
            InlineKeyboardButton(
                text="⭐ Fikr-mulohazalar" if lang == 'uz' else "⭐ Отзывы",
                callback_data="ccs_export_main_feedback"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚙️ Workflow" if lang == 'uz' else "⚙️ Процессы",
                callback_data="ccs_export_main_workflow"
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                callback_data="ccs_export_main_back_main"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_supervisor_export_formats_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Supervisor export formats keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="CSV",
                callback_data="ccs_format_main_csv"
            )
        ],
        [
            InlineKeyboardButton(
                text="Excel",
                callback_data="ccs_format_main_xlsx"
            )
        ],
        [
            InlineKeyboardButton(
                text="Word",
                callback_data="ccs_format_main_docx"
            )
        ],
        [
            InlineKeyboardButton(
                text="PDF",
                callback_data="ccs_format_main_pdf"
            )
        ],
        [
            InlineKeyboardButton(
                text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                callback_data="ccs_export_main_back_types"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_supervisor_export_back_types_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Supervisor export back to types keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                callback_data="ccs_export_main_back_types"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_supervisor_feedback_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Supervisor feedback keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📝 Fikr yozish" if lang == 'uz' else "📝 Написать отзыв",
                callback_data="ccs_write_feedback"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Fikrlarni ko'rish" if lang == 'uz' else "📊 Просмотр отзывов",
                callback_data="ccs_view_feedback"
            )
        ],
        [
            InlineKeyboardButton(
                text="⭐ Baholash" if lang == 'uz' else "⭐ Оценить",
                callback_data="ccs_rate_service"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_supervisor_notification_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Supervisor notification keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔔 Yangi bildirishnomalar" if lang == 'uz' else "🔔 Новые уведомления",
                callback_data="ccs_new_notifications"
            )
        ],
        [
            InlineKeyboardButton(
                text="📨 Xodimga xabar yuborish" if lang == 'uz' else "📨 Отправить сообщение сотруднику",
                callback_data="ccs_send_staff_message"
            )
        ],
        [
            InlineKeyboardButton(
                text="📢 Umumiy e'lon" if lang == 'uz' else "📢 Общее объявление",
                callback_data="ccs_broadcast_message"
            )
        ],
        [
            InlineKeyboardButton(
                text="⚠️ Ogohlantirish yuborish" if lang == 'uz' else "⚠️ Отправить предупреждение",
                callback_data="ccs_send_warning"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Bildirishnomalar tarixi" if lang == 'uz' else "📋 История уведомлений",
                callback_data="ccs_notifications_history"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_supervisor_orders_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Supervisor orders keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📋 Yangi buyurtmalar" if lang == 'uz' else "📋 Новые заказы",
                callback_data="ccs_new_orders"
            ),
            InlineKeyboardButton(
                text="⏳ Jarayondagi" if lang == 'uz' else "⏳ В процессе",
                callback_data="ccs_in_progress_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные",
                callback_data="ccs_completed_orders"
            ),
            InlineKeyboardButton(
                text="❌ Bekor qilingan" if lang == 'uz' else "❌ Отмененные",
                callback_data="ccs_cancelled_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔴 Muammoli" if lang == 'uz' else "🔴 Проблемные",
                callback_data="ccs_problem_orders"
            ),
            InlineKeyboardButton(
                text="⬆️ Yuqoriga ko'tarilgan" if lang == 'uz' else "⬆️ Эскалированные",
                callback_data="ccs_escalated_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔍 Qidirish" if lang == 'uz' else "🔍 Поиск",
                callback_data="ccs_search_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_supervisor_application_management_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Supervisor application management keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📋 Yangi arizalar" if lang == 'uz' else "📋 Новые заявки",
                callback_data="ccs_app_new"
            ),
            InlineKeyboardButton(
                text="⏳ Jarayondagi" if lang == 'uz' else "⏳ В процессе",
                callback_data="ccs_app_in_progress"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные",
                callback_data="ccs_app_completed"
            ),
            InlineKeyboardButton(
                text="❌ Bekor qilingan" if lang == 'uz' else "❌ Отмененные",
                callback_data="ccs_app_cancelled"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔍 Qidirish" if lang == 'uz' else "🔍 Поиск",
                callback_data="ccs_app_search"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_supervisor_staff_creation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Supervisor staff creation keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📱 Telefon" if lang == 'uz' else "📱 Телефон",
                callback_data="ccs_client_search_phone"
            ),
            InlineKeyboardButton(
                text="👤 Ism" if lang == 'uz' else "👤 Имя",
                callback_data="ccs_client_search_name"
            )
        ],
        [
            InlineKeyboardButton(
                text="🆔 ID" if lang == 'uz' else "🆔 ID",
                callback_data="ccs_client_search_id"
            ),
            InlineKeyboardButton(
                text="➕ Yangi mijoz" if lang == 'uz' else "➕ Новый клиент",
                callback_data="ccs_client_search_new"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="ccs_cancel_application_creation"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_supervisor_statistics_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Supervisor statistics keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📊 Bugungi statistika" if lang == 'uz' else "📊 Статистика за сегодня",
                callback_data="ccs_stats_daily"
            )
        ],
        [
            InlineKeyboardButton(
                text="📈 Haftalik hisobot" if lang == 'uz' else "📈 Недельный отчет",
                callback_data="ccs_stats_weekly"
            )
        ],
        [
            InlineKeyboardButton(
                text="📉 Oylik hisobot" if lang == 'uz' else "📉 Месячный отчет",
                callback_data="ccs_stats_monthly"
            )
        ],
        [
            InlineKeyboardButton(
                text="👥 Xodimlar samaradorligi" if lang == 'uz' else "👥 Эффективность персонала",
                callback_data="ccs_stats_staff_performance"
            )
        ],
        [
            InlineKeyboardButton(
                text="📋 Buyurtmalar tahlili" if lang == 'uz' else "📋 Анализ заказов",
                callback_data="ccs_stats_orders_analysis"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="ccs_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_supervisor_navigation_keyboard(current_index: int, total_applications: int, application_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Supervisor navigation keyboard"""
    keyboard = []
    
    # Action buttons row
    action_buttons = []
    
    # Assign to operator button
    action_buttons.append(InlineKeyboardButton(
        text="📞 Operator'ga yuborish" if lang == 'uz' else "📞 Отправить оператору",
        callback_data=f"supervisor_assign_operator_{application_id}"
    ))
    
    keyboard.append(action_buttons)
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущая",
            callback_data="supervisor_prev_application"
        ))
    
    # Next button
    if current_index < total_applications - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️" if lang == 'uz' else "Следующая ➡️",
            callback_data="supervisor_next_application"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def _get_status_emoji(status: str) -> str:
    """Get status emoji for order status"""
    status_emojis = {
        'new': '🆕',
        'pending': '⏳',
        'in_progress': '🔄',
        'completed': '✅',
        'cancelled': '❌',
        'urgent': '🚨',
        'high_priority': '⚡',
        'normal_priority': '📋',
        'low_priority': '📝'
    }
    return status_emojis.get(status, '📋')