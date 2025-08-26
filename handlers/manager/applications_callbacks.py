"""
Applications Callbacks Handler - Mock Data Implementation

Bu modul manager uchun arizalar bilan bog'liq callback funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from states.manager_states import ManagerApplicationStates
from keyboards.manager_buttons import (
    get_manager_main_keyboard,
    get_application_actions_keyboard,
    get_application_navigation_keyboard
)
from typing import Dict, Any, List, Optional
from datetime import datetime
from filters.role_filter import RoleFilter
import logging

logger = logging.getLogger(__name__)

# Mock data storage
mock_applications = [
    {
        'id': 'req_001_2024_01_15',
        'workflow_type': 'connection_request',
        'current_status': 'in_progress',
        'role_current': 'manager',
        'contact_info': {
            'full_name': 'Aziz Karimov',
            'phone': '+998901234567'
        },
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'description': 'Internet ulanish arizasi - yangi uy uchun internet xizmatini ulashish kerak',
        'location': 'Tashkent, Chorsu tumani, 15-uy',
        'client_id': 123456789,
        'priority': 'high'
    },
    {
        'id': 'req_002_2024_01_16',
        'workflow_type': 'technical_service',
        'current_status': 'created',
        'role_current': 'manager',
        'contact_info': {
            'full_name': 'Malika Toshmatova',
            'phone': '+998901234568'
        },
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'description': 'TV signal muammosi - TV kanallar ko\'rinmayapti, signal zaif',
        'location': 'Tashkent, Yunusabad tumani, 25-uy',
        'client_id': 123456790,
        'priority': 'normal'
    },
    {
        'id': 'req_003_2024_01_17',
        'workflow_type': 'call_center_direct',
        'current_status': 'completed',
        'role_current': 'manager',
        'contact_info': {
            'full_name': 'Jahongir Azimov',
            'phone': '+998901234569'
        },
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'description': 'Qo\'ng\'iroq markazi arizasi - mijoz xizmat sifatini yaxshilash haqida',
        'location': 'Tashkent, Sergeli tumani, 10-uy',
        'client_id': 123456791,
        'priority': 'low'
    },
    {
        'id': 'req_004_2024_01_18',
        'workflow_type': 'connection_request',
        'current_status': 'created',
        'role_current': 'manager',
        'contact_info': {
            'full_name': 'Umar Toshmatov',
            'phone': '+998901234570'
        },
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'description': 'Yangi internet paketini qo\'shish - 100 Mbit/s tezlikda',
        'location': 'Tashkent, Chilanzor tumani, 30-uy',
        'client_id': 123456792,
        'priority': 'urgent'
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

# Mock functions
async def get_user_by_telegram_id(telegram_id: int):
    """Mock get user data"""
    for user in mock_users.values():
        if user.get('telegram_id') == telegram_id:
            return user
    return None

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    user = await get_user_by_telegram_id(telegram_id)
    return user.get('language', 'uz') if user else 'uz'

async def answer_and_cleanup(callback: CallbackQuery, text: str, **kwargs):
    """Mock answer and cleanup"""
    try:
        await callback.answer(text, **kwargs)
    except Exception as e:
        logger.error(f"Error in answer_and_cleanup: {e}")

# Mock workflow access control
class MockWorkflowAccessControl:
    """Mock workflow access control"""
    async def get_filtered_requests_for_role(self, user_id: int, user_role: str, region: str = 'toshkent'):
        """Mock get filtered requests for role"""
        try:
            # Return mock applications filtered by role
            if user_role == 'manager':
                return [app for app in mock_applications if app.get('role_current') == 'manager']
            else:
                return mock_applications
        except Exception as e:
            logger.error(f"Mock: Error getting applications: {e}")
            return []

# Mock service request
async def get_service_request(request_id: str):
    """Mock get service request"""
    try:
        # Find request in mock data
        for app in mock_applications:
            if app.get('id') == request_id or app.get('id').startswith(request_id):
                return app
        return None
    except Exception as e:
        logger.error(f"Mock: Error getting service request: {e}")
        return None

# Mock word generator
class MockWordGenerator:
    """Mock word generator"""
    async def generate_act_document(self, request_id: str, document_type: str):
        """Mock generate act document"""
        try:
            print(f"Mock: Generating {document_type} document for request {request_id}")
            # Return a mock file path
            return f"/tmp/mock_document_{request_id}_{document_type}.docx"
        except Exception as e:
            logger.error(f"Mock: Error generating document: {e}")
            return None

def get_manager_applications_callbacks_router():
    """Router for applications callbacks with mock data"""
    router = Router()
    
    # Apply role filter - both manager and junior_manager can access
    role_filter = RoleFilter(["manager", "junior_manager"])
    router.callback_query.filter(role_filter)
    
    @router.callback_query(F.data == "view_applications")
    async def view_applications(callback: CallbackQuery, state: FSMContext):
        """View applications using mock data"""
        try:
            await callback.answer()
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Get region from state or default
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Get mock applications
            access_control = MockWorkflowAccessControl()
            applications = await access_control.get_filtered_requests_for_role(
                user_id=user['id'],
                user_role='manager',
                region=region
            )
            
            if not applications:
                text = "📭 Arizalar topilmadi"
                keyboard = get_manager_main_keyboard(lang=user.get('language', 'uz'))
                await callback.message.edit_text(text, reply_markup=keyboard)
                return
            
            # Update state with applications
            await state.update_data(
                applications=applications,
                current_index=0,
                region=region
            )
            
            # Display first application
            await display_application(callback, state, applications, 0, user)
            
        except Exception as e:
            logger.error(f"Error in view_applications: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("app_"))
    async def handle_application_action(callback: CallbackQuery, state: FSMContext):
        """Handle application actions using mock data"""
        try:
            await callback.answer()
            
            # Extract action and data
            action_data = callback.data.replace("app_", "")
            parts = action_data.split("_")
            action = parts[0]
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Get applications from state
            state_data = await state.get_data()
            applications = state_data.get('applications', [])
            current_index = state_data.get('current_index', 0)
            
            if not applications or current_index >= len(applications):
                await callback.answer("Arizalar topilmadi", show_alert=True)
                return
            
            current_app = applications[current_index]
            
            if action == "view":
                # Display current application
                await display_application(callback, state, applications, current_index, user)
                
            elif action == "next":
                # Go to next application
                if current_index < len(applications) - 1:
                    new_index = current_index + 1
                    await state.update_data(current_index=new_index)
                    await display_application(callback, state, applications, new_index, user)
                else:
                    await callback.answer("Oxirgi ariza", show_alert=True)
                    
            elif action == "prev":
                # Go to previous application
                if current_index > 0:
                    new_index = current_index - 1
                    await state.update_data(current_index=new_index)
                    await display_application(callback, state, applications, new_index, user)
                else:
                    await callback.answer("Birinchi ariza", show_alert=True)
                    
            elif action == "actions":
                # Show application actions
                await show_application_actions(callback, state, current_app, user)
                
            else:
                await callback.answer("Noma'lum amal", show_alert=True)
                
        except Exception as e:
            logger.error(f"Error in handle_application_action: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    async def display_application(callback: CallbackQuery, state: FSMContext, applications: List[Dict], index: int, user: Dict):
        """Display application details using mock data"""
        try:
            app = applications[index]
            
            # Get client info
            client_name = 'Unknown'
            client_phone = 'N/A'
            if app.get('contact_info'):
                client_name = app['contact_info'].get('full_name', 'Unknown')
                client_phone = app['contact_info'].get('phone', 'N/A')
            
            # Format workflow type
            workflow_type_names = {
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Qo\'ng\'iroq markazi'
            }
            
            workflow_type = workflow_type_names.get(app.get('workflow_type'), app.get('workflow_type', 'Ariza'))
            
            # Format status
            status_names = {
                'created': 'Yaratilgan',
                'in_progress': 'Jarayonda',
                'completed': 'Tugallangan',
                'cancelled': 'Bekor qilingan'
            }
            
            status = status_names.get(app.get('current_status'), app.get('current_status', 'Noma\'lum'))
            
            # Format date
            created_date = app.get('created_at')
            if hasattr(created_date, 'strftime'):
                created_date = created_date.strftime('%d.%m.%Y %H:%M')
            else:
                created_date = str(created_date)
            
            # Format priority
            priority_names = {
                'low': 'Past',
                'normal': 'O\'rtacha',
                'high': 'Yuqori',
                'urgent': 'Shoshilinch'
            }
            
            priority = priority_names.get(app.get('priority', 'normal'), app.get('priority', 'normal'))
            
            # Create text
            text = (
                f"📋 <b>Ariza ma'lumotlari</b>\n\n"
                f"🆔 <b>ID:</b> {app.get('id', 'N/A')}\n"
                f"📝 <b>Tur:</b> {workflow_type}\n"
                f"👤 <b>Mijoz:</b> {client_name}\n"
                f"📞 <b>Telefon:</b> {client_phone}\n"
                f"📍 <b>Manzil:</b> {app.get('location', 'N/A')}\n"
                f"📅 <b>Yaratilgan:</b> {created_date}\n"
                f"📊 <b>Holat:</b> {status}\n"
                f"🔴 <b>Muhimlik:</b> {priority}\n"
                f"📝 <b>Tavsif:</b> {app.get('description', 'Tavsif yo\'q')[:100]}{'...' if app.get('description') and len(app.get('description', '')) > 100 else ''}\n\n"
                f"📊 <b>Ariza {index + 1}/{len(applications)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_application_navigation_keyboard(
                app_id=app.get('id'),
                has_prev=index > 0,
                has_next=index < len(applications) - 1,
                lang=user.get('language', 'uz')
            )
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in display_application: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    async def show_application_actions(callback: CallbackQuery, state: FSMContext, app: Dict, user: Dict):
        """Show application action buttons using mock data"""
        try:
            # Create actions keyboard
            keyboard = get_application_actions_keyboard(
                app_id=app.get('id'),
                current_status=app.get('current_status'),
                lang=user.get('language', 'uz')
            )
            
            text = (
                f"🔧 <b>Ariza amallari</b>\n\n"
                f"📝 Ariza ID: {app.get('id', 'N/A')}\n"
                f"📊 Holat: {app.get('current_status', 'N/A')}\n\n"
                f"Quyidagi amallardan birini tanlang:"
            )
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in show_application_actions: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "back_to_main")
    async def back_to_main(callback: CallbackQuery, state: FSMContext):
        """Go back to main menu"""
        try:
            await callback.answer()
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                return
            
            # Clear applications from state
            await state.update_data(applications=None, current_index=None)
            
            # Show main keyboard
            keyboard = get_manager_main_keyboard(lang=user.get('language', 'uz'))
            text = "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:"
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in back_to_main: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    # Additional mock handlers for backward compatibility
    @router.callback_query(F.data == "back_to_applications")
    async def back_to_applications(callback: CallbackQuery, state: FSMContext):
        """Manager back to applications handler"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            text = "Arizalar menyusiga qaytdingiz."
            
            # Inline keyboard ishlatish
            keyboard_buttons = [
                [
                    InlineKeyboardButton(
                        text="📋 Hammasini ko'rish",
                        callback_data="mgr_view_all_applications"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔎 ID bo'yicha ko'rish",
                        callback_data="mgr_view_by_id"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⬅️ Asosiy menyu",
                        callback_data="mgr_back_to_main"
                    )
                ]
            ]
            
            keyboard = get_application_navigation_keyboard(lang=user.get('language', 'uz'))
            
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            await callback.answer()
            await state.clear()
            
        except Exception as e:
            logger.error(f"Error in back_to_applications: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_view_all_applications")
    async def view_all_applications_callback(callback: CallbackQuery, state: FSMContext):
        """Manager view all applications callback handler"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            # Use mock workflow access control to get filtered requests for manager role
            access_control = MockWorkflowAccessControl()
            requests = await access_control.get_filtered_requests_for_role(
                user_id=user['id'],
                user_role='manager'
            )
            
            if not requests:
                text = "Hozircha hech qanday ariza yo'q."
                keyboard_buttons = [
                    [
                        InlineKeyboardButton(
                            text="⬅️ Orqaga",
                            callback_data="back_to_applications"
                        )
                    ]
                ]
                keyboard = get_application_navigation_keyboard(lang=user.get('language', 'uz'))
                
                await callback.message.edit_text(
                    text=text,
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )
                return
            
            # Foydalanuvchi state'da joriy zayavka indeksini saqlash
            data = await state.get_data()
            current_index = data.get('current_application_index', 0)
            
            # Indeksni cheklash
            if current_index >= len(requests):
                current_index = 0
            elif current_index < 0:
                current_index = len(requests) - 1
            
            # Joriy zayavka ma'lumotlari
            current_request = requests[current_index]
            
            # Status belgilarini aniqlash
            status_emoji = {
                'created': '🆕',
                'in_progress': '⏳',
                'completed': '✅',
                'cancelled': '❌'
            }.get(current_request.get('current_status', 'created'), '📋')
            
            workflow_type = current_request.get('workflow_type', 'unknown')
            workflow_emoji = {
                'connection_request': '🔌',
                'technical_service': '🔧',
                'call_center_direct': '📞'
            }.get(workflow_type, '📋')
            
            # Zayavka turini formatlash
            workflow_type_text = {
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Qo\'ng\'iroq markazi'
            }.get(workflow_type, 'Noma\'lum')
            
            # Mijoz ma'lumotlari
            client_name = current_request.get('contact_info', {}).get('full_name', 'N/A') if isinstance(current_request.get('contact_info'), dict) else 'N/A'
            client_phone = current_request.get('contact_info', {}).get('phone', 'N/A') if isinstance(current_request.get('contact_info'), dict) else 'N/A'
            
            # Vaqt ma'lumotlari
            created_at = current_request.get('created_at', 'N/A')
            updated_at = current_request.get('updated_at', 'N/A')
            
            # Vaqt hisoblash
            total_duration = "N/A"
            if created_at and created_at != 'N/A':
                try:
                    if isinstance(created_at, str):
                        created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    else:
                        created_dt = created_at
                    
                    current_time = datetime.now()
                    if created_dt.tzinfo is None:
                        created_dt = created_dt.replace(tzinfo=None)
                    
                    duration = current_time - created_dt
                    total_hours = int(duration.total_seconds() // 3600)
                    total_minutes = int((duration.total_seconds() % 3600) // 60)
                    
                    if total_hours > 0:
                        total_duration = f"{total_hours}s {total_minutes}d"
                    else:
                        total_duration = f"{total_minutes} daqiqa"
                except Exception as e:
                    logger.error(f"Error calculating duration: {e}")
                    total_duration = "N/A"
            
            # Izoh va diagnostika
            description = current_request.get('description', 'Izoh yo\'q')
            location = current_request.get('location', 'Manzil ko\'rsatilmagan')
            
            # Joriy rol va status
            current_role = current_request.get('role_current', 'Noma\'lum')
            current_status = current_request.get('current_status', 'Noma\'lum')
            
            # Status matnini formatlash
            status_text = {
                'created': 'Yaratilgan',
                'in_progress': 'Jarayonda',
                'completed': 'Tugallangan',
                'cancelled': 'Bekor qilingan'
            }.get(current_status, current_status)
            
            text = f"""
