"""
Applications Actions Handler - Mock Data Implementation

Bu modul manager uchun arizalar bilan bog'liq amallar funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from filters.role_filter import RoleFilter
import logging

logger = logging.getLogger(__name__)

# Mock data storage
mock_requests = {
    "REQ001": {
        "id": "REQ001",
        "title": "Internet ulanish arizasi",
        "description": "Yangi internet xizmatini ulashish",
        "status": "created",
        "priority": "normal",
        "role_current": "manager",
        "client_name": "Ahmad Toshmatov",
        "client_phone": "+998901234567",
        "created_at": "2024-01-15 10:00:00"
    },
    "REQ002": {
        "id": "REQ002", 
        "title": "TV xizmat arizasi",
        "description": "TV kanallarini qo'shish",
        "status": "assigned_to_junior_manager",
        "priority": "high",
        "role_current": "manager",
        "client_name": "Malika Karimova",
        "client_phone": "+998901234568",
        "created_at": "2024-01-15 11:00:00"
    }
}

mock_users = {
    1: {
        'id': 1,
        'telegram_id': 123456789,
        'role': 'manager',
        'language': 'uz',
        'full_name': 'Test Manager',
        'phone_number': '+998901234567'
    },
    2: {
        'id': 2,
        'full_name': 'Ahmad Toshmatov',
        'phone_number': '+998901234568',
        'role': 'junior_manager',
        'is_active': True
    },
    3: {
        'id': 3,
        'full_name': 'Malika Karimova',
        'phone_number': '+998901234569',
        'role': 'junior_manager',
        'is_active': True
    },
    4: {
        'id': 4,
        'full_name': 'Jahongir Azimov',
        'phone_number': '+998901234570',
        'role': 'junior_manager',
        'is_active': True
    }
}

# Mock functions
async def get_user_by_telegram_id(telegram_id: int):
    """Mock get user data"""
    for user in mock_users.values():
        if user.get('telegram_id') == telegram_id:
            return user
    return None

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    user = await get_user_by_telegram_id(telegram_id)
    return user.get('language', 'uz') if user else 'uz'

async def get_users_by_role(role: str):
    """Mock get users by role"""
    return [user for user in mock_users.values() if user.get('role') == role]

async def assign_service_request(request_id: str, assigned_to: int, assigned_by: int, new_status: str):
    """Mock assign service request"""
    try:
        if request_id in mock_requests:
            mock_requests[request_id]['status'] = new_status
            mock_requests[request_id]['assigned_to'] = assigned_to
            mock_requests[request_id]['assigned_by'] = assigned_by
            print(f"Mock: Request {request_id} assigned to {assigned_to}")
            return True
        return False
    except Exception as e:
        print(f"Mock: Error assigning request: {e}")
        return False

async def complete_service_request(request_id: str, completed_by: int):
    """Mock complete service request"""
    try:
        if request_id in mock_requests:
            mock_requests[request_id]['status'] = 'completed'
            mock_requests[request_id]['completed_by'] = completed_by
            print(f"Mock: Request {request_id} completed by {completed_by}")
            return True
        return False
    except Exception as e:
        print(f"Mock: Error completing request: {e}")
        return False

async def cancel_service_request(request_id: str, cancelled_by: int):
    """Mock cancel service request"""
    try:
        if request_id in mock_requests:
            mock_requests[request_id]['status'] = 'cancelled'
            mock_requests[request_id]['cancelled_by'] = cancelled_by
            print(f"Mock: Request {request_id} cancelled by {cancelled_by}")
            return True
        return False
    except Exception as e:
        print(f"Mock: Error cancelling request: {e}")
        return False

async def update_application_priority(request_id: str, new_priority: str, updated_by: int):
    """Mock update application priority"""
    try:
        if request_id in mock_requests:
            mock_requests[request_id]['priority'] = new_priority
            mock_requests[request_id]['updated_by'] = updated_by
            print(f"Mock: Request {request_id} priority updated to {new_priority}")
            return True
        return False
    except Exception as e:
        print(f"Mock: Error updating priority: {e}")
        return False

async def get_manager_applications(region_code: str, manager_id: int, status_filter: str):
    """Mock get manager applications"""
    try:
        # Return mock requests that match the filter
        if status_filter == 'created':
            return [req for req in mock_requests.values() if req.get('status') == 'created']
        elif status_filter == 'assigned':
            return [req for req in mock_requests.values() if req.get('status') == 'assigned_to_junior_manager']
        else:
            return list(mock_requests.values())
    except Exception as e:
        print(f"Mock: Error getting applications: {e}")
        return []

# Mock audit logger
class MockAuditLogger:
    async def log_action(self, user_id: int, action: str, target_id: str, details: str):
        """Mock audit logging"""
        print(f"Mock Audit Log: User {user_id} performed {action} on {target_id} - {details}")

audit_logger = MockAuditLogger()

def get_manager_applications_actions_router():
    """Router for applications actions functionality with mock data"""
    router = Router()
    
    # Apply role filter - both manager and junior_manager can access
    role_filter = RoleFilter(["manager", "junior_manager"])
    router.callback_query.filter(role_filter)
    
    @router.callback_query(F.data.startswith("mgr_assign_jm_"))
    async def assign_to_junior_manager(callback: CallbackQuery, state: FSMContext):
        """Assign request to junior manager using mock data"""
        try:
            await callback.answer()
            
            # Extract request ID
            request_id = callback.data.replace("mgr_assign_jm_", "")
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Get available junior managers from mock data
            junior_managers = await get_users_by_role('junior_manager')
            
            if not junior_managers:
                await callback.answer("Kichik menejerlar topilmadi", show_alert=True)
                return
            
            # Create selection keyboard
            buttons = []
            for jm in junior_managers:
                buttons.append([InlineKeyboardButton(
                    text=f"👨‍💼 {jm.get('full_name', 'N/A')}",
                    callback_data=f"mgr_confirm_jm_{request_id}_{jm['id']}"
                )])
            
            # Add back button
            buttons.append([InlineKeyboardButton(
                text="⬅️ Ortga",
                callback_data="mgr_back_to_inbox"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            text = (
                f"👨‍💼 <b>Kichik menjer tanlang</b>\n\n"
                f"📝 Ariza ID: {request_id}\n\n"
                f"Quyidagi kichik menejerlardan birini tanlang:"
            )
            
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            logger.error(f"Error in assign_to_junior_manager: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("mgr_confirm_jm_"))
    async def confirm_junior_manager_assignment(callback: CallbackQuery, state: FSMContext):
        """Confirm assignment to junior manager using mock data"""
        try:
            await callback.answer()
            
            # Extract data
            parts = callback.data.replace("mgr_confirm_jm_", "").split("_")
            request_id = parts[0]
            junior_manager_id = int(parts[1])
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Update service request in mock data
            success = await assign_service_request(
                request_id=request_id,
                assigned_to=junior_manager_id,
                assigned_by=user['id'],
                new_status='assigned_to_junior_manager'
            )
            
            if success:
                # Log the assignment
                await audit_logger.log_action(
                    user_id=user['id'],
                    action='assign_to_junior_manager',
                    target_id=request_id,
                    details=f"Assigned to junior manager {junior_manager_id}"
                )
                
                text = (
                    f"✅ <b>Tayinlash muvaffaqiyatli!</b>\n\n"
                    f"📝 Ariza ID: {request_id}\n"
                    f"👨‍💼 Kichik menjerga yuborildi\n\n"
                    f"Ariza sizning inboxingizdan o'chirilib, kichik menejer inboxiga o'tdi."
                )
                
                # Add back button
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(
                        text="⬅️ Inbox'ga qaytish",
                        callback_data="mgr_back_to_inbox"
                    )
                ]])
                
                await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
            else:
                await callback.answer("Tayinlashda xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            logger.error(f"Error in confirm_junior_manager_assignment: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_back_to_inbox")
    async def back_to_inbox(callback: CallbackQuery, state: FSMContext):
        """Go back to inbox using mock data"""
        try:
            await callback.answer()
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                return
            
            # Get region from state
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Get mock applications
            applications = await get_manager_applications(
                region_code=region,
                manager_id=user.get('id'),
                status_filter='created'
            )
            
            # Filter by role_current
            requests = [r for r in applications if r.get('role_current') == 'manager']
            
            if not requests:
                text = "📭 Inbox bo'sh"
                await callback.message.edit_text(text)
                return
            
            # Update state
            await state.update_data(
                inbox_requests=requests,
                current_index=0
            )
            
            # Show first request
            if requests:
                request = requests[0]
                text = (
                    f"📝 <b>Ariza #{request['id']}</b>\n\n"
                    f"📋 Sarlavha: {request.get('title', 'N/A')}\n"
                    f"📄 Tavsif: {request.get('description', 'N/A')}\n"
                    f"👤 Mijoz: {request.get('client_name', 'N/A')}\n"
                    f"📞 Telefon: {request.get('client_phone', 'N/A')}\n"
                    f"🔴 Muhimlik: {request.get('priority', 'N/A')}\n"
                    f"📅 Sana: {request.get('created_at', 'N/A')}"
                )
                
                # Create action buttons
                buttons = [
                    [InlineKeyboardButton(
                        text="👨‍💼 Kichik menjerga yuborish",
                        callback_data=f"mgr_assign_jm_{request['id']}"
                    )],
                    [InlineKeyboardButton(
                        text="✅ Tugatish",
                        callback_data=f"mgr_complete_{request['id']}"
                    )],
                    [InlineKeyboardButton(
                        text="❌ Bekor qilish",
                        callback_data=f"mgr_cancel_{request['id']}"
                    )],
                    [InlineKeyboardButton(
                        text="🔴 Muhimlik",
                        callback_data=f"mgr_priority_{request['id']}_high"
                    )]
                ]
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in back_to_inbox: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("mgr_complete_"))
    async def complete_request(callback: CallbackQuery, state: FSMContext):
        """Complete service request using mock data"""
        try:
            await callback.answer()
            
            # Extract request ID
            request_id = callback.data.replace("mgr_complete_", "")
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Update service request status in mock data
            success = await complete_service_request(
                request_id=request_id,
                completed_by=user['id']
            )
            
            if success:
                # Log the completion
                await audit_logger.log_action(
                    user_id=user['id'],
                    action='complete_request',
                    target_id=request_id,
                    details="Request completed"
                )
                
                text = (
                    f"✅ <b>Ariza tugallandi!</b>\n\n"
                    f"📝 Ariza ID: {request_id}\n"
                    f"👨‍💼 Tugatuvchi: {user.get('full_name', 'N/A')}\n\n"
                    f"Ariza muvaffaqiyatli tugatildi."
                )
                
                await callback.message.edit_text(text, parse_mode='HTML')
                
            else:
                await callback.answer("Arizani tugatishda xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            logger.error(f"Error in complete_request: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("mgr_cancel_"))
    async def cancel_request(callback: CallbackQuery, state: FSMContext):
        """Cancel service request using mock data"""
        try:
            await callback.answer()
            
            # Extract request ID
            request_id = callback.data.replace("mgr_cancel_", "")
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Update service request status in mock data
            success = await cancel_service_request(
                request_id=request_id,
                cancelled_by=user['id']
            )
            
            if success:
                # Log the cancellation
                await audit_logger.log_action(
                    user_id=user['id'],
                    action='cancel_request',
                    target_id=request_id,
                    details="Request cancelled"
                )
                
                text = (
                    f"❌ <b>Ariza bekor qilindi!</b>\n\n"
                    f"📝 Ariza ID: {request_id}\n"
                    f"👨‍💼 Bekor qiluvchi: {user.get('full_name', 'N/A')}\n\n"
                    f"Ariza bekor qilindi."
                )
                
                await callback.message.edit_text(text, parse_mode='HTML')
                
            else:
                await callback.answer("Arizani bekor qilishda xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            logger.error(f"Error in cancel_request: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("mgr_priority_"))
    async def update_priority(callback: CallbackQuery, state: FSMContext):
        """Update request priority using mock data"""
        try:
            await callback.answer()
            
            # Extract data
            parts = callback.data.replace("mgr_priority_", "").split("_")
            request_id = parts[0]
            new_priority = parts[1]
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Update priority in mock data
            success = await update_application_priority(
                request_id=request_id,
                new_priority=new_priority,
                updated_by=user['id']
            )
            
            if success:
                # Log the priority update
                await audit_logger.log_action(
                    user_id=user['id'],
                    action='update_priority',
                    target_id=request_id,
                    details=f"Priority updated to {new_priority}"
                )
                
                priority_names = {
                    'low': 'Past',
                    'normal': 'O\'rtacha',
                    'high': 'Yuqori',
                    'urgent': 'Shoshilinch'
                }
                
                text = (
                    f"📊 <b>Muhimlik yangilandi!</b>\n\n"
                    f"📝 Ariza ID: {request_id}\n"
                    f"🔴 Yangi muhimlik: {priority_names.get(new_priority, new_priority)}\n"
                    f"👨‍💼 Yangilovchi: {user.get('full_name', 'N/A')}\n\n"
                    f"Arizaning muhimligi muvaffaqiyatli yangilandi."
                )
                
                await callback.message.edit_text(text, parse_mode='HTML')
                
            else:
                await callback.answer("Muhimlikni yangilashda xatolik yuz berdi", show_alert=True)
                
        except Exception as e:
            logger.error(f"Error in update_priority: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    return router