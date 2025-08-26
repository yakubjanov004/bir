"""
Call Center Supervisor Application Management Handler

This module handles application creation, management and workflow for call center supervisors.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List, Optional

# Keyboard imports
from keyboards.call_center_supervisor_buttons import (
    get_client_search_menu, get_client_selection_keyboard, get_application_type_menu,
    get_application_priority_keyboard, get_application_confirmation_keyboard,
    get_supervisor_application_management_keyboard,
    get_supervisor_staff_creation_keyboard
)

# States imports
from states.call_center_supervisor_states import CallCenterSupervisorApplicationStates
from filters.role_filter import RoleFilter

# Mock functions to replace utils and database imports
# Removed duplicate get_role_router - using centralized version from utils.role_system

async def get_user_by_telegram_id(telegram_id: int) -> Dict[str, Any]:
    """Mock user data"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'call_center_supervisor',
        'language': 'uz',
        'full_name': 'Test Supervisor'
    }

async def get_user_lang(user_id: int) -> str:
    """Mock user language"""
    return 'uz'

async def search_clients_by_phone(phone: str) -> List[Dict[str, Any]]:
    """Mock client search by phone"""
    # Mock data - in real app this would query database
    if phone.startswith('+998'):
        return [
            {
                'id': 1,
                'full_name': 'Test Client 1',
                'phone': phone,
                'address': 'Test Address 1'
            },
            {
                'id': 2,
                'full_name': 'Test Client 2', 
                'phone': phone,
                'address': 'Test Address 2'
            }
        ]
    return []

async def search_clients_by_name(name: str) -> List[Dict[str, Any]]:
    """Mock client search by name"""
    # Mock data - in real app this would query database
    if len(name) > 2:
        return [
            {
                'id': 3,
                'full_name': f'{name} Test',
                'phone': '+998901234567',
                'address': 'Test Address 3'
            }
        ]
    return []

async def get_client_by_id(client_id: int) -> Dict[str, Any]:
    """Mock get client by ID"""
    # Mock data - in real app this would query database
    return {
        'id': client_id,
        'full_name': f'Test Client {client_id}',
        'phone': '+998901234567',
        'address': f'Test Address {client_id}'
    }

async def create_new_client(client_data: Dict[str, Any]) -> int:
    """Mock create new client"""
    # Mock data - in real app this would insert into database
    return 999  # Return mock client ID

async def create_staff_application_as_supervisor(supervisor_id: int, client_id: int, application_type: str, details: Dict[str, Any]) -> int:
    """Mock create staff application"""
    # Mock data - in real app this would insert into database
    return 888  # Return mock application ID

async def setup_logger(name: str):
    """Mock logger setup"""
    return None



logger = None  # Mock logger

