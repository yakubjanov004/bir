"""
Call Center Supervisor Module - Complete Implementation

This module provides call center supervisor functionality including:
- Application management
- Feedback system
- Inbox management
- Language settings
- Main menu and dashboard
- Notification management
- Order management
- Staff application creation
- Statistics and reports
- Workflow management
"""

from aiogram import Router
from .main_menu import get_call_center_supervisor_main_menu_router
from .application_management import get_call_center_supervisor_application_management_router
from .feedback import get_call_center_supervisor_feedback_router
from .inbox import get_call_center_supervisor_inbox_router
from .language import get_call_center_supervisor_language_router
from .notification_management import get_call_center_supervisor_notification_management_router
from .orders import get_call_center_supervisor_orders_router
from .staff_application_creation import get_call_center_supervisor_staff_application_creation_router
from .statistics import get_call_center_supervisor_statistics_router
from .workflow_management import get_call_center_supervisor_workflow_management_router
from .export import get_call_center_supervisor_export_router

def get_call_center_supervisor_router():
    """Get the complete call center supervisor router with all handlers"""
    from aiogram import Router
    router = Router()
    
    # Include handlers in priority order
    router.include_router(get_call_center_supervisor_main_menu_router())
    router.include_router(get_call_center_supervisor_application_management_router())
    router.include_router(get_call_center_supervisor_feedback_router())
    router.include_router(get_call_center_supervisor_inbox_router())
    router.include_router(get_call_center_supervisor_language_router())
    router.include_router(get_call_center_supervisor_notification_management_router())
    router.include_router(get_call_center_supervisor_orders_router())
    router.include_router(get_call_center_supervisor_staff_application_creation_router())
    router.include_router(get_call_center_supervisor_statistics_router())
    router.include_router(get_call_center_supervisor_workflow_management_router())
    router.include_router(get_call_center_supervisor_export_router())
    
    return router 
