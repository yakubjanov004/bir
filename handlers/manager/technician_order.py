"""
Manager Technical Service Handler - Mock Data Version

This module provides technical service creation functionality for Manager role,
allowing managers to create technical service orders for clients using mock data.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
import logging
import json

from filters.role_filter import RoleFilter
from keyboards.manager_buttons import (
    get_manager_client_search_keyboard,
    get_manager_confirmation_keyboard,
)
from keyboards.controllers_buttons import (
    get_controller_regions_keyboard,
    controller_zayavka_type_keyboard,
    controller_media_attachment_keyboard,
    controller_geolocation_keyboard,
)
from states.manager_states import ManagerClientSearchStates, ManagerServiceOrderStates

# Mock data instead of database imports
logger = logging.getLogger(__name__)

# Mock client data
MOCK_CLIENTS = [
    {
        'id': 1,
        'full_name': 'Alisher Karimov',
        'phone': '+998901234567',
        'abonent_id': 'AB001',
        'region': 'toshkent'
    },
    {
        'id': 2,
        'full_name': 'Dilfuza Rahimova',
        'phone': '+998901234568',
        'abonent_id': 'AB002',
        'region': 'toshkent'
    },
    {
        'id': 3,
        'full_name': 'Jamshid Toshmatov',
        'phone': '+998901234569',
        'abonent_id': 'AB003',
        'region': 'toshkent'
    },
    {
        'id': 4,
        'full_name': 'Malika Yusupova',
        'phone': '+998901234570',
        'abonent_id': 'AB004',
        'region': 'toshkent'
    },
    {
        'id': 5,
        'full_name': 'Rustam Azimov',
        'phone': '+998901234571',
        'abonent_id': 'AB005',
        'region': 'toshkent'
    }
]

# Mock service requests counter
mock_request_counter = 1000

# Mock search functions
async def search_clients_by_phone(phone: str, region: str = 'toshkent'):
    """Telefon bo'yicha mijozlarni qidirish - Mock data"""
    try:
        # Exact match first
        exact_matches = [c for c in MOCK_CLIENTS if c['phone'] == phone]
        if exact_matches:
            return exact_matches
        
        # Partial search
        partial_matches = [c for c in MOCK_CLIENTS if phone in c['phone']]
        return partial_matches[:5]
    except Exception as e:
        logger.error(f"Error searching by phone: {e}")
        return []

async def search_clients_by_name(name: str, region: str = 'toshkent'):
    """Ism bo'yicha mijozlarni qidirish - Mock data"""
    try:
        name_lower = name.lower()
        matches = [c for c in MOCK_CLIENTS if name_lower in c['full_name'].lower()]
        return matches[:5]
    except Exception as e:
        logger.error(f"Error searching by name: {e}")
        return []

async def search_client_by_id(client_id: int, region: str = 'toshkent'):
    """ID bo'yicha mijozni topish - Mock data"""
    try:
        matches = [c for c in MOCK_CLIENTS if c['id'] == client_id]
        return matches
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        return []

async def search_client_by_abonent_id(abonent_id: str, region: str = 'toshkent'):
    """Abonent ID bo'yicha mijozni topish - Mock data"""
    try:
        matches = [c for c in MOCK_CLIENTS if c['abonent_id'] == abonent_id]
        return matches
    except Exception as e:
        logger.error(f"Error getting user by abonent ID: {e}")
        return []

async def get_user_by_telegram_id(region: str, telegram_id: int):
    """Mock manager user data"""
    return {
        'id': 999,
        'full_name': 'Manager User',
        'telegram_id': telegram_id,
        'role': 'manager',
        'region': region
    }

# Mock service request functions
async def create_service_request(region: str, request_data: dict):
    """Create mock service request"""
    global mock_request_counter
    mock_request_counter += 1
    logger.info(f"Mock service request created: {mock_request_counter}")
    return mock_request_counter

