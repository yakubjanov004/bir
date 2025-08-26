"""
Technician States

This module defines all state classes for the Technician role.
"""

from aiogram.fsm.state import State, StatesGroup


class TechnicianMainMenuStates(StatesGroup):
    """Main menu states for technician"""
    main_menu = State()


class TechnicianCommunicationStates(StatesGroup):
    """Communication states for technician"""
    sending_message = State()
    waiting_for_message = State()
    waiting_for_location = State()
    waiting_for_manager_message = State()


class TechnicianEquipmentStates(StatesGroup):
    """Equipment states for technician"""
    viewing_equipment = State()
    entering_equipment_details = State()
    waiting_for_equipment_request = State()


class TechnicianHelpStates(StatesGroup):
    """Help states for technician"""
    help_menu = State()
    waiting_for_manager_message = State()


class TechnicianWorkflowStates(StatesGroup):
    """Workflow states for technician"""
    viewing_tasks = State()
    task_details = State()
    working_on_task = State()
    completing_task = State()
    reporting_issue = State()
    requesting_equipment = State()
    contacting_manager = State()
    waiting_for_diagnosis = State()
    waiting_for_warehouse_decision = State()
    waiting_for_material_selection = State()
    waiting_for_material_quantity = State()
    confirming_materials = State()
    waiting_for_comment = State()
    entering_service_order_number = State()
    entering_diagnostics_result = State()


class TechnicianStates(StatesGroup):
    """General states for technician"""
    waiting_for_diagnostic = State()
    waiting_for_work_notes = State()
    waiting_for_warehouse_item = State()
    waiting_for_warehouse_quantity = State() 