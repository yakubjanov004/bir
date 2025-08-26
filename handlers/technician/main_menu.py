from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from datetime import datetime
from keyboards.technician_buttons import get_technician_main_menu_keyboard, get_back_technician_keyboard, get_language_keyboard, get_reports_keyboard, get_help_request_types_keyboard
from states.technician_states import TechnicianMainMenuStates
from filters.role_filter import RoleFilter

def get_technician_main_menu_router():
    """Technician main menu router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("technician")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔧 Technician", "🔧 Texnik", "/start"]))
    async def technician_start(message: Message, state: FSMContext):
        """Technician start handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            
            await state.set_state(TechnicianMainMenuStates.main_menu)
            lang = user.get('language', 'uz')
            
            welcome_text = f"""
🔧 <b>Technician Panel</b>

👋 Xush kelibsiz, {user.get('full_name', 'Texnik xodimi')}!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Controllerdan kelgan zayavkalarni qabul qilish
• 🔍 Manzilga borib diagnostika qo'yish
• 📦 Ombor yordami kerakligini hal qilish
• 🛠️ Muammolarni hal qilish va ishlarni bajarish
• ✅ Zayavkalarni yakunlash va mijozga xabar berish
            """
            
            await message.answer(
                welcome_text.strip(),
                parse_mode='HTML',
                reply_markup=get_technician_main_menu_keyboard(lang)
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "tech_main_menu")
    async def tech_back_to_main_menu(callback: CallbackQuery, state: FSMContext):
        """Back to main menu handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            
            await state.set_state(TechnicianMainMenuStates.main_menu)
            lang = user.get('language', 'uz')
            
            welcome_text = f"""
🔧 <b>Technician Panel</b>

👤 {user.get('full_name', 'Texnik xodimi')}
📊 Asosiy menyu

Kerakli bo'limni tanlang:
            """
            
            await callback.message.edit_text(
                welcome_text.strip(),
                parse_mode='HTML',
                reply_markup=get_technician_main_menu_keyboard(lang)
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_back")
    async def tech_back_handler(callback: CallbackQuery, state: FSMContext):
        """Back handler"""
        try:
            await tech_back_to_main_menu(callback, state)
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(F.text == "🌐 Tilni o'zgartirish")
    async def change_language_handler(message: Message, state: FSMContext):
        """Change language handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            
            lang = user.get('language', 'uz')
            text = "🌐 Tilni tanlang:"
            
            await message.answer(
                text,
                reply_markup=get_language_keyboard()
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("tech_lang_"))
    async def set_language_callback(callback: CallbackQuery, state: FSMContext):
        """Set language callback"""
        try:
            new_lang = callback.data.replace("tech_lang_", "")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': new_lang,
                'role': 'technician'
            }
            
            text = "✅ Til muvaffaqiyatli o'zgartirildi!"
            await callback.answer(text, show_alert=True)
            
            await tech_back_to_main_menu(callback, state)
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(F.text == "📋 Vazifalarim")
    async def my_tasks_handler(message: Message, state: FSMContext):
        """My tasks handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            
            lang = user.get('language', 'uz')
            
            text = f"""
📋 <b>Vazifalarim</b>

🔧 Texnik xizmat arizalari
📥 Inbox - tayinlangan arizalar
📊 Hisobotlar - ish natijalari
🆘 Yordam - qo'llab-quvvatlash

Kerakli bo'limni tanlang:
            """
            
            await message.answer(
                text.strip(),
                parse_mode='HTML',
                reply_markup=get_technician_main_menu_keyboard(lang)
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "📊 Hisobotlar")
    async def reports_handler(message: Message, state: FSMContext):
        """Reports handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            
            lang = user.get('language', 'uz')
            
            text = f"""
📊 <b>Hisobotlar</b>

📈 Kunlik hisobot
📊 Haftalik hisobot
📋 Oylik hisobot
📋 Ish natijalari

Kerakli hisobotni tanlang:
            """
            
            await message.answer(
                text.strip(),
                parse_mode='HTML',
                reply_markup=get_reports_keyboard(lang)
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "🆘 Yordam")
    async def help_handler(message: Message, state: FSMContext):
        """Help handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            
            lang = user.get('language', 'uz')
            
            text = f"""
🆘 <b>Yordam</b>

