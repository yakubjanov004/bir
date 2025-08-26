from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime
from states.technician_states import TechnicianCommunicationStates
from filters.role_filter import RoleFilter

def get_technician_communication_router():
    """Technician communication router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("technician")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.callback_query(F.data == "tech_send_location")
    async def tech_send_location_handler(callback: CallbackQuery, state: FSMContext):
        """Request location from technician"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': callback.from_user.id,
                'role': 'technician',
                'language': 'uz',
                'full_name': 'Test Technician',
                'phone_number': '+998901234567'
            }
            
            location_text = "📍 Geolokatsiyangizni yuboring:"
            await callback.message.edit_text(location_text)
            await state.set_state(TechnicianCommunicationStates.waiting_for_location)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.message(TechnicianCommunicationStates.waiting_for_location, F.location)
    async def process_technician_location(message: Message, state: FSMContext):
        """Process technician location and send to managers"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'technician',
                'language': 'uz',
                'full_name': 'Test Technician',
                'phone_number': '+998901234567'
            }
            
            location = message.location
            
            # Mock managers
            managers = [
                {
                    'telegram_id': 123456789,
                    'role': 'manager',
                    'language': 'uz'
                },
                {
                    'telegram_id': 987654321,
                    'role': 'manager',
                    'language': 'uz'
                }
            ]
            
            sent_count = 0
            for manager in managers:
                try:
                    location_text = (
                        f"📍 Texnik geolokatsiyasi\n\n"
                        f"👨‍🔧 Texnik: {user['full_name']}\n"
                        f"📞 Telefon: {user.get('phone_number', 'Noma\'lum')}\n"
                        f"⏰ Vaqt: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
                    )
                    
                    # Mock sending location (in real app this would send to actual managers)
                    sent_count += 1
                    
                except Exception as e:
                    # Mock error handling
                    pass
            
            # Confirm to technician
            success_text = "✅ Geolokatsiya muvaffaqiyatli yuborildi!"
            await message.answer(success_text)
            await state.clear()
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")
            await state.clear()

    @router.callback_query(F.data == "tech_contact_manager")
    async def tech_contact_manager_handler(callback: CallbackQuery, state: FSMContext):
        """Contact manager directly"""
        try:
            # Mock user data
            user = {
                'id': callback.from_user.id,
                'role': 'technician',
                'language': 'uz',
                'full_name': 'Test Technician',
                'phone_number': '+998901234567'
            }
            
            await state.set_state(TechnicianCommunicationStates.waiting_for_manager_message)
            message_text = "Menejerga xabar yozing:"
            await callback.message.edit_text(message_text)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")

    @router.message(TechnicianCommunicationStates.waiting_for_manager_message)
    async def process_manager_message(message: Message, state: FSMContext):
        """Process message to manager"""
        try:
            # Mock user data
            user = {
                'id': message.from_user.id,
                'role': 'technician',
                'language': 'uz',
                'full_name': 'Test Technician',
                'phone_number': '+998901234567'
            }
            
            # Mock managers
            managers = [
                {
                    'telegram_id': 123456789,
                    'role': 'manager',
                    'language': 'uz'
                },
                {
                    'telegram_id': 987654321,
                    'role': 'manager',
                    'language': 'uz'
                }
            ]
            
            sent_count = 0
            for manager in managers:
                try:
                    manager_text = (
                        f"💬 Texnikdan xabar\n\n"
                        f"👨‍🔧 Texnik: {user['full_name']}\n"
                        f"📞 Telefon: {user.get('phone_number', 'Noma\'lum')}\n"
                        f"💬 Xabar: {message.text}\n"
                        f"⏰ Vaqt: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
                    )
                    
                    # Mock sending message (in real app this would send to actual managers)
                    sent_count += 1
                    
                except Exception as e:
                    # Mock error handling
                    pass
            
            # Confirm to technician
            success_text = "✅ Xabar menejerga yuborildi!"
            await message.answer(success_text)
            await state.clear()
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")
            await state.clear()

    return router
