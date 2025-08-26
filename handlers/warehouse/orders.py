from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.warehouse_buttons import warehouse_orders_menu, order_status_keyboard
from states.warehouse_states import WarehouseOrdersStates, WarehouseMainMenuStates
from filters.role_filter import RoleFilter

def get_warehouse_orders_router():
    """Warehouse orders router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("warehouse")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text == "📋 Buyurtmalar")
    async def orders_management_handler(message: Message, state: FSMContext):
        """Orders management handler"""
        try:
            # Debug logging
            print(f"Warehouse orders handler called by user {message.from_user.id}")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            await state.update_data(lang='uz')
            orders_text = "📋 Buyurtmalar boshqaruvi"
            
            await message.answer(
                orders_text,
                reply_markup=warehouse_orders_menu('uz')
            )
            await state.set_state(WarehouseOrdersStates.orders_menu)
            
            print(f"Warehouse orders handler completed successfully")
            
        except Exception as e:
            print(f"Error in warehouse orders handler: {str(e)}")
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "⏳ Kutilayotgan buyurtmalar")
    async def pending_orders_reply_handler(message: Message, state: FSMContext):
        """Reply tugmasi orqali kutilayotgan buyurtmalarni ko'rsatish"""
        try:
            # Mock pending orders data (like other modules)
            orders = [
                {
                    'id': '1001',
                    'client_name': 'Test Client 1',
                    'description': 'Internet ulanish so\'rovi',
                    'created_at': '2024-01-15 10:30:00',
                    'status': 'pending',
                    'client_phone': '+998901234567'
                },
                {
                    'id': '1002',
                    'client_name': 'Test Client 2',
                    'description': 'Texnik xizmat so\'rovi',
                    'created_at': '2024-01-15 11:15:00',
                    'status': 'pending',
                    'client_phone': '+998901234568'
                }
            ]
            
            if orders:
                text = "⏳ Kutilayotgan buyurtmalar:\n\n"
                for order in orders:
                    text += f"🔹 #{order['id']} - {order.get('client_name', 'Noma\'lum')}\n"
                    text += f"   📝 {order['description'][:50]}{'...' if len(order['description']) > 50 else ''}\n"
                    text += f"   📅 {order['created_at']}\n"
                    text += f"   📊 Status: {order['status']}\n"
                    if order.get('client_phone'):
                        text += f"   📞 {order['client_phone']}\n"
                    text += "\n"
                    if len(text) > 3500:
                        text += "... va boshqalar"
                        break
            else:
                text = "📭 Kutilayotgan buyurtmalar yo'q"
            
            await message.answer(text, reply_markup=warehouse_orders_menu('uz'))
            await state.set_state(WarehouseOrdersStates.orders_menu)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "🔄 Jarayondagi buyurtmalar")
    async def in_progress_orders_reply_handler(message: Message, state: FSMContext):
        """Reply tugmasi orqali jarayondagi buyurtmalarni ko'rsatish"""
        try:
            # Mock in progress orders data (like other modules)
            orders = [
                {
                    'id': '1003',
                    'client_name': 'Test Client 3',
                    'description': 'Uskuna o\'rnatish jarayoni',
                    'technician_name': 'Tech 1',
                    'created_at': '2024-01-15 09:00:00',
                    'status': 'in_progress',
                    'client_phone': '+998901234569'
                },
                {
                    'id': '1004',
                    'client_name': 'Test Client 4',
                    'description': 'Tarmoq sozlash ishlari',
                    'technician_name': 'Tech 2',
                    'created_at': '2024-01-15 08:30:00',
                    'status': 'in_progress',
                    'client_phone': '+998901234570'
                }
            ]
            
            if orders:
                text = "🔄 Jarayondagi buyurtmalar:\n\n"
                for order in orders:
                    text += f"🔹 #{order['id']} - {order.get('client_name', 'Noma\'lum')}\n"
                    text += f"   📝 {order['description'][:50]}{'...' if len(order['description']) > 50 else ''}\n"
                    text += f"   👨‍🔧 Texnik: {order.get('technician_name', 'Tayinlanmagan')}\n"
                    text += f"   📅 {order['created_at']}\n"
                    text += f"   📊 Status: {order['status']}\n"
                    if order.get('client_phone'):
                        text += f"   📞 {order['client_phone']}\n"
                    text += "\n"
                    if len(text) > 3500:
                        text += "... va boshqalar"
                        break
            else:
                text = "📭 Jarayondagi buyurtmalar yo'q"
            
            await message.answer(text, reply_markup=warehouse_orders_menu('uz'))
            await state.set_state(WarehouseOrdersStates.orders_menu)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "✅ Bajarilgan buyurtmalar")
    async def completed_orders_reply_handler(message: Message, state: FSMContext):
        """Reply tugmasi orqali bajarilgan buyurtmalarni ko'rsatish"""
        try:
            # Mock completed orders data (like other modules)
            orders = [
                {
                    'id': '999',
                    'client_name': 'Test Client 5',
                    'description': 'Internet ulanish muvaffaqiyatli bajarildi',
                    'technician_name': 'Tech 3',
                    'created_at': '2024-01-14 14:00:00',
                    'completed_at': '2024-01-15 16:30:00',
                    'client_phone': '+998901234571'
                },
                {
                    'id': '998',
                    'client_name': 'Test Client 6',
                    'description': 'Texnik xizmat tugallandi',
                    'technician_name': 'Tech 4',
                    'created_at': '2024-01-14 10:00:00',
                    'completed_at': '2024-01-15 12:00:00',
                    'client_phone': '+998901234572'
                }
            ]
            
            if orders:
                text = "✅ Bajarilgan buyurtmalar:\n\n"
                for order in orders:
                    text += f"🔹 #{order['id']} - {order.get('client_name', 'Noma\'lum')}\n"
                    text += f"   📝 {order['description'][:50]}{'...' if len(order['description']) > 50 else ''}\n"
                    text += f"   👨‍🔧 Texnik: {order.get('technician_name', 'Noma\'lum')}\n"
                    text += f"   📅 Yaratilgan: {order['created_at']}\n"
                    text += f"   ✅ Tugallangan: {order['completed_at']}\n"
                    if order.get('client_phone'):
                        text += f"   📞 {order['client_phone']}\n"
                    text += "\n"
                    if len(text) > 3500:
                        text += "... va boshqalar"
                        break
            else:
                text = "📭 Bajarilgan buyurtmalar yo'q"
            
            await message.answer(text, reply_markup=warehouse_orders_menu('uz'))
            await state.set_state(WarehouseOrdersStates.orders_menu)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "◀️ Orqaga")
    async def orders_back_reply_handler(message: Message, state: FSMContext):
        """Buyurtmalar menyusidan orqaga qaytish"""
        try:
            from keyboards.warehouse_buttons import get_warehouse_main_keyboard
            await message.answer("Ombor bosh menyusi", reply_markup=get_warehouse_main_keyboard('uz'))
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "pending_orders")
    async def pending_orders_handler(callback: CallbackQuery, state: FSMContext):
        """Show pending orders"""
        try:
            # Mock pending orders data (like other modules)
            orders = [
                {
                    'id': '1001',
                    'client_name': 'Test Client 1',
                    'description': 'Internet ulanish so\'rovi',
                    'created_at': '2024-01-15 10:30:00',
                    'status': 'pending',
                    'client_phone': '+998901234567'
                },
                {
                    'id': '1002',
                    'client_name': 'Test Client 2',
                    'description': 'Texnik xizmat so\'rovi',
                    'created_at': '2024-01-15 11:15:00',
                    'status': 'pending',
                    'client_phone': '+998901234568'
                }
            ]
            
            if orders:
                text = "⏳ Kutilayotgan buyurtmalar:\n\n"
                
                for order in orders:
                    text += f"🔹 **#{order['id']}** - {order.get('client_name', 'Noma\'lum')}\n"
                    text += f"   📝 {order['description'][:50]}{'...' if len(order['description']) > 50 else ''}\n"
                    text += f"   📅 {order['created_at']}\n"
                    text += f"   📊 Status: {order['status']}\n"
                    if order.get('client_phone'):
                        text += f"   📞 {order['client_phone']}\n"
                    text += "\n"
                    
                    # Limit text length
                    if len(text) > 3500:
                        text += "... va boshqalar"
                        break
            else:
                text = "📭 Kutilayotgan buyurtmalar yo'q"
            
            await callback.message.edit_text(text, parse_mode="Markdown")
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Buyurtmalarni olishda xatolik")
            await callback.answer()

    @router.callback_query(F.data == "in_progress_orders")
    async def in_progress_orders_handler(callback: CallbackQuery, state: FSMContext):
        """Show in progress orders"""
        try:
            # Mock in progress orders data (like other modules)
            orders = [
                {
                    'id': '1003',
                    'client_name': 'Test Client 3',
                    'description': 'Uskuna o\'rnatish jarayoni',
                    'technician_name': 'Tech 1',
                    'created_at': '2024-01-15 09:00:00',
                    'status': 'in_progress',
                    'client_phone': '+998901234569'
                },
                {
                    'id': '1004',
                    'client_name': 'Test Client 4',
                    'description': 'Tarmoq sozlash ishlari',
                    'technician_name': 'Tech 2',
                    'created_at': '2024-01-15 08:30:00',
                    'status': 'in_progress',
                    'client_phone': '+998901234570'
                }
            ]
            
            if orders:
                text = "🔄 Jarayondagi buyurtmalar:\n\n"
                
                for order in orders:
                    text += f"🔹 **#{order['id']}** - {order.get('client_name', 'Noma\'lum')}\n"
                    text += f"   📝 {order['description'][:50]}{'...' if len(order['description']) > 50 else ''}\n"
                    text += f"   👨‍🔧 Texnik: {order.get('technician_name', 'Tayinlanmagan')}\n"
                    text += f"   📅 {order['created_at']}\n"
                    text += f"   📊 Status: {order['status']}\n"
                    if order.get('client_phone'):
                        text += f"   📞 {order['client_phone']}\n"
                    text += "\n"
                    
                    # Limit text length
                    if len(text) > 3500:
                        text += "... va boshqalar"
                        break
            else:
                text = "📭 Jarayondagi buyurtmalar yo'q"
            
            await callback.message.edit_text(text, parse_mode="Markdown")
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Buyurtmalarni olishda xatolik")
            await callback.answer()

    @router.callback_query(F.data == "completed_orders")
    async def completed_orders_handler(callback: CallbackQuery, state: FSMContext):
        """Show completed orders"""
        try:
            # Mock completed orders data (like other modules)
            orders = [
                {
                    'id': '999',
                    'client_name': 'Test Client 5',
                    'description': 'Internet ulanish muvaffaqiyatli bajarildi',
                    'technician_name': 'Tech 3',
                    'created_at': '2024-01-14 14:00:00',
                    'completed_at': '2024-01-15 16:30:00',
                    'client_phone': '+998901234571'
                },
                {
                    'id': '998',
                    'client_name': 'Test Client 6',
                    'description': 'Texnik xizmat tugallandi',
                    'technician_name': 'Tech 4',
                    'created_at': '2024-01-14 10:00:00',
                    'completed_at': '2024-01-15 12:00:00',
                    'client_phone': '+998901234572'
                }
            ]
            
            if orders:
                text = "✅ Bajarilgan buyurtmalar:\n\n"
                
                for order in orders:
                    text += f"🔹 **#{order['id']}** - {order.get('client_name', 'Noma\'lum')}\n"
                    text += f"   📝 {order['description'][:50]}{'...' if len(order['description']) > 50 else ''}\n"
                    text += f"   👨‍🔧 Texnik: {order.get('technician_name', 'Noma\'lum')}\n"
                    text += f"   📅 Yaratilgan: {order['created_at']}\n"
                    text += f"   ✅ Tugallangan: {order['completed_at']}\n"
                    if order.get('client_phone'):
                        text += f"   📞 {order['client_phone']}\n"
                    text += "\n"
                    
                    # Limit text length
                    if len(text) > 3500:
                        text += "... va boshqalar"
                        break
            else:
                text = "📭 Bajarilgan buyurtmalar yo'q"
            
            await callback.message.edit_text(text, parse_mode="Markdown")
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Buyurtmalarni olishda xatolik")
            await callback.answer()

    @router.callback_query(F.data.startswith("mark_ready_"))
    async def mark_order_ready_handler(callback: CallbackQuery, state: FSMContext):
        """Mark order as ready for installation"""
        try:
            order_id = int(callback.data.split("_")[-1])
            
            # Mock success response (like other modules)
            success_text = f"✅ #{order_id} buyurtma o'rnatishga tayyor deb belgilandi!"
            await callback.message.edit_text(success_text)
            
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("❌ Buyurtmani belgilashda xatolik")
            await callback.answer()

    @router.callback_query(F.data.startswith("update_order_status_"))
    async def update_order_status_handler(callback: CallbackQuery, state: FSMContext):
        """Update order status"""
        try:
            # Parse callback data: update_order_status_{order_id}_{status}
            parts = callback.data.split("_")
            order_id = int(parts[3])
            new_status = parts[4]
            
            # Mock success response (like other modules)
            status_names = {
                'confirmed': 'Tasdiqlangan',
                'in_progress': 'Jarayonda',
                'completed': 'Bajarilgan',
                'cancelled': 'Bekor qilingan'
            }
            
            status_name = status_names.get(new_status, new_status)
            success_text = f"✅ #{order_id} buyurtma holati '{status_name}' ga o'zgartirildi!"
            await callback.message.edit_text(success_text)
            
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("❌ Holatni o'zgartirishda xatolik")
            await callback.answer()

    @router.callback_query(F.data == "orders_by_status")
    async def orders_by_status_handler(callback: CallbackQuery, state: FSMContext):
        """Show orders filtering by status"""
        try:
            filter_text = "📊 Holatga ko'ra filtrlash:"
            
            await callback.message.edit_text(
                filter_text,
                reply_markup=order_status_keyboard('uz')
            )
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.callback_query(F.data.startswith("filter_orders_"))
    async def filter_orders_handler(callback: CallbackQuery, state: FSMContext):
        """Filter orders by specific status"""
        try:
            status = callback.data.split("_")[-1]
            
            # Mock filtered orders data (like other modules)
            orders = [
                {
                    'id': '1001',
                    'client_name': 'Test Client 1',
                    'description': 'Internet ulanish so\'rovi',
                    'created_at': '2024-01-15 10:30:00',
                    'technician_name': 'Tech 1',
                    'client_phone': '+998901234567'
                }
            ]
            
            status_names = {
                'new': 'Yangi',
                'confirmed': 'Tasdiqlangan',
                'in_progress': 'Jarayonda',
                'completed': 'Bajarilgan',
                'cancelled': 'Bekor qilingan'
            }
            
            status_name = status_names.get(status, status)
            
            if orders:
                text = f"📊 {status_name} buyurtmalar:\n\n"
                
                for order in orders:
                    text += f"🔹 **#{order['id']}** - {order.get('client_name', 'Noma\'lum')}\n"
                    text += f"   📝 {order['description'][:50]}{'...' if len(order['description']) > 50 else ''}\n"
                    text += f"   📅 {order['created_at']}\n"
                    if order.get('technician_name'):
                        text += f"   👨‍🔧 {order['technician_name']}\n"
                    if order.get('client_phone'):
                        text += f"   📞 {order['client_phone']}\n"
                    text += "\n"
                    
                    # Limit text length
                    if len(text) > 3500:
                        text += "... va boshqalar"
                        break
            else:
                text = f"📭 {status_name} buyurtmalar yo'q"
            
            await callback.message.edit_text(text, parse_mode="Markdown")
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Filtrlashda xatolik")
            await callback.answer()

    return router

