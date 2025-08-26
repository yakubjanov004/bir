"""
Call Center Supervisor Main Menu Handler

This module implements the main menu handler for Call Center Supervisor role,
including staff management, order oversight, and application creation functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, Optional

# Keyboard imports
from keyboards.call_center_supervisor_buttons import (
    get_call_center_supervisor_main_menu, get_staff_actions_menu,
    get_order_management_menu, get_client_search_menu, get_order_action_menu,
    get_staff_assignment_menu, get_status_change_menu, get_quick_actions_menu,
    get_supervisor_dashboard_menu, get_advanced_staff_management_menu,
    get_advanced_order_management_menu, get_analytics_dashboard_keyboard,
    get_notification_management_keyboard, get_supervisor_settings_keyboard
)

# States imports
from states.call_center_supervisor_states import (
    CallCenterSupervisorStates, CallCenterSupervisorInboxStates, 
    CallCenterSupervisorOrdersStates, CallCenterSupervisorStatisticsStates
)
from filters.role_filter import RoleFilter

def get_call_center_supervisor_main_menu_router():
    """Get router for call center supervisor main menu handlers"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center_supervisor")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📞 Call Center Supervisor", "📞 Супервайзер колл-центра", "📞 Call Center Nazoratchi"]))
    async def call_center_supervisor_start(message: Message, state: FSMContext):
        """Call center supervisor main menu"""
        lang = 'uz'  # Default language
        
        await state.clear()
        
        welcome_text = "📞 Call Center Supervisor paneliga xush kelibsiz!"
        
        await message.answer(
            welcome_text,
            reply_markup=get_call_center_supervisor_main_menu(lang)
        )
        await state.set_state(CallCenterSupervisorStates.main_menu)

    @router.message(F.text.in_(["🏠 Bosh menyu", "🏠 Главное меню"]))
    async def call_center_supervisor_main_menu_handler(message: Message, state: FSMContext):
        """Handle call center supervisor main menu button"""
        lang = 'uz'  # Default language
        
        main_menu_text = "Bosh menyu"
        
        await message.answer(
            main_menu_text,
            reply_markup=get_call_center_supervisor_main_menu(lang)
        )
        if state is not None:
            await state.set_state(CallCenterSupervisorStates.main_menu)


    return router