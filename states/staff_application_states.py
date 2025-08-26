"""
Staff Application States

This module defines all state classes for staff application creation.
"""

from aiogram.fsm.state import State, StatesGroup


class StaffApplicationStates(StatesGroup):
    """States for staff application creation"""
    selecting_application_type = State()
    entering_client_phone = State()
    entering_client_name = State()
    entering_client_id = State()
    entering_new_client_name = State()
    entering_new_client_phone = State()
    entering_application_description = State()
    selecting_priority = State()
    confirming_application = State()
    entering_location = State()
    asking_for_location = State()
    waiting_for_location = State()
    asking_for_media = State()
    waiting_for_media = State()
    confirming_order = State()
    selecting_client_search_method = State()
    creating_new_client = State()
    searching_client = State()
    confirming_client_selection = State()
    application_created = State() 