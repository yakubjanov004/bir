from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from datetime import datetime
from states.technician_states import TechnicianEquipmentStates
from keyboards.technician_buttons import get_equipment_keyboard, get_back_technician_keyboard
from filters.role_filter import RoleFilter

def get_technician_equipment_router():
    """Technician equipment router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("technician")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.callback_query(F.data == "tech_equipment_request")
    async def tech_equipment_request_handler(callback: CallbackQuery, state: FSMContext):
        """Request equipment from warehouse"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': callback.from_user.id,
                'role': 'technician',
                'language': 'uz',
                'full_name': 'Test Technician',
                'phone_number': '+998901234567'
            }
            
            await state.set_state(TechnicianEquipmentStates.waiting_for_equipment_request)
            equipment_text = "Kerakli jihozlar ro'yxatini yozing:"
            await callback.message.edit_text(equipment_text)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.message(TechnicianEquipmentStates.waiting_for_equipment_request)
    async def process_equipment_request(message: Message, state: FSMContext):
        """Process equipment request and send to warehouse"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'technician',
                'language': 'uz',
                'full_name': 'Test Technician',
                'phone_number': '+998901234567'
            }
            
            # Mock recipients (warehouse staff and managers)
            recipients = [
                {
                    'telegram_id': 123456789,
                    'role': 'warehouse',
                    'language': 'uz'
                },
                {
                    'telegram_id': 987654321,
                    'role': 'manager',
                    'language': 'uz'
                }
            ]
            
            sent_count = 0
            for recipient in recipients:
                try:
                    request_text = (
                        f"📦 Jihoz so'rovi\n\n"
                        f"👨‍🔧 Texnik: {user['full_name']}\n"
                        f"📞 Telefon: {user.get('phone_number', 'Noma\'lum')}\n"
                        f"📝 Kerakli jihozlar: {message.text}\n"
                        f"⏰ Vaqt: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
                    )
                    
                    # Mock sending message (in real app this would send to actual recipients)
                    sent_count += 1
                    
                except Exception as e:
                    # Mock error handling
                    pass
            
            # Confirm to technician
            success_text = "✅ Jihoz so'rovi yuborildi!"
            await message.answer(success_text)
            await state.clear()
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")
            await state.clear()

    return router
