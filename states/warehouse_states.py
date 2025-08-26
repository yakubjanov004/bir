"""
Warehouse States

This module defines all state classes for the Warehouse role.
"""

from aiogram.fsm.state import State, StatesGroup


class WarehouseMainMenuStates(StatesGroup):
    """Main menu states for warehouse"""
    main_menu = State()


class WarehouseOrdersStates(StatesGroup):
    """Order states for warehouse"""
    viewing_orders = State()
    entering_order_number = State()
    viewing_order_details = State()
    orders_menu = State()


class WarehouseInventoryStates(StatesGroup):
    """Inventory states for warehouse"""
    inventory_menu = State()
    viewing_inventory = State()
    entering_item_details = State()
    selecting_item = State()
    adding_item_name = State()
    adding_item_quantity = State()
    adding_item_price = State()
    adding_item_total = State()
    adding_item_description = State()
    adding_item_image = State()
    adding_item_location = State()
    adding_item_status = State()
    selecting_item_to_update = State()
    updating_item_quantity = State()
    updating_item_info = State()
    searching_inventory = State()


class WarehouseExportStates(StatesGroup):
    """Export states for warehouse"""
    selecting_type = State()
    selecting_format = State()
    exporting_data = State()
    selecting_export_type = State()
    entering_export_details = State()


class WarehouseStatisticsStates(StatesGroup):
    """Statistics states for warehouse"""
    viewing_statistics = State()
    selecting_report_type = State()
    statistics_menu = State()
    period_menu = State()


class WarehouseWorkflowStates(StatesGroup):
    """Workflow states for warehouse"""
    workflow_monitoring = State()
    workflow_optimization = State()
    entering_return_reason = State()
    preparing_equipment = State() 