"""
Applications List Handler - Mock Data Version

Bu modul manager uchun arizalar ro'yxati va navigatsiya funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, database kerak emas.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from keyboards.manager_buttons import get_manager_view_applications_keyboard, get_manager_back_keyboard
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Mock data for applications
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
    },
    {
        'id': 'APP006',
        'client_name': 'Zarina Karimova',
        'address': 'Toshkent, Uchtepa tumani',
        'status': 'new',
        'created_date': '2024-01-10',
        'priority': 'high',
        'type': 'technical',
        'description': 'Internet uzilishi',
        'contact_info': {
            'full_name': 'Zarina Karimova',
            'phone': '+998 95 678 90 12'
        }
    },
    {
        'id': 'APP007',
        'client_name': 'Farrux Toshmatov',
        'address': 'Toshkent, Bektemir tumani',
        'status': 'active',
        'created_date': '2024-01-09',
        'priority': 'normal',
        'type': 'connection',
        'description': 'Kafe uchun internet',
        'contact_info': {
            'full_name': 'Farrux Toshmatov',
            'phone': '+998 96 789 01 23'
        }
    },
    {
        'id': 'APP008',
        'client_name': 'Nilufar Rahimova',
        'address': 'Toshkent, Yangihayot tumani',
        'status': 'cancelled',
        'created_date': '2024-01-08',
        'priority': 'low',
        'type': 'technical',
        'description': 'WiFi sozlamalari',
        'contact_info': {
            'full_name': 'Nilufar Rahimova',
            'phone': '+998 97 890 12 34'
        }
    }
]

def get_manager_applications_list_router():
    """Router for applications list with mock data"""
    router = Router()
    
    @router.message(F.text.in_(["📋 Arizalar ro'yxati"]))
    async def show_applications_list(message: Message, state: FSMContext):
        """Show applications list using mock data"""
        try:
            # Mock user info
            mock_user = {
                'id': message.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Get applications from mock data
            applications = MOCK_APPLICATIONS
            
            if not applications:
                if lang == 'uz':
                    text = "❌ Arizalar topilmadi"
                else:
                    text = "❌ Заявки не найдены"
                
                await message.answer(text)
                return
            
            # Show first application
            await state.update_data(
                applications=applications,
                current_index=0
            )
            
            await display_application(message, applications[0], 0, len(applications), lang)
            
        except Exception as e:
            logger.error(f"Error showing applications list: {e}")
            await message.answer("❌ Xatolik yuz berdi")
    
    @router.callback_query(F.data.startswith("mgr_apps_"))
    async def handle_applications_filter(callback: CallbackQuery, state: FSMContext):
        """Handle applications filter"""
        try:
            await callback.answer()
            
            data = callback.data
            user_id = callback.from_user.id
            
            # Mock user info
            mock_user = {
                'id': user_id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            if data == "mgr_apps_all":
                applications = MOCK_APPLICATIONS
                filter_name = "Barcha arizalar" if lang == 'uz' else "Все заявки"
            
            elif data == "mgr_apps_active":
                applications = [app for app in MOCK_APPLICATIONS if app['status'] == 'active']
                filter_name = "Faol arizalar" if lang == 'uz' else "Активные заявки"
            
            elif data == "mgr_apps_completed":
                applications = [app for app in MOCK_APPLICATIONS if app['status'] == 'completed']
                filter_name = "Bajarilgan arizalar" if lang == 'uz' else "Выполненные заявки"
            
            elif data == "mgr_apps_new":
                applications = [app for app in MOCK_APPLICATIONS if app['status'] == 'new']
                filter_name = "Yangi arizalar" if lang == 'uz' else "Новые заявки"
            
            elif data == "mgr_apps_cancelled":
                applications = [app for app in MOCK_APPLICATIONS if app['status'] == 'cancelled']
                filter_name = "Bekor qilingan arizalar" if lang == 'uz' else "Отмененные заявки"
            
            else:
                applications = MOCK_APPLICATIONS
                filter_name = "Barcha arizalar" if lang == 'uz' else "Все заявки"
            
            if not applications:
                if lang == 'uz':
                    text = f"❌ {filter_name} topilmadi"
                else:
                    text = f"❌ {filter_name} не найдены"
                
                await callback.message.edit_text(text)
                return
            
            # Update state
            await state.update_data(
                applications=applications,
                current_index=0
            )
            
            # Show first application
            await display_application(callback.message, applications[0], 0, len(applications), lang)
            
        except Exception as e:
            logger.error(f"Error handling applications filter: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_app_prev")
    async def show_previous_application(callback: CallbackQuery, state: FSMContext):
        """Show previous application"""
        try:
            await callback.answer()
            
            # Get current data from state
            state_data = await state.get_data()
            current_index = state_data.get('current_index', 0)
            applications = state_data.get('applications', MOCK_APPLICATIONS)
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_index=new_index)
                
                # Mock user info
                mock_user = {
                    'id': callback.from_user.id,
                    'language': 'uz',
                    'role': 'manager'
                }
                
                lang = mock_user.get('language', 'uz')
                
                await display_application(callback.message, applications[new_index], new_index, len(applications), lang)
            else:
                await callback.answer("Birinchi ariza", show_alert=True)
            
        except Exception as e:
            logger.error(f"Error showing previous application: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_app_next")
    async def show_next_application(callback: CallbackQuery, state: FSMContext):
        """Show next application"""
        try:
            await callback.answer()
            
            # Get current data from state
            state_data = await state.get_data()
            current_index = state_data.get('current_index', 0)
            applications = state_data.get('applications', MOCK_APPLICATIONS)
            
            if current_index < len(applications) - 1:
                new_index = current_index + 1
                await state.update_data(current_index=new_index)
                
                # Mock user info
                mock_user = {
                    'id': callback.from_user.id,
                    'language': 'uz',
                    'role': 'manager'
                }
                
                lang = mock_user.get('language', 'uz')
                
                await display_application(callback.message, applications[new_index], new_index, len(applications), lang)
            else:
                await callback.answer("Oxirgi ariza", show_alert=True)
            
        except Exception as e:
            logger.error(f"Error showing next application: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_back_to_apps")
    async def back_to_applications(callback: CallbackQuery, state: FSMContext):
        """Go back to applications menu"""
        try:
            await callback.answer()
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Show applications filter menu
            keyboard = get_manager_view_applications_keyboard(lang)
            
            if lang == 'uz':
                text = "📋 <b>Arizalar</b>\n\nQaysi arizalarni ko'rmoqchisiz?"
            else:
                text = "📋 <b>Заявки</b>\n\nКакие заявки вы хотите посмотреть?"
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error going back to applications: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    return router

async def display_application(message: Message, application: dict, current_index: int, total_count: int, lang: str):
    """Display application details"""
    try:
        # Status emoji
        status_emoji = {
            'new': '🆕',
            'active': '⏳',
            'completed': '✅',
            'cancelled': '❌'
        }.get(application['status'], '❓')
        
        # Priority emoji
        priority_emoji = {
            'low': '🟢',
            'normal': '🟡',
            'high': '🔴',
            'urgent': '🚨'
        }.get(application['priority'], '🟡')
        
        # Type emoji
        type_emoji = {
            'connection': '🔌',
            'technical': '🔧'
        }.get(application['type'], '📋')
        
        # Format text
        if lang == 'uz':
            text = f"""📋 <b>Ariza ma'lumotlari {current_index + 1}/{total_count}</b>

