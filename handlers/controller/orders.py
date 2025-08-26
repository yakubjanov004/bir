"""
Controller Orders Handler - Mock Data Implementation

Manages orders for controller with mock data.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from filters.role_filter import RoleFilter
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Mock data storage
mock_users = {
    123456789: {
        'id': 1,
        'telegram_id': 123456789,
        'role': 'controller',
        'language': 'uz',
        'full_name': 'Test Controller',
        'phone_number': '+998901234567',
        'region': 'toshkent'
    }
}

# Mock controller orders data
mock_controller_orders = [
    {
        'id': 'REQ001',
        'order_number': 'REQ001',
        'client_name': 'Aziz Karimov',
        'workflow_type': 'connection_request',
        'current_status': 'created',
        'priority': 'high',
        'created_at': datetime.now() - timedelta(hours=2),
        'technician_name': 'Tayinlanmagan',
        'description': 'Yangi uy uchun internet xizmatini ulashish kerak',
        'location': 'Toshkent, Chilonzor tumani, 15-uy',
        'contact_info': {'phone': '+998901234567'},
        'state_data': {'tariff': 'Premium', 'connection_type': 'B2C'}
    },
    {
        'id': 'REQ002',
        'order_number': 'REQ002',
        'client_name': 'Malika Yusupova',
        'workflow_type': 'technical_service',
        'current_status': 'pending_assignment',
        'priority': 'urgent',
        'created_at': datetime.now() - timedelta(hours=4),
        'technician_name': 'Tayinlanmagan',
        'description': 'Internet tezligi juda sekin, 1 Mbps ga tushib qoldi',
        'location': 'Toshkent, Sergeli tumani, 25-uy',
        'contact_info': {'phone': '+998901234568'},
        'state_data': {'service_type': 'Speed Issue', 'abonent_id': 'AB001'}
    },
    {
        'id': 'REQ003',
        'order_number': 'REQ003',
        'client_name': 'Jasur Toshmatov',
        'workflow_type': 'connection_request',
        'current_status': 'assigned_to_technician',
        'priority': 'medium',
        'created_at': datetime.now() - timedelta(hours=6),
        'technician_name': 'Ahmad Texnik',
        'description': 'Biznes markaz uchun internet xizmati',
        'location': 'Toshkent, Yakkasaroy tumani, 8-uy',
        'contact_info': {'phone': '+998901234569'},
        'state_data': {'tariff': 'Business', 'connection_type': 'B2B'}
    },
    {
        'id': 'REQ004',
        'order_number': 'REQ004',
        'client_name': 'Dilfuza Rahimova',
        'workflow_type': 'technical_service',
        'current_status': 'work_in_progress',
        'priority': 'normal',
        'created_at': datetime.now() - timedelta(hours=8),
        'technician_name': 'Bakhtiyor Texnik',
        'description': 'TV kanallar ko\'rinmayapti, signal yo\'q',
        'location': 'Toshkent, Shayxontohur tumani, 12-uy',
        'contact_info': {'phone': '+998901234570'},
        'state_data': {'service_type': 'TV Signal', 'abonent_id': 'AB002'}
    },
    {
        'id': 'REQ005',
        'order_number': 'REQ005',
        'client_name': 'Rustam Alimov',
        'workflow_type': 'call_center_direct',
        'current_status': 'escalated',
        'priority': 'high',
        'created_at': datetime.now() - timedelta(hours=10),
        'technician_name': 'Davron Texnik',
        'description': 'Telefon xizmati bilan bog\'liq muammo, qo\'ng\'iroqlar o\'tmayapti',
        'location': 'Toshkent, Uchtepa tumani, 30-uy',
        'contact_info': {'phone': '+998901234571'},
        'state_data': {}
    },
    {
        'id': 'REQ006',
        'order_number': 'REQ006',
        'client_name': 'Jamshid Karimov',
        'workflow_type': 'technical_service',
        'current_status': 'delayed',
        'priority': 'urgent',
        'created_at': datetime.now() - timedelta(hours=12),
        'technician_name': 'Eldor Texnik',
        'description': 'Internet to\'liq ishlamayapti, tez-tez uziladi',
        'location': 'Toshkent, Zangiota tumani, 45-uy',
        'contact_info': {'phone': '+998901234572'},
        'state_data': {'service_type': 'Connection Issue', 'abonent_id': 'AB003'}
    },
    {
        'id': 'REQ007',
        'order_number': 'REQ007',
        'client_name': 'Malika Abdullayeva',
        'workflow_type': 'connection_request',
        'current_status': 'completed',
        'priority': 'normal',
        'created_at': datetime.now() - timedelta(hours=24),
        'technician_name': 'Ahmad Texnik',
        'description': 'Yangi uy uchun internet xizmati muvaffaqiyatli ulandi',
        'location': 'Toshkent, Chorsu tumani, 18-uy',
        'contact_info': {'phone': '+998901234573'},
        'state_data': {'tariff': 'Standard', 'connection_type': 'B2C'}
    },
    {
        'id': 'REQ008',
        'order_number': 'REQ008',
        'client_name': 'Azamat Toshmatov',
        'workflow_type': 'technical_service',
        'current_status': 'problem',
        'priority': 'high',
        'created_at': datetime.now() - timedelta(hours=36),
        'technician_name': 'Bakhtiyor Texnik',
        'description': 'Kabellar buzilgan, texnik xizmat kerak',
        'location': 'Toshkent, Yunusabad tumani, 22-uy',
        'contact_info': {'phone': '+998901234574'},
        'state_data': {'service_type': 'Cable Repair', 'abonent_id': 'AB004'}
    }
]

# Mock controller dashboard statistics
mock_controller_stats = {
    'pending_assignment': 2,
    'active_work': 3,
    'completed_today': 1,
    'active_technicians': 4
}

# Mock utility classes
class MockAuditLogger:
    """Mock audit logger"""
    async def log_action(self, user_id: int, action: str, details: dict = None, entity_type: str = None, entity_id: str = None, region: str = None):
        """Mock log action"""
        logger.info(f"Mock: User {user_id} performed action: {action}")
        if details:
            logger.info(f"Mock: Details: {details}")

# Initialize mock instances
audit_logger = MockAuditLogger()

# Mock functions
async def get_user_by_telegram_id(region: str, telegram_id: int):
    """Mock get user by telegram ID"""
    logger.info(f"Mock: Getting user by telegram ID {telegram_id} in region {region}")
    return mock_users.get(telegram_id)

async def get_user_region(telegram_id: int):
    """Mock get user region"""
    user = mock_users.get(telegram_id)
    return user.get('region') if user else None

async def get_all_orders(region: str, controller_id: int, limit: int = 50):
    """Get all orders assigned to controller from mock data"""
    try:
        logger.info(f"Mock: Getting all orders for controller {controller_id} in region {region}")
        formatted_orders = []
        for order in mock_controller_orders[:limit]:
            formatted_orders.append({
                'id': order.get('id'),
                'order_number': order.get('order_number', 'N/A'),
                'client_name': order.get('client_name', 'Noma\'lum'),
                'service_type': order.get('workflow_type', 'unknown'),
                'status': order.get('current_status', 'unknown'),
                'priority': order.get('priority', 'normal'),
                'created_at': order.get('created_at'),
                'assigned_to': order.get('technician_name', 'Tayinlanmagan')
            })
        return formatted_orders
    except Exception as e:
        logger.error(f"Error getting all orders: {e}")
        return []

async def get_orders_by_status(region: str, statuses: list):
    """Get orders by status from mock data"""
    try:
        logger.info(f"Mock: Getting orders by statuses {statuses} in region {region}")
        all_orders = []
        for order in mock_controller_orders:
            if order.get('current_status') in statuses:
                all_orders.append({
                    'id': order.get('id'),
                    'order_number': order.get('order_number', 'N/A'),
                    'client_name': order.get('client_name', 'Noma\'lum'),
                    'service_type': order.get('workflow_type', 'unknown'),
                    'status': order.get('current_status', 'unknown'),
                    'priority': order.get('priority', 'normal'),
                    'created_at': order.get('created_at'),
                    'assigned_to': order.get('technician_name', 'Tayinlanmagan')
                })
        return all_orders
    except Exception as e:
        logger.error(f"Error getting orders by status: {e}")
        return []

async def update_order_priority(region: str, order_id: str, priority: str):
    """Update order priority in mock data"""
    try:
        logger.info(f"Mock: Updating order {order_id} priority to {priority} in region {region}")
        
        # Find and update the order
        for order in mock_controller_orders:
            if order['id'] == order_id:
                order['priority'] = priority
                order['updated_at'] = datetime.now()
                return True
        return False
    except Exception as e:
        logger.error(f"Error updating order priority: {e}")
        return False

async def get_unresolved_issues(region: str, controller_id: int):
    """Get unresolved issues from mock data"""
    try:
        logger.info(f"Mock: Getting unresolved issues for controller {controller_id} in region {region}")
        unresolved = []
        
        for order in mock_controller_orders:
            # Check if order has issues (e.g., delayed, escalated, etc.)
            if order.get('current_status') in ['escalated', 'delayed', 'problem']:
                unresolved.append({
                    'id': order.get('id'),
                    'order_number': order.get('order_number'),
                    'client_name': order.get('client_name', 'Noma\'lum'),
                    'issue_type': order.get('workflow_type', 'unknown'),
                    'description': order.get('description', 'Tavsif yo\'q'),
                    'priority': order.get('priority', 'normal'),
                    'created_at': order.get('created_at')
                })
        
        return unresolved
    except Exception as e:
        logger.error(f"Error getting unresolved issues: {e}")
        return []

async def get_single_order_details(region: str, order_id: str):
    """Get single order details from mock data"""
    try:
        logger.info(f"Mock: Getting single order details for {order_id} in region {region}")
        
        for order in mock_controller_orders:
            if order['id'] == order_id:
                return {
                    'id': order.get('id'),
                    'order_number': order.get('order_number'),
                    'client_name': order.get('client_name', 'Noma\'lum'),
                    'client_phone': order.get('contact_info', {}).get('phone', 'N/A'),
                    'service_type': order.get('workflow_type', 'unknown'),
                    'status': order.get('current_status', 'unknown'),
                    'priority': order.get('priority', 'normal'),
                    'created_at': order.get('created_at'),
                    'updated_at': order.get('updated_at'),
                    'assigned_to': order.get('technician_name', 'Tayinlanmagan'),
                    'description': order.get('description', 'Tavsif yo\'q'),
                    'location': order.get('location', 'Manzil ko\'rsatilmagan'),
                    'state_data': order.get('state_data', {})
                }
        return None
    except Exception as e:
        logger.error(f"Error getting single order details: {e}")
        return None

async def get_controller_dashboard_stats(region: str):
    """Mock get controller dashboard statistics"""
    logger.info(f"Mock: Getting controller dashboard stats for region {region}")
    return mock_controller_stats

def orders_control_menu(lang: str):
    """Create orders control menu"""
    if lang == 'uz':
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🆕 Yangi buyurtmalar", callback_data="new_orders"),
                InlineKeyboardButton(text="⏳ Kutilayotgan", callback_data="pending_orders")
            ],
            [
                InlineKeyboardButton(text="🔴 Muammoli buyurtmalar", callback_data="problem_orders"),
                InlineKeyboardButton(text="📊 Buyurtmalar hisoboti", callback_data="orders_report")
            ],
            [
                InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_controllers")
            ]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🆕 Новые заказы", callback_data="new_orders"),
                InlineKeyboardButton(text="⏳ В ожидании", callback_data="pending_orders")
            ],
            [
                InlineKeyboardButton(text="🔴 Проблемные заказы", callback_data="problem_orders"),
                InlineKeyboardButton(text="📊 Отчет по заказам", callback_data="orders_report")
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_controllers")
            ]
        ])

def order_priority_keyboard(order_id: str, lang: str = 'uz'):
    """Create order priority keyboard"""
    if lang == 'uz':
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🟢 Past", callback_data=f"priority_low_{order_id}"),
                InlineKeyboardButton(text="🟡 O'rta", callback_data=f"priority_medium_{order_id}")
            ],
            [
                InlineKeyboardButton(text="🟠 Yuqori", callback_data=f"priority_high_{order_id}"),
                InlineKeyboardButton(text="🔴 Shoshilinch", callback_data=f"priority_urgent_{order_id}")
            ],
            [
                InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_orders")
            ]
        ])
    else:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🟢 Низкий", callback_data=f"priority_low_{order_id}"),
                InlineKeyboardButton(text="🟡 Средний", callback_data=f"priority_medium_{order_id}")
            ],
            [
                InlineKeyboardButton(text="🟠 Высокий", callback_data=f"priority_high_{order_id}"),
                InlineKeyboardButton(text="🔴 Срочный", callback_data=f"priority_urgent_{order_id}")
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_orders")
            ]
        ])

def back_to_controllers_menu():
    """Create back to controllers menu"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_controllers")]
    ])

