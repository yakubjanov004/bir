"""
Client States

This module defines all state classes for the Client role.
"""

from aiogram.fsm.state import State, StatesGroup


class MainMenuStates(StatesGroup):
    """Main menu states for client"""
    main_menu = State()


class StartStates(StatesGroup):
    """Start states for client"""
    start = State()


class LanguageStates(StatesGroup):
    """Language states for client"""
    selecting_language = State()


class ContactStates(StatesGroup):
    """Contact states for client"""
    viewing_contact = State()
    waiting_for_contact = State()


class HelpStates(StatesGroup):
    """Help states for client"""
    help_menu = State()
    main_menu = State()


class FeedbackStates(StatesGroup):
    """Feedback states for client"""
    waiting_for_feedback = State()


class ProfileStates(StatesGroup):
    """Profile states for client"""
    profile_menu = State()
    viewing_profile = State()
    editing_name = State()
    editing_address = State()
    waiting_for_input = State()
    editing_phone = State()
    editing = State()


class OrderStates(StatesGroup):
    """Order states for client"""
    selecting_region = State()
    selecting_order_type = State()
    waiting_for_contact = State()
    entering_description = State()
    asking_for_media = State()
    waiting_for_media = State()
    asking_for_location = State()
    waiting_for_location = State()
    confirming_order = State()
    entering_address = State()
    entering_reason = State()


class ConnectionOrderStates(StatesGroup):
    """Connection order states for client"""
    selecting_region = State()
    selecting_connection_type = State()
    selecting_tariff = State()
    entering_address = State()
    asking_for_geo = State()
    waiting_for_geo = State()
    confirming_connection = State()