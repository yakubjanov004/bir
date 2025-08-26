"""
Connection Order Handler - Mock Data Version

Bu modul manager uchun ulanish arizasi yaratish funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, database kerak emas.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
import logging
import json

from states.manager_states import ManagerClientSearchStates, ManagerConnectionOrderStates
from keyboards.manager_buttons import get_manager_client_search_keyboard, get_manager_confirmation_keyboard

logger = logging.getLogger(__name__)

# Mock data for regions
MOCK_REGIONS = [
    {'id': 1, 'name': 'Toshkent', 'code': 'toshkent'},
    {'id': 2, 'name': 'Samarqand', 'code': 'samarqand'},
    {'id': 3, 'name': 'Buxoro', 'code': 'buxoro'},
    {'id': 4, 'name': 'Andijon', 'code': 'andijon'},
    {'id': 5, 'name': 'Farg\'ona', 'code': 'fargona'}
]

# Mock data for connection types
MOCK_CONNECTION_TYPES = [
    {'id': 1, 'name': 'Internet', 'code': 'internet', 'emoji': '🌐'},
    {'id': 2, 'name': 'TV', 'code': 'tv', 'emoji': '📺'},
    {'id': 3, 'name': 'Internet + TV', 'code': 'combo', 'emoji': '📡'}
]

# Mock data for tariffs
MOCK_TARIFFS = {
    'internet': [
        {'id': 1, 'name': 'Standard', 'speed': '50 Mbps', 'price': 89000, 'emoji': '⚡'},
        {'id': 2, 'name': 'Premium', 'speed': '100 Mbps', 'price': 129000, 'emoji': '🚀'},
        {'id': 3, 'name': 'Ultra', 'speed': '200 Mbps', 'price': 189000, 'emoji': '🔥'}
    ],
    'tv': [
        {'id': 1, 'name': 'Basic', 'channels': 100, 'price': 45000, 'emoji': '📺'},
        {'id': 2, 'name': 'Premium', 'channels': 200, 'price': 65000, 'emoji': '🎬'},
        {'id': 3, 'name': 'Ultra', 'channels': 300, 'price': 89000, 'emoji': '🌟'}
    ],
    'combo': [
        {'id': 1, 'name': 'Standard', 'internet': '50 Mbps', 'tv': 100, 'price': 119000, 'emoji': '📡'},
        {'id': 2, 'name': 'Premium', 'internet': '100 Mbps', 'tv': 200, 'price': 169000, 'emoji': '🚀'},
        {'id': 3, 'name': 'Ultra', 'internet': '200 Mbps', 'tv': 300, 'price': 239000, 'emoji': '🔥'}
    ]
}

# Mock data for clients
MOCK_CLIENTS = [
    {
        'id': 1,
        'full_name': 'Aziz Karimov',
        'phone': '+998 90 123 45 67',
        'address': 'Toshkent, Chilonzor tumani, 1-uy',
        'region': 'toshkent'
    },
    {
        'id': 2,
        'full_name': 'Malika Yusupova',
        'phone': '+998 91 234 56 78',
        'address': 'Toshkent, Sergeli tumani, 15-uy',
        'region': 'toshkent'
    },
    {
        'id': 3,
        'full_name': 'Jasur Toshmatov',
        'phone': '+998 92 345 67 89',
        'address': 'Samarqand, Oq daryo tumani, 7-uy',
        'region': 'samarqand'
    }
]

# Tariff calculations
def calculate_connection_cost(connection_type: str, tariff: str) -> dict:
    """Calculate connection cost based on type and tariff"""
    costs = {
        'internet': {
            'standard': {'setup': 150000, 'monthly': 89000, 'equipment': 250000},
            'premium': {'setup': 100000, 'monthly': 129000, 'equipment': 350000},
            'ultra': {'setup': 80000, 'monthly': 189000, 'equipment': 450000}
        },
        'tv': {
            'basic': {'setup': 100000, 'monthly': 45000, 'equipment': 180000},
            'premium': {'setup': 80000, 'monthly': 65000, 'equipment': 220000},
            'ultra': {'setup': 60000, 'monthly': 89000, 'equipment': 280000}
        },
        'combo': {
            'standard': {'setup': 200000, 'monthly': 119000, 'equipment': 400000},
            'premium': {'setup': 150000, 'monthly': 169000, 'equipment': 500000},
            'ultra': {'setup': 120000, 'monthly': 239000, 'equipment': 600000}
        }
    }
    
    connection_type = connection_type.lower()
    tariff = tariff.lower()
    
    if connection_type in costs and tariff in costs[connection_type]:
        cost_data = costs[connection_type][tariff]
        total = cost_data['setup'] + cost_data['equipment']
        return {
            'setup_fee': cost_data['setup'],
            'monthly_fee': cost_data['monthly'],
            'equipment_fee': cost_data['equipment'],
            'total_initial': total,
            'monthly_total': cost_data['monthly']
        }
    
    return {
        'setup_fee': 150000,
        'monthly_fee': 89000,
        'equipment_fee': 250000,
        'total_initial': 400000,
        'monthly_total': 89000
    }

def get_manager_connection_order_router():
    """Router for connection order creation with mock data"""
    router = Router()
    
    @router.message(F.text.in_(["🔌 Ulanish arizasi yaratish", "🔌 Создать заявку на подключение"]))
    async def show_connection_order_menu(message: Message, state: FSMContext):
        """Show connection order creation menu"""
        try:
            # Mock user info
            mock_user = {
                'id': message.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            if lang == 'uz':
                text = """🔌 <b>Ulanish arizasi yaratish</b>

