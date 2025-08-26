"""
Technician Order Handler - Mock Data Version

Bu modul manager uchun texnik xizmat arizasi yaratish funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, database kerak emas.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
import logging
import json

from keyboards.manager_buttons import (
    get_manager_client_search_keyboard,
    get_manager_confirmation_keyboard,
)
from states.manager_states import ManagerClientSearchStates, ManagerServiceOrderStates

logger = logging.getLogger(__name__)

# Mock data for regions
MOCK_REGIONS = [
    {'id': 1, 'name': 'Toshkent', 'code': 'toshkent'},
    {'id': 2, 'name': 'Samarqand', 'code': 'samarqand'},
    {'id': 3, 'name': 'Buxoro', 'code': 'buxoro'},
    {'id': 4, 'name': 'Andijon', 'code': 'andijon'},
    {'id': 5, 'name': 'Farg\'ona', 'code': 'fargona'}
]

# Mock data for service types
MOCK_SERVICE_TYPES = [
    {'id': 1, 'name': 'Internet muammosi', 'code': 'internet', 'emoji': '🌐'},
    {'id': 2, 'name': 'TV muammosi', 'code': 'tv', 'emoji': '📺'},
    {'id': 3, 'name': 'Internet + TV muammosi', 'code': 'combo', 'emoji': '📡'},
    {'id': 4, 'name': 'Router muammosi', 'code': 'router', 'emoji': '📶'},
    {'id': 5, 'name': 'Kabel muammosi', 'code': 'cable', 'emoji': '🔌'}
]

# Mock data for problem types
MOCK_PROBLEM_TYPES = {
    'internet': [
        {'id': 1, 'name': 'Internet uzilishi', 'code': 'disconnection', 'emoji': '❌'},
        {'id': 2, 'name': 'Tezlik past', 'code': 'slow_speed', 'emoji': '🐌'},
        {'id': 3, 'name': 'Ping baland', 'code': 'high_ping', 'emoji': '📡'},
        {'id': 4, 'name': 'Uzluksiz uzilish', 'code': 'intermittent', 'emoji': '🔄'}
    ],
    'tv': [
        {'id': 1, 'name': 'Kanallar ko\'rinmaydi', 'code': 'no_channels', 'emoji': '📺'},
        {'id': 2, 'name': 'Sifat yomon', 'code': 'poor_quality', 'emoji': '📉'},
        {'id': 3, 'name': 'Ovoz yo\'q', 'code': 'no_sound', 'emoji': '🔇'},
        {'id': 4, 'name': 'Kanallar uziladi', 'code': 'channels_disconnect', 'emoji': '📡'}
    ],
    'combo': [
        {'id': 1, 'name': 'Internet + TV uzilishi', 'code': 'both_disconnect', 'emoji': '❌'},
        {'id': 2, 'name': 'Internet ishlaydi, TV yo\'q', 'code': 'internet_ok_tv_no', 'emoji': '🌐❌📺'},
        {'id': 3, 'name': 'TV ishlaydi, Internet yo\'q', 'code': 'tv_ok_internet_no', 'emoji': '📺❌🌐'},
        {'id': 4, 'name': 'Ikkalasi ham yomon', 'code': 'both_poor', 'emoji': '📉'}
    ],
    'router': [
        {'id': 1, 'name': 'Router ishlamaydi', 'code': 'not_working', 'emoji': '❌'},
        {'id': 2, 'name': 'WiFi signal kuchsiz', 'code': 'weak_signal', 'emoji': '📶'},
        {'id': 3, 'name': 'Parol esdan chiqdi', 'code': 'forgot_password', 'emoji': '🔑'},
        {'id': 4, 'name': 'Router qizib ketdi', 'code': 'overheating', 'emoji': '🔥'}
    ],
    'cable': [
        {'id': 1, 'name': 'Kabel uzilgan', 'code': 'broken', 'emoji': '🔌'},
        {'id': 2, 'name': 'Kabel eskirgan', 'code': 'worn_out', 'emoji': '🔌'},
        {'id': 3, 'name': 'Kabel noto\'g\'ri ulangan', 'code': 'wrong_connection', 'emoji': '🔌'},
        {'id': 4, 'name': 'Kabel uzunligi yetarli emas', 'code': 'too_short', 'emoji': '📏'}
    ]
}

# Mock data for clients
MOCK_CLIENTS = [
    {
        'id': 1,
        'full_name': 'Aziz Karimov',
        'phone': '+998 90 123 45 67',
        'address': 'Toshkent, Chilonzor tumani, 1-uy',
        'region': 'toshkent',
        'abonent_id': 'AB001'
    },
    {
        'id': 2,
        'full_name': 'Malika Yusupova',
        'phone': '+998 91 234 56 78',
        'address': 'Toshkent, Sergeli tumani, 15-uy',
        'region': 'toshkent',
        'abonent_id': 'AB002'
    },
    {
        'id': 3,
        'full_name': 'Jasur Toshmatov',
        'phone': '+998 92 345 67 89',
        'address': 'Samarqand, Oq daryo tumani, 7-uy',
        'region': 'samarqand',
        'abonent_id': 'AB003'
    }
]

# Technical service cost calculations
def calculate_technical_service_cost(service_type: str, problem_type: str = 'standard') -> dict:
    """Calculate technical service cost based on type"""
    costs = {
        'internet': {
            'disconnection': {'visit_fee': 50000, 'repair_fee': 100000, 'parts': 0},
            'slow_speed': {'visit_fee': 50000, 'repair_fee': 150000, 'parts': 50000},
            'high_ping': {'visit_fee': 50000, 'repair_fee': 120000, 'parts': 30000},
            'intermittent': {'visit_fee': 50000, 'repair_fee': 180000, 'parts': 80000}
        },
        'tv': {
            'no_channels': {'visit_fee': 40000, 'repair_fee': 80000, 'parts': 0},
            'poor_quality': {'visit_fee': 40000, 'repair_fee': 120000, 'parts': 30000},
            'no_sound': {'visit_fee': 40000, 'repair_fee': 100000, 'parts': 20000},
            'channels_disconnect': {'visit_fee': 40000, 'repair_fee': 150000, 'parts': 50000}
        },
        'combo': {
            'both_disconnect': {'visit_fee': 60000, 'repair_fee': 200000, 'parts': 80000},
            'internet_ok_tv_no': {'visit_fee': 60000, 'repair_fee': 150000, 'parts': 50000},
            'tv_ok_internet_no': {'visit_fee': 60000, 'repair_fee': 180000, 'parts': 60000},
            'both_poor': {'visit_fee': 60000, 'repair_fee': 250000, 'parts': 100000}
        },
        'router': {
            'not_working': {'visit_fee': 50000, 'repair_fee': 200000, 'parts': 150000},
            'weak_signal': {'visit_fee': 50000, 'repair_fee': 120000, 'parts': 30000},
            'forgot_password': {'visit_fee': 50000, 'repair_fee': 50000, 'parts': 0},
            'overheating': {'visit_fee': 50000, 'repair_fee': 180000, 'parts': 80000}
        },
        'cable': {
            'broken': {'visit_fee': 40000, 'repair_fee': 100000, 'parts': 50000},
            'worn_out': {'visit_fee': 40000, 'repair_fee': 120000, 'parts': 60000},
            'wrong_connection': {'visit_fee': 40000, 'repair_fee': 80000, 'parts': 0},
            'too_short': {'visit_fee': 40000, 'repair_fee': 150000, 'parts': 80000}
        }
    }
    
    service_type = service_type.lower()
    problem_type = problem_type.lower()
    
    if service_type in costs and problem_type in costs[service_type]:
        cost_data = costs[service_type][problem_type]
        total = cost_data['visit_fee'] + cost_data['repair_fee'] + cost_data['parts']
        return {
            'visit_fee': cost_data['visit_fee'],
            'repair_fee': cost_data['repair_fee'],
            'parts_fee': cost_data['parts'],
            'total_cost': total
        }
    
    return {
        'visit_fee': 50000,
        'repair_fee': 100000,
        'parts_fee': 0,
        'total_cost': 150000
    }

def get_manager_technician_order_router():
    """Router for technician order creation with mock data"""
    router = Router()
    
    @router.message(F.text.in_(["🔧 Texnik xizmat yaratish", "🔧 Создать заявку на техобслуживание"])) 
    async def show_technician_order_menu(message: Message, state: FSMContext):
        """Show technician order creation menu"""
        try:
            # Mock user info
            mock_user = {
                'id': message.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            if lang == 'uz':
                text = """🔧 <b>Texnik xizmat arizasi yaratish</b>

