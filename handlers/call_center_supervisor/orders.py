"""
Call Center Supervisor Orders Handler
Manages orders for call center supervisors
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.call_center_supervisor_buttons import get_orders_menu, get_order_actions_menu

# States imports
from states.call_center_supervisor_states import CallCenterSupervisorOrdersStates
from filters.role_filter import RoleFilter
from keyboards.call_center_supervisor_buttons import (
    get_supervisor_orders_keyboard
)

def get_call_center_supervisor_orders_router():
    """Get call center supervisor orders router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center_supervisor")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(['📋 Buyurtmalar', '📋 Заказы']))
    async def call_center_supervisor_orders(message: Message, state: FSMContext):
        """Handle call center supervisor orders"""
        lang = 'uz'  # Default language
        
        # Mock orders data
        orders = [
            {
                'id': 1,
                'order_number': 'ORD-001',
                'client_name': 'Ahmad Karimov',
                'service_type': 'Internet xizmati',
                'status': 'Yangi',
                'created_at': '2024-01-15 10:30'
            },
            {
                'id': 2,
                'order_number': 'ORD-002',
                'client_name': 'Malika Yusupova',
                'service_type': 'TV xizmati',
                'status': 'Jarayonda',
                'created_at': '2024-01-15 09:15'
            }
        ]
        
        if not orders:
            text = (
                "📋 Yangi buyurtmalar yo'q." if lang == 'uz'
                else "📋 Новых заказов нет."
            )
            await message.answer(text)
            await state.clear()
        else:
            if lang == 'uz':
                text = f"📋 <b>Buyurtmalar ({len(orders)})</b>\n\n"
                for i, order in enumerate(orders[:10], 1):
                    text += f"{i}. {order.get('order_number', 'N/A')}\n"
                    text += f"   👤 {order.get('client_name', 'N/A')}\n"
                    text += f"   📝 {order.get('service_type', 'N/A')}\n"
                    text += f"   📊 {order.get('status', 'N/A')}\n"
                    text += f"   ⏰ {order.get('created_at', 'N/A')}\n\n"
            else:
                text = f"📋 <b>Заказы ({len(orders)})</b>\n\n"
                for i, order in enumerate(orders[:10], 1):
                    text += f"{i}. {order.get('order_number', 'N/A')}\n"
                    text += f"   👤 {order.get('client_name', 'N/A')}\n"
                    text += f"   📝 {order.get('service_type', 'N/A')}\n"
                    text += f"   📊 {order.get('status', 'N/A')}\n"
                    text += f"   ⏰ {order.get('created_at', 'N/A')}\n\n"
            
            await message.answer(
                text,
                reply_markup=get_orders_menu(lang)
            )
            await state.set_state(CallCenterSupervisorOrdersStates.viewing_orders)

    @router.message(CallCenterSupervisorOrdersStates.viewing_orders, F.text.in_(['📖 Ko\'rish', '📖 Просмотр']))
    async def call_center_supervisor_view_order(message: Message, state: FSMContext):
        """Handle view order"""
        lang = 'uz'  # Default language
        
        text = "📖 Qaysi buyurtmani ko'rmoqchisiz?\nBuyurtma raqamini kiriting:"
        
        await message.answer(text)
        await state.set_state(CallCenterSupervisorOrdersStates.entering_order_number)

    @router.message(CallCenterSupervisorOrdersStates.entering_order_number)
    async def call_center_supervisor_process_order_number(message: Message, state: FSMContext):
        """Process order number"""
        lang = 'uz'  # Default language
        
        # Validate order number
        try:
            order_number = int(message.text)
            if order_number < 1 or order_number > 10:
                raise ValueError("Invalid number")
        except ValueError:
            text = "❌ Noto'g'ri raqam. 1-10 oralig'ida kiriting."
            await message.answer(text)
            await state.clear()
            return
        
        # Mock order details
        order_details = {
            'id': order_number,
            'order_number': f'ORD-{order_number:03d}',
            'client_name': 'Test Client',
            'service_type': 'Internet xizmati',
            'status': 'Yangi',
            'assigned_to': 'Aziz Karimov',
            'created_at': '2024-01-15 10:30',
            'description': f'Bu {order_number} raqamli buyurtma tafsilotlari'
        }
        
        text = (
            f"📋 <b>Buyurtma #{order_number}</b>\n\n"
            f"🔢 <b>Buyurtma raqami:</b> {order_details.get('order_number', 'N/A')}\n"
            f"👤 <b>Mijoz:</b> {order_details.get('client_name', 'N/A')}\n"
            f"📝 <b>Xizmat turi:</b> {order_details.get('service_type', 'N/A')}\n"
            f"📊 <b>Status:</b> {order_details.get('status', 'N/A')}\n"
            f"👨‍💼 <b>Tayinlangan:</b> {order_details.get('assigned_to', 'N/A')}\n"
            f"⏰ <b>Sana:</b> {order_details.get('created_at', 'N/A')}\n\n"
            f"📄 <b>Tavsif:</b>\n{order_details.get('description', 'Tavsif yo\'q')}"
        )
        
        await message.answer(
            text,
            reply_markup=get_order_actions_menu(lang)
        )
        await state.update_data(current_order_id=order_details.get('id'))
        await state.set_state(CallCenterSupervisorOrdersStates.viewing_order_details)

    @router.message(CallCenterSupervisorOrdersStates.viewing_order_details, F.text.in_(['✅ Tasdiqlash', '✅ Подтверждение']))
    async def call_center_supervisor_confirm_order(message: Message, state: FSMContext):
        """Confirm order"""
        lang = 'uz'  # Default language
        
        success_text = "✅ Buyurtma tasdiqlandi!"
        
        await message.answer(success_text)
        await state.clear()

    @router.message(CallCenterSupervisorOrdersStates.viewing_orders, F.text.in_(['⬅️ Orqaga', '⬅️ Назад']))
    async def call_center_supervisor_orders_back(message: Message, state: FSMContext):
        """Handle back to main menu"""
        lang = 'uz'  # Default language
        
        await message.answer("🏠 Bosh sahifaga qaytdingiz")
        await state.clear()

    # Callback handlers for inline buttons
    @router.callback_query(F.data.startswith("order_details_"))
    async def show_order_details(call: CallbackQuery):
        """Show detailed order information"""
        await call.answer()
        
        order_id = int(call.data.split("_")[-1])
        
        text = (
            f"📋 <b>Buyurtma #{order_id}</b>\n\n"
            f"👤 <b>Mijoz:</b> Bekzod Toirov\n"
            f"📱 <b>Telefon:</b> +998 90 123 45 67\n"
            f"📍 <b>Manzil:</b> Toshkent shahri, Chilonzor-5, 23-uy\n"
            f"📝 <b>Tavsif:</b> Internet uzulib qolgan, routerda signal bor lekin chiqmayapti\n"
            f"📅 <b>Sana:</b> 2025-08-05 10:24\n"
            f"📊 <b>Status:</b> Jarayonda\n"
            f"👨‍💼 <b>Mas\'ul:</b> Aziz Karimov\n\n"
            f"Amalni tanlang:"
        )
        
        keyboard = get_supervisor_orders_keyboard(lang)
        
        await call.message.edit_text(text, reply_markup=keyboard)

    @router.callback_query(F.data.startswith("assign_supervisor_"))
    async def assign_supervisor(call: CallbackQuery):
        """Assign supervisor to order"""
        await call.answer()
        
        order_id = int(call.data.split("_")[-1])
        text = "Mas'ulni tanlang:"
        
        supervisors = [
            {"id": 1, "full_name": "Aziz Karimov", "active_orders": 2},
            {"id": 2, "full_name": "Bekzod Toirov", "active_orders": 1},
            {"id": 3, "full_name": "Davron Alimov", "active_orders": 0}
        ]
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=f"👨‍💼 {sup['full_name']} ({sup['active_orders']} buyurtma)",
                callback_data=f"confirm_assign_supervisor_{order_id}_{sup['id']}"
            )] for sup in supervisors
        ])
        await call.message.edit_text(text, reply_markup=keyboard)

    @router.callback_query(F.data.startswith("confirm_assign_supervisor_"))
    async def confirm_assign_supervisor(call: CallbackQuery):
        """Confirm supervisor assignment"""
        await call.answer()
        
        parts = call.data.split("_")
        order_id, supervisor_id = int(parts[3]), int(parts[4])

        text = f"✅ Buyurtma #{order_id} mas'ulga tayinlandi."
        await call.answer("Tayinlandi!")
        await call.message.edit_text(text)

    @router.callback_query(F.data.startswith("change_status_"))
    async def change_order_status(call: CallbackQuery):
        """Change order status"""
        await call.answer()
        
        order_id = int(call.data.split("_")[-1])
        
        text = "Yangi statusni tanlang:"
        statuses = [
            ("new", "🆕 Yangi"),
            ("pending", "⏳ Kutilmoqda"),
            ("assigned", "👨‍💼 Tayinlangan"),
            ("in_progress", "🔄 Jarayonda"),
            ("completed", "✅ Bajarilgan"),
            ("cancelled", "❌ Bekor qilingan")
        ]
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=status_name, callback_data=f"set_status:{status}:{order_id}")]
            for status, status_name in statuses
        ])
        
        await call.message.edit_text(text, reply_markup=keyboard)

    @router.callback_query(F.data.startswith("set_status:"))
    async def set_order_status(call: CallbackQuery):
        """Set order status"""
        await call.answer()
        
        _, new_status, order_id_str = call.data.split(":")
        order_id = int(order_id_str)

        status_names = {
            'new': 'Yangi',
            'pending': 'Kutilmoqda',
            'assigned': 'Tayinlangan',
            'in_progress': 'Jarayonda',
            'completed': 'Bajarilgan',
            'cancelled': 'Bekor qilingan'
        }
        
        text = f"✅ Buyurtma #{order_id} statusi '{status_names.get(new_status, new_status)}' ga o'zgartirildi."
        await call.answer("Status o'zgartirildi!")
        await call.message.edit_text(text)

    @router.callback_query(F.data.startswith("transfer_to_call_center_"))
    async def transfer_to_call_center(call: CallbackQuery):
        """Transfer order to call center"""
        await call.answer()
        
        order_id = int(call.data.split("_")[-1])
        
        text = f"✅ Buyurtma #{order_id} Call Center ga yuborildi."
        await call.answer("Yuborildi!")
        await call.message.edit_text(text)

    @router.callback_query(F.data.in_(["back", "orqaga", "назад"]))
    async def supervisor_back(call: CallbackQuery, state: FSMContext):
        """Go back to supervisor main menu"""
        await call.answer()
        
        text = "Call Center Supervisor paneliga xush kelibsiz!"
        await call.message.edit_text(text)
        await state.clear()

    return router

