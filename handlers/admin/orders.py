"""
Admin Orders Handler
Manages admin order management
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from functools import wraps
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.admin_buttons import (
    get_zayavka_main_keyboard,
    get_zayavka_status_filter_keyboard,
    get_zayavka_filter_menu_keyboard,
    get_zayavka_section_keyboard
)

# States imports
from states.admin_states import AdminOrderStates, AdminMainMenuStates
from filters.role_filter import RoleFilter

def format_order(order: dict, lang: str) -> str:
    """Format order details in both Uzbek and Russian"""
    return (
        f"🆔 #{order['id']}\n"
        f"👤 {order.get('client_name', 'N/A')}\n"
        f"📱 {order.get('client_phone', 'N/A')}\n"
        f"📍 {order.get('address', 'N/A')}\n"
        f"📝 {order.get('title', 'N/A')}\n"
        f"📅 {order['created_at'].strftime('%d.%m.%Y %H:%M')}\n\n"
        f"Holat: {order.get('status', 'N/A')}\n\n"
        f"Texnik: {order.get('technician_name', 'N/A')}\n\n"
        f"Qo'shimcha ma'lumotlar: {order.get('description', 'N/A')}")

def get_admin_orders_router():
    """Get admin orders router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("admin")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.message(StateFilter(AdminMainMenuStates.main_menu), F.text.in_(["📝 Zayavkalar", "📝 Заявки"]))
    async def orders_menu(message: Message, state: FSMContext):
        """Show orders menu"""
        text = (
            f"📊 <b>Zayavkalar statistikasi</b>\n\n"
            f"Yangi: 15\n"
            f"Jarayonda: 8\n"
            f"Bajarilgan: 32\n"
            f"Bekor qilingan: 3\n\n"
            f"Zayavkalar bo'yicha qidirish va filtrlash uchun quyidagi tugmalardan foydalaning:"
        )
        
        sent_message = await message.answer(
            text,
            reply_markup=get_zayavka_main_keyboard('uz')
        )
        
        # Save message ID for cleanup
        await state.update_data(last_message_id=sent_message.message_id)

    @router.message(F.text.in_(['📂 Holat bo\'yicha', '📂 По статусу']))
    async def handle_status_menu(message: Message, state: FSMContext):
        """Handle status menu"""
        text = (
            f"📂 <b>Holat bo'yicha qidirish</b>\n\n"
            f"Holatni tanlang:"
        )
        
        # Switch to section keyboard
        sent_message = await message.answer(
            text,
            reply_markup=get_zayavka_section_keyboard('uz')
        )
        await state.update_data(last_message_id=sent_message.message_id)
        
        # Show inline keyboard with pagination
        await message.answer(
            text,
            reply_markup=get_zayavka_status_filter_keyboard('uz', page=1, total_pages=1)
        )

    @router.message(F.text == "🔍 Qidirish / Filtrlash")
    async def handle_filter_menu(message: Message, state: FSMContext):
        """Handle filter menu selection"""
        text = (
            f"🔍 <b>Qidirish / Filtrlash</b>\n\n"
            f"Qidirish turini tanlang:"
        )
        
        # Switch to section keyboard
        sent_message = await message.answer(
            text,
            reply_markup=get_zayavka_section_keyboard('uz')
        )
        await state.update_data(last_message_id=sent_message.message_id)
        
        # Show inline keyboard with pagination
        await message.answer(
            text,
            reply_markup=get_zayavka_filter_menu_keyboard('uz', page=1, total_pages=2, admin=True)
        )

    @router.callback_query(F.data.startswith("zayavka:status:"))
    async def handle_status_selection(callback: CallbackQuery, state: FSMContext):
        """Handle status selection from inline keyboard"""
        data = callback.data.split(':')[2:]
        action = data[0]
        
        if action in ["prev", "next"]:
            current_page = int(data[1])
            new_page = current_page - 1 if action == "prev" else current_page + 1
            
            # Mock orders data
            orders = [
                {
                    'id': 12345,
                    'client_name': 'Bekzod Toirov',
                    'client_phone': '+998 90 123 45 67',
                    'address': 'Toshkent shahri, Chilonzor-5, 23-uy',
                    'title': 'Internet uzulib qolgan',
                    'created_at': datetime.now(),
                    'status': 'Jarayonda',
                    'technician_name': 'Aziz Karimov',
                    'description': 'Routerda signal bor lekin chiqmayapti'
                }
            ]
            
            # Show first 10 orders
            text = "Zayavkalar:\n\n"
            for order in orders[:10]:
                text += format_order(order, 'uz')
                text += "\n\n"
            
            await callback.message.edit_reply_markup(
                reply_markup=get_zayavka_status_filter_keyboard('uz', page=new_page, total_pages=1)
            )
            await callback.answer()
            return

        # Get orders for the selected status
        status = data[1]
        
        # Mock orders data
        orders = [
            {
                'id': 12345,
                'client_name': 'Bekzod Toirov',
                'client_phone': '+998 90 123 45 67',
                'address': 'Toshkent shahri, Chilonzor-5, 23-uy',
                'title': 'Internet uzulib qolgan',
                'created_at': datetime.now(),
                'status': status,
                'technician_name': 'Aziz Karimov',
                'description': 'Routerda signal bor lekin chiqmayapti'
            }
        ]
        
        if not orders:
            text = "Zayavkalar topilmadi."
            await callback.message.edit_text(text)
            return
            
        # Show first 10 orders
        text = "Zayavkalar:\n\n"
        for order in orders[:10]:
            text += format_order(order, 'uz')
            text += "\n\n"
            
        await state.update_data(selected_status=status)
        await callback.message.edit_reply_markup(
            reply_markup=get_zayavka_status_filter_keyboard('uz', page=1, total_pages=1)
        )
        await callback.answer()

    @router.callback_query(F.data.startswith("zayavka:filter:"))
    async def handle_filter_selection(callback: CallbackQuery, state: FSMContext):
        """Handle filter selection from inline keyboard"""
        data = callback.data.split(':')[2:]
        action = data[0]
        
        if action in ["prev", "next"]:
            current_page = int(data[1])
            new_page = current_page - 1 if action == "prev" else current_page + 1
            
            # Get current filter type from state
            state_data = await state.get_data()
            active_filter = state_data.get('filter_type')
            
            await callback.message.edit_reply_markup(
                reply_markup=get_zayavka_filter_menu_keyboard('uz', page=new_page, active_filter=active_filter, admin=True)
            )
            await callback.answer()
            return

        filter_map = {
            'username': "🔤 FIO / Username",
            'id': "🔢 Zayavka ID",
            'date': "📆 Sana oraliq",
            'category': "🏷 Kategoriya",
            'technician': "👨‍🔧 Texnik"
        }
    
        filter_type = filter_map.get(action)
        if not filter_type:
            raise ValueError("Invalid filter type")
            
        text = f"🔡 <b>{filter_type} bo'yicha qidirish</b>\n\n"
        text += "Kerakli ma'lumotni kiriting:"
    
        # Set state based on filter type
        if action in ["date", "category"]:
            await state.set_state(AdminOrderStates.filtering_selected)
        else:
            await state.set_state(AdminOrderStates.filtering)
    
        await callback.message.edit_text(text)
        
        # Send new message with filter keyboard (replace with edit_text for inline UX)
        await callback.message.edit_text(
            "Qidirish turini tanlang:",
            reply_markup=get_zayavka_filter_menu_keyboard('uz', active_filter=action if action in ["date", "category"] else None, admin=True)
        )
        await state.update_data(filter_type=action)
        await callback.answer()

    @router.callback_query(F.data.startswith("bulk_assign_"))
    async def bulk_assign_orders(call: CallbackQuery, state: FSMContext):
        """Bulk assign orders to technician"""
        order_type = call.data.split("_")[2]
        
        # Mock technicians data
        technicians = [
            {"id": 1, "full_name": "Aziz Karimov", "active_tasks": 2},
            {"id": 2, "full_name": "Bekzod Toirov", "active_tasks": 1},
            {"id": 3, "full_name": "Davron Alimov", "active_tasks": 0}
        ]
        
        text = "Texnikni tanlang:"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        for tech in technicians[:10]:  # Show first 10
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text=f"👨‍🔧 {tech['full_name']} ({tech['active_tasks']} vazifa)",
                    callback_data=f"bulk_confirm_{order_type}_{tech['id']}"
                )
            ])
        
        await call.message.edit_text(text, reply_markup=keyboard)

    @router.callback_query(F.data.startswith("order_details_"))
    async def show_order_details(call: CallbackQuery, state: FSMContext):
        """Show order details"""
        order_id = int(call.data.split("_")[-1])
        
        # Mock order data
        order = {
            'id': order_id,
            'client_name': 'Bekzod Toirov',
            'client_phone': '+998 90 123 45 67',
            'address': 'Toshkent shahri, Chilonzor-5, 23-uy',
            'title': 'Internet uzulib qolgan',
            'created_at': datetime.now(),
            'status': 'Jarayonda',
            'technician_name': 'Aziz Karimov',
            'description': 'Routerda signal bor lekin chiqmayapti'
        }

        text = (
            "Zayavka ma'lumotlari:\n\n"
            f"🆔 #{order['id']}\n"
            f"👤 {order.get('client_name', 'N/A')}\n"
            f"📱 {order.get('client_phone', 'N/A')}\n"
            f"📍 {order.get('address', 'N/A')}\n"
            f"📝 {order.get('title', 'N/A')}\n"
            f"📅 {order['created_at'].strftime('%d.%m.%Y %H:%M')}\n\n"
            f"Holat: {order.get('status', 'N/A')}\n\n"
            f"Texnik: {order.get('technician_name', 'N/A')}\n\n"
            f"Qo'shimcha ma'lumotlar: {order.get('description', 'N/A')}")
    
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Batafsil",
                    callback_data=f"order_details_{order['id']}"
                )
            ]
        ])
    
        await call.message.edit_text(text, reply_markup=keyboard)

    @router.callback_query(F.data.startswith("change_status_"))
    async def change_order_status(call: CallbackQuery):
        """Change order status"""
        order_id = int(call.data.split("_")[-1])
        
        text = "Yangi statusni tanlang:"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⏳ Kutilmoqda",
                    callback_data=f"set_status_{order_id}_pending"
                ),
                InlineKeyboardButton(
                    text="🔄 Jarayonda",
                    callback_data=f"set_status_{order_id}_in_progress"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Bajarilgan",
                    callback_data=f"set_status_{order_id}_completed"
                ),
                InlineKeyboardButton(
                    text="❌ Bekor qilingan",
                    callback_data=f"set_status_{order_id}_cancelled"
                )
            ]
        ])
        
        await call.message.edit_text(text, reply_markup=keyboard)

    @router.callback_query(F.data.startswith("set_status_"))
    async def set_order_status(call: CallbackQuery):
        """Set order status"""
        parts = call.data.split("_")
        order_id = int(parts[2])
        new_status = parts[3]
        
        status_names = {
            'pending': 'Kutilmoqda',
            'in_progress': 'Jarayonda',
            'completed': 'Bajarilgan',
            'cancelled': 'Bekor qilingan'
        }
        
        status_text = status_names.get(new_status, new_status)
        
        text = f"✅ Zayavka #{order_id} statusi '{status_text}' ga o'zgartirildi."
        await call.answer("Status o'zgartirildi!")
        
        await call.message.delete()

    @router.callback_query(F.data.startswith("bulk_confirm_"))
    async def confirm_bulk_assign(call: CallbackQuery, state: FSMContext):
        """Confirm bulk assign"""
        parts = call.data.split("_")
        order_type = parts[2]
        technician_id = int(parts[3])

        # Mock order IDs from state
        order_ids = [12345, 12346, 12347]

        if not order_ids:
            await call.answer("Buyurtmalar topilmadi.", show_alert=True)
            return

        text = "Buyurtmalar texnikka biriktirildi."
        await call.message.edit_text(text)
        await call.answer()

    @router.message(F.text.in_(["🔍 Zayavka qidirish", "🔍 Поиск заявки"]))
    async def search_orders_menu(message: Message, state: FSMContext):
        """Search orders menu"""
        text = "Zayavka ID sini kiriting:"
        
        await message.answer(text)
        await state.set_state(AdminOrderStates.waiting_for_order_id)

    @router.message(AdminOrderStates.waiting_for_order_id)
    async def process_order_search(message: Message, state: FSMContext):
        """Process order search"""
        try:
            order_id = int(message.text.strip())
        except ValueError:
            text = "Noto'g'ri format. Raqam kiriting."
            await message.answer(text)
            return
        
        # Mock order data
        order = {
            'id': order_id,
            'user_name': 'Bekzod Toirov',
            'client_phone': '+998 90 123 45 67',
            'address': 'Toshkent shahri, Chilonzor-5, 23-uy',
            'description': 'Internet uzulib qolgan, routerda signal bor lekin chiqmayapti',
            'status': 'Jarayonda',
            'created_at': datetime.now()
        }
        
        text = (
            f"🔍 <b>Qidiruv natijasi</b>\n\n"
            f"📋 <b>Zayavka #{order['id']}</b>\n\n"
            f"👤 <b>Mijoz:</b> {order.get('user_name', 'N/A')}\n"
            f"📱 <b>Telefon:</b> {order.get('client_phone', 'N/A')}\n"
            f"📍 <b>Manzil:</b> {order.get('address', 'N/A')}\n"
            f"📝 <b>Tavsif:</b> {order.get('description', 'N/A')}\n"
            f"📊 <b>Status:</b> {order['status']}\n"
            f"📅 <b>Yaratilgan:</b> {order['created_at'].strftime('%d.%m.%Y %H:%M')}\n"
        )
        
        # Add management buttons
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Batafsil",
                    callback_data=f"order_details_{order_id}"
                )
            ]
        ])
        
        # Add back button
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text="◀️ Orqaga",
                callback_data="back_to_orders"
            )
        ])
        
        await message.answer(text, reply_markup=keyboard)
        await state.clear()

    return router
