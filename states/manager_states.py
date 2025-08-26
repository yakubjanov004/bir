"""
Manager States

This module defines all state classes for the Manager role.
"""

from aiogram.fsm.state import State, StatesGroup


class ManagerMainMenuStates(StatesGroup):
    """Main menu states for manager"""
    main_menu = State()
    export_selection = State()
    export_format_selection = State()


class ManagerApplicationStates(StatesGroup):
    """Application states for manager"""
    viewing_applications = State()
    entering_application_number = State()
    viewing_application_details = State()


class ManagerFilterStates(StatesGroup):
    """Filter states for manager"""
    selecting_filter = State()
    entering_filter_value = State()
    selecting_filter_type = State()


class ManagerInboxStates(StatesGroup):
    """Inbox states for manager"""
    viewing_messages = State()
    entering_message_number = State()
    viewing_message_details = State()
    entering_comment = State()


class ManagerNotificationStates(StatesGroup):
    """Notification states for manager"""
    sending_notification = State()
    selecting_notification_type = State()
    sending_notification_message = State()


class ManagerStatusStates(StatesGroup):
    """Status states for manager"""
    changing_status = State()
    entering_status_value = State()


class ManagerTechnicianAssignmentStates(StatesGroup):
    """Technician assignment states for manager"""
    selecting_technician = State()
    confirming_assignment = State()


class ManagerWordDocumentStates(StatesGroup):
    """Word document states for manager"""
    creating_document = State()
    selecting_document_type = State()


class ManagerClientSearchStates(StatesGroup):
    """Client search states for manager (controller-like)"""
    selecting_client_search_method = State()
    entering_phone = State()
    entering_name = State()
    entering_client_id = State()
    entering_new_client_name = State()
    selecting_client = State()


class ManagerConnectionOrderStates(StatesGroup):
    """Connection order creation states for manager (client-like)"""
    selecting_region = State()
    selecting_connection_type = State()
    selecting_tariff = State()
    entering_address = State()
    asking_for_geo = State()
    waiting_for_geo = State()
    confirming_connection = State()


class ManagerServiceOrderStates(StatesGroup):
    """Service order creation states for manager (client-like)"""
    selecting_region = State()
    selecting_order_type = State()
    waiting_for_abonent_id = State()
    entering_description = State()
    asking_for_media = State()
    waiting_for_media = State()
    entering_address = State()
    asking_for_location = State()
    waiting_for_location = State()
    confirming_order = State() 