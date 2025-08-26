"""
Client Connection Order Handler - Full Database Integration

Ulanish zayavkalari uchun handler
Client'dan so'raladigan ma'lumotlar:
1. Region (Toshkent/Samarqand)
2. Ulanish turi (B2C/B2B)
3. Tarif (Standard/Yangi)
4. Manzil
5. Shartnoma raqami
6. Tashkilot nomi (ixtiyoriy)
7. Geolokatsiya (ixtiyoriy)
"""
from datetime import datetime
import logging
from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from keyboards.client_buttons import (
    get_main_menu_keyboard,
    zayavka_type_keyboard,
    geolocation_keyboard,
    get_client_tariff_selection_keyboard,
    confirmation_keyboard
)
from states.client_states import ConnectionOrderStates
from filters.role_filter import RoleFilter

# Mock database functions to replace database imports
async def create_connection_request(region_code: str, client_id: int, connection_type: str, tariff: str, address: str, phone: str, description: str, geo_location: str = None, telegram_id: int = None, full_name: str = None, username: str = None):
    """Mock create connection request"""
    request_id = f"UL_{telegram_id}_{int(datetime.now().timestamp())}"
    print(f"Mock: Created connection request {request_id} for client {client_id} in region {region_code}")
    return request_id

async def get_managers_by_region(region: str):
    """Mock get managers by region"""
    return [
        {
            'id': 1,
            'full_name': 'Manager 1',
            'role': 'manager',
            'telegram_id': 123456789
        },
        {
            'id': 2,
            'full_name': 'Manager 2',
            'role': 'manager',
            'telegram_id': 987654321
        }
    ]

async def get_user_by_telegram_id_redis(telegram_id: int):
    """Mock user data from Redis"""
    return {
        'id': 1,
        'telegram_id': telegram_id,
        'role': 'client',
        'language': 'uz',
        'full_name': 'Test Client',
        'phone_number': '+998901234567',
        'phone': '+998901234567',
        'username': 'testuser'
    }

# Mock utils classes
class WorkflowEngine:
    async def create_workflow(self, workflow_type: str, client_id: int, data: dict, region_code: str):
        """Mock create workflow"""
        workflow_id = f"WF_{workflow_type}_{client_id}_{int(datetime.now().timestamp())}"
        print(f"Mock: Created workflow {workflow_id} for {workflow_type}")
        return workflow_id

class DocumentManager:
    async def generate_completion_document(self, request_id: str, workflow_type: str, db_pool):
        """Mock generate document"""
        doc_path = f"documents/{request_id}_{workflow_type}.pdf"
        print(f"Mock: Generated document {doc_path}")
        return doc_path

class ApplicationTracker:
    async def track_application(self, request_id: str, status: str):
        """Mock track application"""
        print(f"Mock: Tracking application {request_id} with status {status}")

class NotificationSystem:
    async def send_notification(self, user_id: int, message: str):
        """Mock send notification"""
        print(f"Mock: Sent notification to user {user_id}: {message}")

class AuditLogger:
    async def log_action(self, user_id: int, action: str, details: dict):
        """Mock audit logging"""
        print(f"Mock Audit Log: User {user_id} performed {action} with details {details}")

class TimeTracker:
    async def start_tracking(self, request_id: str, user_id: int, role: str, action_type: str, region_code: str):
        """Mock start time tracking"""
        print(f"Mock: Started time tracking for {request_id} by user {user_id}")

# Mock bot and constants
class MockBot:
    def __init__(self):
        self.db = {
            'toshkent': 'toshkent_pool',
            'samarqand': 'samarqand_pool',
            'clients': 'clients_pool'
        }
    
    async def send_message(self, chat_id: int, text: str, parse_mode: str = None):
        """Mock send message"""
        print(f"Mock: Sent message to {chat_id}: {text}")

bot = MockBot()
ZAYAVKA_GROUP_ID = -1001234567890

# Initialize utils
workflow_engine = WorkflowEngine()
document_manager = DocumentManager()
application_tracker = ApplicationTracker()
notification_system = NotificationSystem()
audit_logger = AuditLogger()
time_tracker = TimeTracker()

# Initialize logger at module level
logger = logging.getLogger(__name__)

