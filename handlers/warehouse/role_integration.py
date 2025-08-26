from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from filters.role_filter import RoleFilter

def get_warehouse_role_integration_router():
    """Router for warehouse integration with other roles"""
    router = Router()
    
    # Apply role filter - this is for all roles, so we don't apply a specific role filter
    # The role checking is done within the handlers themselves

    @router.message(F.text == "📦 Ombor bilan ishlash")
    async def warehouse_integration_menu(message: Message, state: FSMContext):
        """Warehouse integration menu for other roles"""
        try:
            # Mock user data (like other modules)
            user = {
                'role': 'manager',
                'language': 'uz'
            }
            
            role = user.get('role')
            
            # Check if user has warehouse access
            allowed_roles = ['manager', 'junior_manager', 'controller', 'call_center', 'technician']
            if role not in allowed_roles:
                text = "Sizda ombor bilan ishlash huquqi yo'q"
                await message.answer(text)
                return
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[])
            
            # Different options based on role
            if role == 'manager':
                keyboard.inline_keyboard.extend([
                    [InlineKeyboardButton(
                        text="📋 Inventar ko'rish",
                        callback_data="view_warehouse_inventory"
                    )],
                    [InlineKeyboardButton(
                        text="📊 Ombor hisoboti",
                        callback_data="warehouse_report"
                    )],
                    [InlineKeyboardButton(
                        text="➕ Mahsulot qo'shish",
                        callback_data="add_material_manager"
                    )]
                ])
            
            elif role == 'junior_manager':
                keyboard.inline_keyboard.extend([
                    [InlineKeyboardButton(
                        text="📋 Inventar ko'rish",
                        callback_data="view_warehouse_inventory"
                    )],
                    [InlineKeyboardButton(
                        text="📊 Ombor holati",
                        callback_data="warehouse_status"
                    )]
                ])
            
            elif role == 'controller':
                keyboard.inline_keyboard.extend([
                    [InlineKeyboardButton(
                        text="📋 Inventar ko'rish",
                        callback_data="view_warehouse_inventory"
                    )],
                    [InlineKeyboardButton(
                        text="🔄 Buyurtma uchun mahsulot",
                        callback_data="materials_for_order"
                    )],
                    [InlineKeyboardButton(
                        text="📊 Ombor hisoboti",
                        callback_data="warehouse_report"
                    )]
                ])
            
            elif role == 'call_center':
                keyboard.inline_keyboard.extend([
                    [InlineKeyboardButton(
                        text="📋 Inventar ko'rish",
                        callback_data="view_warehouse_inventory"
                    )],
                    [InlineKeyboardButton(
                        text="❓ Mahsulot mavjudligi",
                        callback_data="check_material_availability"
                    )]
                ])
            
            elif role == 'technician':
                keyboard.inline_keyboard.extend([
                    [InlineKeyboardButton(
                        text="📋 Kerakli mahsulotlar",
                        callback_data="required_materials"
                    )],
                    [InlineKeyboardButton(
                        text="✅ Ishlatilgan mahsulotlar",
                        callback_data="used_materials"
                    )]
                ])
            
            # Common back button
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text="◀️ Orqaga",
                    callback_data="back_to_main"
                )
            ])
            
            text = f"📦 Ombor bilan ishlash ({role}):"
            await message.answer(text, reply_markup=keyboard)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "view_warehouse_inventory")
    async def view_inventory_for_roles(callback: CallbackQuery, state: FSMContext):
        """View inventory for other roles"""
        try:
            # Mock inventory data (like other modules)
            items = [
                {'name': 'Cable', 'quantity': 50, 'unit': 'dona', 'min_quantity': 10, 'price': 15000},
                {'name': 'Connector', 'quantity': 100, 'unit': 'dona', 'min_quantity': 15, 'price': 5000},
                {'name': 'Router', 'quantity': 10, 'unit': 'dona', 'min_quantity': 5, 'price': 500000},
                {'name': 'Switch', 'quantity': 5, 'unit': 'dona', 'min_quantity': 3, 'price': 300000},
                {'name': 'Cable Tester', 'quantity': 2, 'unit': 'dona', 'min_quantity': 1, 'price': 25000}
            ]
            
            if items:
                text = "📋 Ombor inventari:\n\n"
                
                for item in items[:15]:  # Show first 15 items
                    status_icon = "✅" if item['quantity'] > item.get('min_quantity', 0) else "⚠️"
                    if item['quantity'] == 0:
                        status_icon = "❌"
                    
                    text += f"{status_icon} **{item['name']}**\n"
                    text += f"   📦 Miqdor: {item['quantity']} {item.get('unit', 'dona')}\n"
                    
                    if item.get('min_quantity'):
                        text += f"   ⚠️ Min: {item['min_quantity']}\n"
                    
                    if item.get('price'):
                        text += f"   💰 Narx: {item['price']:,} so'm\n"
                    
                    text += "\n"
                    
                    if len(text) > 3500:
                        text += "... va boshqalar"
                        break
            else:
                text = "📭 Ombor bo'sh"
            
            await callback.message.edit_text(text, parse_mode="Markdown")
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.callback_query(F.data == "warehouse_report")
    async def warehouse_report_for_roles(callback: CallbackQuery, state: FSMContext):
        """Warehouse report for managers and controllers"""
        try:
            # Mock inventory data (like other modules)
            items = [
                {'name': 'Cable', 'quantity': 50, 'unit': 'dona', 'min_quantity': 10, 'price': 15000},
                {'name': 'Connector', 'quantity': 100, 'unit': 'dona', 'min_quantity': 15, 'price': 5000},
                {'name': 'Router', 'quantity': 10, 'unit': 'dona', 'min_quantity': 5, 'price': 500000},
                {'name': 'Switch', 'quantity': 5, 'unit': 'dona', 'min_quantity': 3, 'price': 300000},
                {'name': 'Cable Tester', 'quantity': 2, 'unit': 'dona', 'min_quantity': 1, 'price': 25000}
            ]
            
            if items:
                total_items = len(items)
                total_value = sum(item.get('price', 0) * item['quantity'] for item in items)
                low_stock_items = [item for item in items if item['quantity'] <= item.get('min_quantity', 0)]
                out_of_stock_items = [item for item in items if item['quantity'] == 0]
                
                text = "📊 Ombor hisoboti:\n\n"
                text += f"📦 Jami mahsulotlar: {total_items}\n"
                text += f"💰 Jami qiymat: {total_value:,} so'm\n"
                text += f"⚠️ Kam zaxira: {len(low_stock_items)}\n"
                text += f"❌ Tugagan: {len(out_of_stock_items)}\n\n"
                
                if low_stock_items:
                    text += "⚠️ Kam zaxira mahsulotlari:\n"
                    for item in low_stock_items[:5]:
                        text += f"• {item['name']}: {item['quantity']} (min: {item.get('min_quantity', 0)})\n"
                    if len(low_stock_items) > 5:
                        text += f"... va yana {len(low_stock_items) - 5} ta\n"
                
                if out_of_stock_items:
                    text += "\n❌ Tugagan mahsulotlar:\n"
                    for item in out_of_stock_items[:5]:
                        text += f"• {item['name']}\n"
                    if len(out_of_stock_items) > 5:
                        text += f"... va yana {len(out_of_stock_items) - 5} ta\n"
            else:
                text = "📭 Ombor bo'sh"
            
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.callback_query(F.data == "check_material_availability")
    async def check_material_availability(callback: CallbackQuery, state: FSMContext):
        """Check material availability for call center"""
        try:
            # Mock inventory data (like other modules)
            items = [
                {'name': 'Cable', 'quantity': 50, 'unit': 'dona'},
                {'name': 'Connector', 'quantity': 100, 'unit': 'dona'},
                {'name': 'Router', 'quantity': 10, 'unit': 'dona'},
                {'name': 'Switch', 'quantity': 5, 'unit': 'dona'},
                {'name': 'Cable Tester', 'quantity': 2, 'unit': 'dona'}
            ]
            
            available_items = [item for item in items if item['quantity'] > 0]
            
            if available_items:
                text = "✅ Mavjud mahsulotlar:\n\n"
                
                for item in available_items[:10]:
                    text += f"✅ {item['name']}: {item['quantity']} {item.get('unit', 'dona')}\n"
                
                if len(available_items) > 10:
                    text += f"\n... va yana {len(available_items) - 10} ta mahsulot mavjud"
            else:
                text = "❌ Hozirda mavjud mahsulotlar yo'q"
            
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.callback_query(F.data == "materials_for_order")
    async def materials_for_order(callback: CallbackQuery, state: FSMContext):
        """Show materials needed for orders - for controllers"""
        try:
            # Mock inventory data (like other modules)
            items = [
                {'name': 'Cable', 'quantity': 50, 'unit': 'dona', 'category': 'cables'},
                {'name': 'Connector', 'quantity': 100, 'unit': 'dona', 'category': 'equipment'},
                {'name': 'Router', 'quantity': 10, 'unit': 'dona', 'category': 'equipment'},
                {'name': 'Switch', 'quantity': 5, 'unit': 'dona', 'category': 'equipment'},
                {'name': 'Cable Tester', 'quantity': 2, 'unit': 'dona', 'category': 'tools'}
            ]
            
            common_materials = [
                item for item in items 
                if item.get('category') in ['equipment', 'cables', 'tools', 'general']
            ]
            
            if common_materials:
                text = "🔧 Buyurtmalar uchun mahsulotlar:\n\n"
                
                for item in common_materials[:10]:
                    status = "✅" if item['quantity'] > 5 else "⚠️" if item['quantity'] > 0 else "❌"
                    text += f"{status} {item['name']}: {item['quantity']} {item.get('unit', 'dona')}\n"
                
                text += f"\n💡 Buyurtma uchun kerakli mahsulotlarni oldindan tekshiring"
            else:
                text = "📭 Buyurtmalar uchun mahsulotlar topilmadi"
            
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.callback_query(F.data == "required_materials")
    async def required_materials_for_technician(callback: CallbackQuery, state: FSMContext):
        """Show required materials for technician"""
        try:
            # Mock inventory data (like other modules)
            items = [
                {'name': 'Cable', 'quantity': 50, 'unit': 'dona', 'category': 'cables'},
                {'name': 'Connector', 'quantity': 100, 'unit': 'dona', 'category': 'equipment'},
                {'name': 'Router', 'quantity': 10, 'unit': 'dona', 'category': 'equipment'},
                {'name': 'Switch', 'quantity': 5, 'unit': 'dona', 'category': 'equipment'},
                {'name': 'Cable Tester', 'quantity': 2, 'unit': 'dona', 'category': 'tools'}
            ]
            
            tech_materials = [
                item for item in items 
                if item.get('category') in ['tools', 'equipment', 'cables']
            ]
            
            if tech_materials:
                text = "🔧 Texnik uchun kerakli mahsulotlar:\n\n"
                
                for item in tech_materials:
                    status = "✅" if item['quantity'] > 0 else "❌"
                    text += f"{status} {item['name']}: {item['quantity']} {item.get('unit', 'dona')}\n"
                    
                    if len(text) > 3000:
                        text += "... va boshqalar"
                        break
                
                text += f"\n📞 Kerakli mahsulot yo'q bo'lsa, ombor bilan bog'laning"
            else:
                text = "📭 Texnik uchun mahsulotlar topilmadi"
            
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.callback_query(F.data == "warehouse_status")
    async def warehouse_status_for_junior_manager(callback: CallbackQuery, state: FSMContext):
        """Show warehouse status for junior manager"""
        try:
            # Mock warehouse status data (like other modules)
            status_data = {
                'total_items': 25,
                'available_items': 20,
                'low_stock_items': 3,
                'out_of_stock_items': 2,
                'total_value': 15000000
            }
            
            text = "📊 Ombor holati:\n\n"
            text += f"📦 Jami mahsulotlar: {status_data['total_items']}\n"
            text += f"✅ Mavjud: {status_data['available_items']}\n"
            text += f"⚠️ Kam zaxira: {status_data['low_stock_items']}\n"
            text += f"❌ Tugagan: {status_data['out_of_stock_items']}\n"
            text += f"💰 Jami qiymat: {status_data['total_value']:,} so'm\n"
            
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.callback_query(F.data == "used_materials")
    async def used_materials_for_technician(callback: CallbackQuery, state: FSMContext):
        """Show used materials for technician"""
        try:
            # Mock used materials data (like other modules)
            used_materials = [
                {'name': 'Cable', 'quantity_used': 5, 'date': '2024-01-15'},
                {'name': 'Connector', 'quantity_used': 8, 'date': '2024-01-15'},
                {'name': 'Cable Tester', 'quantity_used': 1, 'date': '2024-01-14'}
            ]
            
            if used_materials:
                text = "✅ Ishlatilgan mahsulotlar:\n\n"
                
                for material in used_materials:
                    text += f"📦 {material['name']}: {material['quantity_used']} dona\n"
                    text += f"📅 Sana: {material['date']}\n\n"
            else:
                text = "📭 Ishlatilgan mahsulotlar yo'q"
            
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.callback_query(F.data == "add_material_manager")
    async def add_material_manager(callback: CallbackQuery, state: FSMContext):
        """Add material for manager"""
        try:
            text = "➕ Mahsulot qo'shish:\n\n"
            text += "Bu funksiya tez orada qo'shiladi.\n"
            text += "Hozirda faqat ombor xodimi mahsulot qo'sha oladi."
            
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.callback_query(F.data == "back_to_main")
    async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
        """Back to main menu"""
        try:
            text = "🏠 Bosh menyuga qaytildi"
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    return router