{status_emoji} <b>Status:</b> {application['status']}
{priority_emoji} <b>Muhimlik:</b> {application['priority']}
{type_emoji} <b>Tur:</b> {application['type']}

🆔 <b>ID:</b> {application['id']}
👤 <b>Mijoz:</b> {application['client_name']}
📱 <b>Telefon:</b> {application['contact_info']['phone']}
📍 <b>Manzil:</b> {application['address']}
📅 <b>Sana:</b> {application['created_date']}
📝 <b>Tavsif:</b> {application['description']}"""
        else:
            text = f"""📋 <b>Информация о заявке {current_index + 1}/{total_count}</b>

{status_emoji} <b>Статус:</b> {application['status']}
{priority_emoji} <b>Приоритет:</b> {application['priority']}
{type_emoji} <b>Тип:</b> {application['type']}

🆔 <b>ID:</b> {application['id']}
👤 <b>Клиент:</b> {application['client_name']}
📱 <b>Телефон:</b> {application['contact_info']['phone']}
📍 <b>Адрес:</b> {application['address']}
📅 <b>Дата:</b> {application['created_date']}
📝 <b>Описание:</b> {application['description']}"""
        
        # Create navigation keyboard
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущий",
                    callback_data="mgr_app_prev"
                ),
                InlineKeyboardButton(
                    text="Keyingi ➡️" if lang == 'uz' else "Следующий ➡️",
                    callback_data="mgr_app_next"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                    callback_data="mgr_back_to_apps"
                )
            ]
        ])
        
        await message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Error displaying application: {e}")
        await message.answer("❌ Xatolik yuz berdi") 