def get_call_center_supervisor_application_management_router():
    """Get call center supervisor application management router"""
    from utils.role_system import get_role_router
    router = get_role_router("call_center_supervisor")

    # Client search handlers
    @router.callback_query(F.data.startswith("ccs_client_search_"))
    async def handle_client_search_method(callback: CallbackQuery, state: FSMContext):
        """Handle client search method selection"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            search_method = callback.data.split("_")[-1]
            
            if search_method == "phone":
                await state.set_state(CallCenterSupervisorApplicationStates.client_search_phone)
                text = (
                    "📱 Mijoz telefon raqamini kiriting:\n\n"
                    "Masalan: +998901234567 yoki 901234567"
                ) if lang == 'uz' else (
                    "📱 Введите номер телефона клиента:\n\n"
                    "Например: +998901234567 или 901234567"
                )
                
            elif search_method == "name":
                await state.set_state(CallCenterSupervisorApplicationStates.client_search_name)
                text = (
                    "👤 Mijoz ismini kiriting:\n\n"
                    "To'liq ism yoki ism qismini yozing"
                ) if lang == 'uz' else (
                    "👤 Введите имя клиента:\n\n"
                    "Полное имя или часть имени"
                )
                
            elif search_method == "id":
                await state.set_state(CallCenterSupervisorApplicationStates.client_search_id)
                text = (
                    "🆔 Mijoz ID raqamini kiriting:"
                ) if lang == 'uz' else (
                    "🆔 Введите ID клиента:"
                )
                
            elif search_method == "new":
                await state.set_state(CallCenterSupervisorApplicationStates.creating_new_client)
                text = (
                    "➕ Yangi mijoz yaratish\n\n"
                    "Mijozning to'liq ismini kiriting:"
                ) if lang == 'uz' else (
                    "➕ Создание нового клиента\n\n"
                    "Введите полное имя клиента:"
                )
                
            else:
                await callback.answer("Noma'lum usul", show_alert=True)
                return

            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(CallCenterSupervisorApplicationStates.client_search_phone)
    async def handle_client_search_by_phone(message: Message, state: FSMContext):
        """Handle client search by phone number"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return

            lang = user.get('language', 'uz')
            phone = message.text.strip()
            
            # Search clients by phone
            clients = await search_clients_by_phone(phone)
            
            if not clients:
                text = (
                    f"📱 Telefon raqami '{phone}' bo'yicha mijoz topilmadi.\n\n"
                    "Yangi mijoz yaratishni xohlaysizmi?"
                ) if lang == 'uz' else (
                    f"📱 Клиент с номером '{phone}' не найден.\n\n"
                    "Хотите создать нового клиента?"
                )
                
                # Store phone for new client creation
                await state.update_data(new_client_phone=phone)
                await state.set_state(CallCenterSupervisorApplicationStates.creating_new_client)
                
                keyboard = get_supervisor_staff_creation_keyboard(lang)
                
                await message.answer(text, reply_markup=keyboard)
                return
            
            # Show found clients
            text = (
                f"📱 Telefon raqami '{phone}' bo'yicha topilgan mijozlar:\n\n"
                "Kerakli mijozni tanlang:"
            ) if lang == 'uz' else (
                f"📱 Клиенты найденные по номеру '{phone}':\n\n"
                "Выберите нужного клиента:"
            )
            
            await message.answer(text, reply_markup=get_client_selection_keyboard(clients, lang))
            await state.set_state(CallCenterSupervisorApplicationStates.selecting_client)
            
        except Exception as e:
            #lang = await get_user_lang(message.from_user.id)
            #error_text = "Xatolik yuz berdi" if lang == 'uz' else "Произошла ошибка"
            #await message.answer(error_text)
            pass

    @router.message(CallCenterSupervisorApplicationStates.client_search_name)
    async def handle_client_search_by_name(message: Message, state: FSMContext):
        """Handle client search by name"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return

            lang = user.get('language', 'uz')
            name = message.text.strip()
            
            # Search clients by name
            clients = await search_clients_by_name(name)
            
            if not clients:
                text = (
                    f"👤 '{name}' nomi bo'yicha mijoz topilmadi.\n\n"
                    "Boshqa nom bilan qidirib ko'ring yoki yangi mijoz yarating."
                ) if lang == 'uz' else (
                    f"👤 Клиент с именем '{name}' не найден.\n\n"
                    "Попробуйте другое имя или создайте нового клиента."
                )
                
                keyboard = get_supervisor_staff_creation_keyboard(lang)
                
                await message.answer(text, reply_markup=keyboard)
                return
            
            # Show found clients
            text = (
                f"👤 '{name}' nomi bo'yicha topilgan mijozlar:\n\n"
                "Kerakli mijozni tanlang:"
            ) if lang == 'uz' else (
                f"👤 Клиенты найденные по имени '{name}':\n\n"
                "Выберите нужного клиента:"
            )
            
            await message.answer(text, reply_markup=get_client_selection_keyboard(clients, lang))
            await state.set_state(CallCenterSupervisorApplicationStates.selecting_client)
            
        except Exception as e:
            #lang = await get_user_lang(message.from_user.id)
            #error_text = "Xatolik yuz berdi" if lang == 'uz' else "Произошла ошибка"
            #await message.answer(error_text)
            pass

    @router.message(CallCenterSupervisorApplicationStates.client_search_id)
    async def handle_client_search_by_id(message: Message, state: FSMContext):
        """Handle client search by ID"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return

            lang = user.get('language', 'uz')
            
            try:
                client_id = int(message.text.strip())
            except ValueError:
                text = (
                    "❌ Noto'g'ri ID format. Faqat raqam kiriting."
                ) if lang == 'uz' else (
                    "❌ Неверный формат ID. Введите только число."
                )
                await message.answer(text)
                return
            
            # Get client by ID
            client = await get_client_by_id(client_id)
            
            if not client:
                text = (
                    f"🆔 ID {client_id} bo'yicha mijoz topilmadi."
                ) if lang == 'uz' else (
                    f"🆔 Клиент с ID {client_id} не найден."
                )
                await message.answer(text)
                return
            
            # Show found client and proceed
            await _proceed_with_selected_client(message, state, client, lang)
            
        except Exception as e:
            #lang = await get_user_lang(message.from_user.id)
            #error_text = "Xatolik yuz berdi" if lang == 'uz' else "Произошла ошибка"
            #await message.answer(error_text)
            pass

    @router.callback_query(F.data.startswith("ccs_select_client_"))
    async def handle_client_selection(callback: CallbackQuery, state: FSMContext):
        """Handle client selection from search results"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            client_id = int(callback.data.split("_")[-1])
            
            # Get selected client
            client = await get_client_by_id(client_id)
            
            if not client:
                await callback.answer("Mijoz topilmadi", show_alert=True)
                return
            
            # Proceed with selected client
            await _proceed_with_selected_client(callback.message, state, client, lang)
            await callback.answer()
            
        except Exception as e:
            # await callback.answer("Xatolik yuz berdi", show_alert=True)   
            pass

    @router.message(CallCenterSupervisorApplicationStates.creating_new_client)
    async def handle_new_client_name(message: Message, state: FSMContext):
        """Handle new client name input"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return

            lang = user.get('language', 'uz')
            client_name = message.text.strip()
            
            if len(client_name) < 2:
                text = (
                    "❌ Ism juda qisqa. Kamida 2 ta harf kiriting."
                ) if lang == 'uz' else (
                    "❌ Имя слишком короткое. Введите минимум 2 символа."
                )
                await message.answer(text)
                return
            
            # Store client name and ask for phone
            await state.update_data(new_client_name=client_name)
            
            data = await state.get_data()
            if 'new_client_phone' in data:
                # Phone already provided, create client
                await _create_new_client_and_proceed(message, state, lang)
            else:
                # Ask for phone number
                text = (
                    f"👤 Mijoz ismi: {client_name}\n\n"
                    "📱 Endi telefon raqamini kiriting:"
                ) if lang == 'uz' else (
                    f"👤 Имя клиента: {client_name}\n\n"
                    "📱 Теперь введите номер телефона:"
                )
                
                await message.answer(text)
                # Stay in the same state to get phone number
            
        except Exception as e:
            #lang = await get_user_lang(message.from_user.id)
            #error_text = "Xatolik yuz berди" if lang == 'uz' else "Произошла ошибка"
            #await message.answer(error_text)
            pass

    @router.callback_query(F.data == "ccs_create_new_client")
    async def handle_create_new_client_callback(callback: CallbackQuery, state: FSMContext):
        """Handle create new client callback"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            
            text = (
                "➕ Yangi mijoz yaratish\n\n"
                "Mijozning to'liq ismini kiriting:"
            ) if lang == 'uz' else (
                "➕ Создание нового клиента\n\n"
                "Введите полное имя клиента:"
            )
            
            await callback.message.edit_text(text)
            await state.set_state(CallCenterSupervisorApplicationStates.creating_new_client)
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    # Application creation handlers
    @router.message(CallCenterSupervisorApplicationStates.entering_application_details)
    async def handle_application_details(message: Message, state: FSMContext):
        """Handle application details input"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return

            lang = user.get('language', 'uz')
            details = message.text.strip()
            
            if len(details) < 10:
                text = (
                    "❌ Tavsif juda qisqa. Kamida 10 ta belgi kiriting."
                ) if lang == 'uz' else (
                    "❌ Описание слишком короткое. Введите минимум 10 символов."
                )
                await message.answer(text)
                return
            
            # Store application details
            await state.update_data(application_details=details)
            
            # Ask for priority
            text = (
                "🎯 Ariza muhimlik darajasini tanlang:"
            ) if lang == 'uz' else (
                "🎯 Выберите приоритет заявки:"
            )
            
            await message.answer(text, reply_markup=get_application_priority_keyboard(lang))
            
        except Exception as e:
            #lang = await get_user_lang(message.from_user.id)
            #error_text = "Xatolik yuz berди" if lang == 'uz' else "Произошла ошибка"
            #await message.answer(error_text)
            pass

    @router.callback_query(F.data.startswith("ccs_priority_"))
    async def handle_priority_selection(callback: CallbackQuery, state: FSMContext):
        """Handle priority selection"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            priority = callback.data.split("_")[-1]
            
            # Store priority and show confirmation
            await state.update_data(application_priority=priority)
            await _show_application_confirmation(callback, state, lang)
            
        except Exception as e:
            # await callback.answer("Xatolik yuz berdi", show_alert=True)
            pass

    @router.callback_query(F.data == "ccs_confirm_application")
    async def handle_application_confirmation(callback: CallbackQuery, state: FSMContext):
        """Handle application confirmation and creation"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return

            lang = user.get('language', 'uz')
            data = await state.get_data()
            
            # Get application data
            client_id = data.get('selected_client_id')
            application_type = data.get('application_type')
            details = data.get('application_details')
            priority = data.get('application_priority', 'medium')
            
            if not all([client_id, application_type, details]):
                await callback.answer("Ma'lumotlar to'liq emas", show_alert=True)
                return
            
            # Create application
            application_details = {
                'description': details,
                'priority': priority,
                'created_by_role': 'call_center_supervisor'
            }
            
            application_id = await create_staff_application_as_supervisor(
                user['id'], client_id, application_type, application_details
            )
            
            if application_id:
                text = (
                    f"✅ Ariza muvaffaqiyatli yaratildi!\n\n"
                    f"📋 Ariza ID: #{application_id}\n"
                    f"👤 Mijoz ID: {client_id}\n"
                    f"📝 Tur: {application_type}\n"
                    f"🎯 Muhimlik: {priority}\n\n"
                    f"Ariza tegishli xodimga tayinlanadi."
                ) if lang == 'uz' else (
                    f"✅ Заявка успешно создана!\n\n"
                    f"📋 ID заявки: #{application_id}\n"
                    f"👤 ID клиента: {client_id}\n"
                    f"📝 Тип: {application_type}\n"
                    f"🎯 Приоритет: {priority}\n\n"
                    f"Заявка будет назначена соответствующему сотруднику."
                )
            else:
                text = (
                    "❌ Ariza yaratishda xatolik yuz berdi."
                ) if lang == 'uz' else (
                    "❌ Ошибка при создании заявки."
                )
            
            await callback.message.edit_text(text)
            await state.clear()
            await callback.answer()
            
        except Exception as e:
            # await callback.answer("Xatolik yuz berdi", show_alert=True)
            pass

    return router