# Mock functions (like other modules)
async def get_all_inventory_items():
    """Get all inventory items (mock function like other modules)"""
    try:
        return [
            {'name': 'Cable', 'quantity': 50, 'unit': 'dona', 'min_quantity': 10, 'price': 15000},
            {'name': 'Connector', 'quantity': 100, 'unit': 'dona', 'min_quantity': 15, 'price': 5000},
            {'name': 'Router', 'quantity': 10, 'unit': 'dona', 'min_quantity': 5, 'price': 500000},
            {'name': 'Switch', 'quantity': 5, 'unit': 'dona', 'min_quantity': 3, 'price': 300000},
            {'name': 'Cable Tester', 'quantity': 2, 'unit': 'dona', 'min_quantity': 1, 'price': 25000}
        ]
    except Exception as e:
        return []

async def update_inventory_quantity(item_id: int, quantity: int):
    """Update inventory quantity (mock function like other modules)"""
    try:
        # Mock update (like other modules)
        return True
    except Exception as e:
        return False

async def log_warehouse_activity(user_id: int, action: str, details: dict):
    """Log warehouse activity (mock function like other modules)"""
    try:
        # Mock logging (like other modules)
        pass
    except Exception as e:
        pass

async def get_warehouse_user_by_telegram_id(telegram_id: int):
    """Get warehouse user by telegram id (mock function like other modules)"""
    try:
        # Mock user data (like other modules)
        return {
            'id': 1,
            'telegram_id': telegram_id,
            'role': 'warehouse',
            'language': 'uz'
        }
    except Exception as e:
        return None