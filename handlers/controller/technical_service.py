"""
Controller Technical Service - Mock Data Implementation

Allows controller to create a technical service request on behalf of a client.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

import logging
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
import uuid

from filters.role_filter import RoleFilter
from states.controller_states import ControllerServiceOrderStates, ControllerApplicationStates
from keyboards.controllers_buttons import (
    get_controller_regions_keyboard,
    controller_zayavka_type_keyboard,
    controller_media_attachment_keyboard,
    controller_geolocation_keyboard,
    controller_confirmation_keyboard,
    get_application_creator_keyboard,
)

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

# Mock clients data
mock_clients = [
    {
        'id': 1,
        'full_name': 'Alisher Karimov',
        'phone': '+998901234567',
        'phone_number': '+998901234567',
        'abonent_id': 'AB001',
        'region': 'toshkent',
        'created_at': '2024-01-15 10:30:00'
    },
    {
        'id': 2,
        'full_name': 'Dilfuza Rahimova',
        'phone': '+998901234568',
        'phone_number': '+998901234568',
        'abonent_id': 'AB002',
        'region': 'toshkent',
        'created_at': '2024-01-14 14:20:00'
    },
    {
        'id': 3,
        'full_name': 'Jamshid Toshmatov',
        'phone': '+998901234569',
        'phone_number': '+998901234569',
        'abonent_id': 'AB003',
        'region': 'toshkent',
        'created_at': '2024-01-13 09:15:00'
    },
    {
        'id': 4,
        'full_name': 'Malika Yusupova',
        'phone': '+998901234570',
        'phone_number': '+998901234570',
        'abonent_id': 'AB004',
        'region': 'toshkent',
        'created_at': '2024-01-12 16:45:00'
    },
    {
        'id': 5,
        'full_name': 'Rustam Azimov',
        'phone': '+998901234571',
        'phone_number': '+998901234571',
        'abonent_id': 'AB005',
        'region': 'toshkent',
        'created_at': '2024-01-11 11:30:00'
    }
]

# Mock service requests storage
mock_service_requests = {}
mock_request_counter = 1000

# Mock functions
async def get_user_by_telegram_id(region: str, telegram_id: int):
    """Mock get user by telegram ID"""
    return mock_users.get(telegram_id, {
        'id': 999,
        'telegram_id': telegram_id,
        'role': 'controller',
        'region': region,
        'full_name': 'Unknown User'
    })

async def search_users(region: str, search_term: str, search_type: str = 'phone'):
    """Mock search users"""
    try:
        if search_type == 'phone':
            return [c for c in mock_clients if search_term in c['phone']]
        elif search_type == 'name':
            return [c for c in mock_clients if search_term.lower() in c['full_name'].lower()]
        elif search_type == 'abonent_id':
            return [c for c in mock_clients if search_term in c['abonent_id']]
        return []
    except Exception as e:
        logger.error(f"Error searching users: {e}")
        return []

async def get_user(user_id: int, region: str):
    """Mock get user by ID"""
    return next((c for c in mock_clients if c['id'] == user_id), None)

async def get_user_by_phone(phone: str, region: str):
    """Mock get user by phone"""
    return next((c for c in mock_clients if c['phone'] == phone), None)

async def get_user_by_abonent_id(abonent_id: str, region: str):
    """Mock get user by abonent ID"""
    return next((c for c in mock_clients if c['abonent_id'] == abonent_id), None)

async def create_or_update_user(region: str, user_data: dict):
    """Mock create or update user"""
    try:
        if 'id' in user_data:
            # Update existing user
            for i, client in enumerate(mock_clients):
                if client['id'] == user_data['id']:
                    mock_clients[i].update(user_data)
                    logger.info(f"Mock: Updated user {user_data['id']}")
                    return True
        else:
            # Create new user
            new_id = max(c['id'] for c in mock_clients) + 1
            new_user = {
                'id': new_id,
                'region': region,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            new_user.update(user_data)
            mock_clients.append(new_user)
            logger.info(f"Mock: Created new user {new_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error in create_or_update_user: {e}")
        return False

async def create_service_request(region: str, request_data: dict):
    """Mock create service request"""
    try:
        global mock_request_counter
        mock_request_counter += 1
        
        # Store the request
        request_id = request_data['id']
        mock_service_requests[request_id] = {
            **request_data,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'mock_id': mock_request_counter
        }
        
        logger.info(f"Mock: Created service request {request_id}")
        return True
    except Exception as e:
        logger.error(f"Error creating service request: {e}")
        return False

async def get_service_request(request_id: str, region: str):
    """Mock get service request"""
    return mock_service_requests.get(request_id)

# Mock audit logger
class MockAuditLogger:
    """Mock audit logger"""
    async def log_action(self, user_id: int, action: str, details: dict = None, entity_type: str = None, entity_id: str = None, region: str = None):
        """Mock log action"""
        logger.info(f"Mock audit log: User {user_id} performed {action}")
        if details:
            logger.info(f"Mock: Details: {details}")
        if entity_type:
            logger.info(f"Mock: Entity type: {entity_type}")
        if entity_id:
            logger.info(f"Mock: Entity ID: {entity_id}")
        if region:
            logger.info(f"Mock: Region: {region}")

audit_logger = MockAuditLogger()

# Mock user region function
async def get_user_region(user_id: int):
    """Mock get user region"""
    user = mock_users.get(user_id, {})
    return user.get('region', 'toshkent')

def get_controller_technical_service_router():
    router = Router()

    # Role guard
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    # 1) Entry: show search method selector
    @router.message(F.text.in_(["🔧 Texnik xizmat yaratish"]))
    async def new_service_request(message: Message, state: FSMContext):
        try:
            region = await get_user_region(message.from_user.id)
            if not region:
                await message.answer("❌ Region aniqlanmadi")
                return
                
            user = await get_user_by_telegram_id(region, message.from_user.id)
            if not user or user.get('role') != 'controller':
                await message.answer("Sizda ruxsat yo'q.")
                return

            await state.update_data(current_flow='technical', controller_region=region)
            await message.answer(
                "Mijozni qanday qidiramiz?",
                reply_markup=get_application_creator_keyboard('uz')
            )
            await state.set_state(ControllerApplicationStates.selecting_client_search_method)
            
            # Log action
            await audit_logger.log_action(
                user_id=message.from_user.id,
                action='CONTROLLER_ACTION',
                details={'action': 'started_technical_service'},
                region=region
            )
        except Exception as e:
            logger.error(f"Error in new_service_request: {e}")
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    # 2) Technical service flow (after client selected by connection_service search handlers)
    @router.callback_query(F.data.startswith("ctrl_region_"), StateFilter(ControllerServiceOrderStates.selecting_region))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            region = callback.data.replace("ctrl_region_", "")
            await state.update_data(service_region=region)

            await callback.message.answer(
                "Abonent turini tanlang:",
                reply_markup=controller_zayavka_type_keyboard('uz')
            )
            await state.set_state(ControllerServiceOrderStates.selecting_order_type)
        except Exception as e:
            logger.error(f"Error in select_region: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("ctrl_zayavka_type_"), StateFilter(ControllerServiceOrderStates.selecting_order_type))
    async def select_abonent_type(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            abonent_type = callback.data.replace("ctrl_zayavka_type_", "")
            await state.update_data(abonent_type=abonent_type)

            await callback.message.answer("Abonent ID raqamini kiriting:")
            await state.set_state(ControllerServiceOrderStates.waiting_for_abonent_id)
        except Exception as e:
            logger.error(f"Error in select_abonent_type: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.message(StateFilter(ControllerServiceOrderStates.waiting_for_abonent_id))
    async def get_abonent_id(message: Message, state: FSMContext):
        try:
            abonent_id = message.text.strip()
            await state.update_data(abonent_id=abonent_id)
            
            # Update client's abonent_id in mock data if needed
            data = await state.get_data()
            selected_client = data.get('selected_client', {})
            controller_region = data.get('controller_region')
            
            if selected_client and controller_region:
                # Update client's abonent_id
                client_update = {
                    'id': selected_client.get('id'),
                    'abonent_id': abonent_id
                }
                await create_or_update_user(controller_region, client_update)
            
            await message.answer("Muammo tavsifini kiriting:")
            await state.set_state(ControllerServiceOrderStates.entering_description)
        except Exception as e:
            logger.error(f"Error in get_abonent_id: {e}")
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.message(StateFilter(ControllerServiceOrderStates.entering_description))
    async def get_service_description(message: Message, state: FSMContext):
        try:
            await state.update_data(description=message.text)

            await message.answer(
                "Foto yoki video yuborasizmi?",
                reply_markup=controller_media_attachment_keyboard('uz')
            )
            await state.set_state(ControllerServiceOrderStates.asking_for_media)
        except Exception as e:
            logger.error(f"Error in get_service_description: {e}")
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.callback_query(F.data.in_(["ctrl_attach_media_yes", "ctrl_attach_media_no"]), StateFilter(ControllerServiceOrderStates.asking_for_media))
    async def ask_for_media(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            if callback.data == "ctrl_attach_media_yes":
                await callback.message.answer("Foto yoki videoni yuboring:")
                await state.set_state(ControllerServiceOrderStates.waiting_for_media)
            else:
                await ask_for_address(callback, state)
        except Exception as e:
            logger.error(f"Error in ask_for_media: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.message(StateFilter(ControllerServiceOrderStates.waiting_for_media), F.photo | F.video)
    async def process_media(message: Message, state: FSMContext):
        try:
            media_file_id = message.photo[-1].file_id if message.photo else message.video.file_id
            media_type = 'photo' if message.photo else 'video'
            await state.update_data(media=media_file_id, media_type=media_type)
            await ask_for_address(message, state)
        except Exception as e:
            logger.error(f"Error in process_media: {e}")
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    async def ask_for_address(message_or_callback, state: FSMContext):
        try:
            if hasattr(message_or_callback, "message"):
                await message_or_callback.message.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
            else:
                await message_or_callback.answer("Xizmat ko'rsatiladigan manzilni kiriting:")
            await state.set_state(ControllerServiceOrderStates.entering_address)
        except Exception as e:
            logger.error(f"Error in ask_for_address: {e}")
            if hasattr(message_or_callback, "message"):
                await message_or_callback.message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")
            else:
                await message_or_callback.message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.message(StateFilter(ControllerServiceOrderStates.entering_address))
    async def get_service_address(message: Message, state: FSMContext):
        try:
            await state.update_data(address=message.text)
            await message.answer(
                "Geolokatsiya yuborasizmi?",
                reply_markup=controller_geolocation_keyboard('uz')
            )
            await state.set_state(ControllerServiceOrderStates.asking_for_location)
        except Exception as e:
            logger.error(f"Error in get_service_address: {e}")
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.callback_query(F.data.in_(["ctrl_send_location_yes", "ctrl_send_location_no"]), StateFilter(ControllerServiceOrderStates.asking_for_location))
    async def ask_for_geo(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            if callback.data == "ctrl_send_location_yes":
                await callback.message.answer("Geolokatsiyani yuboring:")
                await state.set_state(ControllerServiceOrderStates.waiting_for_location)
            else:
                await show_service_confirmation(callback, state)
        except Exception as e:
            logger.error(f"Error in ask_for_geo: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.message(StateFilter(ControllerServiceOrderStates.waiting_for_location), F.location)
    async def get_geo(message: Message, state: FSMContext):
        try:
            geo_data = {
                'latitude': message.location.latitude,
                'longitude': message.location.longitude
            }
            await state.update_data(geo=geo_data)
            await show_service_confirmation(message, state)
        except Exception as e:
            logger.error(f"Error in get_geo: {e}")
            await message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    async def show_service_confirmation(message_or_callback, state: FSMContext):
        try:
            data = await state.get_data()
            selected_client = data.get('selected_client', {})
            service_region = data.get('service_region', '-')
            abonent_type = data.get('abonent_type', '-')
            abonent_id = data.get('abonent_id', '-')
            description = data.get('description', '-')
            address = data.get('address', '-')
            geo = data.get('geo')
            media = data.get('media')

            text = (
                f"👤 <b>Mijoz:</b> {selected_client.get('full_name','N/A')}\n"
                f"🏛️ <b>Hudud:</b> {service_region}\n"
                f"👤 <b>Abonent turi:</b> {abonent_type}\n"
                f"🆔 <b>Abonent ID:</b> {abonent_id}\n"
                f"📝 <b>Muammo tavsifi:</b> {description}\n"
                f"🏠 <b>Manzil:</b> {address}\n"
                f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}\n"
                f"🖼 <b>Media:</b> {'✅ Yuborilgan' if media else '❌ Yuborilmagan'}"
            )

            if hasattr(message_or_callback, 'message'):
                await message_or_callback.message.answer(text, parse_mode='HTML', reply_markup=controller_confirmation_keyboard('uz'))
            else:
                await message_or_callback.answer(text, parse_mode='HTML', reply_markup=controller_confirmation_keyboard('uz'))
            await state.set_state(ControllerServiceOrderStates.confirming_order)
        except Exception as e:
            logger.error(f"Error in show_service_confirmation: {e}")
            if hasattr(message_or_callback, 'message'):
                await message_or_callback.message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")
            else:
                await message_or_callback.message.answer("Xatolik yuz berdi. Qayta urinib ko'ring.")

    @router.callback_query(F.data == "ctrl_confirm_zayavka", StateFilter(ControllerServiceOrderStates.confirming_order))
    async def confirm_service_order(callback: CallbackQuery, state: FSMContext):
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
            request_id = f"TECH_{str(uuid.uuid4())[:8].upper()}"
            
            # Prepare request data
            request_data = {
                'id': request_id,
                'workflow_type': 'technical_service',
                'client_id': selected_client.get('id'),
                'role_current': 'controller',  # Assigned to controller first for tech assignment
                'current_status': 'created',
                'priority': 'medium',
                'description': data.get('description', ''),
                'location': data.get('address', ''),
                'contact_info': {
                    'phone': selected_client.get('phone', selected_client.get('phone_number')),
                    'name': selected_client.get('full_name'),
                    'abonent_id': data.get('abonent_id')
                },
                'state_data': {
                    'abonent_type': data.get('abonent_type'),
                    'abonent_id': data.get('abonent_id'),
                    'service_region': service_region,
                    'geo': data.get('geo'),
                    'media': data.get('media'),
                    'media_type': data.get('media_type')
                },
                'created_by_staff': True,
                'staff_creator_id': callback.from_user.id,
                'staff_creator_role': 'controller',
                'creation_source': 'controller',
                'current_assignee_id': callback.from_user.id  # Assign to controller who created it
            }
            
            # Save media file ID if exists
            if data.get('media'):
                request_data['equipment_used'] = [{
                    'type': 'attachment',
                    'file_id': data.get('media'),
                    'file_type': data.get('media_type', 'photo')
                }]
            
            # Create request in mock data
            success = await create_service_request(service_region, request_data)
            
            if success:
                success_msg = (
                    "✅ Texnik xizmat arizasi muvaffaqiyatli yaratildi!\n"
                    f"📋 Ariza ID: {request_id}\n"
                    f"🏛️ Hudud: {service_region}\n"
                    f"👤 Mijoz: {selected_client.get('full_name')}\n"
                    f"🆔 Abonent ID: {data.get('abonent_id')}\n\n"
                    "Siz endi texnikni tayinlashingiz mumkin."
                )
                
                # Log action
                await audit_logger.log_action(
                    user_id=callback.from_user.id,
                    action='WORKFLOW_CREATED',
                    details={
                        'request_id': request_id,
                        'type': 'technical_service',
                        'client_id': selected_client.get('id'),
                        'abonent_id': data.get('abonent_id'),
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
            logger.error(f"Error in confirm_service_order: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "ctrl_resend_zayavka", StateFilter(ControllerServiceOrderStates.confirming_order))
    async def resend_service_summary(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            await show_service_confirmation(callback, state)
        except Exception as e:
            logger.error(f"Error in resend_service_summary: {e}")
            await callback.answer("Xatolik yuz berdi")

    return router
