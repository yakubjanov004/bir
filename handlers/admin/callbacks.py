"""
Admin Callbacks Handler
Manages admin callback queries
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Optional, Dict, Any

# States imports
from states.admin_states import AdminCallbackStates, AdminMainMenuStates

# Keyboard imports
from keyboards.admin_buttons import get_admin_main_menu

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int) -> Dict[str, Any]:
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'client',
        'language': 'uz',
        'full_name': 'Test User',
        'phone': '+998901234567',
        'created_at': '2025-08-05 10:24:00'
    }

async def update_user_role(telegram_id: int, new_role: str) -> bool:
    """Mock update user role"""
    return True

async def block_user(telegram_id: int) -> bool:
    """Mock block user"""
    return True

async def unblock_user(telegram_id: int) -> bool:
    """Mock unblock user"""
    return True

async def get_order_by_id(order_id: int) -> Dict[str, Any]:
    """Mock get order by ID"""
    return {
        'id': order_id,
        'type': 'connection',
        'status': 'pending',
        'client_name': 'Test Client',
        'description': 'Test order description',
        'created_at': '2025-08-05 10:24:00'
    }

async def update_order_status(order_id: int, new_status: str) -> bool:
    """Mock update order status"""
    return True

async def assign_order_to_technician(order_id: int, technician_id: int) -> bool:
    """Mock assign order to technician"""
    return True

def get_admin_callbacks_router():
    """Get admin callbacks router"""
    from aiogram import Router
    router = Router()
    
    # Apply role filter
    from filters.role_filter import RoleFilter
    role_filter = RoleFilter("admin")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.callback_query(F.data.startswith("search_by_"))
    async def search_method_selected(call: CallbackQuery, state: FSMContext):
        """Handle search method selection"""
        await call.answer()
        
        search_type = call.data.replace('search_by_', '')
        await state.update_data(search_type=search_type)

        if search_type == "telegram_id":
            text = "Telegram ID ni kiriting:"
            await call.message.edit_text(text)
            await state.set_state(AdminCallbackStates.waiting_for_search_value)
        elif search_type == "phone":
            text = "Telefon raqamini kiriting:"
            await call.message.edit_text(text)
            await state.set_state(AdminCallbackStates.waiting_for_search_value)
        else:
            text = "Noto'g'ri qidiruv turi."
            await call.message.edit_text(text)

    @router.callback_query(F.data.startswith("manage_user_"))
    async def manage_user(call: CallbackQuery):
        """Manage a specific user"""
        await call.answer()
        
        telegram_id = int(call.data.split("_")[-1])
        
        text = (
            f"👤 <b>Foydalanuvchi boshqaruvi</b>\n\n"
            f"📝 <b>Ism:</b> Bekzod Toirov\n"
            f"📱 <b>Telefon:</b> +998 90 123 45 67\n"
            f"🆔 <b>Telegram ID:</b> {telegram_id}\n"
            f"👤 <b>Joriy rol:</b> client\n"
            f"📅 <b>Ro'yxatdan o'tgan:</b> 05.08.2025 10:24\n\n"
            f"Amalni tanlang:"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Rolni o'zgartirish",
                    callback_data=f"change_role_{telegram_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚫 Bloklash",
                    callback_data=f"block_user_{telegram_id}"
                )
            ]
        ])
        await call.message.edit_text(text, reply_markup=keyboard)

    @router.callback_query(F.data.startswith("change_role_"))
    async def change_user_role(call: CallbackQuery):
        """Show roles as inline buttons for role change"""
        await call.answer()
        
        telegram_id = int(call.data.split("_")[-1])
        text = "Yangi rolni tanlang:"
        
        roles = [
            ("client", "👤 Mijoz"),
            ("technician", "👨‍🔧 Texnik"),
            ("manager", "👨‍💼 Menejer"),
            ("junior_manager", "👨‍💼 Kichik Menejer"),
            ("admin", "🏢 Admin"),
            ("call_center", "📞 Call Center"),
            ("call_center_supervisor", "🕴️ Call Center Supervisor"),
            ("controller", "🎯 Kontrolyor"),
            ("warehouse", "📦 Sklad")
        ]
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=role_name, callback_data=f"set_role:{role}:{telegram_id}")]
            for role, role_name in roles
        ])
        await call.message.edit_text(text, reply_markup=keyboard)

    @router.callback_query(F.data.startswith("set_role:"))
    async def confirm_role_change(call: CallbackQuery):
        """Confirm role change"""
        await call.answer()
        
        data = call.data.split(":")
        new_role = data[1]
        telegram_id = int(data[2])
        
        # Mock role update
        success = await update_user_role(telegram_id, new_role)
        
        if success:
            text = f"✅ Rol muvaffaqiyatli o'zgartirildi!\n\nYangi rol: {new_role}"
        else:
            text = "❌ Rolni o'zgartirishda xatolik yuz berdi."
        
        await call.message.edit_text(text)

    @router.callback_query(F.data.startswith("block_user_"))
    async def block_user(call: CallbackQuery):
        """Block a user"""
        await _toggle_user_block(call, "block")

    @router.callback_query(F.data.startswith("unblock_user_"))
    async def unblock_user(call: CallbackQuery):
        """Unblock a user"""
        await _toggle_user_block(call, "unblock")

    async def _toggle_user_block(call: CallbackQuery, action: str):
        """Toggle user block status"""
        await call.answer()
        
        telegram_id = int(call.data.split("_")[-1])
        
        if action == "block":
            success = await block_user(telegram_id)
            action_text = "bloklandi"
        else:
            success = await unblock_user(telegram_id)
            action_text = "blokdan chiqarildi"
        
        if success:
            text = f"✅ Foydalanuvchi {action_text}!"
        else:
            text = f"❌ Foydalanuvchini {action_text}da xatolik yuz berdi."
        
        await call.message.edit_text(text)

    @router.callback_query(F.data.startswith("assign_order_"))
    async def assign_order(call: CallbackQuery):
        """Assign order to technician"""
        await call.answer()
        
        order_id = int(call.data.split("_")[-1])
        
        text = (
            f"📋 <b>Buyurtma tayinlash</b>\n\n"
            f"🆔 <b>Buyurtma ID:</b> {order_id}\n"
            f"👤 <b>Mijoz:</b> Test Client\n"
            f"📝 <b>Tavsif:</b> Test order description\n"
            f"📅 <b>Sana:</b> 05.08.2025\n\n"
            f"Texnikni tanlang:"
        )
        
        # Mock technicians list
        technicians = [
            {"id": 1, "name": "Ahmad Texnik"},
            {"id": 2, "name": "Bekzod Texnik"},
            {"id": 3, "name": "Chetan Texnik"}
        ]
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=tech["name"], callback_data=f"confirm_assign_{order_id}_{tech['id']}")]
            for tech in technicians
        ])
        
        await call.message.edit_text(text, reply_markup=keyboard)

    @router.callback_query(F.data.startswith("confirm_assign_"))
    async def confirm_assign_order(call: CallbackQuery):
        """Confirm order assignment"""
        await call.answer()
        
        data = call.data.split("_")
        order_id = int(data[2])
        technician_id = int(data[3])
        
        # Mock assignment
        success = await assign_order_to_technician(order_id, technician_id)
        
        if success:
            text = f"✅ Buyurtma #{order_id} texnikka muvaffaqiyatli tayinlandi!"
        else:
            text = f"❌ Buyurtmani tayinlashda xatolik yuz berdi."
        
        await call.message.edit_text(text)

    @router.callback_query(F.data.startswith("order_details_"))
    async def show_order_details(call: CallbackQuery):
        """Show order details"""
        await call.answer()
        
        order_id = int(call.data.split("_")[-1])
        
        # Mock order data
        order = await get_order_by_id(order_id)
        
        text = (
            f"📋 <b>Buyurtma ma'lumotlari</b>\n\n"
            f"🆔 <b>ID:</b> {order['id']}\n"
            f"👤 <b>Mijoz:</b> {order['client_name']}\n"
            f"📝 <b>Tur:</b> {order['type']}\n"
            f"📊 <b>Holat:</b> {order['status']}\n"
            f"📄 <b>Tavsif:</b> {order['description']}\n"
            f"📅 <b>Sana:</b> {order['created_at']}\n\n"
            f"Amalni tanlang:"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👨‍🔧 Texnikka tayinlash",
                    callback_data=f"assign_order_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Holatni o'zgartirish",
                    callback_data=f"change_status_{order_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Yopish",
                    callback_data="back"
                )
            ]
        ])
        
        await call.message.edit_text(text, reply_markup=keyboard)

    @router.callback_query(F.data.startswith("change_status_"))
    async def change_order_status(call: CallbackQuery):
        """Change order status"""
        await call.answer()
        
        order_id = int(call.data.split("_")[-1])
        
        text = "Yangi holatni tanlang:"
        
        statuses = [
            ("pending", "⏳ Kutilmoqda"),
            ("in_progress", "🔄 Jarayonda"),
            ("completed", "✅ Bajarildi"),
            ("cancelled", "❌ Bekor qilindi")
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
        
        data = call.data.split(":")
        new_status = data[1]
        order_id = int(data[2])
        
        # Mock status update
        success = await update_order_status(order_id, new_status)
        
        if success:
            text = f"✅ Buyurtma holati muvaffaqiyatli o'zgartirildi!\n\nYangi holat: {new_status}"
        else:
            text = "❌ Holatni o'zgartirishda xatolik yuz berdi."
        
        await call.message.edit_text(text)

    @router.callback_query(F.data.in_(["back", "orqaga", "назад"]))
    async def admin_back(call: CallbackQuery, state: FSMContext):
        """Go back to admin main menu"""
        await call.answer()
        
        text = "🏢 <b>Admin panel</b>\n\nKerakli bo'limni tanlang:"
        
        await call.message.edit_text(text, reply_markup=get_admin_main_menu())
        await state.set_state(AdminMainMenuStates.main_menu)

    return router
