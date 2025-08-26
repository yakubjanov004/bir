"""
Client Contact Handler - Database Integrated

This module handles client contact functionality.
"""

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.client_states import ContactStates, MainMenuStates
from filters.role_filter import RoleFilter

# Mock database functions to replace database imports
async def get_user_by_telegram_id_redis(telegram_id: int):
    """Mock user data from Redis"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'client',
        'language': 'uz',
        'full_name': 'Test Client',
        'phone_number': '+998901234567'
    }

# Mock audit logger
class AuditLogger:
    async def log_action(self, user_id: int, action: str, details: dict):
        """Mock audit logging"""
        print(f"Mock Audit Log: User {user_id} performed {action} with details {details}")

audit_logger = AuditLogger()

def get_client_contact_router():
    """Get client contact router with role filtering"""
    from aiogram import Router
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📞 Operator bilan bog'lanish", "📞 Связаться с оператором"]))
    async def contact_handler(message: Message, state: FSMContext):
        """Handle contact request"""
        try:
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            lang = user.get('language', 'uz')
            
            contact_text = (
                "📞 <b>Biz bilan bog'lanish</b>\n\n"
                "📱 <b>Telefon:</b> +998 71 123 45 67\n"
                "📧 <b>Email:</b> info@alfaconnect.uz\n"
                "🌐 <b>Veb-sayt:</b> www.alfaconnect.uz\n"
                "📍 <b>Manzil:</b> Toshkent shahri, Yunusobod tumani\n"
                "⏰ <b>Ish vaqti:</b> Dushanba - Shanba, 9:00 - 18:00\n\n"
                "💬 <b>Telegram kanal:</b> @alfaconnect_uz"
                if lang == 'uz' else
                "📞 <b>Связаться с нами</b>\n\n"
                "📱 <b>Телефон:</b> +998 71 123 45 67\n"
                "📧 <b>Email:</b> info@alfaconnect.uz\n"
                "🌐 <b>Веб-сайт:</b> www.alfaconnect.uz\n"
                "📍 <b>Адрес:</b> г. Ташкент, Юнусабадский район\n"
                "⏰ <b>Время работы:</b> Понедельник - Суббота, 9:00 - 18:00\n\n"
                "💬 <b>Telegram канал:</b> @alfaconnect_uz"
            )
            
            from keyboards.client_buttons import get_contact_options_keyboard
            keyboard = get_contact_options_keyboard(lang)
            
            await message.answer(contact_text, reply_markup=keyboard, parse_mode='HTML')
            await state.set_state(ContactStates.viewing_contact)
            
            # Log action
            await audit_logger.log_action(
                user_id=user['id'],
                action="view_contact_info",
                details={}
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(F.text.in_(["📞 Qo'ng'iroq qilish", "📞 Позвонить"]))
    async def contact_make_call(message: Message, state: FSMContext):
        """Send phone link and keep contact menu"""
        try:
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            lang = user.get('language', 'uz')
            phone_display = "+998 71 123 45 67"
            phone_link = "+998711234567"

            if lang == 'uz':
                text = (
                    f"📱 <b>Telefon:</b> {phone_link}\n\n"
                    "Telefon orqali bog'lanish uchun yuqoridagi raqamni bosing."
                )
            else:
                text = (
                    f"📱 <b>Телефон:</b> {phone_link}\n\n"
                    "Для связи по телефону нажмите на номер выше."
                )
            from keyboards.client_buttons import get_contact_options_keyboard
            await message.answer(text, reply_markup=get_contact_options_keyboard(lang), parse_mode='HTML', disable_web_page_preview=True)
            await state.set_state(ContactStates.viewing_contact)
        except Exception:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(F.web_app_data)
    async def contact_webapp_data(message: Message, state: FSMContext):
        """Handle WebApp chat payload"""
        try:
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            lang = user.get('language', 'uz')
            payload = message.web_app_data.data if message.web_app_data else ""
            ok_text = (
                "✅ Xabar qabul qilindi. Operator tez orada javob beradi."
                if lang == 'uz' else
                "✅ Сообщение получено. Оператор скоро ответит."
            )
            if payload:
                ok_text += f"\n\n<code>{payload}</code>"
            from keyboards.client_buttons import get_contact_options_keyboard
            await message.answer(ok_text, reply_markup=get_contact_options_keyboard(lang), parse_mode='HTML')
            await state.set_state(ContactStates.viewing_contact)
        except Exception:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(F.text.in_(["◀️ Orqaga", "◀️ Назад"]))
    async def contact_back_to_main(message: Message, state: FSMContext):
        """Return to main menu"""
        try:
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            lang = user.get('language', 'uz')
            from keyboards.client_buttons import get_main_menu_keyboard
            text = (
                "Quyidagi menyudan kerakli bo'limni tanlang."
                if lang == 'uz' else
                "Выберите нужный раздел из меню ниже."
            )
            await message.answer(text, reply_markup=get_main_menu_keyboard(lang))
            await state.set_state(MainMenuStates.main_menu)
        except Exception:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    return router
