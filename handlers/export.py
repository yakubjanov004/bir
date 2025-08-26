"""
Manager Export Handler - Mock Data Version

Bu modul manager uchun ma'lumotlarni export qilish funksionalligini o'z ichiga oladi.
Mock data bilan ishlaydi, database kerak emas.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime
from keyboards.manager_buttons import get_manager_main_keyboard
from states.manager_states import ManagerMainMenuStates
import logging
import json
import csv
import io

logger = logging.getLogger(__name__)

# Mock data for export
MOCK_EXPORT_DATA = {
    'orders': [
        {
            'id': 'APP001',
            'client_name': 'Aziz Karimov',
            'status': 'created',
            'priority': 'high',
            'type': 'connection',
            'created_at': '2024-01-15 10:30:00',
            'assigned_to': 'Technician 1',
            'region': 'toshkent',
            'description': 'Internet ulanish so\'rovi'
        },
        {
            'id': 'APP002',
            'client_name': 'Malika Yusupova',
            'status': 'assigned',
            'priority': 'urgent',
            'type': 'technical',
            'created_at': '2024-01-15 11:15:00',
            'assigned_to': 'Technician 2',
            'region': 'toshkent',
            'description': 'Internet tezligi past'
        },
        {
            'id': 'APP003',
            'client_name': 'Jasur Toshmatov',
            'status': 'in_progress',
            'priority': 'normal',
            'type': 'connection',
            'created_at': '2024-01-15 09:45:00',
            'assigned_to': 'Technician 3',
            'region': 'toshkent',
            'description': 'Yangi uy uchun internet'
        }
    ],
    'statistics': [
        {
            'metric': 'Jami arizalar',
            'value': 150,
            'change': '+12%',
            'period': 'Bu oy'
        },
        {
            'metric': 'Bajarilgan arizalar',
            'value': 128,
            'change': '+8%',
            'period': 'Bu oy'
        },
        {
            'metric': 'O\'rtacha bajarish vaqti',
            'value': '2.3 soat',
            'change': '-15%',
            'period': 'Bu oy'
        },
        {
            'metric': 'Mijozlar mamnuniyati',
            'value': '94%',
            'change': '+3%',
            'period': 'Bu oy'
        }
    ],
    'users': [
        {
            'id': 1,
            'full_name': 'Aziz Karimov',
            'role': 'junior_manager',
            'status': 'online',
            'region': 'toshkent',
            'total_tasks': 45,
            'completed_tasks': 38,
            'success_rate': '84.4%'
        },
        {
            'id': 2,
            'full_name': 'Malika Yusupova',
            'role': 'junior_manager',
            'status': 'online',
            'region': 'toshkent',
            'total_tasks': 52,
            'completed_tasks': 47,
            'success_rate': '90.4%'
        },
        {
            'id': 3,
            'full_name': 'Jasur Toshmatov',
            'role': 'technician',
            'status': 'busy',
            'region': 'toshkent',
            'total_tasks': 38,
            'completed_tasks': 35,
            'success_rate': '92.1%'
        }
    ],
    'reports': [
        {
            'report_type': 'Kunlik hisobot',
            'date': '2024-01-15',
            'total_applications': 25,
            'completed': 22,
            'pending': 3,
            'cancelled': 0
        },
        {
            'report_type': 'Haftalik hisobot',
            'date': '2024-01-08 - 2024-01-14',
            'total_applications': 156,
            'completed': 142,
            'pending': 12,
            'cancelled': 2
        },
        {
            'report_type': 'Oylik hisobot',
            'date': '2024-01-01 - 2024-01-31',
            'total_applications': 642,
            'completed': 598,
            'pending': 38,
            'cancelled': 6
        }
    ]
}

def create_csv_export(data: list, filename: str) -> BufferedInputFile:
    """Create CSV export file from data"""
    try:
        if not data:
            return None
        
        # Create CSV string
        output = io.StringIO()
        if data:
            # Get fieldnames from first item
            fieldnames = list(data[0].keys())
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write data
            writer.writerows(data)
        
        # Get CSV content
        csv_content = output.getvalue()
        output.close()
        
        # Create file
        file = BufferedInputFile(
            csv_content.encode('utf-8'),
            filename=f"{filename}.csv"
        )
        
        return file
        
    except Exception as e:
        logger.error(f"Error creating CSV export: {e}")
        return None

def create_json_export(data: list, filename: str) -> BufferedInputFile:
    """Create JSON export file from data"""
    try:
        if not data:
            return None
        
        # Create JSON string
        json_content = json.dumps(data, indent=2, ensure_ascii=False, default=str)
        
        # Create file
        file = BufferedInputFile(
            json_content.encode('utf-8'),
            filename=f"{filename}.json"
        )
        
        return file
        
    except Exception as e:
        logger.error(f"Error creating JSON export: {e}")
        return None

def get_manager_export_router():
    """Manager export router with mock data"""
    router = Router()
    
    @router.message(F.text.in_(["📤 Export", "📤 Экспорт"]))
    async def export_menu_handler(message: Message, state: FSMContext):
        """Export menu handler"""
        try:
            # Mock user info
            mock_user = {
                'id': message.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
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
            
            if lang == 'uz':
                text = """📤 <b>Export qilish</b>

