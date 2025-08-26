from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def get_technician_main_keyboard(lang="uz"):
    """Technician main keyboard - returns main menu keyboard"""
    return get_technician_main_menu_keyboard(lang)

def get_technician_main_menu_keyboard(lang="uz"):
    """Technician main menu keyboard - tex.txt talablariga mos"""
    inbox_text = "📥 Inbox"
    my_tasks_text = "📋 Vazifalarim" if lang == "uz" else "📋 Мои задачи"
    reports_text = "📊 Hisobotlar" if lang == "uz" else "📊 Отчеты"
    help_text = "🆘 Yordam" if lang == "uz" else "🆘 Помощь"
    
    # Tex.txt bo'yicha technician ariza yaratmaydi, faqat bajaradi
    change_language_text = "🌐 Tilni o'zgartirish" if lang == "uz" else "🌐 Изменить язык"
    
    keyboard = [
        [KeyboardButton(text=inbox_text)],
        [KeyboardButton(text=my_tasks_text), KeyboardButton(text=reports_text)],
        [KeyboardButton(text=help_text)],
        [KeyboardButton(text=change_language_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_technician_help_menu(language: str) -> ReplyKeyboardMarkup:
    """Technician help menu"""
    request_help_text = "🆘 Yordam so'rash" if language == "uz" else "🆘 Запросить помощь"
    send_location_text = "📍 Geolokatsiya yuborish" if language == "uz" else "📍 Отправить геолокацию"
    contact_manager_text = "👨‍💼 Menejer bilan bog'lanish" if language == "uz" else "👨‍💼 Связаться с менеджером"
    equipment_request_text = "🔧 Jihoz so'rash" if language == "uz" else "🔧 Запросить оборудование"
    back_text = "◀️ Orqaga" if language == "uz" else "◀️ Назад"
    
    keyboard = [
        [KeyboardButton(text=request_help_text)],
        [KeyboardButton(text=send_location_text)],
        [KeyboardButton(text=contact_manager_text)],
        [KeyboardButton(text=equipment_request_text)],
        [KeyboardButton(text=back_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_help_request_types_keyboard(language: str) -> ReplyKeyboardMarkup:
    """Help request types keyboard"""
    equipment_issue_text = "🔧 Jihoz muammosi" if language == "uz" else "🔧 Проблема с оборудованием"
    parts_needed_text = "🛠️ Qo'shimcha ehtiyot qism kerak" if language == "uz" else "🛠️ Нужны дополнительные запчасти"
    technical_question_text = "❓ Texnik savol" if language == "uz" else "❓ Технический вопрос"
    emergency_text = "🚨 Favqulodda holat" if language == "uz" else "🚨 Экстренная ситуация"
    client_issue_text = "👤 Mijoz bilan muammo" if language == "uz" else "👤 Проблема с клиентом"
    back_text = "◀️ Orqaga" if language == "uz" else "◀️ Назад"
    
    keyboard = [
        [KeyboardButton(text=equipment_issue_text)],
        [KeyboardButton(text=parts_needed_text)],
        [KeyboardButton(text=technical_question_text)],
        [KeyboardButton(text=emergency_text)],
        [KeyboardButton(text=client_issue_text)],
        [KeyboardButton(text=back_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_back_technician_keyboard(lang="uz"):
    """Back to main menu keyboard for technician"""
    back_text = "🏠 Asosiy menyu" if lang == "uz" else "🏠 Главное меню"
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=back_text)]],
        resize_keyboard=True
    )

def get_contact_keyboard(lang="uz"):
    """Contact sharing keyboard"""
    share_contact_text = "📱 Kontakt ulashish" if lang == "uz" else "📱 Поделиться контактом"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=share_contact_text, request_contact=True)]],
        resize_keyboard=True
    )
    return keyboard

def get_language_keyboard(role="technician"):
    """Language selection keyboard"""
    prefix = f"{role}_lang_" if role != "technician" else "tech_lang_"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data=f"{prefix}uz")],
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data=f"{prefix}ru")]
        ]
    )
    return keyboard

