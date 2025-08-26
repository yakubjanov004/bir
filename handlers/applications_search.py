"""
Manager Applications Search Handler - Mock Data Version

This module handles manager applications search functionality.
Mock data bilan ishlaydi, database kerak emas.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from keyboards.manager_buttons import get_manager_search_keyboard, get_manager_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Mock data for applications search
MOCK_APPLICATIONS = [
    {
        'id': 'APP001',
        'client_name': 'Aziz Karimov',
        'address': 'Toshkent, Chilonzor tumani',
        'status': 'new',
        'created_date': '2024-01-15',
        'priority': 'normal',
        'type': 'connection',
        'description': 'Internet ulanish so\'rovi',
        'contact_info': {
            'full_name': 'Aziz Karimov',
            'phone': '+998 90 123 45 67'
        }
    },
    {
        'id': 'APP002',
        'client_name': 'Malika Yusupova',
        'address': 'Toshkent, Sergeli tumani',
        'status': 'active',
        'created_date': '2024-01-14',
        'priority': 'high',
        'type': 'technical',
        'description': 'Internet tezligi past',
        'contact_info': {
            'full_name': 'Malika Yusupova',
            'phone': '+998 91 234 56 78'
        }
    },
    {
        'id': 'APP003',
        'client_name': 'Jasur Toshmatov',
        'address': 'Toshkent, Yashnobod tumani',
        'status': 'completed',
        'created_date': '2024-01-13',
        'priority': 'normal',
        'type': 'connection',
        'description': 'Yangi uy uchun internet',
        'contact_info': {
            'full_name': 'Jasur Toshmatov',
            'phone': '+998 92 345 67 89'
        }
    },
    {
        'id': 'APP004',
        'client_name': 'Dilfuza Rahimova',
        'address': 'Toshkent, Mirabad tumani',
        'status': 'active',
        'created_date': '2024-01-12',
        'priority': 'urgent',
        'type': 'technical',
        'description': 'Router muammosi',
        'contact_info': {
            'full_name': 'Dilfuza Rahimova',
            'phone': '+998 93 456 78 90'
        }
    },
    {
        'id': 'APP005',
        'client_name': 'Rustam Alimov',
        'address': 'Toshkent, Shayxontohur tumani',
        'status': 'completed',
        'created_date': '2024-01-11',
        'priority': 'low',
        'type': 'connection',
        'description': 'Ofis uchun internet',
        'contact_info': {
            'full_name': 'Rustam Alimov',
            'phone': '+998 94 567 89 01'
        }
    }
]

def search_applications_mock(query: str, search_type: str = 'all'):
    """Search applications in mock data"""
    try:
        query = query.lower()
        results = []
        
        for app in MOCK_APPLICATIONS:
            # Search in different fields
            if (query in app['client_name'].lower() or
                query in app['id'].lower() or
                query in app['address'].lower() or
                query in app['description'].lower() or
                query in app['contact_info']['phone'] or
                query in app['status'].lower() or
                query in app['type'].lower()):
                results.append(app)
        
        return results
        
    except Exception as e:
        logger.error(f"Mock search error: {e}")
        return []

class ManagerSearchStates(StatesGroup):
    waiting_for_search_input = State()

def get_manager_applications_search_router():
    """Router for applications search with mock data"""
    router = Router()
    
    @router.message(F.text.in_(["🔎 Qidirish"]))
    async def show_search_menu(message: Message, state: FSMContext):
        """Show search menu using mock data"""
        try:
            # Mock user info
            mock_user = {
                'id': message.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            if lang == 'uz':
                text = """🔎 <b>Arizalar qidirish</b>

Qidirish turini tanlang:"""
            else:
                text = """🔎 <b>Поиск заявок</b>

