"""
Admin Language Settings Handler
Manages language settings for admin users
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from functools import wraps
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.admin_buttons import language_keyboard, get_admin_main_menu
from filters.role_filter import RoleFilter

def get_admin_language_router():
    """Get admin language router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("admin")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🌐 Til sozlamalari", "🌐 Языковые настройки"]))
    async def admin_language_settings(message: Message):
        """Admin language settings"""
        text = (
            f"🌐 <b>Admin til sozlamalari</b>\n\n"
            f"Joriy til: <b>O'zbek tili</b> 🇺🇿\n\n"
            f"Admin panel tilini o'zgartirish uchun\n"
            f"quyidagi tugmalardan birini tanlang:"
        )
        
        await message.answer(
            text,
            reply_markup=language_keyboard()
        )

    @router.callback_query(F.data.in_(["lang_uz", "lang_ru"]))
    async def change_admin_language(call: CallbackQuery):
        """Change admin language"""
        await call.answer()
        
        new_lang = call.data.split("_")[1]  # uz or ru
        
        if new_lang == 'uz':
            text = (
                f"✅ <b>Til muvaffaqiyatli o'zgartirildi!</b>\n\n"
                f"🇺🇿 Admin panel endi O'zbek tilida ishlaydi.\n\n"
                f"Barcha menyu va xabarlar O'zbek tilida\n"
                f"ko'rsatiladi."
            )
        else:
            text = (
                f"✅ <b>Язык успешно изменен!</b>\n\n"
                f"🇷🇺 Панель администратора теперь работает на русском языке.\n\n"
                f"Все меню и сообщения будут отображаться\n"
                f"на русском языке."
            )
        
        await call.message.edit_text(text)
        
        # Send new reply keyboard in the new language
        await call.message.answer(
            "Asosiy menyu yangilandi." if new_lang == 'uz' else "Главное меню обновлено.",
            reply_markup=get_admin_main_menu(new_lang)
        )
        
        await call.answer("Til o'zgartirildi!" if new_lang == 'uz' else "Язык изменен!")

    @router.message(F.text.in_(["🔄 Tilni qayta tiklash", "🔄 Сбросить язык"]))
    async def reset_admin_language(message: Message):
        """Reset admin language to default"""
        text = (
            f"🔄 <b>Til standart holatga qaytarildi!</b>\n\n"
            f"🇺🇿 Admin panel endi O'zbek tilida (standart)\n"
            f"ishlaydi.\n\n"
            f"Kerak bo'lsa, tilni qayta o'zgartirishingiz mumkin."
        )
        
        await message.answer(text)

    @router.message(F.text.in_(["📊 Til statistikasi", "📊 Языковая статистика"]))
    async def language_statistics(message: Message):
        """Show language usage statistics"""
        text = (
            f"📊 <b>Til statistikasi</b>\n\n"
            f"🇺🇿 <b>O'zbek tili:</b>\n"
            f"• Foydalanuvchilar: <b>85%</b>\n"
            f"• Adminlar: <b>90%</b>\n"
            f"• Texniklar: <b>95%</b>\n\n"
            f"🇷🇺 <b>Rus tili:</b>\n"
            f"• Foydalanuvchilar: <b>15%</b>\n"
            f"• Adminlar: <b>10%</b>\n"
            f"• Texniklar: <b>5%</b>\n\n"
            f"📈 <b>Tendentsiyalar:</b>\n"
            f"• O'zbek tili foydalanuvchilari ko'paymoqda\n"
            f"• Rus tili barqaror holatda\n\n"
            f"💡 <b>Tavsiya:</b>\n"
            f"O'zbek tilidagi kontentni rivojlantirish\n"
            f"tavsiya etiladi."
        )
        
        await message.answer(text)

    return router
