"""
Call Center Chat Handler
Manages call center chat functionality
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.call_center_buttons import get_chat_keyboard

# States imports
from states.call_center_states import CallCenterChatStates, CallCenterMainMenuStates
from filters.role_filter import RoleFilter

def get_call_center_chat_router():
    """Get call center chat router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(StateFilter(CallCenterMainMenuStates.main_menu), F.text.in_(["💬 Chat", "💬 Чат"]))
    async def chat_menu(message: Message, state: FSMContext):
        """Chat main menu"""
        text = "💬 <b>Call Center Chat</b>\n\nMijozlar bilan suhbatlashish uchun chat bo'limini tanlang."
        
        await message.answer(
            text,
            reply_markup=get_chat_keyboard('uz')
        )
        await state.set_state(CallCenterChatStates.chat)

    @router.message(F.text.in_(["📱 Faol chatlar", "📱 Активные чаты"]))
    async def active_chats(message: Message):
        """Show active chats"""
        # Mock active chats
        active_chats = [
            {
                'id': 'chat_001',
                'client_name': 'Bekzod Toirov',
                'client_phone': '+998 90 123 45 67',
                'status': 'active',
                'last_message': 'Internet uzulib qolgan',
                'last_message_time': '14:30',
                'unread_count': 2,
                'chat_duration': '15 daqiqa'
            },
            {
                'id': 'chat_002',
                'client_name': 'Aziz Karimov',
                'client_phone': '+998 91 234 56 78',
                'status': 'waiting',
                'last_message': 'TV signal yo\'q',
                'last_message_time': '14:25',
                'unread_count': 1,
                'chat_duration': '8 daqiqa'
            },
            {
                'id': 'chat_003',
                'client_name': 'Dilshod Rahimov',
                'client_phone': '+998 92 345 67 89',
                'status': 'active',
                'last_message': 'Telefon xizmati yo\'q',
                'last_message_time': '14:20',
                'unread_count': 0,
                'chat_duration': '25 daqiqa'
            }
        ]
        
        text = (
            f"📱 <b>Faol chatlar</b>\n\n"
            f"📊 <b>Umumiy:</b> {len(active_chats)} ta faol chat\n\n"
        )
        
        for i, chat in enumerate(active_chats, 1):
            status_emoji = "🟢" if chat['status'] == 'active' else "🟡"
            unread_badge = f" ({chat['unread_count']})" if chat['unread_count'] > 0 else ""
            
            text += (
                f"{i}. {status_emoji} <b>{chat['client_name']}</b>\n"
                f"   📱 {chat['client_phone']}\n"
                f"   💬 {chat['last_message']}\n"
                f"   ⏰ {chat['last_message_time']} • {chat['chat_duration']}\n\n"
            )
        
        await message.answer(text)

    @router.message(F.text.in_(["⏳ Kutilayotgan chatlar", "⏳ Ожидающие чаты"]))
    async def waiting_chats(message: Message):
        """Show waiting chats"""
        # Mock waiting chats
        waiting_chats = [
            {
                'id': 'wait_001',
                'client_name': 'Malika Yusupova',
                'client_phone': '+998 93 456 78 90',
                'waiting_time': '5 daqiqa',
                'issue': 'Internet sekin ishlayapti'
            },
            {
                'id': 'wait_002',
                'client_name': 'Jasur Toshmatov',
                'client_phone': '+998 94 567 89 01',
                'waiting_time': '12 daqiqa',
                'issue': 'TV kanallar ishlamayapti'
            }
        ]
        
        text = (
            f"⏳ <b>Kutilayotgan chatlar</b>\n\n"
            f"📊 <b>Umumiy:</b> {len(waiting_chats)} ta kutilayotgan chat\n\n"
        )
        
        for i, chat in enumerate(waiting_chats, 1):
            text += (
                f"{i}. <b>{chat['client_name']}</b>\n"
                f"   📱 {chat['client_phone']}\n"
                f"   ⏰ Kutilmoqda: {chat['waiting_time']}\n"
                f"   💬 Muammo: {chat['issue']}\n\n"
            )
        
        await message.answer(text)

    @router.message(F.text.in_(["📋 Chat tarixi", "📋 История чатов"]))
    async def chat_history(message: Message):
        """Show chat history"""
        # Mock chat history
        chat_history = [
            {
                'id': 'hist_001',
                'client_name': 'Bekzod Toirov',
                'client_phone': '+998 90 123 45 67',
                'status': 'completed',
                'duration': '25 daqiqa',
                'ended_at': '2024-01-15 15:30',
                'satisfaction': 5
            },
            {
                'id': 'hist_002',
                'client_name': 'Aziz Karimov',
                'client_phone': '+998 91 234 56 78',
                'status': 'completed',
                'duration': '18 daqiqa',
                'ended_at': '2024-01-15 14:45',
                'satisfaction': 4
            }
        ]
        
        text = (
            f"📋 <b>Chat tarixi</b>\n\n"
            f"📊 <b>Umumiy:</b> {len(chat_history)} ta chat\n\n"
        )
        
        for i, chat in enumerate(chat_history, 1):
            satisfaction_stars = "⭐" * chat['satisfaction']
            text += (
                f"{i}. <b>{chat['client_name']}</b>\n"
                f"   📱 {chat['client_phone']}\n"
                f"   ⏰ Davomiyligi: {chat['duration']}\n"
                f"   📅 Tugagan: {chat['ended_at']}\n"
                f"   {satisfaction_stars}\n\n"
            )
        
        await message.answer(text)

    @router.message(F.text.in_(["⚙️ Chat sozlamalari", "⚙️ Настройки чата"]))
    async def chat_settings(message: Message):
        """Show chat settings"""
        text = (
            "⚙️ <b>Chat sozlamalari</b>\n\n"
            "🔔 <b>Bildirishnomalar:</b> Yoqilgan\n"
            "⏰ <b>Avtomatik javob:</b> Yoqilgan\n"
            "📱 <b>Mobil rejim:</b> Yoqilgan\n"
            "🌐 <b>Til:</b> O'zbekcha\n"
            "📊 <b>Statistika:</b> Ko'rsatiladi\n\n"
            "Sozlamalarni o'zgartirish uchun admin bilan bog'laning."
        )
        
        await message.answer(text)

    @router.callback_query(F.data.startswith("open_chat_"))
    async def open_chat(call: CallbackQuery, state: FSMContext):
        """Open specific chat"""
        await call.answer()
        
        chat_id = call.data.replace("open_chat_", "")
        
        # Mock chat details
        chat_details = {
            'id': chat_id,
            'client_name': 'Bekzod Toirov',
            'client_phone': '+998 90 123 45 67',
            'status': 'active',
            'messages': [
                {
                    'sender': 'client',
                    'message': 'Salom, internet muammosi bor',
                    'time': '14:30'
                },
                {
                    'sender': 'operator',
                    'message': 'Salom! Qanday yordam bera olaman?',
                    'time': '14:31'
                },
                {
                    'sender': 'client',
                    'message': 'Internet juda sekin ishlayapti',
                    'time': '14:32'
                }
            ]
        }
        
        text = (
            f"💬 <b>Chat #{chat_id}</b>\n\n"
            f"👤 <b>Mijoz:</b> {chat_details['client_name']}\n"
            f"📱 <b>Telefon:</b> {chat_details['client_phone']}\n"
            f"📊 <b>Status:</b> {chat_details['status']}\n\n"
            f"📝 <b>Xabarlar:</b>\n"
        )
        
        for msg in chat_details['messages']:
            sender_emoji = "👤" if msg['sender'] == 'client' else "👨‍💼"
            text += f"{sender_emoji} <b>{msg['sender'].title()}</b> ({msg['time']}): {msg['message']}\n"
        
        await call.message.edit_text(text)

    @router.callback_query(F.data.startswith("accept_chat_"))
    async def accept_chat(call: CallbackQuery, state: FSMContext):
        """Accept waiting chat"""
        await call.answer()
        
        chat_id = call.data.replace("accept_chat_", "")
        
        success_text = (
            f"✅ Chat #{chat_id} qabul qilindi!\n\n"
            f"Chat ochildi va mijoz bilan suhbatlashishni boshlashingiz mumkin."
        )
        
        await call.message.edit_text(success_text)

    @router.callback_query(F.data.startswith("reply_chat_"))
    async def reply_chat(call: CallbackQuery, state: FSMContext):
        """Reply to chat"""
        await call.answer()
        
        chat_id = call.data.replace("reply_chat_", "")
        
        text = (
            f"💬 <b>Chat #{chat_id} ga javob</b>\n\n"
            f"Javobingizni yozing:"
        )
        
        await call.message.edit_text(text)
        await state.update_data(replying_to_chat=chat_id)
        await state.set_state(CallCenterChatStates.waiting_for_reply)

    @router.message(CallCenterChatStates.waiting_for_reply)
    async def process_reply(message: Message, state: FSMContext):
        """Process chat reply"""
        reply_text = message.text.strip()
        
        if not reply_text:
            await message.answer("Iltimos, javob matnini kiriting.")
            return
        
        data = await state.get_data()
        chat_id = data.get('replying_to_chat')
        
        success_text = (
            f"✅ Javob yuborildi!\n\n"
            f"Chat #{chat_id} ga javob muvaffaqiyatli yuborildi."
        )
        
        await message.answer(success_text)
        await state.clear()

    @router.callback_query(F.data.startswith("end_chat_"))
    async def end_chat(call: CallbackQuery):
        """End chat"""
        await call.answer()
        
        chat_id = call.data.replace("end_chat_", "")
        
        success_text = (
            f"✅ Chat #{chat_id} tugatildi!\n\n"
            f"Chat muvaffaqiyatli yakunlandi."
        )
        
        await call.message.edit_text(success_text)

    return router
