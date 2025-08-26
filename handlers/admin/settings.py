"""
Admin Settings Handler
Manages admin settings and system configuration
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from functools import wraps
import logging
from datetime import datetime
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.admin_buttons import get_settings_keyboard

# States imports
from states.admin_states import AdminSettingsStates, AdminMainMenuStates
from filters.role_filter import RoleFilter

def get_admin_settings_router():
    """Get admin settings router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("admin")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(StateFilter(AdminMainMenuStates.main_menu), F.text.in_(["⚙️ Sozlamalar", "⚙️ Настройки"]))
    async def settings_menu(message: Message, state: FSMContext):
        """Settings main menu"""
        text = "Sozlamalar bo'limi (stub)."
        
        sent_message = await message.answer(
            text,
            reply_markup=get_settings_keyboard('uz')
        )
        await state.set_state(AdminSettingsStates.settings)

    @router.message(F.text.in_(["🔧 Tizim sozlamalari", "🔧 Системные настройки"]))
    async def system_settings(message: Message):
        """Show system settings"""
        # Mock system settings
        settings = {
            'max_orders_per_technician': {'value': '5', 'description': 'Bir texnik uchun maksimal zayavkalar'},
            'order_timeout_hours': {'value': '24', 'description': 'Zayavka timeout vaqti'},
            'notification_enabled': {'value': 'Ha', 'description': 'Bildirishnomalar yoqilgan'},
            'auto_assign_enabled': {'value': 'Ha', 'description': 'Avtomatik tayinlash'},
            'maintenance_mode': {'value': 'Yo\'q', 'description': 'Texnik xizmat rejimi'}
        }
        
        text = f"🔧 <b>Tizim sozlamalari</b>\n\n"
        
        setting_names = {
            'max_orders_per_technician': 'Texnik uchun maksimal zayavkalar',
            'order_timeout_hours': 'Zayavka timeout (soat)',
            'notification_enabled': 'Bildirishnomalar yoqilgan',
            'auto_assign_enabled': 'Avtomatik tayinlash',
            'maintenance_mode': 'Texnik xizmat rejimi'
        }
        
        for key, setting in settings.items():
            setting_name = setting_names.get(key, key)
            text += f"• <b>{setting_name}:</b> {setting['value']}\n"
            if setting.get('description'):
                text += f"  <i>{setting['description']}</i>\n"
            text += "\n"
        
        # Add management buttons
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Sozlamani o'zgartirish",
                    callback_data="edit_system_setting"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Yangilash",
                    callback_data="refresh_system_settings"
                )
            ]
        ])
        
        await message.answer(text, reply_markup=keyboard)

    @router.message(F.text.in_(["📢 Bildirishnoma shablonlari", "📢 Шаблоны уведомлений"]))
    async def notification_templates(message: Message):
        """Show notification templates"""
        # Mock notification templates
        templates = [
            {'template_type': 'order_created', 'language': 'uz', 'content': 'Yangi zayavka yaratildi: #{order_id}'},
            {'template_type': 'order_created', 'language': 'ru', 'content': 'Создана новая заявка: #{order_id}'},
            {'template_type': 'order_assigned', 'language': 'uz', 'content': 'Zayavka texnikka tayinlandi: #{order_id}'},
            {'template_type': 'order_assigned', 'language': 'ru', 'content': 'Заявка назначена технику: #{order_id}'},
            {'template_type': 'order_completed', 'language': 'uz', 'content': 'Zayavka bajarildi: #{order_id}'},
            {'template_type': 'order_completed', 'language': 'ru', 'content': 'Заявка выполнена: #{order_id}'},
            {'template_type': 'welcome_message', 'language': 'uz', 'content': 'Xush kelibsiz! Qanday yordam bera olaman?'},
            {'template_type': 'welcome_message', 'language': 'ru', 'content': 'Добро пожаловать! Как я могу помочь?'}
        ]
        
        text = f"📢 <b>Bildirishnoma shablonlari</b>\n\n"
        
        # Group templates by type
        template_groups = {}
        for template in templates:
            template_type = template['template_type']
            if template_type not in template_groups:
                template_groups[template_type] = []
            template_groups[template_type].append(template)
        
        type_names = {
            'order_created': 'Zayavka yaratildi',
            'order_assigned': 'Zayavka tayinlandi',
            'order_completed': 'Zayavka bajarildi',
            'welcome_message': 'Xush kelibsiz xabari'
        }
        
        for template_type, group_templates in template_groups.items():
            type_name = type_names.get(template_type, template_type)
            
            text += f"📋 <b>{type_name}:</b>\n"
            
            for template in group_templates:
                lang_name = "O'zbek" if template['language'] == 'uz' else "Русский"
                text += f"  • {lang_name}: {template['content'][:50]}...\n"
            
            text += "\n"
        
        # Add management buttons
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Shablonni tahrirlash",
                    callback_data="edit_notification_template"
                )
            ]
        ])
        
        await message.answer(text, reply_markup=keyboard)

    @router.message(F.text.in_(["🔐 Xavfsizlik sozlamalari", "🔐 Настройки безопасности"]))
    async def security_settings(message: Message):
        """Show security settings"""
        text = (
            f"🔐 <b>Xavfsizlik sozlamalari</b>\n\n"
            f"🔒 <b>Joriy sozlamalar:</b>\n"
            f"• Admin huquqlari: Faol\n"
            f"• Avtorizatsiya: Telegram ID bo'yicha\n"
            f"• Sessiya muddati: Cheksiz\n"
            f"• Loglar saqlanishi: 30 kun\n\n"
            f"⚠️ <b>Xavfsizlik choralari:</b>\n"
            f"• Barcha admin amallar loglanadi\n"
            f"• Foydalanuvchi rollari nazorat qilinadi\n"
            f"• Tizimga kirish kuzatiladi\n\n"
            f"📋 <b>Tavsiyalar:</b>\n"
            f"• Admin huquqlarini faqat ishonchli odamlarga bering\n"
            f"• Muntazam ravishda loglarni tekshiring\n"
            f"• Shubhali faollikni darhol xabar qiling"
        )
        
        await message.answer(text)

    @router.message(F.text.in_(["🔄 Backup va tiklash", "🔄 Резервное копирование"]))
    async def backup_restore(message: Message):
        """Show backup and restore options"""
        text = (
            f"🔄 <b>Backup va tiklash</b>\n\n"
            f"💾 <b>Avtomatik backup:</b>\n"
            f"• Kunlik backup: Yoqilgan\n"
            f"• Backup vaqti: 02:00\n"
            f"• Saqlanish muddati: 30 kun\n\n"
            f"📁 <b>Backup ma'lumotlari:</b>\n"
            f"• Foydalanuvchilar ma'lumotlari\n"
            f"• Zayavkalar tarixi\n"
            f"• Tizim sozlamalari\n"
            f"• Loglar\n\n"
            f"⚠️ <b>Diqqat:</b>\n"
            f"Manual backup va tiklash funksiyalari\n"
            f"faqat server administratori tomonidan\n"
            f"amalga oshirilishi mumkin."
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📤 Ma'lumotlarni eksport",
                    callback_data="export_all_data"
                )
            ]
        ])
        
        await message.answer(text, reply_markup=keyboard)

    @router.callback_query(F.data == "edit_system_setting")
    async def edit_system_setting_menu(call: CallbackQuery, state: FSMContext):
        """Show system settings edit menu"""
        await call.answer()
        
        # Mock system settings
        settings = {
            'max_orders_per_technician': {'value': '5'},
            'order_timeout_hours': {'value': '24'},
            'notification_enabled': {'value': 'Ha'},
            'auto_assign_enabled': {'value': 'Ha'}
        }
        
        text = "O'zgartirish uchun sozlamani tanlang:"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[])
        setting_names = {
            'max_orders_per_technician': 'Maksimal zayavkalar',
            'order_timeout_hours': 'Timeout (soat)',
            'notification_enabled': 'Bildirishnomalar',
            'auto_assign_enabled': 'Avto-tayinlash'
        }
        
        for key, setting in list(settings.items())[:10]:  # Show first 10 settings
            setting_name = setting_names.get(key, key[:20])
            
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text=f"{setting_name}: {setting['value']}",
                    callback_data=f"edit_setting_{key}"
                )
            ])
        
        await call.message.edit_text(text, reply_markup=keyboard)
        await state.set_state(AdminSettingsStates.editing_setting)

    @router.callback_query(F.data.startswith("edit_setting_"), AdminSettingsStates.editing_setting)
    async def edit_setting_value(call: CallbackQuery, state: FSMContext):
        """Edit setting value"""
        await call.answer()
        
        setting_key = call.data.split("edit_setting_")[1]
        
        await state.update_data(setting_key=setting_key)
        
        text = f"'{setting_key}' sozlamasi uchun yangi qiymatni kiriting:"
        
        await call.message.edit_text(text)
        await state.set_state(AdminSettingsStates.waiting_for_setting_value)

    @router.message(AdminSettingsStates.waiting_for_setting_value)
    async def process_setting_value(message: Message, state: FSMContext):
        """Process new setting value"""
        data = await state.get_data()
        setting_key = data.get('setting_key')
        new_value = message.text.strip()
        
        if not new_value:
            text = "Qiymat bo'sh bo'lishi mumkin emas."
            await message.answer(text)
            return
        
        text = f"✅ '{setting_key}' sozlamasi '{new_value}' ga o'zgartirildi."
        
        await message.answer(text)
        await state.clear()

    @router.callback_query(F.data == "refresh_system_settings")
    async def refresh_system_settings(call: CallbackQuery):
        """Refresh system settings"""
        await call.answer()
        
        # Mock system settings
        settings = {
            'max_orders_per_technician': {'value': '5'},
            'order_timeout_hours': {'value': '24'},
            'notification_enabled': {'value': 'Ha'},
            'auto_assign_enabled': {'value': 'Ha'}
        }
        
        text = f"🔄 <b>Yangilangan tizim sozlamalari</b>\n\n"
        
        setting_names = {
            'max_orders_per_technician': 'Texnik uchun maksimal zayavkalar',
            'order_timeout_hours': 'Zayavka timeout (soat)',
            'notification_enabled': 'Bildirishnomalar yoqilgan',
            'auto_assign_enabled': 'Avtomatik tayinlash'
        }
        
        for key, setting in settings.items():
            setting_name = setting_names.get(key, key)
            text += f"• <b>{setting_name}:</b> {setting['value']}\n"
        
        text += f"\n🕐 Yangilangan: {datetime.now().strftime('%H:%M:%S')}"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Sozlamani o'zgartirish",
                    callback_data="edit_system_setting"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Yangilash",
                    callback_data="refresh_system_settings"
                )
            ]
        ])
        
        await call.message.edit_text(text, reply_markup=keyboard)
        await call.answer("Sozlamalar yangilandi!")

    @router.callback_query(F.data == "export_all_data")
    async def export_all_data(call: CallbackQuery):
        """Export all system data"""
        await call.answer()
        
        try:
            from utils.export_utils import create_export_file
            from aiogram.types import BufferedInputFile
            
            processing_text = "Barcha ma'lumotlar eksport qilinmoqda..."
            processing_msg = await call.message.edit_text(processing_text)
            
            # Export different types of data
            export_types = ["users", "orders", "statistics"]
            
            # Delete processing message
            await processing_msg.delete()
            
            # Send each export file
            for export_type in export_types:
                file_content, filename = create_export_file(export_type, "csv", "admin")
                
                # Get file size
                file_content.seek(0, 2)  # Move to end
                file_size = file_content.tell()
                file_content.seek(0)  # Reset to beginning
                
                await call.message.answer_document(
                    BufferedInputFile(
                        file_content.read(),
                        filename=filename
                    ),
                    caption=f"✅ {export_type.title()} export muvaffaqiyatli yakunlandi!\n\n"
                            f"📄 Fayl: {filename}\n"
                            f"📦 Hajm: {file_size:,} bayt\n"
                            f"📊 Format: CSV\n"
                            f"📅 Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                )
                
        except Exception as e:
            await call.message.answer("❌ Export xatoligi yuz berdi")

    return router
