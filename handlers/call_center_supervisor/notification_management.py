"""
Call Center Supervisor Notification Management Handler

This module handles notification management functionality for call center supervisors,
including sending messages, announcements, and managing notifications.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from datetime import datetime

# Keyboard imports
from keyboards.call_center_supervisor_buttons import (
    get_notification_management_keyboard, get_communication_menu,
    get_supervisor_notification_keyboard
)

# States imports
from states.call_center_supervisor_states import CallCenterSupervisorStates
from filters.role_filter import RoleFilter

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'call_center_supervisor',
        'language': 'uz',
        'full_name': 'Test Supervisor'
    }

async def get_user_lang(user_id: int) -> str:
    """Mock user language"""
    return 'uz'

# Removed duplicate get_role_router - using centralized version from utils.role_system

async def get_supervisor_notifications(supervisor_id: int):
    """Mock supervisor notifications"""
    return [
        {
            'id': 1,
            'type': 'order_escalated',
            'order_id': '12345678',
            'client_name': 'Test Client',
            'created_at': datetime.now()
        },
        {
            'id': 2,
            'type': 'staff_performance_warning',
            'order_id': '87654321',
            'client_name': 'Another Client',
            'created_at': datetime.now()
        }
    ]

async def get_call_center_staff_list(supervisor_id: int):
    """Mock call center staff list"""
    return [
        {
            'id': 1,
            'full_name': 'Operator 1',
            'role': 'call_center_operator'
        },
        {
            'id': 2,
            'full_name': 'Operator 2',
            'role': 'call_center_operator'
        }
    ]

def get_call_center_supervisor_notification_management_router():
    """Get router for call center supervisor notification management handlers"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center_supervisor")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📢 E'lon yuborish"]))
    async def handle_send_announcement(message: Message, state: FSMContext):
        """Handle sending announcements"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return
            
            text = (
                "📢 E'lon yuborish\n\n"
                "Jamoa uchun e'lon matnini yozing:"
            )
            
            await message.answer(text)
            await state.set_state(CallCenterSupervisorStates.main_menu)
            await state.update_data(action="send_announcement")
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text.in_(["💬 Jamoa xabari"]))
    async def handle_team_message(message: Message, state: FSMContext):
        """Handle sending team messages"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return
            
            text = (
                "💬 Jamoa xabari\n\n"
                "Jamoa a'zolariga yubormoqchi bo'lgan xabaringizni yozing:"
            )
            
            await message.answer(text)
            await state.set_state(CallCenterSupervisorStates.main_menu)
            await state.update_data(action="send_team_message")
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text.in_(["👤 Shaxsiy xabar"]))
    async def handle_individual_message(message: Message, state: FSMContext):
        """Handle sending individual messages"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return
            
            staff_list = await get_call_center_staff_list(user['id'])
            
            if not staff_list:
                text = "Xodimlar topilmadi."
                await message.answer(text)
                return
            
            text = (
                "👤 Shaxsiy xabar yuborish\n\n"
                "Xabar yubormoqchi bo'lgan xodimni tanlang:"
            )
            
            keyboard = get_supervisor_notification_keyboard(lang)
            
            await message.answer(text, reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text.in_(["🚨 Shoshilinch ogohlantirish"]))
    async def handle_urgent_alert(message: Message, state: FSMContext):
        """Handle sending urgent alerts"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return
            
            text = (
                "🚨 Shoshilinch ogohlantirish\n\n"
                "⚠️ Bu xabar barcha xodimlarga shoshilinch ravishda yuboriladi.\n\n"
                "Ogohlantirish matnini yozing:"
            )
            
            await message.answer(text)
            await state.set_state(CallCenterSupervisorStates.main_menu)
            await state.update_data(action="send_urgent_alert")
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("ccs_notification_"))
    async def handle_notification_callbacks(callback: CallbackQuery, state: FSMContext):
        """Handle notification management callbacks"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            data = callback.data
            
            if data == "ccs_new_notifications":
                await _show_new_notifications(callback, user['id'])
            elif data == "ccs_send_staff_message":
                await _show_staff_selection_for_message(callback, user['id'])
            elif data == "ccs_broadcast_message":
                await _show_broadcast_message_form(callback)
            elif data == "ccs_send_warning":
                await _show_warning_message_form(callback)
            elif data == "ccs_notifications_history":
                await _show_notifications_history(callback, user['id'])
            else:
                await callback.answer("Noma'lum buyruq", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ccs_select_staff_msg_"))
    async def handle_staff_selection_for_message(callback: CallbackQuery, state: FSMContext):
        """Handle staff selection for individual message"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            staff_id = int(callback.data.split("_")[-1])
            
            # Get staff info
            staff_list = await get_call_center_staff_list(user['id'])
            selected_staff = next((s for s in staff_list if s['id'] == staff_id), None)
            
            if not selected_staff:
                await callback.answer("Xodim topilmadi", show_alert=True)
                return
            
            text = (
                f"👤 {selected_staff['full_name']} ga xabar yuborish\n\n"
                f"Xabar matnini yozing:"
            )
            
            await callback.message.edit_text(text)
            await state.set_state(CallCenterSupervisorStates.main_menu)
            await state.update_data(action="send_individual_message", target_staff_id=staff_id)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router


