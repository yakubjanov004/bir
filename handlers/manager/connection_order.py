"""
Manager Connection Order Handler - Mock Data Implementation

Bu modul manager uchun mijozlarni qidirish va ulanish arizasi yaratish funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
import logging
import json

from filters.role_filter import RoleFilter
from states.manager_states import ManagerClientSearchStates, ManagerConnectionOrderStates
from keyboards.manager_buttons import get_manager_client_search_keyboard, get_manager_confirmation_keyboard
from keyboards.controllers_buttons import (
    get_controller_regions_keyboard,
    controller_zayavka_type_keyboard,
    controller_geolocation_keyboard,
    get_controller_tariff_selection_keyboard,
)

logger = logging.getLogger(__name__)

# Mock data storage
mock_clients = [
    {
        'id': 1001,
        'full_name': 'Aziz Karimov',
        'phone': '+998901234567',
        'role': 'client',
        'language': 'uz',
        'region': 'toshkent',
        'address': 'Chorsu tumani, 15-uy'
    },
    {
        'id': 1002,
        'full_name': 'Malika Toshmatova',
        'phone': '+998901234568',
        'role': 'client',
        'language': 'uz',
        'region': 'toshkent',
        'address': 'Yunusabad tumani, 25-uy'
    },
    {
        'id': 1003,
        'full_name': 'Jahongir Azimov',
        'phone': '+998901234569',
        'role': 'client',
        'language': 'uz',
        'region': 'toshkent',
        'address': 'Sergeli tumani, 8-uy'
    },
    {
        'id': 1004,
        'full_name': 'Umar Toshmatov',
        'phone': '+998901234570',
        'role': 'client',
        'language': 'uz',
        'region': 'toshkent',
        'address': 'Chilanzor tumani, 30-uy'
    },
    {
        'id': 1005,
        'full_name': 'Dilfuza Karimova',
        'phone': '+998901234571',
        'role': 'client',
        'language': 'uz',
        'region': 'toshkent',
        'address': 'Mirabad tumani, 42-uy'
    }
]

mock_users = {
    1: {
        'id': 1,
        'telegram_id': 123456789,
        'role': 'manager',
        'language': 'uz',
        'full_name': 'Test Manager',
        'phone_number': '+998901234567'
    }
}

mock_service_requests = []

# Mock functions
async def get_user_by_telegram_id(region: str, user_id: int):
    """Mock get user by telegram ID"""
    for user in mock_users.values():
        if user.get('telegram_id') == user_id:
            return user
    return None

async def get_user_by_phone(region: str, phone: str):
    """Mock get user by phone"""
    for client in mock_clients:
        if client.get('phone') == phone:
            return client
    return None

async def search_users(region: str, search_term: str):
    """Mock search users"""
    results = []
    search_term_lower = search_term.lower()
    
    for client in mock_clients:
        if (search_term_lower in client.get('full_name', '').lower() or
            search_term_lower in client.get('phone', '').lower()):
            results.append(client)
    
    return results

async def create_or_update_user(region: str, user_data: dict):
    """Mock create or update user"""
    # Generate new ID
    new_id = max([c['id'] for c in mock_clients]) + 1 if mock_clients else 1001
    
    new_user = {
        'id': new_id,
        'full_name': user_data.get('full_name'),
        'phone': user_data.get('phone'),
        'role': user_data.get('role', 'client'),
        'language': user_data.get('language', 'uz'),
        'region': region,
        'address': user_data.get('address', '')
    }
    
    mock_clients.append(new_user)
    return new_id

async def get_user(region: str, user_id: int):
    """Mock get user by ID"""
    for client in mock_clients:
        if client.get('id') == user_id:
            return client
    return None

async def create_service_request(region: str, request_data: dict):
    """Mock create service request"""
    # Generate new request ID
    request_id = f"req_{len(mock_service_requests) + 1:03d}_{datetime.now().strftime('%Y%m%d_%H%M')}"
    
    # Add request to mock storage
    mock_service_requests.append({
        'id': request_id,
        'region': region,
        **request_data,
        'created_at': datetime.now()
    })
    
    return request_id

# Mock utility classes
class MockApplicationTracker:
    """Mock application tracker"""
    async def get_statistics(self):
        """Mock get statistics"""
        return {
            'total': len(mock_service_requests),
            'completed': 0,
            'completion_rate': 0,
            'avg_rating': 0
        }

class MockAuditLogger:
    """Mock audit logger"""
    async def log_manager_action(self, manager_id: int, action: str, target_type: str = None, target_id: str = None, details: dict = None):
        """Mock log manager action"""
        logger.info(f"Mock: Manager {manager_id} performed action: {action}")
        if target_type and target_id:
            logger.info(f"Mock: Target: {target_type} {target_id}")
        if details:
            logger.info(f"Mock: Details: {details}")

class MockNotificationSystem:
    """Mock notification system"""
    async def send_notification(self, user_id: int, message: str, notification_type: str = 'info'):
        """Mock send notification"""
        logger.info(f"Mock: Notification sent to user {user_id}: {message}")

# Initialize mock instances
application_tracker = MockApplicationTracker()
audit_logger = MockAuditLogger()
notification_system = MockNotificationSystem()

# Search functions using mock data (Manager mijoz qidiradi)
async def search_clients_by_phone(phone: str, region: str = 'toshkent'):
    """Telefon bo'yicha mijozlarni qidirish"""
    try:
        # Avval aniq moslikni qidiramiz
        user = await get_user_by_phone(region, phone)
        if user:
            return [user]
        
        # Qisman qidiruv
        users = await search_users(region, phone)
        return users[:5] if users else []
    except Exception as e:
        logger.error(f"Error searching by phone: {e}")
        return []

