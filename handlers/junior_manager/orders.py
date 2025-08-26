"""
Junior Manager Orders - Mock Data Implementation

Bu modul junior manager uchun arizalarni ko'rish va boshqarish funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from filters.role_filter import RoleFilter
from states.junior_manager_states import JuniorManagerOrderStates
from keyboards.junior_manager_buttons import (
    get_application_list_keyboard,
    get_application_action_keyboard,
    get_junior_manager_main_menu
)
import logging
import uuid

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

# Mock service requests
mock_service_requests = {
    'REQ001001': {
        'id': 'REQ001001',
        'workflow_type': 'connection_request',
        'current_status': 'assigned_to_junior_manager',
        'priority': 'high',
        'description': 'Internet ulanish arizasi - yangi uy uchun',
        'location': 'Toshkent shahri, Chilanzor tumani, 15-uy',
        'contact_info': {
            'full_name': 'Alisher Karimov',
            'phone': '+998901234567'
        },
        'state_data': {
            'notes': 'Mijoz internet xizmatini ulashishni xohlaydi',
            'contact_attempts': 0
        },
        'created_at': datetime.now() - timedelta(hours=2),
        'assigned_to': 1,
        'assigned_role': 'junior_manager',
        'staff_creator_id': 1,
        'current_assignee_id': 1
    },
    'REQ001002': {
        'id': 'REQ001002',
        'workflow_type': 'technical_service',
        'current_status': 'in_progress',
        'priority': 'medium',
        'description': 'TV signal muammosi - kanallar ko\'rinmayapti',
        'location': 'Toshkent shahri, Sergeli tumani, 25-uy',
        'contact_info': {
            'full_name': 'Dilfuza Rahimova',
            'phone': '+998901234568'
        },
        'state_data': {
            'notes': 'TV signal zaif, kanallar ko\'rinmayapti',
            'contact_attempts': 1,
            'last_contact_date': (datetime.now() - timedelta(hours=3)).isoformat(),
            'last_contact_note': 'Mijoz bilan bog\'landik, muammo tasdiqlandi'
        },
        'created_at': datetime.now() - timedelta(hours=5),
        'assigned_to': 1,
        'assigned_role': 'junior_manager',
        'staff_creator_id': 1,
        'current_assignee_id': 1
    },
    'REQ001003': {
        'id': 'REQ001003',
        'workflow_type': 'technical_service',
        'current_status': 'assigned_to_junior_manager',
        'priority': 'urgent',
        'description': 'Internet tezligi juda past',
        'location': 'Toshkent shahri, Yakkasaroy tumani, 8-uy',
        'contact_info': {
            'full_name': 'Jamshid Toshmatov',
            'phone': '+998901234569'
        },
        'state_data': {
            'notes': 'Internet tezligi 1 Mbps ga tushib qoldi',
            'contact_attempts': 0
        },
        'created_at': datetime.now() - timedelta(hours=1),
        'assigned_to': 1,
        'assigned_role': 'junior_manager',
        'staff_creator_id': 1,
        'current_assignee_id': 1
    },
    'REQ001004': {
        'id': 'REQ001004',
        'workflow_type': 'connection_request',
        'current_status': 'created',
        'priority': 'normal',
        'description': 'Yangi uy uchun internet va TV xizmati',
        'location': 'Toshkent shahri, Yunusabad tumani, 42-uy',
        'contact_info': {
            'full_name': 'Malika Yusupova',
            'phone': '+998901234570'
        },
        'state_data': {
            'notes': 'Yangi uy qurilgan, xizmat kerak',
            'contact_attempts': 0
        },
        'created_at': datetime.now() - timedelta(hours=8),
        'assigned_to': 1,
        'assigned_role': 'junior_manager',
        'staff_creator_id': 1,
        'current_assignee_id': 1
    }
}

# Mock workflow engine
class MockWorkflowEngine:
    """Mock workflow engine"""
    def __init__(self):
        self.workflows = []
        self.actions = []
    
    def process_action(self, workflow_id: str, action: str, actor_id: int, actor_role: str):
        """Mock process workflow action"""
        workflow_action = {
            'id': str(uuid.uuid4()),
            'workflow_id': workflow_id,
            'action': action,
            'actor_id': actor_id,
            'actor_role': actor_role,
            'timestamp': datetime.now().isoformat()
        }
        self.actions.append(workflow_action)
        logger.info(f"Mock: Processed action {action} for workflow {workflow_id}")

# Initialize mock instances
mock_workflow_engine = MockWorkflowEngine()

# Mock functions to replace database calls
async def get_user_by_telegram_id(user_id: int):
    """Mock get user by telegram ID"""
    return mock_users.get(user_id)

async def get_junior_manager_requests(region: str, manager_id: int):
    """Mock get junior manager requests"""
    try:
        requests = [req for req in mock_service_requests.values() 
                   if req.get('assigned_to') == manager_id and 
                   req.get('assigned_role') == 'junior_manager']
        return requests
    except Exception as e:
        logger.error(f"Mock: Error getting junior manager requests: {e}")
        return []

async def get_service_requests_by_assignee(region: str, assignee_id: int):
    """Mock get service requests by assignee"""
    try:
        requests = [req for req in mock_service_requests.values() 
                   if req.get('assigned_to') == assignee_id]
        return requests
    except Exception as e:
        logger.error(f"Mock: Error getting service requests by assignee: {e}")
        return []

async def get_service_request(region: str, request_id: str):
    """Mock get service request"""
    try:
        return mock_service_requests.get(request_id)
    except Exception as e:
        logger.error(f"Mock: Error getting service request: {e}")
        return None

async def update_service_request(region: str, request_id: str, update_data: Dict[str, Any]):
    """Mock update service request"""
    try:
        if request_id in mock_service_requests:
            mock_service_requests[request_id].update(update_data)
            logger.info(f"Mock: Updated service request {request_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Mock: Error updating service request: {e}")
        return False

async def create_on_assignment(region_code: str, application_id: str, assigned_role: str, 
                              title: str, description: str, priority: str, application_type: str):
    """Mock create inbox notification"""
    try:
        logger.info(f"Mock: Created inbox notification for {assigned_role} about {application_id}")
        return True
    except Exception as e:
        logger.error(f"Mock: Error creating inbox notification: {e}")
        return False

async def get_user_lang(user_id: int):
    """Mock get user language"""
    user = await get_user_by_telegram_id(user_id)
    return user.get('language', 'uz') if user else 'uz'

async def format_date(date_obj, lang: str = 'uz'):
    """Mock format date"""
    try:
        if isinstance(date_obj, str):
            return date_obj[:16]
        elif isinstance(date_obj, datetime):
            return date_obj.strftime('%d.%m.%Y %H:%M')
        else:
            return str(date_obj)
    except Exception as e:
        logger.error(f"Mock: Error formatting date: {e}")
        return str(date_obj)

# Create router
router = Router(name="junior_manager_orders")

# Apply role filter to all handlers
router.message.filter(RoleFilter(role="junior_manager"))
router.callback_query.filter(RoleFilter(role="junior_manager"))


async def get_junior_manager_applications(user_id: int, region: str) -> List[Dict[str, Any]]:
    """Get applications for junior manager - both created and assigned"""
    try:
        # Get applications created by junior manager
        created_apps = await get_junior_manager_requests(region, user_id)
        
        # Get applications assigned to junior manager
        assigned_apps = await get_service_requests_by_assignee(region, user_id)
        
        # Combine and remove duplicates
        all_apps = []
        seen_ids = set()
        
        for app in created_apps + assigned_apps:
            if app['id'] not in seen_ids:
                seen_ids.add(app['id'])
                # Format for display
                contact_info = app.get('contact_info', {})
                all_apps.append({
                    'id': app['id'],
                    'client_name': contact_info.get('full_name', 'N/A'),
                    'client_phone': contact_info.get('phone', 'N/A'),
                    'client_address': app.get('location', 'N/A'),
                    'priority': app.get('priority', 'medium'),
                    'status': app.get('current_status', 'created'),
                    'details': app.get('description', 'N/A'),
                    'created_at': app.get('created_at', datetime.now()),
                    'client': contact_info.get('full_name', 'N/A')  # For keyboard compatibility
                })
        
        # Sort by creation date (newest first)
        all_apps.sort(key=lambda x: x.get('created_at', datetime.now()), reverse=True)
        
        return all_apps
        
    except Exception as e:
        logger.error(f"Error getting junior manager applications: {str(e)}")
        return []


@router.message(F.text.in_(["📋 Arizalarni ko'rish", "📋 Просмотр заявок"]))
async def view_applications(message: Message, state: FSMContext):
    """View applications list"""
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
        
        # Get language and region
        lang = await get_user_lang(user_id) or user.get('language', 'uz')
        region = user.get('region')
        
        if not region:
            await message.answer("❌ Region tanlanmagan!")
            return
        
        # Get applications
        applications = await get_junior_manager_applications(user.get('id'), region)
        
        if applications:
            if lang == 'uz':
                text = f"📋 Sizning arizalaringiz ({len(applications)} ta):\n\n"
            else:
                text = f"📋 Ваши заявки ({len(applications)} шт):\n\n"
            
            # Save to state for navigation
            await state.update_data(
                applications=applications,
                current_page=0,
                language=lang,
                region=region
            )
            
            await message.answer(
                text,
                reply_markup=get_application_list_keyboard(applications, page=0, lang=lang)
            )
        else:
            if lang == 'uz':
                text = (
                    "📋 Hozircha arizalar yo'q.\n\n"
                    "🔌 Yangi ariza yaratishni xohlaysizmi?"
                )
            else:
                text = (
                    "📋 Пока заявок нет.\n\n"
                    "🔌 Хотите создать новую заявку?"
                )
            
            await message.answer(text, reply_markup=get_junior_manager_main_menu(lang))
        
        logger.info(f"Junior Manager {user_id} viewed applications list")
        
    except Exception as e:
        logger.error(f"Error in view_applications: {str(e)}")
        await message.answer("❌ Xatolik yuz berdi")


@router.callback_query(F.data.startswith("jm_view_app_"))
async def handle_application_view(callback: CallbackQuery, state: FSMContext):
    """Handle application view details"""
    try:
        await callback.answer()
        
        # Get user data
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user.get('role') != 'junior_manager':
            await callback.answer("❌ Ruxsat yo'q", show_alert=True)
            return
        
        # Get state data
        data = await state.get_data()
        lang = data.get('language') or await get_user_lang(callback.from_user.id) or 'uz'
        region = data.get('region') or user.get('region')
        
        if not region:
            await callback.answer("❌ Region tanlanmagan!", show_alert=True)
            return
        
        # Extract application ID
        app_id = callback.data.replace("jm_view_app_", "")
        
        # Get full application details from mock data
        application = await get_service_request(region, app_id)
        
        if application:
            # Format status text
            status_text = {
                'created': 'Yaratilgan' if lang == 'uz' else 'Создано',
                'pending': 'Kutilmoqda' if lang == 'uz' else 'Ожидание',
                'assigned_to_junior_manager': 'Junior Manager\'da' if lang == 'uz' else 'У Junior Manager',
                'assigned_to_controller': 'Controller\'da' if lang == 'uz' else 'У контроллера',
                'assigned_to_technician': 'Texnikda' if lang == 'uz' else 'У техника',
                'in_progress': 'Jarayonda' if lang == 'uz' else 'В процессе',
                'completed': 'Bajarildi' if lang == 'uz' else 'Выполнено',
                'cancelled': 'Bekor qilindi' if lang == 'uz' else 'Отменено'
            }.get(application.get('current_status', 'created'), application.get('current_status', 'created'))
            
            # Format priority text
            priority_text = {
                'low': '🟢 Past' if lang == 'uz' else '🟢 Низкий',
                'medium': '🟡 O\'rta' if lang == 'uz' else '🟡 Средний',
                'high': '🟠 Yuqori' if lang == 'uz' else '🟠 Высокий',
                'urgent': '🔴 Shoshilinch' if lang == 'uz' else '🔴 Срочный'
            }.get(application.get('priority', 'medium'), application.get('priority', 'medium'))
            
            # Get contact info
            contact_info = application.get('contact_info', {})
            
            # Format date
            created_date = ""
            if application.get('created_at'):
                if isinstance(application['created_at'], str):
                    created_date = application['created_at'][:16]
                else:
                    created_date = application['created_at'].strftime('%d.%m.%Y %H:%M')
            
            # Build message text
            if lang == 'uz':
                text = (
                    f"📋 Ariza #{app_id[:8]} ma'lumotlari:\n\n"
                    f"👤 Mijoz: {contact_info.get('full_name', 'N/A')}\n"
                    f"📱 Telefon: {contact_info.get('phone', 'N/A')}\n"
                    f"📍 Manzil: {application.get('location', 'N/A')}\n"
                    f"⚡ Ustuvorlik: {priority_text}\n"
                    f"📊 Holat: {status_text}\n"
                    f"📝 Tafsilotlar: {application.get('description', 'N/A')}\n"
                    f"📅 Yaratilgan: {created_date}"
                )
            else:
                text = (
                    f"📋 Данные заявки #{app_id[:8]}:\n\n"
                    f"👤 Клиент: {contact_info.get('full_name', 'N/A')}\n"
                    f"📱 Телефон: {contact_info.get('phone', 'N/A')}\n"
                    f"📍 Адрес: {application.get('location', 'N/A')}\n"
                    f"⚡ Приоритет: {priority_text}\n"
                    f"📊 Статус: {status_text}\n"
                    f"📝 Детали: {application.get('description', 'N/A')}\n"
                    f"📅 Создано: {created_date}"
                )
            
            # Create action keyboard
            await callback.message.edit_text(
                text,
                reply_markup=get_application_action_keyboard(
                    app_id, 
                    application.get('current_status'), 
                    lang=lang
                )
            )
            
            # Save current application to state
            await state.update_data(current_application=application)
            
        else:
            text = "❌ Ariza topilmadi" if lang == 'uz' else "❌ Заявка не найдена"
            await callback.answer(text, show_alert=True)
        
    except Exception as e:
        logger.error(f"Error in handle_application_view: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data.startswith("jm_cancel_app_"))
async def handle_application_cancellation(callback: CallbackQuery, state: FSMContext):
    """Handle application cancellation"""
    try:
        await callback.answer()
        
        # Get user data
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user.get('role') != 'junior_manager':
            await callback.answer("❌ Ruxsat yo'q", show_alert=True)
            return
        
        # Get state data
        data = await state.get_data()
        lang = data.get('language') or await get_user_lang(callback.from_user.id) or 'uz'
        region = data.get('region') or user.get('region')
        
        if not region:
            await callback.answer("❌ Region tanlanmagan!", show_alert=True)
            return
        
        # Extract application ID
        app_id = callback.data.replace("jm_cancel_app_", "")
        
        # Get application to check if it belongs to this junior manager
        application = await get_service_request(region, app_id)
        
        if not application:
            text = "❌ Ariza topilmadi" if lang == 'uz' else "❌ Заявка не найдена"
            await callback.answer(text, show_alert=True)
            return
        
        # Check if already cancelled
        if application.get('current_status') == 'cancelled':
            text = "❌ Ariza allaqachon bekor qilingan" if lang == 'uz' else "❌ Заявка уже отменена"
            await callback.answer(text, show_alert=True)
            return
        
        # Check if junior manager has permission to cancel
        # (created by them or assigned to them)
        can_cancel = (
            application.get('staff_creator_id') == user.get('id') or
            application.get('current_assignee_id') == user.get('id')
        )
        
        if not can_cancel:
            text = "❌ Siz bu arizani bekor qila olmaysiz" if lang == 'uz' else "❌ Вы не можете отменить эту заявку"
            await callback.answer(text, show_alert=True)
            return
        
        # Cancel application
        success = await update_service_request(region, app_id, {
            'current_status': 'cancelled',
            'state_data': {
                **application.get('state_data', {}),
                'cancelled_by': user.get('id'),
                'cancelled_at': datetime.now().isoformat(),
                'cancelled_reason': 'Cancelled by Junior Manager'
            }
        })
        
        if success:
            # Log with mock workflow engine
            mock_workflow_engine.process_action(
                workflow_id=app_id,
                action='CANCEL_REQUEST',
                actor_id=user.get('id'),
                actor_role='junior_manager'
            )
            
            if lang == 'uz':
                text = (
                    f"✅ Ariza #{app_id[:8]} muvaffaqiyatli bekor qilindi.\n\n"
                    "Status o'zgartirildi: 'Bekor qilindi'"
                )
            else:
                text = (
                    f"✅ Заявка #{app_id[:8]} успешно отменена.\n\n"
                    "Статус изменен на: 'Отменено'"
                )
            
            await callback.message.edit_text(text)
            
            logger.info(f"Junior Manager {user.get('id')} cancelled application {app_id}")
        else:
            text = "❌ Arizani bekor qilishda xatolik" if lang == 'uz' else "❌ Ошибка при отмене заявки"
            await callback.answer(text, show_alert=True)
        
    except Exception as e:
        logger.error(f"Error cancelling application: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data.startswith("jm_details_app_"))
async def handle_application_details_view(callback: CallbackQuery, state: FSMContext):
    """Handle detailed application view - same as jm_view_app_"""
    # This is the same as jm_view_app_ but can be extended for more detailed view
    await handle_application_view(callback, state)


@router.callback_query(F.data.startswith("jm_apps_page_"))
async def handle_application_pagination(callback: CallbackQuery, state: FSMContext):
    """Handle application list pagination"""
    try:
        await callback.answer()
        
        # Get user data
        user = await get_user_by_telegram_id(callback.from_user.id)
        if not user or user.get('role') != 'junior_manager':
            await callback.answer("❌ Ruxsat yo'q", show_alert=True)
            return
        
        # Get state data
        data = await state.get_data()
        lang = data.get('language') or await get_user_lang(callback.from_user.id) or 'uz'
        applications = data.get('applications', [])
        
        # Extract page number
        page = int(callback.data.replace("jm_apps_page_", ""))
        
        # Update current page in state
        await state.update_data(current_page=page)
        
        if lang == 'uz':
            text = f"📋 Sizning arizalaringiz ({len(applications)} ta):\n\n"
        else:
            text = f"📋 Ваши заявки ({len(applications)} шт):\n\n"
        
        await callback.message.edit_text(
            text, 
            reply_markup=get_application_list_keyboard(applications, page=page, lang=lang)
        )
        
    except Exception as e:
        logger.error(f"Error handling pagination: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data == "jm_close_menu")
async def handle_close_menu(callback: CallbackQuery, state: FSMContext):
    """Handle menu closing"""
    try:
        await callback.answer()
        
        user = await get_user_by_telegram_id(callback.from_user.id)
        lang = await get_user_lang(callback.from_user.id) or 'uz'
        
        text = "✅ Menyu yopildi" if lang == 'uz' else "✅ Меню закрыто"
        
        await callback.message.edit_text(text)
        
        # Clear state
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error closing menu: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)