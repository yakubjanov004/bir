"""
Client Bot Guide Handler - Database Integrated

Shows a simple bot usage guide when the reply button
"Bot qo'llanmasi" / "Инструкция по использованию бота" is pressed.
"""

from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

# Mock database functions to replace database imports
# Global mock storage for demonstration
mock_user_data = {}

async def get_user_by_telegram_id_redis(telegram_id: int):
    """Mock user data from Redis"""
    # Initialize mock data if not exists
    if telegram_id not in mock_user_data:
        mock_user_data[telegram_id] = {
            'id': 1,
            'telegram_id': telegram_id,
            'role': 'client',
            'language': 'uz',
            'full_name': 'Test Client',
            'phone_number': '+998901234567',
            'phone': '+998901234567',
            'address': 'Toshkent shahri, Chilanzor tumani, 15-uy',
            'region': 'toshkent',
            'created_at': '2024-01-01 10:00:00'
        }
    
    return mock_user_data[telegram_id]

# Mock audit logger
class AuditLogger:
    async def log_action(self, user_id: int, action: str, details: dict):
        """Mock audit logging"""
        print(f"Mock Audit Log: User {user_id} performed {action} with details {details}")

audit_logger = AuditLogger()


def get_client_bot_guide_router():
    from aiogram import Router

    router = Router()

    # Role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)

    from keyboards.client_buttons import get_back_keyboard

    @router.message(F.text.in_(["Bot qo'llanmasi", "Инструкция по использованию бота"]))
    async def bot_guide_handler(message: Message, state: FSMContext):
        try:
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            lang = user.get("language", "uz")

            guide_text = (
                """
📘 Bot qo'llanmasi

Quyidagi tavsiyalar orqali botdan samarali foydalaning:

1) Asosiy menyu: kerakli bo'limni tanlang (Ulanish, Texnik xizmat, Operator).
2) Buyurtma berish: kerakli ma'lumotlarni kiriting va tasdiqlang.
3) Profil: ism/manzilni yangilang, arizalaringizni ko'ring.
4) Yordam: tez-tez so'raladigan savollar va yo'riqnoma bilan tanishing.
5) Aloqa: telefon orqali yoki onlayn chat orqali bog'laning.

Maslahat: Har qanday vaqtda "🏠 Asosiy menyu" tugmasi orqali bosh sahifaga qayting.
                """.strip()
                if lang == "uz"
                else
                """
📘 Инструкция по использованию бота

Следуйте рекомендациям, чтобы эффективно пользоваться ботом:

1) Главное меню: выберите нужный раздел (Подключение, Техслужба, Оператор).
2) Оформление заявки: введите данные и подтвердите.
3) Профиль: обновляйте имя/адрес, просматривайте свои заявки.
4) Помощь: ознакомьтесь с ЧаВо и инструкцией.
5) Связь: звоните или используйте онлайн-чат.

Совет: Возвращайтесь на главную через кнопку "🏠 Главное меню" в любое время.
                """.strip()
            )

            await message.answer(guide_text, reply_markup=get_back_keyboard(lang), parse_mode="HTML")
            
            # Log action
            await audit_logger.log_action(
                user_id=user['id'],
                action="view_bot_guide",
                details={}
            )
        except Exception as e:
            print(f"Error in bot_guide_handler: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(F.text.in_(["🏠 Asosiy menyu", "🏠 Главное меню"]))
    async def back_to_main_menu_from_guide(message: Message, state: FSMContext):
        try:
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            lang = user.get("language", "uz")
            from keyboards.client_buttons import get_main_menu_keyboard
            await message.answer(
                "Quyidagi menyudan kerakli bo'limni tanlang." if lang == "uz" else "Выберите нужный раздел из меню ниже.",
                reply_markup=get_main_menu_keyboard(lang)
            )
        except Exception as e:
            print(f"Error in back_to_main_menu_from_guide: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            


    return router
