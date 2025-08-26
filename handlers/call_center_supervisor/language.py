"""
Call Center Supervisor Language Handler
Manages language settings for call center supervisor
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.call_center_supervisor_buttons import get_language_selection_inline_menu, get_call_center_supervisor_main_menu

# States imports
from states.call_center_supervisor_states import CallCenterSupervisorLanguageStates
from filters.role_filter import RoleFilter

def get_call_center_supervisor_language_router():
    """Get call center supervisor language router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center_supervisor")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(['🌐 Tilni o\'zgartirish', '🌐 Изменить язык']))
    async def call_center_supervisor_language_settings(message: Message, state: FSMContext):
        """Call center supervisor language settings"""
        lang = 'uz'  # Default language
        
        text = (
            "🌐 <b>Tilni o'zgartirish</b>\n\n"
            "Qaysi tilni tanlaysiz?\n\n"
            "🇺🇿 O'zbekcha\n"
            "🇷🇺 Русский"
        )
        
        await message.answer(
            text,
            reply_markup=get_language_selection_inline_menu()
        )
        await state.set_state(CallCenterSupervisorLanguageStates.selecting_language)

    @router.callback_query(F.data.startswith("set_lang_"))
    async def call_center_supervisor_set_language(callback: CallbackQuery, state: FSMContext):
        """Set call center supervisor language"""
        await callback.answer()
        
        selected_lang = callback.data.replace("set_lang_", "")
        
        # Mock language setting
        success_text = (
            f"✅ Til muvaffaqiyatli o'zgartirildi!\n\n"
            f"🌐 Yangi til: {'O\'zbekcha' if selected_lang == 'uz' else 'Русский'}"
        )
        
        await callback.message.edit_text(success_text)
        await state.clear()

    @router.callback_query(F.data == "cancel_language")
    async def call_center_supervisor_cancel_language(callback: CallbackQuery, state: FSMContext):
        """Cancel language selection"""
        await callback.answer()
        
        cancel_text = "❌ Til o'zgartirish bekor qilindi."
        
        await callback.message.edit_text(cancel_text)
        await state.clear()

    return router 