async def _proceed_with_selected_client(message: Message, state: FSMContext, client: Dict[str, Any], lang: str):
    """Proceed with selected client to application creation"""
    try:
        # Store selected client
        await state.update_data(selected_client_id=client['id'])
        
        # Get application type from state data
        data = await state.get_data()
        application_type = data.get('application_type')
        
        if application_type:
            # Application type already selected, ask for details
            text = (
                f"👤 Tanlangan mijoz: {client['full_name']}\n"
                f"📱 Telefon: {client.get('phone', 'N/A')}\n\n"
                f"📝 {application_type} uchun batafsil tavsif kiriting:"
            ) if lang == 'uz' else (
                f"👤 Выбранный клиент: {client['full_name']}\n"
                f"📱 Телефон: {client.get('phone', 'N/A')}\n\n"
                f"📝 Введите подробное описание для {application_type}:"
            )
            
            await message.answer(text)
            await state.set_state(CallCenterSupervisorApplicationStates.entering_application_details)
        else:
            # Ask for application type
            text = (
                f"👤 Tanlangan mijoz: {client['full_name']}\n"
                f"📱 Telefon: {client.get('phone', 'N/A')}\n\n"
                f"📋 Ariza turini tanlang:"
            ) if lang == 'uz' else (
                f"👤 Выбранный клиент: {client['full_name']}\n"
                f"📱 Телефон: {client.get('phone', 'N/A')}\n\n"
                f"📋 Выберите тип заявки:"
            )
            
            await message.answer(text, reply_markup=get_application_type_menu(lang))
        
    except Exception as e:
        # error_text = "Xatolik yuz berди" if lang == 'uz' else "Произошла ошибка"
        #await message.answer(error_text)
        pass


