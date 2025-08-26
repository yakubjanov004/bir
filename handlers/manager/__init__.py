"""
Manager Module - Complete Implementation

This module provides complete manager functionality including:
- Main menu and navigation
- Language settings
- Inbox management
- Applications management
- Statistics and reports
- Staff activity monitoring
- Status management
- Technician assignment
- Word document generation
- Staff application creation
- Real-time monitoring
"""


from .main_menu import get_manager_main_menu_router
from .language import get_manager_language_router
from .inbox import get_manager_inbox_router_min
from .staff_activity import get_manager_staff_activity_router
from .status_management import get_manager_status_management_router
from .applications_actions import get_manager_applications_actions_router
from .applications_callbacks import get_manager_applications_callbacks_router
from .applications_list import get_manager_applications_list_router
from .applications_search import get_manager_applications_search_router
from .applications import get_manager_applications_router
from .filters import get_manager_filters_router
from .realtime_monitoring import get_manager_realtime_monitoring_router
from .export import get_manager_export_router
from .connection_order import get_manager_connection_order_router
from .technician_order import get_manager_technical_service_router

def get_manager_router():
    from aiogram import Router
    """Get the complete manager router with all handlers"""
    router = Router()
    
    router.include_router(get_manager_main_menu_router())           # Main menu first
    router.include_router(get_manager_inbox_router_min())            
    router.include_router(get_manager_applications_router())         
    router.include_router(get_manager_connection_order_router())     
    router.include_router(get_manager_technical_service_router())    
    router.include_router(get_manager_realtime_monitoring_router())  
    router.include_router(get_manager_staff_activity_router())       
    router.include_router(get_manager_status_management_router())    
    router.include_router(get_manager_export_router())               
    router.include_router(get_manager_language_router())             
    router.include_router(get_manager_applications_actions_router())
    router.include_router(get_manager_applications_callbacks_router())
    router.include_router(get_manager_applications_list_router())
    router.include_router(get_manager_applications_search_router())
    router.include_router(get_manager_filters_router())
    
    return router