async def search_clients_by_name(name: str, region: str = 'toshkent'):
    """Ism bo'yicha mijozlarni qidirish"""
    try:
        users = await search_users(region, name)
        return users[:5] if users else []
    except Exception as e:
        logger.error(f"Error searching by name: {e}")
        return []

async def search_client_by_id(client_id: int, region: str = 'toshkent'):
    """ID bo'yicha mijozni topish"""
    try:
        user = await get_user(region, client_id)
        return [user] if user else []
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return []

# Tariff calculations
def calculate_connection_cost(connection_type: str, tariff: str) -> dict:
    """Calculate connection cost based on type and tariff"""
    costs = {
        'internet': {
            'standard': {'setup': 150000, 'monthly': 89000, 'equipment': 250000},
            'new': {'setup': 100000, 'monthly': 129000, 'equipment': 350000}
        },
        'tv': {
            'standard': {'setup': 100000, 'monthly': 45000, 'equipment': 180000},
            'new': {'setup': 80000, 'monthly': 65000, 'equipment': 220000}
        },
        'combo': {
            'standard': {'setup': 200000, 'monthly': 119000, 'equipment': 400000},
            'new': {'setup': 150000, 'monthly': 169000, 'equipment': 500000}
        }
    }
    
    connection_type = connection_type.lower()
    tariff = tariff.lower()
    
    if connection_type in costs and tariff in costs[connection_type]:
        cost_data = costs[connection_type][tariff]
        total = cost_data['setup'] + cost_data['equipment']
        return {
            'setup_fee': cost_data['setup'],
            'monthly_fee': cost_data['monthly'],
            'equipment_fee': cost_data['equipment'],
            'total_initial': total,
            'currency': 'UZS'
        }
    
    # Default costs
    return {
        'setup_fee': 100000,
        'monthly_fee': 89000,
        'equipment_fee': 200000,
        'total_initial': 300000,
        'currency': 'UZS'
    }

