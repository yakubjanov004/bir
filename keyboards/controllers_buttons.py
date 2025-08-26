from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Any


def get_controller_main_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Controller uchun asosiy reply keyboard"""
    if lang == 'uz':
        keyboard = [
            [KeyboardButton(text="📥 Inbox"), KeyboardButton(text="📋 Arizalarni ko'rish")],
            [KeyboardButton(text="🔌 Ulanish arizasi yaratish"), KeyboardButton(text="🔧 Texnik xizmat yaratish")],
            [KeyboardButton(text="🕐 Real vaqtda kuzatish"), KeyboardButton(text="📊 Monitoring")],
            [KeyboardButton(text="👥 Xodimlar faoliyati"), KeyboardButton(text="📤 Export")],
            [KeyboardButton(text="🌐 Tilni o'zgartirish")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="📥 Входящие"), KeyboardButton(text="📋 Просмотр заявок")],
            [KeyboardButton(text="🔌 Создать заявку на подключение"), KeyboardButton(text="🔧 Создать техническую заявку")],
            [KeyboardButton(text="🕐 Мониторинг в реальном времени"), KeyboardButton(text="📊 Мониторинг")],
            [KeyboardButton(text="👥 Активность сотрудников"), KeyboardButton(text="📤 Экспорт")],
            [KeyboardButton(text="🌐 Изменить язык")]
        ]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def controllers_main_menu(lang='uz'):
    """Legacy function - redirects to new function"""
    return get_controller_main_keyboard(lang)


# Controller-specific inline keyboards mirroring client keyboards

def get_controller_regions_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Toshkent shahri", callback_data="ctrl_region_toshkent_city"),
            InlineKeyboardButton(text="Toshkent viloyati", callback_data="ctrl_region_toshkent_region")
        ],
        [
            InlineKeyboardButton(text="Andijon", callback_data="ctrl_region_andijon"),
            InlineKeyboardButton(text="Farg'ona", callback_data="ctrl_region_fergana")
        ],
        [
            InlineKeyboardButton(text="Namangan", callback_data="ctrl_region_namangan"),
            InlineKeyboardButton(text="Sirdaryo", callback_data="ctrl_region_sirdaryo")
        ],
        [
            InlineKeyboardButton(text="Jizzax", callback_data="ctrl_region_jizzax"),
            InlineKeyboardButton(text="Samarqand", callback_data="ctrl_region_samarkand")
        ],
        [
            InlineKeyboardButton(text="Buxoro", callback_data="ctrl_region_bukhara"),
            InlineKeyboardButton(text="Navoiy", callback_data="ctrl_region_navoi")
        ],
        [
            InlineKeyboardButton(text="Qashqadaryo", callback_data="ctrl_region_kashkadarya"),
            InlineKeyboardButton(text="Surxondaryo", callback_data="ctrl_region_surkhandarya")
        ],
        [
            InlineKeyboardButton(text="Xorazm", callback_data="ctrl_region_khorezm"),
            InlineKeyboardButton(text="Qoraqalpog'iston", callback_data="ctrl_region_karakalpakstan")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def controller_zayavka_type_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    person_physical_text = "👤 Jismoniy shaxs" if lang == "uz" else "👤 Физическое лицо"
    person_legal_text = "🏢 Yuridik shaxs" if lang == "uz" else "🏢 Юридическое лицо"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=person_physical_text, callback_data="ctrl_zayavka_type_b2c")],
            [InlineKeyboardButton(text=person_legal_text, callback_data="ctrl_zayavka_type_b2b")]
        ]
    )
    return keyboard


def controller_media_attachment_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    yes_text = "✅ Ha" if lang == "uz" else "✅ Да"
    no_text = "❌ Yo'q" if lang == "uz" else "❌ Нет"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=yes_text, callback_data="ctrl_attach_media_yes")],
        [InlineKeyboardButton(text=no_text, callback_data="ctrl_attach_media_no")]
    ])
    return keyboard


def controller_geolocation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    yes_text = "✅ Ha" if lang == "uz" else "✅ Да"
    no_text = "❌ Yo'q" if lang == "uz" else "❌ Нет"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=yes_text, callback_data="ctrl_send_location_yes")],
        [InlineKeyboardButton(text=no_text, callback_data="ctrl_send_location_no")]
    ])
    return keyboard


def controller_confirmation_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    confirm_text = "✅ Tasdiqlash" if lang == "uz" else "✅ Подтвердить"
    resend_text = "🔄 Qayta yuborish" if lang == "uz" else "🔄 Отправить заново"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=confirm_text, callback_data="ctrl_confirm_zayavka"),
            InlineKeyboardButton(text=resend_text, callback_data="ctrl_resend_zayavka")
        ]
    ])
    return keyboard


def get_controller_tariff_selection_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Standard", callback_data="ctrl_tariff_standard"),
            InlineKeyboardButton(text="Yangi", callback_data="ctrl_tariff_new")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_application_creator_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=("📱 Telefon" if lang == 'uz' else "📱 Телефон"), callback_data="ctrl_search_phone"),
            InlineKeyboardButton(text=("👤 Ism" if lang == 'uz' else "👤 Имя"), callback_data="ctrl_search_name")
        ],
        [
            InlineKeyboardButton(text=("🆔 ID" if lang == 'uz' else "🆔 ID"), callback_data="ctrl_search_id"),
            InlineKeyboardButton(text=("➕ Yangi mijoz" if lang == 'uz' else "➕ Новый клиент"), callback_data="ctrl_search_new")
        ],
        [
            InlineKeyboardButton(text=("❌ Bekor qilish" if lang == 'uz' else "❌ Отменить"), callback_data="ctrl_cancel_creation")
        ]
    ])


# Realtime monitoring keyboards for controller

def get_realtime_monitoring_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    status_text = "🟢 Jonli holat" if lang == 'uz' else "🟢 Живой статус"
    activities_text = "📝 Faoliyatlar" if lang == 'uz' else "📝 Активности"
    alerts_text = "⚠️ Ogohlantirishlar" if lang == 'uz' else "⚠️ Оповещения"
    performance_text = "📈 Ko'rsatkichlar" if lang == 'uz' else "📈 Показатели"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=status_text, callback_data='ctrl_realtime_status')],
        [InlineKeyboardButton(text=activities_text, callback_data='ctrl_realtime_activities')],
        [InlineKeyboardButton(text=alerts_text, callback_data='ctrl_realtime_alerts')],
        [InlineKeyboardButton(text=performance_text, callback_data='ctrl_realtime_performance')],
    ])


def get_realtime_refresh_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    refresh_text = "🔄 Yangilash" if lang == 'uz' else "🔄 Обновить"
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=refresh_text, callback_data='ctrl_realtime_refresh')],
        [InlineKeyboardButton(text=back_text, callback_data='controllers_back')],
    ])


# Inbox helpers
def build_inbox_request_keyboard(
    can_prev: bool,
    can_next: bool,
    request_full_id: str,
    lang: str = 'uz'
) -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    # Assign buttons
    rows.append([
        InlineKeyboardButton(text=("📞 Call Center Supervisorga yuborish" if lang=='uz' else "📞 Отправить супервайзеру CC"), callback_data=f"ctrl_assign_ccsupervisor_{request_full_id}"),
        InlineKeyboardButton(text=("🔧 Texnik tanlash" if lang=='uz' else "🔧 Назначить техника"), callback_data=f"ctrl_assign_tech_{request_full_id}"),
    ])
    # Navigation
    nav: List[InlineKeyboardButton] = []
    if can_prev:
        nav.append(InlineKeyboardButton(text=("⬅️ Oldingi" if lang=='uz' else "⬅️ Предыдущая"), callback_data="ctrl_prev_any"))
    if can_next:
        nav.append(InlineKeyboardButton(text=("Keyingi ➡️" if lang=='uz' else "Следующая ➡️"), callback_data="ctrl_next_any"))
    if nav:
        rows.append(nav)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_inbox_technicians_keyboard(request_full_id: str, technicians: List[Dict[str, Any]], lang: str = 'uz') -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for tech in technicians:
        rows.append([
            InlineKeyboardButton(
                text=f"🔧 {tech.get('full_name','N/A')} ({tech.get('specialization','Texnik')}) - {tech.get('active_requests',0)} ariza",
                callback_data=f"ctrl_select_tech_{request_full_id}_{tech['id']}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# Export helpers
def build_export_types_keyboard(export_types: List[str], lang: str = 'uz') -> InlineKeyboardMarkup:
    names = {
        'uz': {'orders': '📑 Buyurtmalar','statistics': '📊 Statistika','users': '👥 Texniklar','reports': '📋 Hisobotlar','quality': '🎯 Sifat nazorati'},
        'ru': {'orders': '📑 Заказы','statistics': '📊 Статистика','users': '👥 Техники','reports': '📋 Отчеты','quality': '🎯 Контроль качества'},
    }[lang]
    rows: List[List[InlineKeyboardButton]] = []
    for t in export_types:
        rows.append([InlineKeyboardButton(text=names.get(t, t), callback_data=f"controller_export_{t}")])
    rows.append([InlineKeyboardButton(text=("◀️ Orqaga" if lang=='uz' else "◀️ Назад"), callback_data="controller_export_back_main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_export_formats_keyboard(formats: List[str], lang: str = 'uz') -> InlineKeyboardMarkup:
    labels = {'csv': 'CSV', 'xlsx': 'Excel', 'docx': 'Word', 'pdf': 'PDF'}
    rows: List[List[InlineKeyboardButton]] = []
    for fmt in formats:
        rows.append([InlineKeyboardButton(text=labels.get(fmt, fmt.upper()), callback_data=f"controller_format_{fmt}")])
    rows.append([InlineKeyboardButton(text=("◀️ Orqaga" if lang=='uz' else "◀️ Назад"), callback_data="controller_export_back_types")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# Language helpers (reply)
def build_language_reply_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    back_text = "🔙 Orqaga" if lang=='uz' else "🔙 Назад"
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("🇺🇿 O'zbekcha")],[KeyboardButton(back_text)]],
        resize_keyboard=True
    )


# Monitoring helpers (for controller monitoring.py)
def get_monitoring_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    detailed_text = "📊 Batafsil statistika" if lang == 'uz' else "📊 Подробная статистика"
    system_text = "🖥️ Tizim holati" if lang == 'uz' else "🖥️ Состояние системы"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=detailed_text, callback_data='view_detailed_statistics')],
        [InlineKeyboardButton(text=system_text, callback_data='view_system_status')],
    ])


def get_controller_back_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=back_text, callback_data='back_to_monitoring')]
    ])


def get_monitoring_detailed_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=back_text, callback_data='back_to_monitoring')]
    ])
