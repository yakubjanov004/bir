"""
Client Service Order Handler - Full Database Integration

Texnik xizmat zayavkalari uchun handler
Client'dan so'raladigan ma'lumotlar:
1. Region (Toshkent/Samarqand)
2. Abonent turi (Jismoniy/Yuridik)
3. Abonent ID
4. Muammo tavsifi
5. Sabab (Texnik xizmatga muhtoj bo'lgan sabab)
6. Manzil
7. Media (rasm/video) - ixtiyoriy
8. Geolokatsiya - ixtiyoriy
"""

from datetime import datetime
from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.client_buttons import (
    get_main_menu_keyboard,
    zayavka_type_keyboard,
    geolocation_keyboard,
    media_attachment_keyboard
)
from states.client_states import OrderStates
from filters.role_filter import RoleFilter

# Mock database functions to replace database imports
async def create_technical_service_request(region_code: str, client_id: int, description: str, phone: str, address: str, geo_location: dict = None, abonent_type: str = None, abonent_id: str = None, media_info: list = None, telegram_id: int = None, full_name: str = None, username: str = None, reason: str = None):
    """Mock create technical service request"""
    request_id = f"TX_{telegram_id}_{int(datetime.now().timestamp())}"
    print(f"Mock: Created technical service request {request_id} for client {client_id} in region {region_code}")
    print(f"Mock: Reason: {reason}")
    return request_id

