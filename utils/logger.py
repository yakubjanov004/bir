"""
Logger Utility - Testbot

Bu modul testbot uchun maxsus logger funksiyalarini taqdim etadi.
"""

import logging
import traceback
from datetime import datetime
from typing import Optional, Any

# Asosiy logger
logger = logging.getLogger(__name__)

# Activity logger
activity_logger = logging.getLogger('activity')

# Error logger
error_logger = logging.getLogger('error')

def get_logger(name: str):
    """Get logger for specific module"""
    return logging.getLogger(name)

def log_user_activity(user_id: int, user_name: str, action: str, details: Optional[str] = None):
    """Foydalanuvchi faolligini log qilish"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] User {user_id} ({user_name}) - {action}"
    if details:
        log_message += f" - {details}"
    
    print(f"📝 {log_message}")
    activity_logger.info(log_message)

def log_error(user_id: Optional[int], user_name: Optional[str], error: Exception, context: str = ""):
    """Xatolikni log qilish"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_type = type(error).__name__
    error_msg = str(error)
    
    log_message = f"[{timestamp}] ERROR - User {user_id} ({user_name}) - {error_type}: {error_msg}"
    if context:
        log_message += f" - Context: {context}"
    
    print(f"❌ {log_message}")
    print(f"📁 Error type: {error_type}")
    print(f"🔍 Error location: {error.__traceback__.tb_frame.f_code.co_filename}")
    print(f"📄 Line number: {error.__traceback__.tb_lineno}")
    print(f"📋 Full traceback:")
    traceback.print_exc()
    
    error_logger.error(log_message, exc_info=True)

def log_handler_start(handler_name: str, user_id: int, user_name: str):
    """Handler boshlanishini log qilish"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] Handler START - {handler_name} - User {user_id} ({user_name})"
    
    print(f"🚀 {log_message}")
    activity_logger.info(log_message)

def log_handler_end(handler_name: str, user_id: int, user_name: str, success: bool = True):
    """Handler tugashini log qilish"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "FAILED"
    log_message = f"[{timestamp}] Handler END - {handler_name} - User {user_id} ({user_name}) - {status}"
    
    print(f"✅ {log_message}" if success else f"❌ {log_message}")
    activity_logger.info(log_message)

def log_database_operation(operation: str, table: str, user_id: Optional[int] = None, details: Optional[str] = None):
    """Ma'lumotlar bazasi operatsiyalarini log qilish"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] DB {operation} - Table: {table}"
    if user_id:
        log_message += f" - User: {user_id}"
    if details:
        log_message += f" - Details: {details}"
    
    print(f"🗄️ {log_message}")
    activity_logger.info(log_message)

def log_state_change(user_id: int, user_name: str, old_state: Optional[str], new_state: str):
    """FSM holat o'zgarishini log qilish"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] STATE CHANGE - User {user_id} ({user_name}) - {old_state} → {new_state}"
    
    print(f"🔄 {log_message}")
    activity_logger.info(log_message)

def log_role_access(user_id: int, user_name: str, role: str, action: str):
    """Rol kirishini log qilish"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] ROLE ACCESS - User {user_id} ({user_name}) - Role: {role} - Action: {action}"
    
    print(f"👤 {log_message}")
    activity_logger.info(log_message)

def log_system_event(event: str, details: Optional[str] = None):
    """Tizim hodisasini log qilish"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] SYSTEM - {event}"
    if details:
        log_message += f" - {details}"
    
    print(f"⚙️ {log_message}")
    activity_logger.info(log_message) 