# Mock functions (like other modules)
async def get_pending_warehouse_orders():
    """Get pending warehouse orders (mock function like other modules)"""
    try:
        return [
            {
                'id': '1001',
                'client_name': 'Test Client 1',
                'description': 'Internet ulanish so\'rovi',
                'created_at': '2024-01-15 10:30:00',
                'status': 'pending',
                'client_phone': '+998901234567'
            },
            {
                'id': '1002',
                'client_name': 'Test Client 2',
                'description': 'Texnik xizmat so\'rovi',
                'created_at': '2024-01-15 11:15:00',
                'status': 'pending',
                'client_phone': '+998901234568'
            }
        ]
    except Exception as e:
        return []

async def get_in_progress_warehouse_orders():
    """Get in progress warehouse orders (mock function like other modules)"""
    try:
        return [
            {
                'id': '1003',
                'client_name': 'Test Client 3',
                'description': 'Uskuna o\'rnatish jarayoni',
                'technician_name': 'Tech 1',
                'created_at': '2024-01-15 09:00:00',
                'status': 'in_progress',
                'client_phone': '+998901234569'
            },
            {
                'id': '1004',
                'client_name': 'Test Client 4',
                'description': 'Tarmoq sozlash ishlari',
                'technician_name': 'Tech 2',
                'created_at': '2024-01-15 08:30:00',
                'status': 'in_progress',
                'client_phone': '+998901234570'
            }
        ]
    except Exception as e:
        return []

