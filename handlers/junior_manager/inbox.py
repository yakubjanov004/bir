"""
Junior Manager Inbox - Mock Data Implementation

Bu modul junior manager uchun inbox funksionalligini o'z ichiga oladi.
Mijoz bilan bog'lanish va controllerga yuborish funksiyalari bilan.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.junior_manager_buttons import (
    get_junior_manager_main_menu,
    get_junior_manager_back_keyboard
)
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from filters.role_filter import RoleFilter
from states.junior_manager_states import JuniorManagerInboxStates
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

# Mock inbox messages
mock_inbox_messages = [
    {
        'id': 1,
        'title': 'Yangi mijoz arizasi',
        'description': 'Alisher Karimov tomonidan internet ulanish arizasi',
        'priority': 'high',
        'is_read': False,
        'created_at': datetime.now() - timedelta(hours=2),
        'application_id': 'REQ001001',
        'region_code': 'toshkent',
        'role': 'junior_manager',
        'recipient_id': 1
    },
    {
        'id': 2,
        'title': 'TV xizmat muammosi',
        'description': 'Dilfuza Rahimova TV signal muammosi haqida',
        'priority': 'medium',
        'is_read': True,
        'created_at': datetime.now() - timedelta(hours=5),
        'application_id': 'REQ001002',
        'region_code': 'toshkent',
        'role': 'junior_manager',
        'recipient_id': 1
    },
    {
        'id': 3,
        'title': 'Internet tezligi past',
        'description': 'Jamshid Toshmatov internet tezligi haqida shikoyat',
        'priority': 'urgent',
        'is_read': False,
        'created_at': datetime.now() - timedelta(hours=1),
        'application_id': 'REQ001003',
        'region_code': 'toshkent',
        'role': 'junior_manager',
        'recipient_id': 1
    }
]

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
        'assigned_role': 'junior_manager'
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
        'assigned_role': 'junior_manager'
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
        'assigned_role': 'junior_manager'
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

async def get_role_inbox(region_code: str, role: str, recipient_id: int, limit: int = 50):
    """Mock get role inbox messages"""
    try:
        messages = [msg for msg in mock_inbox_messages 
                   if msg.get('region_code') == region_code and 
                   msg.get('role') == role and 
                   msg.get('recipient_id') == recipient_id]
        return messages[:limit]
    except Exception as e:
        logger.error(f"Mock: Error getting role inbox: {e}")
        return []

async def mark_read(region: str, message_id: int, user_id: int):
    """Mock mark message as read"""
    try:
        for msg in mock_inbox_messages:
            if msg.get('id') == message_id:
                msg['is_read'] = True
                logger.info(f"Mock: Marked message {message_id} as read")
                return True
        return False
    except Exception as e:
        logger.error(f"Mock: Error marking message as read: {e}")
        return False

async def mark_completed(region: str, message_id: int, user_id: int):
    """Mock mark message as completed"""
    try:
        for msg in mock_inbox_messages:
            if msg.get('id') == message_id:
                msg['is_completed'] = True
                logger.info(f"Mock: Marked message {message_id} as completed")
                return True
        return False
    except Exception as e:
        logger.error(f"Mock: Error marking message as completed: {e}")
        return False

async def create_on_assignment(region_code: str, application_id: str, assigned_role: str, 
                              title: str, description: str, priority: str, application_type: str):
    """Mock create inbox notification"""
    try:
        notification = {
            'id': len(mock_inbox_messages) + 1,
            'title': title,
            'description': description,
            'priority': priority,
            'is_read': False,
            'created_at': datetime.now(),
            'application_id': application_id,
            'region_code': region_code,
            'role': assigned_role,
            'recipient_id': None  # Will be assigned when controller logs in
        }
        
        mock_inbox_messages.append(notification)
        logger.info(f"Mock: Created inbox notification for {assigned_role} about {application_id}")
        return True
        
    except Exception as e:
        logger.error(f"Mock: Error creating inbox notification: {e}")
        return False

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

async def assign_service_request(region_code: str, request_id: str, assignee_id: int, assignee_role: str):
    """Mock assign service request"""
    try:
        if request_id in mock_service_requests:
            mock_service_requests[request_id]['assigned_to'] = assignee_id
            mock_service_requests[request_id]['assigned_role'] = assignee_role
            mock_service_requests[request_id]['assigned_at'] = datetime.now().isoformat()
            mock_service_requests[request_id]['current_status'] = 'assigned_to_controller'
            
            logger.info(f"Mock: Assigned request {request_id} to {assignee_role} {assignee_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Mock: Error assigning service request: {e}")
        return False

async def get_service_requests_by_assignee(region: str, assignee_id: int):
    """Mock get service requests by assignee"""
    try:
        requests = [req for req in mock_service_requests.values() 
                   if req.get('assigned_to') == assignee_id]
        return requests
    except Exception as e:
        logger.error(f"Mock: Error getting service requests by assignee: {e}")
        return []

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
router = Router(name="junior_manager_inbox")

# Apply role filter to all handlers
router.message.filter(RoleFilter(role="junior_manager"))
router.callback_query.filter(RoleFilter(role="junior_manager"))


@router.message(F.text.in_(["📥 Inbox", "📥 Входящие"]))
async def view_inbox(message: Message, state: FSMContext):
    """View junior manager inbox"""
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
        
        # Get inbox messages for junior manager
        inbox_messages = await get_role_inbox(
            region_code=region,
            role='junior_manager',
            recipient_id=user.get('id'),
            limit=50
        )
        
        # Get assigned applications
        assigned_apps = await get_service_requests_by_assignee(region, user.get('id'))
        
        # Combine and sort by date
        all_items = []
        
        # Add inbox messages
        for msg in inbox_messages:
            all_items.append({
                'type': 'inbox',
                'id': msg.get('id'),
                'title': msg.get('title'),
                'description': msg.get('description'),
                'priority': msg.get('priority'),
                'is_read': msg.get('is_read'),
                'created_at': msg.get('created_at'),
                'application_id': msg.get('application_id')
            })
        
        # Add assigned applications
        for app in assigned_apps:
            if app.get('current_status') not in ['completed', 'cancelled']:
                all_items.append({
                    'type': 'application',
                    'id': app.get('id'),
                    'title': f"Ariza #{app.get('id', '')[:8]}",
                    'description': app.get('description'),
                    'priority': app.get('priority'),
                    'is_read': False,
                    'created_at': app.get('created_at'),
                    'client_name': app.get('contact_info', {}).get('full_name'),
                    'status': app.get('current_status')
                })
        
        # Sort by date (newest first)
        all_items.sort(key=lambda x: x.get('created_at', datetime.now()), reverse=True)
        
        if not all_items:
            if lang == 'uz':
                text = "📭 Sizning inbox bo'sh"
            else:
                text = "📭 Ваш inbox пуст"
            
            await message.answer(text, reply_markup=get_junior_manager_main_menu(lang))
            return
        
        # Save to state
        await state.update_data(
            inbox_items=all_items,
            current_index=0,
            language=lang,
            region=region
        )
        
        # Show first item
        await show_inbox_item(message, all_items[0], 0, len(all_items), lang)
        
        logger.info(f"Junior Manager {user_id} opened inbox with {len(all_items)} items")
        
    except Exception as e:
        logger.error(f"Error in view_inbox: {str(e)}")
        await message.answer("❌ Xatolik yuz berdi.")


async def show_inbox_item(message_or_callback, item: Dict, index: int, total: int, lang: str):
    """Show single inbox item with details"""
    try:
        # Format priority
        priority_icons = {
            'low': '🟢',
            'medium': '🟡', 
            'high': '🟠',
            'urgent': '🔴'
        }
        
        priority_text = {
            'low': 'Past' if lang == 'uz' else 'Низкий',
            'medium': "O'rta" if lang == 'uz' else 'Средний',
            'high': 'Yuqori' if lang == 'uz' else 'Высокий',
            'urgent': 'Shoshilinch' if lang == 'uz' else 'Срочный'
        }
        
        # Format date
        created_date = ""
        if item.get('created_at'):
            if isinstance(item['created_at'], str):
                created_date = item['created_at'][:16]
            else:
                created_date = item['created_at'].strftime('%d.%m.%Y %H:%M')
        
        # Build message text
        if item['type'] == 'inbox':
            icon = "📨" if not item.get('is_read') else "📧"
            
            if lang == 'uz':
                text = (
                    f"{icon} <b>Xabar #{index + 1}/{total}</b>\n\n"
                    f"📋 <b>Sarlavha:</b> {item.get('title', 'N/A')}\n"
                    f"📝 <b>Tavsif:</b> {item.get('description', 'N/A')}\n"
                    f"{priority_icons.get(item.get('priority', 'medium'))} <b>Muhimlik:</b> {priority_text.get(item.get('priority', 'medium'))}\n"
                    f"📅 <b>Sana:</b> {created_date}\n"
                    f"{'✅ O\'qilgan' if item.get('is_read') else '🔵 O\'qilmagan'}"
                )
            else:
                text = (
                    f"{icon} <b>Сообщение #{index + 1}/{total}</b>\n\n"
                    f"📋 <b>Заголовок:</b> {item.get('title', 'N/A')}\n"
                    f"📝 <b>Описание:</b> {item.get('description', 'N/A')}\n"
                    f"{priority_icons.get(item.get('priority', 'medium'))} <b>Приоритет:</b> {priority_text.get(item.get('priority', 'medium'))}\n"
                    f"📅 <b>Дата:</b> {created_date}\n"
                    f"{'✅ Прочитано' if item.get('is_read') else '🔵 Не прочитано'}"
                )
        else:  # application
            status_icons = {
                'created': '🆕',
                'assigned_to_junior_manager': '👤',
                'in_progress': '⚙️',
                'waiting': '⏳'
            }
            
            if lang == 'uz':
                text = (
                    f"📋 <b>Ariza #{index + 1}/{total}</b>\n\n"
                    f"🆔 <b>ID:</b> {item.get('id', 'N/A')[:8]}\n"
                    f"👤 <b>Mijoz:</b> {item.get('client_name', 'N/A')}\n"
                    f"📝 <b>Tavsif:</b> {item.get('description', 'N/A')}\n"
                    f"{priority_icons.get(item.get('priority', 'medium'))} <b>Muhimlik:</b> {priority_text.get(item.get('priority', 'medium'))}\n"
                    f"{status_icons.get(item.get('status', 'created'))} <b>Holat:</b> {item.get('status', 'N/A')}\n"
                    f"📅 <b>Sana:</b> {created_date}"
                )
            else:
                text = (
                    f"📋 <b>Заявка #{index + 1}/{total}</b>\n\n"
                    f"🆔 <b>ID:</b> {item.get('id', 'N/A')[:8]}\n"
                    f"👤 <b>Клиент:</b> {item.get('client_name', 'N/A')}\n"
                    f"📝 <b>Описание:</b> {item.get('description', 'N/A')}\n"
                    f"{priority_icons.get(item.get('priority', 'medium'))} <b>Приоритет:</b> {priority_text.get(item.get('priority', 'medium'))}\n"
                    f"{status_icons.get(item.get('status', 'created'))} <b>Статус:</b> {item.get('status', 'N/A')}\n"
                    f"📅 <b>Дата:</b> {created_date}"
                )
        
        # Create keyboard
        keyboard = get_inbox_navigation_keyboard(index, total, item, lang)
        
        # Send or edit message
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
        else:
            await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
    except Exception as e:
        logger.error(f"Error in show_inbox_item: {str(e)}")
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer("❌ Xatolik yuz berdi.")
        else:
            await message_or_callback.answer("❌ Xatolik yuz berdi", show_alert=True)


def get_inbox_navigation_keyboard(index: int, total: int, item: Dict, lang: str) -> InlineKeyboardMarkup:
    """Create navigation keyboard for inbox"""
    keyboard = []
    
    # Navigation buttons
    nav_row = []
    if index > 0:
        nav_row.append(InlineKeyboardButton(
            text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущий",
            callback_data="jm_inbox_prev"
        ))
    
    if index < total - 1:
        nav_row.append(InlineKeyboardButton(
            text="Keyingi ➡️" if lang == 'uz' else "Следующий ➡️",
            callback_data="jm_inbox_next"
        ))
    
    if nav_row:
        keyboard.append(nav_row)
    
    # Action buttons
    action_row = []
    
    if item['type'] == 'application':
        # View details button
        action_row.append(InlineKeyboardButton(
            text="👁 Ko'rish" if lang == 'uz' else "👁 Просмотр",
            callback_data=f"jm_view_app_{item['id']}"
        ))
        
        # Contact client button
        action_row.append(InlineKeyboardButton(
            text="📞 Mijoz" if lang == 'uz' else "📞 Клиент",
            callback_data=f"jm_contact_client_{item['id']}"
        ))
        
        # Send to controller button
        action_row.append(InlineKeyboardButton(
            text="📤 Controller'ga" if lang == 'uz' else "📤 Контроллеру",
            callback_data=f"jm_to_controller_{item['id']}"
        ))
    else:  # inbox message
        if not item.get('is_read'):
            action_row.append(InlineKeyboardButton(
                text="✅ O'qildi" if lang == 'uz' else "✅ Прочитано",
                callback_data=f"jm_mark_read_{item['id']}"
            ))
        
        if item.get('application_id'):
            action_row.append(InlineKeyboardButton(
                text="📋 Arizani ko'rish" if lang == 'uz' else "📋 Просмотр заявки",
                callback_data=f"jm_view_app_{item['application_id']}"
            ))
    
    if action_row:
        keyboard.append(action_row)
    
    # Close button
    keyboard.append([InlineKeyboardButton(
        text="❌ Yopish" if lang == 'uz' else "❌ Закрыть",
        callback_data="jm_close_inbox"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.callback_query(F.data == "jm_inbox_prev")
async def show_previous_inbox_item(callback: CallbackQuery, state: FSMContext):
    """Show previous inbox item"""
    try:
        await callback.answer()
        
        data = await state.get_data()
        current_index = data.get('current_index', 0)
        inbox_items = data.get('inbox_items', [])
        lang = data.get('language', 'uz')
        
        if not inbox_items:
            await callback.answer("Ma'lumot topilmadi")
            return
        
        if current_index > 0:
            new_index = current_index - 1
            await state.update_data(current_index=new_index)
            await show_inbox_item(callback, inbox_items[new_index], new_index, len(inbox_items), lang)
        else:
            await callback.answer("Bu birinchi xabar" if lang == 'uz' else "Это первое сообщение")
            
    except Exception as e:
        logger.error(f"Error in show_previous_inbox_item: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data == "jm_inbox_next")
async def show_next_inbox_item(callback: CallbackQuery, state: FSMContext):
    """Show next inbox item"""
    try:
        await callback.answer()
        
        data = await state.get_data()
        current_index = data.get('current_index', 0)
        inbox_items = data.get('inbox_items', [])
        lang = data.get('language', 'uz')
        
        if not inbox_items:
            await callback.answer("Ma'lumot topilmadi")
            return
        
        if current_index < len(inbox_items) - 1:
            new_index = current_index + 1
            await state.update_data(current_index=new_index)
            await show_inbox_item(callback, inbox_items[new_index], new_index, len(inbox_items), lang)
        else:
            await callback.answer("Bu oxirgi xabar" if lang == 'uz' else "Это последнее сообщение")
            
    except Exception as e:
        logger.error(f"Error in show_next_inbox_item: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data.startswith("jm_mark_read_"))
async def mark_message_read(callback: CallbackQuery, state: FSMContext):
    """Mark inbox message as read"""
    try:
        await callback.answer()
        
        message_id = int(callback.data.replace("jm_mark_read_", ""))
        
        data = await state.get_data()
        region = data.get('region')
        lang = data.get('language', 'uz')
        
        if region:
            # Mark as read in database
            user = await get_user_by_telegram_id(callback.from_user.id)
            success = await mark_read(region, message_id, user.get('id'))
            
            if success:
                # Update local state
                inbox_items = data.get('inbox_items', [])
                for item in inbox_items:
                    if item.get('id') == message_id:
                        item['is_read'] = True
                        break
                
                await state.update_data(inbox_items=inbox_items)
                
                # Refresh display
                current_index = data.get('current_index', 0)
                if current_index < len(inbox_items):
                    await show_inbox_item(callback, inbox_items[current_index], current_index, len(inbox_items), lang)
                
                await callback.answer("✅ O'qildi deb belgilandi" if lang == 'uz' else "✅ Отмечено как прочитанное")
            else:
                await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
        
    except Exception as e:
        logger.error(f"Error in mark_message_read: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data.startswith("jm_view_app_"))
async def view_application_details(callback: CallbackQuery, state: FSMContext):
    """View application details"""
    try:
        await callback.answer()
        
        app_id = callback.data.replace("jm_view_app_", "")
        
        data = await state.get_data()
        region = data.get('region')
        lang = data.get('language', 'uz')
        
        if not region:
            await callback.answer("❌ Region tanlanmagan!", show_alert=True)
            return
        
        # Get application details
        application = await get_service_request(region, app_id)
        
        if not application:
            await callback.answer("❌ Ariza topilmadi", show_alert=True)
            return
        
        # Format application details
        contact_info = application.get('contact_info', {})
        state_data = application.get('state_data', {})
        
        priority_text = {
            'low': '🟢 Past' if lang == 'uz' else '🟢 Низкий',
            'medium': '🟡 O\'rta' if lang == 'uz' else '🟡 Средний',
            'high': '🟠 Yuqori' if lang == 'uz' else '🟠 Высокий',
            'urgent': '🔴 Shoshilinch' if lang == 'uz' else '🔴 Срочный'
        }
        
        if lang == 'uz':
            text = (
                f"📋 <b>Ariza tafsilotlari</b>\n\n"
                f"🆔 <b>ID:</b> <code>{app_id[:8]}</code>\n"
                f"📌 <b>Turi:</b> {application.get('workflow_type', 'N/A')}\n"
                f"👤 <b>Mijoz:</b> {contact_info.get('full_name', 'N/A')}\n"
                f"📱 <b>Telefon:</b> {contact_info.get('phone', 'N/A')}\n"
                f"📍 <b>Manzil:</b> {application.get('location', 'N/A')}\n"
                f"📝 <b>Tavsif:</b> {application.get('description', 'N/A')}\n"
                f"⚡ <b>Muhimlik:</b> {priority_text.get(application.get('priority', 'medium'))}\n"
                f"📊 <b>Holat:</b> {application.get('current_status', 'N/A')}\n"
            )
            
            if state_data.get('notes'):
                text += f"💬 <b>Izohlar:</b> {state_data['notes']}\n"
        else:
            text = (
                f"📋 <b>Детали заявки</b>\n\n"
                f"🆔 <b>ID:</b> <code>{app_id[:8]}</code>\n"
                f"📌 <b>Тип:</b> {application.get('workflow_type', 'N/A')}\n"
                f"👤 <b>Клиент:</b> {contact_info.get('full_name', 'N/A')}\n"
                f"📱 <b>Телефон:</b> {contact_info.get('phone', 'N/A')}\n"
                f"📍 <b>Адрес:</b> {application.get('location', 'N/A')}\n"
                f"📝 <b>Описание:</b> {application.get('description', 'N/A')}\n"
                f"⚡ <b>Приоритет:</b> {priority_text.get(application.get('priority', 'medium'))}\n"
                f"📊 <b>Статус:</b> {application.get('current_status', 'N/A')}\n"
            )
            
            if state_data.get('notes'):
                text += f"💬 <b>Заметки:</b> {state_data['notes']}\n"
        
        # Create action keyboard
        keyboard = []
        
        # Contact client button
        keyboard.append([InlineKeyboardButton(
            text="📞 Mijoz bilan bog'lanish" if lang == 'uz' else "📞 Связаться с клиентом",
            callback_data=f"jm_contact_client_{app_id}"
        )])
        
        # Send to controller button
        if application.get('current_status') != 'assigned_to_controller':
            keyboard.append([InlineKeyboardButton(
                text="📤 Controller'ga yuborish" if lang == 'uz' else "📤 Отправить контроллеру",
                callback_data=f"jm_to_controller_{app_id}"
            )])
        
        # Back button
        keyboard.append([InlineKeyboardButton(
            text="⬅️ Orqaga" if lang == 'uz' else "⬅️ Назад",
            callback_data="jm_back_to_inbox"
        )])
        
        await callback.message.edit_text(
            text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
            parse_mode='HTML'
        )
        
        # Save application to state
        await state.update_data(current_application=application)
        
    except Exception as e:
        logger.error(f"Error in view_application_details: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data.startswith("jm_contact_client_"))
async def contact_client(callback: CallbackQuery, state: FSMContext):
    """Start contact with client process"""
    try:
        await callback.answer()
        
        app_id = callback.data.replace("jm_contact_client_", "")
        
        data = await state.get_data()
        lang = data.get('language', 'uz')
        
        # Ask for contact note
        if lang == 'uz':
            text = (
                "📞 <b>Mijoz bilan bog'lanish</b>\n\n"
                "Mijoz bilan qanday bog'landingiz va nima muhokama qilindi?\n"
                "Iltimos, qisqacha ma'lumot kiriting:"
            )
        else:
            text = (
                "📞 <b>Связь с клиентом</b>\n\n"
                "Как вы связались с клиентом и что обсуждалось?\n"
                "Пожалуйста, введите краткую информацию:"
            )
        
        await callback.message.edit_text(text, parse_mode='HTML')
        
        # Set state to wait for contact note
        await state.set_state(JuniorManagerInboxStates.entering_message_number)
        await state.update_data(
            action='contact_client',
            application_id=app_id
        )
        
    except Exception as e:
        logger.error(f"Error in contact_client: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.message(JuniorManagerInboxStates.entering_message_number)
async def handle_contact_note(message: Message, state: FSMContext):
    """Handle contact note from junior manager"""
    try:
        data = await state.get_data()
        action = data.get('action')
        app_id = data.get('application_id')
        region = data.get('region')
        lang = data.get('language', 'uz')
        
        if action == 'contact_client':
            # Save contact note
            contact_note = message.text.strip()
            
            # Update application with contact info
            if region and app_id:
                # Get current application
                application = await get_service_request(region, app_id)
                
                if application:
                    # Update state_data with contact info
                    state_data = application.get('state_data', {})
                    contact_attempts = state_data.get('contact_attempts', 0) + 1
                    
                    state_data['contact_attempts'] = contact_attempts
                    state_data['last_contact_date'] = datetime.now().isoformat()
                    state_data['last_contact_note'] = contact_note
                    
                    # Update in database
                    await update_service_request(region, app_id, {
                        'state_data': state_data
                    })
                    
                    if lang == 'uz':
                        success_text = (
                            "✅ <b>Mijoz bilan bog'lanish qayd etildi</b>\n\n"
                            f"📝 Izoh: {contact_note}\n"
                            f"📞 Urinishlar soni: {contact_attempts}\n\n"
                            "Endi Controller'ga yuborishingiz mumkin."
                        )
                    else:
                        success_text = (
                            "✅ <b>Контакт с клиентом записан</b>\n\n"
                            f"📝 Заметка: {contact_note}\n"
                            f"📞 Количество попыток: {contact_attempts}\n\n"
                            "Теперь вы можете отправить контроллеру."
                        )
                    
                    # Show success with options
                    keyboard = [
                        [InlineKeyboardButton(
                            text="📤 Controller'ga yuborish" if lang == 'uz' else "📤 Отправить контроллеру",
                            callback_data=f"jm_to_controller_{app_id}"
                        )],
                        [InlineKeyboardButton(
                            text="📥 Inbox'ga qaytish" if lang == 'uz' else "📥 Вернуться в Inbox",
                            callback_data="jm_back_to_inbox"
                        )]
                    ]
                    
                    await message.answer(
                        success_text,
                        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
                        parse_mode='HTML'
                    )
                    
                    # Clear state
                    await state.clear()
                    
                    logger.info(f"Junior Manager contacted client for application {app_id}")
        
    except Exception as e:
        logger.error(f"Error in handle_contact_note: {str(e)}")
        await message.answer("❌ Xatolik yuz berdi.")


@router.callback_query(F.data.startswith("jm_to_controller_"))
async def send_to_controller(callback: CallbackQuery, state: FSMContext):
    """Send application to controller"""
    try:
        await callback.answer()
        
        app_id = callback.data.replace("jm_to_controller_", "")
        
        data = await state.get_data()
        region = data.get('region')
        lang = data.get('language', 'uz')
        
        if not region:
            await callback.answer("❌ Region tanlanmagan!", show_alert=True)
            return
        
        # Get application
        application = await get_service_request(region, app_id)
        
        if not application:
            await callback.answer("❌ Ariza topilmadi", show_alert=True)
            return
        
        # Update application status
        user = await get_user_by_telegram_id(callback.from_user.id)
        
        success = await assign_service_request(
            region_code=region,
            request_id=app_id,
            assignee_id=None,  # Will be assigned by controller
            assignee_role='controller'
        )
        
        if success:
            # Create inbox notification for controller
            await create_on_assignment(
                region_code=region,
                application_id=app_id,
                assigned_role='controller',
                title=f"Junior Manager'dan ariza - {application.get('contact_info', {}).get('full_name', 'N/A')}",
                description=f"Junior Manager tomonidan tekshirilgan va yuborilgan",
                priority=application.get('priority', 'medium'),
                application_type=application.get('workflow_type', 'service_request')
            )
            
            # Log with workflow engine
            mock_workflow_engine.process_action(
                workflow_id=app_id,
                action='FORWARD_TO_CONTROLLER',
                actor_id=user.get('id'),
                actor_role='junior_manager'
            )
            
            if lang == 'uz':
                success_text = (
                    "✅ <b>Ariza Controller'ga yuborildi!</b>\n\n"
                    f"📋 Ariza ID: <code>{app_id[:8]}</code>\n"
                    f"👤 Mijoz: {application.get('contact_info', {}).get('full_name', 'N/A')}\n\n"
                    "Controller tez orada arizani ko'rib chiqadi."
                )
            else:
                success_text = (
                    "✅ <b>Заявка отправлена контроллеру!</b>\n\n"
                    f"📋 ID заявки: <code>{app_id[:8]}</code>\n"
                    f"👤 Клиент: {application.get('contact_info', {}).get('full_name', 'N/A')}\n\n"
                    "Контроллер скоро рассмотрит заявку."
                )
            
            await callback.message.edit_text(success_text, parse_mode='HTML')
            
            # Back to main menu button
            await callback.message.answer(
                "Asosiy menyu" if lang == 'uz' else "Главное меню",
                reply_markup=get_junior_manager_main_menu(lang)
            )
            
            logger.info(f"Junior Manager {callback.from_user.id} sent application {app_id} to controller")
            
        else:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
        
    except Exception as e:
        logger.error(f"Error in send_to_controller: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data == "jm_back_to_inbox")
async def back_to_inbox(callback: CallbackQuery, state: FSMContext):
    """Go back to inbox list"""
    try:
        await callback.answer()
        
        data = await state.get_data()
        inbox_items = data.get('inbox_items', [])
        current_index = data.get('current_index', 0)
        lang = data.get('language', 'uz')
        
        if inbox_items and current_index < len(inbox_items):
            await show_inbox_item(callback, inbox_items[current_index], current_index, len(inbox_items), lang)
        else:
            await callback.message.edit_text(
                "📭 Inbox bo'sh" if lang == 'uz' else "📭 Inbox пуст"
            )
            
    except Exception as e:
        logger.error(f"Error in back_to_inbox: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data == "jm_close_inbox")
async def close_inbox(callback: CallbackQuery, state: FSMContext):
    """Close inbox and return to main menu"""
    try:
        await callback.answer()
        
        lang = await get_user_lang(callback.from_user.id) or 'uz'
        
        await callback.message.edit_text(
            "📥 Inbox yopildi" if lang == 'uz' else "📥 Inbox закрыт"
        )
        
        await callback.message.answer(
            "Asosiy menyu" if lang == 'uz' else "Главное меню",
            reply_markup=get_junior_manager_main_menu(lang)
        )
        
        await state.clear()
        
    except Exception as e:
        logger.error(f"Error in close_inbox: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)