from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime
from keyboards.warehouse_buttons import (
    get_warehouse_main_keyboard,
    get_warehouse_export_types_keyboard,
    get_warehouse_export_formats_keyboard,
    get_warehouse_export_back_types_keyboard
)
from states.warehouse_states import WarehouseExportStates, WarehouseMainMenuStates
from utils.export_utils import create_export_file, get_available_export_types, get_available_export_formats
from filters.role_filter import RoleFilter

def get_warehouse_export_router():
    """Warehouse export router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("warehouse")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text == "📤 Export")
    async def export_menu_handler(message: Message, state: FSMContext):
        """Export menu handler"""
        try:
            # Debug logging
            print(f"Warehouse export handler called by user {message.from_user.id}")
            
            # Get user language (default to uz)
            lang = 'uz'
            # Store language in state for later callbacks
            await state.update_data(lang=lang)
            export_types = get_available_export_types('warehouse')
            
            # Export type names in Uzbek
            export_type_names = {
                'inventory': '📦 Inventarizatsiya',
                'issued_items': '📋 Berilgan materiallar',
                'orders': '📑 Buyurtmalar',
                'statistics': '📊 Statistika'
            }
            
            text = "Export qilish\n\nQaysi ma'lumotlarni export qilmoqchisiz?"
            
            # Create inline keyboard for export types
            markup = get_warehouse_export_types_keyboard(lang)
            
            await message.answer(text, reply_markup=markup)
            await state.set_state(WarehouseExportStates.selecting_type)
            
            print(f"Warehouse export handler completed successfully")
            
        except Exception as e:
            print(f"Error in warehouse export handler: {str(e)}")
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("warehouse_export_"))
    async def handle_export_selection(callback: CallbackQuery, state: FSMContext):
        """Handle export type selection"""
        try:
            await callback.answer()
            # Retrieve language preference (default 'uz')
            data_state = await state.get_data()
            lang = data_state.get('lang', 'uz')
            
            # Parse callback data
            action = callback.data.replace("warehouse_export_", "")
            
            # Handle back to main menu
            if action == "back_main":
                await callback.message.delete()
                await callback.message.answer(
                    "🏠 Ombor bosh menyusi",
                    reply_markup=get_warehouse_main_keyboard('uz')
                )
                await state.set_state(WarehouseMainMenuStates.main_menu)
                return
            
            # Handle back to export types
            if action == "back_types":
                export_types = get_available_export_types('warehouse')
                export_type_names = {
                    'inventory': '📦 Inventarizatsiya',
                    'issued_items': '📋 Berilgan materiallar',
                    'orders': '📑 Buyurtmalar',
                    'statistics': '📊 Statistika'
                }
                
                text = "Export qilish\n\nQaysi ma'lumotlarni export qilmoqchisiz?"
                
                markup = get_warehouse_export_back_types_keyboard(lang)
                await callback.message.edit_text(text, reply_markup=markup)
                await state.set_state(WarehouseExportStates.selecting_type)
                return
            
            # Check if it's a valid export type
            available_types = get_available_export_types('warehouse')
            if action not in available_types:
                await callback.answer("❌ Noto'g'ri export turi", show_alert=True)
                return
            
            # Store selected export type
            await state.update_data(selected_export_type=action)
            
            # Export type names in Uzbek
            export_type_names = {
                'inventory': 'Inventarizatsiya',
                'issued_items': 'Berilgan materiallar',
                'orders': 'Buyurtmalar',
                'statistics': 'Statistika'
            }
            
            # Show format selection
            formats = get_available_export_formats()
            text = f"{export_type_names.get(action, action)} export\n\n"
            text += "Qaysi formatda export qilmoqchisiz?\n\n"
            text += "CSV - Universal format (Excel, Google Sheets)\n"
            text += "Excel - Microsoft Excel formati\n"
            text += "Word - Microsoft Word formati\n"
            text += "PDF - Chop etish uchun qulay format"
            
            markup = get_warehouse_export_formats_keyboard(lang)
            await callback.message.edit_text(text, reply_markup=markup)
            await state.set_state(WarehouseExportStates.selecting_format)
            
        except Exception as e:
            print(f"Error in export selection: {str(e)}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("warehouse_format_"))
    async def handle_export_format(callback: CallbackQuery, state: FSMContext):
        """Handle export format selection"""
        try:
            # Send loading message
            await callback.answer("📥 Export tayyorlanmoqda...", show_alert=False)
            
            # Delete the inline keyboard
            await callback.message.delete()
            
            # Get format type
            format_type = callback.data.replace("warehouse_format_", "")
            
            # Get stored data
            data = await state.get_data()
            export_type = data.get('selected_export_type')
            
            if not export_type:
                await callback.message.answer("❌ Export turi tanlanmagan")
                return
            
            # Export type names in Uzbek
            export_type_names = {
                'inventory': 'Inventarizatsiya',
                'issued_items': 'Berilgan materiallar',
                'orders': 'Buyurtmalar',
                'statistics': 'Statistika'
            }
            
            format_names = {
                'csv': 'CSV',
                'xlsx': 'Excel',
                'docx': 'Word',
                'pdf': 'PDF'
            }
            
            # Send processing message
            processing_msg = await callback.message.answer(
                f"⏳ {export_type_names.get(export_type, export_type)} ma'lumotlari {format_names.get(format_type, format_type)} formatida tayyorlanmoqda...\n\n"
                f"Iltimos, kuting..."
            )
            
            try:
                # Update progress
                await processing_msg.edit_text(
                    f"⏳ {export_type_names.get(export_type, export_type)} ma'lumotlari {format_names.get(format_type, format_type)} formatida tayyorlanmoqda...\n\n"
                    f"📊 Ma'lumotlar yig'ilmoqda... (25%)"
                )
                
                # Create export file
                file_content, filename = create_export_file(export_type, format_type, "warehouse")
                
                # Update progress
                await processing_msg.edit_text(
                    f"⏳ {export_type_names.get(export_type, export_type)} ma'lumotlari {format_names.get(format_type, format_type)} formatida tayyorlanmoqda...\n\n"
                    f"📄 Fayl yaratilmoqda... (75%)"
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
                    caption=f"✅ {export_type_names.get(export_type, export_type)} export muvaffaqiyatli yakunlandi!\n\n"
                            f"📄 Fayl nomi: {filename}\n"
                            f"📦 Fayl hajmi: {file_size:,} bayt\n"
                            f"📊 Format: {format_names.get(format_type, format_type)}\n"
                            f"📅 Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                            f"Export muvaffaqiyatli yakunlandi!",
                    reply_markup=get_warehouse_main_keyboard('uz')
                )
                await state.set_state(WarehouseMainMenuStates.main_menu)
                
            except Exception as e:
                print(f"Error creating export file: {str(e)}")
                await processing_msg.delete()
                await callback.message.answer(
                    f"❌ Export jarayonida xatolik yuz berdi:\n{str(e)}\n\n"
                    f"Iltimos, qayta urinib ko'ring.",
                    reply_markup=get_warehouse_main_keyboard('uz')
                )
                await state.set_state(WarehouseMainMenuStates.main_menu)
            
        except Exception as e:
            print(f"Error in export format handler: {str(e)}")
            await callback.message.answer(
                "❌ Export xatoligi yuz berdi",
                reply_markup=get_warehouse_main_keyboard('uz')
            )
            await state.set_state(WarehouseMainMenuStates.main_menu)

    @router.message(F.text == "◀️ Orqaga")
    async def export_back_handler(message: Message, state: FSMContext):
        """Export back handler"""
        try:
            await message.answer(
                "🏠 Ombor bosh menyusi",
                reply_markup=get_warehouse_main_keyboard('uz')
            )
            await state.set_state(WarehouseMainMenuStates.main_menu)
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    return router
