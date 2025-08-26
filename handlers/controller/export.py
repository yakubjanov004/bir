"""
Controller Export Handler - Mock Data Implementation
Handles data export functionality for controllers with mock data
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from keyboards.controllers_buttons import get_controller_main_keyboard
from states.controller_states import ControllerMainMenuStates
from filters.role_filter import RoleFilter
import logging
import csv
import json
import io
from typing import List, Dict, Any

# Mock data storage
mock_users = {
    123456789: {
        'id': 1,
        'telegram_id': 123456789,
        'role': 'controller',
        'language': 'uz',
        'full_name': 'Test Controller',
        'phone_number': '+998901234567',
        'region': 'toshkent'
    }
}

mock_orders = [
    {
        'id': 'ORD_001_2024_01_15',
        'current_status': 'pending_assignment',
        'priority': 'high',
        'client_name': 'Aziz Karimov',
        'contact_info': {'phone': '+998901234567'},
        'location': 'Tashkent, Chorsu tumani, 15-uy',
        'created_at': datetime.now() - timedelta(hours=2),
        'workflow_type': 'connection_request'
    },
    {
        'id': 'ORD_002_2024_01_16',
        'current_status': 'assigned_to_technician',
        'priority': 'medium',
        'client_name': 'Malika Toshmatova',
        'contact_info': {'phone': '+998901234568'},
        'location': 'Tashkent, Yunusabad tumani, 25-uy',
        'created_at': datetime.now() - timedelta(hours=5),
        'workflow_type': 'technical_service'
    },
    {
        'id': 'ORD_003_2024_01_17',
        'current_status': 'work_in_progress',
        'priority': 'low',
        'client_name': 'Jahongir Azimov',
        'contact_info': {'phone': '+998901234569'},
        'location': 'Tashkent, Chilanzor tumani, 8-uy',
        'created_at': datetime.now() - timedelta(hours=8),
        'workflow_type': 'connection_request'
    },
    {
        'id': 'ORD_004_2024_01_18',
        'current_status': 'completed',
        'priority': 'high',
        'client_name': 'Dilfuza Karimova',
        'contact_info': {'phone': '+998901234570'},
        'location': 'Tashkent, Zangiota tumani, 12-uy',
        'created_at': datetime.now() - timedelta(days=1),
        'workflow_type': 'technical_service'
    },
    {
        'id': 'ORD_005_2024_01_19',
        'current_status': 'completed',
        'priority': 'medium',
        'client_name': 'Rustam Toshmatov',
        'contact_info': {'phone': '+998901234571'},
        'location': 'Tashkent, Sergeli tumani, 30-uy',
        'created_at': datetime.now() - timedelta(days=2),
        'workflow_type': 'connection_request'
    }
]

mock_technicians = [
    {
        'id': 2001,
        'full_name': 'Ahmad Texnik',
        'phone': '+998901234572',
        'specialization': 'Internet',
        'status': 'active'
    },
    {
        'id': 2002,
        'full_name': 'Bakhtiyor Texnik',
        'phone': '+998901234573',
        'specialization': 'TV',
        'status': 'active'
    },
    {
        'id': 2003,
        'full_name': 'Davron Texnik',
        'phone': '+998901234574',
        'specialization': 'General',
        'status': 'active'
    },
    {
        'id': 2004,
        'full_name': 'Eldor Texnik',
        'phone': '+998901234575',
        'specialization': 'Internet',
        'status': 'available'
    }
]

mock_workload = [
    {
        'id': 2001,
        'assigned_count': 3,
        'in_progress_count': 2,
        'completed_today': 1
    },
    {
        'id': 2002,
        'assigned_count': 2,
        'in_progress_count': 1,
        'completed_today': 1
    },
    {
        'id': 2003,
        'assigned_count': 1,
        'in_progress_count': 1,
        'completed_today': 0
    },
    {
        'id': 2004,
        'assigned_count': 0,
        'in_progress_count': 0,
        'completed_today': 0
    }
]

# Mock database functions
async def get_user_by_telegram_id(region: str, telegram_id: int):
    """Mock get user by telegram ID"""
    print(f"Mock: Getting user by telegram ID {telegram_id} in region {region}")
    return mock_users.get(telegram_id)

async def get_available_technicians(region: str):
    """Mock get available technicians"""
    print(f"Mock: Getting available technicians in region {region}")
    return mock_technicians

async def get_controller_monitoring_stats(region: str, controller_id: int):
    """Mock get controller monitoring stats"""
    print(f"Mock: Getting monitoring stats for controller {controller_id} in region {region}")
    return {
        'total_orders': len(mock_orders),
        'success_rate': 85,
        'avg_response_time': '2.5 hours'
    }

async def get_controller_requests(region: str, controller_id: int):
    """Mock get controller requests"""
    print(f"Mock: Getting requests for controller {controller_id} in region {region}")
    return mock_orders

async def get_controller_dashboard_stats(region: str):
    """Mock get controller dashboard stats"""
    print(f"Mock: Getting dashboard stats for region {region}")
    
    pending = len([o for o in mock_orders if o['current_status'] == 'pending_assignment'])
    active = len([o for o in mock_orders if o['current_status'] in ['assigned_to_technician', 'work_in_progress']])
    completed_today = len([o for o in mock_orders if o['current_status'] == 'completed' and o['created_at'].date() == datetime.now().date()])
    active_techs = len([t for t in mock_technicians if t['status'] == 'active'])
    
    return {
        'pending_assignment': pending,
        'active_work': active,
        'completed_today': completed_today,
        'active_technicians': active_techs
    }

async def get_technician_workload(region: str):
    """Mock get technician workload"""
    print(f"Mock: Getting technician workload for region {region}")
    return mock_workload

async def get_requests_by_status(region: str, status: str):
    """Mock get requests by status"""
    print(f"Mock: Getting requests with status {status} in region {region}")
    return [o for o in mock_orders if o['current_status'] == status]

# Mock audit logger
class MockAuditLogger:
    async def log_action(self, user_id: int, action: str, details: dict = None, region: str = None, entity_type: str = None, entity_id: str = None):
        print(f"Mock Audit: User {user_id} performed {action} in region {region}")
        if details:
            print(f"Mock Audit Details: {details}")

audit_logger = MockAuditLogger()

# Mock get user region function
async def get_user_region(telegram_id: int):
    """Mock get user region"""
    print(f"Mock: Getting region for user {telegram_id}")
    user = mock_users.get(telegram_id)
    return user.get('region') if user else 'toshkent'

logger = logging.getLogger(__name__)

def get_available_export_types(role: str) -> List[str]:
    """Get available export types for role"""
    if role == 'controller':
        return ['orders', 'statistics', 'users', 'reports', 'quality']
    return []

def get_available_export_formats() -> List[str]:
    """Get available export formats"""
    return ['csv', 'json', 'txt']

async def create_export_file(region: str, controller_id: int, export_type: str, format_type: str, lang: str = 'uz') -> BufferedInputFile:
    """Create export file with mock data"""
    try:
        if export_type == 'orders':
            # Get orders data from mock data
            orders = await get_controller_requests(region, controller_id)
            data = []
            
            for order in orders:
                data.append({
                    'ID': order.get('id'),
                    'Status': order.get('current_status'),
                    'Priority': order.get('priority'),
                    'Client': order.get('client_name', 'N/A'),
                    'Phone': order.get('contact_info', {}).get('phone', 'N/A'),
                    'Location': order.get('location', 'N/A'),
                    'Created': str(order.get('created_at', '')),
                    'Type': order.get('workflow_type', 'unknown')
                })
        
        elif export_type == 'statistics':
            # Get statistics from mock data
            stats = await get_controller_dashboard_stats(region)
            monitoring_stats = await get_controller_monitoring_stats(region, controller_id)
            
            data = [{
                'Metric': 'Pending Assignment',
                'Value': stats.get('pending_assignment', 0)
            }, {
                'Metric': 'Active Work',
                'Value': stats.get('active_work', 0)
            }, {
                'Metric': 'Completed Today',
                'Value': stats.get('completed_today', 0)
            }, {
                'Metric': 'Active Technicians',
                'Value': stats.get('active_technicians', 0)
            }, {
                'Metric': 'Total Orders',
                'Value': monitoring_stats.get('total_orders', 0) if monitoring_stats else 0
            }, {
                'Metric': 'Success Rate',
                'Value': f"{monitoring_stats.get('success_rate', 0)}%" if monitoring_stats else "0%"
            }]
        
        elif export_type == 'users':
            # Get technicians data from mock data
            technicians = await get_available_technicians(region)
            workload = await get_technician_workload(region)
            
            # Merge workload data with technicians
            workload_map = {w['id']: w for w in workload}
            
            data = []
            for tech in technicians:
                tech_id = tech.get('id')
                wl = workload_map.get(tech_id, {})
                
                data.append({
                    'ID': tech_id,
                    'Name': tech.get('full_name', 'N/A'),
                    'Phone': tech.get('phone', 'N/A'),
                    'Specialization': tech.get('specialization', 'General'),
                    'Assigned': wl.get('assigned_count', 0),
                    'In Progress': wl.get('in_progress_count', 0),
                    'Completed Today': wl.get('completed_today', 0),
                    'Status': 'Active' if wl.get('assigned_count', 0) > 0 else 'Available'
                })
        
        elif export_type == 'reports':
            # Get comprehensive report data
            orders = await get_controller_requests(region, controller_id)
            stats = await get_controller_dashboard_stats(region)
            
            # Calculate report metrics
            total = len(orders)
            completed = len([o for o in orders if o.get('current_status') == 'completed'])
            pending = len([o for o in orders if o.get('current_status') == 'pending_assignment'])
            in_progress = len([o for o in orders if o.get('current_status') in ['assigned_to_technician', 'work_in_progress']])
            
            data = [{
                'Report Date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'Total Orders': total,
                'Completed': completed,
                'Pending': pending,
                'In Progress': in_progress,
                'Completion Rate': f"{(completed/max(total, 1)*100):.1f}%",
                'Active Technicians': stats.get('active_technicians', 0),
                'Today Completed': stats.get('completed_today', 0)
            }]
        
        elif export_type == 'quality':
            # Get quality control data
            orders = await get_controller_requests(region, controller_id)
            
            # Calculate quality metrics
            total = len(orders)
            on_time = 0
            delayed = 0
            
            for order in orders:
                created_at = order.get('created_at')
                updated_at = order.get('updated_at')
                
                if created_at and updated_at:
                    if isinstance(created_at, str):
                        created_at = datetime.fromisoformat(created_at)
                    if isinstance(updated_at, str):
                        updated_at = datetime.fromisoformat(updated_at)
                    
                    duration = (updated_at - created_at).total_seconds() / 3600  # hours
                    if duration <= 24:
                        on_time += 1
                    else:
                        delayed += 1
            
            data = [{
                'Metric': 'Total Requests',
                'Value': total
            }, {
                'Metric': 'On Time',
                'Value': on_time
            }, {
                'Metric': 'Delayed',
                'Value': delayed
            }, {
                'Metric': 'On Time Rate',
                'Value': f"{(on_time/max(total, 1)*100):.1f}%"
            }, {
                'Metric': 'Average Response Time',
                'Value': '2.5 hours'  # Can be calculated from actual data
            }]
        
        else:
            data = []
        
        # Format data based on file format
        if format_type == 'csv':
            output = io.StringIO()
            if data:
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            content = output.getvalue().encode('utf-8')
            filename = f"controller_{export_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        elif format_type == 'json':
            content = json.dumps(data, indent=2, ensure_ascii=False, default=str).encode('utf-8')
            filename = f"controller_{export_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        else:  # txt
            lines = []
            if data:
                for item in data:
                    lines.append('-' * 40)
                    for key, value in item.items():
                        lines.append(f"{key}: {value}")
                lines.append('-' * 40)
            content = '\n'.join(lines).encode('utf-8')
            filename = f"controller_{export_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        return BufferedInputFile(content, filename=filename)
        
    except Exception as e:
        logger.error(f"Error creating export file: {e}")
        # Return empty file on error
        content = b"Error creating export file"
        filename = f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        return BufferedInputFile(content, filename=filename)

def get_controller_export_router():
    """Controller export router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("controller")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📤 Export", "📤 Экспорт"]))
    async def export_menu_handler(message: Message, state: FSMContext):
        """Export menu handler"""
        try:
            # Get region
            region = await get_user_region(message.from_user.id)
            if not region:
                await message.answer("❌ Region aniqlanmadi")
                return
            
            user = await get_user_by_telegram_id(region, message.from_user.id)
            if not user or user['role'] != 'controller':
                await message.answer("Sizda controller huquqi yo'q.")
                return
            
            lang = user.get('language', 'uz')
            controller_id = user['id']
            
            # Store region and controller_id in state
            await state.update_data(
                region=region,
                controller_id=controller_id,
                lang=lang
            )
            
            # Log action
            await audit_logger.log_action(
                user_id=message.from_user.id,
                action='CONTROLLER_ACTION',
                details={'action': 'opened_export_menu'},
                region=region
            )
            
            export_types = get_available_export_types('controller')
            
            # Export type names
            export_type_names = {
                'uz': {
                    'orders': '📑 Buyurtmalar',
                    'statistics': '📊 Statistika',
                    'users': '👥 Texniklar',
                    'reports': '📋 Hisobotlar',
                    'quality': '🎯 Sifat nazorati'
                },
                'ru': {
                    'orders': '📑 Заказы',
                    'statistics': '📊 Статистика',
                    'users': '👥 Техники',
                    'reports': '📋 Отчеты',
                    'quality': '🎯 Контроль качества'
                }
            }
            
            text = "📤 <b>Export qilish</b>\n\nQaysi ma'lumotlarni export qilmoqchisiz?" if lang == 'uz' else "📤 <b>Экспорт</b>\n\nКакие данные вы хотите экспортировать?"
            
            # Create inline keyboard for export types
            keyboard = []
            for export_type in export_types:
                keyboard.append([
                    InlineKeyboardButton(
                        text=export_type_names[lang].get(export_type, export_type),
                        callback_data=f"controller_export_{export_type}"
                    )
                ])
            
            keyboard.append([
                InlineKeyboardButton(
                    text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад", 
                    callback_data="controller_export_back_main"
                )
            ])
            
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await message.answer(text, reply_markup=markup, parse_mode='HTML')
            await state.set_state(ControllerMainMenuStates.export_selection)
            
        except Exception as e:
            logger.error(f"Error in controller export handler: {e}")
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("controller_export_"))
    async def handle_export_selection(callback: CallbackQuery, state: FSMContext):
        """Handle export type selection"""
        try:
            await callback.answer()
            
            # Get user data from state
            user_data = await state.get_data()
            lang = user_data.get('lang', 'uz')
            region = user_data.get('region')
            controller_id = user_data.get('controller_id')
            
            if not region or not controller_id:
                await callback.answer("Session expired. Please try again.", show_alert=True)
                return
            
            # Parse callback data
            action = callback.data.replace("controller_export_", "")
            
            # Handle back to main menu
            if action == "back_main":
                await callback.message.delete()
                await callback.message.answer(
                    "🏠 Bosh menyu" if lang == 'uz' else "🏠 Главное меню",
                    reply_markup=get_controller_main_keyboard(lang)
                )
                await state.set_state(ControllerMainMenuStates.main_menu)
                return
            
            # Handle back to export types
            if action == "back_types":
                export_types = get_available_export_types('controller')
                export_type_names = {
                    'uz': {
                        'orders': '📑 Buyurtmalar',
                        'statistics': '📊 Statistika',
                        'users': '👥 Texniklar',
                        'reports': '📋 Hisobotlar',
                        'quality': '🎯 Sifat nazorati'
                    },
                    'ru': {
                        'orders': '📑 Заказы',
                        'statistics': '📊 Статистика',
                        'users': '👥 Техники',
                        'reports': '📋 Отчеты',
                        'quality': '🎯 Контроль качества'
                    }
                }
                
                text = "📤 <b>Export qilish</b>\n\nQaysi ma'lumotlarni export qilmoqchisiz?" if lang == 'uz' else "📤 <b>Экспорт</b>\n\nКакие данные вы хотите экспортировать?"
                
                keyboard = []
                for export_type in export_types:
                    keyboard.append([
                        InlineKeyboardButton(
                            text=export_type_names[lang].get(export_type, export_type),
                            callback_data=f"controller_export_{export_type}"
                        )
                    ])
                
                keyboard.append([
                    InlineKeyboardButton(
                        text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                        callback_data="controller_export_back_main"
                    )
                ])
                
                markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
                await callback.message.edit_text(text, reply_markup=markup, parse_mode='HTML')
                await state.set_state(ControllerMainMenuStates.export_selection)
                return
            
            # Check if it's a valid export type
            available_types = get_available_export_types('controller')
            if action not in available_types:
                await callback.answer("❌ Noto'g'ri export turi" if lang == 'uz' else "❌ Неверный тип экспорта", show_alert=True)
                return
            
            # Store selected export type
            await state.update_data(selected_export_type=action)
            
            # Export type names
            export_type_names = {
                'uz': {
                    'orders': 'Buyurtmalar',
                    'statistics': 'Statistika',
                    'users': 'Texniklar',
                    'reports': 'Hisobotlar',
                    'quality': 'Sifat nazorati'
                },
                'ru': {
                    'orders': 'Заказы',
                    'statistics': 'Статистика',
                    'users': 'Техники',
                    'reports': 'Отчеты',
                    'quality': 'Контроль качества'
                }
            }
            
            selected_name = export_type_names[lang].get(action, action)
            
            # Ask for format selection
            text = f"📤 <b>{selected_name}</b>\n\nQaysi formatda export qilmoqchisiz?" if lang == 'uz' else f"📤 <b>{selected_name}</b>\n\nВ каком формате экспортировать?"
            
            formats = get_available_export_formats()
            keyboard = []
            
            for format_type in formats:
                keyboard.append([
                    InlineKeyboardButton(
                        text=f"📄 {format_type.upper()}",
                        callback_data=f"controller_format_{format_type}"
                    )
                ])
            
            keyboard.append([
                InlineKeyboardButton(
                    text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                    callback_data="controller_export_back_types"
                )
            ])
            
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            await callback.message.edit_text(text, reply_markup=markup, parse_mode='HTML')
            await state.set_state(ControllerMainMenuStates.export_format_selection)
            
        except Exception as e:
            logger.error(f"Error in handle_export_selection: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("controller_format_"))
    async def handle_format_selection(callback: CallbackQuery, state: FSMContext):
        """Handle export format selection"""
        try:
            await callback.answer("📥 Fayl tayyorlanmoqda...")
            
            # Get user data from state
            user_data = await state.get_data()
            lang = user_data.get('lang', 'uz')
            region = user_data.get('region')
            controller_id = user_data.get('controller_id')
            selected_export_type = user_data.get('selected_export_type')
            
            if not region or not controller_id or not selected_export_type:
                await callback.answer("Session expired. Please try again.", show_alert=True)
                return
            
            # Parse format type
            format_type = callback.data.replace("controller_format_", "")
            
            # Create export file with mock data
            export_file = await create_export_file(
                region=region,
                controller_id=controller_id,
                export_type=selected_export_type,
                format_type=format_type,
                lang=lang
            )
            
            # Log export action
            await audit_logger.log_action(
                user_id=callback.from_user.id,
                action='DATA_EXPORTED',
                details={
                    'export_type': selected_export_type,
                    'format': format_type,
                    'role': 'controller'
                },
                region=region
            )
            
            # Send file to user
            caption = f"✅ Export tayyor!\n\n📊 Turi: {selected_export_type}\n📄 Format: {format_type.upper()}\n🕐 Vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M')}" if lang == 'uz' else f"✅ Экспорт готов!\n\n📊 Тип: {selected_export_type}\n📄 Формат: {format_type.upper()}\n🕐 Время: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            await callback.message.answer_document(
                document=export_file,
                caption=caption
            )
            
            # Show success message
            success_text = "✅ <b>Export muvaffaqiyatli yakunlandi!</b>\n\nFayl yuborildi." if lang == 'uz' else "✅ <b>Экспорт успешно завершен!</b>\n\nФайл отправлен."
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="📤 Boshqa export" if lang == 'uz' else "📤 Другой экспорт",
                    callback_data="controller_export_back_types"
                )],
                [InlineKeyboardButton(
                    text="🏠 Bosh menyu" if lang == 'uz' else "🏠 Главное меню",
                    callback_data="controller_export_back_main"
                )]
            ])
            
            await callback.message.edit_text(success_text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error in handle_format_selection: {e}")
            await callback.answer("❌ Export qilishda xatolik", show_alert=True)
            await callback.message.edit_text(
                "❌ Export qilishda xatolik yuz berdi. Qaytadan urinib ko'ring." if lang == 'uz' else "❌ Произошла ошибка при экспорте. Попробуйте снова."
            )

    return router