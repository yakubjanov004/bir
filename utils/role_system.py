"""
Role System - Complete Implementation

This module handles role-based routing and user role detection
for the Alfa Connect bot.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from loader import get_user_role, get_bot
import time
from typing import Dict, Optional

# Global role cache to reduce database queries
_role_cache: Dict[int, str] = {}
_role_cache_timestamps: Dict[int, float] = {}
_cache_duration = 300  # 5 minutes

def invalidate_role_cache(user_id: int = None):
    """Invalidate role cache for specific user or all users"""
    global _role_cache, _role_cache_timestamps
    
    if user_id is None:
        _role_cache.clear()
        _role_cache_timestamps.clear()
        print("Global role cache cleared")
    else:
        _role_cache.pop(user_id, None)
        _role_cache_timestamps.pop(user_id, None)
        print(f"Role cache cleared for user: {user_id}")

def get_cached_role(user_id: int) -> Optional[str]:
    """Get cached role if available and not expired"""
    global _role_cache, _role_cache_timestamps
    
    if user_id in _role_cache:
        timestamp = _role_cache_timestamps.get(user_id, 0)
        if time.time() - timestamp < _cache_duration:
            return _role_cache[user_id]
        else:
            # Remove expired cache
            _role_cache.pop(user_id, None)
            _role_cache_timestamps.pop(user_id, None)
    
    return None

def cache_role(user_id: int, role: str):
    """Cache user role with timestamp"""
    global _role_cache, _role_cache_timestamps
    
    _role_cache[user_id] = role
    _role_cache_timestamps[user_id] = time.time()

def get_role_router(role: str):
    """Get router for specific role - centralized function to avoid duplicates"""
    router = Router()
    
    # No role filtering - allow all handlers to work normally
    return router

def get_efficient_role_router(role: str) -> Router:
    """
    Returns the most efficient Router for the given role.
    This is the recommended router to use for all role-based handlers.
    """
    from filters.role_filter import RoleFilter
    
    router = Router(name=f"{role}_efficient_router")
    
    # Use efficient role filter with caching
    role_filter = RoleFilter(role)
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    return router

def get_lightweight_router(role: str) -> Router:
    """
    Returns a lightweight Router without role filters for use when handlers 
    already have their own role filtering to avoid redundant checks.
    """
    return Router(name=f"{role}_lightweight_router")

def get_filtered_role_router(role: str) -> Router:
    """
    Returns a Router WITH role filters for special cases where router-level filtering is needed.
    Use this only when absolutely necessary.
    """
    from filters.role_filter import RoleFilter
    
    router = Router(name=f"{role}_filtered_router")
    role_filter = RoleFilter(role)
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    return router

def get_optimized_role_router(role: str) -> Router:
    """
    Returns an optimized Router that uses efficient role checking.
    This reduces database queries and improves performance.
    """
    from filters.role_filter import RoleFilter
    
    router = Router(name=f"{role}_optimized_router")
    
    # Use optimized role filter
    role_filter = RoleFilter(role)
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    return router

async def show_role_menu(message: Message, user_role: str):
    """Show appropriate menu based on user role"""
    user_id = message.from_user.id
    
    if user_role == 'admin':
        await show_admin_menu(message)
    elif user_role == 'manager':
        await show_manager_menu(message)
    elif user_role == 'client':
        await show_client_menu(message)
    elif user_role == 'technician':
        await show_technician_menu(message)
    elif user_role == 'warehouse':
        await show_warehouse_menu(message)
    elif user_role == 'call_center':
        await show_call_center_menu(message)
    elif user_role == 'call_center_supervisor':
        await show_call_center_supervisor_menu(message)
    elif user_role == 'junior_manager':
        await show_junior_manager_menu(message)
    elif user_role == 'controller':
        await show_controller_menu(message)
    else:
        await show_default_menu(message)

async def show_admin_menu(message: Message):
    """Show admin menu"""
    from keyboards.admin_buttons import get_admin_main_keyboard
    
    text = "👨‍💼 Admin paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_admin_main_keyboard('uz')
    
    await message.answer(text, reply_markup=keyboard)

async def show_manager_menu(message: Message):
    """Show manager menu"""
    from keyboards.manager_buttons import get_manager_main_keyboard
    
    text = "👨‍💼 Menejer paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_manager_main_keyboard('uz')
    
    await message.answer(text, reply_markup=keyboard)

async def show_client_menu(message: Message):
    """Show client menu"""
    from keyboards.client_buttons import get_client_main_keyboard
    
    text = "👤 Mijoz paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_client_main_keyboard('uz')
    
    await message.answer(text, reply_markup=keyboard)

async def show_technician_menu(message: Message):
    """Show technician menu"""
    from keyboards.technician_buttons import get_technician_main_keyboard
    
    text = "👨‍🔧 Texnik paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_technician_main_keyboard('uz')
    
    await message.answer(text, reply_markup=keyboard)

async def show_warehouse_menu(message: Message):
    """Show warehouse menu"""
    from keyboards.warehouse_buttons import get_warehouse_main_keyboard
    
    text = "📦 Ombor paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_warehouse_main_keyboard('uz')
    
    await message.answer(text, reply_markup=keyboard)

async def show_call_center_menu(message: Message):
    """Show call center menu"""
    from keyboards.call_center_buttons import get_call_center_main_keyboard
    
    text = "📞 Call Center paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_call_center_main_keyboard('uz')
    
    await message.answer(text, reply_markup=keyboard)

async def show_call_center_supervisor_menu(message: Message):
    """Show call center supervisor menu"""
    from keyboards.call_center_supervisor_buttons import get_call_center_supervisor_main_keyboard
    
    text = "👨‍💼 Call Center Supervisor paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_call_center_supervisor_main_keyboard('uz')
    
    await message.answer(text, reply_markup=keyboard)

async def show_junior_manager_menu(message: Message):
    """Show junior manager menu"""
    from keyboards.junior_manager_buttons import get_junior_manager_main_keyboard
    
    text = "👨‍💼 Kichik Menejer paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_junior_manager_main_keyboard('uz')
    
    await message.answer(text, reply_markup=keyboard)

async def show_controller_menu(message: Message):
    """Show controller menu"""
    from keyboards.controllers_buttons import get_controller_main_keyboard
    
    text = "🎛️ Kontroller paneliga xush kelibsiz!\n\nQuyidagi funksiyalardan birini tanlang:"
    keyboard = get_controller_main_keyboard('uz')
    
    await message.answer(text, reply_markup=keyboard)

async def show_default_menu(message: Message):
    """Show default menu for unknown roles"""
    text = "👋 Xush kelibsiz!\n\nSizning rolingiz hali aniqlanmagan. Iltimos, administrator bilan bog'laning."
    
    await message.answer(text)