Qaysi ma'lumotlarni export qilmoqchisiz?

📊 <b>Mavjud export turlari:</b>
• 📑 Buyurtmalar - Barcha arizalar ro'yxati
• 📊 Statistika - Ish natijalari statistikasi
• 👥 Xodimlar - Xodimlar ma'lumotlari
• 📋 Hisobotlar - Turli hisobotlar"""
            else:
                text = """📤 <b>Экспорт</b>

Какие данные вы хотите экспортировать?

📊 <b>Доступные типы экспорта:</b>
• 📑 Заказы - Список всех заявок
• 📊 Статистика - Статистика результатов работы
• 👥 Сотрудники - Данные сотрудников
• 📋 Отчеты - Различные отчеты"""
            
            # Create inline keyboard for export types
            keyboard = []
            for export_type, display_name in export_type_names[lang].items():
                keyboard.append([
                    InlineKeyboardButton(
                        text=display_name,
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
            
            await message.answer(text, reply_markup=markup, parse_mode='HTML')
            await state.set_state(ManagerMainMenuStates.export_selection)
            
        except Exception as e:
            logger.error(f"Error in manager export handler: {str(e)}")
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("manager_export_"))
    async def handle_export_selection(callback: CallbackQuery, state: FSMContext):
        """Handle export type selection"""
        try:
            await callback.answer()
            
            # Extract export type
            export_type = callback.data.replace("manager_export_", "")
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Get data for export type
            data = MOCK_EXPORT_DATA.get(export_type, [])
            
            if not data:
                if lang == 'uz':
                    text = "❌ Bu turdagi ma'lumotlar topilmadi"
                else:
                    text = "❌ Данные этого типа не найдены"
                
                await callback.message.edit_text(text)
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
            
            export_name = export_type_names[lang].get(export_type, export_type)
            
            if lang == 'uz':
                text = f"""📤 <b>Export: {export_name}</b>

📊 <b>Ma'lumotlar:</b>
• Jami qatorlar: {len(data)}
• Export turi: {export_name}
• Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}

Qaysi formatda export qilmoqchisiz?"""
            else:
                text = f"""📤 <b>Экспорт: {export_name}</b>

📊 <b>Данные:</b>
• Всего строк: {len(data)}
• Тип экспорта: {export_name}
• Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}

