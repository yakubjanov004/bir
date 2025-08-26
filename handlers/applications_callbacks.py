"""
Applications Callbacks Handler - Mock Data Version

Bu modul manager uchun arizalar bilan bog'liq callback funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, database kerak emas.
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from states.manager_states import ManagerApplicationStates
from keyboards.manager_buttons import (
    get_manager_main_keyboard,
    get_application_actions_keyboard,
    get_application_navigation_keyboard
)
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
    }
]

def get_manager_applications_callbacks_router():
    """Router for applications callbacks with mock data"""
    router = Router()
    
    @router.callback_query(F.data.startswith("mgr_view_app_"))
    async def view_application_details(callback: CallbackQuery, state: FSMContext):
        """View application details"""
        try:
            await callback.answer()
            
            # Extract application ID
            app_id = callback.data.replace("mgr_view_app_", "")
            
            # Find application in mock data
            application = next((app for app in MOCK_APPLICATIONS if app['id'] == app_id), None)
            
            if not application:
                await callback.answer("❌ Ariza topilmadi", show_alert=True)
                return
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
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
                text = f"""📋 <b>Ariza ma'lumotlari</b>

{status_emoji} <b>Status:</b> {application['status']}
{priority_emoji} <b>Muhimlik:</b> {application['priority']}
{type_emoji} <b>Tur:</b> {application['type']}

🆔 <b>ID:</b> {application['id']}
👤 <b>Mijoz:</b> {application['client_name']}
📱 <b>Telefon:</b> {application['contact_info']['phone']}
📍 <b>Manzil:</b> {application['address']}
📅 <b>Sana:</b> {application['created_date']}
📝 <b>Tavsif:</b> {application['description']}

Qanday amal bajarishni xohlaysiz?"""
            else:
                text = f"""📋 <b>Информация о заявке</b>

{status_emoji} <b>Статус:</b> {application['status']}
{priority_emoji} <b>Приоритет:</b> {application['priority']}
{type_emoji} <b>Тип:</b> {application['type']}

🆔 <b>ID:</b> {application['id']}
👤 <b>Клиент:</b> {application['client_name']}
📱 <b>Телефон:</b> {application['contact_info']['phone']}
📍 <b>Адрес:</b> {application['address']}
📅 <b>Дата:</b> {application['created_date']}
📝 <b>Описание:</b> {application['description']}

Какое действие вы хотите выполнить?"""
            
            # Create actions keyboard
            keyboard = get_application_actions_keyboard(application['id'], lang)
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error viewing application details: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("mgr_contact_client_"))
    async def contact_client(callback: CallbackQuery, state: FSMContext):
        """Contact client"""
        try:
            await callback.answer()
            
            # Extract application ID
            app_id = callback.data.replace("mgr_contact_client_", "")
            
            # Find application in mock data
            application = next((app for app in MOCK_APPLICATIONS if app['id'] == app_id), None)
            
            if not application:
                await callback.answer("❌ Ariza topilmadi", show_alert=True)
                return
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Format text
            if lang == 'uz':
                text = f"""📞 <b>Mijoz bilan bog'lanish</b>

👤 Mijoz: {application['client_name']}
📱 Telefon: {application['contact_info']['phone']}
📝 Ariza: {application['id']}

