"""
Manager Export Handler - Mock Data Implementation

Bu modul manager uchun ma'lumotlarni export qilish funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, hech qanday real database yo'q.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime
from keyboards.manager_buttons import get_manager_main_keyboard
from states.manager_states import ManagerMainMenuStates
from filters.role_filter import RoleFilter
import logging
import io
import csv
import json

logger = logging.getLogger(__name__)

# Mock data storage
mock_users = {
    1: {
        'id': 1,
        'telegram_id': 123456789,
        'role': 'manager',
        'language': 'uz',
        'full_name': 'Test Manager',
        'phone_number': '+998901234567',
        'region': 'toshkent'
    }
}

mock_orders = [
    {
        'id': 'ORD_001_2024_01_15',
        'client_name': 'Aziz Karimov',
        'client_phone': '+998901234567',
        'service_type': 'Internet',
        'status': 'Completed',
        'created_at': '2024-01-15 10:30:00',
        'completed_at': '2024-01-17 14:20:00',
        'amount': 150000,
        'region': 'toshkent'
    },
    {
        'id': 'ORD_002_2024_01_16',
        'client_name': 'Malika Toshmatova',
        'client_phone': '+998901234568',
        'service_type': 'TV',
        'status': 'In Progress',
        'created_at': '2024-01-16 09:15:00',
        'completed_at': None,
        'amount': 100000,
        'region': 'toshkent'
    },
    {
        'id': 'ORD_003_2024_01_17',
        'client_name': 'Jahongir Azimov',
        'client_phone': '+998901234569',
        'service_type': 'Combo',
        'status': 'Pending',
        'created_at': '2024-01-17 11:45:00',
        'completed_at': None,
        'amount': 250000,
        'region': 'toshkent'
    }
]

mock_statistics = {
    'total_orders': 156,
    'completed_orders': 89,
    'pending_orders': 45,
    'cancelled_orders': 22,
    'total_revenue': 23450000,
    'avg_order_value': 150320,
    'completion_rate': 57.1,
    'monthly_growth': 12.5
}

mock_staff = [
    {
        'id': 1,
        'full_name': 'Ahmad Karimov',
        'role': 'Manager',
        'phone': '+998901234567',
        'email': 'ahmad@example.com',
        'status': 'Active',
        'hire_date': '2023-01-15',
        'region': 'toshkent'
    },
    {
        'id': 2,
        'full_name': 'Malika Toshmatova',
        'role': 'Technician',
        'phone': '+998901234568',
        'email': 'malika@example.com',
        'status': 'Active',
        'hire_date': '2023-03-20',
        'region': 'toshkent'
    },
    {
        'id': 3,
        'full_name': 'Umar Azimov',
        'role': 'Call Center',
        'phone': '+998901234569',
        'email': 'umar@example.com',
        'status': 'Active',
        'hire_date': '2023-06-10',
        'region': 'toshkent'
    }
]

mock_reports = [
    {
        'id': 'REP_001_2024_01',
        'title': 'January 2024 Performance Report',
        'type': 'Monthly',
        'created_at': '2024-01-31 23:59:00',
        'status': 'Completed',
        'data_points': 45,
        'region': 'toshkent'
    },
    {
        'id': 'REP_002_2024_01_15',
        'title': 'Mid-Month Service Quality Report',
        'type': 'Interim',
        'created_at': '2024-01-15 12:00:00',
        'status': 'Completed',
        'data_points': 23,
        'region': 'toshkent'
    }
]

# Mock utility classes
class MockAuditLogger:
    """Mock audit logger"""
    async def log_manager_action(self, manager_id: int, action: str, target_type: str = None, target_id: str = None, details: dict = None):
        """Mock log manager action"""
        logger.info(f"Mock: Manager {manager_id} performed action: {action}")
        if target_type and target_id:
            logger.info(f"Mock: Target: {target_type} {target_id}")
        if details:
            logger.info(f"Mock: Details: {details}")

# Initialize mock instances
audit_logger = MockAuditLogger()

# Mock export utility functions
def get_available_export_types(role: str):
    """Mock get available export types"""
    return ['orders', 'statistics', 'users', 'reports']

def get_available_export_formats():
    """Mock get available export formats"""
    return ['csv', 'xlsx', 'docx', 'pdf']

def create_export_file(export_type: str, format_type: str, role: str):
    """Mock create export file"""
    # Create mock data based on export type
    if export_type == 'orders':
        data = mock_orders
    elif export_type == 'statistics':
        data = [mock_statistics]
    elif export_type == 'users':
        data = mock_staff
    elif export_type == 'reports':
        data = mock_reports
    else:
        data = []
    
    # Create file content based on format
    if format_type == 'csv':
        file_content = create_csv_content(data, export_type)
        filename = f"{export_type}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    elif format_type == 'xlsx':
        file_content = create_excel_content(data, export_type)
        filename = f"{export_type}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    elif format_type == 'docx':
        file_content = create_word_content(data, export_type)
        filename = f"{export_type}_{datetime.now().strftime('%Y%m%d_%H%M')}.docx"
    elif format_type == 'pdf':
        file_content = create_pdf_content(data, export_type)
        filename = f"{export_type}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    else:
        file_content = create_csv_content(data, export_type)
        filename = f"{export_type}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    
    return file_content, filename

def create_csv_content(data, export_type):
    """Create CSV content"""
    output = io.StringIO()
    if not data:
        output.write("No data available\n")
        output.seek(0)
        return output
    
    if export_type == 'statistics':
        # Statistics is a single dict, convert to list of key-value pairs
        writer = csv.writer(output)
        writer.writerow(['Metric', 'Value'])
        for key, value in data[0].items():
            writer.writerow([key.replace('_', ' ').title(), value])
    else:
        # Regular data with multiple records
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    output.seek(0)
    return output

def create_excel_content(data, export_type):
    """Create Excel content (simulated as CSV for mock)"""
    return create_csv_content(data, export_type)

def create_word_content(data, export_type):
    """Create Word content (simulated as text for mock)"""
    output = io.StringIO()
    output.write(f"{export_type.upper()} EXPORT REPORT\n")
    output.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    output.write("=" * 50 + "\n\n")
    
    if not data:
        output.write("No data available\n")
    else:
        for item in data:
            output.write(f"Record: {item}\n\n")
    
    output.seek(0)
    return output

def create_pdf_content(data, export_type):
    """Create PDF content (simulated as text for mock)"""
    return create_word_content(data, export_type)

# Mock user functions
async def get_user_by_telegram_id(region: str, user_id: int):
    """Mock get user by telegram ID"""
    for user in mock_users.values():
        if user.get('telegram_id') == user_id:
            return user
    return None

def get_manager_export_router():
    """Manager export router"""
    router = Router()
    
    # Apply role filter - both manager and junior_manager can access
    role_filter = RoleFilter(["manager", "junior_manager"])
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📤 Export", "📤 Экспорт"]), flags={"block": False})
    async def export_menu_handler(message: Message, state: FSMContext):
        """Export menu handler"""
        try:
            # Use hardcoded values for now
            region = 'toshkent'
            lang = 'uz'
            
            # Get user from mock data
            user = await get_user_by_telegram_id(region, message.from_user.id)
            if not user:
                await message.answer("❌ Foydalanuvchi topilmadi")
                return
            
            # Log export access using mock audit logger
            await audit_logger.log_manager_action(
                manager_id=user.get('id'),
                action='access_export_menu',
                details={'region': region}
            )
            
            export_types = get_available_export_types('manager')
            
            # Export type names
            export_type_names = {
                'uz': {
                    'orders': '📑 Buyurtmalar',
                    'statistics': '📊 Statistika',
                    'users': '👥 Xodimlar',
                    'reports': '📋 Hisobotlar'
                },
                'ru': {
                    'orders': '📑 Заказы',
                    'statistics': '📊 Статистика',
                    'users': '👥 Сотрудники',
                    'reports': '📋 Отчеты'
                }
            }
            
            text = "Export qilish\n\nQaysi ma'lumotlarni export qilmoqchisiz?"
            
            # Create inline keyboard for export types
            keyboard = []
            for export_type in export_types:
                keyboard.append([
                    InlineKeyboardButton(
                        text=export_type_names['uz'].get(export_type, export_type),
                        callback_data=f"manager_export_{export_type}"
                    )
                ])
            
            keyboard.append([
                InlineKeyboardButton(
                    text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад", 
                    callback_data="manager_export_back_main"
                )
            ])
            
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await message.answer(text, reply_markup=markup)
            await state.set_state(ManagerMainMenuStates.export_selection)
            
        except Exception as e:
            logger.error(f"Error in manager export handler: {str(e)}")
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("manager_export_"))
    async def handle_export_selection(callback: CallbackQuery, state: FSMContext):
        """Handle export type selection"""
        try:
            await callback.answer()
            
            # Use hardcoded values for now
            lang = 'uz'
            
            # Parse callback data
            action = callback.data.replace("manager_export_", "")
            
            # Handle back to main menu
            if action == "back_main":
                await callback.message.delete()
                await callback.message.answer(
                    "🏠 Bosh menyu",
                    reply_markup=get_manager_main_keyboard('uz')
                )
                await state.set_state(ManagerMainMenuStates.main_menu)
                return
            
            # Handle back to export types
            if action == "back_types":
                export_types = get_available_export_types('manager')
                export_type_names = {
                    'uz': {
                        'orders': '📑 Buyurtmalar',
                        'statistics': '📊 Statistika',
                        'users': '👥 Xodimlar',
                        'reports': '📋 Hisobotlar'
                    }
                }
                
                text = "Export qilish\n\nQaysi ma'lumotlarni export qilmoqchisiz?" if lang == 'uz' else "Экспорт\n\nКакие данные вы хотите экспортировать?"
                
                keyboard = []
                for export_type in export_types:
                    keyboard.append([
                        InlineKeyboardButton(
                            text=export_type_names[lang].get(export_type, export_type),
                            callback_data=f"manager_export_{export_type}"
                        )
                    ])
                
                keyboard.append([
                    InlineKeyboardButton(
                        text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                        callback_data="manager_export_back_main"
                    )
                ])
                
                markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
                await callback.message.edit_text(text, reply_markup=markup)
                await state.set_state(ManagerMainMenuStates.export_selection)
                return
            
            # Check if it's a valid export type
            available_types = get_available_export_types('manager')
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
                    'users': 'Xodimlar',
                    'reports': 'Hisobotlar'
                },
                'ru': {
                    'orders': 'Заказы',
                    'statistics': 'Статистика',
                    'users': 'Сотрудники',
                    'reports': 'Отчеты'
                }
            }
            
            # Show format selection
            formats = get_available_export_formats()
            text = f"{export_type_names[lang].get(action, action)} export\n\n"
            text += "Qaysi formatda export qilmoqchisiz?\n\n" if lang == 'uz' else "В каком формате экспортировать?\n\n"
            text += "CSV - Universal format (Excel, Google Sheets)\n" if lang == 'uz' else "CSV - Универсальный формат (Excel, Google Sheets)\n"
            text += "Excel - Microsoft Excel formati\n" if lang == 'uz' else "Excel - Формат Microsoft Excel\n"
            text += "Word - Microsoft Word formati\n" if lang == 'uz' else "Word - Формат Microsoft Word\n"
            text += "PDF - Chop etish uchun qulay format" if lang == 'uz' else "PDF - Удобный формат для печати"
            
            keyboard = []
            format_icons = {
                'csv': 'CSV',
                'xlsx': 'Excel',
                'docx': 'Word',
                'pdf': 'PDF'
            }
            
            for fmt in formats:
                keyboard.append([
                    InlineKeyboardButton(
                        text=format_icons.get(fmt, fmt.upper()),
                        callback_data=f"manager_format_{fmt}"
                    )
                ])
            
            # Add back button
            keyboard.append([
                InlineKeyboardButton(
                    text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад",
                    callback_data="manager_export_back_types"
                )
            ])
            
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            await callback.message.edit_text(text, reply_markup=markup)
            await state.set_state(ManagerMainMenuStates.export_format_selection)
            
        except Exception as e:
            logger.error(f"Error in export selection: {str(e)}")
            await callback.answer("❌ Xatolik yuz berdi" if lang == 'uz' else "❌ Произошла ошибка", show_alert=True)

    @router.callback_query(F.data.startswith("manager_format_"))
    async def handle_export_format(callback: CallbackQuery, state: FSMContext):
        """Handle export format selection"""
        try:
            # Get user language
            user_data = await state.get_data()
            lang = user_data.get('lang', 'uz')
            
            # Send loading message
            await callback.answer("📥 Export tayyorlanmoqda..." if lang == 'uz' else "📥 Подготовка экспорта...", show_alert=False)
            
            # Delete the inline keyboard
            await callback.message.delete()
            
            # Get format type
            format_type = callback.data.replace("manager_format_", "")
            
            # Get stored data
            export_type = user_data.get('selected_export_type')
            
            if not export_type:
                await callback.message.answer("❌ Export turi tanlanmagan" if lang == 'uz' else "❌ Тип экспорта не выбран")
                return
            
            # Export type names
            export_type_names = {
                'uz': {
                    'orders': 'Buyurtmalar',
                    'statistics': 'Statistika',
                    'users': 'Xodimlar',
                    'reports': 'Hisobotlar'
                },
                'ru': {
                    'orders': 'Заказы',
                    'statistics': 'Статистика',
                    'users': 'Сотрудники',
                    'reports': 'Отчеты'
                }
            }
            
            format_names = {
                'csv': 'CSV',
                'xlsx': 'Excel',
                'docx': 'Word',
                'pdf': 'PDF'
            }
            
            # Send processing message
            processing_msg = await callback.message.answer(
                f"⏳ {export_type_names[lang].get(export_type, export_type)} ma'lumotlari {format_names.get(format_type, format_type)} formatida tayyorlanmoqda...\n\n"
                f"Iltimos, kuting..." if lang == 'uz' else
                f"⏳ Данные {export_type_names['ru'].get(export_type, export_type)} готовятся в формате {format_names.get(format_type, format_type)}...\n\n"
                f"Пожалуйста, подождите..."
            )
            
            try:
                # Get region from state
                region = user_data.get('region', 'toshkent')
                
                # Create export file using mock function
                file_content, filename = create_export_file(export_type, format_type, "manager")
                
                # Log export action using mock audit logger
                user = await get_user_by_telegram_id(region, callback.from_user.id)
                if user:
                    await audit_logger.log_manager_action(
                        manager_id=user.get('id'),
                        action='export_data',
                        target_type=export_type,
                        details={
                            'format': format_type,
                            'filename': filename,
                            'region': region
                        }
                    )
                
                # Get file size
                file_content.seek(0, 2)  # Move to end
                file_size = file_content.tell()
                file_content.seek(0)  # Reset to beginning
                
                # Delete processing message
                await processing_msg.delete()
                
                # Send only the file with all information in caption
                await callback.message.answer_document(
                    BufferedInputFile(
                        file_content.read(),
                        filename=filename
                    ),
                    caption=(
                        f"✅ {export_type_names[lang].get(export_type, export_type)} export muvaffaqiyatli yakunlandi!\n\n"
                        f"📄 Fayl nomi: {filename}\n"
                        f"📦 Fayl hajmi: {file_size:,} bayt\n"
                        f"📊 Format: {format_names.get(format_type, format_type)}\n"
                        f"📅 Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                        f"Export muvaffaqiyatli yakunlandi!" if lang == 'uz' else
                        f"✅ Экспорт {export_type_names['ru'].get(export_type, export_type)} успешно завершен!\n\n"
                        f"📄 Имя файла: {filename}\n"
                        f"📦 Размер файла: {file_size:,} байт\n"
                        f"📊 Формат: {format_names.get(format_type, format_type)}\n"
                        f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                        f"Экспорт успешно завершен!"
                    ),
                    reply_markup=get_manager_main_keyboard(lang)
                )
                await state.set_state(ManagerMainMenuStates.main_menu)
                
            except Exception as e:
                logger.error(f"Error creating export file: {str(e)}")
                await processing_msg.delete()
                await callback.message.answer(
                    f"❌ Export jarayonida xatolik yuz berdi:\n{str(e)}\n\n"
                    f"Iltimos, qayta urinib ko'ring." if lang == 'uz' else
                    f"❌ Ошибка при экспорте:\n{str(e)}\n\n"
                    f"Пожалуйста, попробуйте еще раз.",
                    reply_markup=get_manager_main_keyboard(lang)
                )
                await state.set_state(ManagerMainMenuStates.main_menu)
            
        except Exception as e:
            logger.error(f"Error in export format handler: {str(e)}")
            await callback.message.answer(
                "❌ Export xatoligi yuz berdi" if lang == 'uz' else "❌ Ошибка экспорта",
                reply_markup=get_manager_main_keyboard(lang)
            )
            await state.set_state(ManagerMainMenuStates.main_menu)

    return router