"""
Call Center Orders Handler
Manages orders for call center operators
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.call_center_buttons import get_orders_menu, get_order_actions_menu

# States imports
from states.call_center import CallCenterOrdersStates
from filters.role_filter import RoleFilter

def get_call_center_orders_router():
    """Get call center orders router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(['📋 Buyurtmalar', '📋 Заказы']))
    async def call_center_orders(message: Message, state: FSMContext):
        """Handle orders"""
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
            await state.set_state(CallCenterOrdersStates.viewing_orders)

    @router.message(CallCenterOrdersStates.viewing_orders, F.text.in_(['📖 Ko\'rish', '📖 Просмотр']))
    async def call_center_view_order(message: Message, state: FSMContext):
        """Handle view order"""
        lang = 'uz'  # Default language
        
        text = (
            "📖 Qaysi buyurtmani ko'rmoqchisiz?\n"
            "Buyurtma raqamini kiriting:" if lang == 'uz'
            else "📖 Какой заказ хотите посмотреть?\n"
                 "Введите номер заказа:"
        )
        
        await message.answer(text)
        await state.set_state(CallCenterOrdersStates.entering_order_number)

    @router.message(CallCenterOrdersStates.entering_order_number)
    async def call_center_process_order_number(message: Message, state: FSMContext):
        """Process order number"""
        lang = 'uz'  # Default language
        
        # Validate order number
        try:
            order_number = int(message.text)
            if order_number < 1 or order_number > 10:
                raise ValueError("Invalid number")
        except ValueError:
            text = (
                "❌ Noto'g'ri raqam. 1-10 oralig'ida kiriting." if lang == 'uz'
                else "❌ Неверный номер. Введите от 1 до 10."
            )
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
            'created_at': '2024-01-15 10:30',
            'description': f'Bu {order_number} raqamli buyurtma tafsilotlari'
        }
        
        if lang == 'uz':
            text = (
                f"📋 <b>Buyurtma #{order_number}</b>\n\n"
                f"🔢 <b>Buyurtma raqami:</b> {order_details.get('order_number', 'N/A')}\n"
                f"👤 <b>Mijoz:</b> {order_details.get('client_name', 'N/A')}\n"
                f"📝 <b>Xizmat turi:</b> {order_details.get('service_type', 'N/A')}\n"
                f"📊 <b>Status:</b> {order_details.get('status', 'N/A')}\n"
                f"⏰ <b>Sana:</b> {order_details.get('created_at', 'N/A')}\n\n"
                f"📄 <b>Tavsif:</b>\n{order_details.get('description', 'Tavsif yo\'q')}"
            )
        else:
            text = (
                f"📋 <b>Заказ #{order_number}</b>\n\n"
                f"🔢 <b>Номер заказа:</b> {order_details.get('order_number', 'N/A')}\n"
                f"👤 <b>Клиент:</b> {order_details.get('client_name', 'N/A')}\n"
                f"📝 <b>Тип услуги:</b> {order_details.get('service_type', 'N/A')}\n"
                f"📊 <b>Статус:</b> {order_details.get('status', 'N/A')}\n"
                f"⏰ <b>Дата:</b> {order_details.get('created_at', 'N/A')}\n\n"
                f"📄 <b>Описание:</b>\n{order_details.get('description', 'Нет описания')}"
            )
        
        await message.answer(
            text,
            reply_markup=get_order_actions_menu(lang)
        )
        await state.update_data(current_order_id=order_details.get('id'))
        await state.set_state(CallCenterOrdersStates.viewing_order_details)

    @router.message(CallCenterOrdersStates.viewing_order_details, F.text.in_(['✅ Tasdiqlash', '✅ Подтверждение']))
    async def call_center_confirm_order(message: Message, state: FSMContext):
        """Confirm order"""
        lang = 'uz'  # Default language
        
        success_text = (
            "✅ Buyurtma tasdiqlandi!" if lang == 'uz'
            else "✅ Заказ подтвержден!"
        )
        
        await message.answer(success_text)
        await state.clear()

    @router.message(CallCenterOrdersStates.viewing_orders, F.text.in_(['⬅️ Orqaga', '⬅️ Назад']))
    async def call_center_orders_back(message: Message, state: FSMContext):
        """Handle back to main menu"""
        lang = 'uz'  # Default language
        
        await message.answer(
            "🏠 Bosh sahifaga qaytdingiz" if lang == 'uz' else "🏠 Вернулись на главную страницу"
        )
        await state.clear()

    return router

async def show_call_center_orders(message: Message):
    """Show call center orders"""
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