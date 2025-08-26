"""
Junior Manager Client Search - Mock Data Implementation

This module handles junior manager client search functionality.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.junior_manager_buttons import (
    get_client_search_keyboard, 
    get_junior_manager_back_keyboard,
    get_clients_navigation_keyboard,
    get_junior_manager_main_menu
)
from typing import Dict, Any, List, Optional
from datetime import datetime
from filters.role_filter import RoleFilter
from states.junior_manager_states import JuniorManagerApplicationStates
import logging

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

# Mock clients data
MOCK_CLIENTS = [
    {
        'id': 1,
        'full_name': 'Alisher Karimov',
        'phone': '+998901234567',
        'username': 'alisher_k',
        'address': 'Toshkent shahri, Chilanzor tumani, 15-uy',
        'abonent_id': 'AB001',
        'created_at': '2024-01-15 10:30:00',
        'region': 'toshkent'
    },
    {
        'id': 2,
        'full_name': 'Dilfuza Rahimova',
        'phone': '+998901234568',
        'username': 'dilfuza_r',
        'address': 'Toshkent shahri, Sergeli tumani, 25-uy',
        'abonent_id': 'AB002',
        'created_at': '2024-01-14 14:20:00',
        'region': 'toshkent'
    },
    {
        'id': 3,
        'full_name': 'Jamshid Toshmatov',
        'phone': '+998901234569',
        'username': 'jamshid_t',
        'address': 'Toshkent shahri, Yakkasaroy tumani, 8-uy',
        'abonent_id': 'AB003',
        'created_at': '2024-01-13 09:15:00',
        'region': 'toshkent'
    },
    {
        'id': 4,
        'full_name': 'Malika Yusupova',
        'phone': '+998901234570',
        'username': 'malika_y',
        'address': 'Toshkent shahri, Shayxontohur tumani, 12-uy',
        'abonent_id': 'AB004',
        'created_at': '2024-01-12 16:45:00',
        'region': 'toshkent'
    },
    {
        'id': 5,
        'full_name': 'Rustam Azimov',
        'phone': '+998901234571',
        'username': 'rustam_a',
        'address': 'Toshkent shahri, Uchtepa tumani, 20-uy',
        'abonent_id': 'AB005',
        'created_at': '2024-01-11 11:30:00',
        'region': 'toshkent'
    },
    {
        'id': 6,
        'full_name': 'Aziza Karimova',
        'phone': '+998901234572',
        'username': 'aziza_k',
        'address': 'Toshkent shahri, Chorsu tumani, 30-uy',
        'abonent_id': 'AB006',
        'created_at': '2024-01-10 13:20:00',
        'region': 'toshkent'
    },
    {
        'id': 7,
        'full_name': 'Jahongir Toshmatov',
        'phone': '+998901234573',
        'username': 'jahongir_t',
        'address': 'Toshkent shahri, Zangiota tumani, 18-uy',
        'abonent_id': 'AB007',
        'created_at': '2024-01-09 15:10:00',
        'region': 'toshkent'
    }
]

# Mock service requests data
mock_service_requests = {
    1: [
        {'id': 'SR001', 'status': 'completed', 'created_at': '2024-01-15'},
        {'id': 'SR002', 'status': 'in_progress', 'created_at': '2024-01-16'}
    ],
    2: [
        {'id': 'SR003', 'status': 'completed', 'created_at': '2024-01-14'}
    ],
    3: [
        {'id': 'SR004', 'status': 'pending', 'created_at': '2024-01-13'},
        {'id': 'SR005', 'status': 'completed', 'created_at': '2024-01-12'}
    ],
    4: [
        {'id': 'SR006', 'status': 'in_progress', 'created_at': '2024-01-11'}
    ],
    5: [
        {'id': 'SR007', 'status': 'completed', 'created_at': '2024-01-10'}
    ],
    6: [
        {'id': 'SR008', 'status': 'pending', 'created_at': '2024-01-09'}
    ],
    7: [
        {'id': 'SR009', 'status': 'completed', 'created_at': '2024-01-08'},
        {'id': 'SR010', 'status': 'in_progress', 'created_at': '2024-01-07'}
    ]
}

# Mock functions to replace database calls
async def get_user_by_telegram_id(user_id: int):
    """Mock get user by telegram ID"""
    return mock_users.get(user_id)

async def search_clients_universal(query: str, region: str = 'toshkent'):
    """Mock universal client search"""
    try:
        query_lower = query.lower()
        results = []
        
        for client in MOCK_CLIENTS:
            # Search in various fields
            if (query_lower in str(client.get('id', '')).lower() or
                query_lower in client.get('full_name', '').lower() or
                query_lower in client.get('phone', '').lower() or
                query_lower in client.get('address', '').lower() or
                query_lower in client.get('abonent_id', '').lower() or
                query_lower in client.get('username', '').lower()):
                results.append(client)
        
        return results[:10]  # Limit results
        
    except Exception as e:
        logger.error(f"Mock: Error in universal search: {e}")
        return []

async def search_clients_by_phone(phone: str, region: str = 'toshkent'):
    """Mock search clients by phone"""
    try:
        results = []
        for client in MOCK_CLIENTS:
            if phone in client.get('phone', ''):
                results.append(client)
        return results[:5]
    except Exception as e:
        logger.error(f"Mock: Error searching by phone: {e}")
        return []

async def search_clients_by_name(name: str, region: str = 'toshkent'):
    """Mock search clients by name"""
    try:
        name_lower = name.lower()
        results = []
        for client in MOCK_CLIENTS:
            if name_lower in client.get('full_name', '').lower():
                results.append(client)
        return results[:5]
    except Exception as e:
        logger.error(f"Mock: Error searching by name: {e}")
        return []

async def get_client_by_id(client_id: int, region: str = 'toshkent'):
    """Mock get client by ID"""
    try:
        for client in MOCK_CLIENTS:
            if client.get('id') == client_id:
                return client
        return None
    except Exception as e:
        logger.error(f"Mock: Error getting client by ID: {e}")
        return None

async def create_client(client_data: Dict[str, Any], region: str = 'toshkent'):
    """Mock create client"""
    try:
        new_id = max([c.get('id', 0) for c in MOCK_CLIENTS]) + 1
        new_client = {
            'id': new_id,
            **client_data,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'region': region
        }
        MOCK_CLIENTS.append(new_client)
        return new_client
    except Exception as e:
        logger.error(f"Mock: Error creating client: {e}")
        return None

async def update_client(client_id: int, update_data: Dict[str, Any], region: str = 'toshkent'):
    """Mock update client"""
    try:
        for i, client in enumerate(MOCK_CLIENTS):
            if client.get('id') == client_id:
                MOCK_CLIENTS[i].update(update_data)
                return MOCK_CLIENTS[i]
        return None
    except Exception as e:
        logger.error(f"Mock: Error updating client: {e}")
        return None

async def get_service_requests_by_client(region: str, client_id: int):
    """Mock get service requests by client"""
    try:
        return mock_service_requests.get(client_id, [])
    except Exception as e:
        logger.error(f"Mock: Error getting service requests: {e}")
        return []

async def get_user_lang(user_id: int):
    """Mock get user language"""
    user = await get_user_by_telegram_id(user_id)
    return user.get('language', 'uz') if user else 'uz'

# Create router
router = Router(name="junior_manager_client_search")

# Apply role filter to all handlers
router.message.filter(RoleFilter(role="junior_manager"))
router.callback_query.filter(RoleFilter(role="junior_manager"))

@router.message(F.text.in_(["🔍 Mijoz qidiruv", "🔍 Поиск клиентов"]))
async def view_client_search(message: Message, state: FSMContext):
    """Junior manager view client search handler"""
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
        
        # Get language
        lang = await get_user_lang(user_id) or user.get('language', 'uz')
            
        
        # Prepare search text
        if lang == 'uz':
            search_text = (
                "🔍 <b>Mijoz qidiruv</b>\n\n"
                "📋 <b>Qidirish mumkin bo'lgan ma'lumotlar:</b>\n"
                "• Mijoz ismi va familiyasi\n"
                "• Telefon raqami\n"
                "• Manzil\n"
                "• Abonent ID\n\n"
                "Qidiruv so'zini kiriting:"
            )
        else:
            search_text = (
                "🔍 <b>Поиск клиентов</b>\n\n"
                "📋 <b>Информация для поиска:</b>\n"
                "• Имя и фамилия клиента\n"
                "• Номер телефона\n"
                "• Адрес\n"
                "• Абонент ID\n\n"
                "Введите поисковый запрос:"
            )
        
        await message.answer(
            text=search_text,
            reply_markup=get_client_search_keyboard(lang),
            parse_mode='HTML'
        )
        
        # Set state for search
        await state.clear()
        await state.set_state(JuniorManagerApplicationStates.client_search_name)
        await state.update_data(
            search_results=[], 
            search_query="", 
            current_client_index=0,
            language=lang
        )
        
        logger.info(f"Junior Manager {user_id} opened client search")
        
    except Exception as e:
        logger.error(f"Error in view_client_search: {str(e)}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

@router.message(JuniorManagerApplicationStates.client_search_name)
async def handle_search_query(message: Message, state: FSMContext):
    """Handle search query"""
    user_id = message.from_user.id
    
    try:
        # Check if it's a valid search query
        if not message.text or len(message.text) < 2:
            await message.answer("⚠️ Iltimos, kamida 2 ta belgi kiriting.")
            return
        
        # Check for back button
        if message.text in ["🏠 Asosiy menyu", "🏠 Главное меню"]:
            await state.clear()
            lang = await get_user_lang(user_id) or 'uz'
            await message.answer(
                "🏠 Asosiy menyu" if lang == 'uz' else "🏠 Главное меню",
                reply_markup=get_junior_manager_main_menu(lang)
            )
            return
        
        # Get user data
        user = await get_user_by_telegram_id(user_id)
        if not user or user.get('role') != 'junior_manager':
            return
        
        # Get state data
        state_data = await state.get_data()
        lang = state_data.get('language', 'uz')
        region = user.get('region')
        
        # Perform search in the correct region database
        search_results = await search_clients_universal(message.text)
            
        
        if not search_results:
            if lang == 'uz':
                no_results_text = (
                    f"📭 <b>'{message.text}'</b> bo'yicha natija topilmadi.\n\n"
                    f"Boshqa so'z bilan qidirib ko'ring."
                )
            else:
                no_results_text = (
                    f"📭 По запросу <b>'{message.text}'</b> ничего не найдено.\n\n"
                    f"Попробуйте поиск с другими словами."
                )
            
            await message.answer(
                text=no_results_text,
                reply_markup=get_junior_manager_back_keyboard(lang),
                parse_mode='HTML'
            )
            return
        
        # Store results in state for navigation
        await state.update_data(
            search_results=search_results,
            search_query=message.text,
            current_client_index=0,
        )
        
        # Show first result
        await show_client_details(message, search_results[0], search_results, 0, message.text, lang, region)
        
        logger.info(f"Junior Manager {user_id} searched for '{message.text}', found {len(search_results)} results")
        
    except Exception as e:
        logger.error(f"Error in handle_search_query: {str(e)}")
        await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

async def show_client_details(message_or_callback, client: Dict[str, Any], clients: List[Dict], 
                             index: int, query: str, lang: str, region: str):
    """Show client details with navigation"""
    try:
        # Format date
        created_date = ""
        if client.get('created_at'):
            if isinstance(client['created_at'], str):
                created_date = client['created_at'][:10]
            else:
                created_date = client['created_at'].strftime('%d.%m.%Y')
        
        # Get client applications count (if region is available)
        total_applications = 0
        if region:
            try:
                applications = await get_service_requests_by_client(region, client['id'])
                total_applications = len(applications)
            except:
                pass
        
        # Format client info based on language
        if lang == 'uz':
            text = (
                f"👤 <b>Mijoz ma'lumotlari</b>\n\n"
                f"🔎 <b>Qidiruv so'zi:</b> {query}\n"
                f"🆔 <b>Mijoz ID:</b> {client.get('id', 'N/A')}\n"
                f"👤 <b>To'liq ism:</b> {client.get('full_name', 'N/A')}\n"
                f"📞 <b>Telefon:</b> {client.get('phone', 'N/A')}\n"
                f"📧 <b>Username:</b> @{client.get('username', 'N/A')}\n"
                f"🏠 <b>Manzil:</b> {client.get('address', 'N/A')}\n"
                f"🆔 <b>Abonent ID:</b> {client.get('abonent_id', 'N/A')}\n"
                f"📅 <b>Ro'yxatdan o'tgan:</b> {created_date or 'N/A'}\n"
                f"📊 <b>Jami arizalar:</b> {total_applications}\n\n"
                f"📊 <b>Mijoz #{index + 1} / {len(clients)}</b>"
            )
        else:
            text = (
                f"👤 <b>Информация о клиенте</b>\n\n"
                f"🔎 <b>Поисковый запрос:</b> {query}\n"
                f"🆔 <b>ID клиента:</b> {client.get('id', 'N/A')}\n"
                f"👤 <b>Полное имя:</b> {client.get('full_name', 'N/A')}\n"
                f"📞 <b>Телефон:</b> {client.get('phone', 'N/A')}\n"
                f"📧 <b>Username:</b> @{client.get('username', 'N/A')}\n"
                f"🏠 <b>Адрес:</b> {client.get('address', 'N/A')}\n"
                f"🆔 <b>Абонент ID:</b> {client.get('abonent_id', 'N/A')}\n"
                f"📅 <b>Зарегистрирован:</b> {created_date or 'N/A'}\n"
                f"📊 <b>Всего заявок:</b> {total_applications}\n\n"
                f"📊 <b>Клиент #{index + 1} / {len(clients)}</b>"
            )
        
        # Navigation keyboard
        keyboard = get_clients_navigation_keyboard(index, len(clients), lang)
        
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
        else:
            await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
    except Exception as e:
        logger.error(f"Error in show_client_details: {str(e)}")
        if isinstance(message_or_callback, Message):
            await message_or_callback.answer("❌ Xatolik yuz berdi.")
        else:
            await message_or_callback.answer("❌ Xatolik yuz berdi", show_alert=True)

@router.callback_query(F.data == "client_prev")
async def show_previous_client(callback: CallbackQuery, state: FSMContext):
    """Show previous client"""
    try:
        await callback.answer()
        
        # Get state data
        data = await state.get_data()
        current_index = data.get('current_client_index', 0)
        search_results = data.get('search_results', [])
        query = data.get('search_query', '')
        lang = data.get('language', 'uz')
        
        # Get user region
        user = await get_user_by_telegram_id(callback.from_user.id)
        region = user.get('region') if user else None
        
        if not search_results:
            await callback.answer("Natijalar topilmadi" if lang == 'uz' else "Результаты не найдены")
            return

        if current_index > 0:
            new_index = current_index - 1
            await state.update_data(current_client_index=new_index)
            await show_client_details(callback, search_results[new_index], search_results, new_index, query, lang, region)
        else:
            await callback.answer("Bu birinchi mijoz" if lang == 'uz' else "Это первый клиент")
            
    except Exception as e:
        logger.error(f"Error in show_previous_client: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True)


@router.callback_query(F.data == "client_next")
async def show_next_client(callback: CallbackQuery, state: FSMContext):
    """Show next client"""
    try:
        await callback.answer()
        
        # Get state data
        data = await state.get_data()
        current_index = data.get('current_client_index', 0)
        search_results = data.get('search_results', [])
        query = data.get('search_query', '')
        lang = data.get('language', 'uz')
        
        # Get user region
        user = await get_user_by_telegram_id(callback.from_user.id)
        region = user.get('region') if user else None
        
        if not search_results:
            await callback.answer("Natijalar topilmadi" if lang == 'uz' else "Результаты не найдены")
            return
        
        if current_index < len(search_results) - 1:
            new_index = current_index + 1
            await state.update_data(current_client_index=new_index)
            await show_client_details(callback, search_results[new_index], search_results, new_index, query, lang, region)
        else:
            await callback.answer("Bu oxirgi mijoz" if lang == 'uz' else "Это последний клиент")
            
    except Exception as e:
        logger.error(f"Error in show_next_client: {str(e)}")
        await callback.answer("❌ Xatolik yuz berdi", show_alert=True) 