Выберите тип поиска:"""
            
            # Create search keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="📱 Telefon raqami" if lang == 'uz' else "📱 Номер телефона",
                    callback_data="mgr_search_phone"
                )],
                [InlineKeyboardButton(
                    text="👤 Mijoz ismi" if lang == 'uz' else "👤 Имя клиента",
                    callback_data="mgr_search_name"
                )],
                [InlineKeyboardButton(
                    text="🆔 Ariza ID" if lang == 'uz' else "🆔 ID заявки",
                    callback_data="mgr_search_id"
                )],
                [InlineKeyboardButton(
                    text="📍 Manzil" if lang == 'uz' else "📍 Адрес",
                    callback_data="mgr_search_address"
                )],
                [InlineKeyboardButton(
                    text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                    callback_data="mgr_back_to_main"
                )]
            ])
            
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error showing search menu: {e}")
            await message.answer("❌ Xatolik yuz berdi")
    
    @router.callback_query(F.data.startswith("mgr_search_"))
    async def handle_search_type(callback: CallbackQuery, state: FSMContext):
        """Handle search type selection"""
        try:
            await callback.answer()
            
            search_type = callback.data.replace("mgr_search_", "")
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Update state
            await state.update_data(search_type=search_type)
            
            # Show search input prompt
            if search_type == "phone":
                if lang == 'uz':
                    text = "📱 <b>Telefon raqami orqali qidirish</b>\n\nTelefon raqamini kiriting (masalan: +998 90 123 45 67):"
                else:
                    text = "📱 <b>Поиск по номеру телефона</b>\n\nВведите номер телефона (например: +998 90 123 45 67):"
            
            elif search_type == "name":
                if lang == 'uz':
                    text = "👤 <b>Mijoz ismi orqali qidirish</b>\n\nMijoz ismini kiriting:"
                else:
                    text = "👤 <b>Поиск по имени клиента</b>\n\nВведите имя клиента:"
            
            elif search_type == "id":
                if lang == 'uz':
                    text = "🆔 <b>Ariza ID orqali qidirish</b>\n\nAriza ID sini kiriting (masalan: APP001):"
                else:
                    text = "🆔 <b>Поиск по ID заявки</b>\n\nВведите ID заявки (например: APP001):"
            
            elif search_type == "address":
                if lang == 'uz':
                    text = "📍 <b>Manzil orqali qidirish</b>\n\nManzilni kiriting (masalan: Chilonzor):"
                else:
                    text = "📍 <b>Поиск по адресу</b>\n\nВведите адрес (например: Чиланзар):"
            
            else:
                if lang == 'uz':
                    text = "🔎 <b>Qidirish</b>\n\nQidiruv so'zini kiriting:"
                else:
                    text = "🔎 <b>Поиск</b>\n\nВведите поисковый запрос:"
            
            # Create back keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                    callback_data="mgr_back_to_search"
                )
            ]])
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
            # Set state for waiting for search input
            await state.set_state(ManagerSearchStates.waiting_for_search_input)
            
        except Exception as e:
            logger.error(f"Error handling search type: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.message(StateFilter(ManagerSearchStates.waiting_for_search_input), F.text)
    async def handle_search_input(message: Message, state: FSMContext):
        """Handle search input"""
        try:
            # Get search type from state
            state_data = await state.get_data()
            search_type = state_data.get('search_type', 'all')
            
            # Mock user info
            mock_user = {
                'id': message.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Perform search
            search_query = message.text.strip()
            results = search_applications_mock(search_query, search_type)
            
            if not results:
                if lang == 'uz':
                    text = f"❌ <b>Qidiruv natijasi</b>\n\n'{search_query}' uchun hech narsa topilmadi.\n\nBoshqa so'z bilan qayta urinib ko'ring."
                else:
                    text = f"❌ <b>Результат поиска</b>\n\nПо запросу '{search_query}' ничего не найдено.\n\nПопробуйте с другими словами."
                
                # Create search again keyboard
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(
                        text="🔎 Qayta qidirish" if lang == 'uz' else "🔎 Поиск снова",
                        callback_data="mgr_search_start"
                    )],
                    [InlineKeyboardButton(
                        text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                        callback_data="mgr_back_to_main"
                    )]
                ])
                
                await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
                await state.clear()
                return
            
            # Show search results
            if lang == 'uz':
                text = f"🔎 <b>Qidiruv natijasi</b>\n\n'{search_query}' uchun {len(results)} ta natija topildi:"
            else:
                text = f"🔎 <b>Результат поиска</b>\n\nПо запросу '{search_query}' найдено {len(results)} результатов:"
            
            # Add first result details
            first_result = results[0]
            text += f"\n\n📋 <b>Birinchi natija:</b>\n"
            text += f"🆔 ID: {first_result['id']}\n"
            text += f"👤 Mijoz: {first_result['client_name']}\n"
            text += f"📱 Telefon: {first_result['contact_info']['phone']}\n"
            text += f"📍 Manzil: {first_result['address']}\n"
            text += f"📊 Status: {first_result['status']}\n"
            text += f"📝 Tavsif: {first_result['description']}"
            
            # Create results navigation keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="👁 Batafsil ko'rish" if lang == 'uz' else "👁 Подробнее",
                    callback_data="mgr_view_search_result"
                )],
                [InlineKeyboardButton(
                    text="🔎 Qayta qidirish" if lang == 'uz' else "🔎 Поиск снова",
                    callback_data="mgr_search_start"
                )],
                [InlineKeyboardButton(
                    text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                    callback_data="mgr_back_to_main"
                )]
            ])
            
            # Update state with search results
            await state.update_data(
                search_results=results,
                current_result_index=0,
                search_query=search_query
            )
            
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            await state.clear()
            
        except Exception as e:
            logger.error(f"Error handling search input: {e}")
            await message.answer("❌ Xatolik yuz berdi")
    
    @router.callback_query(F.data == "mgr_view_search_result")
    async def view_search_result(callback: CallbackQuery, state: FSMContext):
        """View detailed search result"""
        try:
            await callback.answer()
            
            # Get search results from state
            state_data = await state.get_data()
            search_results = state_data.get('search_results', [])
            current_index = state_data.get('current_result_index', 0)
            
            if not search_results or current_index >= len(search_results):
                await callback.answer("❌ Natija topilmadi", show_alert=True)
                return
            
            result = search_results[current_index]
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Show detailed result
            if lang == 'uz':
                text = f"""📋 <b>Ariza ma'lumotlari</b>

