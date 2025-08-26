from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.warehouse_buttons import warehouse_inventory_menu, inventory_actions_keyboard, inventory_actions_inline, update_item_fields_inline
from states.warehouse_states import WarehouseInventoryStates, WarehouseMainMenuStates
from aiogram.utils.keyboard import InlineKeyboardBuilder
from filters.role_filter import RoleFilter

# Paginatsiya uchun yordamchi funksiya
def build_pagination_keyboard(page: int, total_pages: int, lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    prev = "⬅️ Avvalgi"
    next_ = "Keyingisi ➡️"
    if page > 1:
        builder.button(text=prev, callback_data=f"inventory_page_{page-1}")
    if page < total_pages:
        builder.button(text=next_, callback_data=f"inventory_page_{page+1}")
    return builder.as_markup()

# Barcha mahsulotlar reply uchun paginatsiyali handler
def chunked(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_warehouse_inventory_router():
    """Warehouse inventory router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("warehouse")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text == "📦 Inventarizatsiya")
    async def inventory_management_handler(message: Message, state: FSMContext):
        """Inventory management handler"""
        try:
            # Debug logging
            print(f"Warehouse inventory handler called by user {message.from_user.id}")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            await state.update_data(lang='uz')
            inventory_text = "📦 Inventarizatsiya boshqaruvi"
            
            await message.answer(
                inventory_text,
                reply_markup=warehouse_inventory_menu('uz')
            )
            await state.set_state(WarehouseInventoryStates.inventory_menu)
            
            print(f"Warehouse inventory handler completed successfully")
            
        except Exception as e:
            print(f"Error in warehouse inventory handler: {str(e)}")
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "view_inventory_list")
    async def view_inventory_list(callback: CallbackQuery, state: FSMContext):
        """View complete inventory list"""
        try:
            # Mock inventory data (like other modules)
            items = [
                {
                    'id': 1,
                    'name': 'Cable',
                    'quantity': 50,
                    'unit': 'dona',
                    'price': 15000,
                    'min_quantity': 10,
                    'category': 'cables',
                    'description': 'Internet kabeli'
                },
                {
                    'id': 2,
                    'name': 'Router',
                    'quantity': 10,
                    'unit': 'dona',
                    'price': 500000,
                    'min_quantity': 5,
                    'category': 'equipment',
                    'description': 'WiFi router'
                },
                {
                    'id': 3,
                    'name': 'Connector',
                    'quantity': 100,
                    'unit': 'dona',
                    'price': 5000,
                    'min_quantity': 15,
                    'category': 'equipment',
                    'description': 'RJ45 connector'
                }
            ]
            
            if items:
                text = "📋 Inventar ro'yxati:\n\n"
                
                for item in items:
                    status_icon = "✅" if item['quantity'] > item.get('min_quantity', 0) else "⚠️"
                    text += f"{status_icon} **{item['name']}**\n"
                    text += f"   📦 Miqdor: {item['quantity']} {item.get('unit', 'dona')}\n"
                    text += f"   💰 Narx: {item.get('price', 0):,} so'm\n"
                    if item.get('min_quantity'):
                        text += f"   ⚠️ Min: {item['min_quantity']}\n"
                    if item.get('category'):
                        text += f"   🏷️ Kategoriya: {item['category']}\n"
                    text += "\n"
                    
                    # Limit text length to avoid Telegram message limits
                    if len(text) > 3500:
                        text += "... va boshqalar"
                        break
            else:
                text = "📭 Inventar ro'yxati bo'sh"
            
            await callback.message.edit_text(
                text,
                parse_mode="Markdown"
            )
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Inventar ro'yxatini olishda xatolik")
            await callback.answer()

    @router.callback_query(F.data == "warehouse_inventory")
    async def warehouse_inventory_callback(callback: CallbackQuery, state: FSMContext):
        """Warehouse inventory callback handler"""
        try:
            await state.set_state(WarehouseInventoryStates.inventory_menu)
            inventory_text = "📦 Inventarizatsiya boshqaruvi"
            
            await callback.message.edit_text(
                inventory_text,
                reply_markup=warehouse_inventory_menu('uz')
            )
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.callback_query(F.data == "add_inventory_item")
    async def add_inventory_item_handler(callback: CallbackQuery, state: FSMContext):
        """Start adding inventory item"""
        try:
            await state.set_state(WarehouseInventoryStates.adding_item_name)
            text = "📝 Mahsulot nomini kiriting:"
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Mahsulot qo'shishda xatolik")
            await callback.answer()

    @router.message(StateFilter(WarehouseInventoryStates.adding_item_name))
    async def get_item_name(message: Message, state: FSMContext):
        await state.update_data(item_name=message.text)
        await state.set_state(WarehouseInventoryStates.adding_item_quantity)
        await message.answer("🔢 Miqdorni kiriting:")

    @router.message(StateFilter(WarehouseInventoryStates.adding_item_quantity))
    async def get_item_quantity(message: Message, state: FSMContext):
        try:
            quantity = int(message.text)
            if quantity < 0:
                raise ValueError
            await state.update_data(item_quantity=quantity)
            await state.set_state(WarehouseInventoryStates.adding_item_price)
            await message.answer("💰 Narxni kiriting (so'm):")
        except ValueError:
            await message.answer("❌ Noto'g'ri miqdor. Musbat raqam kiriting.")

    @router.message(StateFilter(WarehouseInventoryStates.adding_item_price))
    async def get_item_price(message: Message, state: FSMContext):
        try:
            price = float(message.text)
            if price < 0:
                raise ValueError
            await state.update_data(item_price=price)
            data = await state.get_data()
            await state.set_state(WarehouseInventoryStates.adding_item_description)
            await message.answer("📝 Mahsulot tavsifini kiriting (ixtiyoriy, o'tkazib yuborish uchun -)")
        except ValueError:
            await message.answer("❌ Noto'g'ri narx. Musbat raqam kiriting.")

    @router.message(StateFilter(WarehouseInventoryStates.adding_item_description))
    async def get_item_description(message: Message, state: FSMContext):
        data = await state.get_data()
        description = message.text if message.text.strip() != '-' else ''
        item_data = {
            'name': data['item_name'],
            'quantity': data['item_quantity'],
            'price': data['item_price'],
            'unit': 'dona',
            'category': 'general',
            'description': description
        }
        
        # Mock success response (like other modules)
        await message.answer(f"✅ Mahsulot muvaffaqiyatli qo'shildi!\n📦 Nom: {item_data['name']}\n🔢 Miqdor: {item_data['quantity']}\n💰 Narx: {item_data['price']:,} so'm")
        
        await state.set_state(WarehouseInventoryStates.inventory_menu)
        await message.answer(
            "📦 Inventarizatsiya menyusi:",
            reply_markup=warehouse_inventory_menu('uz')
        )

    @router.callback_query(F.data == "update_inventory_item")
    async def update_inventory_item_handler(callback: CallbackQuery, state: FSMContext):
        """Start updating inventory item"""
        try:
            # Mock inventory data (like other modules)
            items = [
                {
                    'id': 1,
                    'name': 'Cable',
                    'quantity': 50,
                    'unit': 'dona',
                    'price': 15000,
                    'min_quantity': 10,
                    'category': 'cables',
                    'description': 'Internet kabeli'
                },
                {
                    'id': 2,
                    'name': 'Router',
                    'quantity': 10,
                    'unit': 'dona',
                    'price': 500000,
                    'min_quantity': 5,
                    'category': 'equipment',
                    'description': 'WiFi router'
                }
            ]
            
            if items:
                text = "🔄 Yangilanadigan mahsulotni tanlang:\n\n"
                
                for i, item in enumerate(items[:10], 1):  # Show first 10 items
                    text += f"{i}. **{item['name']}** (Miqdor: {item['quantity']})\n"
                
                text += f"\n📝 Mahsulot raqamini kiriting:"
                
                await callback.message.edit_text(text, parse_mode="Markdown")
                await state.update_data(available_items=items)
                await state.set_state(WarehouseInventoryStates.selecting_item_to_update)
            else:
                text = "📭 Yangilanadigan mahsulotlar yo'q"
                await callback.message.edit_text(text)
            
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    async def format_item_info(item: dict, lang: str) -> str:
        if not item:
            return "❌ Mahsulot topilmadi."
        text = f"📦 {item['name']}\n"
        text += f"🔢 Miqdor: {item['quantity']}\n"
        text += f"💰 Narx: {item.get('price', 0):,} so'm\n"
        text += f"📝 Tavsif: {item.get('description', '') or '-'}\n"
        return text

    # Yangilash uchun tanlash bosqichida mahsulot ma'lumotlarini chiqarish
    @router.message(StateFilter(WarehouseInventoryStates.selecting_item_to_update))
    async def select_item_to_update(message: Message, state: FSMContext):
        try:
            item_number = int(message.text)
            data = await state.get_data()
            items = data.get('available_items', [])
            if 1 <= item_number <= len(items):
                selected_item = items[item_number - 1]
                await state.update_data(selected_item=selected_item)
                info = await format_item_info(selected_item, 'uz')
                await message.answer("🔎 Tanlangan mahsulot ma'lumotlari:\n" + info)
                await message.answer(
                    f"🛠️ Qaysi maydonni yangilamoqchisiz?",
                    reply_markup=update_item_fields_inline(selected_item['id'], 'uz')
                )
                await state.set_state(WarehouseInventoryStates.updating_item_info)
            else:
                await message.answer("❌ Noto'g'ri raqam. Qaytadan kiriting.")
        except ValueError:
            await message.answer("❌ Noto'g'ri format. Raqam kiriting.")

    @router.message(StateFilter(WarehouseInventoryStates.updating_item_quantity))
    async def update_item_quantity(message: Message, state: FSMContext):
        try:
            quantity = int(message.text)
            if quantity < 0:
                raise ValueError
            data = await state.get_data()
            selected_item = data.get('selected_item')
            item_id = selected_item['id']
            
            # Mock success response (like other modules)
            await message.answer(f"✅ Miqdor yangilandi: {quantity}")
            await state.set_state(WarehouseInventoryStates.inventory_menu)
            await message.answer(
                "📦 Inventarizatsiya menyusi:",
                reply_markup=warehouse_inventory_menu('uz')
            )
        except ValueError:
            await message.answer("❌ Noto'g'ri miqdor. Musbat raqam kiriting.")

    @router.callback_query(F.data == "low_stock_report")
    async def low_stock_report_handler(callback: CallbackQuery, state: FSMContext):
        """Show low stock report"""
        try:
            # Mock low stock data (like other modules)
            low_stock_items = [
                {
                    'name': 'Cable',
                    'quantity': 5,
                    'unit': 'dona',
                    'min_quantity': 10,
                    'price': 15000
                },
                {
                    'name': 'Connector',
                    'quantity': 8,
                    'unit': 'dona',
                    'min_quantity': 15,
                    'price': 5000
                }
            ]
            
            if low_stock_items:
                text = "⚠️ Kam zaxira hisoboti:\n\n"
                
                for item in low_stock_items:
                    text += f"🔴 **{item['name']}**\n"
                    text += f"   📦 Joriy: {item['quantity']} {item.get('unit', 'dona')}\n"
                    text += f"   ⚠️ Minimal: {item.get('min_quantity', 0)}\n"
                    shortage = item.get('min_quantity', 0) - item['quantity']
                    if shortage > 0:
                        text += f"   📉 Kamomad: {shortage}\n"
                    text += "\n"
            else:
                text = "✅ Kam zaxira mahsulotlari yo'q"
            
            await callback.message.edit_text(
                text,
                parse_mode="Markdown"
            )
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Hisobotni olishda xatolik")
            await callback.answer()

    @router.callback_query(F.data == "inventory_search")
    async def inventory_search_handler(callback: CallbackQuery, state: FSMContext):
        """Start inventory search"""
        try:
            await state.set_state(WarehouseInventoryStates.searching_inventory)
            search_text = "🔍 Qidiruv so'zini kiriting:"
            await callback.message.edit_text(search_text)
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.message(StateFilter(WarehouseInventoryStates.searching_inventory))
    async def process_inventory_search(message: Message, state: FSMContext):
        """Process inventory search"""
        try:
            search_query = message.text.strip()
            
            # Mock search results (like other modules)
            found_items = [
                {
                    'name': 'Cable',
                    'quantity': 50,
                    'unit': 'dona',
                    'price': 15000,
                    'description': 'Internet kabeli'
                }
            ] if 'cable' in search_query.lower() else []
            
            if found_items:
                text = "🔍 Qidiruv natijalari:\n\n"
                
                for item in found_items:
                    status_icon = "✅" if item['quantity'] > 0 else "❌"
                    text += f"{status_icon} **{item['name']}**\n"
                    text += f"   📦 Miqdor: {item['quantity']} {item.get('unit', 'dona')}\n"
                    text += f"   💰 Narx: {item.get('price', 0):,} so'm\n"
                    if item.get('description'):
                        text += f"   📝 Tavsif: {item['description']}\n"
                    text += "\n"
            else:
                text = "❌ Hech narsa topilmadi"
            
            await message.answer(text, parse_mode="Markdown")
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
        except Exception as e:
            await message.answer("Qidirishda xatolik")
            await state.set_state(WarehouseMainMenuStates.main_menu)

    @router.callback_query(F.data == "inventory_out_of_stock")
    async def inventory_out_of_stock_handler(callback: CallbackQuery, state: FSMContext):
        """Show out of stock items"""
        try:
            # Mock out of stock data (like other modules)
            out_of_stock_items = [
                {
                    'name': 'Old Router',
                    'quantity': 0,
                    'unit': 'dona',
                    'price': 300000,
                    'min_quantity': 2
                }
            ]
            
            if out_of_stock_items:
                text = "❌ Tugagan mahsulotlar:\n\n"
                
                for item in out_of_stock_items:
                    text += f"🔴 **{item['name']}**\n"
                    text += f"   📦 Miqdor: 0 {item.get('unit', 'dona')}\n"
                    text += f"   💰 Narx: {item.get('price', 0):,} so'm\n"
                    if item.get('min_quantity'):
                        text += f"   ⚠️ Kerakli: {item['min_quantity']}\n"
                    text += "\n"
            else:
                text = "✅ Tugagan mahsulotlar yo'q"
            
            await callback.message.edit_text(text, parse_mode="Markdown")
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Ma'lumotlarni olishda xatolik")
            await callback.answer()

    @router.message(F.text == "➕ Mahsulot qo'shish")
    async def add_item_handler(message: Message, state: FSMContext):
        await state.set_state(WarehouseInventoryStates.adding_item_name)
        await message.answer("📝 Mahsulot nomini kiriting:")

    @router.message(F.text == "⚠️ Kam zaxira")
    async def low_stock_handler(message: Message, state: FSMContext):
        # Mock low stock data (like other modules)
        items = [
            {
                'name': 'Cable',
                'quantity': 5
            },
            {
                'name': 'Connector',
                'quantity': 8
            }
        ]
        
        if items:
            text = "⚠️ Kam zaxira mahsulotlar:\n"
            for item in items:
                text += f"- {item['name']} ({item['quantity']})\n"
        else:
            text = "Barcha mahsulotlar yetarli."
        await message.answer(text)

    @router.message(F.text == "❌ Tugagan mahsulotlar")
    async def out_of_stock_handler(message: Message, state: FSMContext):
        # Mock out of stock data (like other modules)
        items = [
            {
                'name': 'Old Router'
            }
        ]
        
        if items:
            text = "❌ Tugagan mahsulotlar:\n"
            for item in items:
                text += f"- {item['name']}\n"
        else:
            text = "Barcha mahsulotlarda zaxira bor."
        await message.answer(text)

    @router.message(F.text == "🔍 Qidirish")
    async def search_inventory_start(message: Message, state: FSMContext):
        await state.set_state(WarehouseInventoryStates.searching_inventory)
        await message.answer("🔍 Qidiriladigan mahsulot nomini kiriting:")

    @router.message(F.text == "📋 Barcha mahsulotlar")
    async def view_all_inventory_handler(message: Message, state: FSMContext):
        # Mock inventory data (like other modules)
        items = [
            {
                'id': 1,
                'name': 'Cable',
                'quantity': 50,
                'unit': 'dona',
                'price': 15000,
                'min_quantity': 10,
                'category': 'cables',
                'description': 'Internet kabeli'
            },
            {
                'id': 2,
                'name': 'Router',
                'quantity': 10,
                'unit': 'dona',
                'price': 500000,
                'min_quantity': 5,
                'category': 'equipment',
                'description': 'WiFi router'
            },
            {
                'id': 3,
                'name': 'Connector',
                'quantity': 100,
                'unit': 'dona',
                'price': 5000,
                'min_quantity': 15,
                'category': 'equipment',
                'description': 'RJ45 connector'
            }
        ]
        
        if not items:
            await message.answer("Inventar bo'sh.")
            return
            
        await state.update_data(inventory_items=items, inventory_page=1)
        await send_inventory_page(message, state, page=1, lang='uz')

    @router.callback_query(F.data.startswith("inventory_page_"))
    async def inventory_pagination_callback(callback: CallbackQuery, state: FSMContext):
        """Handle pagination for inventory items"""
        try:
            # Get current items from state
            state_data = await state.get_data()
            items = state_data.get('inventory_items', [])
            
            if not items:
                await callback.answer("❌ Hech qanday mahsulot topilmadi")
                return
                
            # Get the requested page number
            page = int(callback.data.split('_')[-1])
            
            # Update the current page in state
            await state.update_data(inventory_page=page)
            
            # Send the requested page
            await send_inventory_page(
                callback.message, 
                state, 
                page=page, 
                lang='uz', 
                edit=True, 
                callback=callback
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi")

    async def send_inventory_page(message_or_callback, state: FSMContext, page: int, lang: str = 'uz', edit=False, callback=None):
        """Display a page of inventory items with pagination"""
        try:
            # Get items from state
            state_data = await state.get_data()
            items = state_data.get('inventory_items', [])
            
            if not items:
                no_items_msg = "Inventar bo'sh."
                if edit and callback:
                    await callback.message.edit_text(no_items_msg)
                    await callback.answer()
                else:
                    await message_or_callback.answer(no_items_msg)
                return
            
            # Calculate pagination
            per_page = 5
            total_pages = max(1, (len(items) + per_page - 1) // per_page)
            page = max(1, min(page, total_pages))
            start = (page - 1) * per_page
            end = start + per_page
            page_items = items[start:end]
            
            # Format items
            texts = []
            for item in page_items:
                item_text = await format_item_info(item, lang)
                texts.append(item_text)
            
            if not texts:
                no_items_msg = "Mahsulot ma'lumotlari topilmadi."
                if edit and callback:
                    await callback.message.edit_text(no_items_msg)
                    await callback.answer()
                else:
                    await message_or_callback.answer(no_items_msg)
                return
            
            # Create message text
            text = f"\n{'-'*20}\n".join(texts)
            header = f"📋 Barcha mahsulotlar (sahifa {page}/{total_pages}):\n\n"
            text = header + text
            
            # Build and send message
            keyboard = build_pagination_keyboard(page, total_pages, lang)
            if edit and callback:
                await callback.message.edit_text(text, reply_markup=keyboard)
                await callback.answer()
            else:
                await message_or_callback.answer(text, reply_markup=keyboard)
                
        except Exception as e:
            error_msg = "Xatolik yuz berdi. Qaytadan urinib ko'ring."
            if edit and callback:
                await callback.message.edit_text(error_msg)
                await callback.answer()
            else:
                await message_or_callback.answer(error_msg)

    @router.callback_query(F.data.startswith("increase_"))
    async def increase_quantity_handler(callback: CallbackQuery, state: FSMContext):
        item_id = int(callback.data.split("_")[1])
        await state.update_data(action_item_id=item_id, action_type="increase")
        await callback.message.answer("➕ Qancha kirim qilmoqchisiz?")
        await state.set_state(WarehouseInventoryStates.updating_item_quantity)
        await callback.answer()

    @router.callback_query(F.data.startswith("decrease_"))
    async def decrease_quantity_handler(callback: CallbackQuery, state: FSMContext):
        item_id = int(callback.data.split("_")[1])
        await state.update_data(action_item_id=item_id, action_type="decrease")
        await callback.message.answer("➖ Qancha chiqim qilmoqchisiz?")
        await state.set_state(WarehouseInventoryStates.updating_item_quantity)
        await callback.answer()

    @router.message(StateFilter(WarehouseInventoryStates.updating_item_quantity))
    async def process_quantity_change(message: Message, state: FSMContext):
        data = await state.get_data()
        item_id = data.get("action_item_id")
        action_type = data.get("action_type")
        try:
            amount = int(message.text)
            if amount < 0:
                raise ValueError
            
            # Mock success response (like other modules)
            new_quantity = 50 + amount if action_type == "increase" else 50 - amount
            if new_quantity < 0:
                await message.answer("Chiqim miqdori mavjud zaxiradan oshib ketdi.")
                return
            await message.answer(f"✅ Yangi miqdor: {new_quantity}")
            await state.set_state(WarehouseInventoryStates.inventory_menu)
        except ValueError:
            await message.answer("Faqat musbat raqam kiriting.")

    @router.message(StateFilter(WarehouseInventoryStates.updating_item_info))
    async def process_item_info_update(message: Message, state: FSMContext):
        """Process item info update"""
        try:
            data = await state.get_data()
            editing_field = data.get("editing_field")
            item_id = data.get("editing_item_id")
            
            if editing_field == "name":
                # Mock success response (like other modules)
                await message.answer(f"✅ Mahsulot nomi yangilandi: {message.text}")
            elif editing_field == "price":
                try:
                    price = float(message.text)
                    await message.answer(f"✅ Mahsulot narxi yangilandi: {price:,} so'm")
                except ValueError:
                    await message.answer("❌ Noto'g'ri narx. Musbat raqam kiriting.")
                    return
            elif editing_field == "description":
                await message.answer(f"✅ Mahsulot tavsifi yangilandi: {message.text}")
            else:
                await message.answer("❌ Noma'lum maydon")
                return
            
            await state.set_state(WarehouseInventoryStates.inventory_menu)
            await message.answer(
                "📦 Inventarizatsiya menyusi:",
                reply_markup=warehouse_inventory_menu('uz')
            )
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")
            await state.set_state(WarehouseInventoryStates.inventory_menu)

    @router.callback_query(F.data.startswith("delete_"))
    async def delete_item_handler(callback: CallbackQuery, state: FSMContext):
        item_id = int(callback.data.split("_")[1])
        
        # Mock success response (like other modules)
        await callback.message.answer("🗑️ Mahsulot o'chirildi.")
        await callback.answer()

    @router.callback_query(F.data.startswith("update_name_"))
    async def update_item_name_handler(callback: CallbackQuery, state: FSMContext):
        """Update item name handler"""
        try:
            item_id = int(callback.data.split("_")[2])
            await state.update_data(editing_item_id=item_id, editing_field="name")
            await state.set_state(WarehouseInventoryStates.updating_item_info)
            await callback.message.answer("📝 Yangi nomni kiriting:")
            await callback.answer()
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.callback_query(F.data.startswith("update_quantity_"))
    async def update_item_quantity_handler(callback: CallbackQuery, state: FSMContext):
        """Update item quantity handler"""
        try:
            item_id = int(callback.data.split("_")[2])
            await state.update_data(editing_item_id=item_id, editing_field="quantity")
            await state.set_state(WarehouseInventoryStates.updating_item_quantity)
            await callback.message.answer("🔢 Yangi miqdorni kiriting:")
            await callback.answer()
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.callback_query(F.data.startswith("update_price_"))
    async def update_item_price_handler(callback: CallbackQuery, state: FSMContext):
        """Update item price handler"""
        try:
            item_id = int(callback.data.split("_")[2])
            await state.update_data(editing_item_id=item_id, editing_field="price")
            await state.set_state(WarehouseInventoryStates.updating_item_info)
            await callback.message.answer("💰 Yangi narxni kiriting:")
            await callback.answer()
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.callback_query(F.data.startswith("update_description_"))
    async def update_item_description_handler(callback: CallbackQuery, state: FSMContext):
        """Update item description handler"""
        try:
            item_id = int(callback.data.split("_")[2])
            await state.update_data(editing_item_id=item_id, editing_field="description")
            await state.set_state(WarehouseInventoryStates.updating_item_info)
            await callback.message.answer("📝 Yangi tavsifni kiriting:")
            await callback.answer()
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.message(F.text == "◀️ Orqaga")
    async def back_to_main_menu_handler(message: Message, state: FSMContext):
        from keyboards.warehouse_buttons import get_warehouse_main_keyboard
        await state.set_state(WarehouseMainMenuStates.main_menu)
        await message.answer(
            "🏢 Ombor paneliga qaytdingiz.",
            reply_markup=get_warehouse_main_keyboard('uz')
        )

    @router.callback_query(F.data == "warehouse_back")
    async def warehouse_back_callback(callback: CallbackQuery, state: FSMContext):
        """Warehouse back callback handler"""
        try:
            from keyboards.warehouse_buttons import get_warehouse_main_keyboard
            await state.set_state(WarehouseMainMenuStates.main_menu)
            await callback.message.edit_text(
                "🏢 Ombor paneliga qaytdingiz."
            )
            await callback.message.answer(
                "🏢 Ombor paneli:",
                reply_markup=get_warehouse_main_keyboard('uz')
            )
            await callback.answer()
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")
            await callback.answer()

    @router.message(F.text == "✏️ Mahsulotni yangilash")
    async def update_item_handler(message: Message, state: FSMContext):
        # Mock inventory data (like other modules)
        items = [
            {
                'id': 1,
                'name': 'Cable',
                'quantity': 50
            },
            {
                'id': 2,
                'name': 'Router',
                'quantity': 10
            }
        ]
        
        if items:
            text = "🔄 Yangilanadigan mahsulotni tanlang:\n\n"
            for i, item in enumerate(items[:10], 1):
                text += f"{i}. {item['name']} (Miqdor: {item['quantity']})\n"
            text += "\n📝 Mahsulot raqamini kiriting:"
            await message.answer(text)
            await state.update_data(available_items=items)
            await state.set_state(WarehouseInventoryStates.selecting_item_to_update)
        else:
            await message.answer("📭 Yangilanadigan mahsulotlar yo'q")

    return router

# Mock functions (like other modules)
async def get_all_inventory_items():
    """Get all inventory items (mock function like other modules)"""
    try:
        return [
            {
                'id': 1,
                'name': 'Cable',
                'quantity': 50,
                'unit': 'dona',
                'price': 15000,
                'min_quantity': 10,
                'category': 'cables',
                'description': 'Internet kabeli'
            },
            {
                'id': 2,
                'name': 'Router',
                'quantity': 10,
                'unit': 'dona',
                'price': 500000,
                'min_quantity': 5,
                'category': 'equipment',
                'description': 'WiFi router'
            },
            {
                'id': 3,
                'name': 'Connector',
                'quantity': 100,
                'unit': 'dona',
                'price': 5000,
                'min_quantity': 15,
                'category': 'equipment',
                'description': 'RJ45 connector'
            }
        ]
    except Exception as e:
        return []

async def add_new_inventory_item(item_data: dict):
    """Add new inventory item (mock function like other modules)"""
    try:
        # Mock add (like other modules)
        return 1  # Return new item ID
    except Exception as e:
        return None

async def update_inventory_item_data(item_id: int, update_data: dict):
    """Update inventory item data (mock function like other modules)"""
    try:
        # Mock update (like other modules)
        return True
    except Exception as e:
        return False

async def search_inventory_items(query: str):
    """Search inventory items (mock function like other modules)"""
    try:
        # Mock search (like other modules)
        if 'cable' in query.lower():
            return [
                {
                    'name': 'Cable',
                    'quantity': 50,
                    'unit': 'dona',
                    'price': 15000,
                    'description': 'Internet kabeli'
                }
            ]
        return []
    except Exception as e:
        return []

async def get_low_stock_inventory_items():
    """Get low stock inventory items (mock function like other modules)"""
    try:
        return [
            {
                'name': 'Cable',
                'quantity': 5,
                'unit': 'dona',
                'min_quantity': 10,
                'price': 15000
            },
            {
                'name': 'Connector',
                'quantity': 8,
                'unit': 'dona',
                'min_quantity': 15,
                'price': 5000
            }
        ]
    except Exception as e:
        return []

async def get_out_of_stock_items():
    """Get out of stock items (mock function like other modules)"""
    try:
        return [
            {
                'name': 'Old Router',
                'quantity': 0,
                'unit': 'dona',
                'price': 300000,
                'min_quantity': 2
            }
        ]
    except Exception as e:
        return []

async def get_inventory_item_by_id(item_id: int):
    """Get inventory item by id (mock function like other modules)"""
    try:
        # Mock item data (like other modules)
        return {
            'id': item_id,
            'name': 'Test Item',
            'quantity': 50,
            'unit': 'dona',
            'price': 15000,
            'description': 'Test description'
        }
    except Exception as e:
        return None
