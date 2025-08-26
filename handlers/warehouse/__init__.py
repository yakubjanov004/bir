"""
Warehouse Module - Complete Implementation

This module provides complete warehouse functionality including:
- Main menu and navigation
- Orders management
- Inventory management
- Export functionality
- Language settings
- Statistics and reports
- Inbox management
- Workflow integration
- Role integration
"""

from aiogram import Router
from .main_menu import get_warehouse_main_keyboard_router
from .orders import get_warehouse_orders_router
from .inventory import get_warehouse_inventory_router
from .export import get_warehouse_export_router
from .statistics import get_warehouse_statistics_router
from .inbox import get_warehouse_inbox_router
from .workflow_integration import get_warehouse_workflow_router
from .role_integration import get_warehouse_role_integration_router

def get_warehouse_router():
    """Get the complete warehouse router with all handlers"""
    router = Router()
    
    # Include all warehouse routers
    router.include_router(get_warehouse_main_keyboard_router())
    router.include_router(get_warehouse_orders_router())
    router.include_router(get_warehouse_inventory_router())
    router.include_router(get_warehouse_export_router())
    router.include_router(get_warehouse_statistics_router())
    router.include_router(get_warehouse_inbox_router())
    router.include_router(get_warehouse_workflow_router())
    router.include_router(get_warehouse_role_integration_router())
    
    return router

def get_warehouse_role_integration():
    """Get the warehouse role integration router"""
    return get_warehouse_role_integration_router()
