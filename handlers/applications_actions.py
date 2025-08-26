"""
Applications Actions Handler - Mock Data Version

Bu modul manager uchun arizalar bilan bog'liq amallar funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, database kerak emas.
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

# Mock data for junior managers
MOCK_JUNIOR_MANAGERS = [
    {'id': 1, 'full_name': 'Aziz Karimov', 'role': 'junior_manager'},
    {'id': 2, 'full_name': 'Malika Yusupova', 'role': 'junior_manager'},
    {'id': 3, 'full_name': 'Jasur Toshmatov', 'role': 'junior_manager'},
    {'id': 4, 'full_name': 'Dilfuza Rahimova', 'role': 'junior_manager'},
    {'id': 5, 'full_name': 'Rustam Alimov', 'role': 'junior_manager'}
]

# Mock data for service requests
MOCK_SERVICE_REQUESTS = [
    {'id': 'REQ001', 'status': 'new', 'priority': 'normal', 'assigned_to': None},
    {'id': 'REQ002', 'status': 'active', 'priority': 'high', 'assigned_to': None},
    {'id': 'REQ003', 'status': 'completed', 'priority': 'normal', 'assigned_to': 1},
    {'id': 'REQ004', 'status': 'cancelled', 'priority': 'low', 'assigned_to': None},
    {'id': 'REQ005', 'status': 'active', 'priority': 'urgent', 'assigned_to': None}
]

def get_manager_applications_actions_router():
    """Router for applications actions functionality with mock data"""
    router = Router()
    
    @router.callback_query(F.data.startswith("mgr_assign_jm_"))
    async def assign_to_junior_manager(callback: CallbackQuery, state: FSMContext):
        """Assign request to junior manager using mock data"""
        try:
            await callback.answer()
            
            # Extract request ID
            request_id = callback.data.replace("mgr_assign_jm_", "")
            
            # Create selection keyboard
            buttons = []
            for jm in MOCK_JUNIOR_MANAGERS:
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
            
            # Find junior manager
            junior_manager = next((jm for jm in MOCK_JUNIOR_MANAGERS if jm['id'] == junior_manager_id), None)
            
            if junior_manager:
                # Update mock data (in real app this would update database)
                for req in MOCK_SERVICE_REQUESTS:
                    if req['id'] == request_id:
                        req['assigned_to'] = junior_manager_id
                        req['status'] = 'assigned_to_junior_manager'
                        break
                
                text = (
                    f"✅ <b>Tayinlash muvaffaqiyatli!</b>\n\n"
                    f"📝 Ariza ID: {request_id}\n"
                    f"👨‍💼 Kichik menjerga yuborildi: {junior_manager['full_name']}\n\n"
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
                await callback.answer("Kichik menejer topilmadi", show_alert=True)
                
        except Exception as e:
            logger.error(f"Error in confirm_junior_manager_assignment: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_back_to_inbox")
    async def back_to_inbox(callback: CallbackQuery, state: FSMContext):
        """Go back to inbox"""
        try:
            await callback.answer()
            
            # Mock inbox data
            mock_inbox_requests = [
                {'id': 'REQ001', 'status': 'new', 'client_name': 'Aziz Karimov', 'subject': 'Ulanish so\'rovi'},
                {'id': 'REQ002', 'status': 'active', 'client_name': 'Malika Yusupova', 'subject': 'Texnik muammo'},
                {'id': 'REQ003', 'status': 'completed', 'client_name': 'Jasur Toshmatov', 'subject': 'Status so\'rovi'}
            ]
            
            if not mock_inbox_requests:
                text = "📭 Inbox bo'sh"
                await callback.message.edit_text(text)
                return
            
            # Show first request
            await display_mock_request(callback, mock_inbox_requests[0])
            
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
            
            # Update mock data
            for req in MOCK_SERVICE_REQUESTS:
                if req['id'] == request_id:
                    req['status'] = 'completed'
                    break
            
            text = (
                f"✅ <b>Ariza tugallandi!</b>\n\n"
                f"📝 Ariza ID: {request_id}\n"
                f"👨‍💼 Tugatuvchi: Manager\n\n"
                f"Ariza muvaffaqiyatli tugatildi."
            )
            
            await callback.message.edit_text(text, parse_mode='HTML')
                
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
            
            # Update mock data
            for req in MOCK_SERVICE_REQUESTS:
                if req['id'] == request_id:
                    req['status'] = 'cancelled'
                    break
            
            text = (
                f"❌ <b>Ariza bekor qilindi!</b>\n\n"
                f"📝 Ariza ID: {request_id}\n"
                f"👨‍💼 Bekor qiluvchi: Manager\n\n"
                f"Ariza bekor qilindi."
            )
            
            await callback.message.edit_text(text, parse_mode='HTML')
                
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
            
            # Update mock data
            for req in MOCK_SERVICE_REQUESTS:
                if req['id'] == request_id:
                    req['priority'] = new_priority
                    break
            
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
                f"👨‍💼 Yangilovchi: Manager\n\n"
                f"Arizaning muhimligi muvaffaqiyatli yangilandi."
            )
            
            await callback.message.edit_text(text, parse_mode='HTML')
                
        except Exception as e:
            logger.error(f"Error in update_priority: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    return router

async def display_mock_request(callback: CallbackQuery, request: dict):
    """Display mock request details"""
    text = f"""📋 <b>Ariza ma'lumotlari</b>

🆔 ID: {request['id']}
👤 Mijoz: {request['client_name']}
📝 Mavzu: {request['subject']}
📊 Status: {request['status']}

Qanday amal bajarishni xohlaysiz?"""
    
    # Create action keyboard
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tugatish", callback_data=f"mgr_complete_{request['id']}")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"mgr_cancel_{request['id']}")],
        [InlineKeyboardButton(text="⬅️ Ortga", callback_data="mgr_back_to_inbox")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')