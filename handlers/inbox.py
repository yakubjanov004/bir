"""
Manager Inbox Handler - Mock Data Version

Bu modul manager uchun inbox funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, database kerak emas.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from keyboards.manager_buttons import (
    get_inbox_navigation_keyboard,
    get_junior_assignment_keyboard,
    get_junior_confirmation_keyboard
)
import logging
import json
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Mock data for inbox messages
MOCK_INBOX_MESSAGES = [
    {
        'id': 1,
        'application_id': 'APP001',
        'title': '🔴 🔌 Ulanish so\'rovi',
        'description': 'Aziz Karimov - Internet ulanish so\'rovi',
        'client_name': 'Aziz Karimov',
        'client_phone': '+998 90 123 45 67',
        'priority': 'high',
        'workflow_type': 'connection_request',
        'status': 'new',
        'created_at': datetime.now() - timedelta(hours=2),
        'time_ago': '2 soat oldin'
    },
    {
        'id': 2,
        'application_id': 'APP002',
        'title': '🟡 🔧 Texnik xizmat',
        'description': 'Malika Yusupova - Internet tezligi past',
        'client_name': 'Malika Yusupova',
        'client_phone': '+998 91 234 56 78',
        'priority': 'normal',
        'workflow_type': 'technical_service',
        'status': 'read',
        'created_at': datetime.now() - timedelta(hours=5),
        'time_ago': '5 soat oldin'
    },
    {
        'id': 3,
        'application_id': 'APP003',
        'title': '🟢 📞 Qo\'ng\'iroq markazi',
        'description': 'Jasur Toshmatov - Hisobot so\'rovi',
        'client_name': 'Jasur Toshmatov',
        'client_phone': '+998 92 345 67 89',
        'priority': 'low',
        'workflow_type': 'call_center_direct',
        'status': 'replied',
        'created_at': datetime.now() - timedelta(days=1),
        'time_ago': '1 kun oldin'
    },
    {
        'id': 4,
        'application_id': 'APP004',
        'title': '🔴 🔌 Ulanish so\'rovi',
        'description': 'Dilfuza Rahimova - Yangi uy uchun internet',
        'client_name': 'Dilfuza Rahimova',
        'client_phone': '+998 93 456 78 90',
        'priority': 'high',
        'workflow_type': 'connection_request',
        'status': 'new',
        'created_at': datetime.now() - timedelta(hours=1),
        'time_ago': '1 soat oldin'
    },
    {
        'id': 5,
        'application_id': 'APP005',
        'title': '🟡 🔧 Texnik xizmat',
        'description': 'Rustam Alimov - Router muammosi',
        'client_name': 'Rustam Alimov',
        'client_phone': '+998 94 567 89 01',
        'priority': 'normal',
        'workflow_type': 'technical_service',
        'status': 'read',
        'created_at': datetime.now() - timedelta(hours=3),
        'time_ago': '3 soat oldin'
    }
]

# Mock data for junior managers
MOCK_JUNIOR_MANAGERS = [
    {'id': 1, 'full_name': 'Aziz Karimov', 'role': 'junior_manager'},
    {'id': 2, 'full_name': 'Malika Yusupova', 'role': 'junior_manager'},
    {'id': 3, 'full_name': 'Jasur Toshmatov', 'role': 'junior_manager'},
    {'id': 4, 'full_name': 'Dilfuza Rahimova', 'role': 'junior_manager'},
    {'id': 5, 'full_name': 'Rustam Alimov', 'role': 'junior_manager'}
]

def get_manager_inbox_router():
    """Router for manager inbox functionality with mock data"""
    router = Router()
    
    @router.message(F.text.in_(["📥 Inbox", "📥 Входящие"]))
    async def show_inbox_menu(message: Message, state: FSMContext):
        """Show inbox main menu"""
        try:
            user_id = message.from_user.id
            
            # Mock user info
            mock_user = {
                'id': user_id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Get inbox statistics
            total_messages = len(MOCK_INBOX_MESSAGES)
            new_messages = len([m for m in MOCK_INBOX_MESSAGES if m['status'] == 'new'])
            read_messages = len([m for m in MOCK_INBOX_MESSAGES if m['status'] == 'read'])
            replied_messages = len([m for m in MOCK_INBOX_MESSAGES if m['status'] == 'replied'])
            
            if lang == 'uz':
                text = f"""📥 <b>Inbox xabarlar</b>

