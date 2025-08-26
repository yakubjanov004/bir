"""
Controller Module - Complete Implementation

This module provides controller functionality including:
- Application creation and management
- Inbox management
- Language settings
- Main menu and dashboard
- Monitoring and real-time tracking
- Order management
- Technical service management
- Export
"""

from aiogram import Router
from .connection_service import get_controller_connection_service_router
from .inbox import get_controller_inbox_router
from .language import get_controller_language_router
from .monitoring import get_controller_monitoring_router
from .orders import get_controller_orders_router
from .realtime_monitoring import get_realtime_monitoring_router
from .technical_service import get_controller_technical_service_router
from .export import get_controller_export_router
from .technicians import get_controller_technicians_router


def get_controller_router():
    """Get the complete controller router with all handlers"""
    router = Router()

    # Include handlers in priority order
    router.include_router(get_controller_connection_service_router())
    router.include_router(get_controller_inbox_router())
    router.include_router(get_controller_language_router())
    router.include_router(get_controller_monitoring_router())
    router.include_router(get_controller_orders_router())
    router.include_router(get_realtime_monitoring_router())
    router.include_router(get_controller_technical_service_router())
    router.include_router(get_controller_technicians_router())
    router.include_router(get_controller_export_router())

    return router

__all__ = ['get_controller_router']
