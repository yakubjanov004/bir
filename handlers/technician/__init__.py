"""
Technician Module - Complete Implementation

This module provides complete technician functionality including:
- Main menu and navigation
- Inbox management
- Reports and statistics
- Help and support
- Communication features
- Equipment management
- Language settings
"""

from aiogram import Router
from .main_menu import get_technician_main_menu_router
from .inbox import get_technician_inbox_router
from .reports import get_reports_router
from .help import get_help_router
from .communication import get_technician_communication_router
from .equipment import get_technician_equipment_router

def get_technician_router():
    """Get the complete technician router with all handlers"""
    router = Router()

    # Include all technician routers
    router.include_router(get_technician_main_menu_router())
    router.include_router(get_technician_inbox_router())
    router.include_router(get_reports_router())
    router.include_router(get_help_router())
    router.include_router(get_technician_communication_router())
    router.include_router(get_technician_equipment_router())

    return router

