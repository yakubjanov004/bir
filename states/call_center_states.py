"""
Call Center States (Additional)

This module defines additional state classes for the Call Center role.
"""

from aiogram.fsm.state import State, StatesGroup





class CallCenterDirectResolutionStates(StatesGroup):
    """Direct resolution states for call center"""
    selecting_problem_type = State()
    entering_resolution = State()


class CallCenterChatStates(StatesGroup):
    """Chat states for call center"""
    waiting_for_reply = State()
    viewing_chat = State()
    selecting_chat = State()


class CallCenterMainMenuStates(StatesGroup):
    """Main menu states for call center"""
    main_menu = State()
    chat_menu = State()
    orders_menu = State()
    clients_menu = State()
    feedback_menu = State()
    statistics_menu = State()


class CallCenterClientsStates(StatesGroup):
    """Clients states for call center"""
    clients = State()
    waiting_for_search_query = State()
    waiting_for_client_data = State()
    waiting_for_client_id = State()
    viewing_client_profile = State()
    editing_client = State()


class CallCenterFeedbackStates(StatesGroup):
    """Feedback states for call center"""
    feedback = State()
    waiting_for_feedback_data = State()
    waiting_for_search_query = State() 