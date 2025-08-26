from typing import List, Dict, Any
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


# Main menu keyboards
def get_junior_manager_main_menu(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Junior manager main menu (reply keyboard)."""
    inbox_text = "📥 Inbox"
    view_apps_text = "📋 Arizalarni ko'rish" if lang == "uz" else "📋 Просмотр заявок"
    create_connection_text = (
        "🔌 Ulanish arizasi yaratish" if lang == "uz" else "🔌 Создать заявку на подключение"
    )
    client_search_text = "🔍 Mijoz qidiruv" if lang == "uz" else "🔍 Поиск клиентов"
    statistics_text = "📊 Statistika" if lang == "uz" else "📊 Статистика"
    change_lang_text = "🌐 Tilni o'zgartirish" if lang == "uz" else "🌐 Изменить язык"

    keyboard = [
        [KeyboardButton(text=inbox_text), KeyboardButton(text=view_apps_text)],
        [KeyboardButton(text=create_connection_text), KeyboardButton(text=client_search_text)],
        [KeyboardButton(text=statistics_text), KeyboardButton(text=change_lang_text)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_junior_manager_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Alias used by role system to get main menu keyboard."""
    return get_junior_manager_main_menu(lang)


# Language selection
def get_language_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Language selection inline keyboard for junior manager."""
    uz_text = "🇺🇿 O'zbekcha" if lang == "uz" else "🇺🇿 Узбекский"
    ru_text = "🇷🇺 Ruscha" if lang == "uz" else "🇷🇺 Русский"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=uz_text, callback_data="jm_lang_uz")],
            [InlineKeyboardButton(text=ru_text, callback_data="jm_lang_ru")],
        ]
    )


# Client search helpers
def get_client_search_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Simple reply keyboard shown on client search prompt (back to main)."""
    back_text = "🏠 Asosiy menyu" if lang == "uz" else "🏠 Главное меню"
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=back_text)]],
        resize_keyboard=True,
    )


def get_junior_manager_back_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Reply keyboard with a single back-to-main button."""
    back_text = "🏠 Asosiy menyu" if lang == "uz" else "🏠 Главное меню"
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=back_text)]],
        resize_keyboard=True,
    )


def get_clients_navigation_keyboard(current_index: int, total_clients: int, lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline navigation for client list (prev/next)."""
    nav_row: List[InlineKeyboardButton] = []
    if current_index > 0:
        nav_row.append(
            InlineKeyboardButton(
                text=("⬅️ Oldingi" if lang == "uz" else "⬅️ Предыдущий"),
                callback_data="client_prev",
            )
        )
    if current_index < max(0, total_clients - 1):
        nav_row.append(
            InlineKeyboardButton(
                text=("Keyingi ➡️" if lang == "uz" else "Следующий ➡️"),
                callback_data="client_next",
            )
        )
    keyboard: List[List[InlineKeyboardButton]] = []
    if nav_row:
        keyboard.append(nav_row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Application list and actions
def get_application_list_keyboard(
    applications: List[Dict[str, Any]], page: int = 0, lang: str = "uz"
) -> InlineKeyboardMarkup:
    """Generate an inline keyboard for applications list with pagination (5 per page)."""
    start_idx = page * 5
    end_idx = min(start_idx + 5, len(applications))

    rows: List[List[InlineKeyboardButton]] = []
    for i in range(start_idx, end_idx):
        app = applications[i]
        app_id = app.get("id", i + 1)
        client_name = (app.get("client_name") or app.get("client") or "N/A")
        label = f"#{app_id} - {str(client_name)[:20]}"
        rows.append(
            [InlineKeyboardButton(text=label, callback_data=f"jm_view_app_{app_id}")]
        )

    nav_buttons: List[InlineKeyboardButton] = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                text=("⬅️ Oldingi" if lang == "uz" else "⬅️ Предыдущая"),
                callback_data=f"jm_apps_page_{page-1}",
            )
        )
    if end_idx < len(applications):
        nav_buttons.append(
            InlineKeyboardButton(
                text=("Keyingi ➡️" if lang == "uz" else "Следующая ➡️"),
                callback_data=f"jm_apps_page_{page+1}",
            )
        )
    if nav_buttons:
        rows.append(nav_buttons)

    rows.append(
        [
            InlineKeyboardButton(
                text=("❌ Yopish" if lang == "uz" else "❌ Закрыть"),
                callback_data="jm_close_menu",
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_application_action_keyboard(app_id: int, status: str, lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline actions for a specific application (cancel/close)."""
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отменить"
    close_text = "❌ Yopish" if lang == "uz" else "❌ Закрыть"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=cancel_text, callback_data=f"jm_cancel_app_{app_id}")],
            [InlineKeyboardButton(text=close_text, callback_data="jm_close_menu")],
        ]
    )


# Inbox helpers
def get_contact_note_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Keyboard shown while entering contact note (cancel/back)."""
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отмена"
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=cancel_text, callback_data="jm_back_to_application")]]
    )