📞 Manager bilan bog'lanish
🔧 Texnik yordam
📦 Ombor bilan bog'lanish
🚨 Shoshilinch holatlar

Kerakli yordam turini tanlang:
            """
            
            await message.answer(
                text.strip(),
                parse_mode='HTML',
                reply_markup=get_help_request_types_keyboard(lang)
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "📥 Inbox")
    async def inbox_handler(message: Message, state: FSMContext):
        """Inbox handler"""
        try:
            # Check user role first - only process if user is technician
            from loader import get_user_role
            user_role = get_user_role(message.from_user.id)
            if user_role != 'technician':
                return  # Skip processing for non-technician users
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            
            lang = user.get('language', 'uz')
            
            text = f"""
📥 <b>Inbox</b>

📋 Tayinlangan arizalar
📊 Holatlar
📈 Statistika

Kerakli bo'limni tanlang:
            """
            
            await message.answer(
                text.strip(),
                parse_mode='HTML',
                reply_markup=get_technician_main_menu_keyboard(lang)
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "🔧 Texnik xizmat")
    async def technical_service_handler(message: Message, state: FSMContext):
        """Technical service handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            
            lang = user.get('language', 'uz')
            
            text = f"""
🔧 <b>Texnik xizmat</b>

🛠️ Muammolarni hal qilish
🔍 Diagnostika
📦 Materiallar
✅ Yakunlash

Kerakli bo'limni tanlang:
            """
            
            await message.answer(
                text.strip(),
                parse_mode='HTML',
                reply_markup=get_technician_main_menu_keyboard(lang)
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "📞 Manager bilan bog'lanish")
    async def contact_manager_handler(message: Message, state: FSMContext):
        """Contact manager handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            
            lang = user.get('language', 'uz')
            
            text = f"""
📞 <b>Manager bilan bog'lanish</b>

👤 Manager: +998901234567
📧 Email: manager@example.com
💬 Telegram: @manager_bot

Xabar yuborish uchun tugmani bosing:
            """
            
            await message.answer(
                text.strip(),
                parse_mode='HTML',
                reply_markup=get_back_technician_keyboard(lang)
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "🔧 Texnik yordam")
    async def technical_help_handler(message: Message, state: FSMContext):
        """Technical help handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            
            lang = user.get('language', 'uz')
            
            text = f"""
🔧 <b>Texnik yordam</b>

📞 Texnik yordam: +998901234568
📧 Email: support@example.com
💬 Telegram: @support_bot

Muammo bo'lsa bog'laning:
            """
            
            await message.answer(
                text.strip(),
                parse_mode='HTML',
                reply_markup=get_back_technician_keyboard(lang)
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "📦 Ombor bilan bog'lanish")
    async def contact_warehouse_handler(message: Message, state: FSMContext):
        """Contact warehouse handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            
            lang = user.get('language', 'uz')
            
            text = f"""
📦 <b>Ombor bilan bog'lanish</b>

👤 Ombor: +998901234569
📧 Email: warehouse@example.com
💬 Telegram: @warehouse_bot

Material kerak bo'lsa bog'laning:
            """
            
            await message.answer(
                text.strip(),
                parse_mode='HTML',
                reply_markup=get_back_technician_keyboard(lang)
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.message(F.text == "🚨 Shoshilinch holatlar")
    async def emergency_handler(message: Message, state: FSMContext):
        """Emergency handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            
            lang = user.get('language', 'uz')
            
            text = f"""
🚨 <b>Shoshilinch holatlar</b>

📞 Shoshilinch: +998901234570
🚑 Ambulansiya: 103
🚔 Politsiya: 102
🔥 O't o'chirish: 101

Shoshilinch holatda darhol bog'laning!
            """
            
            await message.answer(
                text.strip(),
                parse_mode='HTML',
                reply_markup=get_back_technician_keyboard(lang)
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    return router

# Mock functions (like other modules)
async def get_technician_by_telegram_id(telegram_id: int):
    """Get technician by telegram id (mock function like other modules)"""
    try:
        return {
            'id': 1,
            'full_name': 'Technician xodimi',
            'language': 'uz',
            'role': 'technician',
            'telegram_id': telegram_id
        }
    except Exception as e:
        return None

async def update_technician_language(technician_id: int, new_language: str):
    """Update technician language (mock function like other modules)"""
    try:
        return True
    except Exception as e:
        return False
