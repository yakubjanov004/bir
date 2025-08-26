from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.warehouse_buttons import equipment_preparation_keyboard
from states.warehouse_states import WarehouseWorkflowStates
from filters.role_filter import RoleFilter

def get_warehouse_workflow_router():
    """Warehouse workflow integration router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("warehouse")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.callback_query(F.data.startswith("prepare_equipment_"))
    async def prepare_equipment_handler(callback: CallbackQuery, state: FSMContext):
        """Handle equipment preparation request from technician"""
        try:
            request_id = callback.data.split("_")[-1]
            
            # Mock application details (like other modules)
            app_details = {
                'id': request_id,
                'client_name': 'Test Client',
                'description': 'Test equipment preparation request',
                'technician_name': 'Test Technician',
                'materials_needed': [
                    {'name': 'Cable', 'quantity': 2, 'unit': 'dona'},
                    {'name': 'Connector', 'quantity': 4, 'unit': 'dona'}
                ]
            }
            
            text = "🔧 Uskunani tayyorlash so'rovi:\n\n"
            text += f"📋 Ariza #{app_details['id']}\n"
            text += f"👤 Mijoz: {app_details.get('client_name', 'Noma\'lum')}\n"
            text += f"📝 Tavsif: {app_details['description']}\n"
            text += f"👨‍🔧 Texnik: {app_details.get('technician_name', 'Noma\'lum')}\n"
            
            if app_details.get('materials_needed'):
                text += "\n📦 Kerakli materiallar:\n"
                for material in app_details['materials_needed']:
                    text += f"• {material['name']}: {material['quantity']} {material.get('unit', 'dona')}\n"
            
            await callback.message.edit_text(text)
            await state.update_data(current_request=app_details)
            await state.set_state(WarehouseWorkflowStates.preparing_equipment)
            
            # Show preparation options
            keyboard = [[
                {"text": "✅ Tayyorlash tugallandi", "callback_data": f"equipment_ready_{request_id}"}
            ]]
            
            await callback.message.reply(
                "🔧 Uskunani tayyorlang va tugagach tasdiqlang:",
                reply_markup={"inline_keyboard": keyboard}
            )
            
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("equipment_ready_"))
    async def equipment_ready_handler(callback: CallbackQuery, state: FSMContext):
        """Mark equipment as ready and complete warehouse processing"""
        try:
            request_id = int(callback.data.split("_")[-1])
            
            data = await state.get_data()
            current_request = data.get('current_request')
            
            if current_request:
                # Mock success response (like other modules)
                success_text = f"✅ Uskuna tayyor! Ariza #{request_id} texnikka qaytarildi."
                await callback.message.edit_text(success_text)
                
                # Mock notification (like other modules)
                await notify_technician_equipment_ready(request_id, 123)
                
            else:
                await callback.answer("So'rov ma'lumotlari topilmadi", show_alert=True)
            
            await callback.answer()
            await state.clear()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(F.text == "📥 Yangi so'rovlar")
    async def new_requests_handler(message: Message, state: FSMContext):
        """Show new warehouse requests"""
        try:
            # Mock applications data (like other modules)
            applications = [
                {
                    'id': '1001',
                    'client_name': 'Test Client 1',
                    'description': 'Equipment preparation needed for connection',
                    'created_at': '2024-01-15 10:30:00',
                    'technician_name': 'Tech 1',
                    'application_type': 'technical_service'
                },
                {
                    'id': '1002', 
                    'client_name': 'Test Client 2',
                    'description': 'Materials needed for repair work',
                    'created_at': '2024-01-15 11:15:00',
                    'technician_name': 'Tech 2',
                    'application_type': 'connection'
                }
            ]
            
            if applications:
                text = "📥 Yangi ombor so'rovlari:\n\n"
                
                for app in applications:
                    text += f"🔹 #{app['id']} - {app.get('client_name', 'Noma\'lum')}\n"
                    text += f"   📝 {app['description'][:50]}{'...' if len(app['description']) > 50 else ''}\n"
                    text += f"   📅 {app['created_at']}\n"
                    text += f"   👨‍🔧 Texnik: {app.get('technician_name', 'Tayinlanmagan')}\n"
                    text += f"   🏷️ Turi: {app.get('application_type', 'technical_service')}\n"
                    text += "\n"
                    
                    if len(text) > 3500:
                        text += "... va boshqalar"
                        break
            else:
                text = "📭 Yangi so'rovlar yo'q"
            
            await message.answer(text)
            
        except Exception as e:
            error_text = "So'rovlarni olishda xatolik"
            await message.answer(error_text)

    @router.message(F.text == "📦 Materiallar")
    async def materials_handler(message: Message, state: FSMContext):
        """Show available materials"""
        try:
            # Mock materials data (like other modules)
            materials = [
                {'name': 'Cable', 'quantity': 50, 'unit': 'dona'},
                {'name': 'Connector', 'quantity': 100, 'unit': 'dona'},
                {'name': 'Router', 'quantity': 10, 'unit': 'dona'},
                {'name': 'Switch', 'quantity': 5, 'unit': 'dona'}
            ]
            
            text = "📦 Mavjud materiallar:\n\n"
            
            for material in materials:
                text += f"🔹 {material['name']}: {material['quantity']} {material['unit']}\n"
            
            await message.answer(text)
            
        except Exception as e:
            await message.answer("Materiallarni olishda xatolik")

    @router.message(F.text == "📊 Ombor statistikasi")
    async def warehouse_statistics_handler(message: Message, state: FSMContext):
        """Show warehouse statistics"""
        try:
            # Mock statistics data (like other modules)
            stats = {
                'total_requests': 25,
                'completed_today': 8,
                'pending_requests': 3,
                'materials_used': 15
            }
            
            text = "📊 Ombor statistikasi:\n\n"
            text += f"📋 Jami so'rovlar: {stats['total_requests']}\n"
            text += f"✅ Bugun tugallangan: {stats['completed_today']}\n"
            text += f"⏳ Kutilayotgan: {stats['pending_requests']}\n"
            text += f"📦 Ishlatilgan materiallar: {stats['materials_used']}\n"
            
            await message.answer(text)
            
        except Exception as e:
            await message.answer("Statistikani olishda xatolik")

    return router

async def notify_technician_equipment_ready(app_id: int, technician_id: int):
    """Notify technician that equipment is ready (mock function like other modules)"""
    try:
        # Mock notification (like other modules)
        pass
        
    except Exception as e:
        pass

async def get_application_details(app_id: int) -> dict:
    """Get detailed application information (mock function like other modules)"""
    try:
        # Mock application details (like other modules)
        app_details = {
            'id': app_id,
            'client_name': 'Test Client',
            'description': 'Test application description',
            'technician_name': 'Test Technician',
            'materials_needed': [
                {'name': 'Cable', 'quantity': 2, 'unit': 'dona'},
                {'name': 'Connector', 'quantity': 4, 'unit': 'dona'}
            ]
        }
        
        return app_details
        
    except Exception as e:
        return None

async def complete_warehouse_processing(request_id: int, user_id: int, processed_materials: list) -> bool:
    """Complete warehouse processing for an application (mock function like other modules)"""
    try:
        # Mock processing (like other modules)
        return True
        
    except Exception as e:
        return False

async def get_applications_for_role(role: str, user_id: int) -> list:
    """Get applications assigned to warehouse role (mock function like other modules)"""
    try:
        # Mock applications data (like other modules)
        applications = [
            {
                'id': '1001',
                'client_name': 'Test Client 1',
                'description': 'Equipment preparation needed',
                'created_at': '2024-01-15 10:30:00',
                'technician_name': 'Tech 1',
                'application_type': 'technical_service'
            },
            {
                'id': '1002',
                'client_name': 'Test Client 2', 
                'description': 'Materials needed for repair',
                'created_at': '2024-01-15 11:15:00',
                'technician_name': 'Tech 2',
                'application_type': 'connection'
            }
        ]
        
        return applications
        
    except Exception as e:
        return []