В каком формате вы хотите экспортировать?"""
            
            # Create format selection keyboard
            keyboard = [
                [
                    InlineKeyboardButton(
                        text="📊 CSV format",
                        callback_data=f"export_format_{export_type}_csv"
                    ),
                    InlineKeyboardButton(
                        text="📋 JSON format",
                        callback_data=f"export_format_{export_type}_json"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔙 Orqaga" if lang == 'uz' else "🔙 Назад",
                        callback_data="manager_export_menu"
                    )
                ]
            ]
            
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await callback.message.edit_text(text, reply_markup=markup, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error handling export selection: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("export_format_"))
    async def handle_export_format(callback: CallbackQuery, state: FSMContext):
        """Handle export format selection"""
        try:
            await callback.answer()
            
            # Extract export type and format
            parts = callback.data.replace("export_format_", "").split("_")
            export_type = parts[0]
            export_format = parts[1]
            
            # Mock user info
            mock_user = {
                'id': callback.from_user.id,
                'language': 'uz',
                'role': 'manager'
            }
            
            lang = mock_user.get('language', 'uz')
            
            # Get data for export type
            data = MOCK_EXPORT_DATA.get(export_type, [])
            
            if not data:
                if lang == 'uz':
                    text = "❌ Ma'lumotlar topilmadi"
                else:
                    text = "❌ Данные не найдены"
                
                await callback.message.edit_text(text)
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
            
            export_name = export_type_names[lang].get(export_type, export_type)
            
            # Create export file
            if export_format == 'csv':
                file = create_csv_export(data, f"{export_name}_{datetime.now().strftime('%Y%m%d_%H%M')}")
                format_name = "CSV" if lang == 'uz' else "CSV"
            elif export_format == 'json':
                file = create_csv_export(data, f"{export_name}_{datetime.now().strftime('%Y%m%d_%H%M')}")
                format_name = "JSON" if lang == 'uz' else "JSON"
            else:
                await callback.answer("❌ Noto'g'ri format", show_alert=True)
                return
            
            if not file:
                if lang == 'uz':
                    text = "❌ Export fayli yaratishda xatolik"
                else:
                    text = "❌ Ошибка при создании файла экспорта"
                
                await callback.message.edit_text(text)
                return
            
            # Send file
            if lang == 'uz':
                caption = f"""✅ <b>Export muvaffaqiyatli yaratildi!</b>

📊 <b>Ma'lumotlar:</b>
• Tur: {export_name}
• Format: {format_name}
• Qatorlar: {len(data)}
• Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}

📁 Fayl yuklandi va tayyor."""
            else:
                caption = f"""✅ <b>Экспорт успешно создан!</b>

📊 <b>Данные:</b>
• Тип: {export_name}
• Формат: {format_name}
• Строки: {len(data)}
• Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}

📁 Файл загружен и готов."""
            
            await callback.message.answer_document(
                document=file,
                caption=caption,
                parse_mode='HTML'
            )
            
            # Show success message
            if lang == 'uz':
                text = f"""✅ <b>Export muvaffaqiyatli yakunlandi!</b>

📊 <b>Ma'lumotlar:</b>
• Tur: {export_name}
• Format: {format_name}
• Qatorlar: {len(data)}
• Sana: {datetime.now().strftime('%d.%m.%Y %H:%M')}

📁 Fayl yuklandi va tayyor."""
            else:
                text = f"""✅ <b>Экспорт успешно завершен!</b>

📊 <b>Данные:</b>
• Тип: {export_name}
• Формат: {format_name}
• Строки: {len(data)}
• Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}

📁 Файл загружен и готов."""
            
            # Create back keyboard
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(
                    text="🔙 Export menyuga qaytish" if lang == 'uz' else "🔙 Вернуться в меню экспорта",
                    callback_data="manager_export_menu"
                )
            ]])
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error handling export format: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "manager_export_menu")
    async def back_to_export_menu(callback: CallbackQuery, state: FSMContext):
        """Go back to export menu"""
        try:
            await callback.answer()
            
            # Clear state
            await state.clear()
            
            # Show export menu again
            await export_menu_handler(callback.message, state)
            
        except Exception as e:
            logger.error(f"Error going back to export menu: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "manager_export_back_main")
    async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
        """Go back to main menu"""
        try:
            await callback.answer()
            
            # Clear state
            await state.clear()
            
            # Import and show main keyboard
            keyboard = get_manager_main_keyboard('uz')  # Default to Uzbek
            
            text = "🏠 <b>Asosiy menyu</b>\n\nKerakli bo'limni tanlang:"
            
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='HTML')
            
        except Exception as e:
            logger.error(f"Error going back to main menu: {e}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)
    
    return router