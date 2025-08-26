"""
Technician Inbox Handler - To'liq yangilangan versiya

Bu modul texnik uchun inbox funksionalligini o'z ichiga oladi.
Qabul qilish, diagnostika, ombor bilan ishlash va yakunlash funksiyalari bilan.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.technician_buttons import (
    get_technician_inbox_keyboard, 
    get_technician_back_keyboard,
    get_diagnostic_keyboard,
    get_cancel_keyboard,
    get_warehouse_confirmation_keyboard,
    get_warehouse_items_keyboard,
    get_warehouse_quantity_keyboard,
    get_work_completion_keyboard,
    get_work_notes_keyboard,
    get_back_to_application_keyboard,
    get_application_action_keyboard
)
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from filters.role_filter import RoleFilter
from states.technician_states import TechnicianStates

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'technician',
        'language': 'uz',
        'full_name': 'Test Technician',
        'phone_number': '+998901234567'
    }

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    return 'uz'

async def get_technician_applications(user_id: int):
    """Mock get technician applications"""
    now = datetime.now()
    
    return [
        {
            'id': 'req_001_2024_01_15',
            'workflow_type': 'technical_service',
            'current_status': 'assigned_to_technician',
            'contact_info': {
                'full_name': 'Aziz Karimov',
                'phone': '+998901234567',
                'phone_number': '+998901234567',
                'email': 'aziz.karimov@example.com'
            },
            'created_at': now - timedelta(hours=3),
            'description': 'Router ishlamayapti\nYangi router kerak\nManzil: Tashkent, Shayxontohur tumani, 67-uy',
            'location': 'Tashkent, Shayxontohur tumani, 67-uy',
            'priority': 'urgent',
            'service_type': 'Router replacement',
            'equipment_needed': 'Yangi router',
            'estimated_cost': '300,000 so\'m',
            'expected_completion': '1 kun',
            'diagnostic_result': None,
            'work_started': False,
            'warehouse_needed': False,
            'work_completed': False,
            'work_notes': ''
        },
        {
            'id': 'req_002_2024_01_16',
            'workflow_type': 'connection_request',
            'current_status': 'assigned_to_technician',
            'contact_info': {
                'full_name': 'Malika Toshmatova',
                'phone': '+998901234568',
                'phone_number': '+998901234568',
                'email': 'malika.toshmatova@example.com'
            },
            'created_at': now - timedelta(hours=2, minutes=30),
            'description': 'Internet ulanish arizasi\nTariff: 100 Mbps\nB2C mijoz\nManzil: Tashkent, Chorsu tumani, 15-uy',
            'location': 'Tashkent, Chorsu tumani, 15-uy',
            'priority': 'high',
            'tariff': '100 Mbps',
            'connection_type': 'B2C',
            'equipment_needed': 'Router, optic kabel',
            'estimated_cost': '500,000 so\'m',
            'expected_completion': '3-5 kun',
            'diagnostic_result': None,
            'work_started': False,
            'warehouse_needed': False,
            'work_completed': False,
            'work_notes': ''
        },
        {
            'id': 'req_003_2024_01_17',
            'workflow_type': 'technical_service',
            'current_status': 'assigned_to_technician',
            'contact_info': {
                'full_name': 'Jasur Rahimov',
                'phone': '+998901234569',
                'phone_number': '+998901234569',
                'email': 'jasur.rahimov@example.com'
            },
            'created_at': now - timedelta(hours=1, minutes=45),
            'description': 'WiFi signal kuchsiz\nSignal kuchaytirgich kerak\nManzil: Tashkent, Mirabad tumani, 34-uy',
            'location': 'Tashkent, Mirabad tumani, 34-uy',
            'priority': 'medium',
            'service_type': 'WiFi signal booster',
            'equipment_needed': 'WiFi extender',
            'estimated_cost': '250,000 so\'m',
            'expected_completion': '2-3 kun',
            'diagnostic_result': None,
            'work_started': False,
            'warehouse_needed': False,
            'work_completed': False,
            'work_notes': ''
        },
        {
            'id': 'req_004_2024_01_18',
            'workflow_type': 'technical_service',
            'current_status': 'assigned_to_technician',
            'contact_info': {
                'full_name': 'Dilfuza Karimova',
                'phone': '+998901234570',
                'phone_number': '+998901234570',
                'email': 'dilfuza.karimova@example.com'
            },
            'created_at': now - timedelta(hours=1, minutes=20),
            'description': 'TV signal yo\'q\nKabel uzilgan\nManzil: Tashkent, Yunusabad tumani, 45-uy',
            'location': 'Tashkent, Yunusabad tumani, 45-uy',
            'priority': 'medium',
            'service_type': 'TV signal repair',
            'equipment_needed': 'Yangi kabel',
            'estimated_cost': '150,000 so\'m',
            'expected_completion': '1-2 kun',
            'diagnostic_result': None,
            'work_started': False,
            'warehouse_needed': False,
            'work_completed': False,
            'work_notes': ''
        },
        {
            'id': 'req_005_2024_01_19',
            'workflow_type': 'connection_request',
            'current_status': 'assigned_to_technician',
            'contact_info': {
                'full_name': 'Asadbek Abdullayev',
                'phone': '+998901234571',
                'phone_number': '+998901234571',
                'email': 'asadbek.abdullayev@example.com'
            },
            'created_at': now - timedelta(hours=1, minutes=10),
            'description': 'Internet ulanish arizasi\nTariff: 50 Mbps\nB2B mijoz\nManzil: Tashkent, Sergeli tumani, 78-uy',
            'location': 'Tashkent, Sergeli tumani, 78-uy',
            'priority': 'normal',
            'tariff': '50 Mbps',
            'connection_type': 'B2B',
            'equipment_needed': 'Router, switch',
            'estimated_cost': '800,000 so\'m',
            'expected_completion': '5-7 kun',
            'diagnostic_result': None,
            'work_started': False,
            'warehouse_needed': False,
            'work_completed': False,
            'work_notes': ''
        }
    ]

# Mock warehouse functions
async def get_warehouse_items():
    """Mock get warehouse items"""
    return [
        {
            'id': 1,
            'name': 'Router TP-Link Archer C6',
            'category': 'Router',
            'quantity': 15,
            'price': '250,000 so\'m'
        },
        {
            'id': 2,
            'name': 'Optic kabel 100m',
            'category': 'Cable',
            'quantity': 25,
            'price': '50,000 so\'m'
        },
        {
            'id': 3,
            'name': 'WiFi extender TP-Link',
            'category': 'WiFi',
            'quantity': 8,
            'price': '180,000 so\'m'
        },
        {
            'id': 4,
            'name': 'TV kabel RG6',
            'category': 'Cable',
            'quantity': 30,
            'price': '25,000 so\'m'
        },
        {
            'id': 5,
            'name': 'Switch 8-port',
            'category': 'Network',
            'quantity': 12,
            'price': '350,000 so\'m'
        }
    ]

async def request_warehouse_item(item_id: int, quantity: int, request_id: str):
    """Mock request warehouse item"""
    print(f"Mock: Requesting warehouse item {item_id}, quantity {quantity} for request {request_id}")
    return True

async def complete_work(request_id: str, work_notes: str, warehouse_used: bool = False):
    """Mock complete work"""
    print(f"Mock: Completing work for request {request_id} with notes: {work_notes}")
    return True

def get_technician_inbox_router():
    """Router for technician inbox functionality"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("technician")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📥 Inbox", "📥 Входящие"]))
    async def view_inbox(message: Message, state: FSMContext):
        """Technician view inbox handler"""
        try:
            # Check user role first - only process if user is technician
            from loader import get_user_role
            user_role = get_user_role(message.from_user.id)
            if user_role != 'technician':
                return  # Skip processing for non-technician users
            
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'technician':
                return
            
            lang = user.get('language', 'uz')
            
            # Get technician applications
            applications = await get_technician_applications(message.from_user.id)
            
            if not applications:
                no_applications_text = (
                    "📭 Hozircha sizga biriktirilgan arizalar yo'q."
                    if lang == 'uz' else
                    "📭 Пока нет заявок, назначенных вам."
                )
                
                await message.answer(
                    text=no_applications_text,
                    reply_markup=get_technician_back_keyboard(lang)
                )
                return
            
            # Store applications in state
            await state.update_data(
                applications=applications,
                current_app_index=0,
                lang=lang
            )
            
            # Show first application
            await show_application_details(message, applications[0], applications, 0)
            
        except Exception as e:
            print(f"Error in view_inbox: {e}")

    async def show_application_details(message_or_callback, application, applications, index):
        """Show application details with technician actions"""
        try:
            # Format workflow type
            workflow_type_emoji = {
                'connection_request': '🔌',
                'technical_service': '🔧',
                'call_center_direct': '📞'
            }.get(application['workflow_type'], '📄')
            
            workflow_type_text = {
                'connection_request': 'Ulanish arizasi',
                'technical_service': 'Texnik xizmat',
                'call_center_direct': 'Call Center'
            }.get(application['workflow_type'], 'Boshqa')
            
            # Format priority
            priority_emoji = {
                'urgent': '🚨',
                'high': '🔴',
                'medium': '🟡',
                'normal': '🟢'
            }.get(application.get('priority', 'normal'), '🟢')
            
            priority_text = {
                'urgent': 'Shoshilinch',
                'high': 'Yuqori',
                'medium': 'O\'rtacha',
                'normal': 'Oddiy'
            }.get(application.get('priority', 'normal'), 'Oddiy')
            
            # Format date
            created_date = application['created_at'].strftime('%d.%m.%Y %H:%M')
            
            # Get additional details
            tariff_info = application.get('tariff', '')
            connection_type = application.get('connection_type', '')
            equipment_needed = application.get('equipment_needed', '')
            estimated_cost = application.get('estimated_cost', '')
            expected_completion = application.get('expected_completion', '')
            diagnostic_result = application.get('diagnostic_result', '')
            work_started = application.get('work_started', False)
            warehouse_needed = application.get('warehouse_needed', False)
            work_completed = application.get('work_completed', False)
            work_notes = application.get('work_notes', '')
            
            # Work status
            work_status = "⏳ Ish boshlanmagan"
            if work_started:
                work_status = "🔄 Ish jarayonda"
            if work_completed:
                work_status = "✅ Ish tugallangan"
            
            # Clean text with essential information
            text = (
                f"{workflow_type_emoji} <b>{workflow_type_text} - Texnik ko'rinishi</b>\n\n"
                f"🆔 <b>ID:</b> {application['id']}\n"
                f"📅 <b>Sana:</b> {created_date}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"📍 <b>Manzil:</b> {application['location']}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n"
                f"📝 <b>Tavsif:</b> {application['description'][:100]}{'...' if len(application['description']) > 100 else ''}\n"
            )
            
            # Add essential additional details
            if tariff_info:
                text += f"📊 <b>Tarif:</b> {tariff_info}\n"
            if connection_type:
                text += f"🔗 <b>Ulanish turi:</b> {connection_type}\n"
            if equipment_needed:
                text += f"🔧 <b>Kerakli jihozlar:</b> {equipment_needed}\n"
            if estimated_cost:
                text += f"💰 <b>Narx:</b> {estimated_cost}\n"
            if expected_completion:
                text += f"⏱ <b>Muddat:</b> {expected_completion}\n"
            
            # Add work status
            text += f"\n{work_status}\n"
            
            # Add diagnostic result if available
            if diagnostic_result:
                text += f"🔍 <b>Diagnostika:</b> {diagnostic_result}\n"
            
            # Add work notes if available
            if work_notes:
                text += f"📝 <b>Ish izohi:</b> {work_notes}\n"
            
            text += f"\n📊 <b>Ariza #{index + 1} / {len(applications)}</b>"
            
            # Create action keyboard based on work status
            keyboard = get_technician_action_keyboard(application, index, len(applications))
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            print(f"Error in show_application_details: {e}")

    @router.callback_query(F.data == "tech_prev_application")
    async def show_previous_application(callback: CallbackQuery, state: FSMContext):
        """Show previous application"""
        try:
            await callback.answer()
            
            # Get current index from state
            data = await state.get_data()
            current_index = data.get('current_app_index', 0)
            applications = data.get('applications', [])
            
            if not applications:
                await callback.answer("Arizalar topilmadi")
                return
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu birinchi ariza")
                
        except Exception as e:
            print(f"Error in show_previous_application: {e}")

    @router.callback_query(F.data == "tech_next_application")
    async def show_next_application(callback: CallbackQuery, state: FSMContext):
        """Show next application"""
        try:
            await callback.answer()
            
            # Get current index from state
            data = await state.get_data()
            current_index = data.get('current_app_index', 0)
            applications = data.get('applications', [])
            
            if not applications:
                await callback.answer("Arizalar topilmadi")
                return
            
            if current_index < len(applications) - 1:
                new_index = current_index + 1
                await state.update_data(current_app_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu oxirgi ariza")
                
        except Exception as e:
            print(f"Error in show_next_application: {e}")

    @router.callback_query(F.data == "tech_accept_work")
    async def accept_work_handler(callback: CallbackQuery, state: FSMContext):
        """Handle accept work button"""
        try:
            await callback.answer()
            
            # Get current application
            data = await state.get_data()
            current_index = data.get('current_app_index', 0)
            applications = data.get('applications', [])
            # Retrieve user language (default to 'uz' if not found)
            lang = await get_user_lang(callback.from_user.id)
            
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            application = applications[current_index]
            
            # Update work status
            applications[current_index]['work_started'] = True
            await state.update_data(applications=applications)
            
            # Show confirmation
            confirmation_text = (
                f"✅ <b>Ish qabul qilindi!</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📍 <b>Manzil:</b> {application['location']}\n"
                f"⏰ <b>Qabul qilingan vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                f"🔍 Endi diagnostika qo'yishingiz kerak."
            )
            
            # Create diagnostic button
            keyboard = get_diagnostic_keyboard(lang)
            
            await callback.message.edit_text(
                confirmation_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in accept_work_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "tech_start_diagnostic")
    async def start_diagnostic_handler(callback: CallbackQuery, state: FSMContext):
        """Handle start diagnostic button"""
        try:
            await callback.answer()
            
            # Get current application
            data = await state.get_data()
            current_index = data.get('current_app_index', 0)
            applications = data.get('applications', [])
            # Retrieve user language
            lang = await get_user_lang(callback.from_user.id)
            
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            application = applications[current_index]
            
            # Store application info in state
            await state.update_data(
                current_application_id=application['id'],
                current_application_data=application
            )
            
            # Show diagnostic input prompt
            input_text = (
                f"🔍 <b>Diagnostika natijasini kiriting</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📍 <b>Manzil:</b> {application['location']}\n\n"
                f"🔍 Iltimos, diagnostika natijasini yozing:\n"
                f"• Muammo turi\n"
                f"• Kerakli jihozlar\n"
                f"• Ish vaqti\n"
                f"• Qo'shimcha ma'lumotlar"
            )
            
            keyboard = get_cancel_keyboard(lang)
            
            await callback.message.edit_text(
                input_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Set state to wait for diagnostic input
            await state.set_state(TechnicianStates.waiting_for_diagnostic)
            
        except Exception as e:
            print(f"Error in start_diagnostic_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.message(TechnicianStates.waiting_for_diagnostic)
    async def handle_diagnostic_input(message: Message, state: FSMContext):
        """Handle diagnostic input"""
        try:
            # Get the diagnostic text
            diagnostic_text = message.text.strip()
            # Retrieve user language
            lang = await get_user_lang(message.from_user.id)
            
            if len(diagnostic_text) < 10:
                await message.answer(
                    "⚠️ Iltimos, kamida 10 ta belgi kiriting. Diagnostika natijasini batafsil yozing."
                )
                return
            
            # Get application data from state
            data = await state.get_data()
            application = data.get('current_application_data')
            
            if not application:
                await message.answer("❌ Ariza ma'lumotlari topilmadi. Iltimos, qaytadan urinib ko'ring.")
                return
            
            # Update application diagnostic result
            applications = data.get('applications', [])
            current_index = data.get('current_app_index', 0)
            
            if applications and current_index < len(applications):
                applications[current_index]['diagnostic_result'] = diagnostic_text
                await state.update_data(applications=applications)
            
            # Show warehouse question
            warehouse_text = (
                f"✅ <b>Diagnostika qo'yildi!</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"🔍 <b>Diagnostika:</b>\n"
                f"<i>{diagnostic_text}</i>\n\n"
                f"📦 <b>Ombor bilan ishlaysizmi?</b>\n"
                f"Agar kerakli jihozlar omborda bo'lsa, ularni olish kerak."
            )
            
            keyboard = get_warehouse_confirmation_keyboard(lang)
            
            await message.answer(
                warehouse_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Clear the waiting state
            await state.clear()
            
        except Exception as e:
            print(f"Error in handle_diagnostic_input: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "tech_warehouse_yes")
    async def warehouse_yes_handler(callback: CallbackQuery, state: FSMContext):
        """Handle warehouse yes choice"""
        try:
            await callback.answer()
            
            # Get application data from state
            data = await state.get_data()
            application = data.get('current_application_data')
            
            if not application:
                await callback.answer("Ariza ma'lumotlari topilmadi")
                return
            
            # Store application info in state
            await state.update_data(
                current_application_id=application['id'],
                current_application_data=application
            )
            
            # Get warehouse items
            warehouse_items = await get_warehouse_items()
            
            # Create selection keyboard
            buttons = []
            for item in warehouse_items:
                buttons.append([InlineKeyboardButton(
                    text=f"📦 {item['name']} - {item['price']} ({item['quantity']} dona)",
                    callback_data=f"tech_select_item_{item['id']}"
                )])
            
            # Add custom input button
            buttons.append([InlineKeyboardButton(
                text="✏️ Boshqa mahsulot kiritish",
                callback_data="tech_custom_warehouse_item"
            )])
            
            # Add cancel button
            buttons.append([InlineKeyboardButton(
                text="❌ Bekor qilish",
                callback_data="tech_back_to_application"
            )])
            
            text = (
                f"📦 <b>Ombor jihozlari</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📍 <b>Manzil:</b> {application['location']}\n\n"
                f"Kerakli jihozlarni tanlang yoki boshqa mahsulot kiritish:"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in warehouse_yes_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("tech_select_item_"))
    async def select_warehouse_item_handler(callback: CallbackQuery, state: FSMContext):
        """Handle warehouse item selection"""
        try:
            await callback.answer()
            # Retrieve user language
            lang = await get_user_lang(callback.from_user.id)
            
            item_id = int(callback.data.replace("tech_select_item_", ""))
            
            # Get application data from state
            data = await state.get_data()
            application = data.get('current_application_data')
            
            if not application:
                await callback.answer("Ariza ma'lumotlari topilmadi")
                return
            
            # Get warehouse items
            warehouse_items = await get_warehouse_items()
            selected_item = next((item for item in warehouse_items if item['id'] == item_id), None)
            
            if not selected_item:
                await callback.answer("Jihoz topilmadi")
                return
            
            # Store selected item info in state
            await state.update_data(
                selected_warehouse_item=selected_item,
                waiting_for_quantity=True
            )
            
            # Show quantity input prompt
            input_text = (
                f"📦 <b>Miqdorni kiriting</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📍 <b>Manzil:</b> {application['location']}\n"
                f"📦 <b>Tanlangan mahsulot:</b> {selected_item['name']}\n"
                f"💰 <b>Narx:</b> {selected_item['price']}\n"
                f"📊 <b>Mavjud:</b> {selected_item['quantity']} dona\n\n"
                f"📝 Iltimos, olinadigan miqdorni kiriting:\n"
                f"• Faqat raqam (masalan: 2)\n"
                f"• Yoki miqdor + o'lchov (masalan: 5 metr, 3 kg)\n\n"
                f"<i>Maksimal: {selected_item['quantity']} dona</i>"
            )
            
            keyboard = get_warehouse_quantity_keyboard(lang)
            
            await callback.message.edit_text(
                input_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Set state to wait for quantity input
            await state.set_state(TechnicianStates.waiting_for_warehouse_quantity)
            
        except Exception as e:
            print(f"Error in select_warehouse_item_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.message(TechnicianStates.waiting_for_warehouse_quantity)
    async def handle_warehouse_quantity_input(message: Message, state: FSMContext):
        """Handle warehouse quantity input"""
        try:
            # Get the quantity text
            quantity_text = message.text.strip()
            
            if len(quantity_text) < 1:
                await message.answer(
                    "⚠️ Iltimos, miqdorni kiriting."
                )
                return
            
            # Get application data from state
            data = await state.get_data()
            application = data.get('current_application_data')
            selected_item = data.get('selected_warehouse_item')
            
            if not application or not selected_item:
                await message.answer("❌ Ariza ma'lumotlari topilmadi. Iltimos, qaytadan urinib ko'ring.")
                return
            
            # Create warehouse item text
            warehouse_item_text = f"{selected_item['name']} - {quantity_text}"
            
            # Update application warehouse info
            applications = data.get('applications', [])
            current_index = data.get('current_app_index', 0)
            
            if applications and current_index < len(applications):
                applications[current_index]['warehouse_needed'] = True
                applications[current_index]['warehouse_item'] = warehouse_item_text
                await state.update_data(applications=applications)
            
            # Show confirmation
            confirmation_text = (
                f"✅ <b>Ombor so'rovi yuborildi!</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📍 <b>Manzil:</b> {application['location']}\n"
                f"📦 <b>Olinadigan mahsulot:</b>\n"
                f"<i>{warehouse_item_text}</i>\n"
                f"💰 <b>Narx:</b> {selected_item['price']}\n\n"
                f"📦 Mahsulot ombordan olinadi va sizga yetkazib beriladi."
            )
            
            # Create complete work button
            complete_button = InlineKeyboardButton(
                text="✅ Ishni yakunlash",
                callback_data="tech_complete_work"
            )
            back_button = InlineKeyboardButton(
                text="⬅️ Orqaga qaytish",
                callback_data="tech_back_to_application"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[complete_button], [back_button]])
            
            await message.answer(
                confirmation_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Clear the waiting state
            await state.clear()
            
        except Exception as e:
            print(f"Error in handle_warehouse_quantity_input: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "tech_custom_warehouse_item")
    async def custom_warehouse_item_handler(callback: CallbackQuery, state: FSMContext):
        """Handle custom warehouse item input"""
        try:
            await callback.answer()
            # Retrieve user language
            lang = await get_user_lang(callback.from_user.id)
            
            # Get application data from state
            data = await state.get_data()
            application = data.get('current_application_data')
            
            if not application:
                await callback.answer("Ariza ma'lumotlari topilmadi")
                return
            
            # Show custom input prompt
            input_text = (
                f"📦 <b>Boshqa mahsulot kiritish</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📍 <b>Manzil:</b> {application['location']}\n\n"
                f"📝 Iltimos, ombordan olinadigan mahsulotni yozing:\n"
                f"• Mahsulot nomi\n"
                f"• Miqdori (dona, metr, kg)\n"
                f"• Qo'shimcha ma'lumotlar\n\n"
                f"<i>Masalan: Router TP-Link Archer C6 - 1 dona</i>"
            )
            
            keyboard = get_cancel_keyboard(lang)
            
            await callback.message.edit_text(
                input_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Set state to wait for custom warehouse input
            await state.set_state(TechnicianStates.waiting_for_warehouse_item)
            
        except Exception as e:
            print(f"Error in custom_warehouse_item_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.message(TechnicianStates.waiting_for_warehouse_item)
    async def handle_warehouse_item_input(message: Message, state: FSMContext):
        """Handle custom warehouse item input"""
        try:
            # Get the warehouse item text
            warehouse_item_text = message.text.strip()
            
            if len(warehouse_item_text) < 5:
                await message.answer(
                    "⚠️ Iltimos, kamida 5 ta belgi kiriting. Mahsulot nomi va miqdorini yozing."
                )
                return
            
            # Get application data from state
            data = await state.get_data()
            application = data.get('current_application_data')
            
            if not application:
                await message.answer("❌ Ariza ma'lumotlari topilmadi. Iltimos, qaytadan urinib ko'ring.")
                return
            
            # Update application warehouse info
            applications = data.get('applications', [])
            current_index = data.get('current_app_index', 0)
            
            if applications and current_index < len(applications):
                applications[current_index]['warehouse_needed'] = True
                applications[current_index]['warehouse_item'] = warehouse_item_text
                await state.update_data(applications=applications)
            
            # Show confirmation
            confirmation_text = (
                f"✅ <b>Ombor so'rovi yuborildi!</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📍 <b>Manzil:</b> {application['location']}\n"
                f"📦 <b>Olinadigan mahsulot:</b>\n"
                f"<i>{warehouse_item_text}</i>\n\n"
                f"📦 Mahsulot ombordan olinadi va sizga yetkazib beriladi."
            )
            
            # Create complete work button
            complete_button = InlineKeyboardButton(
                text="✅ Ishni yakunlash",
                callback_data="tech_complete_work"
            )
            back_button = InlineKeyboardButton(
                text="⬅️ Orqaga qaytish",
                callback_data="tech_back_to_application"
            )
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[complete_button], [back_button]])
            
            await message.answer(
                confirmation_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Clear the waiting state
            await state.clear()
            
        except Exception as e:
            print(f"Error in handle_warehouse_item_input: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "tech_warehouse_no")
    async def warehouse_no_handler(callback: CallbackQuery, state: FSMContext):
        """Handle warehouse no choice"""
        try:
            await callback.answer()
            # Retrieve user language
            lang = await get_user_lang(callback.from_user.id)
            
            # Get application data from state
            data = await state.get_data()
            application = data.get('current_application_data')
            
            if not application:
                await callback.answer("Ariza ma'lumotlari topilmadi")
                return
            
            text = (
                f"✅ <b>Ombor bilan ishlash bekor qilindi</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n\n"
                f"🔧 Endi o'zingiz qilgan ishlarni yozib, arizani yakunlashingiz kerak."
            )
            
            keyboard = get_work_completion_keyboard(lang)
            
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"Error in warehouse_no_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "tech_complete_work")
    async def complete_work_handler(callback: CallbackQuery, state: FSMContext):
        """Handle complete work button"""
        try:
            await callback.answer()
            # Retrieve user language
            lang = await get_user_lang(callback.from_user.id)
            
            # Get current application
            data = await state.get_data()
            current_index = data.get('current_app_index', 0)
            applications = data.get('applications', [])
            
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            application = applications[current_index]
            
            # Store application info in state
            await state.update_data(
                current_application_id=application['id'],
                current_application_data=application
            )
            
            # Show work notes input prompt
            input_text = (
                f"✅ <b>Ishni yakunlash</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📍 <b>Manzil:</b> {application['location']}\n\n"
                f"📝 Iltimos, qilgan ishlaringizni yozing:\n"
                f"• Qilgan ishlar\n"
                f"• O'rnatilgan jihozlar\n"
                f"• Natija\n"
                f"• Qo'shimcha ma'lumotlar"
            )
            
            keyboard = get_work_notes_keyboard(lang)
            
            await callback.message.edit_text(
                input_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
            # Set state to wait for work notes input
            await state.set_state(TechnicianStates.waiting_for_work_notes)
            
        except Exception as e:
            print(f"Error in complete_work_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.message(TechnicianStates.waiting_for_work_notes)
    async def handle_work_notes_input(message: Message, state: FSMContext):
        """Handle work notes input"""
        try:
            # Get the work notes text
            work_notes_text = message.text.strip()
            
            if len(work_notes_text) < 20:
                await message.answer(
                    "⚠️ Iltimos, kamida 20 ta belgi kiriting. Qilgan ishlaringizni batafsil yozing."
                )
                return
            
            # Get application data from state
            data = await state.get_data()
            application = data.get('current_application_data')
            
            if not application:
                await message.answer("❌ Ariza ma'lumotlari topilmadi. Iltimos, qaytadan urinib ko'ring.")
                return
            
            # Update application work notes
            applications = data.get('applications', [])
            current_index = data.get('current_app_index', 0)
            
            if applications and current_index < len(applications):
                applications[current_index]['work_notes'] = work_notes_text
                applications[current_index]['work_completed'] = True
                await state.update_data(applications=applications)
            
            # Mock complete work
            warehouse_used = applications[current_index].get('warehouse_needed', False) if applications else False
            warehouse_item = applications[current_index].get('warehouse_item', '') if applications else ''
            success = await complete_work(application['id'], work_notes_text, warehouse_used)
            
            if success:
                # Show completion confirmation
                completion_text = (
                    f"✅ <b>Ish muvaffaqiyatli yakunlandi!</b>\n\n"
                    f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                    f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                    f"📍 <b>Manzil:</b> {application['location']}\n"
                    f"⏰ <b>Yakunlangan vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
                    f"📝 <b>Qilgan ishlar:</b>\n"
                    f"<i>{work_notes_text}</i>\n\n"
                    f"📦 <b>Ombor ishlatildi:</b> {'Ha' if warehouse_used else 'Yo\'q'}"
                )
                
                if warehouse_used and warehouse_item:
                    completion_text += f"\n📦 <b>Olingan mahsulot:</b> {warehouse_item}\n"
                
                completion_text += f"\n\n🎉 Ariza yakunlandi va mijozga xabar yuborildi."
                
                # Create back to inbox button
                back_button = InlineKeyboardButton(
                    text="📥 Inbox'ga qaytish",
                    callback_data="tech_back_to_inbox"
                )
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[back_button]])
                
                await message.answer(
                    completion_text,
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )
                
                # Remove the request from current session
                updated_applications = [a for a in applications if a['id'] != application['id']]
                new_index = current_index
                
                if updated_applications:
                    # Adjust index if needed
                    if new_index >= len(updated_applications):
                        new_index = len(updated_applications) - 1
                    
                    await state.update_data(
                        applications=updated_applications,
                        current_app_index=new_index
                    )
                else:
                    await state.clear()
            else:
                await message.answer("❌ Ishni yakunlashda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            
            # Clear the waiting state
            await state.clear()
            
        except Exception as e:
            print(f"Error in handle_work_notes_input: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "tech_back_to_application")
    async def back_to_application_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to application button"""
        try:
            await callback.answer()
            
            # Get current application
            data = await state.get_data()
            current_index = data.get('current_app_index', 0)
            applications = data.get('applications', [])
            
            if not applications or current_index >= len(applications):
                await callback.answer("Ariza topilmadi")
                return
            
            # Show application details again
            await show_application_details(callback, applications[current_index], applications, current_index)
            
        except Exception as e:
            print(f"Error in back_to_application_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "tech_back_to_inbox")
    async def back_to_inbox_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to inbox button"""
        try:
            await callback.answer()
            
            # Show inbox again
            await view_inbox(callback.message, state)
            
        except Exception as e:
            print(f"Error in back_to_inbox_handler: {e}")
            await callback.answer("Xatolik yuz berdi")

    return router

def get_technician_action_keyboard(application, current_index: int, total_applications: int):
    """Create action keyboard for technician based on work status"""
    return get_application_action_keyboard(application, current_index, total_applications, 'uz')