async def get_controllers_by_region(region: str):
    """Mock get controllers by region"""
    return [
        {
            'id': 1,
            'full_name': 'Controller 1',
            'role': 'controller',
            'telegram_id': 123456789
        },
        {
            'id': 2,
            'full_name': 'Controller 2',
            'role': 'controller',
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
    async def generate_service_document(self, request_id: str, client_name: str, phone: str, address: str, abonent_id: str, abonent_type: str, description: str, reason: str, region: str):
        """Mock generate service document"""
        doc_path = f"documents/{request_id}_technical_service.docx"
        print(f"Mock: Generated service document {doc_path} with reason: {reason}")
        return doc_path

class ApplicationTracker:
    async def create_application(self, workflow_type: str, client_id: int, description: str, location: str, priority: str, metadata: dict):
        """Mock create application"""
        app_id = f"APP_{workflow_type}_{client_id}_{int(datetime.now().timestamp())}"
        print(f"Mock: Created application {app_id} with metadata: {metadata}")
        return app_id

class NotificationSystem:
    async def send_notification(self, user_id: int, message: str):
        """Mock send notification"""
        print(f"Mock: Sent notification to user {user_id}: {message}")

class AuditLogger:
    async def log_action(self, user_id: int, action: str, details: dict):
        """Mock audit logging"""
        print(f"Mock Audit Log: User {user_id} performed {action} with details {details}")

# Mock bot and constants
class MockBot:
    def __init__(self):
        pass
    
    async def send_message(self, chat_id: int, text: str, parse_mode: str = None):
        """Mock send message"""
        print(f"Mock: Sent message to {chat_id}: {text}")
    
    async def send_photo(self, chat_id: int, photo: str):
        """Mock send photo"""
        print(f"Mock: Sent photo to {chat_id}: {photo}")
    
    async def send_video(self, chat_id: int, video: str):
        """Mock send video"""
        print(f"Mock: Sent video to {chat_id}: {video}")
    
    async def send_location(self, chat_id: int, latitude: float, longitude: float):
        """Mock send location"""
        print(f"Mock: Sent location to {chat_id}: {latitude}, {longitude}")

bot = MockBot()
ZAYAVKA_GROUP_ID = -1001234567890

# Initialize utils
workflow_engine = WorkflowEngine()
document_manager = DocumentManager()
application_tracker = ApplicationTracker()
notification_system = NotificationSystem()
audit_logger = AuditLogger()

def get_service_order_router():
    from aiogram import Router
    import logging
    logger = logging.getLogger(__name__)
    
    router = Router()
    
    role_filter = RoleFilter("client")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["🔧 Texnik xizmat", "🔧 Техническая служба"]))
    async def start_service_order(message: Message, state: FSMContext):
        """1. BOSHLASH - REGION TANLASH"""
        try:
            user = await get_user_by_telegram_id_redis(message.from_user.id)
            if not user:
                await message.answer("❌ Foydalanuvchi topilmadi. /start bosing.")
                return
            
            lang = user.get('language', 'uz')
            await state.clear()  # Reason field bilan state tozalash
            
            await state.update_data(
                user_id=user.get('id'),
                telegram_id=message.from_user.id,
                user_name=user.get('full_name'),
                user_phone=user.get('phone'),
                phone_number=user.get('phone'),  # Add phone number to state
                language=lang
            )
            
            # Audit log
            try:
                await audit_logger.log_action(
                    user_id=message.from_user.id,
                    action='service_order_started',
                    details={'step': 'region_selection'}
                )
            except Exception:
                pass
            
            # REGION TANLASH
            region_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📍 Toshkent", callback_data="service_region:toshkent")],
                [InlineKeyboardButton(text="📍 Samarqand", callback_data="service_region:samarqand")]
            ])
            
            await message.answer(
                "🔧 <b>Texnik xizmat arizasi</b>\n\n"
                "📍 Qaysi hududda xizmat kerak?" if lang == 'uz' else
                "🔧 <b>Заявка на техническое обслуживание</b>\n\n"
                "📍 В каком регионе нужна услуга?",
                reply_markup=region_keyboard,
                parse_mode='HTML'
            )
            
            await state.set_state(OrderStates.selecting_region)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            await message.answer("❌ Xatolik yuz berdi.")

    @router.callback_query(F.data.startswith("service_region:"), StateFilter(OrderStates.selecting_region))
    async def select_region(callback: CallbackQuery, state: FSMContext):
        """2. REGION TANLANDI - ABONENT TURI"""
        try:
            await callback.answer()
            # Remove inline keyboard after selection
            await callback.message.edit_reply_markup(reply_markup=None)
            
            region = callback.data.split(":")[1]
            data = await state.get_data()
            lang = data.get('language', 'uz')
            
            # Ensure region is saved properly
            await state.update_data(selected_region=region, region=region)
            # Tarif selection without image
            await callback.message.answer(
                f"✅ <b>Hudud:</b> {region.title()}\n\n"
                "Abonent turini tanlang:" if lang == 'uz' else
                f"✅ <b>Регион:</b> {region.title()}\n\n"
                "Выберите тип абонента:",
                reply_markup=zayavka_type_keyboard(lang),
                parse_mode='HTML'
            )
            
            
            await state.set_state(OrderStates.selecting_order_type)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("zayavka_type_"), StateFilter(OrderStates.selecting_order_type))
    async def select_abonent_type(callback: CallbackQuery, state: FSMContext):
        """3. ABONENT TURI TANLANDI - ABONENT ID SO'RASH"""
        try:
            await callback.answer()
            # Remove inline keyboard after selection
            await callback.message.edit_reply_markup(reply_markup=None)
            
            abonent_type = callback.data.split("_")[-1].upper()  # B2C yoki B2B
            await state.update_data(abonent_type=abonent_type)
            
            data = await state.get_data()
            lang = data.get('language', 'uz')
            
            await callback.message.answer(
                "🆔 Abonent ID raqamingizni kiriting:" if lang == 'uz' else
                "🆔 Введите ваш абонентский ID:"
            )
            
            await state.set_state(OrderStates.waiting_for_contact)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(OrderStates.waiting_for_contact), F.text)
    async def get_abonent_id(message: Message, state: FSMContext):
        """4. ABONENT ID KIRITILDI - MUAMMO TAVSIFI"""
        try:
            await state.update_data(abonent_id=message.text)
            
            data = await state.get_data()
            lang = data.get('language', 'uz')
            
            await message.answer(
                "📝 Muammoni batafsil yozing:" if lang == 'uz' else
                "📝 Опишите проблему подробно:"
            )
            
            await state.set_state(OrderStates.entering_reason)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")



    @router.message(StateFilter(OrderStates.entering_reason), F.text)
    async def get_reason(message: Message, state: FSMContext):
        """6. SABAB KIRITILDI - MANZIL SO'RASH"""
        try:
            await state.update_data(reason=message.text)
            
            data = await state.get_data()
            lang = data.get('language', 'uz')
            
            await message.answer(
                "📍 Manzilingizni kiriting:" if lang == 'uz' else
                "📍 Введите ваш адрес:"
            )
            
            await state.set_state(OrderStates.entering_address)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

    @router.message(StateFilter(OrderStates.entering_address), F.text)
    async def get_address(message: Message, state: FSMContext):
        """7. MANZIL KIRITILDI - MEDIA SO'RASH"""
        try:
            await state.update_data(address=message.text)
            
            data = await state.get_data()
            lang = data.get('language', 'uz')
            
            # MEDIA (RASM/VIDEO) SO'RASH
            await message.answer(
                "📷 Muammo rasmi yoki videosini yuborasizmi?" if lang == 'uz' else
                "📷 Хотите отправить фото или видео проблемы?",
                reply_markup=media_attachment_keyboard(lang)
            )
            
            await state.set_state(OrderStates.asking_for_media)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

    @router.callback_query(F.data.in_(["attach_media_yes", "attach_media_no"]), StateFilter(OrderStates.asking_for_media))
    async def ask_for_media(callback: CallbackQuery, state: FSMContext):
        """8. MEDIA QARORI"""
        try:
            await callback.answer()
            # Remove inline keyboard
            await callback.message.edit_reply_markup(reply_markup=None)
            
            if callback.data == "attach_media_yes":
                data = await state.get_data()
                lang = data.get('language', 'uz')
                
                await callback.message.answer(
                    "📷 Rasm yoki video yuboring:" if lang == 'uz' else
                    "📷 Отправьте фото или видео:"
                )
                await state.set_state(OrderStates.waiting_for_media)
            else:
                # Media'siz davom etish - geolokatsiya so'rash
                await ask_for_geolocation(callback.message, state)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(OrderStates.waiting_for_media), F.photo | F.video)
    async def get_media(message: Message, state: FSMContext):
        """9. MEDIA OLINDI - GEOLOKATSIYA SO'RASH"""
        try:
            # Media ma'lumotlarini saqlash
            if message.photo:
                media_id = message.photo[-1].file_id
                media_type = 'photo'
            elif message.video:
                media_id = message.video.file_id
                media_type = 'video'
            else:
                media_id = None
                media_type = None
            
            await state.update_data(media_id=media_id, media_type=media_type)
            
            # Geolokatsiya so'rash
            await ask_for_geolocation(message, state)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

    async def ask_for_geolocation(message, state: FSMContext):
        """GEOLOKATSIYA SO'RASH"""
        data = await state.get_data()
        lang = data.get('language', 'uz')
        
        await message.answer(
            "📍 Geolokatsiya yuborasizmi?" if lang == 'uz' else
            "📍 Хотите отправить геолокацию?",
            reply_markup=geolocation_keyboard(lang)
        )
        await state.set_state(OrderStates.asking_for_location)

    @router.callback_query(F.data.in_(["send_location_yes", "send_location_no"]), StateFilter(OrderStates.asking_for_location))
    async def geo_decision(callback: CallbackQuery, state: FSMContext):
        """10. GEOLOKATSIYA QARORI"""
        try:
            await callback.answer()
            # Remove inline keyboard
            await callback.message.edit_reply_markup(reply_markup=None)
            
            if callback.data == "send_location_yes":
                data = await state.get_data()
                lang = data.get('language', 'uz')
                
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
                    "📍 Joylashuvingizni yuboring:" if lang == 'uz' else
                    "📍 Отправьте вашу локацию:",
                    reply_markup=location_keyboard
                )
                await state.set_state(OrderStates.waiting_for_location)
            else:
                await finish_service_order(callback.message, state, geo=None)
            
        except Exception as e:
            logger.error(f"Error: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(StateFilter(OrderStates.waiting_for_location), F.location)
    async def get_geo(message: Message, state: FSMContext):
        """11. GEOLOKATSIYA OLINDI - YAKUNLASH"""
        try:
            await state.update_data(geo=message.location)
            
            # Remove location keyboard
            await message.answer(
                "✅ Joylashuv qabul qilindi!",
                reply_markup=ReplyKeyboardRemove()
            )
            
            await finish_service_order(message, state, geo=message.location)
        except Exception as e:
            logger.error(f"Error: {e}")
            await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")

    async def finish_service_order(message, state: FSMContext, geo=None):
        """YAKUNLASH - 6 TA UTILS INTEGRATSIYA (reason field qo'shildi)"""
        try:
            data = await state.get_data()
            user = await get_user_by_telegram_id_redis(data['telegram_id'])
            
            # Get region from state data - ensure it's correctly saved
            region = data.get('selected_region')
            if not region:
                region = data.get('region', 'toshkent')
            
            # Ensure region is lowercase for database consistency
            region = region.lower()
            
            # 1. DATABASE - zayavka yaratish (reason field bilan)
            request_id = await create_technical_service_request(
                region_code=region,
                client_id=user['id'],
                description=data.get('description', ''),
                phone=data.get('phone_number', user.get('phone', '')),
                address=data.get('address', ''),
                geo_location={"latitude": geo.latitude, "longitude": geo.longitude} if geo else None,
                abonent_type=data.get('abonent_type', ''),
                abonent_id=data.get('abonent_id', ''),
                media_info=[data.get('media_id')] if data.get('media_id') else None,  
                telegram_id=data['telegram_id'],
                full_name=user.get('full_name', ''),
                username=user.get('username', ''),
                reason=data.get('reason', '')  
            )
            
            # 1.5. APPLICATION TRACKER - tracking uchun (reason field bilan)
            await application_tracker.create_application(
                workflow_type='technical_service',
                client_id=user['id'],  # Use database user ID, not telegram_id
                description=data.get('description', ''),
                location=data.get('address', ''),
                priority='high',
                metadata={
                    'request_id': request_id,
                    'reason': data.get('reason', '')
                }
            )
            
            # 2. WORKFLOW ENGINE - jarayonni boshlash (reason field bilan)
            workflow_id = await workflow_engine.create_workflow(
                workflow_type='technical_service',
                client_id=user['id'],  # Use database user ID, not telegram_id
                data={
                    'request_id': request_id,
                    'region': region,
                    'abonent_id': data.get('abonent_id'),
                    'description': data.get('description'),
                    'address': data.get('address'),
                    'reason': data.get('reason', '')
                },
                region_code=region
            )
            
            # 3. DOCUMENT MANAGER - Word hujjat (reason field bilan)
            doc_path = await document_manager.generate_service_document(
                request_id=request_id,
                client_name=user.get('full_name'),
                phone=data.get('phone_number', user.get('phone')),
                address=data.get('address'),
                abonent_id=data.get('abonent_id'),
                abonent_type=data.get('abonent_type'),
                description=data.get('description'),
                reason=data.get('reason', ''),
                region=region
            )
            
            # 4. NOTIFICATION SYSTEM - xabarlar (reason field bilan)
            # Guruhga batafsil xabar yuborish (reason field bilan)
            if ZAYAVKA_GROUP_ID:
                try:
                    geo_text = ""
                    if geo:
                        geo_text = f"\n📍 <b>Lokatsiya:</b> <a href='https://maps.google.com/?q={geo.latitude},{geo.longitude}'>Google Maps</a>"
                    
                    group_msg = (
                        f"🔧 <b>YANGI TEXNIK XIZMAT ARIZASI</b>\n"
                        f"{'='*30}\n"
                        f"🆔 <b>ID:</b> <code>{request_id}</code>\n"
                        f"👤 <b>Mijoz:</b> {user.get('full_name')}\n"
                        f"📞 <b>Tel:</b> {data.get('phone_number', user.get('phone'))}\n"
                        f"🏢 <b>Hudud:</b> {region.title()}\n"
                        f"🏢 <b>Abonent:</b> {data.get('abonent_type')} - {data.get('abonent_id')}\n"
                        f"📍 <b>Manzil:</b> {data.get('address')}\n"
                        f"📝 <b>Muammo:</b> {data.get('description')[:100]}...\n"
                        f"📋 <b>Sabab:</b> {data.get('reason', '')[:100]}..."
                        f"{geo_text}\n"
                        f"📷 <b>Media:</b> {'✅ Mavjud' if data.get('media_id') else '❌ Yo`q'}\n"
                        f"🕐 <b>Vaqt:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
                        f"{'='*30}"
                    )
                    
                    # Xabar yuborish
                    await bot.send_message(
                        chat_id=ZAYAVKA_GROUP_ID,
                        text=group_msg,
                        parse_mode='HTML'
                    )
                    
                    # Media yuborish (reason field bilan)
                    if data.get('media_id'):
                        if data.get('media_type') == 'photo':
                            await bot.send_photo(ZAYAVKA_GROUP_ID, photo=data['media_id'])
                        elif data.get('media_type') == 'video':
                            await bot.send_video(ZAYAVKA_GROUP_ID, video=data['media_id'])
                    
                    # Geolokatsiya yuborish (reason field bilan)
                    if geo:
                        await bot.send_location(ZAYAVKA_GROUP_ID, latitude=geo.latitude, longitude=geo.longitude)
                    
                except Exception as group_error:
                    logger.error(f"Group notification error: {group_error}")
            
            # Controller'larga qisqa xabar yuborish (reason field bilan)
            controllers = await get_controllers_by_region(region)
            for controller in controllers:
                try:
                    # Qisqa xabar (reason field bilan)
                    short_msg = f"🔧 Yangi texnik #{request_id} | {user.get('full_name')} | {region.title()} | {data.get('abonent_id')} | Sabab: {data.get('reason', '')[:50]}..."
                    
                    await bot.send_message(
                        chat_id=controller['telegram_id'],
                        text=short_msg
                    )
                except Exception as notify_error:
                    logger.error(f"Controller notify error: {notify_error}")
            
            # 5. AUDIT LOGGER - muhim harakat (reason field bilan)
            try:
                await audit_logger.log_action(
                    user_id=data['telegram_id'],
                    action='service_request_completed',
                    details={
                        'request_id': request_id,
                        'region': region,
                        'workflow_id': workflow_id,
                        'abonent_id': data.get('abonent_id'),
                        'reason': data.get('reason', ''),
                        'has_media': bool(data.get('media_id')),
                        'has_geo': bool(geo)
                    }
                )
            except Exception:
                pass
            
            # Mijozga javob (reason field bilan)
            lang = data.get('language', 'uz')
            await message.answer(
                f"✅ <b>Texnik xizmat arizangiz qabul qilindi!</b>\n\n"
                f"🆔 Ariza raqami: <code>{request_id}</code>\n"
                f"📍 Hudud: {region.title()}\n"
                f"🏢 Abonent ID: {data.get('abonent_id')}\n"
                f"📍 Manzil: {data.get('address')}\n"
                f"📋 Sabab: {data.get('reason', '')}\n\n"
                f"⏰ Texnik mutaxassis tez orada bog'lanadi!\n"
                f"📊 Ariza holatini <b>Kabinet</b> bo'limidan kuzatishingiz mumkin." if lang == 'uz' else
                f"✅ <b>Ваша заявка на техобслуживание принята!</b>\n\n"
                f"🆔 Номер заявки: <code>{request_id}</code>\n"
                f"📍 Регион: {region.title()}\n"
                f"🏢 Абонент ID: {data.get('abonent_id')}\n"
                f"📍 Адрес: {data.get('address')}\n"
                f"📋 Причина: {data.get('reason', '')}\n\n"
                f"⏰ Технический специалист скоро свяжется!\n"
                f"📊 Статус заявки можно отслеживать в разделе <b>Кабинет</b>.",
                parse_mode='HTML',
                reply_markup=get_main_menu_keyboard(lang)
            )
            
            await state.clear()
            
        except Exception as e:
            logger.error(f"Error in finish_service_order: {e}")
            logger.error(f"Full error details: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            await message.answer("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.", reply_markup=get_main_menu_keyboard('uz'))
            await state.clear()  # Reason field bilan state tozalash

    @router.callback_query(F.data == "service_cancel")
    async def cancel_order(callback: CallbackQuery, state: FSMContext):
        """BEKOR QILISH"""
        try:
            await callback.answer("Bekor qilindi")
            await callback.message.edit_reply_markup(reply_markup=None)
            
            data = await state.get_data()
            lang = data.get('language', 'uz')
            
            await state.clear()  # Reason field bilan state tozalash
            
            await callback.message.answer(
                "❌ Texnik xizmat arizasi bekor qilindi" if lang == 'uz' else
                "❌ Заявка на техобслуживание отменена",
                reply_markup=get_main_menu_keyboard(lang)
            )
        except Exception as e:
            logger.error(f"Error in cancel_order: {e}")
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router