📋 <b>Ariza #{current_index + 1} / {len(requests)}</b>

{status_emoji}{workflow_emoji} <b>{client_name}</b>
   📋 ID: {current_request['id'][:8]}...
   🏷️ Turi: {workflow_type_text}
   📊 Status: {status_text}
   👤 Joriy rol: {current_role}

📞 <b>Mijoz ma'lumotlari:</b>
   • Nomi: {client_name}
   • Telefon: {client_phone}
   • Manzil: {location}

⏰ <b>Vaqt ma'lumotlari:</b>
   • Yaratilgan: {created_at}
   • Yangilangan: {updated_at}
   • Umumiy vaqt: {total_duration}

📝 <b>Izoh va diagnostika:</b>
   {description}

🔧 <b>Texnik ma'lumotlar:</b>
   • Workflow type: {workflow_type}
   • Current status: {current_status}
   • Role current: {current_role}
"""
            
            # Asosiy tugmalar
            keyboard_buttons = []
            if current_request.get('current_status') != 'completed':
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="👨‍💼 Junior menejerga berish",
                        callback_data=f"assign_junior_{current_request['id'][:8]}"
                    )
                ])
            
            # Word hujjat tugmasi (barcha statuslar uchun)
            keyboard_buttons.append([
                InlineKeyboardButton(
                    text="📄 Word hujjat olish",
                    callback_data=f"mgr_word_doc_{current_request['id'][:20]}"
                )
            ])
            
            # Navigatsiya tugmalari
            if len(requests) > 1:
                keyboard_buttons.append([
                    InlineKeyboardButton(
                        text="◀️ Oldingi",
                        callback_data="mgr_prev_application"
                    ),
                    InlineKeyboardButton(
                        text="Keyingi ▶️",
                        callback_data="mgr_next_application"
                    )
                ])
            
            keyboard = get_application_navigation_keyboard(lang=user.get('language', 'uz'))
            
            # State'da joriy indeksni saqlash
            await state.update_data(current_application_index=current_index)
            
            try:
                await callback.message.edit_text(
                    text=text,
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )
            except Exception as e:
                if "message is not modified" in str(e):
                    await callback.answer()
                else:
                    await callback.message.edit_text(
                        text=text,
                        reply_markup=keyboard,
                        parse_mode='HTML'
                    )
            
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error in view_all_applications_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_view_by_id")
    async def view_by_id_callback(callback: CallbackQuery, state: FSMContext):
        """Manager view by ID callback handler"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            text = "Ariza ID raqamini kiriting :"
            
            keyboard_buttons = [
                [
                    InlineKeyboardButton(
                        text="⬅️ Orqaga",
                        callback_data="back_to_applications"
                    )
                ]
            ]
            keyboard = get_application_navigation_keyboard(lang=user.get('language', 'uz'))
            
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            await state.set_state(ManagerApplicationStates.waiting_for_id)
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error in view_by_id_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_back_to_main")
    async def back_to_main_callback(callback: CallbackQuery, state: FSMContext):
        """Manager back to main callback handler"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            
            text = "Asosiy menyuga qaytdingiz."
            
            # Yangi xabar yuborish (edit_text emas)
            await callback.message.answer(text, reply_markup=get_manager_main_keyboard(lang))
            await callback.answer()
            await state.clear()
            
        except Exception as e:
            logger.error(f"Error in back_to_main_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("mgr_word_doc_"))
    async def manager_generate_word(callback: CallbackQuery):
        """Manager uchun Word hujjat yaratish"""
        try:
            lang = await get_user_lang(callback.from_user.id)
            request_id = callback.data.replace("mgr_word_doc_", "")
            
            # Get request details to determine document type
            request = await get_service_request(request_id)
            
            if not request:
                await callback.answer(
                    "❌ Zayavka topilmadi",
                    show_alert=True
                )
                return
            
            # Determine document type based on workflow
            doc_type = 'connection'
            if request.get('workflow_type') == 'technical_service':
                doc_type = 'technical_service'
            elif request.get('created_by_staff'):
                doc_type = 'staff_created'
            
            # Generate ACT document
            word_generator = MockWordGenerator()
            file_path = await word_generator.generate_act_document(
                request_id=request_id,
                document_type=doc_type
            )
            
            if file_path:
                # Send document
                await callback.message.answer_document(
                    open(file_path, 'rb'),
                    caption=f"📄 Xizmat buyurtmasi #{request_id}"
                )
                
                await callback.answer(
                    "✅ Word hujjat yuborildi"
                )
            else:
                await callback.answer(
                    "❌ Hujjat yaratishda xatolik",
                    show_alert=True
                )
        except Exception as e:
            logger.error(f"Error generating Word document: {e}")
            await callback.answer(
                "❌ Xatolik yuz berdi",
                show_alert=True
            )

    @router.callback_query(F.data == "mgr_prev_application")
    async def prev_application_callback(callback: CallbackQuery, state: FSMContext):
        """Manager previous application callback handler"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            # Get current index from state
            data = await state.get_data()
            current_index = data.get('current_application_index', 0)
            
            # Decrease index
            current_index = max(0, current_index - 1)
            
            # Update state
            await state.update_data(current_application_index=current_index)
            
            # Trigger view all applications with new index
            await view_all_applications_callback(callback, state)
            
        except Exception as e:
            logger.error(f"Error in prev_application_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "mgr_next_application")
    async def next_application_callback(callback: CallbackQuery, state: FSMContext):
        """Manager next application callback handler"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'manager':
                await callback.answer("Ruxsat yo'q!", show_alert=True)
                return
            
            # Get current index from state
            data = await state.get_data()
            current_index = data.get('current_application_index', 0)
            
            # Get total applications count
            access_control = MockWorkflowAccessControl()
            requests = await access_control.get_filtered_requests_for_role(
                user_id=user['id'],
                user_role='manager'
            )
            
            # Increase index
            current_index = min(len(requests) - 1, current_index + 1)
            
            # Update state
            await state.update_data(current_application_index=current_index)
            
            # Trigger view all applications with new index
            await view_all_applications_callback(callback, state)
            
        except Exception as e:
            logger.error(f"Error in next_application_callback: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    return router 