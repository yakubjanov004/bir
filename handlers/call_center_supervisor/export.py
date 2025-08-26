from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime
from filters.role_filter import RoleFilter
from states.call_center_supervisor_states import CallCenterSupervisorMainMenuStates
from keyboards.call_center_supervisor_buttons import (
    get_call_center_supervisor_main_keyboard,
    get_supervisor_export_types_keyboard,
    get_supervisor_export_formats_keyboard,
    get_supervisor_export_back_types_keyboard
)
from utils.export_utils import create_export_file, get_available_export_types, get_available_export_formats

def get_call_center_supervisor_export_router():
    """Call Center Supervisor export router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center_supervisor")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📤 Export", "📤 Экспорт"]))
    async def export_menu_handler(message: Message, state: FSMContext):
        """Export menu handler"""
        try:
            # Get user language
            user_data = await state.get_data()
            lang = user_data.get('lang', 'uz')
            
            export_types = get_available_export_types('call_center_supervisor')
            
            # Export type names
            export_type_names = {
                'uz': {
                    'orders': '📑 Buyurtmalar',
                    'statistics': '📊 Statistika',
                    'users': '👥 Xodimlar',
                    'feedback': '⭐ Fikr-mulohazalar',
                    'workflow': '⚙️ Workflow'
                },
                'ru': {
                    'orders': '📑 Заказы',
                    'statistics': '📊 Статистика',
                    'users': '👥 Сотрудники',
                    'feedback': '⭐ Отзывы',
                    'workflow': '⚙️ Процессы'
                }
            }
            
            text = "Export qilish\n\nQaysi ma'lumotlarni export qilmoqchisiz?" if lang == 'uz' else "Экспорт\n\nКакие данные вы хотите экспортировать?"
            
            # Create inline keyboard for export types
            keyboard = []
            for export_type in export_types:
                keyboard.append([
                    InlineKeyboardButton(
                        text=export_type_names[lang].get(export_type, export_type),
                        callback_data=f"ccs_export_main_{export_type}"
                    )
                ])
            
            keyboard.append([
                InlineKeyboardButton(
                    text="◀️ Orqaga" if lang == 'uz' else "◀️ Назад", 
                    callback_data="ccs_export_main_back_main"
                )
            ])
            
            markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
            
            await message.answer(text, reply_markup=markup)
            await state.set_state(CallCenterSupervisorMainMenuStates.export_selection)
            
        except Exception as e:
            print(f"Error in call center supervisor export handler: {str(e)}")
            await message.answer("❌ Xatolik yuz berdi" if lang == 'uz' else "❌ Произошла ошибка")

    @router.callback_query(F.data.startswith("ccs_export_main_"))
    async def handle_export_selection(callback: CallbackQuery, state: FSMContext):
        """Handle export type selection"""
        try:
            await callback.answer()
            
            # Get user language
            user_data = await state.get_data()
            lang = user_data.get('lang', 'uz')
            
            # Parse callback data
            action = callback.data.replace("ccs_export_main_", "")
            
            # Handle back to main menu
            if action == "back_main":
                await callback.message.delete()
                await callback.message.answer(
                    "🏠 Bosh menyu" if lang == 'uz' else "🏠 Главное меню",
                    reply_markup=get_call_center_supervisor_main_keyboard(lang)
                )
                await state.set_state(CallCenterSupervisorMainMenuStates.main_menu)
                return
            
            # Handle back to export types
            if action == "back_types":
                export_types = get_available_export_types('call_center_supervisor')
                export_type_names = {
                    'uz': {
                        'orders': '📑 Buyurtmalar',
                        'statistics': '📊 Statistika',
                        'users': '👥 Xodimlar',
                        'feedback': '⭐ Fikr-mulohazalar',
                        'workflow': '⚙️ Workflow'
                    },
                    'ru': {
                        'orders': '📑 Заказы',
                        'statistics': '📊 Статистика',
                        'users': '👥 Сотрудники',
                        'feedback': '⭐ Отзывы',
                        'workflow': '⚙️ Процессы'
                    }
                }
                
                text = "Export qilish\n\nQaysi ma'lumotlarni export qilmoqchisiz?" if lang == 'uz' else "Экспорт\n\nКакие данные вы хотите экспортировать?"
                
                markup = get_supervisor_export_types_keyboard(lang)
                await callback.message.edit_text(text, reply_markup=markup)
                await state.set_state(CallCenterSupervisorMainMenuStates.export_selection)
                return
            
            # Check if it's a valid export type
            available_types = get_available_export_types('call_center_supervisor')
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
                    'feedback': 'Fikr-mulohazalar',
                    'workflow': 'Workflow'
                },
                'ru': {
                    'orders': 'Заказы',
                    'statistics': 'Статистика',
                    'users': 'Сотрудники',
                    'feedback': 'Отзывы',
                    'workflow': 'Процессы'
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
            
            markup = get_supervisor_export_formats_keyboard(lang)
            await callback.message.edit_text(text, reply_markup=markup)
            await state.set_state(CallCenterSupervisorMainMenuStates.export_format_selection)
            
        except Exception as e:
            print(f"Error in export selection: {str(e)}")
            await callback.answer("❌ Xatolik yuz berdi" if lang == 'uz' else "❌ Произошла ошибка", show_alert=True)

    @router.callback_query(F.data.startswith("ccs_format_main_"))
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
            format_type = callback.data.replace("ccs_format_main_", "")
            
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
                    'feedback': 'Fikr-mulohazalar',
                    'workflow': 'Workflow'
                },
                'ru': {
                    'orders': 'Заказы',
                    'statistics': 'Статистика',
                    'users': 'Сотрудники',
                    'feedback': 'Отзывы',
                    'workflow': 'Процессы'
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
                # Create export file
                file_content, filename = create_export_file(export_type, format_type, "call_center_supervisor")
                
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
                    reply_markup=get_call_center_supervisor_main_keyboard(lang)
                )
                await state.set_state(CallCenterSupervisorMainMenuStates.main_menu)
                
            except Exception as e:
                print(f"Error creating export file: {str(e)}")
                await processing_msg.delete()
                await callback.message.answer(
                    f"❌ Export jarayonida xatolik yuz berdi:\n{str(e)}\n\n"
                    f"Iltimos, qayta urinib ko'ring." if lang == 'uz' else
                    f"❌ Ошибка при экспорте:\n{str(e)}\n\n"
                    f"Пожалуйста, попробуйте еще раз.",
                    reply_markup=get_call_center_supervisor_main_keyboard(lang)
                )
                await state.set_state(CallCenterSupervisorMainMenuStates.main_menu)
            
        except Exception as e:
            print(f"Error in export format handler: {str(e)}")
            await callback.message.answer(
                "❌ Export xatoligi yuz berdi" if lang == 'uz' else "❌ Ошибка экспорта",
                reply_markup=get_call_center_supervisor_main_keyboard(lang)
            )
            await state.set_state(CallCenterSupervisorMainMenuStates.main_menu)

    return router