Qaysi viloyat uchun ariza yaratmoqchisiz?

Viloyatni tanlang:"""
            else:
                text = """🔌 <b>Создание заявки на подключение</b>

Для какой области вы хотите создать заявку?

Выберите область:"""
            
            # Create regions keyboard
            buttons = []
            for region in MOCK_REGIONS:
                buttons.append([InlineKeyboardButton(
                    text=f"📍 {region['name']}",
                    callback_data=f"mgr_region_{region['code']}"
                )])
            
            # Add back button
            buttons.append([InlineKeyboardButton(
                text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                callback_data="mgr_back_to_main"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error showing connection order menu: {e}")
            await message.answer("❌ Xatolik yuz berdi")
    
    @router.callback_query(F.data.startswith("mgr_region_"))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        """Select region for connection order"""
        try:
            await callback.answer()
            
            # Extract region code
            region_code = callback.data.replace("mgr_region_", "")
            
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
                text = f"""🔌 <b>Ulanish arizasi yaratish</b>

📍 Viloyat: {region_code.title()}

Ulanish turini tanlang:"""
            else:
                text = f"""🔌 <b>Создание заявки на подключение</b>

📍 Область: {region_code.title()}

Выберите тип подключения:"""
            
            # Create connection types keyboard
            buttons = []
            for conn_type in MOCK_CONNECTION_TYPES:
                buttons.append([InlineKeyboardButton(
                    text=f"{conn_type['emoji']} {conn_type['name']}",
                    callback_data=f"mgr_conn_type_{conn_type['code']}"
                )])
            
            # Add back button
            buttons.append([InlineKeyboardButton(
                text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                callback_data="mgr_back_to_connection"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error selecting region: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("mgr_conn_type_"))
    async def select_connection_type(callback: CallbackQuery, state: FSMContext):
        """Select connection type"""
        try:
            await callback.answer()
            
            # Extract connection type
            conn_type = callback.data.replace("mgr_conn_type_", "")
            
            # Update state
            await state.update_data(connection_type=conn_type)
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            if lang == 'uz':
                text = f"""🔌 <b>Ulanish arizasi yaratish</b>