def get_technician_selection_keyboard(technicians):
    """Keyboard for selecting technician for task transfer"""
    keyboard = []
    for tech in technicians:
        keyboard.append([
            InlineKeyboardButton(
                text=f"👨‍🔧 {tech['full_name']}",
                callback_data=f"transfer_to_tech_{tech['id']}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_technician_inbox_keyboard(lang='uz'):
    """Generate inbox keyboard for technician with locale support"""
    new_messages_text = "🆕 Yangi xabarlar" if lang == "uz" else "🆕 Новые сообщения"
    read_messages_text = "✅ O'qilgan xabarlar" if lang == "uz" else "✅ Прочитанные сообщения"
    urgent_messages_text = "🚨 Shoshilinch xabarlar" if lang == "uz" else "🚨 Срочные сообщения"
    all_messages_text = "📋 Barcha xabarlar" if lang == "uz" else "📋 Все сообщения"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=new_messages_text, callback_data="tech_inbox_new"),
            InlineKeyboardButton(text=read_messages_text, callback_data="tech_inbox_read")
        ],
        [
            InlineKeyboardButton(text=urgent_messages_text, callback_data="tech_inbox_urgent"),
            InlineKeyboardButton(text=all_messages_text, callback_data="tech_inbox_all")
        ],
        [
            InlineKeyboardButton(text=back_text, callback_data="back_to_technician_main")
        ]
    ])
    return keyboard

def get_technician_back_keyboard(lang='uz'):
    """Technician back keyboard"""
    back_text = "🏠 Asosiy menyu" if lang == "uz" else "🏠 Главное меню"
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=back_text)]],
        resize_keyboard=True
    )

