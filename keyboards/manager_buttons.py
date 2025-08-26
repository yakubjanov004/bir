from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict


def get_manager_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """
    Manager uchun asosiy reply menyu (O'zbek va Rus tillarida).
    """
    if lang == "uz":
        keyboard = [
            [KeyboardButton(text="📥 Inbox"), KeyboardButton(text="📋 Arizalarni ko'rish")],
            [KeyboardButton(text="🔌 Ulanish arizasi yaratish"), KeyboardButton(text="🔧 Texnik xizmat yaratish")],
            [KeyboardButton(text="🕐 Real vaqtda kuzatish")],
            [KeyboardButton(text="👥 Xodimlar faoliyati"), KeyboardButton(text="🔄 Status o'zgartirish")],
            [KeyboardButton(text="📤 Export"), KeyboardButton(text="🌐 Tilni o'zgartirish")],
        ]
    else:  # ruscha
        keyboard = [
            [KeyboardButton(text="📥 Входящие"), KeyboardButton(text="📋 Все заявки")],
            [KeyboardButton(text="🔌 Создать заявку на подключение"), KeyboardButton(text="🔧 Создать заявку на тех. обслуживание")],
            [KeyboardButton(text="🕐 Мониторинг в реальном времени"), KeyboardButton(text="📊 Мониторинг")],
            [KeyboardButton(text="👥 Активность сотрудников"), KeyboardButton(text="🔄 Изменить статус")],
            [KeyboardButton(text="📤 Экспорт"), KeyboardButton(text="🌐 Изменить язык")],
        ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


# Inline keyboards required by handlers

def get_manager_client_search_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=("📱 Telefon" if lang == 'uz' else "📱 Телефон"), callback_data="mgr_search_phone"),
            InlineKeyboardButton(text=("👤 Ism" if lang == 'uz' else "👤 Имя"), callback_data="mgr_search_name"),
        ],
        [
            InlineKeyboardButton(text=("🆔 ID" if lang == 'uz' else "🆔 ID"), callback_data="mgr_search_id"),
            InlineKeyboardButton(text=("➕ Yangi mijoz" if lang == 'uz' else "➕ Новый клиент"), callback_data="mgr_search_new"),
        ],
        [
            InlineKeyboardButton(text=("❌ Bekor qilish" if lang == 'uz' else "❌ Отменить"), callback_data="mgr_cancel_creation"),
        ],
    ])


def get_manager_confirmation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    confirm_text = "✅ Tasdiqlash" if lang == 'uz' else "✅ Подтвердить"
    resend_text = "🔄 Qayta yuborish" if lang == 'uz' else "🔄 Отправить заново"
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=confirm_text, callback_data="mgr_confirm_zayavka"),
            InlineKeyboardButton(text=resend_text, callback_data="mgr_resend_zayavka"),
        ]
    ])


def get_manager_view_applications_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    all_text = "📋 Hammasi" if lang == 'uz' else "📋 Все"
    active_text = "⏳ Faol" if lang == 'uz' else "⏳ Активные"
    completed_text = "✅ Bajarilgan" if lang == 'uz' else "✅ Выполненные"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=all_text, callback_data="mgr_view_all_applications")],
        [InlineKeyboardButton(text=active_text, callback_data="mgr_view_active_applications")],
        [InlineKeyboardButton(text=completed_text, callback_data="mgr_view_completed_applications")],
        [InlineKeyboardButton(text="⬅️ Orqaga" if lang=='uz' else "⬅️ Назад", callback_data="back_to_main_menu")],
    ])


def get_manager_back_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back_to_main_menu")]
    ])


def get_manager_search_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("🔍 Qidirish" if lang == 'uz' else "🔍 Поиск"), callback_data="mgr_search_start")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang=='uz' else "⬅️ Назад"), callback_data="back_to_main_menu")],
    ])


def get_manager_filters_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("🆕 Yangi" if lang=='uz' else "🆕 Новые"), callback_data="mgr_filter_new"),
         InlineKeyboardButton(text=("🔄 Jarayonda" if lang=='uz' else "🔄 В процессе"), callback_data="mgr_filter_in_progress")],
        [InlineKeyboardButton(text=("✅ Bajarilgan" if lang=='uz' else "✅ Выполненные"), callback_data="mgr_filter_completed"),
         InlineKeyboardButton(text=("❌ Bekor qilingan" if lang=='uz' else "❌ Отмененные"), callback_data="mgr_filter_cancelled")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang=='uz' else "⬅️ Назад"), callback_data="back_to_main_menu")]
    ])


def get_status_management_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("📋 Barchasi" if lang=='uz' else "📋 Все"), callback_data="status_view_all_applications")],
        [InlineKeyboardButton(text=("🆕 Yangi" if lang=='uz' else "🆕 Новые"), callback_data="status_view_new_applications")],
        [InlineKeyboardButton(text=("🔄 Jarayonda" if lang=='uz' else "🔄 В процессе"), callback_data="status_view_progress_applications")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang=='uz' else "⬅️ Назад"), callback_data="back_to_status_main")],
    ])


