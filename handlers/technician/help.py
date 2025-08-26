from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
from keyboards.technician_buttons import get_technician_help_menu, get_technician_main_menu_keyboard, get_help_back_keyboard
from states.technician_states import TechnicianHelpStates
from filters.role_filter import RoleFilter

def get_help_router():
    """Technician help router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("technician")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text == "🆘 Yordam")
    async def show_help_menu(message: Message, state: FSMContext):
        """Show help menu"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': message.from_user.id,
                'role': 'technician',
                'language': 'uz',
                'full_name': 'Test Technician'
            }
            
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
                reply_markup=get_technician_help_menu('uz')
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "tech_contact_manager")
    async def contact_manager(callback: CallbackQuery, state: FSMContext):
        """Contact manager from help menu"""
        try:
            await state.set_state(TechnicianHelpStates.waiting_for_manager_message)
            
            text = "📞 Managerga xabar yozing:"
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(TechnicianHelpStates.waiting_for_manager_message))
    async def process_manager_message(message: Message, state: FSMContext):
        """Process manager message from help menu"""
        try:
            manager_message = message.text
            
            # Mock success - send message to managers
            await message.answer("✅ Xabar yuborildi!")
            await state.clear()
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")
            await state.clear()

    @router.callback_query(F.data == "tech_technical_help")
    async def technical_help(callback: CallbackQuery, state: FSMContext):
        """Show technical help information"""
        try:
            text = f"""
🔧 <b>Texnik yordam</b>

📋 <b>Asosiy funksiyalar:</b>
• 📥 Inbox - Zayavkalarni ko'rish
• 📋 Vazifalarim - Tayinlangan vazifalar
• 📊 Hisobotlar - Statistikalar
• 🌐 Tilni o'zgartirish

🔧 <b>Ish jarayoni:</b>
1. Controllerdan zayavka olish
2. Manzilga borib diagnostika qo'yish
3. Ombor kerakligini hal qilish
4. Ishni bajarish va yakunlash

📞 <b>Qo'llab-quvvatlash:</b>
Muammo bo'lsa menejer bilan bog'laning.
            """
            
            keyboard = get_help_back_keyboard('uz')
            await callback.message.edit_text(
                text.strip(),
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_warehouse_help")
    async def warehouse_help(callback: CallbackQuery, state: FSMContext):
        """Show warehouse help information"""
        try:
            text = f"""
📦 <b>Ombor bilan bog'lanish</b>

📞 <b>Ombor xodimlari:</b>
• Telefon: +998901234567
• Telegram: @warehouse_support

📋 <b>Jihozlar so'rash:</b>
1. Ish jarayonida ombor kerakligini aniqlang
2. Kerakli jihozlar ro'yxatini tayyorlang
3. Ombor xodimlariga so'rov yuboring
4. Jihozlarni olish va ishni davom ettirish

⚠️ <b>Eslatma:</b>
Faqat kerakli jihozlarni so'rang.
            """
            
            keyboard = get_help_back_keyboard('uz')
            await callback.message.edit_text(
                text.strip(),
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_emergency_help")
    async def emergency_help(callback: CallbackQuery, state: FSMContext):
        """Show emergency help information"""
        try:
            text = f"""
🚨 <b>Shoshilinch holatlar</b>

📞 <b>Shoshilinch raqamlar:</b>
• Menejer: +998901234567
• Texnik yordam: +998901234568
• Ombor: +998901234569

⚠️ <b>Shoshilinch holatlar:</b>
• Xavfsizlik muammosi
• Jihozlar buzilishi
• Mijoz bilan kelishmovchilik
• Boshqa shoshilinch holatlar

📞 Darhol menejer bilan bog'laning!
            """
            
            keyboard = get_help_back_keyboard('uz')
            await callback.message.edit_text(
                text.strip(),
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_back_to_help")
    async def back_to_help(callback: CallbackQuery, state: FSMContext):
        """Return to help menu"""
        try:
            text = f"""
🆘 <b>Yordam</b>

📞 Manager bilan bog'lanish
🔧 Texnik yordam
📦 Ombor bilan bog'lanish
🚨 Shoshilinch holatlar

Kerakli yordam turini tanlang:
            """
            
            await callback.message.edit_text(
                text.strip(),
                parse_mode='HTML',
                reply_markup=get_technician_help_menu('uz')
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router