def get_task_action_keyboard(task_id, status, lang="uz") -> InlineKeyboardMarkup:
    """Task action keyboard"""
    buttons = []
    
    if status == 'assigned':
        accept_text = "✅ Qabul qilish" if lang == "uz" else "✅ Принять"
        transfer_text = "🔄 O'tkazish" if lang == "uz" else "🔄 Передать"
        buttons = [
            [InlineKeyboardButton(text=accept_text, callback_data=f"accept_task_{task_id}")],
            [InlineKeyboardButton(text=transfer_text, callback_data=f"transfer_task_{task_id}")]
        ]
    elif status == 'accepted':
        start_text = "▶️ Boshlash" if lang == "uz" else "▶️ Начать"
        transfer_text = "🔄 O'tkazish" if lang == "uz" else "🔄 Передать"
        buttons = [
            [InlineKeyboardButton(text=start_text, callback_data=f"start_task_{task_id}")],
            [InlineKeyboardButton(text=transfer_text, callback_data=f"transfer_task_{task_id}")]
        ]
    elif status == 'in_progress':
        complete_text = "✅ Yakunlash" if lang == "uz" else "✅ Завершить"
        buttons = [
            [InlineKeyboardButton(text=complete_text, callback_data=f"complete_task_{task_id}")]
        ]
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_equipment_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Equipment request keyboard for technician"""
    request_text = "🔧 Jihoz so'rang" if lang == "uz" else "🔧 Запросить оборудование"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=request_text,
                callback_data="tech_equipment_request"
            )
        ],
        [
            InlineKeyboardButton(
                text=back_text,
                callback_data="tech_back_to_help"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_completion_keyboard(task_id, lang="uz"):
    """Completion keyboard for task"""
    with_comment_text = "✅ Bajarildi (izoh bilan)" if lang == "uz" else "✅ Выполнено (с комментарием)"
    without_comment_text = "✅ Bajarildi" if lang == "uz" else "✅ Выполнено"
    
    keyboard = [
        [InlineKeyboardButton(text=with_comment_text, callback_data=f"complete_with_comment_{task_id}")],
        [InlineKeyboardButton(text=without_comment_text, callback_data=f"complete_without_comment_{task_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_reports_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Reports menu keyboard for technician"""
    stats_text = "📊 Statistikalarim" if lang == "uz" else "📊 Мои статистики"
    detailed_text = "📄 Batafsil" if lang == "uz" else "📄 Подробнее"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=stats_text,
                callback_data="tech_stats"
            )
        ],
        [
            InlineKeyboardButton(
                text=detailed_text,
                callback_data="tech_detailed_report"
            )
        ],
        [
            InlineKeyboardButton(
                text=back_text,
                callback_data="tech_back_to_main"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def equipment_documentation_keyboard(request_id: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """Equipment documentation keyboard for technician"""
    document_text = "📝 Uskunani hujjatlash" if lang == "uz" else "📝 Документировать оборудование"
    
    keyboard = [
        [InlineKeyboardButton(
            text=document_text,
            callback_data=f"document_equipment_for_warehouse_{request_id}"
        )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# New centralized keyboard functions for technician module
def get_diagnostic_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Diagnostic keyboard for technician"""
    diagnostic_text = "🔍 Diagnostika boshlash" if lang == "uz" else "🔍 Начать диагностику"
    back_text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    
    keyboard = [
        [InlineKeyboardButton(text=diagnostic_text, callback_data="tech_start_diagnostic")],
        [InlineKeyboardButton(text=back_text, callback_data="tech_back_to_application")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_cancel_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Cancel keyboard for technician"""
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отмена"
    
    keyboard = [
        [InlineKeyboardButton(text=cancel_text, callback_data="tech_cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_warehouse_confirmation_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Warehouse confirmation keyboard for technician"""
    yes_text = "✅ Ha" if lang == "uz" else "✅ Да"
    no_text = "❌ Yo'q" if lang == "uz" else "❌ Нет"
    
    keyboard = [
        [InlineKeyboardButton(text=yes_text, callback_data="tech_warehouse_yes")],
        [InlineKeyboardButton(text=no_text, callback_data="tech_warehouse_no")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_warehouse_items_keyboard(items: list, lang: str = "uz") -> InlineKeyboardMarkup:
    """Warehouse items selection keyboard for technician"""
    keyboard = []
    for item in items:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{item['name']} ({item['quantity']} dona)",
                callback_data=f"tech_select_item_{item['id']}"
            )
        ])
    
    custom_text = "✏️ Boshqa jihoz" if lang == "uz" else "✏️ Другое оборудование"
    keyboard.append([InlineKeyboardButton(text=custom_text, callback_data="tech_custom_warehouse_item")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_warehouse_quantity_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Warehouse quantity input keyboard for technician"""
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отмена"
    
    keyboard = [
        [InlineKeyboardButton(text=cancel_text, callback_data="tech_cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_work_completion_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Work completion keyboard for technician"""
    complete_text = "✅ Ishni yakunlash" if lang == "uz" else "✅ Завершить работу"
    back_text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    
    keyboard = [
        [InlineKeyboardButton(text=complete_text, callback_data="tech_complete_work")],
        [InlineKeyboardButton(text=back_text, callback_data="tech_back_to_application")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_work_notes_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Work notes input keyboard for technician"""
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отмена"
    
    keyboard = [
        [InlineKeyboardButton(text=cancel_text, callback_data="tech_cancel")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_to_application_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Back to application keyboard for technician"""
    back_text = "⬅️ Ariza qaytish" if lang == "uz" else "⬅️ Вернуться к заявке"
    
    keyboard = [
        [InlineKeyboardButton(text=back_text, callback_data="tech_back_to_application")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_help_back_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Help back keyboard for technician"""
    back_text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    
    keyboard = [
        [InlineKeyboardButton(text=back_text, callback_data="tech_back_to_help")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_reports_back_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Reports back keyboard for technician"""
    back_text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    
    keyboard = [
        [InlineKeyboardButton(text=back_text, callback_data="tech_back_to_reports")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_application_action_keyboard(application, current_index: int, total_applications: int, lang: str = "uz") -> InlineKeyboardMarkup:
    """Application action keyboard for technician"""
    keyboard = []
    
    # Navigation buttons
    if total_applications > 1:
        if current_index > 0:
            prev_text = "⬅️ Oldingi" if lang == "uz" else "⬅️ Предыдущий"
            keyboard.append([InlineKeyboardButton(text=prev_text, callback_data="tech_prev_application")])
        
        if current_index < total_applications - 1:
            next_text = "Keyingi ➡️" if lang == "uz" else "Следующий ➡️"
            keyboard.append([InlineKeyboardButton(text=next_text, callback_data="tech_next_application")])
    
    # Action buttons
    if application.get('current_status') == 'assigned_to_technician':
        accept_text = "✅ Ishni qabul qilish" if lang == "uz" else "✅ Принять работу"
        keyboard.append([InlineKeyboardButton(text=accept_text, callback_data="tech_accept_work")])
    
    if application.get('work_started', False) and not application.get('work_completed', False):
        diagnostic_text = "🔍 Diagnostika" if lang == "uz" else "🔍 Диагностика"
        keyboard.append([InlineKeyboardButton(text=diagnostic_text, callback_data="tech_start_diagnostic")])
    
    # Back button
    back_text = "🏠 Asosiy menyu" if lang == "uz" else "🏠 Главное меню"
    keyboard.append([InlineKeyboardButton(text=back_text, callback_data="tech_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