📍 Viloyat: {callback.message.text.split('📍')[1].split('\n')[0].strip()}
🔌 Tur: {conn_type.title()}

Tarifni tanlang:"""
            else:
                text = f"""🔌 <b>Создание заявки на подключение</b>

📍 Область: {callback.message.text.split('📍')[1].split('\n')[0].strip()}
🔌 Тип: {conn_type.title()}

Выберите тариф:"""
            
            # Create tariffs keyboard
            buttons = []
            tariffs = MOCK_TARIFFS.get(conn_type, [])
            for tariff in tariffs:
                if conn_type == 'internet':
                    display_text = f"{tariff['emoji']} {tariff['name']} - {tariff['speed']} - {tariff['price']:,} so'm"
                elif conn_type == 'tv':
                    display_text = f"{tariff['emoji']} {tariff['name']} - {tariff['channels']} kanal - {tariff['price']:,} so'm"
                else:  # combo
                    display_text = f"{tariff['emoji']} {tariff['name']} - {tariff['internet']} + {tariff['tv']} kanal - {tariff['price']:,} so'm"
                
                buttons.append([InlineKeyboardButton(
                    text=display_text,
                    callback_data=f"mgr_tariff_{conn_type}_{tariff['name'].lower()}"
                )])
            
            # Add back button
            buttons.append([InlineKeyboardButton(
                text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                callback_data=f"mgr_region_{callback.message.text.split('📍')[1].split('\n')[0].strip().lower()}"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error selecting connection type: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("mgr_tariff_"))
    async def select_tariff(callback: CallbackQuery, state: FSMContext):
        """Select tariff"""
        try:
            await callback.answer()
            
            # Extract tariff info
            parts = callback.data.replace("mgr_tariff_", "").split("_")
            conn_type = parts[0]
            tariff = parts[1]
            
            # Update state
            await state.update_data(tariff=tariff)
            
            # Calculate costs
            costs = calculate_connection_cost(conn_type, tariff)
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            if lang == 'uz':
                text = f"""🔌 <b>Ulanish arizasi yaratish</b>

📍 Viloyat: {callback.message.text.split('📍')[1].split('\n')[0].strip()}
🔌 Tur: {conn_type.title()}
📊 Tarif: {tariff.title()}

💰 <b>Narx ma'lumotlari:</b>
• O'rnatish: {costs['setup_fee']:,} so'm
• Jihozlar: {costs['equipment_fee']:,} so'm
• Oylik to'lov: {costs['monthly_fee']:,} so'm
• Jami boshlang'ich: {costs['total_initial']:,} so'm

Keyingi qadam uchun mijoz ma'lumotlarini kiriting."""
            else:
                text = f"""🔌 <b>Создание заявки на подключение</b>

📍 Область: {callback.message.text.split('📍')[1].split('\n')[0].strip()}
🔌 Тип: {conn_type.title()}
📊 Тариф: {tariff.title()}

💰 <b>Информация о ценах:</b>
• Установка: {costs['setup_fee']:,} сум
• Оборудование: {costs['equipment_fee']:,} сум
• Ежемесячный платеж: {costs['monthly_fee']:,} сум
• Общий начальный: {costs['total_initial']:,} сум

Для следующего шага введите данные клиента."""
            
            # Create client search keyboard
            keyboard = get_manager_client_search_keyboard(lang)
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
            # Set state for client search
            await state.set_state(ManagerClientSearchStates.selecting_client_search_method)
            
        except Exception as e:
            logger.error(f"Error selecting tariff: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_back_to_connection")
    async def back_to_connection(callback: CallbackQuery, state: FSMContext):
        """Go back to connection order menu"""
        try:
            await callback.answer()
            
            # Clear state
            await state.clear()
            
            # Show connection order menu again
            await show_connection_order_menu(callback.message, state)
            
        except Exception as e:
            logger.error(f"Error going back to connection: {e}")
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