🆔 ID: {result['id']}
👤 Mijoz: {result['client_name']}
📱 Telefon: {result['contact_info']['phone']}
📍 Manzil: {result['address']}
📊 Status: {result['status']}
🔴 Muhimlik: {result['priority']}
📝 Tur: {result['type']}
📅 Sana: {result['created_date']}
📄 Tavsif: {result['description']}"""
            else:
                text = f"""📋 <b>Информация о заявке</b>

🆔 ID: {result['id']}
👤 Клиент: {result['client_name']}
📱 Телефон: {result['contact_info']['phone']}
📍 Адрес: {result['address']}
📊 Статус: {result['status']}
🔴 Приоритет: {result['priority']}
📝 Тип: {result['type']}
📅 Дата: {result['created_date']}
📄 Описание: {result['description']}"""
            
            # Create navigation keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                    callback_data="mgr_back_to_search"
                )]
            ])
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error viewing search result: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_search_start")
    async def start_new_search(callback: CallbackQuery, state: FSMContext):
        """Start new search"""
        try:
            await callback.answer()
            
            # Clear state
            await state.clear()
            
            # Show search menu again
            await show_search_menu(callback.message, state)
            
        except Exception as e:
            logger.error(f"Error starting new search: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_back_to_search")
    async def back_to_search(callback: CallbackQuery, state: FSMContext):
        """Go back to search menu"""
        try:
            await callback.answer()
            
            # Clear state
            await state.clear()
            
            # Show search menu
            await show_search_menu(callback.message, state)
            
        except Exception as e:
            logger.error(f"Error going back to search: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_back_to_main")
    async def back_to_main(callback: CallbackQuery, state: FSMContext):
        """Go back to main menu"""
        try:
            await callback.answer()
            
            # Clear state
            await state.clear()
            
            # Import and show main keyboard
            from keyboards.manager_buttons import get_manager_main_keyboard
            keyboard = get_manager_main_keyboard('uz')  # Default to Uzbek
            
            text = "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:"
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error going back to main: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    return router 