def get_manager_connection_order_router():
    router = Router()

    # Role guard - both manager and junior_manager can access
    role_filter = RoleFilter(["manager", "junior_manager"])
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    # 1) Entry: client search method
    @router.message(F.text == "🔌 Ulanish arizasi yaratish")
    async def start_connection_order(message: Message, state: FSMContext):
        await state.update_data(current_flow='connection')
        await message.answer(
            "Mijozni qanday qidiramiz?",
            reply_markup=get_manager_client_search_keyboard('uz')
        )
        await state.set_state(ManagerClientSearchStates.selecting_client_search_method)

    # 2) Search flow
    @router.callback_query(F.data == "mgr_search_phone", StateFilter(ManagerClientSearchStates.selecting_client_search_method))
    async def search_by_phone(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ManagerClientSearchStates.entering_phone)
        await callback.message.edit_text("📱 Telefon raqamini kiriting:\nMasalan: +998901234567")

    @router.callback_query(F.data == "mgr_search_name", StateFilter(ManagerClientSearchStates.selecting_client_search_method))
    async def search_by_name(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ManagerClientSearchStates.entering_name)
        await callback.message.edit_text("👤 Mijoz ismini kiriting:\nMasalan: Alisher Karimov")

    @router.callback_query(F.data == "mgr_search_id", StateFilter(ManagerClientSearchStates.selecting_client_search_method))
    async def search_by_id(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ManagerClientSearchStates.entering_client_id)
        await callback.message.edit_text("🆔 Mijoz ID sini kiriting:\nMasalan: 12345")

    @router.callback_query(F.data == "mgr_search_new", StateFilter(ManagerClientSearchStates.selecting_client_search_method))
    async def create_new_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ManagerClientSearchStates.entering_new_client_name)
        await callback.message.edit_text("➕ Yangi mijoz nomini kiriting:")

    @router.callback_query(F.data == "mgr_cancel_creation")
    async def cancel_creation(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.edit_text("❌ Zayavka yaratish bekor qilindi")
        await callback.answer()

    @router.message(StateFilter(ManagerClientSearchStates.entering_phone))
    async def process_phone_search(message: Message, state: FSMContext):
        phone = message.text.strip()
        # Use hardcoded values for now
        region = 'toshkent'
        
        # Agar yangi mijoz yaratayotgan bo'lsak
        if data.get('creating_new'):
            new_client_name = data.get('new_client_name')
            # Yangi mijozni yaratamiz
            user_data = {
                'full_name': new_client_name,
                'phone': phone,
                'role': 'client',
                'language': 'uz'
            }
            user_id = await create_or_update_user(region, user_data)
            
            if user_id:
                new_client = await get_user(region, user_id)
                if new_client:
                    await message.answer(f"✅ Yangi mijoz yaratildi: {new_client_name}")
                    await _show_clients_list(message, state, [new_client])
                else:
                    await message.answer("❌ Mijoz yaratishda xatolik")
            else:
                await message.answer("❌ Mijoz yaratishda xatolik")
            
            await state.update_data(creating_new=False)
        else:
            # Oddiy qidiruv
            clients = await search_clients_by_phone(phone, region)
            
            # Log search action using mock audit logger
            await audit_logger.log_manager_action(
                manager_id=message.from_user.id,
                action='search_client_by_phone',
                details={'phone': phone, 'results': len(clients)}
            )
            
            await _show_clients_list(message, state, clients)

    @router.message(StateFilter(ManagerClientSearchStates.entering_name))
    async def process_name_search(message: Message, state: FSMContext):
        name = message.text.strip()
        # Use hardcoded values for now
        region = 'toshkent'
        
        clients = await search_clients_by_name(name, region)
        
        # Log search action using mock audit logger
        await audit_logger.log_manager_action(
            manager_id=message.from_user.id,
            action='search_client_by_name',
            details={'name': name, 'results': len(clients)}
        )
        
        await _show_clients_list(message, state, clients)

    @router.message(StateFilter(ManagerClientSearchStates.entering_client_id))
    async def process_id_search(message: Message, state: FSMContext):
        client_id = message.text.strip()
        if not client_id.isdigit():
            await message.answer("❌ ID faqat raqamlardan iborat bo'lishi kerak")
            return
        
        # Get region from state or use default
        data = await state.get_data()
        region = data.get('active_region') or data.get('region', 'toshkent')
        
        clients = await search_client_by_id(int(client_id), region)
        
        # Log search action using mock audit logger
        await audit_logger.log_manager_action(
            manager_id=message.from_user.id,
            action='search_client_by_id',
            details={'client_id': client_id, 'found': len(clients) > 0}
        )
        
        await _show_clients_list(message, state, clients)

    @router.message(StateFilter(ManagerClientSearchStates.entering_new_client_name))
    async def process_new_client(message: Message, state: FSMContext):
        full_name = message.text.strip()
        
        # Yangi mijoz yaratish o'rniga, ism bo'yicha qidiramiz
        data = await state.get_data()
        region = data.get('active_region') or data.get('region', 'toshkent')
        
        clients = await search_clients_by_name(full_name, region)
        
        if not clients:
            # Agar topilmasa, yangi mijoz yaratish uchun ma'lumot so'raymiz
            await message.answer(
                "❌ Bunday mijoz topilmadi.\n\n"
                "Yangi mijoz yaratish uchun to'liq ma'lumot kerak.\n"
                "📱 Telefon raqamini kiriting:"
            )
            await state.update_data(new_client_name=full_name, creating_new=True)
            await state.set_state(ManagerClientSearchStates.entering_phone)
        else:
            # Topilgan mijozlarni ko'rsatamiz
            await _show_clients_list(message, state, clients)

    async def _show_clients_list(message: Message, state: FSMContext, clients):
        if not clients:
            await message.answer("Mijoz topilmadi. Qayta urinib ko'ring.")
            await state.set_state(ManagerClientSearchStates.selecting_client_search_method)
            await message.answer("Qidirish usulini tanlang:", reply_markup=get_manager_client_search_keyboard('uz'))
            return
        await state.update_data(found_clients=clients)
        await state.set_state(ManagerClientSearchStates.selecting_client)

        rows = []
        for i, c in enumerate(clients[:5]):
            rows.append([InlineKeyboardButton(text=f"{c['full_name']} - {c.get('phone','N/A')}", callback_data=f"mgr_select_client_{i}")])
        rows.append([InlineKeyboardButton(text="🔍 Boshqa qidirish", callback_data="mgr_search_again")])
        rows.append([InlineKeyboardButton(text="❌ Bekor qilish", callback_data="mgr_cancel_creation")])
        kb = InlineKeyboardMarkup(inline_keyboard=rows)
        await message.answer("Mijozni tanlang:", reply_markup=kb)

    @router.callback_query(lambda c: c.data.startswith("mgr_select_client_"), StateFilter(ManagerClientSearchStates.selecting_client))
    async def select_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        clients = data.get('found_clients', [])
        idx = int(callback.data.split('_')[-1])
        if idx >= len(clients):
            await callback.answer("Xato", show_alert=True)
            return
        await state.update_data(selected_client=clients[idx])
        await callback.message.edit_text("Hududni tanlang:")
        await callback.message.answer("Hududni tanlang:", reply_markup=get_controller_regions_keyboard('uz'))
        await state.set_state(ManagerConnectionOrderStates.selecting_region)

    @router.callback_query(F.data == "mgr_search_again")
    async def search_again(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ManagerClientSearchStates.selecting_client_search_method)
        await callback.message.edit_text("Qidirish usulini tanlang:")
        await callback.message.answer("Qidirish usulini tanlang:", reply_markup=get_manager_client_search_keyboard('uz'))

    # 3) Connection order flow (after client selected)
    @router.callback_query(F.data.startswith("ctrl_region_"), StateFilter(ManagerConnectionOrderStates.selecting_region))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        region = callback.data.replace("ctrl_region_", "")
        await state.update_data(region=region)
        await callback.message.answer("Ulanish turini tanlang:", reply_markup=controller_zayavka_type_keyboard('uz'))
        await state.set_state(ManagerConnectionOrderStates.selecting_connection_type)

    @router.callback_query(F.data.startswith("ctrl_zayavka_type_"), StateFilter(ManagerConnectionOrderStates.selecting_connection_type))
    async def select_connection_type(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        connection_type = callback.data.replace("ctrl_zayavka_type_", "")
        await state.update_data(connection_type=connection_type)
        await callback.message.answer("Tariflardan birini tanlang:", reply_markup=get_controller_tariff_selection_keyboard('uz'))
        await state.set_state(ManagerConnectionOrderStates.selecting_tariff)

    @router.callback_query(F.data.in_(["ctrl_tariff_standard", "ctrl_tariff_new"]), StateFilter(ManagerConnectionOrderStates.selecting_tariff))
    async def select_tariff(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        tariff = "Standard" if callback.data == "ctrl_tariff_standard" else "Yangi"
        await state.update_data(selected_tariff=tariff)
        await callback.message.answer("Manzilingizni kiriting:")
        await state.set_state(ManagerConnectionOrderStates.entering_address)

    @router.message(StateFilter(ManagerConnectionOrderStates.entering_address))
    async def get_connection_address(message: Message, state: FSMContext):
        await state.update_data(address=message.text)
        await message.answer("Geolokatsiya yuborasizmi?", reply_markup=controller_geolocation_keyboard('uz'))
        await state.set_state(ManagerConnectionOrderStates.asking_for_geo)

    @router.callback_query(F.data.in_(["ctrl_send_location_yes", "ctrl_send_location_no"]), StateFilter(ManagerConnectionOrderStates.asking_for_geo))
    async def ask_for_geo(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        if callback.data == "ctrl_send_location_yes":
            await callback.message.answer("Geolokatsiyani yuboring:")
            await state.set_state(ManagerConnectionOrderStates.waiting_for_geo)
        else:
            await show_connection_confirmation(callback, state, geo=None)

    @router.message(StateFilter(ManagerConnectionOrderStates.waiting_for_geo), F.location)
    async def get_geo(message: Message, state: FSMContext):
        await state.update_data(geo=message.location)
        await show_connection_confirmation(message, state, geo=message.location)

    async def show_connection_confirmation(message_or_callback, state: FSMContext, geo=None):
        data = await state.get_data()
        selected_client = data.get('selected_client', {})
        region = data.get('region', '-')
        connection_type = data.get('connection_type', '-')
        tariff = data.get('selected_tariff', '-')
        address = data.get('address', '-')
        
        # Calculate costs
        costs = calculate_connection_cost(connection_type, tariff)
        
        # Format costs for display
        def format_sum(amount):
            return f"{amount:,}".replace(',', ' ')

        text = (
            f"👤 <b>Mijoz:</b> {selected_client.get('full_name','N/A')}\n"
            f"📱 <b>Telefon:</b> {selected_client.get('phone','N/A')}\n"
            f"🏛️ <b>Hudud:</b> {region}\n"
            f"🔌 <b>Ulanish turi:</b> {connection_type}\n"
            f"💳 <b>Tarif:</b> {tariff}\n"
            f"🏠 <b>Manzil:</b> {address}\n"
            f"\n💰 <b>Hisob-kitob:</b>\n"
            f"├ O'rnatish: {format_sum(costs['setup_fee'])} so'm\n"
            f"├ Uskunalar: {format_sum(costs['equipment_fee'])} so'm\n"
            f"├ Oylik to'lov: {format_sum(costs['monthly_fee'])} so'm\n"
            f"└ <b>Jami boshlang'ich:</b> {format_sum(costs['total_initial'])} so'm\n"
            f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}"
        )

        if hasattr(message_or_callback, 'message'):
            await message_or_callback.message.answer(text, parse_mode='HTML', reply_markup=get_manager_confirmation_keyboard('uz'))
        else:
            await message_or_callback.answer(text, parse_mode='HTML', reply_markup=get_manager_confirmation_keyboard('uz'))
        await state.set_state(ManagerConnectionOrderStates.confirming_connection)

    @router.callback_query(F.data == "mgr_confirm_zayavka", StateFilter(ManagerConnectionOrderStates.confirming_connection))
    async def confirm_connection_order(callback: CallbackQuery, state: FSMContext):
        try:
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
            
            data = await state.get_data()
            selected_client = data.get('selected_client', {})
            region = data.get('active_region') or data.get('region', 'toshkent')
            connection_type = data.get('connection_type', 'internet')
            tariff = data.get('selected_tariff', 'standard')
            address = data.get('address', '')
            geo = data.get('geo')
            
            # Calculate costs
            costs = calculate_connection_cost(connection_type, tariff)
            
            # Get manager info using mock function
            manager = await get_user_by_telegram_id(region, callback.from_user.id)
            manager_id = manager.get('id') if manager else None
            
            # Prepare request data - MIJOZ NOMIDAN yaratiladi
            request_data = {
                'workflow_type': 'connection_request',
                'client_id': selected_client.get('id'),  # Mijoz ID
                'role_current': 'call_center',  # Call center'ga yuboriladi (client yaratgandek)
                'current_status': 'created',
                'priority': 'medium',
                'description': f"Ulanish arizasi: {connection_type} - {tariff}",
                'location': address,
                'contact_info': json.dumps({
                    'full_name': selected_client.get('full_name'),
                    'phone': selected_client.get('phone'),
                    'address': address
                }),
                'state_data': json.dumps({
                    'connection_type': connection_type,
                    'tariff': tariff,
                    'costs': costs,
                    'region': region,
                    'geo': {
                        'lat': geo.latitude if geo else None,
                        'lon': geo.longitude if geo else None
                    } if geo else None,
                    'created_via': 'manager_assistance',  # Manager yordam bergani belgilanadi
                    'assisted_by': manager_id
                }),
                'created_by_staff': True,  # Staff yaratgan
                'staff_creator_id': manager_id,  # Kim yaratgan
                'staff_creator_role': 'manager',
                'creation_source': 'client'  # Lekin mijoz nomidan
            }
            
            # Create service request using mock function
            request_id = await create_service_request(region, request_data)
            
            if request_id:
                # Log action using mock audit logger
                await audit_logger.log_manager_action(
                    manager_id=manager_id or callback.from_user.id,
                    action='create_connection_order',
                    target_type='service_request',
                    target_id=request_id,
                    details={
                        'client_id': selected_client.get('id'),
                        'connection_type': connection_type,
                        'tariff': tariff,
                        'total_cost': costs['total_initial']
                    }
                )
                
                await callback.answer("✅ Zayavka yaratildi!", show_alert=True)
                
                # Format success message with costs
                def format_sum(amount):
                    return f"{amount:,}".replace(',', ' ')
                
                success_msg = (
                    f"✅ <b>Mijoz nomidan ulanish arizasi yaratildi!</b>\n\n"
                    f"📋 <b>Ariza raqami:</b> <code>{request_id}</code>\n"
                    f"👤 <b>Mijoz:</b> {selected_client.get('full_name','N/A')}\n"
                    f"📱 <b>Telefon:</b> {selected_client.get('phone','N/A')}\n"
                    f"🏠 <b>Manzil:</b> {address}\n"
                    f"🔌 <b>Ulanish turi:</b> {connection_type}\n"
                    f"💳 <b>Tarif:</b> {tariff}\n\n"
                    f"💰 <b>To'lov ma'lumotlari:</b>\n"
                    f"├ O'rnatish: {format_sum(costs['setup_fee'])} so'm\n"
                    f"├ Uskunalar: {format_sum(costs['equipment_fee'])} so'm\n"
                    f"├ Jami boshlang'ich: {format_sum(costs['total_initial'])} so'm\n"
                    f"└ Oylik to'lov: {format_sum(costs['monthly_fee'])} so'm\n\n"
                    f"📅 <b>Yaratilgan vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                    f"🔄 <b>Status:</b> Call Center'ga yuborildi\n"
                    f"👨‍💼 <b>Manager:</b> {manager.get('full_name', 'N/A')}\n\n"
                    f"Call Center xodimlari tez orada mijoz bilan bog'lanadi."
                )
                await callback.message.answer(success_msg, parse_mode='HTML')
            else:
                await callback.answer("❌ Xatolik yuz berdi!", show_alert=True)
                await callback.message.answer("❌ Zayavka yaratishda xatolik yuz berdi. Qayta urinib ko'ring.")
            
            await state.clear()
            
        except Exception as e:
            logger.error(f"Error creating connection order: {e}")
            await callback.answer("❌ Texnik xatolik yuz berdi!", show_alert=True)

    @router.callback_query(F.data == "mgr_resend_zayavka", StateFilter(ManagerConnectionOrderStates.confirming_connection))
    async def resend_connection_summary(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        await show_connection_confirmation(callback, state, geo=data.get('geo'))

    return router
