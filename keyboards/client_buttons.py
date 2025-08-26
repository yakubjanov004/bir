from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from typing import List, Dict, Any


def get_contact_keyboard(lang="uz"):
    """Kontakt ulashish klaviaturasi"""
    share_contact_text = "📱 Kontakt ulashish" if lang == "uz" else "📱 Поделиться контактом"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=share_contact_text, request_contact=True)]],
        resize_keyboard=True
    )
    return keyboard

def get_main_menu_keyboard(lang="uz"):
    """Asosiy menyu klaviaturasi - chiroyli va mantiqiy tartibda"""
    service_order_text = "🔧 Texnik xizmat" if lang == "uz" else "🔧 Техническая служба"
    connection_order_text = "🔌 Ulanish uchun ariza" if lang == "uz" else "🔌 Заявка на подключение"
    contact_operator_text = "📞 Operator bilan bog'lanish" if lang == "uz" else "📞 Связаться с оператором"
    cabinet_text = "👤 Kabinet" if lang == "uz" else "👤 Кабинет"
    bot_guide_text = "Bot qo'llanmasi" if lang == "uz" else "Инструкция по использованию бота"
    change_language_text = "🌐 Til o'zgartirish" if lang == "uz" else "🌐 Изменить язык"
    
    buttons = [
        [
            KeyboardButton(text=connection_order_text),
            KeyboardButton(text=service_order_text)    
        ],
        [
            KeyboardButton(text=contact_operator_text),
            KeyboardButton(text=cabinet_text)
        ],
        [
            KeyboardButton(text=bot_guide_text),
            KeyboardButton(text=change_language_text)
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard

def get_help_menu_keyboard(lang="uz"):
    """Help menu keyboard for client"""
    faq_text = "❓ Tez-tez so'raladigan savollar" if lang == "uz" else "❓ Часто задаваемые вопросы"
    how_to_order_text = "📝 Qanday buyurtma berish" if lang == "uz" else "📝 Как сделать заказ"
    track_order_text = "📍 Buyurtmani kuzatish" if lang == "uz" else "📍 Отслеживание заказа"
    contact_support_text = "📞 Qo'llab-quvvatlash xizmati" if lang == "uz" else "📞 Служба поддержки"
    
    keyboard = [
        [KeyboardButton(text=faq_text)],
        [KeyboardButton(text=how_to_order_text)],
        [KeyboardButton(text=track_order_text)],
        [KeyboardButton(text=contact_support_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_back_to_help_menu_keyboard(lang="uz"):
    """Back to help menu keyboard for client"""
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard = [
        [KeyboardButton(text=back_text)]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_back_to_help_menu_inline(lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline back button for help menu"""
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=back_text, callback_data="client_back_help")]]
    )

def get_back_keyboard(lang="uz"):
    """Foydalanuvchiga har doim faqat 'Asosiy menyu' tugmasini chiqaradi"""
    main_menu_text = "🏠 Asosiy menyu" if lang == "uz" else "🏠 Главное меню"
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=main_menu_text)]
        ],
        resize_keyboard=True
    )
    return keyboard


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

def get_contact_options_keyboard(lang: str = "uz"):

    call_text = "📞 Qo'ng'iroq qilish" if lang == "uz" else "📞 Позвонить"
    chat_text = "💬 Onlayn chat" if lang == "uz" else "💬 Онлайн-чат"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=call_text)],
            [KeyboardButton(text=chat_text, web_app=WebAppInfo(url="https://webapp-gamma-three.vercel.app/"))],
            [KeyboardButton(text=back_text)],
        ],
        resize_keyboard=True,
    )

    return reply_keyboard

def get_language_keyboard(role="client"):
    """Til tanlash klaviaturasi - role asosida callback data"""
    prefix = f"{role}_lang_" if role != "client" else "client_lang_"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data=f"{prefix}uz")],
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data=f"{prefix}ru")]
        ]
    )
    return keyboard

def zayavka_type_keyboard(lang="uz"):
    """Zayavka turini tanlash klaviaturasi - 2 tilda"""
    person_physical_text = "👤 Jismoniy shaxs" if lang == "uz" else "👤 Физическое лицо"
    person_legal_text = "🏢 Yuridik shaxs" if lang == "uz" else "🏢 Юридическое лицо"
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=person_physical_text, callback_data="zayavka_type_b2c")],
            [InlineKeyboardButton(text=person_legal_text, callback_data="zayavka_type_b2b")]
        ]
    )
    return keyboard

def media_attachment_keyboard(lang="uz"):
    """Media biriktirish klaviaturasi - 2 tilda"""
    yes_text = "✅ Ha" if lang == "uz" else "✅ Да"
    no_text = "❌ Yo'q" if lang == "uz" else "❌ Нет"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=yes_text, callback_data="attach_media_yes")],
        [InlineKeyboardButton(text=no_text, callback_data="attach_media_no")]
    ])
    return keyboard

def geolocation_keyboard(lang="uz"):
    """Geolokatsiya klaviaturasi - 2 tilda"""
    yes_text = "✅ Ha" if lang == "uz" else "✅ Да"
    no_text = "❌ Yo'q" if lang == "uz" else "❌ Нет"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=yes_text, callback_data="send_location_yes")],
        [InlineKeyboardButton(text=no_text, callback_data="send_location_no")]
    ])
    return keyboard

def confirmation_keyboard(lang="uz"):
    """Tasdiqlash klaviaturasi - 2 tilda"""
    confirm_text = "✅ Tasdiqlash" if lang == "uz" else "✅ Подтвердить"
    resend_text = "🔄 Qayta yuborish" if lang == "uz" else "🔄 Отправить заново"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=confirm_text, callback_data="confirm_zayavka"),
            InlineKeyboardButton(text=resend_text, callback_data="resend_zayavka")
        ]
    ])
    return keyboard

def get_client_profile_menu(lang="uz"):
    """Client profile menu"""
    view_info_text = "👁️ Ma'lumotlarni ko'rish" if lang == "uz" else "👁️ Просмотр информации"
    view_orders_text = "🔄 Mening arizalarim" if lang == "uz" else "🔄 Мои заявки"
    edit_profile_text = "✏️ Ma'lumotlarni o'zgartirish" if lang == "uz" else "✏️ Редактировать информацию"
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=view_info_text,
                callback_data="client_view_info"
            ),
            InlineKeyboardButton(
                text=view_orders_text,
                callback_data="client_order_stats"
            )
        ],
        [
            InlineKeyboardButton(
                text=edit_profile_text,
                callback_data="client_edit_profile"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_to_profile_menu(lang="uz"):
    """Back button for profile menu"""
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=back_text, callback_data="client_profile_back")]]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_client_profile_reply_keyboard(lang: str = 'uz') -> ReplyKeyboardMarkup:
    """Reply keyboard for client profile (cabinet) section"""
    view_info_text = "👁️ Ma'lumotlarni ko'rish" if lang == 'uz' else "👁️ Просмотр информации"
    view_orders_text = "📋 Mening buyurtmalarim" if lang == 'uz' else "📋 Мои заявки"
    edit_name_text = "✏️ Ismni o'zgartirish" if lang == 'uz' else "✏️ Изменить имя"
    back_text = "◀️ Orqaga" if lang == 'uz' else "◀️ Назад"

    keyboard = [
        [KeyboardButton(text=view_info_text)],
        [KeyboardButton(text=view_orders_text)],
        [KeyboardButton(text=edit_name_text)],
        [KeyboardButton(text=back_text)],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_client_help_menu(lang="uz"):
    """Client help menu"""
    faq_text = "❓ Tez-tez so'raladigan savollar" if lang == "uz" else "❓ Часто задаваемые вопросы"
    contact_support_text = "📞 Qo'llab-quvvatlash xizmati" if lang == "uz" else "📞 Служба поддержки"
    how_to_order_text = "📝 Qanday buyurtma berish" if lang == "uz" else "📝 Как сделать заказ"
    track_order_text = "📍 Buyurtmani kuzatish" if lang == "uz" else "📍 Отслеживание заказа"
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=faq_text,
                callback_data="client_faq"
            )
        ],
        [
            InlineKeyboardButton(
                text=how_to_order_text,
                callback_data="client_how_to_order"
            )
        ],
        [
            InlineKeyboardButton(
                text=track_order_text,
                callback_data="client_track_order"
            )
        ],
        [
            InlineKeyboardButton(
                text=contact_support_text,
                callback_data="client_contact_support"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_cancel_edit_keyboard(lang="uz"):
    """Cancel edit keyboard"""
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отменить"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=cancel_text, callback_data="client_profile_back")]]
    )
    return keyboard

def get_edit_profile_keyboard(lang="uz"):
    """Edit profile keyboard"""
    edit_name_text = "✏️ Ism o'zgartirish" if lang == "uz" else "✏️ Изменить имя"
    edit_address_text = "📍 Manzil o'zgartirish" if lang == "uz" else "📍 Изменить адрес"
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=edit_name_text,
                callback_data="client_edit_name"
            )
        ],
        [
            InlineKeyboardButton(
                text=edit_address_text,
                callback_data="client_edit_address"
            )
        ],
        [
            InlineKeyboardButton(
                text=back_text,
                callback_data="client_profile_back"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def technical_service_keyboard(lang="uz"):
    """Technical service request keyboard"""
    confirm_text = "✅ Tasdiqlash" if lang == "uz" else "✅ Подтвердить"
    cancel_text = "❌ Bekor qilish" if lang == "uz" else "❌ Отменить"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=confirm_text, callback_data="confirm_technical_request")],
        [InlineKeyboardButton(text=cancel_text, callback_data="cancel_technical_request")]
    ])
    return keyboard

def get_orders_menu_keyboard(lang="uz"):
    """Orders menu keyboard"""
    all_orders_text = "📋 Barcha buyurtmalar" if lang == "uz" else "📋 Все заказы"
    active_orders_text = "⏳ Faol buyurtmalar" if lang == "uz" else "⏳ Активные заказы"
    completed_orders_text = "✅ Bajarilgan buyurtmalar" if lang == "uz" else "✅ Выполненные заказы"
    
    keyboard = [
        [
            InlineKeyboardButton(
                text=all_orders_text,
                callback_data="client_view_all_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text=active_orders_text,
                callback_data="client_view_active_orders"
            )
        ],
        [
            InlineKeyboardButton(
                text=completed_orders_text,
                callback_data="client_view_completed_orders"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_back_to_orders_menu_keyboard(lang="uz"):
    """Back to orders menu keyboard"""
    back_text = "◀️ Orqaga" if lang == "uz" else "◀️ Назад"
    keyboard = [
        [InlineKeyboardButton(
            text=back_text,
            callback_data="client_orders_back"
        )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_client_main_keyboard(lang="uz"):
    """Client main keyboard - returns main menu keyboard"""
    return get_main_menu_keyboard(lang)

# New centralized keyboard functions for client module
def get_client_regions_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Regions selection keyboard for client"""
    keyboard = [
        [
            InlineKeyboardButton(text="Toshkent shahri", callback_data="region_toshkent_city"),
            InlineKeyboardButton(text="Toshkent viloyati", callback_data="region_toshkent_region")
        ],
        [
            InlineKeyboardButton(text="Andijon", callback_data="region_andijon"),
            InlineKeyboardButton(text="Farg'ona", callback_data="region_fergana")
        ],
        [
            InlineKeyboardButton(text="Namangan", callback_data="region_namangan"),
            InlineKeyboardButton(text="Sirdaryo", callback_data="region_sirdaryo")
        ],
        [
            InlineKeyboardButton(text="Jizzax", callback_data="region_jizzax"),
            InlineKeyboardButton(text="Samarqand", callback_data="region_samarkand")
        ],
        [
            InlineKeyboardButton(text="Buxoro", callback_data="region_bukhara"),
            InlineKeyboardButton(text="Navoiy", callback_data="region_navoi")
        ],
        [
            InlineKeyboardButton(text="Qashqadaryo", callback_data="region_kashkadarya"),
            InlineKeyboardButton(text="Surxondaryo", callback_data="region_surkhandarya")
        ],
        [
            InlineKeyboardButton(text="Xorazm", callback_data="region_khorezm"),
            InlineKeyboardButton(text="Qoraqalpog'iston", callback_data="region_karakalpakstan")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_client_tariff_selection_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Tariff selection keyboard for client"""
    keyboard = [
        [
            InlineKeyboardButton(text="Standard", callback_data="tariff_standard"),
            InlineKeyboardButton(text="Yangi", callback_data="tariff_new")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_client_profile_back_keyboard(lang: str = 'uz') -> InlineKeyboardMarkup:
    """Back to profile keyboard for client"""
    back_text = "⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад"
    keyboard = [
        [InlineKeyboardButton(text=back_text, callback_data="client_profile_back")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_client_orders_navigation_keyboard(current_index: int, current_page: int, total_pages: int, orders_on_page: int, order_id: int, lang: str = 'uz') -> InlineKeyboardMarkup:
    """Create navigation keyboard for orders"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0 or current_page > 1:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data=f"order_prev_{current_index}_{current_page}_{order_id}"
        ))
    
    # Next button
    if current_index < orders_on_page - 1 or current_page < total_pages:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data=f"order_next_{current_index}_{current_page}_{order_id}"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
        
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
