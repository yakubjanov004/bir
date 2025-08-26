"""
Admin Users Handler
Manages admin user management
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from functools import wraps
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.admin_buttons import get_users_keyboard

# States imports
from states.admin_states import AdminUsersStates, AdminMainMenuStates
from filters.role_filter import RoleFilter

def get_admin_users_router():
    """Get admin users router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("admin")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(StateFilter(AdminMainMenuStates.main_menu), F.text.in_(["👥 Foydalanuvchilar", "👥 Пользователи"]))
    async def users_menu(message: Message, state: FSMContext):
        """Users main menu"""
        text = "👥 <b>Foydalanuvchilar boshqaruvi</b>\n\nFoydalanuvchilarni boshqarish uchun turini tanlang."
        
        sent_message = await message.answer(
            text,
            reply_markup=get_users_keyboard('uz')
        )
        await state.set_state(AdminUsersStates.users)

    @router.message(F.text.in_(["🔍 Foydalanuvchi qidirish", "🔍 Поиск пользователя"]))
    async def search_user(message: Message, state: FSMContext):
        """Search user interface"""
        text = (
            f"🔍 <b>Foydalanuvchi qidirish</b>\n\n"
            f"Qidirish uchun quyidagi ma'lumotlardan birini kiriting:\n\n"
            f"📱 <b>Telefon raqam:</b>\n"
            f"Masalan: +998 90 123 45 67\n\n"
            f"👤 <b>Ism:</b>\n"
            f"Masalan: Bekzod Toirov\n\n"
            f"🆔 <b>Telegram ID:</b>\n"
            f"Masalan: 123456789\n\n"
            f"📧 <b>Email:</b>\n"
            f"Masalan: user@example.com\n\n"
            f"Qidirish ma'lumotini yuboring:"
        )
        
        await message.answer(text)
        await state.set_state(AdminUsersStates.waiting_for_search_query)

    @router.message(AdminUsersStates.waiting_for_search_query)
    async def process_search_query(message: Message, state: FSMContext):
        """Process search query"""
        search_query = message.text.strip()
        
        if not search_query:
            await message.answer("Iltimos, qidirish ma'lumotini kiriting.")
            return
            
        # Mock search results
        search_results = [
            {
                'id': 1,
                'name': 'Bekzod Toirov',
                'phone': '+998 90 123 45 67',
                'telegram_id': 123456789,
                'role': 'client',
                'status': 'active',
                'created_at': '2024-01-15',
                'last_activity': '2024-08-05 14:30'
            },
            {
                'id': 2,
                'name': 'Aziz Karimov',
                'phone': '+998 91 234 56 78',
                'telegram_id': 987654321,
                'role': 'technician',
                'status': 'active',
                'created_at': '2024-02-20',
                'last_activity': '2024-08-05 15:45'
            }
        ]
        
        if not search_results:
            text = f"❌ '{search_query}' bo'yicha foydalanuvchi topilmadi."
            await message.answer(text)
            await state.clear()
            return
            
        text = f"🔍 <b>Qidirish natijalari</b>\n\n"
        text += f"'{search_query}' bo'yicha {len(search_results)} ta foydalanuvchi topildi:\n\n"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        
        for i, user in enumerate(search_results, 1):
            role_names = {
                'client': 'Mijoz',
                'technician': 'Texnik',
                'manager': 'Menejer',
                'admin': 'Admin',
                'call_center': 'Call Center',
                'controller': 'Kontroller',
                'warehouse': 'Ombor',
                'junior_manager': 'Junior Menejer'
            }
            
            role_name = role_names.get(user['role'], user['role'])
            status_emoji = "🟢" if user['status'] == 'active' else "🔴"
            
            text += (
                f"{i}. <b>{user['name']}</b>\n"
                f"   📱 {user['phone']}\n"
                f"   👤 {role_name} {status_emoji}\n"
                f"   📅 Ro'yxatdan: {user['created_at']}\n"
                f"   ⏰ So'nggi faollik: {user['last_activity']}\n\n"
            )
            
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text=f"👤 {user['name']}",
                    callback_data=f"view_user_{user['id']}"
                )
            ])
        
        await message.answer(text, reply_markup=keyboard)
        await state.clear()

    @router.message(F.text.in_(["📋 Foydalanuvchilar ro'yxati", "📋 Список пользователей"]))
    async def users_list(message: Message):
        """Show users list"""
        # Mock users list
        users = [
            {
                'id': 1,
                'name': 'Bekzod Toirov',
                'phone': '+998 90 123 45 67',
                'role': 'client',
                'status': 'active',
                'region': 'Toshkent',
                'orders_count': 15
            },
            {
                'id': 2,
                'name': 'Aziz Karimov',
                'phone': '+998 91 234 56 78',
                'role': 'technician',
                'status': 'active',
                'region': 'Toshkent',
                'orders_count': 156
            },
            {
                'id': 3,
                'name': 'Dilshod Rahimov',
                'phone': '+998 92 345 67 89',
                'role': 'manager',
                'status': 'active',
                'region': 'Samarqand',
                'orders_count': 89
            },
            {
                'id': 4,
                'name': 'Olimjon Karimov',
                'phone': '+998 93 456 78 90',
                'role': 'client',
                'status': 'inactive',
                'region': 'Buxoro',
                'orders_count': 3
            }
        ]
        
        text = f"📋 <b>Foydalanuvchilar ro'yxati</b>\n\n"
        text += f"Jami: {len(users)} ta foydalanuvchi\n\n"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        
        for user in users:
            role_names = {
                'client': 'Mijoz',
                'technician': 'Texnik',
                'manager': 'Menejer',
                'admin': 'Admin',
                        'call_center': 'Call Center',
                'controller': 'Kontroller',
                'warehouse': 'Ombor',
                'junior_manager': 'Junior Menejer'
            }
            
            role_name = role_names.get(user['role'], user['role'])
            status_emoji = "🟢" if user['status'] == 'active' else "🔴"
            
            text += (
                f"👤 <b>{user['name']}</b>\n"
                f"   📱 {user['phone']}\n"
                f"   👤 {role_name} {status_emoji}\n"
                f"   🌍 {user['region']}\n"
                f"   📋 Zayavkalar: {user['orders_count']}\n\n"
            )
            
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text=f"👤 {user['name']}",
                    callback_data=f"view_user_{user['id']}"
                )
            ])
        
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text="📊 Barcha foydalanuvchilar",
                callback_data="view_all_users"
            )
        ])
        
        await message.answer(text, reply_markup=keyboard)

    @router.message(F.text.in_(["➕ Yangi foydalanuvchi qo'shish", "➕ Добавить пользователя"]))
    async def add_user(message: Message, state: FSMContext):
        """Add new user interface"""
        text = (
            f"➕ <b>Yangi foydalanuvchi qo'shish</b>\n\n"
            f"Yangi foydalanuvchi ma'lumotlarini kiriting:\n\n"
            f"👤 <b>To'liq ism:</b>\n"
            f"📱 <b>Telefon raqam:</b>\n"
            f"👤 <b>Rol:</b> (client/technician/manager/admin)\n"
            f"🌍 <b>Hudud:</b>\n"
            f"📧 <b>Email:</b> (ixtiyoriy)\n\n"
            f"Ma'lumotlarni quyidagi formatda kiriting:\n"
            f"<code>Ism|Telefon|Rol|Hudud|Email</code>\n\n"
            f"Masalan:\n"
            f"<code>Bekzod Toirov|+998 90 123 45 67|client|Toshkent|bekzod@example.com</code>"
        )
        
        await message.answer(text)
        await state.set_state(AdminUsersStates.waiting_for_user_data)

    @router.message(AdminUsersStates.waiting_for_user_data)
    async def process_user_data(message: Message, state: FSMContext):
        """Process new user data"""
        user_data = message.text.strip()
        
        if not user_data or '|' not in user_data:
            await message.answer("Iltimos, ma'lumotlarni to'g'ri formatda kiriting.")
            return
            
        try:
            parts = user_data.split('|')
            if len(parts) < 4:
                await message.answer("Iltimos, barcha majburiy ma'lumotlarni kiriting.")
                return
            
            name = parts[0].strip()
            phone = parts[1].strip()
            role = parts[2].strip()
            region = parts[3].strip()
            email = parts[4].strip() if len(parts) > 4 else ""
            
            # Mock user creation
            new_user = {
                'id': 999,
                'name': name,
                'phone': phone,
                'role': role,
                'region': region,
                'email': email,
                'status': 'active',
                'created_at': datetime.now().strftime('%Y-%m-%d')
            }
            
            text = (
                f"✅ <b>Yangi foydalanuvchi qo'shildi</b>\n\n"
                f"👤 <b>Ism:</b> {new_user['name']}\n"
                f"📱 <b>Telefon:</b> {new_user['phone']}\n"
                f"👤 <b>Rol:</b> {new_user['role']}\n"
                f"🌍 <b>Hudud:</b> {new_user['region']}\n"
                f"📧 <b>Email:</b> {new_user['email'] or 'Kiritilmagan'}\n"
                f"📅 <b>Yaratilgan:</b> {new_user['created_at']}\n"
                f"🆔 <b>ID:</b> {new_user['id']}"
            )
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="👤 Foydalanuvchini ko'rish",
                        callback_data=f"view_user_{new_user['id']}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="✏️ Tahrirlash",
                        callback_data=f"edit_user_{new_user['id']}"
                    )
                ]
            ])
            
            await message.answer(text, reply_markup=keyboard)
            
        except Exception as e:
            # await message.answer(f"Xatolik yuz berdi: {str(e)}")
            pass
        
        await state.clear()

    @router.message(F.text.in_(["👤 Foydalanuvchi profili", "👤 Профиль пользователя"]))
    async def user_profile(message: Message, state: FSMContext):
        """Show user profile interface"""
        text = (
            f"👤 <b>Foydalanuvchi profili</b>\n\n"
            f"Foydalanuvchi ID yoki telefon raqamini kiriting:\n\n"
            f"🆔 <b>Foydalanuvchi ID:</b>\n"
            f"Masalan: 123\n\n"
            f"📱 <b>Telefon raqam:</b>\n"
            f"Masalan: +998 90 123 45 67\n\n"
            f"ID yoki telefon raqamni kiriting:"
        )
        
        await message.answer(text)
        await state.set_state(AdminUsersStates.waiting_for_user_id)

    @router.message(AdminUsersStates.waiting_for_user_id)
    async def process_user_id(message: Message, state: FSMContext):
        """Process user ID for profile view"""
        user_id = message.text.strip()
        
        if not user_id:
            await message.answer("Iltimos, foydalanuvchi ID yoki telefon raqamini kiriting.")
            return
                
        # Mock user profile
        user_profile = {
            'id': 123,
            'name': 'Bekzod Toirov',
            'phone': '+998 90 123 45 67',
            'telegram_id': 123456789,
            'role': 'client',
            'status': 'active',
            'region': 'Toshkent',
            'email': 'bekzod@example.com',
            'created_at': '2024-01-15',
            'last_activity': '2024-08-05 14:30',
            'orders_count': 15,
            'completed_orders': 12,
            'pending_orders': 3,
            'total_spent': '450,000 so\'m',
            'rating': 4.8
        }
        
        text = (
            f"👤 <b>Foydalanuvchi profili</b>\n\n"
            f"🆔 <b>ID:</b> {user_profile['id']}\n"
            f"👤 <b>Ism:</b> {user_profile['name']}\n"
            f"📱 <b>Telefon:</b> {user_profile['phone']}\n"
            f"🆔 <b>Telegram ID:</b> {user_profile['telegram_id']}\n"
            f"👤 <b>Rol:</b> {user_profile['role']}\n"
            f"🌍 <b>Hudud:</b> {user_profile['region']}\n"
            f"📧 <b>Email:</b> {user_profile['email']}\n"
            f"📅 <b>Ro'yxatdan:</b> {user_profile['created_at']}\n"
            f"⏰ <b>So'nggi faollik:</b> {user_profile['last_activity']}\n\n"
            f"📋 <b>Faollik:</b>\n"
            f"• Jami zayavkalar: {user_profile['orders_count']}\n"
            f"• Bajarilgan: {user_profile['completed_orders']}\n"
            f"• Kutilmoqda: {user_profile['pending_orders']}\n"
            f"• Jami xarid: {user_profile['total_spent']}\n"
            f"• Reyting: ⭐ {user_profile['rating']}"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Tahrirlash",
                    callback_data=f"edit_user_{user_profile['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Zayavkalar tarixi",
                    callback_data=f"user_orders_{user_profile['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔒 Bloklash",
                    callback_data=f"block_user_{user_profile['id']}"
                )
            ]
        ])
        
        await message.answer(text, reply_markup=keyboard)
        await state.clear()
            
    @router.callback_query(F.data.startswith("view_user_"))
    async def view_user_details(call: CallbackQuery):
        """View user details"""
        await call.answer()
        
        user_id = call.data.split("view_user_")[1]
        
        # Mock user details
        user_details = {
            'id': int(user_id),
            'name': 'Bekzod Toirov',
            'phone': '+998 90 123 45 67',
            'telegram_id': 123456789,
            'role': 'client',
            'status': 'active',
            'region': 'Toshkent',
            'email': 'bekzod@example.com',
            'created_at': '2024-01-15',
            'last_activity': '2024-08-05 14:30',
            'orders_count': 15,
            'completed_orders': 12,
            'pending_orders': 3,
            'total_spent': '450,000 so\'m',
            'rating': 4.8
        }
        
        text = (
            f"👤 <b>Foydalanuvchi ma'lumotlari</b>\n\n"
            f"🆔 <b>ID:</b> {user_details['id']}\n"
            f"👤 <b>Ism:</b> {user_details['name']}\n"
            f"📱 <b>Telefon:</b> {user_details['phone']}\n"
            f"🆔 <b>Telegram ID:</b> {user_details['telegram_id']}\n"
            f"👤 <b>Rol:</b> {user_details['role']}\n"
            f"🌍 <b>Hudud:</b> {user_details['region']}\n"
            f"📧 <b>Email:</b> {user_details['email']}\n"
            f"📅 <b>Ro'yxatdan:</b> {user_details['created_at']}\n"
            f"⏰ <b>So'nggi faollik:</b> {user_details['last_activity']}\n\n"
            f"📋 <b>Faollik:</b>\n"
            f"• Jami zayavkalar: {user_details['orders_count']}\n"
            f"• Bajarilgan: {user_details['completed_orders']}\n"
            f"• Kutilmoqda: {user_details['pending_orders']}\n"
            f"• Jami xarid: {user_details['total_spent']}\n"
            f"• Reyting: ⭐ {user_details['rating']}"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Tahrirlash",
                    callback_data=f"edit_user_{user_details['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📋 Zayavkalar tarixi",
                    callback_data=f"user_orders_{user_details['id']}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔒 Bloklash",
                    callback_data=f"block_user_{user_details['id']}"
                )
            ]
        ])
        
        await call.message.edit_text(text, reply_markup=keyboard)

    @router.callback_query(F.data.startswith("edit_user_"))
    async def edit_user(call: CallbackQuery, state: FSMContext):
        """Edit user"""
        await call.answer()
        
        user_id = call.data.split("edit_user_")[1]
        
        text = (
            f"✏️ <b>Foydalanuvchi tahrirlash</b>\n\n"
            f"Foydalanuvchi ID: {user_id}\n\n"
            f"O'zgartirish uchun quyidagi ma'lumotlardan birini tanlang:\n\n"
            f"👤 <b>Ism</b>\n"
            f"📱 <b>Telefon</b>\n"
            f"👤 <b>Rol</b>\n"
            f"🌍 <b>Hudud</b>\n"
            f"📧 <b>Email</b>\n"
            f"🔒 <b>Holat</b>\n\n"
            f"O'zgartirmoqchi bo'lgan maydonni tanlang:"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👤 Ism",
                    callback_data=f"edit_user_field_{user_id}_name"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📱 Telefon",
                    callback_data=f"edit_user_field_{user_id}_phone"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👤 Rol",
                    callback_data=f"edit_user_field_{user_id}_role"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🌍 Hudud",
                    callback_data=f"edit_user_field_{user_id}_region"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📧 Email",
                    callback_data=f"edit_user_field_{user_id}_email"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔒 Holat",
                    callback_data=f"edit_user_field_{user_id}_status"
                )
            ]
        ])
        
        await call.message.edit_text(text, reply_markup=keyboard)
        await state.update_data(editing_user_id=user_id)

    @router.callback_query(F.data.startswith("edit_user_field_"))
    async def edit_user_field(call: CallbackQuery, state: FSMContext):
        """Edit specific user field"""
        await call.answer()
            
        parts = call.data.split("_")
        user_id = parts[3]
        field = parts[4]
        
        field_names = {
            'name': 'Ism',
            'phone': 'Telefon',
            'role': 'Rol',
            'region': 'Hudud',
            'email': 'Email',
            'status': 'Holat'
        }
        
        field_name = field_names.get(field, field)
        
        text = f"✏️ <b>{field_name} o'zgartirish</b>\n\nFoydalanuvchi ID: {user_id}\n\nYangi {field_name.lower()}ni kiriting:"
        
        await call.message.edit_text(text)
        await state.update_data(editing_field=field)
        await state.set_state(AdminUsersStates.waiting_for_field_value)

    @router.message(AdminUsersStates.waiting_for_field_value)
    async def process_field_value(message: Message, state: FSMContext):
        """Process field value update"""
        data = await state.get_data()
        user_id = data.get('editing_user_id')
        field = data.get('editing_field')
        
        new_value = message.text.strip()
        
        if not new_value:
            await message.answer("Qiymat bo'sh bo'lishi mumkin emas.")
            return
                
        field_names = {
            'name': 'Ism',
            'phone': 'Telefon',
            'role': 'Rol',
            'region': 'Hudud',
            'email': 'Email',
            'status': 'Holat'
        }
        
        field_name = field_names.get(field, field)
        
        text = f"✅ Foydalanuvchi {field_name.lower()} '{new_value}' ga o'zgartirildi."
        
        await message.answer(text)
        await state.clear()

    @router.callback_query(F.data.startswith("block_user_"))
    async def block_user(call: CallbackQuery):
        """Block user"""
        await call.answer()
            
        user_id = call.data.split("block_user_")[1]
        
        text = (
            f"🔒 <b>Foydalanuvchi bloklash</b>\n\n"
            f"Foydalanuvchi ID: {user_id}\n"
            f"Ism: Bekzod Toirov\n\n"
            f"⚠️ <b>Diqqat:</b>\n"
            f"Foydalanuvchini bloklash uning tizimga kirishini to'xtatadi.\n"
            f"Bloklashni tasdiqlaysizmi?"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tasdiqlash",
                    callback_data=f"confirm_block_user_{user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Bekor qilish",
                    callback_data=f"cancel_block_user_{user_id}"
                )
            ]
        ])
        
        await call.message.edit_text(text, reply_markup=keyboard)

    @router.callback_query(F.data.startswith("confirm_block_user_"))
    async def confirm_block_user(call: CallbackQuery):
        """Confirm block user"""
        await call.answer()
        
        user_id = call.data.split("confirm_block_user_")[1]
        
        text = f"✅ Foydalanuvchi ID {user_id} muvaffaqiyatli bloklandi."
        
        await call.message.edit_text(text)

    @router.callback_query(F.data.startswith("cancel_block_user_"))
    async def cancel_block_user(call: CallbackQuery):
        """Cancel block user"""
        await call.answer()
        
        user_id = call.data.split("cancel_block_user_")[1]
        
        text = f"❌ Foydalanuvchi ID {user_id} bloklash bekor qilindi."
        
        await call.message.edit_text(text)

    return router