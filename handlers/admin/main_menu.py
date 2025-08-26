"""
Admin Main Menu Handler
Manages admin main menu and dashboard
"""

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.admin_buttons import get_admin_main_menu

# States imports
from states.admin_states import AdminMainMenuStates
from filters.role_filter import RoleFilter

def get_admin_main_menu_router():
    """Get admin main menu router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("admin")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["/start", "/admin"]))
    async def admin_start(message: Message, state: FSMContext):
        """Admin start"""
        welcome_text = (
            f"🛠 <b>Admin Panel</b>\n\n"
            f"📊 <b>Tizim holati:</b>\n"
            f"👥 Jami foydalanuvchilar: <b>1250</b>\n"
            f"📋 Bugungi zayavkalar: <b>45</b>\n"
            f"✅ Bugun bajarilgan: <b>32</b>\n"
            f"⏳ Kutilayotgan: <b>13</b>\n"
            f"👨‍🔧 Faol texniklar: <b>8</b>\n\n"
            f"Kerakli bo'limni tanlang:"
        )
        
        await message.answer(
            welcome_text,
            reply_markup=get_admin_main_menu('uz')
        )
        
        await state.set_state(AdminMainMenuStates.main_menu)

    @router.message(F.text.in_(['🏠 Bosh sahifa', '🏠 Главная']))
    async def admin_home(message: Message, state: FSMContext):
        """Return to admin home"""
        await admin_start(message, state)

    @router.message(F.text.in_(['ℹ️ Yordam', 'ℹ️ Помощь']))
    async def admin_help(message: Message, state: FSMContext):
        """Show admin help"""
        help_text = (
            f"ℹ️ <b>Admin Panel Yordami</b>\n\n"
            f"📋 <b>Asosiy funksiyalar:</b>\n"
            f"• 👥 Foydalanuvchilar - foydalanuvchilarni boshqarish\n"
            f"• 📝 Zayavkalar - zayavkalarni ko'rish va boshqarish\n"
            f"• 📊 Statistika - tizim statistikasini ko'rish\n"
            f"• ⚙️ Sozlamalar - tizim sozlamalarini o'zgartirish\n\n"
            f"🔧 <b>Foydalanuvchi boshqaruvi:</b>\n"
            f"• Rol o'zgartirish\n"
            f"• Bloklash/blokdan chiqarish\n"
            f"• Qidirish (ID, telefon, ism bo'yicha)\n\n"
            f"📋 <b>Zayavka boshqaruvi:</b>\n"
            f"• Status o'zgartirish\n"
            f"• Texnik tayinlash\n"
            f"• Filtrlash va qidirish\n\n"
            f"📞 <b>Yordam uchun:</b> @support"
        )
        
        await message.answer(help_text)
        await state.set_state(AdminMainMenuStates.main_menu)

    # Test handler without decorator
    @router.message(F.text == '/test_admin')
    async def test_admin(message: Message):
        """Test admin access without decorator"""
        await message.answer("✅ Admin access confirmed!")

    return router

async def show_admin_main_menu(message: Message):
    """Show admin main menu"""
    welcome_text = (
        f"🛠 <b>Admin Panel</b>\n\n"
        f"Kerakli bo'limni tanlang:"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=get_admin_main_menu('uz')
    )
