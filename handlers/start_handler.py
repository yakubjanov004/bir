"""
Start Handler - Simplified Implementation

This module handles the /start command and shows appropriate menus
based on user role.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, Contact
from aiogram.fsm.context import FSMContext
from loader import get_user_role
from utils.role_system import show_role_menu
from keyboards.client_buttons import get_contact_keyboard, get_main_menu_keyboard
from states.client_states import ContactStates

def get_start_router():
    """Get start router with all handlers"""
    router = Router()
    
    @router.message(F.text == "/start")
    async def start_command(message: Message, state: FSMContext):
        """Handle /start command"""
        try:
            user_role = get_user_role(message.from_user.id)
            
            # Clear any existing state
            await state.clear()
            
            if user_role == 'client':
                # Ask for contact information first
                await message.answer(
                    "🤖 Alfa Connect botiga xush kelibsiz!\n\n"
                    "📱 Davom etish uchun kontakt ma'lumotlaringizni ulashing:",
                    reply_markup=get_contact_keyboard('uz')
                )
                await state.set_state(ContactStates.waiting_for_contact)
            else:
                await show_role_menu(message, user_role)
            
        except Exception as e:
            #await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            pass

    @router.message(ContactStates.waiting_for_contact, F.contact)
    async def handle_contact_shared(message: Message, state: FSMContext):
        """Handle when user shares their contact"""
        contact = message.contact

        # Defensive: check for required fields
        phone_number = getattr(contact, "phone_number", None)
        full_name = getattr(contact, "full_name", None)
        user_id = getattr(contact, "user_id", None)

        if not phone_number or not user_id:
            await message.answer("❌ Kontakt ma'lumotlarini to'g'ri yuboring. Qaytadan urinib ko'ring.")
            return

        try:
            # Save contact information to state (you can save to database here)
            await state.update_data(
                phone_number=phone_number,
                full_name=full_name or "",
                user_id=user_id
            )
            
            # Show welcome message and main menu
            await message.answer(
                f"✅ Rahmat! {full_name or ''}\n\n"
                "🎉 Endi botdan foydalanishingiz mumkin!",
                reply_markup=get_main_menu_keyboard('uz')
            )
            
            # Clear the contact state
            await state.clear()
            
        except Exception as e:
            await message.answer("❌ Kontaktni saqlashda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
    
    @router.message(ContactStates.waiting_for_contact)
    async def handle_non_contact_message(message: Message, state: FSMContext):
        """Handle non-contact messages while waiting for contact"""
        await message.answer(
            "📱 Iltimos, kontakt ma'lumotlaringizni ulashing:\n"
            "👆 Yuqoridagi '📱 Kontakt ulashish' tugmasini bosing",
            reply_markup=get_contact_keyboard('uz')
        )
    
    @router.callback_query(F.data == "back_to_main_menu")
    async def back_to_main_menu_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to main menu button"""
        try:
            await callback.answer()
            
            user_role = get_user_role(callback.from_user.id)
            
            # Clear any existing state
            await state.clear()
            
            # Show appropriate menu based on role
            if user_role == 'client':
                keyboard = get_main_menu_keyboard('uz')
                await callback.message.edit_text(
                    "Quyidagi menyudan kerakli bo'limni tanlang.",
                    reply_markup=keyboard
                )
            else:
                await show_role_menu(callback.message, user_role)
            
        except Exception as e:
            #await callback.message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            pass
    
    return router 