# Helper functions for notification management
async def _show_new_notifications(callback: CallbackQuery, supervisor_id: int):
    """Show new notifications"""
    try:
        notifications = await get_supervisor_notifications(supervisor_id)
        
        if not notifications:
            text = "Yangi bildirishnomalar yo'q."
            await callback.message.edit_text(text, reply_markup=get_notification_management_keyboard('uz'))
            return
        
        text = f"🔔 Yangi bildirishnomalar ({len(notifications)}):\n\n"
        
        for notification in notifications[:5]:
            type_emoji = "⬆️" if notification['type'] == 'order_escalated' else "⏰"
            text += (
                f"{type_emoji} {notification['type'].replace('_', ' ').title()}\n"
                f"   📋 #{notification['order_id']}\n"
                f"   👤 {notification.get('client_name', 'N/A')}\n"
                f"   📅 {notification['created_at'].strftime('%d.%m %H:%M')}\n\n"
            )
        
        await callback.message.edit_text(text, reply_markup=get_notification_management_keyboard('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_staff_selection_for_message(callback: CallbackQuery, supervisor_id: int):
    """Show staff selection for messaging"""
    try:
        staff_list = await get_call_center_staff_list(supervisor_id)
        
        if not staff_list:
            text = "Xodimlar topilmadi."
            await callback.message.edit_text(text)
            return
        
        text = (
            "👥 Xodim tanlash\n\n"
            "Xabar yubormoqchi bo'lgan xodimni tanlang:"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"👤 {staff['full_name']} ({staff['role']})",
                    callback_data=f"ccs_select_staff_msg_{staff['id']}"
                )
            ] for staff in staff_list[:8]
        ] + [
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="ccs_cancel_staff_selection"
                )
            ]
        ])
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_broadcast_message_form(callback: CallbackQuery):
    """Show broadcast message form"""
    try:
        text = (
            "📢 Ommaviy xabar yuborish\n\n"
            "⚠️ Bu xabar barcha nazorat ostidagi xodimlarga yuboriladi.\n\n"
            "Xabar matnini yozing:"
        )
        
        await callback.message.edit_text(text)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_warning_message_form(callback: CallbackQuery):
    """Show warning message form"""
    try:
        text = (
            "⚠️ Ogohlantirish yuborish\n\n"
            "🚨 Bu shoshilinch ogohlantirish xabari.\n\n"
            "Ogohlantirish matnini yozing:"
        )
        
        await callback.message.edit_text(text)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _show_notifications_history(callback: CallbackQuery, supervisor_id: int):
    """Show notifications history"""
    try:
        # This would typically fetch from a notifications history table
        # For now, we'll show a placeholder
        text = (
            "📋 Bildirishnomalar tarixi\n\n"
            "Oxirgi bildirishnomalar:\n\n"
            "📅 Bugun:\n"
            "• 09:30 - Yangi buyurtma eskalatsiyasi\n"
            "• 11:15 - Xodim samaradorlik ogohlantirishsi\n"
            "• 14:20 - Tizim yangilanish xabari\n\n"
            "📅 Kecha:\n"
            "• 16:45 - Haftalik hisobot tayyor\n"
            "• 18:00 - Ish kuni yakunlandi\n\n"
            "Batafsil tarix uchun hisobot so'rang."
        )
        
        await callback.message.edit_text(text, reply_markup=get_notification_management_keyboard('uz'))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)