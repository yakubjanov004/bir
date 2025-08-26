"""
Call Center Clients Handler
Manages call center client interactions
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.call_center_buttons import get_clients_keyboard

# States imports
from states.call_center_states import CallCenterClientsStates, CallCenterMainMenuStates
from filters.role_filter import RoleFilter

def get_call_center_clients_router():
    """Get call center clients router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(StateFilter(CallCenterMainMenuStates.main_menu), F.text.in_(["👥 Mijozlar", "👥 Клиенты"]))
    async def clients_menu(message: Message, state: FSMContext):
        """Clients main menu"""
        text = "👥 <b>Call Center Mijozlar</b>\n\nMijozlar bilan ishlash uchun bo'limni tanlang."
        
        await message.answer(
            text,
            reply_markup=get_clients_keyboard('uz')
        )
        await state.set_state(CallCenterClientsStates.clients)

    @router.message(F.text.in_(["🔍 Mijoz qidirish", "🔍 Поиск клиента"]))
    async def search_client(message: Message, state: FSMContext):
        """Search client interface"""
        text = (
            f"🔍 <b>Mijoz qidirish</b>\n\n"
            f"Qidirish uchun quyidagi ma'lumotlardan birini kiriting:\n\n"
            f"📱 <b>Telefon raqam:</b>\n"
            f"Masalan: +998 90 123 45 67\n\n"
            f"👤 <b>Ism:</b>\n"
            f"Masalan: Bekzod Toirov\n\n"
            f"🆔 <b>Mijoz ID:</b>\n"
            f"Masalan: CL123456\n\n"
            f"📧 <b>Email:</b>\n"
            f"Masalan: client@example.com\n\n"
            f"Qidirish ma'lumotini yuboring:"
        )
        
        await message.answer(text)
        await state.set_state(CallCenterClientsStates.waiting_for_search_query)

    @router.message(CallCenterClientsStates.waiting_for_search_query)
    async def process_search_query(message: Message, state: FSMContext):
        """Process search query"""
        search_query = message.text.strip()
        
        if not search_query:
            await message.answer("Iltimos, qidirish ma'lumotini kiriting.")
            return
            
        # Mock search results
        search_results = [
            {
                'id': 'CL123456',
                'name': 'Bekzod Toirov',
                'phone': '+998 90 123 45 67',
                'email': 'bekzod@example.com',
                'address': 'Toshkent shahri, Chilonzor-5, 23-uy',
                'status': 'active',
                'created_at': '2024-01-15',
                'last_contact': '2024-08-05 14:30',
                'orders_count': 5,
                'total_spent': '450,000 so\'m'
            },
            {
                'id': 'CL789012',
                'name': 'Aziz Karimov',
                'phone': '+998 91 234 56 78',
                'email': 'aziz@example.com',
                'address': 'Samarqand shahri, Registon ko\'chasi, 45-uy',
                'status': 'active',
                'created_at': '2024-02-20',
                'last_contact': '2024-08-05 13:45',
                'orders_count': 3,
                'total_spent': '280,000 so\'m'
            }
        ]
        
        if not search_results:
            text = f"❌ '{search_query}' bo'yicha mijoz topilmadi."
            await message.answer(text)
            await state.clear()
            return
            
        text = f"🔍 <b>Qidirish natijalari</b>\n\n"
        text += f"'{search_query}' bo'yicha {len(search_results)} ta mijoz topildi:\n\n"
        
        for i, client in enumerate(search_results, 1):
            text += f"{i}. <b>{client['name']}</b>\n"
            text += f"   📱 {client['phone']}\n"
            text += f"   📧 {client['email']}\n"
            text += f"   📍 {client['address']}\n"
            text += f"   📊 Status: {client['status']}\n"
            text += f"   📅 Ro'yxatdan o'tgan: {client['created_at']}\n"
            text += f"   💰 Buyurtmalar: {client['orders_count']} ta\n"
            text += f"   💵 Jami xarid: {client['total_spent']}\n\n"
        
        await message.answer(text)
        await state.clear()

    @router.message(F.text.in_(["📋 Mijozlar ro'yxati", "📋 Список клиентов"]))
    async def clients_list(message: Message):
        """Show clients list"""
        # Mock clients list
        clients = [
            {
                'id': 'CL123456',
                'name': 'Bekzod Toirov',
                'phone': '+998 90 123 45 67',
                'status': 'active',
                'orders_count': 5
            },
            {
                'id': 'CL789012',
                'name': 'Aziz Karimov',
                'phone': '+998 91 234 56 78',
                'status': 'active',
                'orders_count': 3
            },
            {
                'id': 'CL345678',
                'name': 'Malika Yusupova',
                'phone': '+998 92 345 67 89',
                'status': 'inactive',
                'orders_count': 1
            }
        ]
        
        text = f"📋 <b>Mijozlar ro'yxati ({len(clients)})</b>\n\n"
        
        for i, client in enumerate(clients, 1):
            status_emoji = "✅" if client['status'] == 'active' else "❌"
            text += f"{i}. {status_emoji} <b>{client['name']}</b>\n"
            text += f"   📱 {client['phone']}\n"
            text += f"   🆔 {client['id']}\n"
            text += f"   📦 Buyurtmalar: {client['orders_count']} ta\n\n"
        
        await message.answer(text)

    @router.message(F.text.in_(["➕ Yangi mijoz qo'shish", "➕ Добавить клиента"]))
    async def add_client(message: Message, state: FSMContext):
        """Add new client"""
        text = (
            "➕ <b>Yangi mijoz qo'shish</b>\n\n"
            "Mijoz ma'lumotlarini quyidagi formatda kiriting:\n\n"
            "👤 <b>Ism:</b> Mijoz ismi\n"
            "📱 <b>Telefon:</b> +998 XX XXX XX XX\n"
            "📧 <b>Email:</b> email@example.com\n"
            "📍 <b>Manzil:</b> To'liq manzil\n\n"
            "Ma'lumotlarni kiriting:"
        )
        
        await message.answer(text)
        await state.set_state(CallCenterClientsStates.waiting_for_client_data)

    @router.message(CallCenterClientsStates.waiting_for_client_data)
    async def process_client_data(message: Message, state: FSMContext):
        """Process client data"""
        client_data = message.text.strip()
        
        if not client_data:
            await message.answer("Iltimos, mijoz ma'lumotlarini kiriting.")
            return
        
        # Mock client creation
        success_text = (
            "✅ Yangi mijoz muvaffaqiyatli qo'shildi!\n\n"
            "👤 <b>Mijoz ID:</b> CL123456\n"
            "📅 <b>Qo'shilgan sana:</b> 2024-01-15\n"
            "📊 <b>Status:</b> Faol"
        )
        
        await message.answer(success_text)
        await state.clear()

    @router.message(F.text.in_(["👤 Mijoz profili", "👤 Профиль клиента"]))
    async def client_profile(message: Message):
        """Show client profile"""
        text = (
            "👤 <b>Mijoz profili</b>\n\n"
            "Mijoz ID yoki telefon raqamini kiriting:"
        )
        
        await message.answer(text)
        await state.set_state(CallCenterClientsStates.waiting_for_client_id)

    @router.message(CallCenterClientsStates.waiting_for_client_id)
    async def process_client_id(message: Message, state: FSMContext):
        """Process client ID"""
        client_id = message.text.strip()
        
        if not client_id:
            await message.answer("Iltimos, mijoz ID yoki telefon raqamini kiriting.")
            return
        
        # Mock client profile
        client_profile = {
            'id': 'CL123456',
            'name': 'Bekzod Toirov',
            'phone': '+998 90 123 45 67',
            'email': 'bekzod@example.com',
            'address': 'Toshkent shahri, Chilonzor-5, 23-uy',
            'status': 'active',
            'created_at': '2024-01-15',
            'last_contact': '2024-08-05 14:30',
            'orders_count': 5,
            'total_spent': '450,000 so\'m',
            'notes': 'Doimiy mijoz, yuqori sifatli xizmat talab qiladi'
        }
        
        text = (
            f"👤 <b>Mijoz profili</b>\n\n"
            f"🆔 <b>ID:</b> {client_profile['id']}\n"
            f"👤 <b>Ism:</b> {client_profile['name']}\n"
            f"📱 <b>Telefon:</b> {client_profile['phone']}\n"
            f"📧 <b>Email:</b> {client_profile['email']}\n"
            f"📍 <b>Manzil:</b> {client_profile['address']}\n"
            f"📊 <b>Status:</b> {client_profile['status']}\n"
            f"📅 <b>Ro'yxatdan o'tgan:</b> {client_profile['created_at']}\n"
            f"⏰ <b>Oxirgi aloqa:</b> {client_profile['last_contact']}\n"
            f"📦 <b>Buyurtmalar:</b> {client_profile['orders_count']} ta\n"
            f"💵 <b>Jami xarid:</b> {client_profile['total_spent']}\n\n"
            f"📝 <b>Izohlar:</b>\n{client_profile['notes']}"
        )
        
        await message.answer(text)
        await state.clear()

    return router
