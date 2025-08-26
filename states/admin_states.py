"""
Admin States

This module defines all state classes for the Admin role.
"""

from aiogram.fsm.state import State, StatesGroup


class AdminMainMenuStates(StatesGroup):
    """Main menu states for admin"""
    main_menu = State()
    export_selection = State()
    export_format_selection = State()


class AdminCallbackStates(StatesGroup):
    """Callback states for admin"""
    waiting_for_confirmation = State()
    waiting_for_search_value = State()


class AdminOrderStates(StatesGroup):
    """Order states for admin"""
    viewing_orders = State()
    entering_order_number = State()
    viewing_order_details = State()
    waiting_for_order_id = State()
    filtering = State()
    filtering_selected = State()


class AdminUsersStates(StatesGroup):
    """User states for admin"""
    users = State()
    waiting_for_search_query = State()
    waiting_for_user_data = State()
    waiting_for_user_id = State()
    waiting_for_field_value = State()


class AdminSettingsStates(StatesGroup):
    """Settings states for admin"""
    settings = State()
    editing_setting = State()
    waiting_for_setting_value = State()


class AdminStatisticsStates(StatesGroup):
    """Statistics states for admin"""
    viewing_statistics = State()
    statistics = State()


class AdminWorkflowRecoveryStates(StatesGroup):
    """Workflow recovery states for admin"""
    recovery_menu = State()
    workflow_recovery = State() 