def get_connection_order_router():
    from aiogram import Router
    
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔌 Ulanish uchun ariza", "🔌 Заявка на подключение"]))
    async def start_connection_order_client(message: Message, state: FSMContext):
        """Client uchun yangi ulanish arizasi - AVVAL REGION TANLASH"""
        try:
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            if not user:
                await message.answer("❌ Foydalanuvchi topilmadi. /start bosing.")
                return
            
            lang = user.get('language', 'uz')
            await state.clear()
            
            # User ma'lumotlarini saqlash
            await state.update_data(
                user_id=user.get('id'),
                telegram_id=message.from_user.id,
                user_name=user.get('full_name'),
                user_phone=user.get('phone'),
                phone_number=user.get('phone'),  # Add phone number to state
                language=lang
            )
            
            # 1. AVVAL REGION TANLASH
            region_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📍 Toshkent", callback_data="conn_region:toshkent")],
                [InlineKeyboardButton(text="📍 Samarqand", callback_data="conn_region:samarqand")]
            ])
            
            await message.answer(
                "🔌 <b>Yangi ulanish arizasi</b>\n\n"
                "📍 Qaysi regionda ulanmoqchisiz?" if lang == 'uz' else
                "🔌 <b>Новая заявка на подключение</b>\n\n"
                "📍 В каком регионе хотите подключиться?",
                reply_markup=region_keyboard,
                parse_mode='HTML'
            )
            
            await state.set_state(ConnectionOrderStates.selecting_region)
            
            # Audit log (ixtiyoriy)
            try:
                await audit_logger.log_action(
                    user_id=message.from_user.id,
                    action='connection_order_started',
                    details={'region_selection': 'initiated'}
                )
            except Exception:
                pass  # Audit xatoligi asosiy jarayonni to'xtatmasin
            
        except Exception as e:
            logger.error(f"Error in start_connection_order_client: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("conn_region:"), StateFilter(ConnectionOrderStates.selecting_region))
    async def select_region_client(callback: CallbackQuery, state: FSMContext):
        """Client uchun 2. REGION TANLANGANDAN KEYIN - ULANISH TURI"""
        try:
            await callback.answer()
            # Remove inline keyboard after selection
            await callback.message.edit_reply_markup(reply_markup=None)
            
            region = callback.data.split(":")[1]
            data = await state.get_data()
            lang = data.get('language', 'uz')
            
            # Ensure region is saved properly
            await state.update_data(selected_region=region, region=region)
            
            # 2. ULANISH TURINI SO'RASH (B2C yoki B2B)
            await callback.message.answer(
                f"✅ <b>Region:</b> {region.title()}\n\n"
                "Ulanish turini tanlang:" if lang == 'uz' else
                f"✅ <b>Регион:</b> {region.title()}\n\n"
                "Выберите тип подключения:",
                reply_markup=zayavka_type_keyboard(lang),
                parse_mode='HTML'
            )
            
            await state.set_state(ConnectionOrderStates.selecting_connection_type)
            
        except Exception as e:
            logger.error(f"Error in select_region_client: {e}")
            await callback.answer("Xatolik", show_alert=True)
    
    # Eski format uchun (backward compatibility)
    @router.callback_query(F.data.startswith("region_"), StateFilter(ConnectionOrderStates.selecting_region))
    async def select_region_old_client(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            # Remove inline keyboard after selection
            await callback.message.edit_reply_markup(reply_markup=None)
            
            region = callback.data.split("_")[-1]
            await state.update_data(selected_region=region, region=region)
            
            await callback.message.answer(
                "Ulanish turini tanlang:",
                reply_markup=zayavka_type_keyboard('uz')
            )
            
            await state.set_state(ConnectionOrderStates.selecting_connection_type)
            
        except Exception as e:
            logger.error(f"Error in select_region_old_client: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("zayavka_type_"), StateFilter(ConnectionOrderStates.selecting_connection_type))
    async def select_connection_type_client(callback: CallbackQuery, state: FSMContext):
        """Client uchun 3. ULANISH TURI TANLANGANDAN KEYIN - TARIF TANLASH"""
        try:
            await callback.answer()
            # Remove previous inline keyboard
            await callback.message.edit_reply_markup(reply_markup=None)
            
            connection_type = callback.data.split("_")[-1]  # b2c yoki b2b
            await state.update_data(connection_type=connection_type)
            
            user = await get_user_by_telegram_id_redis(callback.from_user.id)
            if not user:
                await callback.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.", show_alert=True)
                return
            
            # Tarifni rasm bilan birga ko'rsatish
            try:
                photo = FSInputFile("static/image.png")
                await callback.message.answer_photo(
                    photo=photo,
                    caption="📋 <b>Tariflardan birini tanlang:</b>\n\n"
                           "🔹 <b>Standard</b> - Oddiy ulanish tarifi\n"
                           "🔹 <b>Yangi</b> - Yangi mijozlar uchun maxsus tarif",
                    reply_markup=get_client_tariff_selection_keyboard(),
                    parse_mode='HTML'
                )
            except Exception as img_error:
                logger.warning(f"Could not send tariff image: {img_error}")
                # Fallback to text message if image fails
                await callback.message.answer(
                    "📋 <b>Tariflardan birini tanlang:</b>\n\n"
                    "🔹 <b>Standard</b> - Oddiy ulanish tarifi\n"
                    "🔹 <b>Yangi</b> - Yangi mijozlar uchun maxsus tarif",
                    reply_markup=get_client_tariff_selection_keyboard(),
                    parse_mode='HTML'
                )
            await state.set_state(ConnectionOrderStates.selecting_tariff)
            
        except Exception as e:
            logger.error(f"Error in select_connection_type_client: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.in_(["tariff_standard", "tariff_new"]))
    async def select_tariff_client(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            # Remove inline keyboard after selection
            await callback.message.edit_reply_markup(reply_markup=None)
            
            tariff = "Standard" if callback.data == "tariff_standard" else "Yangi"
            await state.update_data(selected_tariff=tariff)
            
            user = await get_user_by_telegram_id_redis(callback.from_user.id)
            if not user:
                await callback.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.", show_alert=True)
                return
            
            # Manzilni so'rash
            await callback.message.answer("📍 Manzilingizni kiriting:")
            
            await state.set_state(ConnectionOrderStates.entering_address)
            
        except Exception as e:
            logger.error(f"Error in select_tariff_client: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(ConnectionOrderStates.entering_address))
    async def get_connection_address_client(message: Message, state: FSMContext):
        try:
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            if not user:
                await message.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi. Iltimos, qaytadan kiriting.")
                return
            
            await state.update_data(address=message.text)
            
            # Geolokatsiya so'rash
            await message.answer(
                "Geolokatsiya yuborasizmi?",
                reply_markup=geolocation_keyboard('uz')
            )
            
            await state.set_state(ConnectionOrderStates.asking_for_geo)
            
        except Exception as e:
            logger.error(f"Error in get_connection_address_client: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.in_(["send_location_yes", "send_location_no"]), StateFilter(ConnectionOrderStates.asking_for_geo))
    async def ask_for_geo_client(callback: CallbackQuery, state: FSMContext):
        try:
            await callback.answer()
            # Remove inline keyboard
            await callback.message.edit_reply_markup(reply_markup=None)
            
            if callback.data == "send_location_yes":
                user = await get_user_by_telegram_id_redis(callback.from_user.id)
                if not user:
                    await callback.answer("Xatolik: Foydalanuvchi ma'lumotlari topilmadi.", show_alert=True)
                    return
                
                # Create reply keyboard for location sharing
                location_keyboard = ReplyKeyboardMarkup(
                    keyboard=[[
                        KeyboardButton(
                            text="📍 Joylashuvni yuborish",
                            request_location=True
                        )
                    ]],
                    resize_keyboard=True,
                    one_time_keyboard=True
                )
                
                await callback.message.answer(
                    "📍 Joylashuvingizni yuboring:",
                    reply_markup=location_keyboard
                )
                
                await state.set_state(ConnectionOrderStates.waiting_for_geo)
            else:
                await finish_connection_order_client(callback, state, geo=None)
            
        except Exception as e:
            logger.error(f"Error in ask_for_geo_client: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(ConnectionOrderStates.waiting_for_geo), F.location)
    async def get_geo_client(message: Message, state: FSMContext):
        try:
            await state.update_data(geo=message.location)
            
            # Remove location keyboard and return to normal keyboard
            await message.answer(
                "✅ Joylashuv qabul qilindi!",
                reply_markup=ReplyKeyboardRemove()
            )
            
            await finish_connection_order_client(message, state, geo=message.location)
            
        except Exception as e:
            logger.error(f"Error in get_geo_client: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    async def finish_connection_order_client(message_or_callback, state: FSMContext, geo=None):
        """Client uchun complete connection request submission"""
        try:
            data = await state.get_data()
            user_id = message_or_callback.from_user.id if hasattr(message_or_callback, 'from_user') else message_or_callback.message.from_user.id
            
            user = await get_user_by_telegram_id_redis(user_id)
            region = data.get('selected_region', data.get('region', 'toshkent'))
            connection_type = data.get('connection_type', 'standard')
            tariff = data.get('selected_tariff', 'Standard')
            address = data.get('address', '-')
            
            # Tasdiqlash xabari
            text = (
                f"🏛️ <b>Hudud:</b> {region.title()}\n"
                f"🔌 <b>Ulanish turi:</b> {connection_type.upper()}\n"
                f"💳 <b>Tarif:</b> {tariff}\n"
                f"🏠 <b>Manzil:</b> {address}\n"
                f"📍 <b>Geolokatsiya:</b> {'✅ Yuborilgan' if geo else '❌ Yuborilmagan'}\n\n"
                f"Ma'lumotlar to'g'rimi?"
            )
            
            if hasattr(message_or_callback, "message"):
                # Callback uchun
                await message_or_callback.message.answer(
                    text,
                    parse_mode='HTML',
                    reply_markup=confirmation_keyboard('uz')
                )
            else:
                # Message uchun
                await message_or_callback.answer(
                    text,
                    parse_mode='HTML',
                    reply_markup=confirmation_keyboard('uz')
                )
            
            await state.set_state(ConnectionOrderStates.confirming_connection)
            
        except Exception as e:
            logger.error(f"Error in finish_connection_order_client: {e}")
            if hasattr(message_or_callback, "message"):
                await message_or_callback.message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            else:
                await message_or_callback.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "confirm_zayavka", StateFilter(ConnectionOrderStates.confirming_connection))
    async def confirm_connection_order_client(callback: CallbackQuery, state: FSMContext):
        """Client zayavkasini tasdiqlash va database'ga yozish"""
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
            await callback.answer("⏳ Zayavka yaratilmoaqda...")
            
            data = await state.get_data()
            user = await get_user_by_telegram_id_redis(callback.from_user.id)
            
            # Get region from state data - ensure it's correctly saved
            region = data.get('selected_region')
            if not region:
                region = data.get('region', 'toshkent')
            
            # Ensure region is lowercase for database consistency
            region = region.lower()
            
            # Database'ga zayavka yozish - region_code ni to'g'ri uzatish
            # Use user's database ID, not telegram_id
            user_db_id = user.get('id')
            if not user_db_id:
                await callback.message.answer("❌ Foydalanuvchi ma'lumotlari topilmadi. /start bosing.")
                await state.clear()
                return
            
            request_id = await create_connection_request(
                region_code=region,  # toshkent yoki samarqand
                client_id=user_db_id,  # Use database user ID, not telegram_id
                connection_type=data.get('connection_type', 'B2C').upper(),
                tariff=data.get('selected_tariff', 'Standard'),
                address=data.get('address', 'Kiritilmagan'),
                phone=data.get('phone_number', user.get('phone', '')),
                description=f"Mijoz: {user.get('full_name')}\nRegion: {region.capitalize()}",
                geo_location=f"{geo_data.latitude},{geo_data.longitude}" if (geo_data := data.get('geo')) else None,
                telegram_id=callback.from_user.id,  # Pass telegram_id
                full_name=user.get('full_name'),  # Pass full_name
                username=user.get('username')  # Pass username
            )
            
            # Workflow boshlash
            workflow_id = await workflow_engine.create_workflow(
                workflow_type='connection_request',
                client_id=user_db_id,  # Use database user ID, not telegram_id
                data={
                    'request_id': request_id,
                    'region': region,
                    'tariff': data.get('selected_tariff'),
                    'address': data.get('address')
                },
                region_code=region
            )
            
            # Time tracking boshlash
            region_pool = bot.db.get(region)
            if region_pool:
                await time_tracker.start_tracking(
                    request_id=request_id,
                    user_id=user_db_id,  # Use database user ID, not telegram_id
                    role='client',
                    action_type='connection_request_created',
                    region_code=region
                )
            else:
                # Fallback to clients pool if region pool not found
                clients_pool = bot.db.get('clients')
                if clients_pool:
                    await time_tracker.start_tracking(
                        request_id=request_id,
                        user_id=user_db_id,  # Use database user ID, not telegram_id
                        role='client',
                        action_type='connection_request_created',
                        region_code=region
                    )
            
            # Hujjat yaratish
            region_pool = bot.db.get(region)
            if region_pool:
                doc_path = await document_manager.generate_completion_document(
                    request_id=request_id,
                    workflow_type='connection_request',
                    db_pool=region_pool
                )
            else:
                # Fallback to clients pool if region pool not found
                clients_pool = bot.db.get('clients')
                if clients_pool:
                    doc_path = await document_manager.generate_completion_document(
                        request_id=request_id,
                        workflow_type='connection_request',
                        db_pool=clients_pool
                    )
                else:
                    doc_path = None
            
            # Guruhga xabar yuborish (batafsil)
            if ZAYAVKA_GROUP_ID:
                try:
                    geo_text = ""
                    geo_data = data.get('geo')
                    if geo_data:
                        geo_text = f"\n📍 <b>Lokatsiya:</b> <a href='https://maps.google.com/?q={geo_data.latitude},{geo_data.longitude}'>Google Maps</a>"
                    
                    group_msg = (
                        f"🔌 <b>YANGI ULANISH ARIZASI</b>\n"
                        f"{'='*30}\n"
                        f"🆔 <b>ID:</b> <code>{request_id}</code>\n"
                        f"👤 <b>Mijoz:</b> {user.get('full_name')}\n"
                        f"📞 <b>Tel:</b> {data.get('phone_number', user.get('phone'))}\n"
                        f"🏢 <b>Region:</b> {region.title()}\n"
                        f"🔌 <b>Turi:</b> {data.get('connection_type', 'B2C').upper()}\n"
                        f"💳 <b>Tarif:</b> {data.get('selected_tariff')}\n"
                        f"📍 <b>Manzil:</b> {data.get('address')}"
                        f"{geo_text}\n"
                        f"🕐 <b>Vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                        f"{'='*30}"
                    )
                    
                    await bot.send_message(
                        chat_id=ZAYAVKA_GROUP_ID,
                        text=group_msg,
                        parse_mode='HTML'
                    )
                except Exception as group_error:
                    # Group notification error - handle silently
                    pass
            
            # Manager'larga qisqa xabar yuborish (1 qatorli)
            managers = await get_managers_by_region(region)
            for manager in managers:
                try:
                    # Qisqa 1 qatorli xabar
                    short_msg = f"🔌 Yangi ariza #{request_id} | {user.get('full_name')} | {region.title()} | {data.get('selected_tariff')}"
                    
                    await bot.send_message(
                        chat_id=manager['telegram_id'],
                        text=short_msg
                    )
                except Exception as notify_error:
                    # Manager notification error - handle silently
                    pass
            
            # Success message with main menu button (only one message)
            from keyboards.client_buttons import get_main_menu_keyboard
            success_msg = (
                f"✅ <b>Arizangiz muvaffaqiyatli qabul qilindi!</b>\n\n"
                f"🆔 Ariza raqami: <code>{request_id}</code>\n"
                f"📍 Hudud: {region.title()}\n"
                f"💳 Tarif: {data.get('selected_tariff')}\n"
                f"📞 Telefon: {data.get('phone_number', user.get('phone'))}\n"
                f"📍 Manzil: {data.get('address')}\n\n"
                f"⏰ Menejerlarimiz tez orada siz bilan bog'lanadi!\n"
                f"📊 Ariza holatini <b>Kabinet</b> bo'limidan kuzatishingiz mumkin."
            )
            await callback.message.answer(
                success_msg,
                parse_mode='HTML',
                reply_markup=get_main_menu_keyboard('uz')
            )
            
            await state.clear()
            
        except Exception as e:
            # Use universal error logger for detailed error information
            try:
                from utils.universal_error_logger import log_error
                log_error(
                    error=e, 
                    context="Connection order confirmation failed", 
                    user_id=callback.from_user.id,
                    **{
                        'state_data': data,
                        'user_info': user,
                        'region': region,
                        'connection_type': data.get('connection_type'),
                        'tariff': data.get('selected_tariff'),
                        'address': data.get('address'),
                        'phone': data.get('phone_number')
                    }
                )
            except ImportError:
                # Fallback to regular logging if universal logger is not available
                logger.error(f"Error in confirm_connection_order_client: {e}")
                logger.error(f"State data: {data}")
                logger.error(f"User info: {user}")
            
            await callback.message.answer(
                "❌0 Zayavka yaratishda xatolik. Qaytadan urinib ko'ring.",
                parse_mode='HTML'
            )
            await state.clear()
    
    @router.callback_query(F.data == "resend_zayavka", StateFilter(ConnectionOrderStates.confirming_connection))
    async def resend_connection_order_client(callback: CallbackQuery, state: FSMContext):
        """Client zayavkasini qayta yuborish"""
        try:
            await callback.answer("Qayta yuborish...")
            await callback.message.edit_reply_markup(reply_markup=None)
            
            # Start over from region selection
            await state.clear()
            
            user = await get_user_by_telegram_id_redis(callback.from_user.id)
            lang = user.get('language', 'uz')
            
            # User ma'lumotlarini saqlash
            await state.update_data(
                user_id=user.get('id'),
                telegram_id=callback.from_user.id,
                user_name=user.get('full_name'),
                user_phone=user.get('phone'),
                phone_number=user.get('phone'),
                language=lang
            )
            
            # 1. AVVAL REGION TANLASH
            region_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📍 Toshkent", callback_data="conn_region:toshkent")],
                [InlineKeyboardButton(text="📍 Samarqand", callback_data="conn_region:samarqand")]
            ])
            
            await callback.message.answer(
                "🔌 <b>Yangi ulanish arizasi</b>\n\n"
                "📍 Qaysi regionda ulanmoqchisiz?" if lang == 'uz' else
                "🔌 <b>Новая заявка на подключение</b>\n\n"
                "📍 В каком регионе хотите подключиться?",
                reply_markup=region_keyboard,
                parse_mode='HTML'
            )
            
            await state.set_state(ConnectionOrderStates.selecting_region)
            
        except Exception as e:
            # Fallback logging - try logger first, then print if logger is not defined
            try:
                logger.error(f"Error in resend_connection_order_client: {e}")
            except NameError:
                print(f"Fallback log: Error in resend_connection_order_client: {e}")
                # Also try to log to a basic logger
                try:
                    import logging
                    basic_logger = logging.getLogger(__name__)
                    basic_logger.error(f"Error in resend_connection_order_client: {e}")
                except:
                    pass
            
            await callback.answer("Xatolik yuz berdi", show_alert=True)
    
    @router.callback_query(F.data == "conn_cancel")
    async def cancel_connection_order_client(callback: CallbackQuery, state: FSMContext):
        """Client zayavkasini bekor qilish"""
        try:
            await callback.answer("Bekor qilindi")
            await state.clear()
            
            await callback.message.edit_text(
                "❌ Ulanish arizasi bekor qilindi.",
                parse_mode='HTML'
            )
            
            # Main menu
            from keyboards.client_buttons import get_main_menu_keyboard
            await callback.message.answer(
                "Bosh menyu:",
                reply_markup=get_main_menu_keyboard('uz')
            )
            
        except Exception as e:
            # Fallback logging - try logger first, then print if logger is not defined
            try:
                logger.error(f"Error in cancel_connection_order_client: {e}")
            except NameError:
                print(f"Fallback log: Error in cancel_connection_order_client: {e}")
                # Also try to log to a basic logger
                try:
                    import logging
                    basic_logger = logging.getLogger(__name__)
                    basic_logger.error(f"Error in cancel_connection_order_client: {e}")
                except:
                    pass
            
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router


