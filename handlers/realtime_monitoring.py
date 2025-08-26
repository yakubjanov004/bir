"""
Menejer uchun real vaqtda kuzatish handleri - Mock Data Version

Bu modul manager uchun real vaqtda monitoring funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, database kerak emas.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from keyboards.manager_buttons import (
    get_manager_realtime_keyboard,
    get_realtime_navigation_keyboard
)
from .message_builders import (
    build_main_dashboard_message,
    build_applications_list_message,
    build_technicians_list_message
)
import logging
import json
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Constants
ITEMS_PER_PAGE = 5

# Mock data for realtime monitoring
MOCK_APPLICATIONS = [
    {
        'id': 'APP001',
        'client_name': 'Aziz Karimov',
        'status': 'active',
        'priority': 'high',
        'type': 'connection',
        'created_at': datetime.now() - timedelta(hours=2),
        'updated_at': datetime.now() - timedelta(minutes=30),
        'assigned_to': 'Technician 1',
        'region': 'toshkent',
        'description': 'Internet ulanish so\'rovi'
    },
    {
        'id': 'APP002',
        'client_name': 'Malika Yusupova',
        'status': 'active',
        'priority': 'urgent',
        'type': 'technical',
        'created_at': datetime.now() - timedelta(hours=1),
        'updated_at': datetime.now() - timedelta(minutes=15),
        'assigned_to': 'Technician 2',
        'region': 'toshkent',
        'description': 'Internet tezligi past'
    },
    {
        'id': 'APP003',
        'client_name': 'Jasur Toshmatov',
        'status': 'pending',
        'priority': 'normal',
        'type': 'connection',
        'created_at': datetime.now() - timedelta(hours=3),
        'updated_at': datetime.now() - timedelta(hours=2),
        'assigned_to': None,
        'region': 'toshkent',
        'description': 'Yangi uy uchun internet'
    },
    {
        'id': 'APP004',
        'client_name': 'Dilfuza Rahimova',
        'status': 'active',
        'priority': 'urgent',
        'type': 'technical',
        'created_at': datetime.now() - timedelta(minutes=45),
        'updated_at': datetime.now() - timedelta(minutes=10),
        'assigned_to': 'Technician 3',
        'region': 'toshkent',
        'description': 'Router muammosi'
    },
    {
        'id': 'APP005',
        'client_name': 'Rustam Alimov',
        'status': 'completed',
        'priority': 'low',
        'type': 'connection',
        'created_at': datetime.now() - timedelta(hours=5),
        'updated_at': datetime.now() - timedelta(hours=4),
        'assigned_to': 'Technician 1',
        'region': 'toshkent',
        'description': 'Ofis uchun internet'
    },
    {
        'id': 'APP006',
        'client_name': 'Zarina Karimova',
        'status': 'active',
        'priority': 'high',
        'type': 'technical',
        'created_at': datetime.now() - timedelta(hours=1, minutes=30),
        'updated_at': datetime.now() - timedelta(minutes=20),
        'assigned_to': 'Technician 2',
        'region': 'toshkent',
        'description': 'Internet uzilishi'
    }
]

# Mock technicians data
MOCK_TECHNICIANS = [
    {
        'id': 1,
        'name': 'Technician 1',
        'status': 'busy',
        'current_task': 'APP001',
        'region': 'toshkent',
        'last_seen': datetime.now() - timedelta(minutes=5)
    },
    {
        'id': 2,
        'name': 'Technician 2',
        'status': 'busy',
        'current_task': 'APP002',
        'region': 'toshkent',
        'last_seen': datetime.now() - timedelta(minutes=2)
    },
    {
        'id': 3,
        'name': 'Technician 3',
        'status': 'available',
        'current_task': None,
        'region': 'toshkent',
        'last_seen': datetime.now() - timedelta(minutes=1)
    },
    {
        'id': 4,
        'name': 'Technician 4',
        'status': 'offline',
        'current_task': None,
        'region': 'toshkent',
        'last_seen': datetime.now() - timedelta(hours=2)
    }
]

def calculate_time_duration(start_time: datetime, end_time: datetime = None) -> str:
    """Calculate time duration between start and end time"""
    if end_time is None:
        end_time = datetime.now()
    
    duration = end_time - start_time
    total_seconds = int(duration.total_seconds())
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}s {minutes}d"
    else:
        return f"{minutes} daqiqa"

def get_priority_emoji(priority: str) -> str:
    """Get priority emoji based on priority level"""
    priority_emojis = {
        'urgent': '🔴',
        'high': '🟠', 
        'normal': '🟡',
        'low': '🟢'
    }
    return priority_emojis.get(priority, '⚪')

def get_status_emoji(duration_minutes: int) -> str:
    """Get status emoji based on duration"""
    if duration_minutes <= 30:
        return '🟢'
    elif duration_minutes <= 60:
        return '🟡'
    else:
        return '🔴'

def get_manager_realtime_dashboard_mock(region: str = 'toshkent'):
    """Get manager realtime dashboard from mock data"""
    try:
        now = datetime.now()
        
        # Filter applications by region
        applications = [app for app in MOCK_APPLICATIONS if app['region'] == region]
        
        # Filter and categorize
        active_requests = []
        urgent_count = 0
        normal_count = 0
        low_count = 0
        
        for app in applications:
            if app['status'] not in ['completed', 'cancelled']:
                # Calculate durations
                created_at = app['created_at']
                updated_at = app['updated_at']
                
                # Calculate time since creation and last update
                time_since_creation = now - created_at
                time_since_update = now - updated_at
                
                creation_minutes = int(time_since_creation.total_seconds() / 60)
                update_minutes = int(time_since_update.total_seconds() / 60)
                
                # Add to counts
                if app['priority'] == 'urgent':
                    urgent_count += 1
                elif app['priority'] == 'high':
                    normal_count += 1
                else:
                    low_count += 1
                
                # Add to active requests
                active_requests.append({
                    'id': app['id'],
                    'client_name': app['client_name'],
                    'status': app['status'],
                    'priority': app['priority'],
                    'type': app['type'],
                    'created_at': created_at,
                    'updated_at': updated_at,
                    'assigned_to': app['assigned_to'],
                    'creation_minutes': creation_minutes,
                    'update_minutes': update_minutes,
                    'description': app['description']
                })
        
        # Sort by priority and time
        active_requests.sort(key=lambda x: (
            {'urgent': 0, 'high': 1, 'normal': 2, 'low': 3}[x['priority']],
            x['creation_minutes']
        ))
        
        return {
            'active_requests': active_requests,
            'urgent_count': urgent_count,
            'normal_count': normal_count,
            'low_count': low_count,
            'total_active': len(active_requests)
        }
        
    except Exception as e:
        logger.error(f"Error getting mock realtime dashboard: {e}")
        return {
            'active_requests': [],
            'urgent_count': 0,
            'normal_count': 0,
            'low_count': 0,
            'total_active': 0
        }

def get_technicians_status_mock(region: str = 'toshkent'):
    """Get technicians status from mock data"""
    try:
        # Filter technicians by region
        technicians = [tech for tech in MOCK_TECHNICIANS if tech['region'] == region]
        
        # Calculate status counts
        busy_count = len([tech for tech in technicians if tech['status'] == 'busy'])
        available_count = len([tech for tech in technicians if tech['status'] == 'available'])
        offline_count = len([tech for tech in technicians if tech['status'] == 'offline'])
        
        return {
            'technicians': technicians,
            'busy_count': busy_count,
            'available_count': available_count,
            'offline_count': offline_count,
            'total_technicians': len(technicians)
        }
        
    except Exception as e:
        logger.error(f"Error getting mock technicians status: {e}")
        return {
            'technicians': [],
            'busy_count': 0,
            'available_count': 0,
            'offline_count': 0,
            'total_technicians': 0
        }

def get_manager_realtime_monitoring_router():
    """Router for realtime monitoring with mock data"""
    router = Router()
    
    # --- Main Dashboard --- #
    @router.message(F.text.in_(["🕐 Real vaqtda kuzatish", "🕐 Мониторинг в реальном времени"])) # Matn tugmaga moslashtirildi
    async def show_realtime_monitoring_dashboard(message: Message, state: FSMContext):
        """Show realtime monitoring dashboard"""
        try:
            mock_user = {'language': 'uz'} # Simplified mock
            lang = mock_user.get('language', 'uz')
            
            dashboard_data = get_manager_realtime_dashboard_mock('toshkent')
            technicians_data = get_technicians_status_mock('toshkent')
            
            text = build_main_dashboard_message(dashboard_data, technicians_data, lang)
            keyboard = get_manager_realtime_keyboard(lang)
            
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error showing realtime monitoring dashboard: {e}")
            await message.answer("❌ Xatolik yuz berdi")

    # --- Callback Handlers --- #
    @router.callback_query(F.data.startswith("rm:"))
    async def handle_realtime_callbacks(callback: CallbackQuery, state: FSMContext):
        """Unified handler for all realtime monitoring callbacks."""
        try:
            await callback.answer()
            mock_user = {'language': 'uz'} # Simplified mock
            lang = mock_user.get('language', 'uz')

            action_parts = callback.data.split(':')
            action = action_parts[1]

            if action == 'back':
                await show_dashboard_from_callback(callback, lang)
                return

            if action == 'refresh':
                await refresh_dashboard(callback, lang)
                return

            if action in ['list', 'urgent', 'techs']:
                page = int(action_parts[2])
                await show_paginated_list(callback, lang, action, page)
                return
            
            if action == 'nav':
                direction, context, page_str = action_parts[2], action_parts[3], action_parts[4]
                current_page = int(page_str)
                next_page = current_page + 1 if direction == 'next' else current_page - 1
                await show_paginated_list(callback, lang, context, next_page)
                return

        except Exception as e:
            logger.error(f"Error in realtime callback handler: {e}")
            await callback.message.answer("❌ Xatolik yuz berdi")

    # --- Helper Functions for Callbacks --- #
    async def show_dashboard_from_callback(callback: CallbackQuery, lang: str):
        """Shows the main dashboard, editing the existing message."""
        dashboard_data = get_manager_realtime_dashboard_mock('toshkent')
        technicians_data = get_technicians_status_mock('toshkent')
        text = build_main_dashboard_message(dashboard_data, technicians_data, lang)
        keyboard = get_manager_realtime_keyboard(lang)
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')

    async def refresh_dashboard(callback: CallbackQuery, lang: str):
        """Refreshes the main dashboard view."""
        dashboard_data = get_manager_realtime_dashboard_mock('toshkent')
        technicians_data = get_technicians_status_mock('toshkent')
        text = build_main_dashboard_message(dashboard_data, technicians_data, lang, updated=True)
        keyboard = get_manager_realtime_keyboard(lang)
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')

    async def show_paginated_list(callback: CallbackQuery, lang: str, context: str, page: int):
        """Displays a paginated list of applications or technicians."""
        if context == 'list' or context == 'urgent':
            all_apps = get_manager_realtime_dashboard_mock('toshkent')['active_requests']
            if context == 'urgent':
                items = [app for app in all_apps if app['priority'] == 'urgent']
            else:
                items = all_apps
            builder_func = build_applications_list_message
        elif context == 'techs':
            items = get_technicians_status_mock('toshkent')['technicians']
            builder_func = build_technicians_list_message
        else:
            return

        total_items = len(items)
        total_pages = (total_items + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        start_index = (page - 1) * ITEMS_PER_PAGE
        end_index = start_index + ITEMS_PER_PAGE
        paginated_items = items[start_index:end_index]

        text = builder_func(paginated_items, page, total_pages, lang)
        keyboard = get_realtime_navigation_keyboard(lang, context, page, total_pages)
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')

    return router