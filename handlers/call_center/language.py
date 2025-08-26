"""
Call Center Language Handler
Manages language settings for call center operators
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.call_center_buttons import get_language_selection_inline_menu, call_center_main_menu_reply

# States imports
from states.call_center import CallCenterLanguageStates
from filters.role_filter import RoleFilter

def get_call_center_language_router():
    """Get call center language router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(['🌐 Tilni o\'zgartirish', '🌐 Изменить язык']))
    async def call_center_language_settings(message: Message, state: FSMContext):
        """Handle language settings"""
        lang = 'uz'  # Default language
        
        text = "Tilni tanlang / Выберите язык:" if lang == 'uz' else "Выберите язык / Tilni tanlang:"
        
        await message.answer(
            text,
            reply_markup=get_language_selection_inline_menu()
        )
        await state.set_state(CallCenterLanguageStates.selecting_language)

    @router.callback_query(F.data.startswith("cc_lang_"))
    async def call_center_select_language(callback: CallbackQuery, state: FSMContext):
        """Handle language selection"""
        await callback.answer()
        
        selected_lang = callback.data.replace("cc_lang_", "")
        
        if selected_lang in ['uz', 'ru']:
            # Mock language update
            success_text = (
                "✅ Til o'zgartirildi!" if selected_lang == 'uz'
                else "✅ Язык изменен!"
            )
            
            await callback.message.edit_text(success_text)
            await state.clear()
        else:
            error_text = (
                "❌ Noto'g'ri til tanlandi." if selected_lang == 'uz'
                else "❌ Неверный язык выбран."
            )
            await callback.message.edit_text(error_text)

    @router.callback_query(F.data == "cc_cancel_lang")
    async def call_center_cancel_language(callback: CallbackQuery, state: FSMContext):
        """Handle language selection cancel"""
        await callback.answer()
        
        cancel_text = (
            "❌ Til o'zgartirish bekor qilindi." if callback.from_user.language_code == 'uz'
            else "❌ Изменение языка отменено."
        )
        
        await callback.message.edit_text(cancel_text)
        await state.clear()

    return router

async def show_call_center_language_menu(message: Message):
    """Show call center language menu"""
    lang = 'uz'  # Default language
    
    text = "Tilni tanlang / Выберите язык:" if lang == 'uz' else "Выберите язык / Tilni tanlang:"
    
    await message.answer(
        text,
        reply_markup=get_language_selection_inline_menu()
    )
