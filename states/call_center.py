"""
Call Center States

This module defines all state classes for the Call Center role.
"""

from aiogram.fsm.state import State, StatesGroup


class CallCenterMainMenuStates(StatesGroup):
    """Main menu states for call center"""
    main_menu = State()


class CallCenterLanguageStates(StatesGroup):
    """Language states for call center"""
    selecting_language = State()


class CallCenterInboxStates(StatesGroup):
    """Inbox states for call center"""
    viewing_messages = State()
    entering_message_number = State()
    viewing_message_details = State()
    entering_resolution_notes = State()


class CallCenterOrdersStates(StatesGroup):
    """Orders states for call center"""
    viewing_orders = State()
    entering_order_number = State()
    viewing_order_details = State()


class CallCenterReportsStates(StatesGroup):
    """Reports states for call center"""
    statistics = State()


class CallCenterChatStates(StatesGroup):
    """Chat states for call center"""
    chat = State()
    waiting_for_reply = State()


class CallCenterFeedbackStates(StatesGroup):
    """Feedback states for call center"""
    feedback = State()
    writing_feedback = State()
    waiting_for_feedback_data = State()


class CallCenterClientsStates(StatesGroup):
    """Clients states for call center"""
    clients = State()
    waiting_for_search_query = State()
    waiting_for_client_data = State()
    waiting_for_client_id = State()


class CallCenterClientRatingStates(StatesGroup):
    """Client rating states for call center"""
    viewing_rating = State()


class CallCenterDirectResolutionStates(StatesGroup):
    """Direct resolution states for call center"""
    direct_resolution = State()
    selecting_problem_type = State()
    entering_resolution = State()


class CallCenterSupervisorStates(StatesGroup):
    """Supervisor states for call center"""
    supervisor = State()
    supervisor_menu = State()
    assign_requests = State() 