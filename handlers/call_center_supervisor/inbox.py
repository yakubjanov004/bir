"""
Call Center Supervisor Inbox Handler - Simplified Implementation

This module handles call center supervisor inbox functionality.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Optional, Dict, Any, List
from datetime import datetime

# States imports
from states.call_center_supervisor_states import CallCenterSupervisorMainMenuStates
from filters.role_filter import RoleFilter
from aiogram.filters import StateFilter
from keyboards.call_center_supervisor_buttons import (
    get_supervisor_operator_assignment_keyboard,
    get_supervisor_back_to_inbox_keyboard,
    get_supervisor_navigation_keyboard
)

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'call_center_supervisor',
        'language': 'uz',
        'full_name': 'Test Supervisor',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

async def get_supervisor_applications(user_id: int):
    """Mock get supervisor applications"""
    return [
        {
            'id': 'req_001_2024_01_15',
            'workflow_type': 'call_center_direct',
            'current_status': 'assigned_to_supervisor',
            'contact_info': {
                'full_name': 'Aziz Karimov',
                'phone': '+998901234567'
            },
            'created_at': datetime.now(),
            'description': 'Internet xizmati haqida shikoyat',
            'location': 'Tashkent, Chorsu tumani, 45-uy',
            'priority': 'high',
            'region': 'Toshkent shahri',
            'call_type': 'complaint',
            'client_issue': 'Internet juda sekin ishlayapti',
            'client_expectation': 'Tezroq internet kerak',
            'additional_notes': 'Mijoz juda norozi'
        },
        {
            'id': 'req_002_2024_01_16',
            'workflow_type': 'call_center_direct',
            'current_status': 'assigned_to_supervisor',
            'contact_info': {
                'full_name': 'Malika Toshmatova',
                'phone': '+998901234568'
            },
            'created_at': datetime.now(),
            'description': 'Yangi xizmat haqida ma\'lumot',
            'location': 'Tashkent, Yunusabad tumani, 23-uy',
            'priority': 'normal',
            'region': 'Toshkent shahri',
            'call_type': 'information',
            'client_issue': 'Yangi internet paketlari haqida ma\'lumot kerak',
            'client_expectation': 'Eng yaxshi paketni tanlash',
            'additional_notes': 'Mijoz yangi mijoz'
        },
        {
            'id': 'req_003_2024_01_17',
            'workflow_type': 'call_center_direct',
            'current_status': 'assigned_to_supervisor',
            'contact_info': {
                'full_name': 'Bobur Rahimov',
                'phone': '+998901234569'
            },
            'created_at': datetime.now(),
            'description': 'Texnik muammo haqida yordam',
            'location': 'Tashkent, Shayxontohur tumani, 67-uy',
            'priority': 'high',
            'region': 'Toshkent shahri',
            'call_type': 'support',
            'client_issue': 'Router ishlamayapti',
            'client_expectation': 'Router o\'rnatish kerak',
            'additional_notes': 'Mijoz texnik yordam so\'rayapti'
        },
        {
            'id': 'req_004_2024_01_18',
            'workflow_type': 'call_center_direct',
            'current_status': 'assigned_to_supervisor',
            'contact_info': {
                'full_name': 'Dilfuza Karimova',
                'phone': '+998901234570'
            },
            'created_at': datetime.now(),
            'description': 'Hisob-kitob haqida savol',
            'location': 'Tashkent, Sergeli tumani, 89-uy',
            'priority': 'normal',
            'region': 'Toshkent shahri',
            'call_type': 'request',
            'client_issue': 'Hisob-kitobda xatolik bor',
            'client_expectation': 'Hisobni to\'g\'rilash',
            'additional_notes': 'Mijoz hisob-kitob haqida savol berdi'
        },
        {
            'id': 'req_005_2024_01_19',
            'workflow_type': 'call_center_direct',
            'current_status': 'assigned_to_supervisor',
            'contact_info': {
                'full_name': 'Jahongir Toshmatov',
                'phone': '+998901234571'
            },
            'created_at': datetime.now(),
            'description': 'Xizmatni bekor qilish',
            'location': 'Tashkent, Yashnobod tumani, 12-uy',
            'priority': 'high',
            'region': 'Toshkent shahri',
            'call_type': 'complaint',
            'client_issue': 'Xizmatni bekor qilmoqchi',
            'client_expectation': 'Xizmatni bekor qilish',
            'additional_notes': 'Mijoz xizmatni bekor qilmoqchi'
        }
    ]

async def get_call_center_operators():
    """Mock get call center operators"""
    return [
        {
            'id': 1,
            'name': 'Aziza Abdullayeva',
            'phone': '+998 90 123 45 67',
            'status': 'available',
            'active_calls': 2
        },
        {
            'id': 2,
            'name': 'Bobur Karimov',
            'phone': '+998 91 234 56 78',
            'status': 'available',
            'active_calls': 1
        },
        {
            'id': 3,
            'name': 'Malika Toshmatova',
            'phone': '+998 92 345 67 89',
            'status': 'available',
            'active_calls': 0
        },
        {
            'id': 4,
            'name': 'Jahongir Rahimov',
            'phone': '+998 93 456 78 90',
            'status': 'busy',
            'active_calls': 3
        }
    ]

async def assign_to_call_center_operator(application_id: str, operator_id: int, supervisor_notes: str = ""):
    """Mock assign to call center operator"""
    try:
        # Mock assignment
        return True
    except Exception as e:
        return False

def get_supervisor_inbox_router():
    """Router for supervisor inbox functionality"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center_supervisor")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📥 Inbox", "📥 Входящие"]))
    async def view_inbox(message: Message, state: FSMContext):
        """Supervisor view inbox handler"""
        try:
            # Check user role first - only process if user is call_center_supervisor
            from loader import get_user_role
            user_role = get_user_role(message.from_user.id)
            if user_role != 'call_center_supervisor':
                return  # Skip processing for non-supervisor users
            
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return
            
            lang = user.get('language', 'uz')
            
            # Get supervisor applications
            applications = await get_supervisor_applications(message.from_user.id)
            
            if not applications:
                no_applications_text = (
                    "📭 Hozircha qo'ng'iroq markazi arizalari yo'q."
                    if lang == 'uz' else
                    "📭 Пока нет заявок call center."
                )
                
                await message.answer(
                    text=no_applications_text,
                    reply_markup=get_supervisor_back_to_inbox_keyboard(lang)
                )
                return
            
            # Show first application
            await show_application_details(message, applications[0], applications, 0)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def show_application_details(message_or_callback, application, applications, index):
        """Show application details with navigation"""
        try:
            # Format workflow type
            workflow_type_emoji = {
                'call_center_direct': '📞',
                'connection_request': '🔌',
                'technical_service': '🔧'
            }.get(application['workflow_type'], '📄')
            
            workflow_type_text = {
                'call_center_direct': 'Call Center arizasi',
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat'
            }.get(application['workflow_type'], 'Boshqa')
            
            # Format status
            status_emoji = {
                'pending': '🟡',
                'in_progress': '🟠',
                'completed': '🟢',
                'cancelled': '🔴'
            }.get(application['current_status'], '⚪')
            
            status_text = {
                'pending': 'Kutilmoqda',
                'in_progress': 'Jarayonda',
                'completed': 'Bajarilgan',
                'cancelled': 'Bekor qilingan'
            }.get(application['current_status'], 'Noma\'lum')
            
            # Format priority
            priority_emoji = {
                'high': '🔴',
                'normal': '🟡',
                'low': '🟢'
            }.get(application.get('priority', 'normal'), '🟡')
            
            priority_text = {
                'high': 'Yuqori',
                'normal': 'O\'rtacha',
                'low': 'Past'
            }.get(application.get('priority', 'normal'), 'O\'rtacha')
            
            # Format call type
            call_type_text = {
                'complaint': 'Shikoyat',
                'information': 'Ma\'lumot',
                'request': 'So\'rov',
                'support': 'Yordam'
            }.get(application.get('call_type', 'unknown'), 'Boshqa')
            
            # Format date
            created_date = application['created_at'].strftime('%d.%m.%Y %H:%M')
            
            # To'liq ma'lumot
            text = (
                f"{workflow_type_emoji} <b>{workflow_type_text} - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"📅 <b>Sana:</b> {created_date}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"🏛️ <b>Hudud:</b> {application.get('region', 'Noma\'lum')}\n"
                f"🏠 <b>Manzil:</b> {application.get('location', 'Noma\'lum')}\n"
                f"📝 <b>Tavsif:</b> {application['description']}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"📞 <b>Qo'ng'iroq turi:</b> {call_type_text}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n\n"
                f"📋 <b>Mijoz muammosi:</b>\n"
                f"<i>{application.get('client_issue', 'Ko\'rsatilmagan')}</i>\n\n"
                f"🎯 <b>Mijoz kutayotgani:</b>\n"
                f"<i>{application.get('client_expectation', 'Ko\'rsatilmagan')}</i>\n\n"
                f"📝 <b>Qo'shimcha izohlar:</b>\n"
                f"<i>{application.get('additional_notes', 'Yo\'q')}</i>\n\n"
                f"📊 <b>Ariza #{index + 1} / {len(applications)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_supervisor_navigation_keyboard(index, len(applications), application['id'], 'uz')
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "supervisor_prev_application")
    async def show_previous_application(callback: CallbackQuery, state: FSMContext):
        """Show previous application"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            applications = await get_supervisor_applications(callback.from_user.id)
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu birinchi ariza")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "supervisor_next_application")
    async def show_next_application(callback: CallbackQuery, state: FSMContext):
        """Show next application"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            applications = await get_supervisor_applications(callback.from_user.id)
            
            if current_index < len(applications) - 1:
                new_index = current_index + 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu oxirgi ariza")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("supervisor_assign_operator_"))
    async def assign_to_operator_handler(callback: CallbackQuery, state: FSMContext):
        """Handle assign to operator"""
        try:
            await callback.answer()
            
            application_id = callback.data.replace("supervisor_assign_operator_", "")
            
            # Get current application
            applications = await get_supervisor_applications(callback.from_user.id)
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            if current_index < len(applications):
                application = applications[current_index]
                
                # Get available operators
                operators = await get_call_center_operators()
                available_operators = [op for op in operators if op['status'] == 'available']
                
                if not available_operators:
                    await callback.answer("❌ Mavjud operatorlar yo'q", show_alert=True)
                    return
                
                # Show operator selection
                text = (
                    f"📞 <b>Operator tanlash</b>\n\n"
                    f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                    f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                    f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                    f"📝 <b>Tavsif:</b> {application['description']}\n\n"
                    f"📞 Mavjud operatorlarni tanlang:"
                )
                
                # Create operator selection buttons
                buttons = []
                for operator in available_operators:
                    status_emoji = "🟢" if operator['status'] == 'available' else "🔴"
                    buttons.append([InlineKeyboardButton(
                        text=f"{status_emoji} {operator['name']} ({operator['active_calls']} qo'ng'iroq)",
                        callback_data=f"supervisor_select_operator_{application_id}_{operator['id']}"
                    )])
                
                # Add cancel button
                buttons.append([InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data="supervisor_back_to_application"
                )])
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                
                await callback.message.edit_text(
                    text,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
                
            else:
                await callback.answer("❌ Ariza topilmadi", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("supervisor_select_operator_"))
    async def select_operator_handler(callback: CallbackQuery, state: FSMContext):
        """Handle operator selection"""
        try:
            await callback.answer()
            
            # Parse callback data
            parts = callback.data.replace("supervisor_select_operator_", "").split("_")
            application_id = parts[0]
            operator_id = int(parts[1])
            
            # Get application and operator data
            applications = await get_supervisor_applications(callback.from_user.id)
            operators = await get_call_center_operators()
            
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            if current_index < len(applications):
                application = applications[current_index]
                operator = next((op for op in operators if op['id'] == operator_id), None)
                
                if not operator:
                    await callback.answer("❌ Operator topilmadi", show_alert=True)
                    return
                
                # Show assignment confirmation
                text = (
                    f"✅ <b>Operator'ga yuborish tasdiqlash</b>\n\n"
                    f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                    f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                    f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                    f"📝 <b>Tavsif:</b> {application['description']}\n\n"
                    f"📞 <b>Tanlangan operator:</b>\n"
                    f"👤 {operator['name']}\n"
                    f"📞 {operator['phone']}\n"
                    f"📊 {operator['active_calls']} faol qo'ng'iroq\n\n"
                    f"✅ Operator'ga yuborilsinmi?"
                )
                
                keyboard = get_supervisor_operator_assignment_keyboard(lang)
                
                await callback.message.edit_text(
                    text,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
                
            else:
                await callback.answer("❌ Ariza topilmadi", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("supervisor_confirm_assign_"))
    async def confirm_assign_handler(callback: CallbackQuery, state: FSMContext):
        """Handle assignment confirmation"""
        try:
            await callback.answer()
            
            # Parse callback data
            parts = callback.data.replace("supervisor_confirm_assign_", "").split("_")
            application_id = parts[0]
            operator_id = int(parts[1])
            
            # Get application and operator data
            applications = await get_supervisor_applications(callback.from_user.id)
            operators = await get_call_center_operators()
            
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            if current_index < len(applications):
                application = applications[current_index]
                operator = next((op for op in operators if op['id'] == operator_id), None)
                
                if not operator:
                    await callback.answer("❌ Operator topilmadi", show_alert=True)
                    return
                
                # Mock assignment
                success = await assign_to_call_center_operator(application_id, operator_id)
                
                if success:
                    # Show success message
                    success_text = (
                        f"✅ <b>Ariza operator'ga yuborildi!</b>\n\n"
                        f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                        f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                        f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                        f"📝 <b>Tavsif:</b> {application['description']}\n\n"
                        f"📞 <b>Yuborilgan operator:</b>\n"
                        f"👤 {operator['name']}\n"
                        f"📞 {operator['phone']}\n\n"
                        f"✅ Operator mijoz bilan bog'lanadi."
                    )
                    
                    keyboard = get_supervisor_back_to_inbox_keyboard(lang)
                    
                    await callback.message.edit_text(
                        success_text,
                        parse_mode='HTML',
                        reply_markup=keyboard
                    )
                    await callback.answer("✅ Ariza yuborildi!")
                    
                    # Remove the application from the list
                    applications.pop(current_index)
                    
                    if applications:
                        # Show next application or previous if at end
                        new_index = min(current_index, len(applications) - 1)
                        await state.update_data(current_app_index=new_index)
                        
                        # Show updated application list
                        await show_application_details(callback, applications[new_index], applications, new_index)
                    else:
                        # No more applications
                        await callback.message.edit_text("📭 Barcha arizalar operator'larga yuborildi!")
                else:
                    await callback.answer("❌ Yuborishda xatolik yuz berdi", show_alert=True)
            else:
                await callback.answer("❌ Ariza topilmadi", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "supervisor_back_to_application")
    async def back_to_application_handler(callback: CallbackQuery, state: FSMContext):
        """Return to application details"""
        try:
            await callback.answer()
            
            # Get current application
            applications = await get_supervisor_applications(callback.from_user.id)
            current_index = await state.get_data()
            current_index = current_index.get('current_app_index', 0)
            
            if current_index < len(applications):
                await show_application_details(callback, applications[current_index], applications, current_index)
            else:
                await callback.answer("❌ Ariza topilmadi", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "supervisor_back_to_inbox")
    async def back_to_inbox_handler(callback: CallbackQuery, state: FSMContext):
        """Return to inbox"""
        try:
            await callback.answer()
            
            # Get applications
            applications = await get_supervisor_applications(callback.from_user.id)
            
            if not applications:
                await callback.message.edit_text("📭 Hozircha qo'ng'iroq markazi arizalari yo'q.")
                return
            
            # Reset to first application
            await state.update_data(current_app_index=0)
            await show_application_details(callback, applications[0], applications, 0)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router



def get_call_center_supervisor_inbox_router():
    """Get call center supervisor inbox router - alias for get_supervisor_inbox_router"""
    return get_supervisor_inbox_router()