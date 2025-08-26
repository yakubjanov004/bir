"""
Call Center Supervisor States

This module defines all state classes for the Call Center Supervisor role.
"""

from aiogram.fsm.state import State, StatesGroup


class CallCenterSupervisorMainMenuStates(StatesGroup):
    """Main menu states for Call Center Supervisor"""
    main_menu = State()
    export_selection = State()
    export_format_selection = State()


class CallCenterSupervisorStates(StatesGroup):
    """Main states for Call Center Supervisor"""
    main_menu = State()
    waiting_for_comment = State()
    waiting_for_operator_select = State()


class CallCenterSupervisorInboxStates(StatesGroup):
    """Inbox states for Call Center Supervisor"""
    viewing_messages = State()
    entering_message_number = State()
    viewing_message_details = State()


class CallCenterSupervisorOrdersStates(StatesGroup):
    """Orders states for Call Center Supervisor"""
    viewing_orders = State()
    entering_order_number = State()
    viewing_order_details = State()


class CallCenterSupervisorStatisticsStates(StatesGroup):
    """Statistics states for Call Center Supervisor"""
    viewing_statistics = State()
    selecting_report_type = State()


class CallCenterSupervisorApplicationStates(StatesGroup):
    """Application creation states for Call Center Supervisor"""
    client_search_phone = State()
    client_search_name = State()
    client_search_id = State()
    creating_new_client = State()
    entering_application_details = State()
    selecting_priority = State()
    confirming_application = State()


class CallCenterSupervisorFeedbackStates(StatesGroup):
    """Feedback states for Call Center Supervisor"""
    writing_feedback = State()
    viewing_feedback = State()
    rating_service = State()


class CallCenterSupervisorLanguageStates(StatesGroup):
    """Language states for Call Center Supervisor"""
    selecting_language = State()


class CallCenterSupervisorWorkflowStates(StatesGroup):
    """Workflow management states for Call Center Supervisor"""
    workflow_monitoring = State()
    workflow_optimization = State()
    team_coordination = State()


class CallCenterSupervisorNotificationStates(StatesGroup):
    """Notification states for Call Center Supervisor"""
    sending_announcement = State()
    team_message = State()
    individual_message = State()
    urgent_alert = State() 