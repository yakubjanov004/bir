from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters.callback_data import CallbackData
from typing import List, Dict, Any

def get_call_center_main_keyboard(lang="uz"):
    """Call center main keyboard - returns main menu keyboard"""
    return call_center_main_menu_reply(lang)

def call_center_main_menu_reply(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Main menu keyboard for call center operator"""
    inbox = "📥 Inbox"
    orders = "📝 Buyurtmalar" if lang == 'uz' else "📝 Заказы"
    client_search = "🔍 Mijoz qidirish" if lang == 'uz' else "🔍 Поиск клиента"
    create_connection = "🔌 Ulanish arizasi yaratish" if lang == 'uz' else "🔌 Создать заявку на подключение"
    create_technical = "🔧 Texnik xizmat yaratish" if lang == 'uz' else "🔧 Создать техническую заявку"
    call_management = "📞 Qo'ng'iroqlar boshqaruvi" if lang == 'uz' else "📞 Управление звонками"
    statistics = "📊 Statistikalar" if lang == 'uz' else "📊 Статистика"
    feedback = "⭐️ Fikr-mulohaza" if lang == 'uz' else "⭐️ Обратная связь"
    change_lang = "🌐 Tilni o'zgartirish" if lang == 'uz' else "🌐 Изменить язык"
    webapp_text = "🌐 Web ilovasi" if lang == 'uz' else "🌐 Веб-приложение"

    keyboard = [
        [KeyboardButton(text=inbox)],
        [KeyboardButton(text=orders)],
        [KeyboardButton(text=client_search)],
        [KeyboardButton(text=create_connection), KeyboardButton(text=create_technical)],
        [KeyboardButton(text=call_management)],
        [KeyboardButton(text=statistics)],
        [KeyboardButton(text=feedback)],
        [KeyboardButton(text=change_lang)],
        [KeyboardButton(text=webapp_text, web_app=WebAppInfo(url="https://webapp-gamma-three.vercel.app/"))]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_call_center_quick_actions_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Quick actions menu for call center operator"""
    new_calls = "📞 Yangi qo'ng'iroqlar" if lang == 'uz' else "📞 Новые звонки"
    pending_callbacks = "⏰ Qayta qo'ng'iroqlar" if lang == 'uz' else "⏰ Обратные звонки"
    active_orders = "⚡ Faol buyurtmalar" if lang == 'uz' else "⚡ Активные заказы"
    daily_stats = "📊 Kunlik hisobot" if lang == 'uz' else "📊 Дневной отчет"
    client_support = "🆘 Mijoz yordami" if lang == 'uz' else "🆘 Поддержка клиентов"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=new_calls), KeyboardButton(text=pending_callbacks)],
        [KeyboardButton(text=active_orders), KeyboardButton(text=daily_stats)],
        [KeyboardButton(text=client_support)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def new_order_reply_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """New order reply keyboard (only back button)"""
    back = "🔄 Orqaga" if lang == 'uz' else "🔄 Назад"
    keyboard = [
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def client_search_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Client search menu keyboard with search methods"""
    search_by_name = "👤 Ism bo'yicha qidirish" if lang == 'uz' else "👤 Поиск по имени"
    search_by_phone = "📱 Telefon bo'yicha qidirish" if lang == 'uz' else "📱 Поиск по телефону"
    search_by_id = "🆔 ID bo'yicha qidirish" if lang == 'uz' else "🆔 Поиск по ID"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=search_by_name),
                KeyboardButton(text=search_by_phone)
            ],
            [
                KeyboardButton(text=search_by_id)
            ],
            [
                KeyboardButton(text=back_text)
            ]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_client_actions_reply(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Reply keyboard for client actions"""
    order = "📄 Buyurtma yaratish" if lang == 'uz' else "📄 Создать заказ"
    call = "📞 Qo'ng'iroq qilish" if lang == 'uz' else "📞 Позвонить"
    chat = "💬 Chat o'chirish" if lang == 'uz' else "💬 Начать чат"
    details = "🔍 To'liq ma'lumot" if lang == 'uz' else "🔍 Полная информация"
    back = "🔙 Ortga" if lang == 'uz' else "🔙 Назад"

    keyboard = [
        [KeyboardButton(text=order), KeyboardButton(text=call)],
        [KeyboardButton(text=chat), KeyboardButton(text=details)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def order_types_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Order types selection keyboard with workflow routing"""
    if lang == 'uz':
        types = [
            ("🔌 O'rnatish (Ulanish)", "installation"),
            ("📡 Sozlash (Ulanish)", "setup"),
            ("🔧 Ta'mirlash (Texnik)", "repair"),
            ("🧰 Profilaktika (Texnik)", "maintenance"),
            ("❓ Konsultatsiya (To'g'ridan-to'g'ri)", "consultation")
        ]
    else:
        types = [
            ("🔌 Установка (Подключение)", "installation"),
            ("📡 Настройка (Подключение)", "setup"),
            ("🔧 Ремонт (Техническая)", "repair"),
            ("🧰 Профилактика (Техническая)", "maintenance"),
            ("❓ Консультация (Прямая)", "consultation")
        ]
    
    keyboard = []
    for text, type_ in types:
        keyboard.append([InlineKeyboardButton(text=text, callback_data=f"service_type_{type_}")])
    
    keyboard.append([InlineKeyboardButton(text=("🔄 Orqaga" if lang == 'uz' else "🔄 Назад"), callback_data="call_center_back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def call_status_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Call status keyboard"""
    priorities = [
        ("🔴 Yuqori", "high"),
        ("🟡 O'rta", "medium"),
        ("🟢 Past", "low")
    ]
    keyboard = [
        [InlineKeyboardButton(text=text, callback_data=f"priority_{priority}") for text, priority in priorities],
        [InlineKeyboardButton(text=("🔄 Orqaga" if lang == 'uz' else "🔄 Назад"), callback_data="call_center_back")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def callback_schedule_keyboard(language: str) -> InlineKeyboardMarkup:
    """Callback scheduling keyboard"""
    schedule_in_1_hour_text = "⏰ 1 soatdan keyin" if language == "uz" else "⏰ Через 1 час"
    schedule_in_2_hours_text = "⏰ 2 soatdan keyin" if language == "uz" else "⏰ Через 2 часа"
    schedule_tomorrow_text = "📅 Ertaga" if language == "uz" else "📅 Завтра"
    custom_time_text = "🕐 Maxsus vaqt" if language == "uz" else "🕐 Специальное время"
    back_text = "◀️ Orqaga" if language == "uz" else "◀️ Назад"
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=schedule_in_1_hour_text,
                callback_data="callback_1h"
            )
        ],
        [
            InlineKeyboardButton(
                text=schedule_in_2_hours_text,
                callback_data="callback_2h"
            )
        ],
        [
            InlineKeyboardButton(
                text=schedule_tomorrow_text,
                callback_data="callback_tomorrow"
            )
        ],
        [
            InlineKeyboardButton(
                text=custom_time_text,
                callback_data="callback_custom"
            )
        ],
        [
            InlineKeyboardButton(
                text=back_text,
                callback_data="call_center_back"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def call_result_keyboard(language: str) -> InlineKeyboardMarkup:
    """Call result keyboard"""
    order_created_text = "✅ Buyurtma yaratildi" if language == "uz" else "✅ Заказ создан"
    callback_scheduled_text = "📞 Qayta qo'ng'iroq rejalashtirildi" if language == "uz" else "📞 Обратный звонок запланирован"
    information_provided_text = "ℹ️ Ma'lumot berildi" if language == "uz" else "ℹ️ Предоставлена информация"
    no_answer_text = "📵 Javob yo'q" if language == "uz" else "📵 Нет ответа"
    client_refused_text = "❌ Mijoz rad etdi" if language == "uz" else "❌ Клиент отказался"
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=order_created_text,
                callback_data="call_result_order"
            )
        ],
        [
            InlineKeyboardButton(
                text=callback_scheduled_text,
                callback_data="call_result_callback"
            )
        ],
        [
            InlineKeyboardButton(
                text=information_provided_text,
                callback_data="call_result_info"
            )
        ],
        [
            InlineKeyboardButton(
                text=no_answer_text,
                callback_data="call_result_no_answer"
            )
        ],
        [
            InlineKeyboardButton(
                text=client_refused_text,
                callback_data="call_result_refused"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)



def call_center_statistics_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Call center statistics menu"""
    daily_stats = "📅 Bugungi ko'rsatkichlar" if lang == 'uz' else "📅 Сегодняшние показатели"
    weekly_stats = "📊 Haftalik hisobot" if lang == 'uz' else "📊 Недельный отчет"
    monthly_stats = "📈 Oylik hisobot" if lang == 'uz' else "📈 Месячный отчет"
    performance = "🎯 Mening samaradorligim" if lang == 'uz' else "🎯 Моя эффективность"
    conversion = "📈 Konversiya darajasi" if lang == 'uz' else "📈 Коэффициент конверсии"
    back = "🔄 Orqaga" if lang == 'uz' else "🔄 Назад"
    
    keyboard = [
        [KeyboardButton(text=daily_stats),
         KeyboardButton(text=weekly_stats)],
        [KeyboardButton(text=monthly_stats),
         KeyboardButton(text=performance)],
        [KeyboardButton(text=conversion)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def call_center_operator_main_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Call center operator main menu"""
    direct_resolution = "📋 Masofadan hal qilish" if lang == 'uz' else "📋 Удаленное решение"
    remote_support = "🔧 Masofaviy yordam" if lang == 'uz' else "🔧 Удаленная поддержка"
    client_consultation = "💬 Mijoz maslahati" if lang == 'uz' else "💬 Консультация клиента"
    technical_guidance = "📚 Texnik ko'rsatma" if lang == 'uz' else "📚 Техническое руководство"
    back = "🔄 Orqaga" if lang == 'uz' else "🔄 Назад"
    
    keyboard = [
        [KeyboardButton(text=direct_resolution), KeyboardButton(text=remote_support)],
        [KeyboardButton(text=client_consultation), KeyboardButton(text=technical_guidance)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def call_center_supervisor_main_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Call center supervisor main menu"""
    assign_requests = "📋 So'rovlarni tayinlash" if lang == 'uz' else "📋 Назначить запросы"
    pending_assignments = "⏳ Kutilayotgan tayinlashlar" if lang == 'uz' else "⏳ Ожидающие назначения"
    team_performance = "📊 Jamoa samaradorligi" if lang == 'uz' else "📊 Производительность команды"
    back = "🔄 Orqaga" if lang == 'uz' else "🔄 Назад"
    
    keyboard = [
        [KeyboardButton(text=assign_requests), KeyboardButton(text=pending_assignments)],
        [KeyboardButton(text=team_performance)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def call_center_operator_selection_keyboard(operators: list, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Keyboard for selecting call center operator"""
    keyboard = []
    
    for operator in operators:
        operator_name = operator.get('full_name', f"Operator {operator['id']}")
        keyboard.append([
            InlineKeyboardButton(
                text=f"👤 {operator_name}",
                callback_data=f"assign_cc_operator_{operator['id']}"
            )
        ])
    
    back_text = "🔄 Orqaga" if lang == 'uz' else "🔄 Назад"
    keyboard.append([InlineKeyboardButton(text=back_text, callback_data="cc_supervisor_back")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def remote_resolution_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Keyboard for remote resolution actions"""
    resolve_text = "✅ Masofadan hal qilish" if lang == 'uz' else "✅ Решить удаленно"
    escalate_text = "⬆️ Yuqoriga ko'tarish" if lang == 'uz' else "⬆️ Эскалировать"
    back_text = "🔄 Orqaga" if lang == 'uz' else "🔄 Назад"
    
    keyboard = [
        [InlineKeyboardButton(text=resolve_text, callback_data="resolve_remotely")],
        [InlineKeyboardButton(text=escalate_text, callback_data="escalate_request")],
        [InlineKeyboardButton(text=back_text, callback_data="cc_operator_back")]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def rating_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Rating keyboard for client feedback"""
    rating_text = "Xizmatni baholang" if lang == 'uz' else "Оцените услугу"
    
    keyboard = []
    for i in range(1, 6):
        star_text = "⭐" * i
        keyboard.append([
            InlineKeyboardButton(
                text=f"{star_text} ({i})",
                callback_data=f"rate_service_{i}"
            )
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Additional Reply Keyboards for Call Center
def get_call_center_orders_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Orders management menu for call center operator"""
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


def get_call_management_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Call management menu for call center operator"""
    incoming_calls = "📞 Kiruvchi qo'ng'iroqlar" if lang == 'uz' else "📞 Входящие звонки"
    outgoing_calls = "📤 Chiquvchi qo'ng'iroqlar" if lang == 'uz' else "📤 Исходящие звонки"
    scheduled_callbacks = "⏰ Rejalashtirilgan qo'ng'iroqlar" if lang == 'uz' else "⏰ Запланированные звонки"
    call_history = "📋 Qo'ng'iroqlar tarixi" if lang == 'uz' else "📋 История звонков"
    call_notes = "📝 Qo'ng'iroq eslatmalari" if lang == 'uz' else "📝 Заметки звонков"
    call_stats = "📊 Qo'ng'iroq statistikasi" if lang == 'uz' else "📊 Статистика звонков"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=incoming_calls), KeyboardButton(text=outgoing_calls)],
        [KeyboardButton(text=scheduled_callbacks), KeyboardButton(text=call_history)],
        [KeyboardButton(text=call_notes), KeyboardButton(text=call_stats)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_client_support_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Client support menu for call center operator"""
    technical_support = "🔧 Texnik yordam" if lang == 'uz' else "🔧 Техническая поддержка"
    billing_support = "💰 Hisob-kitob yordami" if lang == 'uz' else "💰 Поддержка по счетам"
    service_info = "ℹ️ Xizmat ma'lumotlari" if lang == 'uz' else "ℹ️ Информация об услугах"
    complaint_handling = "⚠️ Shikoyatlar" if lang == 'uz' else "⚠️ Жалобы"
    general_inquiry = "❓ Umumiy so'rovlar" if lang == 'uz' else "❓ Общие запросы"
    escalate_issue = "⬆️ Muammoni ko'tarish" if lang == 'uz' else "⬆️ Эскалировать проблему"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=technical_support), KeyboardButton(text=billing_support)],
        [KeyboardButton(text=service_info), KeyboardButton(text=complaint_handling)],
        [KeyboardButton(text=general_inquiry), KeyboardButton(text=escalate_issue)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_call_center_analytics_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Analytics menu for call center operator"""
    daily_performance = "📊 Kunlik samaradorlik" if lang == 'uz' else "📊 Дневная производительность"
    weekly_report = "📈 Haftalik hisobot" if lang == 'uz' else "📈 Недельный отчет"
    monthly_summary = "📉 Oylik xulosa" if lang == 'uz' else "📉 Месячная сводка"
    call_metrics = "📞 Qo'ng'iroq ko'rsatkichlari" if lang == 'uz' else "📞 Метрики звонков"
    resolution_rate = "✅ Hal qilish darajasi" if lang == 'uz' else "✅ Уровень решения"
    customer_satisfaction = "⭐ Mijoz mamnunligi" if lang == 'uz' else "⭐ Удовлетворенность клиентов"
    back = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=daily_performance), KeyboardButton(text=weekly_report)],
        [KeyboardButton(text=monthly_summary), KeyboardButton(text=call_metrics)],
        [KeyboardButton(text=resolution_rate), KeyboardButton(text=customer_satisfaction)],
        [KeyboardButton(text=back)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Enhanced Inline Keyboards for Call Center
def get_order_management_inline_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Order management inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📋 Yangi buyurtmalar" if lang == 'uz' else "📋 Новые заказы",
                callback_data="cc_new_orders"
            ),
            InlineKeyboardButton(
                text="⏳ Jarayondagi" if lang == 'uz' else "⏳ В процессе",
                callback_data="cc_in_progress_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные",
                callback_data="cc_completed_orders"
            ),
            InlineKeyboardButton(
                text="❌ Bekor qilingan" if lang == 'uz' else "❌ Отмененные",
                callback_data="cc_cancelled_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔍 Qidirish" if lang == 'uz' else "🔍 Поиск",
                callback_data="cc_search_orders"
            ),
            InlineKeyboardButton(
                text="📊 Statistika" if lang == 'uz' else "📊 Статистика",
                callback_data="cc_orders_stats"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="cc_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_client_search_inline_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Client search inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📱 Telefon" if lang == 'uz' else "📱 Телефон",
                callback_data="cc_search_phone"
            ),
            InlineKeyboardButton(
                text="👤 Ism" if lang == 'uz' else "👤 Имя",
                callback_data="cc_search_name"
            )
        ],
        [
            InlineKeyboardButton(
                text="🆔 ID" if lang == 'uz' else "🆔 ID",
                callback_data="cc_search_id"
            ),
            InlineKeyboardButton(
                text="📧 Email" if lang == 'uz' else "📧 Email",
                callback_data="cc_search_email"
            )
        ],
        [
            InlineKeyboardButton(
                text="➕ Yangi mijoz" if lang == 'uz' else "➕ Новый клиент",
                callback_data="cc_new_client"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="cc_cancel_search"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_type_inline_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Application type selection inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔌 Ulanish arizasi" if lang == 'uz' else "🔌 Заявка на подключение",
                callback_data="cc_app_connection"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔧 Texnik xizmat" if lang == 'uz' else "🔧 Техническое обслуживание",
                callback_data="cc_app_technical"
            )
        ],
        [
            InlineKeyboardButton(
                text="📞 Qo'ng'iroq markazi" if lang == 'uz' else "📞 Колл-центр",
                callback_data="cc_app_call_center"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="cc_cancel_app"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_call_actions_inline_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Call actions inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📞 Qo'ng'iroq qilish" if lang == 'uz' else "📞 Позвонить",
                callback_data="cc_make_call"
            ),
            InlineKeyboardButton(
                text="📝 Eslatma qo'shish" if lang == 'uz' else "📝 Добавить заметку",
                callback_data="cc_add_note"
            )
        ],
        [
            InlineKeyboardButton(
                text="⏰ Qayta qo'ng'iroq" if lang == 'uz' else "⏰ Обратный звонок",
                callback_data="cc_schedule_callback"
            ),
            InlineKeyboardButton(
                text="✅ Masofadan hal qilish" if lang == 'uz' else "✅ Решить удаленно",
                callback_data="cc_resolve_remote"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬆️ Eskalatsiya" if lang == 'uz' else "⬆️ Эскалация",
                callback_data="cc_escalate"
            ),
            InlineKeyboardButton(
                text="📋 Buyurtma yaratish" if lang == 'uz' else "📋 Создать заказ",
                callback_data="cc_create_order"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="cc_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_order_actions_inline_menu(order_id: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Order actions inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="👁️ Ko'rish" if lang == 'uz' else "👁️ Просмотр",
                callback_data=f"cc_view_order_{order_id}"
            ),
            InlineKeyboardButton(
                text="📝 Tahrirlash" if lang == 'uz' else "📝 Редактировать",
                callback_data=f"cc_edit_order_{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔄 Status o'zgartirish" if lang == 'uz' else "🔄 Изменить статус",
                callback_data=f"cc_change_status_{order_id}"
            ),
            InlineKeyboardButton(
                text="📞 Mijozga qo'ng'iroq" if lang == 'uz' else "📞 Позвонить клиенту",
                callback_data=f"cc_call_client_{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Izoh qo'shish" if lang == 'uz' else "💬 Добавить комментарий",
                callback_data=f"cc_add_comment_{order_id}"
            ),
            InlineKeyboardButton(
                text="⬆️ Eskalatsiya" if lang == 'uz' else "⬆️ Эскалация",
                callback_data=f"cc_escalate_order_{order_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="cc_close_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_priority_selection_inline_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Priority selection inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔴 Yuqori" if lang == 'uz' else "🔴 Высокий",
                callback_data="cc_priority_high"
            ),
            InlineKeyboardButton(
                text="🟡 O'rta" if lang == 'uz' else "🟡 Средний",
                callback_data="cc_priority_medium"
            )
        ],
        [
            InlineKeyboardButton(
                text="🟢 Past" if lang == 'uz' else "🟢 Низкий",
                callback_data="cc_priority_low"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="cc_cancel_priority"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_status_change_inline_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Status change inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🆕 Yangi" if lang == 'uz' else "🆕 Новый",
                callback_data="cc_status_new"
            ),
            InlineKeyboardButton(
                text="⏳ Jarayonda" if lang == 'uz' else "⏳ В процессе",
                callback_data="cc_status_in_progress"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Bajarilgan" if lang == 'uz' else "✅ Выполнен",
                callback_data="cc_status_completed"
            ),
            InlineKeyboardButton(
                text="⏸️ To'xtatilgan" if lang == 'uz' else "⏸️ Приостановлен",
                callback_data="cc_status_on_hold"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilingan" if lang == 'uz' else "❌ Отменен",
                callback_data="cc_status_cancelled"
            ),
            InlineKeyboardButton(
                text="🔴 Muammo" if lang == 'uz' else "🔴 Проблема",
                callback_data="cc_status_issue"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="cc_cancel_status"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_feedback_inline_menu(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Feedback inline keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📝 Fikr yozish" if lang == 'uz' else "📝 Написать отзыв",
                callback_data="cc_write_feedback"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Fikrlarni ko'rish" if lang == 'uz' else "📊 Просмотр отзывов",
                callback_data="cc_view_feedback"
            )
        ],
        [
            InlineKeyboardButton(
                text="⭐ Baholash" if lang == 'uz' else "⭐ Оценить",
                callback_data="cc_rate_service"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
                callback_data="cc_close_menu"
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
                callback_data="cc_lang_uz"
            ),
            InlineKeyboardButton(
                text="🇷🇺 Русский",
                callback_data="cc_lang_ru"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data="cc_cancel_lang"
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
        client_name = order.get('client_name', 'N/A')[:15]
        text = f"{status_emoji} #{order['id']} - {client_name}"
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"cc_view_order_{order['id']}"
            )
        ])
    
    # Pagination buttons
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущая",
                callback_data=f"cc_orders_page_{page-1}"
            )
        )
    
    if end_idx < len(orders):
        nav_buttons.append(
            InlineKeyboardButton(
                text="Keyingi ➡️" if lang == 'uz' else "Следующая ➡️",
                callback_data=f"cc_orders_page_{page+1}"
            )
        )
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Close button
    keyboard.append([
        InlineKeyboardButton(
            text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
            callback_data="cc_close_menu"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_client_list_keyboard(clients: List[Dict[str, Any]], lang: str = 'uz') -> InlineKeyboardMarkup:
    """Generate keyboard for client list"""
    keyboard = []
    
    for client in clients[:8]:  # Limit to 8 clients
        name = client.get('full_name', 'N/A')[:20]
        phone = client.get('phone', 'N/A')
        text = f"👤 {name} - {phone}"
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"cc_select_client_{client['id']}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            text="🔍 Boshqa qidirish" if lang == 'uz' else "🔍 Другой поиск",
            callback_data="cc_search_again"
        )
    ])
    
    keyboard.append([
        InlineKeyboardButton(
            text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
            callback_data="cc_cancel_search"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def _get_status_emoji(status: str) -> str:
    """Get emoji for order status"""
    status_emojis = {
        'new': '🆕',
        'assigned': '👤',
        'in_progress': '⏳',
        'on_hold': '⏸️',
        'completed': '✅',
        'cancelled': '❌',
        'issue': '🔴',
        'escalated': '⬆️',
        'pending': '⏳',
        'review': '👁️'
    }
    return status_emojis.get(status, '❓')

def get_language_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Call center uchun til tanlash inline keyboard"""
    uz_text = "🇺🇿 O'zbekcha" if lang == "uz" else "🇺🇿 Узбекский"
    ru_text = "🇷🇺 Ruscha" if lang == "uz" else "🇷🇺 Русский"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=uz_text, callback_data="cc_lang_uz")],
            [InlineKeyboardButton(text=ru_text, callback_data="cc_lang_ru")]
        ]
    )
    return keyboard

def get_chat_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Chat keyboard for call center operators"""
    active_chats_text = "📱 Faol chatlar" if lang == 'uz' else "📱 Активные чаты"
    waiting_chats_text = "⏳ Kutilayotgan chatlar" if lang == 'uz' else "⏳ Ожидающие чаты"
    chat_history_text = "📋 Chat tarixi" if lang == 'uz' else "📋 История чатов"
    chat_settings_text = "⚙️ Chat sozlamalari" if lang == 'uz' else "⚙️ Настройки чата"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=active_chats_text)],
        [KeyboardButton(text=waiting_chats_text)],
        [KeyboardButton(text=chat_history_text)],
        [KeyboardButton(text=chat_settings_text)],
        [KeyboardButton(text=back_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_clients_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Clients keyboard for call center operators"""
    search_client_text = "🔍 Mijoz qidirish" if lang == 'uz' else "🔍 Поиск клиента"
    clients_list_text = "📋 Mijozlar ro'yxati" if lang == 'uz' else "📋 Список клиентов"
    add_client_text = "➕ Yangi mijoz qo'shish" if lang == 'uz' else "➕ Добавить клиента"
    client_profile_text = "👤 Mijoz profili" if lang == 'uz' else "👤 Профиль клиента"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=search_client_text)],
        [KeyboardButton(text=clients_list_text)],
        [KeyboardButton(text=add_client_text)],
        [KeyboardButton(text=client_profile_text)],
        [KeyboardButton(text=back_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_direct_resolution_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Direct resolution keyboard for call center operators"""
    technical_issues_text = "🔧 Texnik muammolar" if lang == 'uz' else "🔧 Технические проблемы"
    connection_issues_text = "🔌 Ulanish muammolari" if lang == 'uz' else "🔌 Проблемы подключения"
    billing_issues_text = "💰 Hisob-kitob muammolari" if lang == 'uz' else "💰 Проблемы с оплатой"
    service_questions_text = "❓ Xizmat savollari" if lang == 'uz' else "❓ Вопросы по услугам"
    remote_assistance_text = "🖥️ Masofaviy yordam" if lang == 'uz' else "🖥️ Удаленная помощь"
    escalation_text = "⬆️ Eskalatsiya" if lang == 'uz' else "⬆️ Эскалация"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=technical_issues_text)],
        [KeyboardButton(text=connection_issues_text)],
        [KeyboardButton(text=billing_issues_text)],
        [KeyboardButton(text=service_questions_text)],
        [KeyboardButton(text=remote_assistance_text)],
        [KeyboardButton(text=escalation_text)],
        [KeyboardButton(text=back_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_feedback_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Feedback keyboard for call center operators"""
    write_feedback_text = "📝 Fikr yozish" if lang == 'uz' else "📝 Написать отзыв"
    view_feedback_text = "📊 Fikrlarni ko'rish" if lang == 'uz' else "📊 Просмотр отзывов"
    rate_service_text = "⭐ Xizmatni baholash" if lang == 'uz' else "⭐ Оценить услугу"
    feedback_stats_text = "📈 Fikr statistikasi" if lang == 'uz' else "📈 Статистика отзывов"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=write_feedback_text)],
        [KeyboardButton(text=view_feedback_text)],
        [KeyboardButton(text=rate_service_text)],
        [KeyboardButton(text=feedback_stats_text)],
        [KeyboardButton(text=back_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_inbox_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Inbox menu keyboard for call center operators"""
    new_messages_text = "🆕 Yangi xabarlar" if lang == 'uz' else "🆕 Новые сообщения"
    unread_messages_text = "📨 O'qilmagan xabarlar" if lang == 'uz' else "📨 Непрочитанные сообщения"
    urgent_messages_text = "🚨 Shoshilinch xabarlar" if lang == 'uz' else "🚨 Срочные сообщения"
    all_messages_text = "📋 Barcha xabarlar" if lang == 'uz' else "📋 Все сообщения"
    message_history_text = "📜 Xabar tarixi" if lang == 'uz' else "📜 История сообщений"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=new_messages_text)],
        [KeyboardButton(text=unread_messages_text)],
        [KeyboardButton(text=urgent_messages_text)],
        [KeyboardButton(text=all_messages_text)],
        [KeyboardButton(text=message_history_text)],
        [KeyboardButton(text=back_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_message_actions_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Message actions menu keyboard for call center operators"""
    reply_text = "💬 Javob berish" if lang == 'uz' else "💬 Ответить"
    forward_text = "➡️ Yuborish" if lang == 'uz' else "➡️ Переслать"
    mark_read_text = "✅ O'qilgan deb belgilash" if lang == 'uz' else "✅ Отметить как прочитанное"
    mark_urgent_text = "🚨 Shoshilinch deb belgilash" if lang == 'uz' else "🚨 Отметить как срочное"
    archive_text = "📁 Arxivga ko'chirish" if lang == 'uz' else "📁 Архивировать"
    delete_text = "🗑️ O'chirish" if lang == 'uz' else "🗑️ Удалить"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=reply_text), KeyboardButton(text=forward_text)],
        [KeyboardButton(text=mark_read_text), KeyboardButton(text=mark_urgent_text)],
        [KeyboardButton(text=archive_text), KeyboardButton(text=delete_text)],
        [KeyboardButton(text=back_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_orders_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Orders menu keyboard for call center operators"""
    my_orders_text = "📋 Mening buyurtmalarim" if lang == 'uz' else "📋 Мои заказы"
    new_orders_text = "🆕 Yangi buyurtmalar" if lang == 'uz' else "🆕 Новые заказы"
    in_progress_text = "⏳ Jarayondagi" if lang == 'uz' else "⏳ В процессе"
    completed_text = "✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные"
    pending_review_text = "👁️ Ko'rib chiqilmoqda" if lang == 'uz' else "👁️ На рассмотрении"
    search_orders_text = "🔍 Buyurtma qidirish" if lang == 'uz' else "🔍 Поиск заказов"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=my_orders_text), KeyboardButton(text=new_orders_text)],
        [KeyboardButton(text=in_progress_text), KeyboardButton(text=completed_text)],
        [KeyboardButton(text=pending_review_text), KeyboardButton(text=search_orders_text)],
        [KeyboardButton(text=back_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_order_actions_menu(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Order actions menu keyboard for call center operators"""
    view_order_text = "👁️ Buyurtmani ko'rish" if lang == 'uz' else "👁️ Просмотр заказа"
    edit_order_text = "📝 Tahrirlash" if lang == 'uz' else "📝 Редактировать"
    change_status_text = "🔄 Status o'zgartirish" if lang == 'uz' else "🔄 Изменить статус"
    call_client_text = "📞 Mijozga qo'ng'iroq" if lang == 'uz' else "📞 Позвонить клиенту"
    add_comment_text = "💬 Izoh qo'shish" if lang == 'uz' else "💬 Добавить комментарий"
    escalate_text = "⬆️ Eskalatsiya" if lang == 'uz' else "⬆️ Эскалация"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    
    keyboard = [
        [KeyboardButton(text=view_order_text), KeyboardButton(text=edit_order_text)],
        [KeyboardButton(text=change_status_text), KeyboardButton(text=call_client_text)],
        [KeyboardButton(text=add_comment_text), KeyboardButton(text=escalate_text)],
        [KeyboardButton(text=back_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# New centralized keyboard functions for call center module
def get_rating_statistics_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Rating statistics keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📈 Batafsil hisobot" if lang == 'uz' else "📈 Подробный отчет",
                callback_data="detailed_rating_report"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Reyting grafigi" if lang == 'uz' else "📊 График рейтинга",
                callback_data="rating_chart"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_feedback_complaints_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Feedback and complaints keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📋 Barcha fikrlar" if lang == 'uz' else "📋 Все отзывы",
                callback_data="view_all_feedback"
            )
        ],
        [
            InlineKeyboardButton(
                text="📊 Fikrlar statistikasi" if lang == 'uz' else "📊 Статистика отзывов",
                callback_data="feedback_statistics"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_top_operators_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Top operators keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📊 Batafsil reyting" if lang == 'uz' else "📊 Подробный рейтинг",
                callback_data="detailed_operator_rating"
            )
        ],
        [
            InlineKeyboardButton(
                text="🏆 Mukofotlar" if lang == 'uz' else "🏆 Награды",
                callback_data="operator_rewards"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_rating_dynamics_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Rating dynamics keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📊 Grafik ko'rinish" if lang == 'uz' else "📊 Графический вид",
                callback_data="rating_dynamics_chart"
            )
        ],
        [
            InlineKeyboardButton(
                text="📈 Batafsil tahlil" if lang == 'uz' else "📈 Подробный анализ",
                callback_data="detailed_rating_analysis"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_rating_settings_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Rating settings keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📝 Reyting shablonlari" if lang == 'uz' else "📝 Шаблоны рейтинга",
                callback_data="rating_templates"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔧 Boshqa sozlamalar" if lang == 'uz' else "🔧 Другие настройки",
                callback_data="other_rating_settings"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_operator_resolve_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Operator resolve issue keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="✅ Muammoni hal qilish" if lang == 'uz' else "✅ Решить проблему",
                callback_data="operator_resolve_issue"
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga qaytish" if lang == 'uz' else "⬅️ Вернуться назад",
                callback_data="operator_back_to_application"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_operator_cancel_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Operator cancel keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="❌ Bekor qilish" if lang == 'uz' else "❌ Отмена",
                callback_data="operator_back_to_application"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_operator_back_to_inbox_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Operator back to inbox keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📥 Inbox'ga qaytish" if lang == 'uz' else "📥 Вернуться в inbox",
                callback_data="operator_back_to_inbox"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_operator_navigation_keyboard(current_index: int, total_applications: int, application_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Operator navigation keyboard"""
    keyboard = []
    
    # Action buttons row
    action_buttons = []
    
    # Contact client button
    action_buttons.append(InlineKeyboardButton(
        text="📞 Mijoz bilan bog'lanish" if lang == 'uz' else "📞 Связаться с клиентом",
        callback_data=f"operator_contact_client_{application_id}"
    ))
    
    # Resolve issue button
    action_buttons.append(InlineKeyboardButton(
        text="✅ Muammoni hal qilish" if lang == 'uz' else "✅ Решить проблему",
        callback_data=f"operator_resolve_issue_{application_id}"
    ))
    
    keyboard.append(action_buttons)
    
    # Navigation buttons row
    nav_buttons = []
    
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущая",
            callback_data="operator_prev_application"
        ))
    
    if current_index < total_applications - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️" if lang == 'uz' else "Следующая ➡️",
            callback_data="operator_next_application"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)