# Mock audit logger
class MockAuditLogger:
    async def log_manager_action(self, manager_id, action, target_type=None, target_id=None, details=None):
        logger.info(f"Mock audit log: Manager {manager_id} performed {action}")

audit_logger = MockAuditLogger()

# Technical service cost calculations
def calculate_technical_service_cost(service_type: str, problem_type: str = 'standard') -> dict:
    """Calculate technical service cost based on type"""
    costs = {
        'internet': {
            'standard': {'visit_fee': 50000, 'repair_fee': 100000, 'parts': 0},
            'complex': {'visit_fee': 50000, 'repair_fee': 150000, 'parts': 50000},
            'equipment': {'visit_fee': 50000, 'repair_fee': 200000, 'parts': 150000}
        },
        'tv': {
            'standard': {'visit_fee': 40000, 'repair_fee': 80000, 'parts': 0},
            'complex': {'visit_fee': 40000, 'repair_fee': 120000, 'parts': 30000},
            'equipment': {'visit_fee': 40000, 'repair_fee': 150000, 'parts': 100000}
        },
        'combo': {
            'standard': {'visit_fee': 60000, 'repair_fee': 150000, 'parts': 0},
            'complex': {'visit_fee': 60000, 'repair_fee': 200000, 'parts': 80000},
            'equipment': {'visit_fee': 60000, 'repair_fee': 250000, 'parts': 200000}
        }
    }
    
    service_type = service_type.lower()
    problem_type = problem_type.lower()
    
    if service_type in costs:
        if problem_type in costs[service_type]:
            cost_data = costs[service_type][problem_type]
        else:
            cost_data = costs[service_type]['standard']
        
        total = cost_data['visit_fee'] + cost_data['repair_fee'] + cost_data['parts']
        return {
            'visit_fee': cost_data['visit_fee'],
            'repair_fee': cost_data['repair_fee'],
            'parts_fee': cost_data['parts'],
            'total': total,
            'currency': 'UZS'
        }
    
    # Default costs
    return {
        'visit_fee': 50000,
        'repair_fee': 100000,
        'parts_fee': 0,
        'total': 150000,
        'currency': 'UZS'
    }


