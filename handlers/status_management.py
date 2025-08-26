"""
Manager Status Management Handler - Mock Data Version

Bu modul manager uchun ariza statuslarini boshqarish funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, database kerak emas.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime
import logging
import json
from typing import List, Dict, Any, Optional

from keyboards.manager_buttons import (
    get_status_keyboard, 
    get_manager_main_keyboard,
    get_status_management_keyboard,
    get_status_navigation_keyboard,
    get_status_confirmation_keyboard
)
from states.manager_states import ManagerStatusStates

logger = logging.getLogger(__name__)

# Mock data for applications with statuses
MOCK_APPLICATIONS = [
    {
        'id': 'APP001',
        'client_name': 'Aziz Karimov',
        'status': 'created',
        'priority': 'high',
        'type': 'connection',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'assigned_to': None,
        'region': 'toshkent',
        'description': 'Internet ulanish so\'rovi'
    },
    {
        'id': 'APP002',
        'client_name': 'Malika Yusupova',
        'status': 'assigned',
        'priority': 'urgent',
        'type': 'technical',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'assigned_to': 'Technician 1',
        'region': 'toshkent',
        'description': 'Internet tezligi past'
    },
    {
        'id': 'APP003',
        'client_name': 'Jasur Toshmatov',
        'status': 'in_progress',
        'priority': 'normal',
        'type': 'connection',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'assigned_to': 'Technician 2',
        'region': 'toshkent',
        'description': 'Yangi uy uchun internet'
    },
    {
        'id': 'APP004',
        'client_name': 'Dilfuza Rahimova',
        'status': 'pending',
        'priority': 'urgent',
        'type': 'technical',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'assigned_to': 'Technician 3',
        'region': 'toshkent',
        'description': 'Router muammosi'
    },
    {
        'id': 'APP005',
        'client_name': 'Rustam Alimov',
        'status': 'completed',
        'priority': 'low',
        'type': 'connection',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'assigned_to': 'Technician 1',
        'region': 'toshkent',
        'description': 'Ofis uchun internet'
    },
    {
        'id': 'APP006',
        'client_name': 'Zarina Karimova',
        'status': 'cancelled',
        'priority': 'high',
        'type': 'technical',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'assigned_to': None,
        'region': 'toshkent',
        'description': 'Internet uzilishi'
    }
]

# Status workflow configuration
STATUS_WORKFLOW = {
    'created': ['assigned', 'cancelled'],
    'assigned': ['in_progress', 'transferred', 'cancelled'],
    'in_progress': ['completed', 'pending', 'cancelled'],
    'pending': ['in_progress', 'cancelled'],
    'completed': [],  # Terminal state
    'cancelled': ['created'],  # Can reopen
    'transferred': ['assigned', 'in_progress'],
}

# Status display names
STATUS_DISPLAY = {
    'uz': {
        'created': '🆕 Yangi',
        'assigned': '👤 Tayinlangan',
        'in_progress': '⏳ Jarayonda',
        'pending': '⏸️ Kutilmoqda',
        'completed': '✅ Bajarilgan',
        'cancelled': '❌ Bekor qilingan',
        'transferred': '↔️ O\'tkazilgan'
    },
    'ru': {
        'created': '🆕 Новая',
        'assigned': '👤 Назначена',
        'in_progress': '⏳ В процессе',
        'pending': '⏸️ Ожидание',
        'completed': '✅ Выполнена',
        'cancelled': '❌ Отменена',
        'transferred': '↔️ Передана'
    }
}

def get_status_statistics_mock(region: str = 'toshkent') -> Dict[str, Any]:
    """Get status statistics from mock data"""
    try:
        # Filter applications by region
        applications = [app for app in MOCK_APPLICATIONS if app['region'] == region]
        
        # Count by status
        status_counts = {}
        for status in ['created', 'assigned', 'in_progress', 'pending', 'completed', 'cancelled']:
            status_counts[status] = len([app for app in applications if app['status'] == status])
        
        # Calculate percentages
        total = sum(status_counts.values())
        if total > 0:
            for status in status_counts:
                status_counts[f'{status}_percent'] = round((status_counts[status] / total) * 100, 1)
        
        return {
            'status_counts': status_counts,
            'total_applications': total,
            'region': region
        }
        
    except Exception as e:
        logger.error(f"Error getting mock status statistics: {e}")
        return {
            'status_counts': {},
            'total_applications': 0,
            'region': region
        }

def get_applications_by_status_mock(status: str, region: str = 'toshkent') -> List[Dict[str, Any]]:
    """Get applications by status from mock data"""
    try:
        applications = [app for app in MOCK_APPLICATIONS if app['status'] == status and app['region'] == region]
        return applications
    except Exception as e:
        logger.error(f"Error getting mock applications by status: {e}")
        return []

def update_application_status_mock(app_id: str, new_status: str, region: str = 'toshkent') -> bool:
    """Update application status in mock data"""
    try:
        # Find application
        app = next((app for app in MOCK_APPLICATIONS if app['id'] == app_id and app['region'] == region), None)
        if app:
            # Check if status change is valid
            current_status = app['status']
            if new_status in STATUS_WORKFLOW.get(current_status, []):
                app['status'] = new_status
                app['updated_at'] = datetime.now()
                return True
        return False
    except Exception as e:
        logger.error(f"Error updating mock application status: {e}")
        return False

def get_manager_status_management_router():
    """Router for status management with mock data"""
    router = Router()
    
    @router.message(F.text.in_(["🔄 Status o'zgartirish", "🔄 Изменить статус"])) 
    async def show_status_management_menu(message: Message, state: FSMContext):
        """Show status management menu"""
        try:
            # Mock user info
            mock_user = {
                'id': message.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Get status statistics
            stats = get_status_statistics_mock('toshkent')
            status_counts = stats['status_counts']
            
            if lang == 'uz':
                text = f"""🔄 <b>Status boshqarish</b>

