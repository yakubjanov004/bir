"""
Call Center Operator Inbox Handler - To'liq yangilangan versiya

Bu modul call center operator'larining inbox funksiyalarini boshqaradi.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Optional, Dict, Any, List
from datetime import datetime

# States imports
from states.call_center import CallCenterInboxStates
from filters.role_filter import RoleFilter
from aiogram.filters import StateFilter
from keyboards.call_center_buttons import (
    get_operator_resolve_keyboard,
    get_operator_cancel_keyboard,
    get_operator_back_to_inbox_keyboard,
    get_operator_navigation_keyboard
)

# Mock functions for call center operator
async def get_operator_applications(operator_id: int):
    """Mock get operator applications"""
    return [
        {
            'id': 'req_001_2024_01_15',
            'client_name': 'Aziz Karimov',
            'client_phone': '+998901234567',
            'client_location': 'Tashkent, Chorsu tumani, 45-uy',
            'created_at': datetime.now(),
            'issue_type': 'complaint',
            'issue_description': 'Internet juda sekin ishlayapti',
            'client_expectation': 'Tezroq internet kerak',
            'supervisor_notes': 'Mijoz juda norozi, tez yordam kerak',
            'status': 'assigned_to_operator',
            'priority': 'high',
            'assigned_by': 'Call Center Supervisor'
        },
        {
            'id': 'req_002_2024_01_16',
            'client_name': 'Malika Toshmatova',
            'client_phone': '+998901234568',
            'client_location': 'Tashkent, Yunusabad tumani, 23-uy',
            'created_at': datetime.now(),
            'issue_type': 'information',
            'issue_description': 'Yangi internet paketlari haqida ma\'lumot kerak',
            'client_expectation': 'Eng yaxshi paketni tanlash',
            'supervisor_notes': 'Mijoz yangi mijoz, batafsil ma\'lumot berish kerak',
            'status': 'assigned_to_operator',
            'priority': 'normal',
            'assigned_by': 'Call Center Supervisor'
        },
        {
            'id': 'req_003_2024_01_17',
            'client_name': 'Bobur Rahimov',
            'client_phone': '+998901234569',
            'client_location': 'Tashkent, Shayxontohur tumani, 67-uy',
            'created_at': datetime.now(),
            'issue_type': 'support',
            'issue_description': 'Router ishlamayapti',
            'client_expectation': 'Router o\'rnatish kerak',
            'supervisor_notes': 'Mijoz texnik yordam so\'rayapti',
            'status': 'assigned_to_operator',
            'priority': 'high',
            'assigned_by': 'Call Center Supervisor'
        },
        {
            'id': 'req_004_2024_01_18',
            'client_name': 'Dilfuza Karimova',
            'client_phone': '+998901234570',
            'client_location': 'Tashkent, Sergeli tumani, 89-uy',
            'created_at': datetime.now(),
            'issue_type': 'request',
            'issue_description': 'Hisob-kitobda xatolik bor',
            'client_expectation': 'Hisobni to\'g\'rilash',
            'supervisor_notes': 'Mijoz hisob-kitob haqida savol berdi',
            'status': 'assigned_to_operator',
            'priority': 'normal',
            'assigned_by': 'Call Center Supervisor'
        },
        {
            'id': 'req_005_2024_01_19',
            'client_name': 'Jahongir Toshmatov',
            'client_phone': '+998901234571',
            'client_location': 'Tashkent, Yashnobod tumani, 12-uy',
            'created_at': datetime.now(),
            'issue_type': 'complaint',
            'issue_description': 'Xizmatni bekor qilmoqchi',
            'client_expectation': 'Xizmatni bekor qilish',
            'supervisor_notes': 'Mijoz xizmatni bekor qilmoqchi',
            'status': 'assigned_to_operator',
            'priority': 'high',
            'assigned_by': 'Call Center Supervisor'
        }
    ]

async def contact_client(client_phone: str, client_name: str):
    """Mock contact client"""
    try:
        # Mock successful contact
        return True
    except Exception as e:
        return False

async def resolve_issue(application_id: str, resolution_notes: str, resolution_type: str):
    """Mock resolve issue"""
    try:
        # Mock successful resolution
        return True
    except Exception as e:
        return False

def get_call_center_inbox_router():
    """Get call center inbox router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.callback_query(F.data.startswith("open_inbox_"))
    async def handle_inbox_notification(callback: CallbackQuery, state: FSMContext):
        """Handle inbox notification button click"""
        await callback.answer()
        
        # Extract request ID
        request_id_short = callback.data.replace("open_inbox_", "")
        
        # Show inbox
        await show_call_center_inbox_from_notification(callback.message, state, request_id_short)
    
    async def show_call_center_inbox_from_notification(message: Message, state: FSMContext, target_request_id: str = None):
        """Show call center inbox with focus on specific request"""
        # Show regular inbox
        await call_center_inbox(message, state)

    @router.message(F.text.in_(['📥 Inbox', '📥 Входящие']))
    async def call_center_inbox(message: Message, state: FSMContext):
        """Handle operator inbox"""
        try:
            # Get operator applications
            applications = await get_operator_applications(message.from_user.id)
            
            if not applications:
                text = "📭 Sizga biriktirilgan arizalar yo'q."
                await message.answer(text)
                return
            
            # Store applications in state
            await state.update_data(applications=applications, current_index=0)
            
            # Show first application
            await show_application_details(message, applications[0], applications, 0)
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def show_application_details(message_or_callback, application, applications, index):
        """Show application details with navigation"""
        try:
            # Format issue type
            issue_type_emoji = {
                'complaint': '🚨',
                'information': 'ℹ️',
                'support': '🔧',
                'request': '📋'
            }.get(application['issue_type'], '📄')
            
            issue_type_text = {
                'complaint': 'Shikoyat',
                'information': 'Ma\'lumot',
                'support': 'Yordam',
                'request': 'So\'rov'
            }.get(application['issue_type'], 'Boshqa')
            
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
            
            # Format date
            created_date = application['created_at'].strftime('%d.%m.%Y %H:%M')
            
            # To'liq ma'lumot
            text = (
                f"{issue_type_emoji} <b>{issue_type_text} - To'liq ma'lumot</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"📅 <b>Sana:</b> {created_date}\n"
                f"👤 <b>Mijoz:</b> {application['client_name']}\n"
                f"📞 <b>Telefon:</b> {application['client_phone']}\n"
                f"📍 <b>Manzil:</b> {application['client_location']}\n"
                f"📝 <b>Muammo:</b> {application['issue_description']}\n"
                f"🎯 <b>Mijoz kutayotgani:</b> {application['client_expectation']}\n"
                f"📋 <b>Supervisor izohi:</b> {application['supervisor_notes']}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n"
                f"👨‍💼 <b>Yuboruvchi:</b> {application['assigned_by']}\n\n"
                f"📊 <b>Ariza #{index + 1} / {len(applications)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_operator_navigation_keyboard(index, len(applications), application['id'], 'uz')
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "operator_prev_application")
    async def operator_prev_application(callback: CallbackQuery, state: FSMContext):
        """Navigate to previous application"""
        try:
            await callback.answer()
            
            data = await state.get_data()
            applications = data.get('applications', [])
            current_index = data.get('current_index', 0)
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu birinchi ariza")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "operator_next_application")
    async def operator_next_application(callback: CallbackQuery, state: FSMContext):
        """Navigate to next application"""
        try:
            await callback.answer()
            
            data = await state.get_data()
            applications = data.get('applications', [])
            current_index = data.get('current_index', 0)
            
            if current_index < len(applications) - 1:
                new_index = current_index + 1
                await state.update_data(current_index=new_index)
                await show_application_details(callback, applications[new_index], applications, new_index)
            else:
                await callback.answer("Bu oxirgi ariza")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("operator_contact_client_"))
    async def contact_client_handler(callback: CallbackQuery, state: FSMContext):
        """Handle contact client"""
        try:
            await callback.answer()
            
            application_id = callback.data.replace("operator_contact_client_", "")
            
            # Get current application
            data = await state.get_data()
            applications = data.get('applications', [])
            current_index = data.get('current_index', 0)
            
            if current_index < len(applications):
                application = applications[current_index]
                
                # Mock contact client
                success = await contact_client(application['client_phone'], application['client_name'])
                
                if success:
                    # Show contact confirmation
                    contact_text = (
                        f"📞 <b>Mijoz bilan bog'lanish</b>\n\n"
                        f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                        f"👤 <b>Mijoz:</b> {application['client_name']}\n"
                        f"📞 <b>Telefon:</b> {application['client_phone']}\n"
                        f"📍 <b>Manzil:</b> {application['client_location']}\n"
                        f"📝 <b>Muammo:</b> {application['issue_description']}\n\n"
                        f"✅ Mijoz bilan bog'lanish muvaffaqiyatli!"
                    )
                    
                    # Create resolve issue button
                    resolve_button = InlineKeyboardButton(
                        text="✅ Muammoni hal qilish",
                        callback_data=f"operator_resolve_issue_{application_id}"
                    )
                    back_button = InlineKeyboardButton(
                        text="⬅️ Orqaga qaytish",
                        callback_data="operator_back_to_application"
                    )
                    keyboard = get_operator_resolve_keyboard(lang)
                    
                    await callback.message.edit_text(
                        contact_text,
                        parse_mode='HTML',
                        reply_markup=keyboard
                    )
                    await callback.answer("✅ Mijoz bilan bog'landingiz!")
                else:
                    await callback.answer("❌ Bog'lanishda xatolik yuz berdi", show_alert=True)
            else:
                await callback.answer("❌ Ariza topilmadi", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("operator_resolve_issue_"))
    async def resolve_issue_handler(callback: CallbackQuery, state: FSMContext):
        """Handle resolve issue"""
        try:
            await callback.answer()
            
            application_id = callback.data.replace("operator_resolve_issue_", "")
            
            # Get current application
            data = await state.get_data()
            applications = data.get('applications', [])
            current_index = data.get('current_index', 0)
            
            if current_index < len(applications):
                application = applications[current_index]
                
                # Show resolution input
                resolution_text = (
                    f"✅ <b>Muammoni hal qilish</b>\n\n"
                    f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                    f"👤 <b>Mijoz:</b> {application['client_name']}\n"
                    f"📞 <b>Telefon:</b> {application['client_phone']}\n"
                    f"📝 <b>Muammo:</b> {application['issue_description']}\n\n"
                    f"📝 Iltimos, qilgan ishlaringizni yozing:\n"
                    f"• Qanday yordam berdingiz\n"
                    f"• Qanday hal qildingiz\n"
                    f"• Mijoz qoniqdi mi\n\n"
                    f"<i>Masalan: Mijoz bilan bog'landim, internet tezligini oshirdim, mijoz qoniqdi</i>"
                )
                
                # Store application info in state
                await state.update_data(
                    current_resolve_application_id=application_id,
                    current_resolve_application_data=application
                )
                
                keyboard = get_operator_cancel_keyboard(lang)
                
                await callback.message.edit_text(
                    resolution_text,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
                
                # Set state to wait for resolution input
                await state.set_state(CallCenterInboxStates.entering_resolution_notes)
                
            else:
                await callback.answer("❌ Ariza topilmadi", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(CallCenterInboxStates.entering_resolution_notes)
    async def handle_resolution_notes_input(message: Message, state: FSMContext):
        """Handle resolution notes input"""
        try:
            # Get the resolution notes
            resolution_notes = message.text.strip()
            
            if len(resolution_notes) < 10:
                await message.answer(
                    "⚠️ Iltimos, kamida 10 ta belgi kiriting. Qilgan ishlaringizni batafsil yozing."
                )
                return
            
            # Get application data from state
            data = await state.get_data()
            application_id = data.get('current_resolve_application_id')
            application = data.get('current_resolve_application_data')
            applications = data.get('applications', [])
            current_index = data.get('current_index', 0)
            
            if not application_id or not application:
                await message.answer("❌ Ariza ma'lumotlari topilmadi. Iltimos, qaytadan urinib ko'ring.")
                return
            
            # Mock resolve issue
            success = await resolve_issue(application_id, resolution_notes, "resolved")
            
            if success:
                # Show completion confirmation
                completion_text = (
                    f"✅ <b>Muammo hal qilindi!</b>\n\n"
                    f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                    f"👤 <b>Mijoz:</b> {application['client_name']}\n"
                    f"📞 <b>Telefon:</b> {application['client_phone']}\n"
                    f"📝 <b>Muammo:</b> {application['issue_description']}\n\n"
                    f"📝 <b>Qilgan ishlar:</b>\n"
                    f"<i>{resolution_notes}</i>\n\n"
                    f"✅ Ariza yakunlandi va mijozga xabar yuborildi."
                )
                
                keyboard = get_operator_back_to_inbox_keyboard(lang)
                
                await message.answer(
                    completion_text,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
                
                # Remove the application from the list
                if applications and current_index < len(applications):
                    applications.pop(current_index)
                    await state.update_data(applications=applications)
                    
                    if applications:
                        # Show next application or previous if at end
                        new_index = min(current_index, len(applications) - 1)
                        await state.update_data(current_index=new_index)
                        
                        # Show updated application list
                        await show_application_details(message, applications[new_index], applications, new_index)
                    else:
                        # No more applications
                        await message.answer("📭 Barcha arizalar hal qilindi!")
                
                # Clear the waiting state
                await state.clear()
                
            else:
                await message.answer("❌ Muammoni hal qilishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            
        except Exception as e:
            print(f"Error in handle_resolution_notes_input: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "operator_back_to_application")
    async def back_to_application_handler(callback: CallbackQuery, state: FSMContext):
        """Return to application details"""
        try:
            await callback.answer()
            
            # Get current application
            data = await state.get_data()
            applications = data.get('applications', [])
            current_index = data.get('current_index', 0)
            
            if current_index < len(applications):
                await show_application_details(callback, applications[current_index], applications, current_index)
            else:
                await callback.answer("❌ Ariza topilmadi", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "operator_back_to_inbox")
    async def back_to_inbox_handler(callback: CallbackQuery, state: FSMContext):
        """Return to inbox"""
        try:
            await callback.answer()
            
            # Get applications
            applications = await get_operator_applications(callback.from_user.id)
            
            if not applications:
                await callback.message.edit_text("📭 Sizga biriktirilgan arizalar yo'q.")
                return
            
            # Reset to first application
            await state.update_data(applications=applications, current_index=0)
            await show_application_details(callback, applications[0], applications, 0)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router
