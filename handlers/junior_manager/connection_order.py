"""
Junior Manager Connection Order Handler - Mock Data Implementation

Bu modul junior manager uchun ulanish arizasi yaratish funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from datetime import datetime
import uuid
from filters.role_filter import RoleFilter
from keyboards.client_buttons import (
    get_client_regions_keyboard,
    zayavka_type_keyboard,
    get_client_tariff_selection_keyboard,
    geolocation_keyboard,
    confirmation_keyboard,
)
from keyboards.junior_manager_buttons import (
    get_junior_manager_main_menu,
    get_client_search_menu,
    get_application_priority_keyboard
)
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Mock data storage
mock_users = {
    123456789: {
        'id': 1,
        'telegram_id': 123456789,
        'role': 'junior_manager',
        'language': 'uz',
        'full_name': 'Test Junior Manager',
        'phone_number': '+998901234567',
        'region': 'toshkent'
    }
}

# Mock clients data
MOCK_CLIENTS = [
    {
        'id': 1,
        'full_name': 'Alisher Karimov',
        'phone': '+998901234567',
        'username': 'alisher_k',
        'address': 'Toshkent shahri, Chilanzor tumani, 15-uy',
        'abonent_id': 'AB001',
        'created_at': '2024-01-15 10:30:00',
        'region': 'toshkent'
    },
    {
        'id': 2,
        'full_name': 'Dilfuza Rahimova',
        'phone': '+998901234568',
        'username': 'dilfuza_r',
        'address': 'Toshkent shahri, Sergeli tumani, 25-uy',
        'abonent_id': 'AB002',
        'created_at': '2024-01-14 14:20:00',
        'region': 'toshkent'
    },
    {
        'id': 3,
        'full_name': 'Jamshid Toshmatov',
        'phone': '+998901234569',
        'username': 'jamshid_t',
        'address': 'Toshkent shahri, Yakkasaroy tumani, 8-uy',
        'abonent_id': 'AB003',
        'created_at': '2024-01-13 09:15:00',
        'region': 'toshkent'
    },
    {
        'id': 4,
        'full_name': 'Malika Yusupova',
        'phone': '+998901234570',
        'username': 'malika_y',
        'address': 'Toshkent shahri, Shayxontohur tumani, 12-uy',
        'abonent_id': 'AB004',
        'created_at': '2024-01-12 16:45:00',
        'region': 'toshkent'
    },
    {
        'id': 5,
        'full_name': 'Rustam Azimov',
        'phone': '+998901234571',
        'username': 'rustam_a',
        'address': 'Toshkent shahri, Uchtepa tumani, 20-uy',
        'abonent_id': 'AB005',
        'created_at': '2024-01-11 11:30:00',
        'region': 'toshkent'
    }
]

# Mock service requests storage
mock_service_requests = {}
mock_request_counter = 1000

# Mock inbox notifications storage
mock_inbox_notifications = []

# Mock workflow engine
class MockWorkflowEngine:
    """Mock workflow engine"""
    def __init__(self):
        self.workflows = []
    
    def create_workflow(self, workflow_type, initiator_id, initiator_role, data):
        """Mock create workflow"""
        workflow = {
            'id': str(uuid.uuid4()),
            'workflow_type': workflow_type,
            'initiator_id': initiator_id,
            'initiator_role': initiator_role,
            'data': data,
            'created_at': datetime.now().isoformat()
        }
        self.workflows.append(workflow)
        logger.info(f"Mock: Created workflow {workflow['id']} of type {workflow_type}")
        return workflow

# Initialize mock instances
mock_workflow_engine = MockWorkflowEngine()

# Mock functions to replace database calls
async def get_user_by_telegram_id(user_id: int):
    """Mock get user by telegram ID"""
    return mock_users.get(user_id)

async def search_clients_by_phone(phone: str, region: str = 'toshkent'):
    """Mock search clients by phone"""
    try:
        results = []
        for client in MOCK_CLIENTS:
            if phone in client.get('phone', ''):
                results.append(client)
        return results[:5]
    except Exception as e:
        logger.error(f"Mock: Error searching by phone: {e}")
        return []

async def search_clients_by_name(name: str, region: str = 'toshkent'):
    """Mock search clients by name"""
    try:
        name_lower = name.lower()
        results = []
        for client in MOCK_CLIENTS:
            if name_lower in client.get('full_name', '').lower():
                results.append(client)
        return results[:5]
    except Exception as e:
        logger.error(f"Mock: Error searching by name: {e}")
        return []

async def get_client_by_id(client_id: int, region: str = 'toshkent'):
    """Mock get client by ID"""
    try:
        for client in MOCK_CLIENTS:
            if client.get('id') == client_id:
                return client
        return None
    except Exception as e:
        logger.error(f"Mock: Error getting client by ID: {e}")
        return None

async def create_new_client(client_data: Dict[str, Any], region: str = 'toshkent'):
    """Mock create new client"""
    try:
        new_id = max([c.get('id', 0) for c in MOCK_CLIENTS]) + 1
        new_client = {
            'id': new_id,
            **client_data,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'region': region
        }
        MOCK_CLIENTS.append(new_client)
        return new_client
    except Exception as e:
        logger.error(f"Mock: Error creating client: {e}")
        return None

async def create_service_request(region: str, request_data: Dict[str, Any]):
    """Mock create service request"""
    try:
        global mock_request_counter
        mock_request_counter += 1
        
        request_id = f"REQ{mock_request_counter:06d}"
        request_data['id'] = request_id
        request_data['created_at'] = datetime.now().isoformat()
        request_data['region'] = region
        
        mock_service_requests[request_id] = request_data
        
        logger.info(f"Mock: Created service request {request_id} in region {region}")
        return request_id
        
    except Exception as e:
        logger.error(f"Mock: Error creating service request: {e}")
        return None

async def assign_service_request(region: str, request_id: str, assignee_id: int, assignee_role: str):
    """Mock assign service request"""
    try:
        if request_id in mock_service_requests:
            mock_service_requests[request_id]['assigned_to'] = assignee_id
            mock_service_requests[request_id]['assigned_role'] = assignee_role
            mock_service_requests[request_id]['assigned_at'] = datetime.now().isoformat()
            
            logger.info(f"Mock: Assigned request {request_id} to {assignee_role} {assignee_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Mock: Error assigning service request: {e}")
        return False

async def create_on_assignment(region_code: str, application_id: str, assigned_role: str, 
                              title: str, description: str, priority: str, application_type: str):
    """Mock create inbox notification"""
    try:
        notification = {
            'id': str(uuid.uuid4()),
            'region_code': region_code,
            'application_id': application_id,
            'assigned_role': assigned_role,
            'title': title,
            'description': description,
            'priority': priority,
            'application_type': application_type,
            'created_at': datetime.now().isoformat(),
            'is_read': False
        }
        
        mock_inbox_notifications.append(notification)
        logger.info(f"Mock: Created inbox notification for {assigned_role} about {application_id}")
        return True
        
    except Exception as e:
        logger.error(f"Mock: Error creating inbox notification: {e}")
        return False

async def get_user_lang(user_id: int):
    """Mock get user language"""
    user = await get_user_by_telegram_id(user_id)
    return user.get('language', 'uz') if user else 'uz'

async def get_text(key: str, lang: str = 'uz'):
    """Mock get text by key and language"""
    # Simple mock text function
    texts = {
        'uz': {
            'client_not_found': 'Mijoz topilmadi',
            'client_created': 'Mijoz yaratildi',
            'request_created': 'Ariza yaratildi'
        },
        'ru': {
            'client_not_found': 'Клиент не найден',
            'client_created': 'Клиент создан',
            'request_created': 'Заявка создана'
        }
    }
    return texts.get(lang, {}).get(key, key)


class JuniorManagerConnectionStates(StatesGroup):
    # Client selection states
    selecting_client_method = State()
    searching_client_phone = State()
    searching_client_name = State()
    searching_client_id = State()
    creating_new_client = State()
    entering_client_name = State()
    entering_client_phone = State()
    entering_client_address = State()
    
    # Connection order states
    selecting_region = State()
    selecting_connection_type = State()
    selecting_tariff = State()
    entering_address = State()
    asking_for_geo = State()
    waiting_for_geo = State()
    selecting_priority = State()
    entering_notes = State()
    confirming_connection = State()


# Create router
router = Router(name="junior_manager_connection_order")

# Apply role filter to all handlers
router.message.filter(RoleFilter(role="junior_manager"))
router.callback_query.filter(RoleFilter(role="junior_manager"))

@router.message(F.text.in_(["🔌 Ulanish arizasi yaratish", "🔌 Создать заявку на подключение"]))
async def start_connection_order(message: Message, state: FSMContext):
    """Start connection order creation on behalf of a client."""
    user_id = message.from_user.id
    
    try:
        # Get user data
        user = await get_user_by_telegram_id(user_id)
        if not user:
            await message.answer("❌ Foydalanuvchi topilmadi.")
            return
        
        # Verify role
        if user.get('role') != 'junior_manager':
            await message.answer("⛔ Sizda bu bo'limga kirish ruxsati yo'q.")
            return
        
        # Get language
        lang = await get_user_lang(user_id) or user.get('language', 'uz')
        
        # Clear previous state
        await state.clear()
        
        # Ask how to find client
        if lang == 'uz':
            text = (
                "🔌 <b>Ulanish arizasi yaratish</b>\n\n"
                "Mijozni qanday topamiz?"
            )
        else:
            text = (
                "🔌 <b>Создание заявки на подключение</b>\n\n"
                "Как найти клиента?"
            )
        
        await message.answer(
            text,
            reply_markup=get_client_search_menu(lang),
            parse_mode='HTML'
        )
        
        await state.set_state(JuniorManagerConnectionStates.selecting_client_method)
        await state.update_data(
            language=lang,
            region=user.get('region'),
            creator_id=user.get('id'),
            creator_telegram_id=user_id
        )
        
        logger.info(f"Junior Manager {user_id} started connection order creation")
        
    except Exception as e:
        logger.error(f"Error in start_connection_order: {str(e)}")
        await message.answer("❌ Xatolik yuz berdi.")

# Client search handlers
@router.callback_query(F.data == "jm_search_phone", StateFilter(JuniorManagerConnectionStates.selecting_client_method))
async def search_by_phone(callback: CallbackQuery, state: FSMContext):
    """Search client by phone number"""
    await callback.answer()
    
    data = await state.get_data()
    lang = data.get('language', 'uz')
    
    text = "📱 Mijoz telefon raqamini kiriting:" if lang == 'uz' else "📱 Введите номер телефона клиента:"
    await callback.message.edit_text(text)
    await state.set_state(JuniorManagerConnectionStates.searching_client_phone)


@router.callback_query(F.data == "jm_search_name", StateFilter(JuniorManagerConnectionStates.selecting_client_method))
async def search_by_name(callback: CallbackQuery, state: FSMContext):
    """Search client by name"""
    await callback.answer()
    
    data = await state.get_data()
    lang = data.get('language', 'uz')
    
    text = "👤 Mijoz ismini kiriting:" if lang == 'uz' else "👤 Введите имя клиента:"
    await callback.message.edit_text(text)
    await state.set_state(JuniorManagerConnectionStates.searching_client_name)


@router.callback_query(F.data == "jm_search_id", StateFilter(JuniorManagerConnectionStates.selecting_client_method))
async def search_by_id(callback: CallbackQuery, state: FSMContext):
    """Search client by ID"""
    await callback.answer()
    
    data = await state.get_data()
    lang = data.get('language', 'uz')
    
    text = "🆔 Mijoz ID raqamini kiriting:" if lang == 'uz' else "🆔 Введите ID клиента:"
    await callback.message.edit_text(text)
    await state.set_state(JuniorManagerConnectionStates.searching_client_id)


@router.callback_query(F.data == "jm_search_new", StateFilter(JuniorManagerConnectionStates.selecting_client_method))
async def create_new_client(callback: CallbackQuery, state: FSMContext):
    """Create new client"""
    await callback.answer()
    
    data = await state.get_data()
    lang = data.get('language', 'uz')
    
    text = "👤 Yangi mijoz ismini kiriting:" if lang == 'uz' else "👤 Введите имя нового клиента:"
    await callback.message.edit_text(text)
    await state.set_state(JuniorManagerConnectionStates.entering_client_name)


# Handle client search results
@router.message(StateFilter(JuniorManagerConnectionStates.searching_client_phone))
async def handle_phone_search(message: Message, state: FSMContext):
    """Handle phone search"""
    try:
        phone = message.text.strip()
        clients = await search_clients_by_phone(phone)
        
        if clients:
            client = clients[0]  # Take first match
            await state.update_data(client_id=client['id'], client_data=client)
            await proceed_with_client(message, state, client)
        else:
            data = await state.get_data()
            lang = data.get('language', 'uz')
            
            text = "❌ Mijoz topilmadi. Yangi mijoz yaratilsinmi?" if lang == 'uz' else "❌ Клиент не найден. Создать нового?"
            await message.answer(text)
            await state.set_state(JuniorManagerConnectionStates.entering_client_name)
            
    except Exception as e:
        logger.error(f"Error in handle_phone_search: {str(e)}")
        await message.answer("❌ Xatolik yuz berdi.")


async def proceed_with_client(message: Message, state: FSMContext, client: dict):
    """Proceed with selected client"""
    data = await state.get_data()
    lang = data.get('language', 'uz')
    
    if lang == 'uz':
        text = (
            f"✅ Mijoz tanlandi:\n"
            f"👤 {client.get('full_name', 'N/A')}\n"
            f"📱 {client.get('phone', 'N/A')}\n\n"
            f"Hududni tanlang:"
        )
    else:
        text = (
            f"✅ Клиент выбран:\n"
            f"👤 {client.get('full_name', 'N/A')}\n"
            f"📱 {client.get('phone', 'N/A')}\n\n"
            f"Выберите регион:"
        )
    
    await message.answer(text, reply_markup=get_client_regions_keyboard())
    await state.set_state(JuniorManagerConnectionStates.selecting_region)


@router.callback_query(
    F.data.startswith("region_"),
    StateFilter(JuniorManagerConnectionStates.selecting_region),
)
async def select_region(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    region = callback.data.split("_")[-1]
    await state.update_data(selected_region=region)
    
    data = await state.get_data()
    lang = data.get('language', 'uz')

    await callback.message.answer(
        "Ulanish turini tanlang:" if lang == 'uz' else "Выберите тип подключения:",
        reply_markup=zayavka_type_keyboard(lang)
    )
    await state.set_state(JuniorManagerConnectionStates.selecting_connection_type)

@router.callback_query(
    F.data.startswith("zayavka_type_"),
    StateFilter(JuniorManagerConnectionStates.selecting_connection_type),
)
async def select_connection_type(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    connection_type = callback.data.split("_")[-1]  # b2c or b2b
    await state.update_data(connection_type=connection_type)
    
    data = await state.get_data()
    lang = data.get('language', 'uz')

    await callback.message.answer(
        "Tariflardan birini tanlang:" if lang == 'uz' else "Выберите тариф:",
        reply_markup=get_client_tariff_selection_keyboard()
    )
    await state.set_state(JuniorManagerConnectionStates.selecting_tariff)

@router.callback_query(
    F.data.in_(["tariff_standard", "tariff_new"]),
    StateFilter(JuniorManagerConnectionStates.selecting_tariff),
)
async def select_tariff(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    tariff = "Standard" if callback.data == "tariff_standard" else "Yangi"
    await state.update_data(selected_tariff=tariff)
    
    data = await state.get_data()
    lang = data.get('language', 'uz')

    text = "Mijoz manzilini kiriting:" if lang == 'uz' else "Введите адрес клиента:"
    await callback.message.answer(text)
    await state.set_state(JuniorManagerConnectionStates.entering_address)


@router.message(StateFilter(JuniorManagerConnectionStates.entering_address))
async def get_connection_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text.strip())
    
    data = await state.get_data()
    lang = data.get('language', 'uz')

    await message.answer(
        "Geolokatsiya yuborasizmi?" if lang == 'uz' else "Отправить геолокацию?",
        reply_markup=geolocation_keyboard(lang)
    )
    await state.set_state(JuniorManagerConnectionStates.asking_for_geo)


@router.callback_query(
    F.data.in_(["send_location_yes", "send_location_no"]),
    StateFilter(JuniorManagerConnectionStates.asking_for_geo),
)
async def ask_for_geo(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    data = await state.get_data()
    lang = data.get('language', 'uz')
    
    if callback.data == "send_location_yes":
        text = "📍 Geolokatsiyani yuboring:" if lang == 'uz' else "📍 Отправьте геолокацию:"
        await callback.message.answer(text)
        await state.set_state(JuniorManagerConnectionStates.waiting_for_geo)
    else:
        # Skip geo and ask for priority
        await callback.message.answer(
            "Ariza muhimligini tanlang:" if lang == 'uz' else "Выберите приоритет заявки:",
            reply_markup=get_application_priority_keyboard(lang)
        )
        await state.set_state(JuniorManagerConnectionStates.selecting_priority)


@router.message(StateFilter(JuniorManagerConnectionStates.waiting_for_geo), F.location)
async def get_geo(message: Message, state: FSMContext):
    location = message.location
    await state.update_data(
        geo_lat=location.latitude,
        geo_lon=location.longitude
    )
    
    data = await state.get_data()
    lang = data.get('language', 'uz')
    
    # Ask for priority
    await message.answer(
        "Ariza muhimligini tanlang:" if lang == 'uz' else "Выберите приоритет заявки:",
        reply_markup=get_application_priority_keyboard(lang)
    )
    await state.set_state(JuniorManagerConnectionStates.selecting_priority)


@router.callback_query(
    F.data.startswith("jm_priority_"),
    StateFilter(JuniorManagerConnectionStates.selecting_priority)
)
async def select_priority(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    priority = callback.data.replace("jm_priority_", "")
    await state.update_data(priority=priority)
    
    data = await state.get_data()
    lang = data.get('language', 'uz')
    
    # Ask for additional notes
    text = "Qo'shimcha izoh kiriting (ixtiyoriy):" if lang == 'uz' else "Введите дополнительные заметки (необязательно):"
    await callback.message.answer(text)
    await state.set_state(JuniorManagerConnectionStates.entering_notes)


@router.message(StateFilter(JuniorManagerConnectionStates.entering_notes))
async def get_notes(message: Message, state: FSMContext):
    notes = message.text.strip() if message.text != "/skip" else ""
    await state.update_data(notes=notes)
    
    # Show confirmation
    await show_confirmation(message, state)


async def show_confirmation(message: Message, state: FSMContext):
    """Show final confirmation before creating the request."""
    data = await state.get_data()
    lang = data.get('language', 'uz')
    
    client_data = data.get('client_data', {})
    region = data.get('selected_region', '-')
    connection_type = data.get('connection_type', 'standard')
    tariff = data.get('selected_tariff', 'Standard')
    address = data.get('address', '-')
    priority = data.get('priority', 'medium')
    notes = data.get('notes', '')
    has_geo = bool(data.get('geo_lat'))
    
    priority_text = {
        'low': '🟢 Past' if lang == 'uz' else '🟢 Низкий',
        'medium': '🟡 O\'rta' if lang == 'uz' else '🟡 Средний',
        'high': '🟠 Yuqori' if lang == 'uz' else '🟠 Высокий',
        'urgent': '🔴 Shoshilinch' if lang == 'uz' else '🔴 Срочный'
    }
    
    if lang == 'uz':
        text = (
            f"📋 <b>Ariza ma'lumotlari:</b>\n\n"
            f"👤 <b>Mijoz:</b> {client_data.get('full_name', 'N/A')}\n"
            f"📱 <b>Telefon:</b> {client_data.get('phone', 'N/A')}\n"
            f"🏛️ <b>Hudud:</b> {region}\n"
            f"🔌 <b>Ulanish turi:</b> {connection_type}\n"
            f"💳 <b>Tarif:</b> {tariff}\n"
            f"🏠 <b>Manzil:</b> {address}\n"
            f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if has_geo else '❌ Yuborilmagan'}\n"
            f"⚡ <b>Muhimlik:</b> {priority_text.get(priority, priority)}\n"
        )
        if notes:
            text += f"📝 <b>Izoh:</b> {notes}\n"
        text += "\nTasdiqlaysizmi?"
    else:
        text = (
            f"📋 <b>Данные заявки:</b>\n\n"
            f"👤 <b>Клиент:</b> {client_data.get('full_name', 'N/A')}\n"
            f"📱 <b>Телефон:</b> {client_data.get('phone', 'N/A')}\n"
            f"🏛️ <b>Регион:</b> {region}\n"
            f"🔌 <b>Тип подключения:</b> {connection_type}\n"
            f"💳 <b>Тариф:</b> {tariff}\n"
            f"🏠 <b>Адрес:</b> {address}\n"
            f"📍 <b>Геолокация:</b> {'✅ Отправлена' if has_geo else '❌ Не отправлена'}\n"
            f"⚡ <b>Приоритет:</b> {priority_text.get(priority, priority)}\n"
        )
        if notes:
            text += f"📝 <b>Заметка:</b> {notes}\n"
        text += "\nПодтвердить?"

    await message.answer(text, parse_mode='HTML', reply_markup=confirmation_keyboard(lang))
    await state.set_state(JuniorManagerConnectionStates.confirming_connection)


@router.callback_query(
    F.data == "confirm_zayavka",
    StateFilter(JuniorManagerConnectionStates.confirming_connection),
)
async def confirm_connection_order(callback: CallbackQuery, state: FSMContext):
    """Create the connection order"""
    try:
        await callback.answer()
        
        # Remove keyboard
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except:
            pass
        
        data = await state.get_data()
        lang = data.get('language', 'uz')
        region = data.get('region') or data.get('selected_region')
        
        # Prepare request data
        request_id = str(uuid.uuid4())
        
        # Determine workflow type and target role based on connection type
        connection_type = data.get('connection_type', 'b2c')
        
        # B2C (Jismoniy shaxs) ulanish goes to Manager
        # B2B (Yuridik shaxs) goes to Controller for technical review
        if connection_type == 'b2c':
            target_role = 'manager'
            workflow_type = 'connection_request'
            description = f"Jismoniy shaxs ulanish arizasi, Tariff: {data.get('selected_tariff', 'Standard')}"
        elif connection_type == 'b2b':
            # B2B requires Controller review first
            target_role = 'controller'
            workflow_type = 'connection_request_b2b'
            description = f"Yuridik shaxs ulanish arizasi, Tariff: {data.get('selected_tariff', 'Standard')}"
        else:
            # Default to manager
            target_role = 'manager'
            workflow_type = 'connection_request'
            description = f"Ulanish arizasi, Tariff: {data.get('selected_tariff', 'Standard')}"
        
        request_data = {
            'id': request_id,
            'workflow_type': workflow_type,
            'client_id': data.get('client_id'),
            'role_current': target_role,  # Send to appropriate role
            'current_status': 'created',
            'priority': data.get('priority', 'medium'),
            'description': description,
            'location': data.get('address'),
            'contact_info': data.get('client_data', {}),
            'state_data': {
                'connection_type': connection_type,
                'tariff': data.get('selected_tariff'),
                'notes': data.get('notes', ''),
                'geo_lat': data.get('geo_lat'),
                'geo_lon': data.get('geo_lon')
            },
            'created_by_staff': True,
            'staff_creator_id': data.get('creator_id'),
            'staff_creator_role': 'junior_manager',
            'creation_source': 'junior_manager'
        }
        
        # Create service request in database
        if region:
            created_id = await create_service_request(region, request_data)
            
            # Create inbox notification for appropriate role
            if target_role == 'manager':
                notification_title = f"Yangi B2C ulanish arizasi - {data.get('client_data', {}).get('full_name', 'N/A')}"
                notification_desc = f"Junior Manager tomonidan yaratilgan jismoniy shaxs arizasi"
            else:
                notification_title = f"Yangi B2B ulanish arizasi - {data.get('client_data', {}).get('full_name', 'N/A')}"
                notification_desc = f"Junior Manager tomonidan yaratilgan yuridik shaxs arizasi"
            
            await create_on_assignment(
                region_code=region,
                application_id=created_id,
                assigned_role=target_role,
                title=notification_title,
                description=notification_desc,
                priority=data.get('priority', 'medium'),
                application_type=workflow_type
            )
            
            # Log with workflow engine
            mock_workflow_engine.create_workflow(
                workflow_type=workflow_type,
                initiator_id=data.get('creator_telegram_id'),
                initiator_role='junior_manager',
                data=request_data
            )
            
            if lang == 'uz':
                if connection_type == 'b2c':
                    success_msg = (
                        "✅ <b>Jismoniy shaxs ulanish arizasi yaratildi!</b>\n\n"
                        f"📋 Ariza ID: <code>{created_id[:8]}</code>\n"
                        f"👤 Mijoz: {data.get('client_data', {}).get('full_name', 'N/A')}\n"
                        f"📍 Hudud: {region}\n\n"
                        "Ariza Manager'ga yuborildi va tez orada ko'rib chiqiladi."
                    )
                else:  # b2b
                    success_msg = (
                        "✅ <b>Yuridik shaxs ulanish arizasi yaratildi!</b>\n\n"
                        f"📋 Ariza ID: <code>{created_id[:8]}</code>\n"
                        f"🏢 Kompaniya: {data.get('client_data', {}).get('full_name', 'N/A')}\n"
                        f"📍 Hudud: {region}\n\n"
                        "Ariza Controller'ga texnik ko'rib chiqish uchun yuborildi."
                    )
            else:
                if connection_type == 'b2c':
                    success_msg = (
                        "✅ <b>Заявка физического лица на подключение создана!</b>\n\n"
                        f"📋 ID заявки: <code>{created_id[:8]}</code>\n"
                        f"👤 Клиент: {data.get('client_data', {}).get('full_name', 'N/A')}\n"
                        f"📍 Регион: {region}\n\n"
                        "Заявка отправлена менеджеру и будет рассмотрена в ближайшее время."
                    )
                else:  # b2b
                    success_msg = (
                        "✅ <b>Заявка юридического лица на подключение создана!</b>\n\n"
                        f"📋 ID заявки: <code>{created_id[:8]}</code>\n"
                        f"👤 Компания: {data.get('client_data', {}).get('full_name', 'N/A')}\n"
                        f"📍 Регион: {region}\n\n"
                        "Заявка отправлена контроллеру для технического рассмотрения."
                    )
            
            await callback.message.answer(
                success_msg,
                parse_mode='HTML',
                reply_markup=get_junior_manager_main_menu(lang)
            )
            
            logger.info(f"Junior Manager {data.get('creator_telegram_id')} created connection order {created_id}")
        else:
            await callback.message.answer("❌ Region tanlanmagan!")
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error in confirm_connection_order: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data == "jm_cancel_creation")
async def cancel_creation(callback: CallbackQuery, state: FSMContext):
    """Cancel application creation"""
    await callback.answer()
    
    data = await state.get_data()
    lang = data.get('language', 'uz')
    
    text = "❌ Ariza yaratish bekor qilindi" if lang == 'uz' else "❌ Создание заявки отменено"
    
    await callback.message.edit_text(text)
    await callback.message.answer(
        "Asosiy menyu" if lang == 'uz' else "Главное меню",
        reply_markup=get_junior_manager_main_menu(lang)
    )
    
    await state.clear() 