def get_controller_note_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Keyboard for controller note entry (cancel/back)."""
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отмена"
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=cancel_text, callback_data="jm_back_to_application")]]
    )


def get_send_to_controller_confirmation_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Confirmation keyboard to send application to controller."""
    confirm_text = "✅ Yuborish" if lang == "uz" else "✅ Отправить"
    edit_text = "✏️ Tahrirlash" if lang == "uz" else "✏️ Редактировать"
    back_text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=confirm_text, callback_data="jm_confirm_send_to_controller")],
            [InlineKeyboardButton(text=edit_text, callback_data="jm_edit_controller_note")],
            [InlineKeyboardButton(text=back_text, callback_data="jm_back_to_application")],
        ]
    )


def get_edit_controller_note_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Keyboard for editing controller note (cancel/back)."""
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отмена"
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=cancel_text, callback_data="jm_back_to_application")]]
    )


def get_back_to_application_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Single back-to-application button keyboard."""
    back_text = "⬅️ Orqaga qaytish" if lang == "uz" else "⬅️ Вернуться назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=back_text, callback_data="jm_back_to_application")]]
    )


# Application creation helpers
def get_client_search_menu(lang: str = "uz") -> InlineKeyboardMarkup:
    """Client search method selection used in application creation flow."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=("📱 Telefon" if lang == "uz" else "📱 Телефон"),
                    callback_data="jm_search_phone",
                ),
                InlineKeyboardButton(
                    text=("👤 Ism" if lang == "uz" else "👤 Имя"),
                    callback_data="jm_search_name",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=("🆔 ID" if lang == "uz" else "🆔 ID"),
                    callback_data="jm_search_id",
                ),
                InlineKeyboardButton(
                    text=("➕ Yangi mijoz" if lang == "uz" else "➕ Новый клиент"),
                    callback_data="jm_search_new",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=("❌ Bekor qilish" if lang == "uz" else "❌ Отмена"),
                    callback_data="jm_cancel_creation",
                )
            ],
        ]
    )


def get_application_priority_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Priority selection for application creation."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=("🟢 Past" if lang == "uz" else "🟢 Низкий"),
                    callback_data="jm_priority_low",
                ),
                InlineKeyboardButton(
                    text=("🟡 O'rta" if lang == "uz" else "🟡 Средний"),
                    callback_data="jm_priority_medium",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=("🟠 Yuqori" if lang == "uz" else "🟠 Высокий"),
                    callback_data="jm_priority_high",
                ),
                InlineKeyboardButton(
                    text=("🔴 Shoshilinch" if lang == "uz" else "🔴 Срочный"),
                    callback_data="jm_priority_urgent",
                ),
            ],
        ]
    )


def get_application_confirmation_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Confirmation UI for application creation."""
    confirm_text = "✅ Tasdiqlash" if lang == "uz" else "✅ Подтвердить"
    back_text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=confirm_text, callback_data="jm_confirm_application")],
            [InlineKeyboardButton(text=back_text, callback_data="jm_back_to_application")],
        ]
    )


# Statistics keyboards
def get_statistics_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Main statistics menu for junior manager."""
    detailed_text = "📊 Batafsil statistika" if lang == "uz" else "📊 Подробная статистика"
    close_text = "❌ Yopish" if lang == "uz" else "❌ Закрыть"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=detailed_text, callback_data="view_detailed_statistics")],
            [InlineKeyboardButton(text=close_text, callback_data="jm_close_menu")],
        ]
    )


def get_detailed_statistics_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Detailed statistics navigation keyboard."""
    back_text = "⬅️ Orqaga" if lang == "uz" else "⬅️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=back_text, callback_data="back_to_statistics")]]
    )