📊 <b>Joriy holat:</b>
• Jami arizalar: {stats['total_applications']}

📈 <b>Status taqsimoti:</b>
• 🆕 Yangi: {status_counts.get('created', 0)} ({status_counts.get('created_percent', 0)}%)
• 👤 Tayinlangan: {status_counts.get('assigned', 0)} ({status_counts.get('assigned_percent', 0)}%)
• ⏳ Jarayonda: {status_counts.get('in_progress', 0)} ({status_counts.get('in_progress_percent', 0)}%)
• ⏸️ Kutilmoqda: {status_counts.get('pending', 0)} ({status_counts.get('pending_percent', 0)}%)
• ✅ Bajarilgan: {status_counts.get('completed', 0)} ({status_counts.get('completed_percent', 0)}%)
• ❌ Bekor: {status_counts.get('cancelled', 0)} ({status_counts.get('cancelled_percent', 0)}%)

Quyidagi bo'limlardan birini tanlang:"""
            else:
                text = f"""🔄 <b>Управление статусами</b>

📊 <b>Текущее состояние:</b>
• Всего заявок: {stats['total_applications']}

📈 <b>Распределение статусов:</b>
• 🆕 Новая: {status_counts.get('created', 0)} ({status_counts.get('created_percent', 0)}%)
• 👤 Назначена: {status_counts.get('assigned', 0)} ({status_counts.get('assigned_percent', 0)}%)
• ⏳ В процессе: {status_counts.get('in_progress', 0)} ({status_counts.get('in_progress_percent', 0)}%)
• ⏸️ Ожидание: {status_counts.get('pending', 0)} ({status_counts.get('pending_percent', 0)}%)
• ✅ Выполнена: {status_counts.get('completed', 0)} ({status_counts.get('completed_percent', 0)}%)
• ❌ Отменена: {status_counts.get('cancelled', 0)} ({status_counts.get('cancelled_percent', 0)}%)

Выберите один из следующих разделов:"""
            
            # Create status management keyboard
            keyboard = get_status_management_keyboard(lang)
            
            await message.answer(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error showing status management menu: {e}")
            await message.answer("❌ Xatolik yuz berdi")
    
    @router.callback_query(F.data == "mgr_status_change")
    async def show_status_change_menu(callback: CallbackQuery, state: FSMContext):
        """Show status change menu"""
        try:
            await callback.answer()
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            if lang == 'uz':
                text = """🔄 <b>Status o'zgartirish</b>

Qaysi statusdagi arizalarni ko'rmoqchisiz?

Statusni tanlang:"""
            else:
                text = """🔄 <b>Изменение статуса</b>

Какие заявки вы хотите просмотреть?

Выберите статус:"""
            
            # Create status selection keyboard
            buttons = []
            for status, display_name in STATUS_DISPLAY[lang].items():
                count = len(get_applications_by_status_mock(status, 'toshkent'))
                if count > 0:
                    buttons.append([InlineKeyboardButton(
                        text=f"{display_name} ({count})",
                        callback_data=f"mgr_status_select_{status}"
                    )])
            
            # Add back button
            buttons.append([InlineKeyboardButton(
                text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                callback_data="mgr_status_management"
            )])
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error showing status change menu: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("mgr_status_select_"))
    async def select_status_for_change(callback: CallbackQuery, state: FSMContext):
        """Select status for change"""
        try:
            await callback.answer()
            
            # Extract status
            status = callback.data.replace("mgr_status_select_", "")
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Get applications with this status
            applications = get_applications_by_status_mock(status, 'toshkent')
            
            if not applications:
                if lang == 'uz':
                    text = f"📭 {STATUS_DISPLAY[lang][status]} statusdagi arizalar topilmadi"
                else:
                    text = f"📭 Заявки со статусом {STATUS_DISPLAY[lang][status]} не найдены"
                
                await callback.message.edit_text(text)
                return
            
            # Show first application
            await state.update_data(
                selected_status=status,
                applications=applications,
                current_index=0
            )
            
            await display_application_for_status_change(callback.message, applications[0], 0, len(applications), lang)
            
        except Exception as e:
            logger.error(f"Error selecting status for change: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data.startswith("mgr_change_to_"))
    async def change_application_status(callback: CallbackQuery, state: FSMContext):
        """Change application status"""
        try:
            await callback.answer()
            
            # Extract new status
            new_status = callback.data.replace("mgr_change_to_", "")
            
            # Get state data
            data = await state.get_data()
            applications = data.get('applications', [])
            current_index = data.get('current_index', 0)
            selected_status = data.get('selected_status', '')
            
            if not applications or current_index >= len(applications):
                await callback.answer("❌ Ariza topilmadi", show_alert=True)
                return
            
            # Get current application
            current_app = applications[current_index]
            
            # Update status
            success = update_application_status_mock(current_app['id'], new_status, 'toshkent')
            
            if success:
                # Update local data
                current_app['status'] = new_status
                current_app['updated_at'] = datetime.now()
                
                # Mock user info
                mock_user = {
                    'id': callback.from_user.id,
                    'language': 'uz',
                    'role': 'manager'
                }
                
                lang = mock_user.get('language', 'uz')
                
                if lang == 'uz':
                    text = f"""✅ <b>Status muvaffaqiyatli o'zgartirildi!</b>

📋 <b>Ariza:</b> {current_app['id']}
👤 <b>Mijoz:</b> {current_app['client_name']}
🔄 <b>Eski status:</b> {STATUS_DISPLAY[lang][selected_status]}
✅ <b>Yangi status:</b> {STATUS_DISPLAY[lang][new_status]}
⏰ <b>O'zgartirilgan vaqt:</b> {datetime.now().strftime('%H:%M')}

Ariza endi {STATUS_DISPLAY[lang][new_status]} statusiga o'tdi."""
                else:
                    text = f"""✅ <b>Статус успешно изменен!</b>

📋 <b>Заявка:</b> {current_app['id']}
👤 <b>Клиент:</b> {current_app['client_name']}
🔄 <b>Старый статус:</b> {STATUS_DISPLAY[lang][selected_status]}
✅ <b>Новый статус:</b> {STATUS_DISPLAY[lang][new_status]}
⏰ <b>Время изменения:</b> {datetime.now().strftime('%H:%M')}

Заявка теперь перешла в статус {STATUS_DISPLAY[lang][new_status]}."""
                
                # Create success keyboard
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(
                        text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                        callback_data=f"mgr_status_select_{selected_status}"
                    )
                ]])
                
                await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
                
            else:
                await callback.answer("❌ Status o'zgartirishda xatolik", show_alert=True)
            
        except Exception as e:
            logger.error(f"Error changing application status: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "mgr_status_management")
    async def back_to_status_management(callback: CallbackQuery, state: FSMContext):
        """Go back to status management menu"""
        try:
            await callback.answer()
            
            # Clear state
            await state.clear()
            
            # Show status management menu again
            await show_status_management_menu(callback.message, state)
            
        except Exception as e:
            logger.error(f"Error going back to status management: {e}")
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

async def display_application_for_status_change(message: Message, application: dict, current_index: int, total_count: int, lang: str):
    """Display application for status change"""
    try:
        # Get current status display name
        current_status = STATUS_DISPLAY[lang].get(application['status'], application['status'])
        
        # Get available next statuses
        available_statuses = STATUS_WORKFLOW.get(application['status'], [])
        
        # Format text
        if lang == 'uz':
            text = f"""📋 <b>Ariza ma'lumotlari {current_index + 1}/{total_count}</b>

🆔 <b>ID:</b> {application['id']}
👤 <b>Mijoz:</b> {application['client_name']}
📊 <b>Joriy status:</b> {current_status}
🎯 <b>Muhimlik:</b> {application['priority']}
🔌 <b>Tur:</b> {application['type']}
📍 <b>Hudud:</b> {application['region']}
👨‍🔧 <b>Tayinlangan:</b> {application['assigned_to'] or 'Tayinlanmagan'}
📝 <b>Tavsif:</b> {application['description']}
📅 <b>Yaratilgan:</b> {application['created_at'].strftime('%H:%M')}
🔄 <b>Yangilangan:</b> {application['updated_at'].strftime('%H:%M')}

🔄 <b>Keyingi statusni tanlang:</b>"""
        else:
            text = f"""📋 <b>Информация о заявке {current_index + 1}/{total_count}</b>

🆔 <b>ID:</b> {application['id']}
👤 <b>Клиент:</b> {application['client_name']}
📊 <b>Текущий статус:</b> {current_status}
🎯 <b>Приоритет:</b> {application['priority']}
🔌 <b>Тип:</b> {application['type']}
📍 <b>Регион:</b> {application['region']}
👨‍🔧 <b>Назначен:</b> {application['assigned_to'] or 'Не назначен'}
📝 <b>Описание:</b> {application['description']}
📅 <b>Создано:</b> {application['created_at'].strftime('%H:%M')}
🔄 <b>Обновлено:</b> {application['updated_at'].strftime('%H:%M')}

🔄 <b>Выберите следующий статус:</b>"""
        
        # Create status change keyboard
        buttons = []
        for status in available_statuses:
            display_name = STATUS_DISPLAY[lang].get(status, status)
            buttons.append([InlineKeyboardButton(
                text=f"🔄 {display_name}",
                callback_data=f"mgr_change_to_{status}"
            )])
        
        # Add navigation buttons
        if total_count > 1:
            buttons.append([
                InlineKeyboardButton(
                    text="⬅️ Oldingi" if lang == 'uz' else "⬅️ Предыдущий",
                    callback_data="mgr_status_prev"
                ),
                InlineKeyboardButton(
                    text="Keyingi ➡️" if lang == 'uz' else "Следующий ➡️",
                    callback_data="mgr_status_next"
                )
            ])
        
        # Add back button
        buttons.append([InlineKeyboardButton(
            text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
            callback_data="mgr_status_change"
        )])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        await message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Error displaying application for status change: {e}")
        await message.answer("❌ Xatolik yuz berdi")
