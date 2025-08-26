"""
Junior Manager States

This module defines all state classes for the Junior Manager role.
"""

from aiogram.fsm.state import State, StatesGroup


class JuniorManagerMainMenuStates(StatesGroup):
    """Main menu states for junior manager"""
    main_menu = State()


class JuniorManagerStates(StatesGroup):
    """General states for junior manager"""
    viewing_applications = State()
    entering_application_number = State()
    viewing_application_details = State()
    waiting_for_controller_note = State()
    waiting_for_contact_note = State()


class JuniorManagerApplicationStates(StatesGroup):
    """Application states for junior manager"""
    client_search_phone = State()
    client_search_name = State()
    client_search_id = State()
    creating_new_client = State()
    entering_application_details = State()
    selecting_priority = State()
    confirming_application = State()


class JuniorManagerInboxStates(StatesGroup):
    """Inbox states for junior manager"""
    viewing_messages = State()
    entering_message_number = State()
    viewing_message_details = State()


class JuniorManagerOrderStates(StatesGroup):
    """Order states for junior manager"""
    viewing_orders = State()
    entering_order_number = State()
    viewing_order_details = State()


class JuniorManagerFilterStates(StatesGroup):
    """Filter states for junior manager"""
    selecting_filter = State()
    entering_filter_value = State()


class JuniorManagerAssignStates(StatesGroup):
    """Assignment states for junior manager"""
    selecting_assignee = State()
    confirming_assignment = State()


class JuniorManagerStatisticsStates(StatesGroup):
    """Statistics states for junior manager"""
    viewing_statistics = State()
    selecting_report_type = State()


class JuniorManagerLanguageStates(StatesGroup):
    """Language states for junior manager"""
    selecting_language = State()


class JuniorManagerDetailsInputStates(StatesGroup):
    """Details input states for junior manager"""
    entering_details = State()
    confirming_details = State()


class JuniorManagerWorkflowStates(StatesGroup):
    """Workflow states for junior manager"""
    workflow_monitoring = State()
    workflow_optimization = State() 