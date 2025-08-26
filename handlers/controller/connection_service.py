"""
Controller Connection Service - Client-like Flow with Client Search

Allows controller to create a connection request on behalf of a client.
Mock data implementation - no real database integration.
"""

import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
import uuid

from filters.role_filter import RoleFilter
from states.controller_states import (
    ControllerApplicationStates,
    ControllerOrdersStates,
    ControllerConnectionOrderStates,
    ControllerServiceOrderStates,
)
from keyboards.controllers_buttons import (
    get_controller_regions_keyboard,
    controller_zayavka_type_keyboard,
    controller_geolocation_keyboard,
    controller_confirmation_keyboard,
    get_controller_tariff_selection_keyboard,
    get_application_creator_keyboard,
)

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

mock_clients = [
    {
        'id': 1001,
        'full_name': 'Aziz Karimov',
        'phone': '+998901234567',
        'phone_number': '+998901234567',
        'role': 'client',
        'language': 'uz',
        'region': 'toshkent'
    },
    {
        'id': 1002,
        'full_name': 'Malika Toshmatova',
        'phone': '+998901234568',
        'phone_number': '+998901234568',
        'role': 'client',
        'language': 'uz',
        'region': 'toshkent'
    },
    {
        'id': 1003,
        'full_name': 'Jahongir Azimov',
        'phone': '+998901234569',
        'phone_number': '+998901234569',
        'role': 'client',
        'language': 'uz',
        'region': 'toshkent'
    },
    {
        'id': 1004,
        'full_name': 'Dilfuza Karimova',
        'phone': '+998901234570',
        'phone_number': '+998901234570',
        'role': 'client',
        'language': 'uz',
        'region': 'toshkent'
    }
]

mock_service_requests = []

# Mock database functions
async def get_user_by_telegram_id(region: str, telegram_id: int):
    """Mock get user by telegram ID"""
    print(f"Mock: Getting user by telegram ID {telegram_id} in region {region}")
    return mock_users.get(telegram_id)

async def search_users(region: str, search_term: str):
    """Mock search users"""
    print(f"Mock: Searching users in region {region} with term '{search_term}'")
    results = []
    search_lower = search_term.lower()
    
    for client in mock_clients:
        if (search_lower in client['full_name'].lower() or 
            search_lower in client['phone'].lower() or
            search_lower in str(client['id'])):
            results.append(client)
    
    return results

async def get_user(region: str, user_id: int):
    """Mock get user by ID"""
    print(f"Mock: Getting user {user_id} in region {region}")
    for client in mock_clients:
        if client['id'] == user_id:
            return client
    return None

async def get_user_by_phone(region: str, phone: str):
    """Mock get user by phone"""
    print(f"Mock: Getting user by phone {phone} in region {region}")
    for client in mock_clients:
        if client['phone'] == phone or client['phone_number'] == phone:
            return client
    return None

async def get_user_by_abonent_id(region: str, abonent_id: str):
    """Mock get user by abonent ID"""
    print(f"Mock: Getting user by abonent ID {abonent_id} in region {region}")
    for client in mock_clients:
        if str(client['id']) == abonent_id:
            return client
    return None

async def create_or_update_user(region: str, user_data: dict):
    """Mock create or update user"""
    print(f"Mock: Creating/updating user in region {region} with data {user_data}")
    
    # Generate new ID
    new_id = max([c['id'] for c in mock_clients]) + 1 if mock_clients else 1001
    
    new_user = {
        'id': new_id,
        'full_name': user_data.get('full_name', 'New Client'),
        'phone': '+998900000000',
        'phone_number': '+998900000000',
        'role': user_data.get('role', 'client'),
        'language': user_data.get('language', 'uz'),
        'region': region
    }
    
    mock_clients.append(new_user)
    return new_id

async def create_service_request(region: str, request_data: dict):
    """Mock create service request"""
    print(f"Mock: Creating service request in region {region} with data {request_data}")
    
    # Add to mock storage
    mock_service_requests.append(request_data)
    
    # Log the creation
    print(f"Mock: Service request created successfully: {request_data['id']}")
    return True

async def get_service_request(region: str, request_id: str):
    """Mock get service request"""
    print(f"Mock: Getting service request {request_id} in region {region}")
    for request in mock_service_requests:
        if request['id'] == request_id:
            return request
    return None

# Mock audit logger
class MockAuditLogger:
    async def log_action(self, user_id: int, action: str, details: dict = None, region: str = None, entity_type: str = None, entity_id: str = None):
        print(f"Mock Audit: User {user_id} performed {action} in region {region}")
        if details:
            print(f"Mock Audit Details: {details}")

audit_logger = MockAuditLogger()

