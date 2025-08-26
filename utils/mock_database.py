"""
Mock Database Module - Centralized mock data for all handlers

This module provides mock database functions that simulate real database operations.
All handlers should import from this module instead of creating their own mock functions.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import random

# Mock users data
MOCK_USERS = {
    123456789: {
        "id": 1,
        "telegram_id": 123456789,
        "full_name": "Manager User",
        "phone": "+998901234567",
        "role": "manager",
        "language": "uz",
        "region": "toshkent",
        "created_at": datetime.now() - timedelta(days=30)
    },
    987654321: {
        "id": 2,
        "telegram_id": 987654321,
        "full_name": "Client User",
        "phone": "+998909876543",
        "role": "client",
        "language": "uz",
        "region": "toshkent",
        "created_at": datetime.now() - timedelta(days=20)
    },
    111111111: {
        "id": 3,
        "telegram_id": 111111111,
        "full_name": "Junior Manager",
        "phone": "+998901111111",
        "role": "junior_manager",
        "language": "uz",
        "region": "toshkent",
        "created_at": datetime.now() - timedelta(days=25)
    },
    222222222: {
        "id": 4,
        "telegram_id": 222222222,
        "full_name": "Controller User",
        "phone": "+998902222222",
        "role": "controller",
        "language": "uz",
        "region": "toshkent",
        "created_at": datetime.now() - timedelta(days=15)
    },
    333333333: {
        "id": 5,
        "telegram_id": 333333333,
        "full_name": "Technician User",
        "phone": "+998903333333",
        "role": "technician",
        "language": "uz",
        "region": "toshkent",
        "created_at": datetime.now() - timedelta(days=10)
    }
}

# Mock applications data
MOCK_APPLICATIONS = [
    {
        "id": "APP_2024_001",
        "client_name": "Alisher Karimov",
        "client_phone": "+998901234567",
        "address": "Toshkent, Chilonzor 5",
        "service_type": "connection",
        "status": "new",
        "created_at": datetime.now() - timedelta(hours=2),
        "manager_id": 1,
        "technician_id": None,
        "notes": "Yangi ulanish"
    },
    {
        "id": "APP_2024_002",
        "client_name": "Dilshod Rahimov",
        "client_phone": "+998909876543",
        "address": "Toshkent, Yunusobod 10",
        "service_type": "technical",
        "status": "in_progress",
        "created_at": datetime.now() - timedelta(hours=5),
        "manager_id": 1,
        "technician_id": 5,
        "notes": "Internet sekin ishlayapti"
    },
    {
        "id": "APP_2024_003",
        "client_name": "Sardor Azimov",
        "client_phone": "+998905555555",
        "address": "Toshkent, Mirzo Ulugbek 7",
        "service_type": "connection",
        "status": "completed",
        "created_at": datetime.now() - timedelta(days=1),
        "manager_id": 1,
        "technician_id": 5,
        "notes": "Muvaffaqiyatli ulandi"
    }
]

async def get_user_by_telegram_id(telegram_id: int, region: str = None) -> Optional[Dict[str, Any]]:
    """Get user by telegram ID from mock database"""
    return MOCK_USERS.get(telegram_id)

async def get_users_by_role(role: str, region: str = None) -> List[Dict[str, Any]]:
    """Get all users with specific role from mock database"""
    return [user for user in MOCK_USERS.values() if user.get("role") == role]

async def get_user_by_id(user_id: int, region: str = None) -> Optional[Dict[str, Any]]:
    """Get user by internal ID from mock database"""
    for user in MOCK_USERS.values():
        if user.get("id") == user_id:
            return user
    return None

async def get_applications(region: str = None, **filters) -> List[Dict[str, Any]]:
    """Get applications with optional filters from mock database"""
    applications = MOCK_APPLICATIONS.copy()
    
    # Apply filters
    if filters.get("status"):
        applications = [app for app in applications if app["status"] == filters["status"]]
    if filters.get("manager_id"):
        applications = [app for app in applications if app["manager_id"] == filters["manager_id"]]
    if filters.get("technician_id"):
        applications = [app for app in applications if app["technician_id"] == filters["technician_id"]]
    if filters.get("service_type"):
        applications = [app for app in applications if app["service_type"] == filters["service_type"]]
    
    return applications

async def get_application_by_id(app_id: str, region: str = None) -> Optional[Dict[str, Any]]:
    """Get single application by ID from mock database"""
    for app in MOCK_APPLICATIONS:
        if app["id"] == app_id:
            return app
    return None

async def get_application_statistics(region: str = None, manager_id: int = None) -> Dict[str, int]:
    """Get application statistics from mock database"""
    applications = await get_applications(region, manager_id=manager_id)
    
    stats = {
        "total": len(applications),
        "new": len([a for a in applications if a["status"] == "new"]),
        "in_progress": len([a for a in applications if a["status"] == "in_progress"]),
        "completed": len([a for a in applications if a["status"] == "completed"]),
        "cancelled": len([a for a in applications if a["status"] == "cancelled"]),
        "active": len([a for a in applications if a["status"] in ["new", "in_progress"]]),
        "today": len([a for a in applications if (datetime.now() - a["created_at"]).days == 0]),
        "this_week": len([a for a in applications if (datetime.now() - a["created_at"]).days <= 7])
    }
    
    return stats

async def create_application(data: Dict[str, Any], region: str = None) -> Dict[str, Any]:
    """Create new application in mock database"""
    new_app = {
        "id": f"APP_2024_{len(MOCK_APPLICATIONS) + 1:03d}",
        "created_at": datetime.now(),
        "status": "new",
        **data
    }
    MOCK_APPLICATIONS.append(new_app)
    return new_app

async def update_application(app_id: str, updates: Dict[str, Any], region: str = None) -> Optional[Dict[str, Any]]:
    """Update application in mock database"""
    for app in MOCK_APPLICATIONS:
        if app["id"] == app_id:
            app.update(updates)
            return app
    return None

# Mock clients data
MOCK_CLIENTS = [
    {
        "id": 1,
        "name": "Alisher Karimov",
        "phone": "+998901234567",
        "address": "Toshkent, Chilonzor 5",
        "tariff": "Premium",
        "balance": 150000,
        "status": "active"
    },
    {
        "id": 2,
        "name": "Dilshod Rahimov", 
        "phone": "+998909876543",
        "address": "Toshkent, Yunusobod 10",
        "tariff": "Standard",
        "balance": 75000,
        "status": "active"
    },
    {
        "id": 3,
        "name": "Sardor Azimov",
        "phone": "+998905555555",
        "address": "Toshkent, Mirzo Ulugbek 7",
        "tariff": "Basic",
        "balance": -25000,
        "status": "suspended"
    }
]

async def search_clients(query: str, search_type: str = "name", region: str = None) -> List[Dict[str, Any]]:
    """Search clients in mock database"""
    results = []
    query = query.lower()
    
    for client in MOCK_CLIENTS:
        if search_type == "name" and query in client["name"].lower():
            results.append(client)
        elif search_type == "phone" and query in client["phone"]:
            results.append(client)
        elif search_type == "id" and str(client["id"]) == query:
            results.append(client)
    
    return results

async def get_client_by_id(client_id: int, region: str = None) -> Optional[Dict[str, Any]]:
    """Get client by ID from mock database"""
    for client in MOCK_CLIENTS:
        if client["id"] == client_id:
            return client
    return None

# Export all functions for easy import
__all__ = [
    'get_user_by_telegram_id',
    'get_users_by_role',
    'get_user_by_id',
    'get_applications',
    'get_application_by_id',
    'get_application_statistics',
    'create_application',
    'update_application',
    'search_clients',
    'get_client_by_id',
    'MOCK_USERS',
    'MOCK_APPLICATIONS',
    'MOCK_CLIENTS'
]