class ControllerOrdersStates:
    orders_control = "orders_control"
    viewing_orders = "viewing_orders"
    order_details = "order_details"

def get_controller_orders_router():
    """Get controller orders router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📋 Arizalarni ko'rish", "📋 Просмотр заявок"]))
    async def orders_control_menu_handler(message: Message, state: FSMContext):
        """Handle orders control menu"""
        user_id = message.from_user.id
        
        try:
            # Get user region
            region = await get_user_region(user_id)
            if not region:
                await message.answer("❌ Region aniqlanmadi")
                return
            
            user = await get_user_by_telegram_id(region, user_id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Get orders statistics from mock data
            stats = await get_controller_dashboard_stats(region)
            all_orders = await get_all_orders(region, controller_id)
            
            # Log action
            await audit_logger.log_action(
                user_id=user_id,
                action='CONTROLLER_ACTION',
                details={'action': 'viewed_orders_menu'},
                region=region
            )
            
            if lang == 'uz':
                orders_text = (
                    "📋 <b>Buyurtmalar nazorati</b>\n\n"
                    f"📊 <b>Statistika:</b>\n"
                    f"• Jami buyurtmalar: {len(all_orders)}\n"
                    f"• Yangi: {stats.get('pending_assignment', 0)}\n"
                    f"• Jarayonda: {stats.get('active_work', 0)}\n"
                    f"• Bajarilgan (bugun): {stats.get('completed_today', 0)}\n\n"
                    "Quyidagi bo'limlardan birini tanlang:"
                )
            else:
                orders_text = (
                    "📋 <b>Контроль заказов</b>\n\n"
                    f"📊 <b>Статистика:</b>\n"
                    f"• Всего заказов: {len(all_orders)}\n"
                    f"• Новые: {stats.get('pending_assignment', 0)}\n"
                    f"• В процессе: {stats.get('active_work', 0)}\n"
                    f"• Выполнено (сегодня): {stats.get('completed_today', 0)}\n\n"
                    "Выберите один из разделов:"
                )
            
            await message.answer(
                orders_text,
                reply_markup=orders_control_menu(lang),
                parse_mode='HTML'
            )
            await state.set_state(ControllerOrdersStates.orders_control)
            
        except Exception as e:
            logger.error(f"Error in orders_control_menu_handler: {e}")
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "new_orders")
    async def new_orders_handler(callback: CallbackQuery, state: FSMContext):
        """Handle new orders"""
        try:
            await callback.answer()
            
            # Get user region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Get new orders from mock data
            new_orders = await get_orders_by_status(region, ['created', 'pending_assignment'])
            
            if not new_orders:
                if lang == 'uz':
                    text = "🆕 <b>Yangi buyurtmalar</b>\n\nHozircha yangi buyurtmalar yo'q."
                else:
                    text = "🆕 <b>Новые заказы</b>\n\nПока нет новых заказов."
            else:
                if lang == 'uz':
                    text = "🆕 <b>Yangi buyurtmalar</b>\n\n"
                else:
                    text = "🆕 <b>Новые заказы</b>\n\n"
                
                for i, order in enumerate(new_orders[:10], 1):
                    created_at = order.get('created_at')
                    if isinstance(created_at, datetime):
                        created_at = created_at.strftime('%Y-%m-%d %H:%M')
                    
                    text += (
                        f"{i}. 📦 <b>#{order['order_number']}</b>\n"
                        f"   👤 {order['client_name']}\n"
                        f"   📌 {order['service_type']}\n"
                        f"   🕐 {created_at}\n\n"
                    )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Yangilash" if lang == 'uz' else "🔄 Обновить", callback_data="refresh_new_orders")],
                [InlineKeyboardButton(text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад", callback_data="back_to_orders_menu")]
            ])
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in new_orders_handler: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "pending_orders")
    async def pending_orders_handler(callback: CallbackQuery, state: FSMContext):
        """Handle pending orders"""
        try:
            await callback.answer()
            
            # Get user region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Get pending orders from mock data
            pending_orders = await get_orders_by_status(region, ['assigned_to_technician', 'work_in_progress'])
            
            if not pending_orders:
                if lang == 'uz':
                    text = "⏳ <b>Kutilayotgan buyurtmalar</b>\n\nHozircha kutilayotgan buyurtmalar yo'q."
                else:
                    text = "⏳ <b>Ожидающие заказы</b>\n\nПока нет ожидающих заказов."
            else:
                if lang == 'uz':
                    text = "⏳ <b>Kutilayotgan buyurtmalar</b>\n\n"
                else:
                    text = "⏳ <b>Ожидающие заказы</b>\n\n"
                
                for i, order in enumerate(pending_orders[:10], 1):
                    priority_emoji = '🔴' if order['priority'] == 'urgent' else '🟡' if order['priority'] == 'high' else '🟢'
                    text += (
                        f"{i}. {priority_emoji} <b>#{order['order_number']}</b>\n"
                        f"   👤 {order['client_name']}\n"
                        f"   📌 Status: {order['status']}\n"
                        f"   👷 {order.get('assigned_to', 'Tayinlanmagan')}\n\n"
                    )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Yangilash" if lang == 'uz' else "🔄 Обновить", callback_data="refresh_pending_orders")],
                [InlineKeyboardButton(text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад", callback_data="back_to_orders_menu")]
            ])
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in pending_orders_handler: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "problem_orders")
    async def problem_orders_handler(callback: CallbackQuery, state: FSMContext):
        """Handle problem orders"""
        try:
            await callback.answer()
            
            # Get user region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Get unresolved issues from mock data
            problem_orders = await get_unresolved_issues(region, controller_id)
            
            if not problem_orders:
                if lang == 'uz':
                    text = "🔴 <b>Muammoli buyurtmalar</b>\n\nHozircha muammoli buyurtmalar yo'q. ✅"
                else:
                    text = "🔴 <b>Проблемные заказы</b>\n\nПока нет проблемных заказов. ✅"
            else:
                if lang == 'uz':
                    text = "🔴 <b>Muammoli buyurtmalar</b>\n\n"
                else:
                    text = "🔴 <b>Проблемные заказы</b>\n\n"
                
                for i, order in enumerate(problem_orders[:10], 1):
                    text += (
                        f"{i}. ⚠️ <b>#{order['order_number']}</b>\n"
                        f"   👤 {order['client_name']}\n"
                        f"   ❗ {order['issue_type']}\n"
                        f"   📝 {order['description'][:50]}...\n\n"
                    )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Yangilash" if lang == 'uz' else "🔄 Обновить", callback_data="refresh_problem_orders")],
                [InlineKeyboardButton(text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад", callback_data="back_to_orders_menu")]
            ])
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in problem_orders_handler: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "orders_report")
    async def orders_report_handler(callback: CallbackQuery, state: FSMContext):
        """Handle orders report"""
        try:
            await callback.answer()
            
            # Get user region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get comprehensive statistics from mock data
            stats = await get_controller_dashboard_stats(region)
            
            # Log action
            await audit_logger.log_action(
                user_id=callback.from_user.id,
                action='CONTROLLER_ACTION',
                details={'action': 'viewed_orders_report'},
                region=region
            )
            
            if lang == 'uz':
                report_text = (
                    "📊 <b>Buyurtmalar hisoboti</b>\n\n"
                    "📈 <b>Umumiy ko'rsatkichlar:</b>\n"
                    f"• Tayinlash kutilmoqda: {stats.get('pending_assignment', 0)}\n"
                    f"• Faol ishlar: {stats.get('active_work', 0)}\n"
                    f"• Bugun bajarilgan: {stats.get('completed_today', 0)}\n"
                    f"• Faol texniklar: {stats.get('active_technicians', 0)}\n\n"
                    "💡 <b>Tahlil:</b>\n"
                    f"• Samaradorlik: {'Yaxshi' if stats.get('completed_today', 0) > 10 else 'O\'rtacha'}\n"
                    f"• Yuklanish: {'Yuqori' if stats.get('active_work', 0) > 20 else 'Normal'}\n"
                )
            else:
                report_text = (
                    "📊 <b>Отчет по заказам</b>\n\n"
                    "📈 <b>Общие показатели:</b>\n"
                    f"• Ожидает назначения: {stats.get('pending_assignment', 0)}\n"
                    f"• Активные работы: {stats.get('active_work', 0)}\n"
                    f"• Выполнено сегодня: {stats.get('completed_today', 0)}\n"
                    f"• Активные техники: {stats.get('active_technicians', 0)}\n\n"
                    "💡 <b>Анализ:</b>\n"
                    f"• Эффективность: {'Хорошая' if stats.get('completed_today', 0) > 10 else 'Средняя'}\n"
                    f"• Загрузка: {'Высокая' if stats.get('active_work', 0) > 20 else 'Нормальная'}\n"
                )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📤 Export" if lang == 'uz' else "📤 Экспорт", callback_data="export_orders_report")],
                [InlineKeyboardButton(text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад", callback_data="back_to_orders_menu")]
            ])
            
            await callback.message.edit_text(report_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in orders_report_handler: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("priority_"))
    async def change_priority_handler(callback: CallbackQuery, state: FSMContext):
        """Handle priority change"""
        try:
            await callback.answer()
            
            # Parse priority and order ID
            parts = callback.data.split('_')
            priority = parts[1]  # low, medium, high, urgent
            order_id = '_'.join(parts[2:])  # Handle complex order IDs
            
            # Get user region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Update priority in mock data
            success = await update_order_priority(region, order_id, priority)
            
            if success:
                # Log action
                await audit_logger.log_action(
                    user_id=callback.from_user.id,
                    action='DATA_UPDATED',
                    details={
                        'order_id': order_id,
                        'field': 'priority',
                        'new_value': priority
                    },
                    entity_type='service_request',
                    entity_id=order_id,
                    region=region
                )
                
                if lang == 'uz':
                    await callback.answer("✅ Buyurtma ustuvorligi o'zgartirildi", show_alert=True)
                else:
                    await callback.answer("✅ Приоритет заказа изменен", show_alert=True)
            else:
                if lang == 'uz':
                    await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
                else:
                    await callback.answer("❌ Произошла ошибка", show_alert=True)
            
            # Return to orders menu
            await back_to_orders_menu_handler(callback, state)
            
        except Exception as e:
            logger.error(f"Error in change_priority_handler: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_orders_menu")
    async def back_to_orders_menu_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to orders menu"""
        try:
            await callback.answer()
            
            # Get user region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Get updated statistics
            stats = await get_controller_dashboard_stats(region)
            all_orders = await get_all_orders(region, controller_id)
            
            if lang == 'uz':
                orders_text = (
                    "📋 <b>Buyurtmalar nazorati</b>\n\n"
                    f"📊 <b>Statistika:</b>\n"
                    f"• Jami buyurtmalar: {len(all_orders)}\n"
                    f"• Yangi: {stats.get('pending_assignment', 0)}\n"
                    f"• Jarayonda: {stats.get('active_work', 0)}\n"
                    f"• Bajarilgan (bugun): {stats.get('completed_today', 0)}\n\n"
                    "Quyidagi bo'limlardan birini tanlang:"
                )
            else:
                orders_text = (
                    "📋 <b>Контроль заказов</b>\n\n"
                    f"📊 <b>Статистика:</b>\n"
                    f"• Всего заказов: {len(all_orders)}\n"
                    f"• Новые: {stats.get('pending_assignment', 0)}\n"
                    f"• В процессе: {stats.get('active_work', 0)}\n"
                    f"• Выполнено (сегодня): {stats.get('completed_today', 0)}\n\n"
                    "Выберите один из разделов:"
                )
            
            await callback.message.edit_text(
                orders_text,
                reply_markup=orders_control_menu(lang),
                parse_mode='HTML'
            )
            
        except Exception as e:
            logger.error(f"Error in back_to_orders_menu_handler: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("refresh_"))
    async def refresh_orders_handler(callback: CallbackQuery, state: FSMContext):
        """Handle refresh orders"""
        try:
            await callback.answer("🔄 Yangilanmoqda...")
            
            # Determine which type to refresh
            order_type = callback.data.replace("refresh_", "")
            
            # Call appropriate handler based on type
            if order_type == "new_orders":
                await new_orders_handler(callback, state)
            elif order_type == "pending_orders":
                await pending_orders_handler(callback, state)
            elif order_type == "problem_orders":
                await problem_orders_handler(callback, state)
            
        except Exception as e:
            logger.error(f"Error in refresh_orders_handler: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router