Qaysi viloyat uchun ariza yaratmoqchisiz?

Viloyatni tanlang:"""
            else:
                text = """🔧 <b>Создание заявки на техническое обслуживание</b>

Для какой области вы хотите создать заявку?

Выберите область:"""
            
            # Create regions keyboard
            buttons = []
            for region in MOCK_REGIONS:
                buttons.append([InlineKeyboardButton(
                    text=f"📍 {region['name']}",
                    callback_data=f"mgr_tech_region_{region['code']}"
                )])
            
            # Add back button
            buttons.append([InlineKeyboardButton(
                text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                callback_data="mgr_back_to_main"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error showing technician order menu: {e}")
            await message.answer("❌ Xatolik yuz berdi")
    
    @router.callback_query(F.data.startswith("mgr_tech_region_"))
    async def select_tech_region(callback: CallbackQuery, state: FSMContext):
        """Select region for technician order"""
        try:
            await callback.answer()
            
            # Extract region code
            region_code = callback.data.replace("mgr_tech_region_", "")
            
            # Update state
            await state.update_data(region=region_code)
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            if lang == 'uz':
                text = f"""🔧 <b>Texnik xizmat arizasi yaratish</b>

📍 Viloyat: {region_code.title()}

Xizmat turini tanlang:"""
            else:
                text = f"""🔧 <b>Создание заявки на техническое обслуживание</b>

