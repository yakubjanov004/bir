"""
Manager Applications Search Handler - Mock Data Implementation

This module handles manager applications search functionality.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_manager_search_keyboard, get_manager_back_keyboard
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
        'contact_info': {
            'full_name': 'Aziz Karimov',
            'phone': '+998901234567'
        },
        'created_at': datetime.now(),
        'description': 'Internet ulanish arizasi - yangi uy uchun internet xizmatini ulashish kerak',
        'location': 'Tashkent, Chorsu tumani, 15-uy',
        'priority': 'high',
        'region': 'Toshkent shahri',
        'client_id': 123456789
    },
    {
        'id': 'req_002_2024_01_16',
        'workflow_type': 'technical_service',
        'current_status': 'created',
        'contact_info': {
            'full_name': 'Malika Toshmatova',
            'phone': '+998901234568'
        },
        'created_at': datetime.now(),
        'description': 'TV signal muammosi - TV kanallar ko\'rinmayapti, signal zaif',
        'location': 'Tashkent, Yunusabad tumani, 25-uy',
        'priority': 'normal',
        'region': 'Toshkent shahri',
        'client_id': 123456790
    },
    {
        'id': 'req_003_2024_01_17',
        'workflow_type': 'call_center_direct',
        'current_status': 'completed',
        'contact_info': {
            'full_name': 'Jahongir Azimov',
            'phone': '+998901234569'
        },
        'created_at': datetime.now(),
        'description': 'Qo\'ng\'iroq markazi arizasi - mijoz xizmat sifatini yaxshilash haqida',
        'location': 'Tashkent, Sergeli tumani, 8-uy',
        'priority': 'low',
        'region': 'Toshkent shahri',
        'client_id': 123456791
    },
    {
        'id': 'req_004_2024_01_18',
        'workflow_type': 'connection_request',
        'current_status': 'created',
        'contact_info': {
            'full_name': 'Umar Toshmatov',
            'phone': '+998901234570'
        },
        'created_at': datetime.now(),
        'description': 'Yangi internet paketini qo\'shish - 100 Mbit/s tezlikda',
        'location': 'Tashkent, Chilanzor tumani, 30-uy',
        'priority': 'urgent',
        'region': 'Toshkent shahri',
        'client_id': 123456792
    },
    {
        'id': 'req_005_2024_01_19',
        'workflow_type': 'technical_service',
        'current_status': 'in_progress',
        'contact_info': {
            'full_name': 'Dilfuza Karimova',
            'phone': '+998901234571'
        },
        'created_at': datetime.now(),
        'description': 'Router muammosi - internet tezligi past, qayta ishga tushirish kerak',
        'location': 'Tashkent, Mirabad tumani, 42-uy',
        'priority': 'high',
        'region': 'Toshkent shahri',
        'client_id': 123456793
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
async def find_user_by_telegram_id(telegram_id: int):
    """Mock find user by telegram ID"""
    for user in mock_users.values():
        if user.get('telegram_id') == telegram_id:
            return user
    return None

async def get_user_by_telegram_id(telegram_id: int):
    """Mock get user data"""
    return await find_user_by_telegram_id(telegram_id)

async def get_user_lang(telegram_id: int):
    """Mock get user language"""
    user = await find_user_by_telegram_id(telegram_id)
    return user.get('language', 'uz') if user else 'uz'

async def search_applications(query: str, region: str = 'toshkent'):
    """Mock search applications"""
    try:
        query_lower = query.lower()
        results = []
        
        for app in mock_applications:
            # Search in various fields
            if (query_lower in app['id'].lower() or
                query_lower in app['contact_info']['full_name'].lower() or
                query_lower in app['contact_info']['phone'].lower() or
                query_lower in app['description'].lower() or
                query_lower in app['location'].lower() or
                query_lower in app.get('region', '').lower()):
                results.append(app)
        
        return results
        
    except Exception as e:
        logger.error(f"Mock: Error searching applications: {e}")
        return []

def get_manager_applications_search_router():
    """Router for applications search with mock data"""
    router = Router()
    
    # Apply role filter - both manager and junior_manager can access
    role_filter = RoleFilter(["manager", "junior_manager"])
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.message(F.text.in_(["🔎 Qidirish"]), flags={"block": False})
    async def show_search_menu(message: Message, state: FSMContext):
        """Show search menu using mock data"""
        try:
            # Get user
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("❌ Foydalanuvchi topilmadi")
                return
            
            # Get region from state or default
            state_data = await state.get_data()
            region = state_data.get('region', 'toshkent')
            
            # Update state
            await state.update_data(search_region=region)
            
            # Show search keyboard
            keyboard = get_manager_search_keyboard(lang=user.get('language', 'uz'))
            text = (
                f"🔎 <b>Arizalar qidirish</b>\n\n"
                f"📍 Hudud: {region.title()}\n\n"
                f"Qidirish turini tanlang:"
            )
            
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in show_search_menu: {e}")
            await message.answer("Xatolik yuz berdi")
    
    @router.callback_query(F.data.startswith("search_"))
    async def handle_search_action(callback: CallbackQuery, state: FSMContext):
        """Handle search actions using mock data"""
        try:
            await callback.answer()
            
            # Extract search type
            search_type = callback.data.replace("search_", "")
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            if search_type == "by_id":
                # Search by ID
                await state.set_state("waiting_for_search_id")
                text = "🔍 Ariza ID raqamini kiriting:"
                
            elif search_type == "by_phone":
                # Search by phone
                await state.set_state("waiting_for_search_phone")
                text = "📞 Mijoz telefon raqamini kiriting:"
                
            elif search_type == "by_name":
                # Search by name
                await state.set_state("waiting_for_search_name")
                text = "👤 Mijoz ismini kiriting:"
                
            elif search_type == "by_location":
                # Search by location
                await state.set_state("waiting_for_search_location")
                text = "📍 Manzilni kiriting:"
                
            else:
                await callback.answer("Noma'lum qidirish turi", show_alert=True)
                return
            
            # Create back button
            keyboard = get_manager_back_keyboard(lang=user.get('language', 'uz'))
            
            await callback.message.edit_text(text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error in handle_search_action: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.message(F.state == "waiting_for_search_id")
    async def search_by_id(message: Message, state: FSMContext):
        """Search applications by ID using mock data"""
        try:
            search_query = message.text.strip()
            
            if not search_query:
                await message.answer("Iltimos, ariza ID raqamini kiriting.")
                return
            
            # Get user and region
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("❌ Foydalanuvchi topilmadi")
                return
            
            state_data = await state.get_data()
            region = state_data.get('search_region', 'toshkent')
            
            # Search in mock data
            results = await search_applications(search_query, region)
            
            if not results:
                text = f"🔍 <b>Qidirish natijasi</b>\n\nID: {search_query}\n\n❌ Arizalar topilmadi"
                keyboard = get_manager_back_keyboard(lang=user.get('language', 'uz'))
                await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
                await state.clear()
                return
            
            # Display results
            await display_search_results(message, state, results, user, f"ID: {search_query}")
            
        except Exception as e:
            logger.error(f"Error in search_by_id: {e}")
            await message.answer("Xatolik yuz berdi")
    
    @router.message(F.state == "waiting_for_search_phone")
    async def search_by_phone(message: Message, state: FSMContext):
        """Search applications by phone using mock data"""
        try:
            search_query = message.text.strip()
            
            if not search_query:
                await message.answer("Iltimos, telefon raqamini kiriting.")
                return
            
            # Get user and region
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("❌ Foydalanuvchi topilmadi")
                return
            
            state_data = await state.get_data()
            region = state_data.get('search_region', 'toshkent')
            
            # Search in mock data
            results = await search_applications(search_query, region)
            
            if not results:
                text = f"🔍 <b>Qidirish natijasi</b>\n\n📞 Telefon: {search_query}\n\n❌ Arizalar topilmadi"
                keyboard = get_manager_back_keyboard(lang=user.get('language', 'uz'))
                await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
                await state.clear()
                return
            
            # Display results
            await display_search_results(message, state, results, user, f"Telefon: {search_query}")
            
        except Exception as e:
            logger.error(f"Error in search_by_phone: {e}")
            await message.answer("Xatolik yuz berdi")
    
    @router.message(F.state == "waiting_for_search_name")
    async def search_by_name(message: Message, state: FSMContext):
        """Search applications by name using mock data"""
        try:
            search_query = message.text.strip()
            
            if not search_query:
                await message.answer("Iltimos, mijoz ismini kiriting.")
                return
            
            # Get user and region
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("❌ Foydalanuvchi topilmadi")
                return
            
            state_data = await state.get_data()
            region = state_data.get('search_region', 'toshkent')
            
            # Search in mock data
            results = await search_applications(search_query, region)
            
            if not results:
                text = f"🔍 <b>Qidirish natijasi</b>\n\n👤 Ism: {search_query}\n\n❌ Arizalar topilmadi"
                keyboard = get_manager_back_keyboard(lang=user.get('language', 'uz'))
                await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
                await state.clear()
                return
            
            # Display results
            await display_search_results(message, state, results, user, f"Ism: {search_query}")
            
        except Exception as e:
            logger.error(f"Error in search_by_name: {e}")
            await message.answer("Xatolik yuz berdi")
    
    @router.message(F.state == "waiting_for_search_location")
    async def search_by_location(message: Message, state: FSMContext):
        """Search applications by location using mock data"""
        try:
            search_query = message.text.strip()
            
            if not search_query:
                await message.answer("Iltimos, manzilni kiriting.")
                return
            
            # Get user and region
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user:
                await message.answer("❌ Foydalanuvchi topilmadi")
                return
            
            state_data = await state.get_data()
            region = state_data.get('search_region', 'toshkent')
            
            # Search in mock data
            results = await search_applications(search_query, region)
            
            if not results:
                text = f"🔍 <b>Qidirish natijasi</b>\n\n📍 Manzil: {search_query}\n\n❌ Arizalar topilmadi"
                keyboard = get_manager_back_keyboard(lang=user.get('language', 'uz'))
                await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
                await state.clear()
                return
            
            # Display results
            await display_search_results(message, state, results, user, f"Manzil: {search_query}")
            
        except Exception as e:
            logger.error(f"Error in search_by_location: {e}")
            await message.answer("Xatolik yuz berdi")
    
    async def display_search_results(message: Message, state: FSMContext, results: List[Dict], user: Dict, search_info: str):
        """Display search results using mock data"""
        try:
            # Update state with results
            await state.update_data(
                search_results=results,
                current_result_index=0,
                search_info=search_info
            )
            
            # Display first result
            await display_single_result(message, state, results, 0, user, search_info)
            
        except Exception as e:
            logger.error(f"Error in display_search_results: {e}")
            await message.answer("Xatolik yuz berdi")
    
    async def display_single_result(message: Message, state: FSMContext, results: List[Dict], index: int, user: Dict, search_info: str):
        """Display single search result using mock data"""
        try:
            result = results[index]
            
            # Get client info
            client_name = 'Unknown'
            client_phone = 'N/A'
            if result.get('contact_info'):
                client_name = result['contact_info'].get('full_name', 'Unknown')
                client_phone = result['contact_info'].get('phone', 'N/A')
            
            # Format workflow type
            workflow_type_names = {
                'connection_request': '🔌 Ulanish arizasi',
                'technical_service': '🔧 Texnik xizmat',
                'call_center_direct': '📞 Qo\'ng\'iroq markazi'
            }
            
            workflow_type = workflow_type_names.get(result.get('workflow_type'), f"📋 {result.get('workflow_type', 'Ariza')}")
            
            # Format status
            status_names = {
                'created': '🆕 Yaratilgan',
                'in_progress': '⏳ Jarayonda',
                'completed': '✅ Tugallangan',
                'cancelled': '❌ Bekor qilingan'
            }
            
            status = status_names.get(result.get('current_status'), f"📋 {result.get('current_status', 'Noma\'lum')}")
            
            # Format priority
            priority_emoji = {
                'low': '🔵',
                'normal': '🟢',
                'high': '🔴',
                'urgent': '🚨'
            }.get(result.get('priority'), '🟢')
            
            # Format date
            created_date = result.get('created_at')
            if hasattr(created_date, 'strftime'):
                created_date = created_date.strftime('%d.%m.%Y %H:%M')
            else:
                created_date = str(created_date)
            
            # Create text
            text = (
                f"🔍 <b>Qidirish natijasi</b>\n\n"
                f"{search_info}\n"
                f"📊 Natijalar: {index + 1}/{len(results)}\n\n"
                f"📋 <b>Ariza ma'lumotlari:</b>\n"
                f"🆔 <b>ID:</b> {result.get('id', 'N/A')}\n"
                f"{workflow_type}\n"
                f"{status}\n"
                f"{priority_emoji} <b>Muhimlik:</b> {result.get('priority', 'normal').title()}\n\n"
                f"👤 <b>Mijoz:</b> {client_name}\n"
                f"📞 <b>Telefon:</b> {client_phone}\n"
                f"📍 <b>Manzil:</b> {result.get('location', 'N/A')}\n"
                f"📅 <b>Yaratilgan:</b> {created_date}\n"
                f"📝 <b>Tavsif:</b> {result.get('description', 'Tavsif yo\'q')[:100]}{'...' if result.get('description') and len(result.get('description', '')) > 100 else ''}"
            )
            
            # Create navigation keyboard
            keyboard = create_search_navigation_keyboard(
                has_prev=index > 0,
                has_next=index < len(results) - 1,
                lang=user.get('language', 'uz')
            )
            
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in display_single_result: {e}")
            await message.answer("Xatolik yuz berdi")
    
    def create_search_navigation_keyboard(has_prev: bool, has_next: bool, lang: str = 'uz'):
        """Create navigation keyboard for search results"""
        keyboard = []
        
        # Navigation row
        nav_buttons = []
        
        if has_prev:
            nav_buttons.append(InlineKeyboardButton(
                text="⬅️ Oldingi",
                callback_data="search_prev"
            ))
        
        if has_next:
            nav_buttons.append(InlineKeyboardButton(
                text="Keyingi ➡️",
                callback_data="search_next"
            ))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        # Back buttons
        keyboard.append([InlineKeyboardButton(
            text="🔍 Yangi qidirish",
            callback_data="search_new"
        )])
        
        keyboard.append([InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="search_back"
        )])
        
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    @router.callback_query(F.data.startswith("search_"))
    async def handle_search_navigation(callback: CallbackQuery, state: FSMContext):
        """Handle search navigation using mock data"""
        try:
            await callback.answer()
            
            # Extract action
            action = callback.data.replace("search_", "")
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                await callback.answer("Foydalanuvchi topilmadi", show_alert=True)
                return
            
            # Get search results from state
            state_data = await state.get_data()
            results = state_data.get('search_results', [])
            current_index = state_data.get('current_result_index', 0)
            search_info = state_data.get('search_info', 'Qidirish')
            
            if action == "prev":
                # Go to previous result
                if current_index > 0:
                    new_index = current_index - 1
                    await state.update_data(current_result_index=new_index)
                    await display_single_result(callback.message, state, results, new_index, user, search_info)
                else:
                    await callback.answer("Birinchi natija", show_alert=True)
                    
            elif action == "next":
                # Go to next result
                if current_index < len(results) - 1:
                    new_index = current_index + 1
                    await state.update_data(current_result_index=new_index)
                    await display_single_result(callback.message, state, results, new_index, user, search_info)
                else:
                    await callback.answer("Oxirgi natija", show_alert=True)
                    
            elif action == "new":
                # Start new search
                await state.clear()
                await show_search_menu(callback.message, state)
                
            elif action == "back":
                # Go back to search menu
                await state.clear()
                await show_search_menu(callback.message, state)
                
            else:
                await callback.answer("Noma'lum amal", show_alert=True)
                
        except Exception as e:
            logger.error(f"Error in handle_search_navigation: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "back_to_search")
    async def back_to_search(callback: CallbackQuery, state: FSMContext):
        """Go back to search menu"""
        try:
            await callback.answer()
            
            # Get user
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user:
                return
            
            # Clear search state
            await state.clear()
            
            # Show search menu
            await show_search_menu(callback.message, state)
            
        except Exception as e:
            logger.error(f"Error in back_to_search: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    # Additional mock handlers for backward compatibility
    @router.message(F.text.in_(["🔍 Qidiruv", "🔍 Поиск"]), flags={"block": False})
    async def view_search(message: Message, state: FSMContext):
        """Manager view search handler"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] not in ['manager', 'junior_manager']:
                return
            
            lang = user.get('language', 'uz')
            
            search_text = (
                "🔍 <b>Qidiruv - To'liq ma'lumot</b>\n\n"
                "📋 <b>Qidirish mumkin bo'lgan ma'lumotlar:</b>\n"
                "• Ariza ID raqami\n"
                "• Mijoz ismi va familiyasi\n"
                "• Telefon raqami\n"
                "• Ariza tavsifi\n"
                "• Manzil va hudud\n\n"
                "Qidiruv so'zini kiriting:"
                if lang == 'uz' else
                "🔍 <b>Поиск - Полная информация</b>\n\n"
                "📋 <b>Информация для поиска:</b>\n"
                "• Номер заявки ID\n"
                "• Имя и фамилия клиента\n"
                "• Номер телефона\n"
                "• Описание заявки\n"
                "• Адрес и регион\n\n"
                "Введите поисковый запрос:"
            )
            
            sent_message = await message.answer(
                text=search_text,
                reply_markup=get_manager_search_keyboard(lang),
                parse_mode='HTML'
            )
            
            await state.set_state("waiting_for_search_query")
            
        except Exception as e:
            logger.error(f"Error in view_search: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.message(lambda message: message.text and len(message.text) > 2)
    async def handle_search_query(message: Message, state: FSMContext):
        """Handle search query"""
        try:
            current_state = await state.get_state()
            if current_state != "waiting_for_search_query":
                return
            
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] not in ['manager', 'junior_manager']:
                return
            
            # Perform search
            search_results = await search_applications(message.text)
            
            if not search_results:
                no_results_text = (
                    f"📭 '{message.text}' bo'yicha natija topilmadi.\n\n"
                    f"Boshqa so'z bilan qidirib ko'ring."
                    if user.get('language', 'uz') == 'uz' else
                    f"📭 По запросу '{message.text}' ничего не найдено.\n\n"
                    f"Попробуйте поиск с другими словами."
                )
                
                await message.answer(
                    text=no_results_text,
                    reply_markup=get_manager_back_keyboard(user.get('language', 'uz'))
                )
                return
            
            # Show first result
            await show_search_result(message, search_results[0], search_results, 0, message.text)
            
        except Exception as e:
            logger.error(f"Error in handle_search_query: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def show_search_result(message_or_callback, application, applications, index, query):
        """Show search result details"""
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
            
            # Format status
            status_emoji = {
                'in_progress': '🟡',
                'created': '🟠',
                'completed': '🟢',
                'cancelled': '🔴'
            }.get(application['current_status'], '⚪')
            
            status_text = {
                'in_progress': 'Jarayonda',
                'created': 'Yaratilgan',
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
            
            # Format date
            created_date = application['created_at'].strftime('%d.%m.%Y %H:%M')
            
            # To'liq ma'lumot
            text = (
                f"🔍 <b>Qidiruv natijasi - To'liq ma'lumot</b>\n\n"
                f"🔎 <b>Qidiruv so'zi:</b> {query}\n"
                f"{workflow_type_emoji} <b>{workflow_type_text}</b>\n\n"
                f"🆔 <b>Ariza ID:</b> {application['id']}\n"
                f"📅 <b>Sana:</b> {created_date}\n"
                f"👤 <b>Mijoz:</b> {application['contact_info']['full_name']}\n"
                f"📞 <b>Telefon:</b> {application['contact_info']['phone']}\n"
                f"🏛️ <b>Hudud:</b> {application.get('region', 'Noma\'lum')}\n"
                f"🏠 <b>Manzil:</b> {application.get('location', 'Noma\'lum')}\n"
                f"📝 <b>Tavsif:</b> {application['description']}\n"
                f"{status_emoji} <b>Holat:</b> {status_text}\n"
                f"{priority_emoji} <b>Ustuvorlik:</b> {priority_text}\n\n"
                f"📊 <b>Natija #{index + 1} / {len(applications)}</b>"
            )
            
            # Create navigation keyboard
            keyboard = get_search_results_navigation_keyboard(index, len(applications))
            
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer(text, reply_markup=keyboard, parse_mode='HTML')
            else:
                await message_or_callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
        except Exception as e:
            logger.error(f"Error in show_search_result: {e}")
            if isinstance(message_or_callback, Message):
                await message_or_callback.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "prev_search_result")
    async def show_previous_search_result(callback: CallbackQuery, state: FSMContext):
        """Show previous search result"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_search_index', 0)
            
            # Get search results from state
            search_data = await state.get_data()
            search_results = search_data.get('search_results', [])
            query = search_data.get('search_query', '')
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_search_index=new_index)
                await show_search_result(callback, search_results[new_index], search_results, new_index, query)
            else:
                await callback.answer("Bu birinchi natija")
                
        except Exception as e:
            logger.error(f"Error in show_previous_search_result: {e}")
            await callback.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "next_search_result")
    async def show_next_search_result(callback: CallbackQuery, state: FSMContext):
        """Show next search result"""
        try:
            await callback.answer()
            
            # Get current index from state or default to 0
            current_index = await state.get_data()
            current_index = current_index.get('current_search_index', 0)
            
            # Get search results from state
            search_data = await state.get_data()
            search_results = search_data.get('search_results', [])
            query = search_data.get('search_query', '')
            
            if current_index < len(search_results) - 1:
                new_index = current_index + 1
                await state.update_data(current_search_index=new_index)
                await show_search_result(callback, search_results[new_index], search_results, new_index, query)
            else:
                await callback.answer("Bu oxirgi natija")
                
        except Exception as e:
            logger.error(f"Error in show_next_search_result: {e}")
            await callback.answer("Xatolik yuz berdi")

    return router

def get_search_results_navigation_keyboard(current_index: int, total_results: int):
    """Create navigation keyboard for search results"""
    keyboard = []
    
    # Navigation row
    nav_buttons = []
    
    # Previous button
    if current_index > 0:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Oldingi",
            callback_data="prev_search_result"
        ))
    
    # Next button
    if current_index < total_results - 1:
        nav_buttons.append(InlineKeyboardButton(
            text="Keyingi ➡️",
            callback_data="next_search_result"
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Back to menu
    keyboard.append([InlineKeyboardButton(text="🏠 Bosh sahifa", callback_data="back_to_main_menu")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 