async def show_call_center_supervisor_orders(message: Message):
    """Show call center supervisor orders"""
    lang = 'uz'  # Default language
    
    # Mock orders data
    orders = [
        {
            'id': 1,
            'order_number': 'ORD-001',
            'client_name': 'Ahmad Karimov',
            'service_type': 'Internet xizmati',
            'status': 'Yangi',
            'assigned_to': 'Aziz Karimov',
            'created_at': '2024-01-15 10:30'
        },
        {
            'id': 2,
            'order_number': 'ORD-002',
            'client_name': 'Malika Yusupova',
            'service_type': 'TV xizmati',
            'status': 'Jarayonda',
            'assigned_to': 'Malika Yusupova',
            'created_at': '2024-01-15 09:15'
        }
    ]
    
    if not orders:
        text = "📋 Yangi buyurtmalar yo'q."
        await message.answer(text)
    else:
        text = f"📋 <b>Buyurtmalar ({len(orders)})</b>\n\n"
        for i, order in enumerate(orders[:10], 1):
            text += f"{i}. {order.get('order_number', 'N/A')}\n"
            text += f"   👤 {order.get('client_name', 'N/A')}\n"
            text += f"   📝 {order.get('service_type', 'N/A')}\n"
            text += f"   📊 {order.get('status', 'N/A')}\n"
            text += f"   👨‍💼 {order.get('assigned_to', 'N/A')}\n"
            text += f"   ⏰ {order.get('created_at', 'N/A')}\n\n"
        
        await message.answer(
            text,
            reply_markup=get_orders_menu(lang)
        )