# Mock get user region function
async def get_user_region(telegram_id: int):
    """Mock get user region"""
    print(f"Mock: Getting region for user {telegram_id}")
    user = mock_users.get(telegram_id)
    return user.get('region') if user else 'toshkent'

logger = logging.getLogger(__name__)

def get_controller_connection_service_router():
    router = Router()

    # Role guard
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    # 1) Entry point: start with selecting search method
    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish"]))
    async def start_connection_order(message: Message, state: FSMContext):
        try:
            region = await get_user_region(message.from_user.id)
            if not region:
                await message.answer("❌ Region aniqlanmadi")
                return
                
            user = await get_user_by_telegram_id(region, message.from_user.id)
            if not user or user.get('role') != 'controller':
                await message.answer("Sizda ruxsat yo'q.")
                return

            await state.update_data(current_flow='connection', controller_region=region)
            await message.answer(
                "Mijozni qanday qidiramiz?",
                reply_markup=get_application_creator_keyboard('uz')
            )
            await state.set_state(ControllerApplicationStates.selecting_client_search_method)
            
            # Log action
            await audit_logger.log_action(
                user_id=message.from_user.id,
                action='CONTROLLER_ACTION',
                details={'action': 'started_connection_order'},
                region=region
            )
        except Exception as e:
            logger.error(f"Error in start_connection_order: {e}")
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    # 2) Search flow (shared)
    @router.callback_query(F.data == "ctrl_search_phone", StateFilter(ControllerApplicationStates.selecting_client_search_method))
    async def search_by_phone(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ControllerApplicationStates.entering_phone)
        await callback.message.edit_text("📱 Telefon raqamini kiriting:\nMasalan: +998901234567")

    @router.callback_query(F.data == "ctrl_search_name", StateFilter(ControllerApplicationStates.selecting_client_search_method))
    async def search_by_name(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ControllerApplicationStates.entering_name)
        await callback.message.edit_text("👤 Mijoz ismini kiriting:\nMasalan: Alisher Karimov")

    @router.callback_query(F.data == "ctrl_search_id", StateFilter(ControllerApplicationStates.selecting_client_search_method))
    async def search_by_id(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ControllerApplicationStates.entering_client_id)
        await callback.message.edit_text("🆔 Mijoz ID sini kiriting:\nMasalan: 12345")

    @router.callback_query(F.data == "ctrl_search_new", StateFilter(ControllerApplicationStates.selecting_client_search_method))
    async def create_new_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ControllerApplicationStates.entering_new_client_name)
        await callback.message.edit_text("➕ Yangi mijoz nomini kiriting:")

    @router.callback_query(F.data == "ctrl_cancel_creation")
    async def cancel_creation(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.edit_text("❌ Zayavka yaratish bekor qilindi")
        await callback.answer()

    @router.message(StateFilter(ControllerApplicationStates.entering_phone))
    async def process_phone_search(message: Message, state: FSMContext):
        phone = message.text.strip()
        data = await state.get_data()
        region = data.get('controller_region')
        
        # Search in mock data
        client = await get_user_by_phone(region, phone)
        if client:
            clients = [client]
        else:
            # Try broader search
            clients = await search_users(region, phone)
        
        await _show_clients_list(message, state, clients)

    @router.message(StateFilter(ControllerApplicationStates.entering_name))
    async def process_name_search(message: Message, state: FSMContext):
        name = message.text.strip()
        data = await state.get_data()
        region = data.get('controller_region')
        
        # Search in mock data
        clients = await search_users(region, name)
        await _show_clients_list(message, state, clients)

    @router.message(StateFilter(ControllerApplicationStates.entering_client_id))
    async def process_id_search(message: Message, state: FSMContext):
        client_id = message.text.strip()
        data = await state.get_data()
        region = data.get('controller_region')
        
        # Search by abonent ID or user ID
        if client_id.isdigit():
            client = await get_user(region, int(client_id))
            if client:
                clients = [client]
            else:
                # Try as abonent ID
                client = await get_user_by_abonent_id(region, client_id)
                clients = [client] if client else []
        else:
            client = await get_user_by_abonent_id(region, client_id)
            clients = [client] if client else []
            
        await _show_clients_list(message, state, clients)

    @router.message(StateFilter(ControllerApplicationStates.entering_new_client_name))
    async def process_new_client(message: Message, state: FSMContext):
        full_name = message.text.strip()
        data = await state.get_data()
        region = data.get('controller_region')
        
        # Create new client in mock data
        new_client_data = {
            'full_name': full_name,
            'role': 'client',
            'language': 'uz',
            'created_by_controller': True
        }
        
        client_id = await create_or_update_user(region, new_client_data)
        if client_id:
            client = await get_user(region, client_id)
            clients = [client] if client else []
        else:
            clients = []
            
        await _show_clients_list(message, state, clients)

    async def _show_clients_list(message: Message, state: FSMContext, clients):
        if not clients:
            await message.answer("Mijoz topilmadi. Qayta urinib ko'ring.")
            await state.set_state(ControllerApplicationStates.selecting_client_search_method)
            await message.answer("Qidirish usulini tanlang:", reply_markup=get_application_creator_keyboard('uz'))
            return
        await state.update_data(found_clients=clients)
        await state.set_state(ControllerApplicationStates.selecting_client)

        buttons = []
        for i, c in enumerate(clients[:5]):
            client_name = c.get('full_name', 'Noma\'lum')
            client_phone = c.get('phone', c.get('phone_number', 'N/A'))
            buttons.append([{"text": f"{client_name} - {client_phone}", "cb": f"ctrl_select_client_{i}"}])
        
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            *[ [InlineKeyboardButton(text=b[0]['text'], callback_data=b[0]['cb'])] for b in buttons ],
            [InlineKeyboardButton(text="🔍 Boshqa qidirish", callback_data="ctrl_search_again")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="ctrl_cancel_creation")],
        ])
        await message.answer("Mijozni tanlang:", reply_markup=ikb)

    @router.callback_query(lambda c: c.data.startswith("ctrl_select_client_"), StateFilter(ControllerApplicationStates.selecting_client))
    async def select_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        clients = data.get('found_clients', [])
        idx = int(callback.data.split('_')[-1])
        if idx >= len(clients):
            await callback.answer("Xato", show_alert=True)
            return
        await state.update_data(selected_client=clients[idx])

        # Branch to next flow based on current_flow
        flow = (await state.get_data()).get('current_flow', 'connection')
        if flow == 'connection':
            await callback.message.edit_text("Hududni tanlang:")
            await callback.message.answer("Hududni tanlang:", reply_markup=get_controller_regions_keyboard('uz'))
            await state.set_state(ControllerConnectionOrderStates.selecting_region)
        else:
            await callback.message.edit_text("Hududni tanlang:")
            await callback.message.answer("Hududni tanlang:", reply_markup=get_controller_regions_keyboard('uz'))
            await state.set_state(ControllerServiceOrderStates.selecting_region)

    @router.callback_query(F.data == "ctrl_search_again")
    async def search_again(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.set_state(ControllerApplicationStates.selecting_client_search_method)
        await callback.message.edit_text("Qidirish usulini tanlang:")
        await callback.message.answer("Qidirish usulini tanlang:", reply_markup=get_application_creator_keyboard('uz'))

    # 3) Connection order flow (after client selected)
    @router.callback_query(F.data.startswith("ctrl_region_"), StateFilter(ControllerConnectionOrderStates.selecting_region))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            region = callback.data.replace("ctrl_region_", "")
            await state.update_data(service_region=region)

            await callback.message.answer(
                "Ulanish turini tanlang:",
                reply_markup=controller_zayavka_type_keyboard('uz')
            )
            await state.set_state(ControllerConnectionOrderStates.selecting_connection_type)
        except Exception as e:
            logger.error(f"Error in select_region: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_zayavka_type_"), StateFilter(ControllerConnectionOrderStates.selecting_connection_type))
    async def select_connection_type(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            connection_type = callback.data.replace("ctrl_zayavka_type_", "")
            await state.update_data(connection_type=connection_type)

            await callback.message.answer(
                "Tariflardan birini tanlang:",
                reply_markup=get_controller_tariff_selection_keyboard('uz')
            )
            await state.set_state(ControllerConnectionOrderStates.selecting_tariff)
        except Exception as e:
            logger.error(f"Error in select_connection_type: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.in_(["ctrl_tariff_standard", "ctrl_tariff_new"]), StateFilter(ControllerConnectionOrderStates.selecting_tariff))
    async def select_tariff(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            tariff = "Standard" if callback.data == "ctrl_tariff_standard" else "Yangi"
            await state.update_data(selected_tariff=tariff)

            await callback.message.answer("Manzilingizni kiriting:")
            await state.set_state(ControllerConnectionOrderStates.entering_address)
        except Exception as e:
            logger.error(f"Error in select_tariff: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(ControllerConnectionOrderStates.entering_address))
    async def get_connection_address(message: Message, state: FSMContext):
        try:
            await state.update_data(address=message.text)

            await message.answer(
                "Geolokatsiya yuborasizmi?",
                reply_markup=controller_geolocation_keyboard('uz')
            )
            await state.set_state(ControllerConnectionOrderStates.asking_for_geo)
        except Exception as e:
            logger.error(f"Error in get_connection_address: {e}")
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.callback_query(F.data.in_(["ctrl_send_location_yes", "ctrl_send_location_no"]), StateFilter(ControllerConnectionOrderStates.asking_for_geo))
    async def ask_for_geo(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            if callback.data == "ctrl_send_location_yes":
                await callback.message.answer("Geolokatsiyani yuboring:")
                await state.set_state(ControllerConnectionOrderStates.waiting_for_geo)
            else:
                await show_connection_confirmation(callback, state, geo=None)
        except Exception as e:
            logger.error(f"Error in ask_for_geo: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(ControllerConnectionOrderStates.waiting_for_geo), F.location)
    async def get_geo(message: Message, state: FSMContext):
        try:
            geo_data = {
                'latitude': message.location.latitude,
                'longitude': message.location.longitude
            }
            await state.update_data(geo=geo_data)
            await show_connection_confirmation(message, state, geo=geo_data)
        except Exception as e:
            logger.error(f"Error in get_geo: {e}")
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    async def show_connection_confirmation(message_or_callback, state: FSMContext, geo=None):
        data = await state.get_data()
        selected_client = data.get('selected_client', {})
        service_region = data.get('service_region', '-')
        connection_type = data.get('connection_type', '-')
        tariff = data.get('selected_tariff', '-')
        address = data.get('address', '-')

        text = (
            f"👤 <b>Mijoz:</b> {selected_client.get('full_name','N/A')}\n"
            f"🏛️ <b>Hudud:</b> {service_region}\n"
            f"🔌 <b>Ulanish turi:</b> {connection_type}\n"
            f"💳 <b>Tarif:</b> {tariff}\n"
            f"🏠 <b>Manzil:</b> {address}\n"
            f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}"
        )

        if hasattr(message_or_callback, 'message'):
            await message_or_callback.message.answer(text, parse_mode='HTML', reply_markup=controller_confirmation_keyboard('uz'))
        else:
            await message_or_callback.answer(text, parse_mode='HTML', reply_markup=controller_confirmation_keyboard('uz'))
        await state.set_state(ControllerConnectionOrderStates.confirming_connection)

    @router.callback_query(F.data == "ctrl_confirm_zayavka", StateFilter(ControllerConnectionOrderStates.confirming_connection))
    async def confirm_connection_order(callback: CallbackQuery, state: FSMContext):
        try:
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
            await callback.answer()

            data = await state.get_data()
            controller_region = data.get('controller_region')
            service_region = data.get('service_region')
            selected_client = data.get('selected_client', {})
            
            # Generate unique request ID
            request_id = f"CON_{str(uuid.uuid4())[:8].upper()}"
            
            # Prepare request data
            request_data = {
                'id': request_id,
                'workflow_type': 'connection_request',
                'client_id': selected_client.get('id'),
                'role_current': 'manager',  # Assigned to manager after creation
                'current_status': 'created',
                'priority': 'medium',
                'description': f"Ulanish so'rovi - {data.get('connection_type', 'B2C')} - Tarif: {data.get('selected_tariff', 'Standard')}",
                'location': data.get('address', ''),
                'contact_info': {
                    'phone': selected_client.get('phone', selected_client.get('phone_number')),
                    'name': selected_client.get('full_name')
                },
                'state_data': {
                    'connection_type': data.get('connection_type'),
                    'tariff': data.get('selected_tariff'),
                    'service_region': service_region,
                    'geo': data.get('geo')
                },
                'created_by_staff': True,
                'staff_creator_id': callback.from_user.id,
                'staff_creator_role': 'controller',
                'creation_source': 'controller'
            }
            
            # Create request in mock data
            success = await create_service_request(service_region, request_data)
            
            if success:
                success_msg = (
                    "✅ Ulanish arizasi muvaffaqiyatli yaratildi!\n"
                    f"📋 Ariza ID: {request_id}\n"
                    f"🏛️ Hudud: {service_region}\n"
                    f"👤 Mijoz: {selected_client.get('full_name')}\n\n"
                    "Menejerlar tez orada mijoz bilan bog'lanadi."
                )
                
                # Log action
                await audit_logger.log_action(
                    user_id=callback.from_user.id,
                    action='WORKFLOW_CREATED',
                    details={
                        'request_id': request_id,
                        'type': 'connection',
                        'client_id': selected_client.get('id'),
                        'region': service_region
                    },
                    entity_type='service_request',
                    entity_id=request_id,
                    region=controller_region
                )
            else:
                success_msg = "❌ Ariza yaratishda xatolik yuz berdi. Qayta urinib ko'ring."
                
            await callback.message.answer(success_msg)
            await state.clear()
        except Exception as e:
            logger.error(f"Error in confirm_connection_order: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_resend_zayavka", StateFilter(ControllerConnectionOrderStates.confirming_connection))
    async def resend_connection_summary(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            data = await state.get_data()
            await show_connection_confirmation(callback, state, geo=data.get('geo'))
        except Exception as e:
            logger.error(f"Error in resend_connection_summary: {e}")
            await callback.answer("Xatolik yuz berdi")

    return router