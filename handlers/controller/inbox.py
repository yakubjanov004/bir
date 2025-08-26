"""
Controller Inbox - Mock Data Implementation

Bu modul controller uchun inbox funksionalligini o'z ichiga oladi.
Call center supervisor yoki texniklarga tayinlash funksiyasi bilan.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from datetime import datetime, timedelta
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from states.controller_states import ControllerRequestStates
from filters.role_filter import RoleFilter
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

# Mock controller applications
mock_controller_applications = [
    {
        'id': 'REQ001',
        'workflow_type': 'connection_request',
        'current_status': 'sent_to_controller',
        'contact_info': {
            'full_name': 'Aziz Karimov',
            'phone': '+998901234567'
        },
        'created_at': datetime.now() - timedelta(hours=2),
        'description': 'Yangi uy uchun internet xizmatini ulashish kerak. Uy Chilonzor tumanida joylashgan.',
        'location': 'Toshkent, Chilonzor tumani, 15-uy',
        'priority': 'high',
        'assigned_to': None,
        'state_data': {
            'tariff': 'Premium',
            'connection_type': 'B2C'
        }
    },
    {
        'id': 'REQ002',
        'workflow_type': 'technical_service',
        'current_status': 'pending_assignment',
        'contact_info': {
            'full_name': 'Malika Yusupova',
            'phone': '+998901234568'
        },
        'created_at': datetime.now() - timedelta(hours=4),
        'description': 'Internet tezligi juda sekin. Tezlik 1 Mbps ga tushib qoldi, 100 Mbps bo\'lishi kerak.',
        'location': 'Toshkent, Sergeli tumani, 25-uy',
        'priority': 'urgent',
        'assigned_to': None,
        'state_data': {
            'service_type': 'Speed Issue',
            'abonent_id': 'AB001'
        }
    },
    {
        'id': 'REQ003',
        'workflow_type': 'connection_request',
        'current_status': 'created',
        'contact_info': {
            'full_name': 'Jasur Toshmatov',
            'phone': '+998901234569'
        },
        'created_at': datetime.now() - timedelta(hours=6),
        'description': 'Biznes markaz uchun internet xizmati. 10 ta kompyuter uchun yuqori tezlik kerak.',
        'location': 'Toshkent, Yakkasaroy tumani, 8-uy',
        'priority': 'medium',
        'assigned_to': None,
        'state_data': {
            'tariff': 'Business',
            'connection_type': 'B2B'
        }
    },
    {
        'id': 'REQ004',
        'workflow_type': 'technical_service',
        'current_status': 'sent_to_controller',
        'contact_info': {
            'full_name': 'Dilfuza Rahimova',
            'phone': '+998901234570'
        },
        'created_at': datetime.now() - timedelta(hours=8),
        'description': 'TV kanallar ko\'rinmayapti. Signal yo\'q yoki juda zaif.',
        'location': 'Toshkent, Shayxontohur tumani, 12-uy',
        'priority': 'normal',
        'assigned_to': None,
        'state_data': {
            'service_type': 'TV Signal',
            'abonent_id': 'AB002'
        }
    },
    {
        'id': 'REQ005',
        'workflow_type': 'call_center_direct',
        'current_status': 'inbox',
        'contact_info': {
            'full_name': 'Rustam Alimov',
            'phone': '+998901234571'
        },
        'created_at': datetime.now() - timedelta(hours=1),
        'description': 'Telefon xizmati bilan bog\'liq muammo. Qo\'ng\'iroqlar o\'tmayapti.',
        'location': 'Toshkent, Uchtepa tumani, 30-uy',
        'priority': 'high',
        'assigned_to': None,
        'state_data': {}
    }
]

# Mock technicians
mock_technicians = [
    {
        'id': 2001,
        'full_name': 'Ahmad Texnik',
        'role': 'technician',
        'telegram_id': 987654321,
        'active_requests': 2,
        'specialization': 'Internet'
    },
    {
        'id': 2002,
        'full_name': 'Bakhtiyor Texnik',
        'role': 'technician',
        'telegram_id': 987654322,
        'active_requests': 1,
        'specialization': 'TV'
    },
    {
        'id': 2003,
        'full_name': 'Davron Texnik',
        'role': 'technician',
        'telegram_id': 987654323,
        'active_requests': 0,
        'specialization': 'Umumiy'
    },
    {
        'id': 2004,
        'full_name': 'Eldor Texnik',
        'role': 'technician',
        'telegram_id': 987654324,
        'active_requests': 3,
        'specialization': 'Internet'
    }
]

# Mock call center supervisors
mock_call_center_supervisors = [
    {
        'id': 3001,
        'full_name': 'Malika Supervisor',
        'role': 'call_center_supervisor',
        'telegram_id': 987654325,
        'is_active': True
    },
    {
        'id': 3002,
        'full_name': 'Jasur Supervisor',
        'role': 'call_center_supervisor',
        'telegram_id': 987654326,
        'is_active': True
    }
]

# Mock utility classes
class MockAuditLogger:
    """Mock audit logger"""
    async def log_action(self, user_id: int, action: str, details: dict = None, entity_type: str = None, entity_id: str = None, region: str = None):
        """Mock log action"""
        logger.info(f"Mock: User {user_id} performed action: {action}")
        if details:
            logger.info(f"Mock: Details: {details}")

class MockWorkflowEngine:
    """Mock workflow engine"""
    async def transition_request(self, region: str, request_id: str, action: str, actor_id: int, target_user_id: int = None):
        """Mock workflow transition"""
        logger.info(f"Mock: Workflow transition for request {request_id}: {action}")

# Initialize mock instances
audit_logger = MockAuditLogger()
workflow_engine = MockWorkflowEngine()

# Mock functions
async def get_user_by_telegram_id(region: str, telegram_id: int):
    """Mock get user by telegram ID"""
    logger.info(f"Mock: Getting user by telegram ID {telegram_id} in region {region}")
    return mock_users.get(telegram_id)

async def get_user_region(telegram_id: int):
    """Mock get user region"""
    user = mock_users.get(telegram_id)
    return user.get('region') if user else None

async def get_controller_applications(region: str, controller_id: int):
    """Mock get controller applications"""
    logger.info(f"Mock: Getting controller applications for controller {controller_id} in region {region}")
    return mock_controller_applications

async def get_users_by_role(region: str, role: str):
    """Mock get users by role"""
    logger.info(f"Mock: Getting users by role {role} in region {region}")
    if role == 'technician':
        return mock_technicians
    elif role == 'call_center_supervisor':
        return mock_call_center_supervisors
    return []

async def assign_request_to_technician(region: str, request_id: str, technician_id: int, controller_id: int):
    """Mock assign request to technician"""
    logger.info(f"Mock: Assigning request {request_id} to technician {technician_id} by controller {controller_id}")
    
    # Find and update the request
    for app in mock_controller_applications:
        if app['id'] == request_id:
            app['assigned_to'] = technician_id
            app['current_status'] = 'assigned_to_technician'
            app['updated_at'] = datetime.now()
            return True
    return False

async def update_service_request(region: str, request_id: str, update_data: dict):
    """Mock update service request"""
    logger.info(f"Mock: Updating service request {request_id} with data: {update_data}")
    
    # Find and update the request
    for app in mock_controller_applications:
        if app['id'] == request_id:
            app.update(update_data)
            return True
    return False

def get_controller_inbox_router():
    """Get controller inbox router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📥 Inbox", "📥 Входящие"]))
    async def controller_inbox(message: Message, state: FSMContext):
        """Controller inbox handler"""
        try:
            # Get region
            region = await get_user_region(message.from_user.id)
            if not region:
                await message.answer("❌ Region aniqlanmadi")
                return
            
            user = await get_user_by_telegram_id(region, message.from_user.id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Get applications from mock data
            applications = await get_controller_applications(region, controller_id)
            
            # Log action
            await audit_logger.log_action(
                user_id=message.from_user.id,
                action='CONTROLLER_ACTION',
                details={'action': 'viewed_inbox', 'count': len(applications)},
                region=region
            )
            
            if not applications:
                if lang == 'uz':
                    await message.answer(
                        "📥 <b>Inbox</b>\n\n"
                        "Hozircha yangi arizalar yo'q.",
                        parse_mode='HTML'
                    )
                else:
                    await message.answer(
                        "📥 <b>Входящие</b>\n\n"
                        "Пока нет новых заявок.",
                        parse_mode='HTML'
                    )
                return
            
            # Display applications
            for app in applications[:5]:  # Show first 5
                await display_application(message, app, lang, region)
            
            if len(applications) > 5:
                if lang == 'uz':
                    await message.answer(
                        f"📊 Jami {len(applications)} ta ariza mavjud.\n"
                        f"Faqat birinchi 5 tasi ko'rsatildi.",
                        parse_mode='HTML'
                    )
                else:
                    await message.answer(
                        f"📊 Всего {len(applications)} заявок.\n"
                        f"Показаны только первые 5.",
                        parse_mode='HTML'
                    )
            
            await state.set_state(ControllerRequestStates.viewing_inbox)
            
        except Exception as e:
            logger.error(f"Error in controller_inbox: {e}")
            await message.answer("❌ Xatolik yuz berdi")

    async def display_application(message_or_callback, app, lang, region):
        """Display single application"""
        try:
            # Format time
            created_at = app.get('created_at')
            if isinstance(created_at, datetime):
                time_str = created_at.strftime('%d.%m.%Y %H:%M')
                time_diff = datetime.now() - created_at
                hours_ago = int(time_diff.total_seconds() / 3600)
                if hours_ago < 1:
                    time_ago = f"{int(time_diff.total_seconds() / 60)} daqiqa oldin"
                elif hours_ago < 24:
                    time_ago = f"{hours_ago} soat oldin"
                else:
                    time_ago = f"{int(hours_ago / 24)} kun oldin"
            else:
                time_str = 'N/A'
                time_ago = ''
            
            # Get workflow type emoji
            workflow_emoji = {
                'connection_request': '🌐',
                'technical_service': '🔧',
                'call_center_direct': '📞',
                'unknown': '📋'
            }.get(app.get('workflow_type', 'unknown'), '📋')
            
            # Get priority emoji
            priority_emoji = {
                'urgent': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'normal': '🟢',
                'low': '⚪'
            }.get(app.get('priority', 'normal'), '⚪')
            
            # Format contact info
            contact = app.get('contact_info', {})
            client_name = contact.get('full_name') or contact.get('name') or 'Noma\'lum'
            client_phone = contact.get('phone') or contact.get('phone_number') or 'N/A'
            
            if lang == 'uz':
                text = (
                    f"{workflow_emoji} <b>Ariza #{app['id']}</b>\n"
                    f"{priority_emoji} Muhimlik: {app.get('priority', 'normal')}\n\n"
                    f"👤 <b>Mijoz:</b> {client_name}\n"
                    f"📞 <b>Telefon:</b> {client_phone}\n"
                    f"📍 <b>Manzil:</b> {app.get('location', 'Ko\'rsatilmagan')}\n"
                    f"📝 <b>Tavsif:</b>\n{app.get('description', 'Tavsif yo\'q')}\n"
                    f"🕐 <b>Yaratilgan:</b> {time_str}"
                )
                if time_ago:
                    text += f" ({time_ago})"
            else:
                text = (
                    f"{workflow_emoji} <b>Заявка #{app['id']}</b>\n"
                    f"{priority_emoji} Приоритет: {app.get('priority', 'normal')}\n\n"
                    f"👤 <b>Клиент:</b> {client_name}\n"
                    f"📞 <b>Телефон:</b> {client_phone}\n"
                    f"📍 <b>Адрес:</b> {app.get('location', 'Не указан')}\n"
                    f"📝 <b>Описание:</b>\n{app.get('description', 'Нет описания')}\n"
                    f"🕐 <b>Создано:</b> {time_str}"
                )
                if time_ago:
                    text += f" ({time_ago})"
            
            # Add workflow-specific info
            if app.get('workflow_type') == 'connection_request':
                if lang == 'uz':
                    text += f"\n\n💼 <b>Turi:</b> Ulanish so'rovi"
                    text += f"\n📊 <b>Tarif:</b> {app.get('state_data', {}).get('tariff', 'Standard')}"
                    text += f"\n🏢 <b>Mijoz turi:</b> {app.get('state_data', {}).get('connection_type', 'B2C')}"
                else:
                    text += f"\n\n💼 <b>Тип:</b> Заявка на подключение"
                    text += f"\n📊 <b>Тариф:</b> {app.get('state_data', {}).get('tariff', 'Standard')}"
                    text += f"\n🏢 <b>Тип клиента:</b> {app.get('state_data', {}).get('connection_type', 'B2C')}"
            elif app.get('workflow_type') == 'technical_service':
                if lang == 'uz':
                    text += f"\n\n💼 <b>Turi:</b> Texnik xizmat"
                    if app.get('state_data', {}).get('abonent_id'):
                        text += f"\n🆔 <b>Abonent ID:</b> {app.get('state_data', {}).get('abonent_id')}"
                else:
                    text += f"\n\n💼 <b>Тип:</b> Техническое обслуживание"
                    if app.get('state_data', {}).get('abonent_id'):
                        text += f"\n🆔 <b>ID абонента:</b> {app.get('state_data', {}).get('abonent_id')}"
            
            # Create action buttons
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="👷 Texnikka tayinlash" if lang == 'uz' else "👷 Назначить технику",
                        callback_data=f"assign_tech_{app['id']}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📞 Call Center'ga yuborish" if lang == 'uz' else "📞 Отправить в Call Center",
                        callback_data=f"send_callcenter_{app['id']}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Bekor qilish" if lang == 'uz' else "❌ Отменить",
                        callback_data=f"cancel_request_{app['id']}"
                    )
                ]
            ])
            
            # Send message
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.answer(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            logger.error(f"Error displaying application: {e}")

    @router.callback_query(F.data.startswith("assign_tech_"))
    async def assign_to_technician(callback: CallbackQuery, state: FSMContext):
        """Assign request to technician"""
        try:
            await callback.answer()
            
            request_id = callback.data.replace("assign_tech_", "")
            
            # Get region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # Get available technicians from mock data
            technicians = await get_users_by_role(region, 'technician')
            
            if not technicians:
                if lang == 'uz':
                    await callback.message.answer("❌ Hozircha mavjud texniklar yo'q")
                else:
                    await callback.message.answer("❌ Нет доступных техников")
                return
            
            # Create technician selection keyboard
            keyboard_buttons = []
            for tech in technicians:
                tech_text = f"👷 {tech['full_name']}"
                if tech.get('active_requests', 0) > 0:
                    tech_text += f" ({tech['active_requests']} ta ish)"
                else:
                    tech_text += " (bo'sh)"
                
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text=tech_text,
                        callback_data=f"confirm_tech_{request_id}_{tech['id']}"
                    )
                ])
            
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
                    callback_data="back_to_inbox"
                )
            ])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
            
            if lang == 'uz':
                text = f"📋 <b>Ariza #{request_id}</b>\n\n👷 Texnikni tanlang:"
            else:
                text = f"📋 <b>Заявка #{request_id}</b>\n\n👷 Выберите техника:"
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in assign_to_technician: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("confirm_tech_"))
    async def confirm_technician_assignment(callback: CallbackQuery, state: FSMContext):
        """Confirm technician assignment"""
        try:
            await callback.answer()
            
            # Parse data
            parts = callback.data.replace("confirm_tech_", "").split("_")
            request_id = parts[0]
            technician_id = int(parts[1])
            
            # Get region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Assign request to technician in mock data
            success = await assign_request_to_technician(
                region=region,
                request_id=request_id,
                technician_id=technician_id,
                controller_id=controller_id
            )
            
            if success:
                # Log action
                await audit_logger.log_action(
                    user_id=callback.from_user.id,
                    action='TECHNICIAN_ASSIGNED',
                    details={
                        'request_id': request_id,
                        'technician_id': technician_id,
                        'controller_id': controller_id
                    },
                    entity_type='service_request',
                    entity_id=request_id,
                    region=region
                )
                
                # Update workflow
                await workflow_engine.transition_request(
                    region=region,
                    request_id=request_id,
                    action='ASSIGN_TO_TECHNICIAN',
                    actor_id=controller_id,
                    target_user_id=technician_id
                )
                
                if lang == 'uz':
                    success_text = (
                        f"✅ <b>Muvaffaqiyatli tayinlandi!</b>\n\n"
                        f"📋 Ariza #{request_id}\n"
                        f"👷 Texnikka tayinlandi\n\n"
                        f"Texnik xabardor qilindi."
                    )
                else:
                    success_text = (
                        f"✅ <b>Успешно назначено!</b>\n\n"
                        f"📋 Заявка #{request_id}\n"
                        f"👷 Назначена технику\n\n"
                        f"Техник уведомлен."
                    )
                
                await callback.message.edit_text(success_text, parse_mode='HTML')
                
                # Notify technician (mock)
                try:
                    technicians = await get_users_by_role(region, 'technician')
                    tech = next((t for t in technicians if t['id'] == technician_id), None)
                    if tech and tech.get('telegram_id'):
                        logger.info(f"Mock: Notifying technician {tech['full_name']} about assignment")
                except Exception as notify_error:
                    logger.error(f"Error notifying technician: {notify_error}")
                
            else:
                if lang == 'uz':
                    await callback.message.answer("❌ Tayinlashda xatolik yuz berdi")
                else:
                    await callback.message.answer("❌ Ошибка при назначении")
            
        except Exception as e:
            logger.error(f"Error in confirm_technician_assignment: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("send_callcenter_"))
    async def send_to_callcenter(callback: CallbackQuery, state: FSMContext):
        """Send request to call center"""
        try:
            await callback.answer()
            
            request_id = callback.data.replace("send_callcenter_", "")
            
            # Get region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Update request status in mock data
            update_data = {
                'current_status': 'sent_to_call_center',
                'role_current': 'call_center',
                'updated_at': datetime.now()
            }
            
            success = await update_service_request(region, request_id, update_data)
            
            if success:
                # Log action
                await audit_logger.log_action(
                    user_id=callback.from_user.id,
                    action='WORKFLOW_TRANSFERRED',
                    details={
                        'request_id': request_id,
                        'from_role': 'controller',
                        'to_role': 'call_center'
                    },
                    entity_type='service_request',
                    entity_id=request_id,
                    region=region
                )
                
                if lang == 'uz':
                    success_text = (
                        f"✅ <b>Call Center'ga yuborildi!</b>\n\n"
                        f"📋 Ariza #{request_id}\n"
                        f"📞 Call Center xodimlari ko'rib chiqadi."
                    )
                else:
                    success_text = (
                        f"✅ <b>Отправлено в Call Center!</b>\n\n"
                        f"📋 Заявка #{request_id}\n"
                        f"📞 Сотрудники Call Center рассмотрят."
                    )
                
                await callback.message.edit_text(success_text, parse_mode='HTML')
                
            else:
                if lang == 'uz':
                    await callback.message.answer("❌ Yuborishda xatolik yuz berdi")
                else:
                    await callback.message.answer("❌ Ошибка при отправке")
            
        except Exception as e:
            logger.error(f"Error in send_to_callcenter: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("cancel_request_"))
    async def cancel_request(callback: CallbackQuery, state: FSMContext):
        """Cancel request"""
        try:
            await callback.answer()
            
            request_id = callback.data.replace("cancel_request_", "")
            
            # Get region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Update request status in mock data
            update_data = {
                'current_status': 'cancelled',
                'cancelled_by': controller_id,
                'cancelled_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            success = await update_service_request(region, request_id, update_data)
            
            if success:
                # Log action
                await audit_logger.log_action(
                    user_id=callback.from_user.id,
                    action='WORKFLOW_CANCELLED',
                    details={
                        'request_id': request_id,
                        'cancelled_by': 'controller'
                    },
                    entity_type='service_request',
                    entity_id=request_id,
                    region=region
                )
                
                if lang == 'uz':
                    success_text = (
                        f"❌ <b>Ariza bekor qilindi!</b>\n\n"
                        f"📋 Ariza #{request_id}\n"
                        f"Bekor qilindi va arxivlandi."
                    )
                else:
                    success_text = (
                        f"❌ <b>Заявка отменена!</b>\n\n"
                        f"📋 Заявка #{request_id}\n"
                        f"Отменена и архивирована."
                    )
                
                await callback.message.edit_text(success_text, parse_mode='HTML')
                
            else:
                if lang == 'uz':
                    await callback.message.answer("❌ Bekor qilishda xatolik yuz berdi")
                else:
                    await callback.message.answer("❌ Ошибка при отмене")
            
        except Exception as e:
            logger.error(f"Error in cancel_request: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "back_to_inbox")
    async def back_to_inbox(callback: CallbackQuery, state: FSMContext):
        """Back to inbox"""
        try:
            await callback.answer()
            
            # Get region
            region = await get_user_region(callback.from_user.id)
            if not region:
                await callback.answer("Region aniqlanmadi", show_alert=True)
                return
            
            user = await get_user_by_telegram_id(region, callback.from_user.id)
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Get applications from mock data
            applications = await get_controller_applications(region, controller_id)
            
            if not applications:
                if lang == 'uz':
                    text = "📥 <b>Inbox</b>\n\nHozircha yangi arizalar yo'q."
                else:
                    text = "📥 <b>Входящие</b>\n\nПока нет новых заявок."
                
                await callback.message.edit_text(text, parse_mode='HTML')
                return
            
            # Show summary
            if lang == 'uz':
                text = (
                    f"📥 <b>Inbox</b>\n\n"
                    f"📊 Jami arizalar: {len(applications)}\n\n"
                    f"Arizalarni ko'rish uchun qayta /start bosing."
                )
            else:
                text = (
                    f"📥 <b>Входящие</b>\n\n"
                    f"📊 Всего заявок: {len(applications)}\n\n"
                    f"Для просмотра заявок нажмите /start снова."
                )
            
            await callback.message.edit_text(text, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in back_to_inbox: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router