async def _create_new_client_and_proceed(message: Message, state: FSMContext, lang: str):
    """Create new client and proceed with application"""
    try:
        data = await state.get_data()
        client_name = data.get('new_client_name')
        client_phone = data.get('new_client_phone')
        
        if not client_name:
            text = (
                "❌ Mijoz ismi topilmadi. Qaytadan boshlang."
            ) if lang == 'uz' else (
                "❌ Имя клиента не найдено. Начните заново."
            )
            await message.answer(text)
            return
        
        # If phone not provided yet, ask for it
        if not client_phone:
            # Check if current message is phone number
            phone_text = message.text.strip()
            if phone_text and (phone_text.startswith('+') or phone_text.isdigit()):
                client_phone = phone_text
                await state.update_data(new_client_phone=client_phone)
            else:
                text = (
                    "📱 Telefon raqamini kiriting:"
                ) if lang == 'uz' else (
                    "📱 Введите номер телефона:"
                )
                await message.answer(text)
                return
        
        # Create new client
        client_data = {
            'full_name': client_name,
            'phone': client_phone,
            'created_by_supervisor': True
        }
        
        client_id = await create_new_client(client_data)
        
        if client_id:
            # Get created client and proceed
            client = await get_client_by_id(client_id)
            if client:
                await _proceed_with_selected_client(message, state, client, lang)
            else:
                text = (
                    "❌ Yaratilgan mijozni olishda xatolik."
                ) if lang == 'uz' else (
                    "❌ Ошибка при получении созданного клиента."
                )
                await message.answer(text)
        else:
            text = (
                "❌ Mijoz yaratishda xatolik yuz berdi."
            ) if lang == 'uz' else (
                "❌ Ошибка при создании клиента."
            )
            await message.answer(text)
        
    except Exception as e:
        error_text = "Xatolik yuz berdi" if lang == 'uz' else "Произошла ошибка"
        await message.answer(error_text)