def get_status_navigation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("📋 Barchasi" if lang=='uz' else "📋 Все"), callback_data="status_view_all_applications"),
         InlineKeyboardButton(text=("🆕 Yangi" if lang=='uz' else "🆕 Новые"), callback_data="status_view_new_applications"),
         InlineKeyboardButton(text=("🔄 Jarayonda" if lang=='uz' else "🔄 В процессе"), callback_data="status_view_progress_applications")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang=='uz' else "⬅️ Назад"), callback_data="back_to_status_main")],
    ])


def get_status_keyboard(available_statuses, app_id: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    rows = []
    labels = {
        'new': '🆕 Yangi',
        'in_progress': '🔄 Jarayonda',
        'completed': '✅ Bajarilgan',
        'cancelled': '❌ Bekor qilingan',
    }
    for st in available_statuses:
        rows.append([InlineKeyboardButton(text=labels.get(st, st), callback_data=f"status_{st}_{app_id}")])
    rows.append([InlineKeyboardButton(text=("⬅️ Orqaga" if lang=='uz' else "⬅️ Назад"), callback_data="back_to_status_main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_status_confirmation_keyboard(app_id: str, new_status: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    confirm_text = "✅ Tasdiqlash" if lang == 'uz' else "✅ Подтвердить"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=confirm_text, callback_data=f"confirm_status_change_{app_id}_{new_status}")],
        [InlineKeyboardButton(text=back_text, callback_data="back_to_status_main")],
    ])


def get_inbox_navigation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create navigation keyboard for manager inbox"""
    keyboard = []
    
    # Action buttons
    action_row = []
    
    # View details button
    action_row.append(InlineKeyboardButton(
        text="👁 Ko'rish" if lang == 'uz' else "👁 Просмотр",
        callback_data="mgr_view_app"
    ))
    
    # Contact client button
    action_row.append(InlineKeyboardButton(
        text="📞 Mijoz" if lang == 'uz' else "📞 Клиент",
        callback_data="mgr_contact_client"
    ))
    
    # Assign to junior manager button
    action_row.append(InlineKeyboardButton(
        text="👨‍💼 Kichik menejer" if lang == 'uz' else "👨‍💼 Младший менеджер",
        callback_data="mgr_assign_jm"
    ))
    
    if action_row:
        keyboard.append(action_row)
    

    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_junior_assignment_keyboard(full_id: str, junior_managers: List[Dict], lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create keyboard for assigning to junior managers"""
    keyboard = []
    
    # Junior manager selection buttons
    for jm in junior_managers:
        keyboard.append([InlineKeyboardButton(
            text=f"👨‍💼 {jm.get('full_name', 'N/A')}",
            callback_data=f"mgr_confirm_jm_{full_id}_{jm['id']}"
        )])
    
    # Back button
    keyboard.append([InlineKeyboardButton(
        text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
        callback_data="mgr_back_to_inbox"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_junior_confirmation_keyboard(full_id: str, junior_manager_id: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create confirmation keyboard for junior manager assignment"""
    keyboard = []
    
    # Confirm button
    keyboard.append([InlineKeyboardButton(
        text="✅ Tasdiqlash" if lang == 'uz' else "✅ Подтвердить",
        callback_data=f"mgr_confirm_jm_{full_id}_{junior_manager_id}"
    )])
    
    # Back button
    keyboard.append([InlineKeyboardButton(
        text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
        callback_data="mgr_back_to_inbox"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_actions_keyboard(app_id: str, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create keyboard for application actions"""
    keyboard = []
    
    # Action buttons
    action_row = []
    
    # View details button
    action_row.append(InlineKeyboardButton(
        text="👁 Ko'rish" if lang == 'uz' else "👁 Просмотр",
        callback_data=f"mgr_view_app_{app_id}"
    ))
    
    # Contact client button
    action_row.append(InlineKeyboardButton(
        text="📞 Mijoz" if lang == 'uz' else "📞 Клиент",
        callback_data=f"mgr_contact_client_{app_id}"
    ))
    
    # Assign to junior manager button
    action_row.append(InlineKeyboardButton(
        text="👨‍💼 Kichik menejer" if lang == 'uz' else "👨‍💼 Младший менеджер",
        callback_data=f"mgr_assign_jm_{app_id}"
    ))
    
    if action_row:
        keyboard.append(action_row)
    
    # Close button
    keyboard.append([InlineKeyboardButton(
        text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
        callback_data="mgr_close_app"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_navigation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create navigation keyboard for applications"""
    keyboard = []
    
    # Navigation buttons
    nav_row = []
    
    # Previous button
    nav_row.append(InlineKeyboardButton(
        text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущий",
        callback_data="mgr_app_prev"
    ))
    
    # Next button
    nav_row.append(InlineKeyboardButton(
        text="Keyingi ➡️" if lang == 'uz' else "Следующий ➡️",
        callback_data="mgr_app_next"
    ))
    
    if nav_row:
        keyboard.append(nav_row)
    
    # Back button
    keyboard.append([InlineKeyboardButton(
        text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
        callback_data="mgr_back_to_apps"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_manager_realtime_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create keyboard for manager realtime monitoring"""
    keyboard = []
    
    # Main monitoring options
    main_row = []
    
    # Real-time requests button
    main_row.append(InlineKeyboardButton(
        text="📋 Zayavkalar" if lang == 'uz' else "📋 Заявки",
        callback_data="mgr_realtime_requests"
    ))
    
    # Urgent requests button
    main_row.append(InlineKeyboardButton(
        text="🚨 Shoshilinch" if lang == 'uz' else "🚨 Срочные",
        callback_data="mgr_realtime_urgent"
    ))
    
    if main_row:
        keyboard.append(main_row)
    
    # Secondary options
    secondary_row = []
    
    # Time tracking button
    secondary_row.append(InlineKeyboardButton(
        text="⏱️ Vaqt kuzatish" if lang == 'uz' else "⏱️ Отслеживание времени",
        callback_data="mgr_realtime_time"
    ))
    
    # Workflow history button
    secondary_row.append(InlineKeyboardButton(
        text="📊 Jarayon tarixi" if lang == 'uz' else "📊 История процесса",
        callback_data="mgr_realtime_workflow"
    ))
    
    if secondary_row:
        keyboard.append(secondary_row)
    
    # Back button
    keyboard.append([InlineKeyboardButton(
        text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
        callback_data="mgr_back_to_main"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_realtime_navigation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create navigation keyboard for realtime monitoring"""
    keyboard = []
    
    # Navigation buttons
    nav_row = []
    
    # Previous button
    nav_row.append(InlineKeyboardButton(
        text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущий",
        callback_data="mgr_realtime_prev"
    ))
    
    # Next button
    nav_row.append(InlineKeyboardButton(
        text="Keyingi ➡️" if lang == 'uz' else "Следующий ➡️",
        callback_data="mgr_realtime_next"
    ))
    
    if nav_row:
        keyboard.append(nav_row)
    
    # Back button
    keyboard.append([InlineKeyboardButton(
        text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
        callback_data="mgr_realtime_back"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_realtime_refresh_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create refresh keyboard for realtime monitoring"""
    keyboard = []
    
    # Refresh button
    keyboard.append([InlineKeyboardButton(
        text="🔄 Yangilash" if lang == 'uz' else "🔄 Обновить",
        callback_data="mgr_realtime_refresh"
    )])
    
    # Back button
    keyboard.append([InlineKeyboardButton(
        text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
        callback_data="mgr_realtime_back"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_manager_realtime_monitoring_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create realtime monitoring keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("📡 Signal monitoring" if lang == 'uz' else "📡 Мониторинг сигнала"), callback_data="mgr_rtm_signal")],
        [InlineKeyboardButton(text=("🌐 Network monitoring" if lang == 'uz' else "🌐 Мониторинг сети"), callback_data="mgr_rtm_network")],
        [InlineKeyboardButton(text=("⚡ Performance monitoring" if lang == 'uz' else "⚡ Мониторинг производительности"), callback_data="mgr_rtm_performance")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back_to_main_menu")]
    ])


def get_manager_monitoring_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create monitoring keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("📊 Umumiy statistika" if lang == 'uz' else "📊 Общая статистика"), callback_data="mgr_mon_general")],
        [InlineKeyboardButton(text=("📈 Trend analizi" if lang == 'uz' else "📈 Анализ трендов"), callback_data="mgr_mon_trends")],
        [InlineKeyboardButton(text=("🔍 Detal tahlil" if lang == 'uz' else "🔍 Детальный анализ"), callback_data="mgr_mon_detailed")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back_to_main_menu")]
    ])


def get_manager_staff_activity_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create staff activity keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("👥 Barcha xodimlar" if lang == 'uz' else "👥 Все сотрудники"), callback_data="mgr_staff_all")],
        [InlineKeyboardButton(text=("⏰ Faol xodimlar" if lang == 'uz' else "⏰ Активные сотрудники"), callback_data="mgr_staff_active")],
        [InlineKeyboardButton(text=("📊 Faoliyat statistikasi" if lang == 'uz' else "📊 Статистика активности"), callback_data="mgr_staff_stats")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back_to_main_menu")]
    ])


def get_manager_export_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create export keyboard"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=("📊 Excel export" if lang == 'uz' else "📊 Экспорт в Excel"), callback_data="mgr_export_excel")],
        [InlineKeyboardButton(text=("📄 PDF export" if lang == 'uz' else "📄 Экспорт в PDF"), callback_data="mgr_export_pdf")],
        [InlineKeyboardButton(text=("📋 Word export" if lang == 'uz' else "📋 Экспорт в Word"), callback_data="mgr_export_word")],
        [InlineKeyboardButton(text=("⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"), callback_data="back_to_main_menu")]
    ])
