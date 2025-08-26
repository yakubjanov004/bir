"""
Junior Manager Module - Complete Implementation

This module provides junior manager functionality including:
- Main menu and navigation
- Client search and management
- Connection order creation
- Inbox management
- Order viewing and management
- Statistics and reporting
- Language settings
"""

from aiogram import Router

# Import all handler routers
from .client_search import router as client_search_router
from .connection_order import router as connection_order_router
from .inbox import router as inbox_router
from .language import router as language_router
from .orders import router as orders_router
from .statistics import router as statistics_router

def get_junior_manager_router():
    """Get the complete junior manager router with all handlers"""
    router = Router(name="junior_manager")
    
    # Include all sub-routers in priority order
    router.include_router(inbox_router)
    router.include_router(orders_router)
    router.include_router(client_search_router)
    router.include_router(connection_order_router)
    router.include_router(statistics_router)
    router.include_router(language_router)
    
    return router

# Export for convenience
__all__ = [
    'get_junior_manager_router',
    'main_menu_router',
    'client_search_router', 
    'connection_order_router',
    'inbox_router',
    'language_router',
    'orders_router',
    'statistics_router'
]
