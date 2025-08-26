"""
Call Center Supervisor Staff Application Creation Handler

This module implements staff application creation handlers for Call Center Supervisor role,
allowing call center supervisors to create both connection requests and technical service
applications on behalf of clients during phone calls.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

# Keyboard imports
from keyboards.call_center_supervisor_buttons import get_call_center_supervisor_main_menu
from keyboards.call_center_supervisor_buttons import (
    get_supervisor_staff_creation_keyboard
)

# States imports
from states.staff_application_states import StaffApplicationStates
from filters.role_filter import RoleFilter

def get_call_center_supervisor_staff_application_creation_router():
    """Get router for call center supervisor staff application creation handlers"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center_supervisor")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish", "🔌 Создать заявку на подключение"]))
    async def call_center_supervisor_create_connection_request(message: Message, state: FSMContext):
        """Handle call center supervisor creating connection request for client"""
        lang = 'uz'  # Default language
        
        # Mock application creation start
        await state.update_data(
            creator_context={'role': 'call_center_supervisor', 'id': 123},
            application_type='connection_request'
        )
        
        prompt_text = (
            "📞 Call Center Supervisor: Ulanish arizasi yaratish\n\n"
            "Mijoz bilan telefon orqali gaplashayotgan vaqtda ariza yaratish.\n\n"
            "Mijozni qanday qidirishni xohlaysiz?\n\n"
            "📱 Telefon raqami bo'yicha\n"
            "👤 Ism bo'yicha\n"
            "🆔 Mijoz ID bo'yicha\n"
            "➕ Yangi mijoz qo'shish"
        )
        
        # Create inline keyboard for client search options
        keyboard = get_supervisor_staff_creation_keyboard(lang)
        
        await message.answer(prompt_text, reply_markup=keyboard)
        await state.set_state(StaffApplicationStates.selecting_client_search_method)
    
    @router.message(F.text.in_(["🔧 Texnik xizmat yaratish", "🔧 Создать техническую заявку"]))
    async def call_center_supervisor_create_technical_service(message: Message, state: FSMContext):
        """Handle call center supervisor creating technical service request for client"""
        lang = 'uz'  # Default language
        
        # Mock application creation start
        await state.update_data(
            creator_context={'role': 'call_center_supervisor', 'id': 123},
            application_type='technical_service'
        )
        
        prompt_text = (
            "📞 Call Center Supervisor: Texnik xizmat arizasi yaratish\n\n"
            "Mijoz bilan telefon orqali gaplashayotgan vaqtda texnik xizmat arizasi yaratish.\n\n"
            "Mijozni qanday qidirishni xohlaysiz?\n\n"
            "📱 Telefon raqami bo'yicha\n"
            "👤 Ism bo'yicha\n"
            "🆔 Mijoz ID bo'yicha\n"
            "➕ Yangi mijoz qo'shish"
        )
        
        # Create inline keyboard for client search options
        keyboard = get_supervisor_staff_creation_keyboard(lang)
        
        await message.answer(prompt_text, reply_markup=keyboard)
        await state.set_state(StaffApplicationStates.selecting_client_search_method)
    
    @router.callback_query(F.data.startswith("ccs_client_search_"))
    async def handle_call_center_supervisor_client_search_method(callback: CallbackQuery, state: FSMContext):
        """Handle client search method selection for call center supervisor"""
        await callback.answer()
        
        lang = 'uz'  # Default language
        search_method = callback.data.split("_")[-1]  # phone, name, id, new
        
        # Update FSM data with search method
        await state.update_data(client_search_method=search_method)
        
        if search_method == "phone":
            await state.set_state(StaffApplicationStates.entering_client_phone)
            prompt_text = (
                "📱 Mijoz telefon raqamini kiriting:\n\n"
                "Masalan: +998901234567\n\n"
                "💡 Supervisor sifatida mijoz ma'lumotlarini aniq kiriting."
            )
            
        elif search_method == "name":
            await state.set_state(StaffApplicationStates.entering_client_name)
            prompt_text = (
                "👤 Mijoz ismini kiriting:\n\n"
                "To'liq ism va familiyani kiriting\n\n"
                "💡 Supervisor sifatida to'liq ma'lumot kiriting."
            )
            
        elif search_method == "id":
            await state.set_state(StaffApplicationStates.entering_client_id)
            prompt_text = (
                "🆔 Mijoz ID raqamini kiriting:\n\n"
                "💡 Supervisor sifatida aniq ID raqamini kiriting."
            )
            
        elif search_method == "new":
            await state.set_state(StaffApplicationStates.creating_new_client)
            prompt_text = (
                "➕ Yangi mijoz yaratish\n\n"
                "Supervisor sifatida yangi mijoz ma'lumotlarini kiritishni boshlaymiz.\n\n"
                "Birinchi navbatda, mijoz ismini kiriting:"
            )
            await state.set_state(StaffApplicationStates.entering_new_client_name)
        
        await callback.message.edit_text(prompt_text)
    
    @router.callback_query(F.data == "ccs_cancel_application_creation")
    async def call_center_supervisor_cancel_application_creation(callback: CallbackQuery, state: FSMContext):
        """Cancel application creation and return to main menu for call center supervisor"""
        await callback.answer()
        
        lang = 'uz'  # Default language
        await state.clear()
        
        cancel_text = (
            "❌ Ariza yaratish bekor qilindi.\n\n"
            "Bosh menyuga qaytdingiz."
        )
        
        await callback.message.edit_text(cancel_text, reply_markup=None)
        
        # Send main menu
        main_menu_text = "Call Center Supervisor - Bosh menyu"
        await callback.message.answer(
            main_menu_text,
            reply_markup=get_call_center_supervisor_main_menu(lang)
        )
    
    @router.message(StaffApplicationStates.entering_new_client_name)
    async def handle_new_client_name(message: Message, state: FSMContext):
        """Handle new client name input"""
        lang = 'uz'  # Default language
        client_name = message.text.strip()
        
        if len(client_name) < 3:
            error_text = "❌ Ism juda qisqa. Kamida 3 ta belgi kiriting."
            await message.answer(error_text)
            return
        
        await state.update_data(new_client_name=client_name)
        
        prompt_text = (
            f"✅ Mijoz ismi: {client_name}\n\n"
            "📱 Endi mijozning telefon raqamini kiriting:\n"
            "(Masalan: +998901234567)"
        )
        
        await message.answer(prompt_text)
        await state.set_state(StaffApplicationStates.entering_new_client_phone)
    
    @router.message(StaffApplicationStates.entering_new_client_phone)
    async def handle_new_client_phone(message: Message, state: FSMContext):
        """Handle new client phone input and create client"""
        lang = 'uz'  # Default language
        phone = message.text.strip()
        
        # Basic phone validation
        import re
        phone_pattern = re.compile(r'^\+?998[0-9]{9}$')
        clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        
        if not phone_pattern.match(clean_phone):
            error_text = (
                "❌ Noto'g'ri telefon raqam formati.\n"
                "To'g'ri format: +998901234567"
            )
            await message.answer(error_text)
            return
        
        # Normalize phone number
        if not clean_phone.startswith('+'):
            clean_phone = '+' + clean_phone
        
        data = await state.get_data()
        client_name = data.get('new_client_name')
        
        # Mock client creation
        client_id = 123  # Mock client ID
        client = {
            'id': client_id,
            'full_name': client_name,
            'phone': clean_phone,
            'role': 'client',
            'language': 'uz',
            'is_active': True
        }
        
        await state.update_data(selected_client_id=client_id, selected_client=client)
        
        success_text = (
            f"✅ Yangi mijoz muvaffaqiyatli yaratildi!\n\n"
            f"👤 Ism: {client_name}\n"
            f"📱 Telefon: {clean_phone}\n\n"
            "Endi ariza turini tanlang:"
        )
        
        # Show application type selection
        keyboard = get_supervisor_staff_creation_keyboard(lang)
        
        await message.answer(success_text, reply_markup=keyboard)
        await state.set_state(StaffApplicationStates.selecting_application_type)
    
    @router.callback_query(F.data.startswith("ccs_app_type_"))
    async def handle_application_type_selection(callback: CallbackQuery, state: FSMContext):
        """Handle application type selection"""
        await callback.answer()
        
        app_type = callback.data.split("_")[-1]  # connection or technical
        
        if app_type == "connection":
            await state.update_data(application_type='connection_request')
            prompt_text = (
                "🔌 Ulanish arizasi yaratish\n\n"
                "Mijoz ma'lumotlari:\n"
                "👤 Ism: {client_name}\n"
                "📱 Telefon: {client_phone}\n\n"
                "Ariza tavsifini kiriting:"
            )
        else:
            await state.update_data(application_type='technical_service')
            prompt_text = (
                "🔧 Texnik xizmat arizasi yaratish\n\n"
                "Mijoz ma'lumotlari:\n"
                "👤 Ism: {client_name}\n"
                "📱 Telefon: {client_phone}\n\n"
                "Muammo tavsifini kiriting:"
            )
        
        await callback.message.edit_text(prompt_text)
        await state.set_state(StaffApplicationStates.entering_application_description)
    
    @router.message(StaffApplicationStates.entering_application_description)
    async def handle_application_description(message: Message, state: FSMContext):
        """Handle application description input"""
        lang = 'uz'  # Default language
        description = message.text.strip()
        
        if len(description) < 10:
            error_text = "❌ Tavsif juda qisqa. Kamida 10 ta belgi kiriting."
            await message.answer(error_text)
            return
        
        await state.update_data(application_description=description)
        
        # Mock application creation
        data = await state.get_data()
        client = data.get('selected_client', {})
        app_type = data.get('application_type', 'unknown')
        
        success_text = (
            f"✅ Ariza muvaffaqiyatli yaratildi!\n\n"
            f"📋 Ariza turi: {app_type}\n"
            f"👤 Mijoz: {client.get('full_name', 'N/A')}\n"
            f"📱 Telefon: {client.get('phone', 'N/A')}\n"
            f"📝 Tavsif: {description}\n\n"
            f"🎯 Ariza raqami: APP-{123:03d}\n"
            f"📅 Yaratilgan: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        
        await message.answer(success_text)
        await state.clear()
    
    @router.callback_query(F.data == "ccs_create_new_client_btn")
    async def handle_create_new_client_button(callback: CallbackQuery, state: FSMContext):
        """Handle create new client button from search results"""
        await callback.answer()
        
        lang = 'uz'  # Default language
        
        prompt_text = (
            "➕ Yangi mijoz yaratish\n\n"
            "Mijoz ismini kiriting:"
        )
        
        await callback.message.edit_text(prompt_text)
        await state.set_state(StaffApplicationStates.entering_new_client_name)
    
    @router.callback_query(F.data == "ccs_confirm_client_selection")
    async def handle_confirm_client_selection(callback: CallbackQuery, state: FSMContext):
        """Handle client selection confirmation"""
        await callback.answer()
        
        lang = 'uz'  # Default language
        
        # Get client data from state
        data = await state.get_data()
        client = data.get('selected_client', {})
        app_type = data.get('application_type', 'unknown')
        
        prompt_text = (
            f"✅ Mijoz tanlandi!\n\n"
            f"👤 Ism: {client.get('full_name', 'N/A')}\n"
            f"📱 Telefon: {client.get('phone', 'N/A')}\n"
            f"📋 Ariza turi: {app_type}\n\n"
            f"Ariza tavsifini kiriting:"
        )
        
        await callback.message.edit_text(prompt_text)
        await state.set_state(StaffApplicationStates.entering_application_description)
    
    @router.callback_query(F.data.in_(["back", "orqaga", "назад"]))
    async def supervisor_back(call: CallbackQuery, state: FSMContext):
        """Go back to supervisor main menu"""
        await call.answer()
        
        text = "Call Center Supervisor paneliga xush kelibsiz!"
        await call.message.edit_text(text)
        await state.clear()

    return router
