"""
Main Handlers Module - Simplified Implementation

This module sets up all role-based routers with clean integration.
All modules have been simplified to focus on core functionality.
"""

from aiogram import Dispatcher

def setup_handlers(dp: Dispatcher):
    """Setup all role-based handlers with proper priority"""
    try:
        # Import start handler first (highest priority)
        from handlers.start_handler import get_start_router
        start_router = get_start_router()
        dp.include_router(start_router)
        
        # Import all role routers
        from handlers.admin import get_admin_router
        from handlers.manager import get_manager_router
        from handlers.junior_manager import get_junior_manager_router
        from handlers.controller import get_controller_router
        from handlers.technician import get_technician_router
        from handlers.client import get_client_router
        from handlers.call_center import get_call_center_router
        from handlers.call_center_supervisor import get_call_center_supervisor_router
        from handlers.warehouse import get_warehouse_router
        
        # Include role-based routers in order of usage frequency
        # Client router should be included early since it's the most common
        client_router = get_client_router()
        dp.include_router(client_router)
        
        # Include manager router early to ensure it gets priority for inbox handlers
        manager_router = get_manager_router()
        dp.include_router(manager_router)
        
        # Include other role routers
        call_center_router = get_call_center_router()
        dp.include_router(call_center_router)
        
        call_center_supervisor_router = get_call_center_supervisor_router()
        dp.include_router(call_center_supervisor_router)
        
        technician_router = get_technician_router()
        dp.include_router(technician_router)
        
        junior_manager_router = get_junior_manager_router()
        dp.include_router(junior_manager_router)
        
        controller_router = get_controller_router()
        dp.include_router(controller_router)
        
        warehouse_router = get_warehouse_router()
        dp.include_router(warehouse_router)
        
        admin_router = get_admin_router()
        dp.include_router(admin_router)

        
        print("✅ All handlers setup completed successfully")
        
    except Exception as e:
        print(f"❌ Error setting up handlers: {e}")
        raise

def get_global_instances():
    """Get global instances for use in handlers (simplified)"""
    return {
        'mock_data': True  # Indicate mock data usage
    }
