"""
Client Orders Handler - Database Integrated

This module handles viewing client orders with pagination.
"""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
from states.client_states import OrderStates
from filters.role_filter import RoleFilter
from keyboards.client_buttons import (
    get_orders_menu_keyboard,
    get_back_to_orders_menu_keyboard,
    get_client_orders_navigation_keyboard
)

# Mock database functions to replace database imports
async def get_user_by_telegram_id_redis(telegram_id: int):
    """Mock user data from Redis"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'client',
        'language': 'uz',
        'full_name': 'Test Client',
        'phone_number': '+998901234567',
        'region': 'toshkent'
    }

async def get_db_pool(region: str):
    """Mock database pool"""
    print(f"Mock: Getting database pool for region {region}")
    return MockPool()

class MockPool:
    """Mock database pool"""
    async def acquire(self):
        return MockConnection()
    
    async def close(self):
        print("Mock: Closing database pool")

class MockConnection:
    """Mock database connection"""
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def fetchval(self, query: str, *args):
        """Mock fetchval - return mock count"""
        print(f"Mock: Executing count query: {query} with args: {args}")
        return 5  # Return mock total count
    
    async def fetch(self, query: str, *args):
        """Mock fetch - return mock orders"""
        print(f"Mock: Executing orders query: {query} with args: {args}")
        # Mock orders data
        orders = [
            {
                'id': '1',
                'type': 'service',
                'status': 'active',
                'created_at': datetime.now(),
                'description': 'Internet tezligi sekin',
                'address': 'Chilanzor tumani, 15-uy',
                'state_data': '{"region": "Toshkent shahri"}'
            },
            {
                'id': '2',
                'type': 'connection',
                'status': 'completed',
                'created_at': datetime.now(),
                'description': 'Yangi ulanish',
                'address': 'Zangiota tumani, 25-uy',
                'state_data': '{"region": "Toshkent viloyati"}'
            },
            {
                'id': '3',
                'type': 'service',
                'status': 'pending',
                'created_at': datetime.now(),
                'description': 'TV signal yo\'q',
                'address': 'Andijon shahri, 8-uy',
                'state_data': '{"region": "Andijon"}'
            },
            {
                'id': '4',
                'type': 'connection',
                'status': 'active',
                'created_at': datetime.now(),
                'description': 'Uy internet ulanishi',
                'address': 'Farg\'ona shahri, 12-uy',
                'state_data': '{"region": "Farg\'ona"}'
            },
            {
                'id': '5',
                'type': 'service',
                'status': 'completed',
                'created_at': datetime.now(),
                'description': 'Router muammosi',
                'address': 'Samarqand shahri, 30-uy',
                'state_data': '{"region": "Samarqand"}'
            }
        ]
        return orders
    
    async def fetchrow(self, query: str, *args):
        """Mock fetchrow - return mock order details"""
        print(f"Mock: Executing order details query: {query} with args: {args}")
        order_id = args[0] if args else '1'
        return {
            'id': order_id,
            'type': 'service' if int(order_id) % 2 == 1 else 'connection',
            'status': 'active',
            'created_at': datetime.now(),
            'description': 'Test order description',
            'address': 'Test address',
            'contact_info': '{"phone": "+998901234567"}',
            'state_data': '{"region": "Test region"}',
            'full_name': 'Test Client',
            'phone': '+998901234567'
        }

async def get_user_orders(pool, user_id: int, page: int = 1, limit: int = 5):
    """Mock get user orders from database with pagination"""
    try:
        # Simulate database operations
        print(f"Mock: Getting orders for user {user_id}, page {page}, limit {limit}")
        
        # Mock orders data
        orders = [
            {
                'id': '1',
                'type': 'service',
                'status': 'active',
                'created_at': datetime.now(),
                'description': 'Internet tezligi sekin',
                'address': 'Chilanzor tumani, 15-uy',
                'region': 'Toshkent shahri',
                'request_id': '1'
            },
            {
                'id': '2',
                'type': 'connection',
                'status': 'completed',
                'created_at': datetime.now(),
                'description': 'Yangi ulanish',
                'address': 'Zangiota tumani, 25-uy',
                'region': 'Toshkent viloyati',
                'request_id': '2'
            },
            {
                'id': '3',
                'type': 'service',
                'status': 'pending',
                'created_at': datetime.now(),
                'description': 'TV signal yo\'q',
                'address': 'Andijon shahri, 8-uy',
                'region': 'Andijon',
                'request_id': '3'
            },
            {
                'id': '4',
                'type': 'connection',
                'status': 'active',
                'created_at': datetime.now(),
                'description': 'Uy internet ulanishi',
                'address': 'Farg\'ona shahri, 12-uy',
                'region': 'Farg\'ona',
                'request_id': '4'
            },
            {
                'id': '5',
                'type': 'service',
                'status': 'completed',
                'created_at': datetime.now(),
                'description': 'Router muammosi',
                'address': 'Samarqand shahri, 30-uy',
                'region': 'Samarqand',
                'request_id': '5'
            }
        ]
        
        # Pagination
        start = (page - 1) * limit
        end = start + limit
        paginated_orders = orders[start:end]
        
        return {
            'orders': paginated_orders,
            'total': len(orders),
            'page': page,
            'total_pages': (len(orders) + limit - 1) // limit
        }
        
    except Exception as e:
        print(f"Error getting user orders: {e}")
        return {
            'orders': [],
            'total': 0,
            'page': 1,
            'total_pages': 0
        }

async def get_order_details(pool, order_id: str):
    """Mock get detailed order information from database"""
    try:
        print(f"Mock: Getting order details for {order_id}")
        
        # Mock order details
        order = {
            'id': order_id,
            'type': 'service' if int(order_id) % 2 == 1 else 'connection',
            'status': 'active',
            'created_at': datetime.now(),
            'description': 'Test order description',
            'address': 'Test address',
            'phone': '+998901234567',
            'full_name': 'Test Client',
            'region': 'Test region',
            'request_id': order_id
        }
        
        return order
        
    except Exception as e:
        print(f"Error getting order details: {e}")
        
    return None

# Mock audit logger
class AuditLogger:
    async def log_action(self, user_id: int, action: str, details: dict):
        """Mock audit logging"""
        print(f"Mock Audit Log: User {user_id} performed {action} with details {details}")

audit_logger = AuditLogger()

def get_orders_router():
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📋 Mening buyurtmalarim"]))
    async def show_my_orders(message: Message, state: FSMContext):
        """Show user orders"""
        try:
            # Get user from Redis cache
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            if not user:
                await message.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.")
                return
            
            # Get user region to determine database
            region = user.get('region', 'toshkent')
            if region:
                region = region.lower()
            else:
                region = 'toshkent'
            pool = await get_db_pool(region)
            
            # Get user orders from database
            orders_data = await get_user_orders(pool, user['id'], page=1)
            
            if not orders_data['orders']:
                await message.answer("📋 Sizda hali buyurtmalar mavjud emas.")
                return
            
            # Save region in state for later use
            await state.update_data(user_region=region)
            
            # Show first order
            await show_order_details(message, orders_data['orders'][0], orders_data, 0, pool)
            
            # Log action (ixtiyoriy)
            await audit_logger.log_action(
                user_id=user['id'],
                action="view_orders",
                details={"total_orders": orders_data['total']}
            )
            
        except Exception as e:
            print(f"Error in show_my_orders: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("order_"))
    async def handle_order_navigation(callback: CallbackQuery, state: FSMContext):
        """Handle order navigation"""
        try:
            await callback.answer()
            
            # Get user and region from state
            user = await get_user_by_telegram_id_redis(callback.from_user.id)
            if not user:
                await callback.answer("Xatolik: Foydalanuvchi topilmadi", show_alert=True)
                return
                
            state_data = await state.get_data()
            region = state_data.get('user_region', user.get('region', 'toshkent')).lower()
            pool = await get_db_pool(region)
            
            data = callback.data.split("_")
            action = data[1]
            
            if action == "next":
                current_index = int(data[2])
                current_page = int(data[3])
                await show_next_order(callback, current_index, current_page, pool, user['id'])
            elif action == "prev":
                current_index = int(data[2])
                current_page = int(data[3])
                await show_previous_order(callback, current_index, current_page, pool, user['id'])
            elif action == "details":
                order_id = data[2]  # Keep as string since our IDs are strings
                order = await get_order_details(pool, order_id)
                if order:
                    await show_order_details(callback, order, None, 0, pool)
                else:
                    await callback.answer("Buyurtma topilmadi", show_alert=True)
                    
        except Exception as e:
            print(f"Error in handle_order_navigation: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    async def show_order_details(message_or_callback, order, orders_data, index, pool):
        """Show order details with navigation"""
        try:
            # Format order type
            order_type_emoji = "🔧" if order['type'] == 'service' else "🔌"
            order_type_text = "Texnik xizmat" if order['type'] == 'service' else "Ulanish"
            
            # Format status
            status_emoji = {
                'active': '🟡',
                'in_progress': '🟡',
                'pending': '🟠',
                'created': '🟠', 
                'completed': '🟢',
                'cancelled': '🔴',
                'rejected': '🔴'
            }.get(order.get('status', ''), '⚪')
            
            status_text = {
                'active': 'Faol',
                'in_progress': 'Jarayonda',
                'pending': 'Kutilmoqda',
                'created': 'Yaratilgan',
                'completed': 'Bajarilgan',
                'cancelled': 'Bekor qilingan',
                'rejected': 'Rad etilgan'
            }.get(order.get('status', ''), 'Noma\'lum')
            
            # Format date
            if order.get('created_at'):
                if isinstance(order['created_at'], str):
                    created_date = datetime.strptime(order['created_at'], '%Y-%m-%d %H:%M:%S')
                else:
                    created_date = order['created_at']
                formatted_date = created_date.strftime('%d.%m.%Y %H:%M')
            else:
                formatted_date = 'Noma\'lum'
            
            # To'liq ma'lumot
            text = (
                f"{order_type_emoji} <b>{order_type_text} - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {order.get('request_id', 'Noma\'lum')}\n"
                f"📅 <b>Sana:</b> {formatted_date}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"📍 <b>Hudud:</b> {order.get('region', 'Noma\'lum')}\n"
                f"🏠 <b>Manzil:</b> {order.get('address', 'Noma\'lum')}\n\n"
                f"📝 <b>Tavsif:</b>\n{order.get('description', 'Ma\'lumot yo\'q')}"
            )
            
            # Create navigation keyboard if orders_data provided
            keyboard = None
            if orders_data:
                total = orders_data['total']
                current_page = orders_data['page']
                total_pages = orders_data['total_pages']
                
                buttons = []
                nav_buttons = []
                
                # Previous button
                if index > 0:
                    nav_buttons.append(
                        InlineKeyboardButton(
                            text="⬅️ Oldingi",
                            callback_data=f"order_prev_{index}_{current_page}"
                        )
                    )
                
                # Counter
                nav_buttons.append(
                    InlineKeyboardButton(
                        text=f"{index + 1}/{len(orders_data['orders'])}",
                        callback_data="none"
                    )
                )
                
                # Next button
                if index < len(orders_data['orders']) - 1:
                    nav_buttons.append(
                        InlineKeyboardButton(
                            text="Keyingi ➡️",
                            callback_data=f"order_next_{index}_{current_page}"
                        )
                    )
                
                
                if nav_buttons:
                    buttons.append(nav_buttons)
                

                
                keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            # Send or edit message
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, parse_mode="HTML", reply_markup=keyboard)
            else:
                await message_or_callback.message.edit_text(text, parse_mode="HTML", reply_markup=keyboard)
                
        except Exception as e:
            print(f"Error in show_order_details: {e}")
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("❌ Xatolik yuz berdi")
            else:
                await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    async def show_next_order(callback: CallbackQuery, current_index: int, current_page: int, pool, user_id: int):
        """Show next order"""
        try:
            orders_data = await get_user_orders(pool, user_id, page=current_page)
            
            if current_index + 1 < len(orders_data['orders']):
                # Show next order on same page
                await show_order_details(
                    callback,
                    orders_data['orders'][current_index + 1],
                    orders_data,
                    current_index + 1,
                    pool
                )
            elif current_page < orders_data['total_pages']:
                # Load next page
                next_page_data = await get_user_orders(pool, user_id, page=current_page + 1)
                if next_page_data['orders']:
                    await show_order_details(
                        callback,
                        next_page_data['orders'][0],
                        next_page_data,
                        0,
                        pool
                    )
                    
        except Exception as e:
            print(f"Error in show_next_order: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    async def show_previous_order(callback: CallbackQuery, current_index: int, current_page: int, pool, user_id: int):
        """Show previous order"""
        try:
            orders_data = await get_user_orders(pool, user_id, page=current_page)
            
            if current_index > 0:
                # Show previous order on same page
                await show_order_details(
                    callback,
                    orders_data['orders'][current_index - 1],
                    orders_data,
                    current_index - 1,
                    pool
                )
            elif current_page > 1:
                # Load previous page
                prev_page_data = await get_user_orders(pool, user_id, page=current_page - 1)
                if prev_page_data['orders']:
                    await show_order_details(
                        callback,
                        prev_page_data['orders'][-1],
                        prev_page_data,
                        len(prev_page_data['orders']) - 1,
                        pool
                    )
                    
        except Exception as e:
            print(f"Error in show_previous_order: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router