📨 Jami xabarlar: {total_messages}
🆕 Yangi: {new_messages}
📖 O'qilgan: {read_messages}
⏳ Javob berilgan: {replied_messages}

Inbox'ni ko'rish uchun tugmani bosing:"""
            else:
                text = f"""📥 <b>Входящие сообщения</b>

📨 Всего сообщений: {total_messages}
🆕 Новые: {new_messages}
📖 Прочитанные: {read_messages}
⏳ Отвеченные: {replied_messages}

Нажмите кнопку для просмотра inbox:"""
            
            # Create keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text="📥 Inbox'ni ko'rish" if lang == 'uz' else "📥 Просмотр inbox",
                    callback_data="mgr_view_inbox"
                )
            ]])
            
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error showing inbox menu: {e}")
            await message.answer("❌ Xatolik yuz berdi")
    
    @router.callback_query(F.data == "mgr_view_inbox")
    async def view_inbox(callback: CallbackQuery, state: FSMContext):
        """View inbox messages"""
        try:
            await callback.answer()
            
            # Update state
            await state.update_data(
                inbox_messages=MOCK_INBOX_MESSAGES,
                current_index=0
            )
            
            # Show first message
            await display_inbox_message(callback, MOCK_INBOX_MESSAGES[0], 0, len(MOCK_INBOX_MESSAGES))
            
        except Exception as e:
            logger.error(f"Error viewing inbox: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_view_app")
    async def view_application_details(callback: CallbackQuery, state: FSMContext):
        """View application details"""
        try:
            await callback.answer()
            
            # Get current message from state
            state_data = await state.get_data()
            current_index = state_data.get('current_index', 0)
            inbox_messages = state_data.get('inbox_messages', MOCK_INBOX_MESSAGES)
            
            if current_index < len(inbox_messages):
                message = inbox_messages[current_index]
                
                # Show detailed view
                text = f"""📋 <b>Ariza ma'lumotlari</b>

🆔 Ariza ID: {message['application_id']}
👤 Mijoz: {message['client_name']}
📱 Telefon: {message['client_phone']}
📝 Mavzu: {message['title']}
📄 Tavsif: {message['description']}
🔴 Muhimlik: {message['priority']}
📊 Status: {message['status']}
⏰ Vaqt: {message['time_ago']}

Qanday amal bajarishni xohlaysiz?"""
                
                # Create action keyboard
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="📞 Mijoz bilan bog'lanish", callback_data="mgr_contact_client")],
                    [InlineKeyboardButton(text="👨‍💼 Kichik menejerga yuborish", callback_data="mgr_assign_jm")],
                    [InlineKeyboardButton(text="⬅️ Ortga", callback_data="mgr_back_to_inbox")]
                ])
                
                await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error viewing application details: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_contact_client")
    async def contact_client(callback: CallbackQuery, state: FSMContext):
        """Contact client"""
        try:
            await callback.answer()
            
            # Get current message from state
            state_data = await state.get_data()
            current_index = state_data.get('current_index', 0)
            inbox_messages = state_data.get('inbox_messages', MOCK_INBOX_MESSAGES)
            
            if current_index < len(inbox_messages):
                message = inbox_messages[current_index]
                
                text = f"""📞 <b>Mijoz bilan bog'lanish</b>

👤 Mijoz: {message['client_name']}
📱 Telefon: {message['client_phone']}
📝 Ariza: {message['application_id']}