def get_manager_technical_service_router():
    router = Router()

    role_filter = RoleFilter("manager")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    # Entry point
    @router.message(F.text == "🔧 Texnik xizmat yaratish", flags={"block": False})
    async def start_manager_service(message: Message, state: FSMContext):
        await state.update_data(current_flow='technical')
        await message.answer("Mijozni qanday qidiramiz?", reply_markup=get_manager_client_search_keyboard('uz'))
        await state.set_state(ManagerClientSearchStates.selecting_client_search_method)

    # Search method callbacks
    @router.callback_query(F.data == "mgr_search_phone", StateFilter(ManagerClientSearchStates.selecting_client_search_method))
    async def mgr_search_by_phone(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.update_data(search_method='phone')
        await callback.message.edit_text("📱 Telefon raqamini kiriting:\nMasalan: +998901234567")
        await state.set_state(ManagerClientSearchStates.entering_phone)

    @router.callback_query(F.data == "mgr_search_name", StateFilter(ManagerClientSearchStates.selecting_client_search_method))
    async def mgr_search_by_name(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.update_data(search_method='name')
        await callback.message.edit_text("👤 Mijoz ismini kiriting:\nMasalan: Alisher Karimov")
        await state.set_state(ManagerClientSearchStates.entering_name)

    @router.callback_query(F.data == "mgr_search_id", StateFilter(ManagerClientSearchStates.selecting_client_search_method))
    async def mgr_search_by_id(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.update_data(search_method='id')
        await callback.message.edit_text("🆔 Mijoz ID sini kiriting:\nMasalan: 12345")
        await state.set_state(ManagerClientSearchStates.entering_client_id)

    @router.callback_query(F.data == "mgr_search_new", StateFilter(ManagerClientSearchStates.selecting_client_search_method))
    async def mgr_create_new_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await state.update_data(search_method='new')
        await callback.message.edit_text("➕ Yangi mijoz nomini kiriting:")
        await state.set_state(ManagerClientSearchStates.entering_new_client_name)

    @router.callback_query(F.data == "mgr_cancel_creation")
    async def mgr_cancel_creation(callback: CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.edit_text("❌ Ariza yaratish bekor qilindi")
        await callback.answer()

    # Collect user input for search entries
    @router.message(StateFilter(ManagerClientSearchStates.entering_phone, ManagerClientSearchStates.entering_name, ManagerClientSearchStates.entering_client_id, ManagerClientSearchStates.entering_new_client_name))
    async def handle_search_inputs(message: Message, state: FSMContext):
        data = await state.get_data()
        method = data.get('search_method')
        query = message.text.strip()
        region = data.get('region', 'toshkent')
        
        # Real database search
        if method == 'phone':
            clients = await search_clients_by_phone(query, region)
            
            # Log search
            await audit_logger.log_manager_action(
                manager_id=message.from_user.id,
                action='search_client_by_phone_tech',
                details={'phone': query, 'results': len(clients)}
            )
            
        elif method == 'name':
            clients = await search_clients_by_name(query, region)
            
            # Log search
            await audit_logger.log_manager_action(
                manager_id=message.from_user.id,
                action='search_client_by_name_tech',
                details={'name': query, 'results': len(clients)}
            )
            
        elif method == 'id':
            if not query.isdigit():
                await message.answer("❌ ID faqat raqamlardan iborat bo'lishi kerak")
                return
            clients = await search_client_by_id(int(query), region)
            
            # Log search
            await audit_logger.log_manager_action(
                manager_id=message.from_user.id,
                action='search_client_by_id_tech',
                details={'client_id': query, 'found': len(clients) > 0}
            )
            
        else:  # new - yangi mijoz yaratish o'rniga qidiramiz
            clients = await search_clients_by_name(query, region)
            if not clients:
                # Agar topilmasa, yangi mijoz yaratish uchun ma'lumot so'raymiz
                await message.answer(
                    "❌ Bunday mijoz topilmadi.\n\n"
                    "Yangi mijoz yaratish uchun telefon raqamini kiriting:"
                )
                await state.update_data(new_client_name=query, creating_new=True)
                await state.set_state(ManagerClientSearchStates.entering_phone)
                return

        if not clients:
            await message.answer("❌ Mijoz topilmadi. Qayta urinib ko'ring.")
            return

        await state.update_data(found_clients=clients)
        await state.set_state(ManagerClientSearchStates.selecting_client)
        
        ikb = InlineKeyboardMarkup(inline_keyboard=[
            *[[InlineKeyboardButton(text=f"{c['full_name']} - {c.get('phone','N/A')}", callback_data=f"mgr_select_client_{i}")] for i, c in enumerate(clients[:5])],
            [InlineKeyboardButton(text="🔍 Boshqa qidirish", callback_data="mgr_search_again")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="mgr_cancel_creation")],
        ])
        await message.answer("Mijozni tanlang:", reply_markup=ikb)

    @router.callback_query(lambda c: c.data.startswith("mgr_select_client_"), StateFilter(ManagerClientSearchStates.selecting_client))
    async def mgr_select_client(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        data = await state.get_data()
        clients = data.get('found_clients', [])
        idx = int(callback.data.split('_')[-1])
        if idx >= len(clients):
            await callback.answer("Xato", show_alert=True)
            return
        await state.update_data(selected_client=clients[idx])
        # Proceed to service flow
        await callback.message.edit_text("Hududni tanlang:")
        await callback.message.answer("Hududni tanlang:", reply_markup=get_controller_regions_keyboard('uz'))
        await state.set_state(ManagerServiceOrderStates.selecting_region)

    @router.callback_query(F.data == "mgr_search_again", StateFilter(ManagerClientSearchStates.selecting_client))
    async def mgr_search_again(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await callback.message.edit_text("Qidirish usulini tanlang:")
        await callback.message.answer("Qidirish usulini tanlang:", reply_markup=get_manager_client_search_keyboard('uz'))

    # Service order flow (mirrors controller)
    @router.callback_query(F.data.startswith("ctrl_region_"), StateFilter(ManagerServiceOrderStates.selecting_region))
    async def mgr_select_region(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        region = callback.data.replace("ctrl_region_", "")
        await state.update_data(region=region)
        await callback.message.answer("Abonent turini tanlang:", reply_markup=controller_zayavka_type_keyboard('uz'))
        await state.set_state(ManagerServiceOrderStates.selecting_order_type)

    @router.callback_query(F.data.startswith("ctrl_zayavka_type_"), StateFilter(ManagerServiceOrderStates.selecting_order_type))
    async def mgr_select_abonent_type(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        abonent_type = callback.data.replace("ctrl_zayavka_type_", "")
        await state.update_data(abonent_type=abonent_type)
        await callback.message.answer("Abonent ID raqamini kiriting:")
        await state.set_state(ManagerServiceOrderStates.waiting_for_abonent_id)

    @router.message(StateFilter(ManagerServiceOrderStates.waiting_for_abonent_id))
    async def mgr_get_abonent_id(message: Message, state: FSMContext):
        await state.update_data(abonent_id=message.text)
        await message.answer("Muammo tavsifini kiriting:")
        await state.set_state(ManagerServiceOrderStates.entering_description)

    @router.message(StateFilter(ManagerServiceOrderStates.entering_description))
    async def mgr_get_service_description(message: Message, state: FSMContext):
        await state.update_data(description=message.text)
        await message.answer("Foto yoki video yuborasizmi?", reply_markup=controller_media_attachment_keyboard('uz'))
        await state.set_state(ManagerServiceOrderStates.asking_for_media)

    @router.callback_query(F.data.in_(["ctrl_attach_media_yes", "ctrl_attach_media_no"]), StateFilter(ManagerServiceOrderStates.asking_for_media))
    async def mgr_ask_for_media(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        if callback.data == "ctrl_attach_media_yes":
            await callback.message.answer("Foto yoki videoni yuboring:")
            await state.set_state(ManagerServiceOrderStates.waiting_for_media)
        else:
            await mgr_ask_for_address(callback, state)

    @router.message(StateFilter(ManagerServiceOrderStates.waiting_for_media), F.photo | F.video)
    async def mgr_process_media(message: Message, state: FSMContext):
        media_file_id = message.photo[-1].file_id if message.photo else message.video.file_id
        await state.update_data(media=media_file_id)
        await mgr_ask_for_address(message, state)

    async def mgr_ask_for_address(message_or_callback, state: FSMContext):
        if hasattr(message_or_callback, "message"):
            await message_or_callback.message.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
        else:
            await message_or_callback.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
        await state.set_state(ManagerServiceOrderStates.entering_address)

    @router.message(StateFilter(ManagerServiceOrderStates.entering_address))
    async def mgr_get_service_address(message: Message, state: FSMContext):
        await state.update_data(address=message.text)
        await message.answer("Geolokatsiya yuborasizmi?", reply_markup=controller_geolocation_keyboard('uz'))
        await state.set_state(ManagerServiceOrderStates.asking_for_location)

    @router.callback_query(F.data.in_(["ctrl_send_location_yes", "ctrl_send_location_no"]), StateFilter(ManagerServiceOrderStates.asking_for_location))
    async def mgr_ask_for_geo(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        if callback.data == "ctrl_send_location_yes":
            await callback.message.answer("Geolokatsiyani yuboring:")
            await state.set_state(ManagerServiceOrderStates.waiting_for_location)
        else:
            await mgr_show_service_confirmation(callback, state)

    @router.message(StateFilter(ManagerServiceOrderStates.waiting_for_location), F.location)
    async def mgr_get_geo(message: Message, state: FSMContext):
        await state.update_data(geo=message.location)
        await mgr_show_service_confirmation(message, state)

    async def mgr_show_service_confirmation(message_or_callback, state: FSMContext):
        data = await state.get_data()
        selected_client = data.get('selected_client', {})
        region = data.get('region', '-')
        abonent_type = data.get('abonent_type', '-')
        abonent_id = data.get('abonent_id', '-')
        description = data.get('description', '-')
        address = data.get('address', '-')
        
        # Muammo turini aniqlash (description asosida)
        problem_type = 'standard'
        if 'uskunalar' in description.lower() or 'modem' in description.lower() or 'router' in description.lower():
            problem_type = 'equipment'
        elif 'murakkab' in description.lower() or 'kabel' in description.lower():
            problem_type = 'complex'
        
        # Calculate costs
        costs = calculate_technical_service_cost(abonent_type, problem_type)
        
        # Format costs for display
        def format_sum(amount):
            return f"{amount:,}".replace(',', ' ')
        geo = data.get('geo')
        media = data.get('media')

        text = (
            f"👤 <b>Mijoz:</b> {selected_client.get('full_name','N/A')}\n"
            f"📱 <b>Telefon:</b> {selected_client.get('phone','N/A')}\n"
            f"🏛️ <b>Hudud:</b> {region}\n"
            f"👤 <b>Abonent turi:</b> {abonent_type}\n"
            f"🆔 <b>Abonent ID:</b> {abonent_id}\n"
            f"📝 <b>Muammo tavsifi:</b> {description}\n"
            f"🏠 <b>Manzil:</b> {address}\n"
            f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}\n"
            f"🖼 <b>Media:</b> {'✅ Yuborilgan' if media else '❌ Yuborilmagan'}\n"
            f"\n💰 <b>Taxminiy xizmat narxi:</b>\n"
            f"├ Chiqish: {format_sum(costs['visit_fee'])} so'm\n"
            f"├ Ta'mirlash: {format_sum(costs['repair_fee'])} so'm\n"
            f"├ Ehtiyot qismlar: {format_sum(costs['parts_fee'])} so'm\n"
            f"└ <b>Jami:</b> {format_sum(costs['total'])} so'm"
        )

        if hasattr(message_or_callback, 'message'):
            await message_or_callback.message.answer(text, parse_mode='HTML', reply_markup=get_manager_confirmation_keyboard('uz'))
        else:
            await message_or_callback.answer(text, parse_mode='HTML', reply_markup=get_manager_confirmation_keyboard('uz'))
        await state.set_state(ManagerServiceOrderStates.confirming_order)

    @router.callback_query(F.data == "mgr_confirm_zayavka", StateFilter(ManagerServiceOrderStates.confirming_order))
    async def mgr_confirm_service_order(callback: CallbackQuery, state: FSMContext):
        try:
            try:
                await callback.message.edit_reply_markup(reply_markup=None)
            except Exception:
                pass
            
            data = await state.get_data()
            selected_client = data.get('selected_client', {})
            region = data.get('region', 'toshkent')
            abonent_type = data.get('abonent_type', 'internet')
            abonent_id = data.get('abonent_id', '')
            description = data.get('description', '')
            address = data.get('address', '')
            geo = data.get('geo')
            media = data.get('media')
            
            # Muammo turini aniqlash
            problem_type = 'standard'
            if 'uskunalar' in description.lower() or 'modem' in description.lower():
                problem_type = 'equipment'
            elif 'murakkab' in description.lower() or 'kabel' in description.lower():
                problem_type = 'complex'
            
            # Calculate costs
            costs = calculate_technical_service_cost(abonent_type, problem_type)
            
            # Get manager info
            manager = await get_user_by_telegram_id(region, callback.from_user.id)
            manager_id = manager.get('id') if manager else None
            
            # Prepare request data - MIJOZ NOMIDAN yaratiladi
            request_data = {
                'workflow_type': 'technical_service',
                'client_id': selected_client.get('id'),  # Mijoz ID
                'role_current': 'technician',  # To'g'ridan-to'g'ri technician'ga
                'current_status': 'created',
                'priority': 'medium',
                'description': description,
                'location': address,
                'contact_info': json.dumps({
                    'full_name': selected_client.get('full_name'),
                    'phone': selected_client.get('phone'),
                    'address': address,
                    'abonent_id': abonent_id
                }),
                'state_data': json.dumps({
                    'abonent_type': abonent_type,
                    'abonent_id': abonent_id,
                    'problem_type': problem_type,
                    'costs': costs,
                    'region': region,
                    'geo': {
                        'lat': geo.latitude if geo else None,
                        'lon': geo.longitude if geo else None
                    } if geo else None,
                    'media_file_id': media,
                    'created_via': 'manager_assistance',  # Manager yordam bergani
                    'assisted_by': manager_id
                }),
                'created_by_staff': True,  # Staff yaratgan
                'staff_creator_id': manager_id,  # Kim yaratgan
                'staff_creator_role': 'manager',
                'creation_source': 'client'  # Lekin mijoz nomidan
            }
            
            # Create service request in database
            request_id = await create_service_request(region, request_data)
            
            if request_id:
                # Log action
                await audit_logger.log_manager_action(
                    manager_id=manager_id or callback.from_user.id,
                    action='create_technical_service_order',
                    target_type='service_request',
                    target_id=request_id,
                    details={
                        'client_id': selected_client.get('id'),
                        'abonent_type': abonent_type,
                        'problem_type': problem_type,
                        'total_cost': costs['total']
                    }
                )
                
                await callback.answer("✅ Ariza yaratildi!", show_alert=True)
                
                # Format success message
                def format_sum(amount):
                    return f"{amount:,}".replace(',', ' ')
                
                success_msg = (
                    f"✅ <b>Mijoz nomidan texnik xizmat arizasi yaratildi!</b>\n\n"
                    f"📋 <b>Ariza raqami:</b> <code>{request_id}</code>\n"
                    f"👤 <b>Mijoz:</b> {selected_client.get('full_name','N/A')}\n"
                    f"📱 <b>Telefon:</b> {selected_client.get('phone','N/A')}\n"
                    f"🆔 <b>Abonent ID:</b> {abonent_id}\n"
                    f"📝 <b>Muammo:</b> {description[:50]}...\n"
                    f"🏠 <b>Manzil:</b> {address}\n\n"
                    f"💰 <b>Taxminiy narx:</b>\n"
                    f"├ Chiqish: {format_sum(costs['visit_fee'])} so'm\n"
                    f"├ Ta'mirlash: {format_sum(costs['repair_fee'])} so'm\n"
                    f"└ Jami: {format_sum(costs['total'])} so'm\n\n"
                    f"📅 <b>Yaratilgan vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                    f"🔄 <b>Status:</b> Technician'ga yuborildi\n"
                    f"👨‍💼 <b>Manager:</b> {manager.get('full_name', 'N/A')}\n\n"
                    f"Texnik xodimlar tez orada mijoz bilan bog'lanadi."
                )
                await callback.message.answer(success_msg, parse_mode='HTML')
            else:
                await callback.answer("❌ Xatolik yuz berdi!", show_alert=True)
                await callback.message.answer("❌ Ariza yaratishda xatolik yuz berdi. Qayta urinib ko'ring.")
            
            await state.clear()
            
        except Exception as e:
            logger.error(f"Error creating technical service order: {e}")
            await callback.answer("❌ Texnik xatolik yuz berdi!", show_alert=True)

    @router.callback_query(F.data == "mgr_resend_zayavka", StateFilter(ManagerServiceOrderStates.confirming_order))
    async def mgr_resend_service_summary(callback: CallbackQuery, state: FSMContext):
        await callback.answer()
        await mgr_show_service_confirmation(callback, state)

    return router 