Mijoz bilan bog'lanish uchun yuqoridagi telefon raqamini ishlatishingiz mumkin."""
            else:
                text = f"""📞 <b>Связь с клиентом</b>

👤 Клиент: {application['client_name']}
📱 Телефон: {application['contact_info']['phone']}
📝 Заявка: {application['id']}

Для связи с клиентом используйте номер телефона выше."""
            
            # Create back keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                    callback_data=f"mgr_view_app_{app_id}"
                )
            ]])
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error contacting client: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("mgr_assign_jm_"))
    async def assign_to_junior_manager(callback: CallbackQuery, state: FSMContext):
        """Assign to junior manager"""
        try:
            await callback.answer()
            
            # Extract application ID
            app_id = callback.data.replace("mgr_assign_jm_", "")
            
            # Find application in mock data
            application = next((app for app in MOCK_APPLICATIONS if app['id'] == app_id), None)
            
            if not application:
                await callback.answer("❌ Ariza topilmadi", show_alert=True)
                return
            
            # Mock junior managers
            mock_junior_managers = [
                {'id': 1, 'full_name': 'Aziz Karimov', 'role': 'junior_manager'},
                {'id': 2, 'full_name': 'Malika Yusupova', 'role': 'junior_manager'},
                {'id': 3, 'full_name': 'Jasur Toshmatov', 'role': 'junior_manager'},
                {'id': 4, 'full_name': 'Dilfuza Rahimova', 'role': 'junior_manager'},
                {'id': 5, 'full_name': 'Rustam Alimov', 'role': 'junior_manager'}
            ]
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Format text
            if lang == 'uz':
                text = f"""👨‍💼 <b>Kichik menejer tanlang</b>

📝 Ariza ID: {application['id']}
👤 Mijoz: {application['client_name']}

Quyidagi kichik menejerlardan birini tanlang:"""
            else:
                text = f"""👨‍💼 <b>Выберите младшего менеджера</b>

📝 ID заявки: {application['id']}
👤 Клиент: {application['client_name']}

Выберите одного из следующих младших менеджеров:"""
            
            # Create junior manager selection keyboard
            buttons = []
            for jm in mock_junior_managers:
                buttons.append([InlineKeyboardButton(
                    text=f"👨‍💼 {jm['full_name']}",
                    callback_data=f"mgr_confirm_jm_{application['id']}_{jm['id']}"
                )])
            
            # Add back button
            buttons.append([InlineKeyboardButton(
                text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                callback_data=f"mgr_view_app_{app_id}"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
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
            app_id = parts[0]
            jm_id = int(parts[1])
            
            # Find application in mock data
            application = next((app for app in MOCK_APPLICATIONS if app['id'] == app_id), None)
            
            if not application:
                await callback.answer("❌ Ariza topilmadi", show_alert=True)
                return
            
            # Mock junior managers
            mock_junior_managers = [
                {'id': 1, 'full_name': 'Aziz Karimov', 'role': 'junior_manager'},
                {'id': 2, 'full_name': 'Malika Yusupova', 'role': 'junior_manager'},
                {'id': 3, 'full_name': 'Jasur Toshmatov', 'role': 'junior_manager'},
                {'id': 4, 'full_name': 'Dilfuza Rahimova', 'role': 'junior_manager'},
                {'id': 5, 'full_name': 'Rustam Alimov', 'role': 'junior_manager'}
            ]
            
            # Find junior manager
            junior_manager = next((jm for jm in mock_junior_managers if jm['id'] == jm_id), None)
            
            if not junior_manager:
                await callback.answer("❌ Kichik menejer topilmadi", show_alert=True)
                return
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Format text
            if lang == 'uz':
                text = f"""✅ <b>Tayinlash muvaffaqiyatli!</b>

📝 Ariza ID: {application['id']}
👤 Mijoz: {application['client_name']}
👨‍💼 Kichik menejer: {junior_manager['full_name']}

Ariza muvaffaqiyatli kichik menejerga yuborildi."""
            else:
                text = f"""✅ <b>Назначение успешно!</b>

📝 ID заявки: {application['id']}
👤 Клиент: {application['client_name']}
👨‍💼 Младший менеджер: {junior_manager['full_name']}

Заявка успешно отправлена младшему менеджеру."""
            
            # Create back keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                    callback_data="mgr_back_to_apps"
                )
            ]])
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error confirming junior manager assignment: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_close_app")
    async def close_application(callback: CallbackQuery, state: FSMContext):
        """Close application view"""
        try:
            await callback.answer()
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Format text
            if lang == 'uz':
                text = "📋 Ariza ko'rinishi yopildi. Asosiy menyuga qaytish uchun /start buyrug'ini ishlatishingiz mumkin."
            else:
                text = "📋 Просмотр заявки закрыт. Используйте команду /start для возврата в главное меню."
            
            await callback.message.edit_text(text)
            
        except Exception as e:
            logger.error(f"Error closing application: {e}")
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
            
            # Import and show applications filter menu
            from keyboards.manager_buttons import get_manager_view_applications_keyboard
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