Mijoz bilan bog'lanish uchun yuqoridagi telefon raqamini ishlatishingiz mumkin."""
                
                # Create back keyboard
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text="⬅️ Ortga", callback_data="mgr_view_app")
                ]])
                
                await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error contacting client: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_assign_jm")
    async def assign_to_junior_manager(callback: CallbackQuery, state: FSMContext):
        """Assign to junior manager"""
        try:
            await callback.answer()
            
            # Get current message from state
            state_data = await state.get_data()
            current_index = state_data.get('current_index', 0)
            inbox_messages = state_data.get('inbox_messages', MOCK_INBOX_MESSAGES)
            
            if current_index < len(inbox_messages):
                message = inbox_messages[current_index]
                
                # Create junior manager selection keyboard
                buttons = []
                for jm in MOCK_JUNIOR_MANAGERS:
                    buttons.append([InlineKeyboardButton(
                        text=f"👨‍💼 {jm['full_name']}",
                        callback_data=f"mgr_confirm_jm_{message['application_id']}_{jm['id']}"
                    )])
                
                # Add back button
                buttons.append([InlineKeyboardButton(
                    text="⬅️ Ortga",
                    callback_data="mgr_view_app"
                )])
                
                keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                
                text = f"""👨‍💼 <b>Kichik menejer tanlang</b>

📝 Ariza ID: {message['application_id']}
👤 Mijoz: {message['client_name']}

Quyidagi kichik menejerlardan birini tanlang:"""
                
                await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error assigning to junior manager: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("mgr_confirm_jm_"))
    async def confirm_junior_manager_assignment(callback: CallbackQuery, state: FSMContext):
        """Confirm junior manager assignment"""
        try:
            await callback.answer()
            
            # Extract data
            parts = callback.data.replace("mgr_confirm_jm_", "").split("_")
            application_id = parts[0]
            junior_manager_id = int(parts[1])
            
            # Find junior manager
            junior_manager = next((jm for jm in MOCK_JUNIOR_MANAGERS if jm['id'] == junior_manager_id), None)
            
            if junior_manager:
                text = f"""✅ <b>Tayinlash muvaffaqiyatli!</b>

📝 Ariza ID: {application_id}
👨‍💼 Kichik menejer: {junior_manager['full_name']}

Ariza muvaffaqiyatli kichik menejerga yuborildi."""
                
                # Create back keyboard
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text="⬅️ Inbox'ga qaytish", callback_data="mgr_view_inbox")
                ]])
                
                await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await callback.answer("❌ Kichik menejer topilmadi", show_alert=True)
            
        except Exception as e:
            logger.error(f"Error confirming junior manager assignment: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_back_to_inbox")
    async def back_to_inbox(callback: CallbackQuery, state: FSMContext):
        """Go back to inbox"""
        try:
            await callback.answer()
            
            # Get current message from state
            state_data = await state.get_data()
            current_index = state_data.get('current_index', 0)
            inbox_messages = state_data.get('inbox_messages', MOCK_INBOX_MESSAGES)
            
            if current_index < len(inbox_messages):
                await display_inbox_message(callback, inbox_messages[current_index], current_index, len(inbox_messages))
            
        except Exception as e:
            logger.error(f"Error going back to inbox: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_close_inbox")
    async def close_inbox(callback: CallbackQuery, state: FSMContext):
        """Close inbox"""
        try:
            await callback.answer()
            
            # Clear state
            await state.clear()
            
            text = "📥 Inbox yopildi. Asosiy menyuga qaytish uchun /start buyrug'ini ishlatishingiz mumkin."
            
            await callback.message.edit_text(text)
            
        except Exception as e:
            logger.error(f"Error closing inbox: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    return router

async def display_inbox_message(callback: CallbackQuery, message: dict, current_index: int, total_count: int):
    """Display inbox message with navigation"""
    try:
        # Format message
        text = f"""📥 <b>Inbox xabar {current_index + 1}/{total_count}</b>

{message['title']}
📝 {message['description']}
👤 {message['client_name']}
⏰ {message['time_ago']}
📊 Status: {message['status']}

Qanday amal bajarishni xohlaysiz?"""
        
        # Create navigation keyboard
        keyboard = get_inbox_navigation_keyboard('uz')  # Default to Uzbek
        
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Error displaying inbox message: {e}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