📍 Область: {region_code.title()}

Выберите тип услуги:"""
            
            # Create service types keyboard
            buttons = []
            for service_type in MOCK_SERVICE_TYPES:
                buttons.append([InlineKeyboardButton(
                    text=f"{service_type['emoji']} {service_type['name']}",
                    callback_data=f"mgr_service_type_{service_type['code']}"
                )])
            
            # Add back button
            buttons.append([InlineKeyboardButton(
                text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                callback_data="mgr_back_to_tech"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error selecting tech region: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("mgr_service_type_"))
    async def select_service_type(callback: CallbackQuery, state: FSMContext):
        """Select service type"""
        try:
            await callback.answer()
            
            # Extract service type
            service_type = callback.data.replace("mgr_service_type_", "")
            
            # Update state
            await state.update_data(service_type=service_type)
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            if lang == 'uz':
                text = f"""🔧 <b>Texnik xizmat arizasi yaratish</b>

📍 Viloyat: {callback.message.text.split('📍')[1].split('\n')[0].strip()}
🔧 Xizmat: {service_type.title()}

Muammo turini tanlang:"""
            else:
                text = f"""🔧 <b>Создание заявки на техническое обслуживание</b>

📍 Область: {callback.message.text.split('📍')[1].split('\n')[0].strip()}
🔧 Услуга: {service_type.title()}

Выберите тип проблемы:"""
            
            # Create problem types keyboard
            buttons = []
            problem_types = MOCK_PROBLEM_TYPES.get(service_type, [])
            for problem in problem_types:
                buttons.append([InlineKeyboardButton(
                    text=f"{problem['emoji']} {problem['name']}",
                    callback_data=f"mgr_problem_{service_type}_{problem['code']}"
                )])
            
            # Add back button
            buttons.append([InlineKeyboardButton(
                text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                callback_data=f"mgr_tech_region_{callback.message.text.split('📍')[1].split('\n')[0].strip().lower()}"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error selecting service type: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("mgr_problem_"))
    async def select_problem_type(callback: CallbackQuery, state: FSMContext):
        """Select problem type"""
        try:
            await callback.answer()
            
            # Extract problem info
            parts = callback.data.replace("mgr_problem_", "").split("_")
            service_type = parts[0]
            problem_type = parts[1]
            
            # Update state
            await state.update_data(problem_type=problem_type)
            
            # Calculate costs
            costs = calculate_technical_service_cost(service_type, problem_type)
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            if lang == 'uz':
                text = f"""🔧 <b>Texnik xizmat arizasi yaratish</b>

📍 Viloyat: {callback.message.text.split('📍')[1].split('\n')[0].strip()}
🔧 Xizmat: {service_type.title()}
⚠️ Muammo: {problem_type.replace('_', ' ').title()}

💰 <b>Narx ma'lumotlari:</b>
• Tashrif: {costs['visit_fee']:,} so'm
• Tuzatish: {costs['repair_fee']:,} so'm
• Qismlar: {costs['parts_fee']:,} so'm
• Jami: {costs['total_cost']:,} so'm

Keyingi qadam uchun mijoz ma'lumotlarini kiriting."""
            else:
                text = f"""🔧 <b>Создание заявки на техническое обслуживание</b>

📍 Область: {callback.message.text.split('📍')[1].split('\n')[0].strip()}
🔧 Услуга: {service_type.title()}
⚠️ Проблема: {problem_type.replace('_', ' ').title()}

💰 <b>Информация о ценах:</b>
• Визит: {costs['visit_fee']:,} сум
• Ремонт: {costs['repair_fee']:,} сум
• Детали: {costs['parts_fee']:,} сум
• Всего: {costs['total_cost']:,} сум

Для следующего шага введите данные клиента."""
            
            # Create client search keyboard
            keyboard = get_manager_client_search_keyboard(lang)
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
            # Set state for client search
            await state.set_state(ManagerClientSearchStates.selecting_client_search_method)
            
        except Exception as e:
            logger.error(f"Error selecting problem type: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_back_to_tech")
    async def back_to_technician(callback: CallbackQuery, state: FSMContext):
        """Go back to technician order menu"""
        try:
            await callback.answer()
            
            # Clear state
            await state.clear()
            
            # Show technician order menu again
            await show_technician_order_menu(callback.message, state)
            
        except Exception as e:
            logger.error(f"Error going back to technician: {e}")
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