async def _show_application_confirmation(callback: CallbackQuery, state: FSMContext, lang: str):
    """Show application confirmation"""
    try:
        data = await state.get_data()
        
        client_id = data.get('selected_client_id')
        application_type = data.get('application_type')
        details = data.get('application_details')
        priority = data.get('application_priority')
        
        # Get client info (you might want to cache this)
        client = await get_client_by_id(client_id) if client_id else None
        client_name = client['full_name'] if client else 'Noma\'lum'
        
        priority_text = {
            'high': ('Yuqori', 'Высокий'),
            'medium': ('O\'rta', 'Средний'),
            'low': ('Past', 'Низкий')
        }.get(priority, (priority, priority))
        
        priority_display = priority_text[0 if lang == 'uz' else 1]
        
        text = (
            f"📋 Ariza tasdiqlash\n\n"
            f"👤 Mijoz: {client_name}\n"
            f"📝 Tur: {application_type}\n"
            f"🎯 Muhimlik: {priority_display}\n"
            f"📄 Tavsif: {details}\n\n"
            f"Arizani yaratishni tasdiqlaysizmi?"
        ) if lang == 'uz' else (
            f"📋 Подтверждение заявки\n\n"
            f"👤 Клиент: {client_name}\n"
            f"📝 Тип: {application_type}\n"
            f"🎯 Приоритет: {priority_display}\n"
            f"📄 Описание: {details}\n\n"
            f"Подтвердить создание заявки?"
        )
        
        await callback.message.edit_text(text, reply_markup=get_application_confirmation_keyboard(lang))
        await state.set_state(CallCenterSupervisorApplicationStates.confirming_application)
        
    except Exception as e:
        # await callback.answer("Xatolik yuz berdi", show_alert=True)
        pass