async def get_completed_warehouse_orders(limit: int = 10):
    """Get completed warehouse orders (mock function like other modules)"""
    try:
        return [
            {
                'id': '999',
                'client_name': 'Test Client 5',
                'description': 'Internet ulanish muvaffaqiyatli bajarildi',
                'technician_name': 'Tech 3',
                'created_at': '2024-01-14 14:00:00',
                'completed_at': '2024-01-15 16:30:00',
                'client_phone': '+998901234571'
            },
            {
                'id': '998',
                'client_name': 'Test Client 6',
                'description': 'Texnik xizmat tugallandi',
                'technician_name': 'Tech 4',
                'created_at': '2024-01-14 10:00:00',
                'completed_at': '2024-01-15 12:00:00',
                'client_phone': '+998901234572'
            }
        ]
    except Exception as e:
        return []

async def update_order_status_warehouse(order_id: int, new_status: str, user_id: int):
    """Update order status warehouse (mock function like other modules)"""
    try:
        # Mock update (like other modules)
        return True
    except Exception as e:
        return False

async def mark_order_ready_for_installation(order_id: int, user_id: int):
    """Mark order ready for installation (mock function like other modules)"""
    try:
        # Mock mark ready (like other modules)
        return True
    except Exception as e:
        return False

async def get_warehouse_orders_by_status(statuses: list):
    """Get warehouse orders by status (mock function like other modules)"""
    try:
        return [
            {
                'id': '1001',
                'client_name': 'Test Client 1',
                'description': 'Internet ulanish so\'rovi',
                'created_at': '2024-01-15 10:30:00',
                'technician_name': 'Tech 1',
                'client_phone': '+998901234567'
            }
        ]
    except Exception as e:
        return []
