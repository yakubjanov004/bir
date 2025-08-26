"""
Call Center Direct Resolution Handler
Manages call center direct problem resolution
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.call_center_buttons import get_direct_resolution_keyboard

# States imports
from states.call_center_states import CallCenterDirectResolutionStates, CallCenterMainMenuStates
from filters.role_filter import RoleFilter

def get_call_center_direct_resolution_router():
    """Get call center direct resolution router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(StateFilter(CallCenterMainMenuStates.main_menu), F.text.in_(["🔧 To'g'ridan-to'g'ri hal qilish", "🔧 Прямое решение"]))
    async def direct_resolution_menu(message: Message, state: FSMContext):
        """Direct resolution main menu"""
        text = "🔧 <b>To'g'ridan-to'g'ri hal qilish</b>\n\nMuammolarni to'g'ridan-to'g'ri hal qilish uchun bo'limni tanlang."
        
        await message.answer(
            text,
            reply_markup=get_direct_resolution_keyboard('uz')
        )
        await state.set_state(CallCenterDirectResolutionStates.direct_resolution)

    @router.message(F.text.in_(["📋 Muammo turlari", "📋 Типы проблем"]))
    async def problem_types(message: Message):
        """Show problem types"""
        # Mock problem types
        problem_types = [
            {
                'id': 'PT001',
                'name': 'Internet uzulish',
                'description': 'Internet xizmati ishlamayapti',
                'frequency': '45%',
                'avg_resolution_time': '2.5 soat',
                'success_rate': '95%'
            },
            {
                'id': 'PT002',
                'name': 'TV signal yo\'q',
                'description': 'TV kanallar ko\'rinmayapti',
                'frequency': '25%',
                'avg_resolution_time': '1.8 soat',
                'success_rate': '92%'
            },
            {
                'id': 'PT003',
                'name': 'Telefon xizmati',
                'description': 'Telefon qo\'ng\'iroqlar ishlamayapti',
                'frequency': '15%',
                'avg_resolution_time': '3.2 soat',
                'success_rate': '88%'
            },
            {
                'id': 'PT004',
                'name': 'Hisob muammosi',
                'description': 'To\'lov yoki hisob ma\'lumotlari',
                'frequency': '10%',
                'avg_resolution_time': '0.5 soat',
                'success_rate': '98%'
            },
            {
                'id': 'PT005',
                'name': 'Boshqa muammolar',
                'description': 'Boshqa texnik muammolar',
                'frequency': '5%',
                'avg_resolution_time': '4.1 soat',
                'success_rate': '85%'
            }
        ]
        
        text = (
            f"📋 <b>Muammo turlari</b>\n\n"
            f"📊 <b>Umumiy:</b> {len(problem_types)} ta muammo turi\n\n"
        )
        
        for i, problem in enumerate(problem_types, 1):
            text += (
                f"{i}. <b>{problem['name']}</b>\n"
                f"   📝 {problem['description']}\n"
                f"   📊 Ko'rinish: {problem['frequency']}\n"
                f"   ⏱ O'rtacha hal qilish: {problem['avg_resolution_time']}\n"
                f"   ✅ Muvaffaqiyat: {problem['success_rate']}\n\n"
            )
        
        await message.answer(text)

    @router.message(F.text.in_(["⚡ Tezkor hal qilish", "⚡ Быстрое решение"]))
    async def quick_resolution(message: Message):
        """Show quick resolution options"""
        # Mock quick resolution options
        quick_options = [
            {
                'id': 'QR001',
                'name': 'Router qayta ishga tushirish',
                'description': 'Router va modem qayta ishga tushirish',
                'success_rate': '85%',
                'time': '5-10 daqiqa'
            },
            {
                'id': 'QR002',
                'name': 'Kabel tekshirish',
                'description': 'Internet va TV kabelini tekshirish',
                'success_rate': '70%',
                'time': '10-15 daqiqa'
            },
            {
                'id': 'QR003',
                'name': 'Hisob to\'ldirish',
                'description': 'Hisobni to\'ldirish va xizmatni yoqish',
                'success_rate': '95%',
                'time': '2-3 daqiqa'
            },
            {
                'id': 'QR004',
                'name': 'Kanallar qayta sozlash',
                'description': 'TV kanallarni qayta sozlash',
                'success_rate': '80%',
                'time': '5-8 daqiqa'
            }
        ]
        
        text = (
            f"⚡ <b>Tezkor hal qilish</b>\n\n"
            f"🚀 <b>Eng tezkor hal qilish usullari:</b>\n\n"
        )
        
        for i, option in enumerate(quick_options, 1):
            text += (
                f"{i}. <b>{option['name']}</b>\n"
                f"   📝 {option['description']}\n"
                f"   ✅ Muvaffaqiyat: {option['success_rate']}\n"
                f"   ⏱ Vaqt: {option['time']}\n\n"
            )
        
        await message.answer(text)

    @router.message(F.text.in_(["🔍 Muammo diagnostikasi", "🔍 Диагностика проблем"]))
    async def problem_diagnosis(message: Message):
        """Show problem diagnosis"""
        # Mock diagnosis steps
        diagnosis_steps = [
            {
                'step': 1,
                'name': 'Muammo turini aniqlash',
                'description': 'Mijoz muammosini batafsil so\'rash',
                'questions': [
                    'Qaysi xizmat ishlamayapti?',
                    'Qachondan boshlangan?',
                    'Qanday belgilar ko\'rinadi?'
                ]
            },
            {
                'step': 2,
                'name': 'Asosiy tekshirishlar',
                'description': 'Oddiy tekshirishlarni amalga oshirish',
                'questions': [
                    'Router yonib turibdimi?',
                    'Internet kabel ulanganmi?',
                    'Hisobda pul bormi?'
                ]
            },
            {
                'step': 3,
                'name': 'Texnik diagnostika',
                'description': 'Texnik parametrlarni tekshirish',
                'questions': [
                    'Signal kuchi qanday?',
                    'Ping natijasi qanday?',
                    'Speed test natijasi?'
                ]
            }
        ]
        
        text = (
            f"🔍 <b>Muammo diagnostikasi</b>\n\n"
            f"📋 <b>Diagnostika bosqichlari:</b>\n\n"
        )
        
        for step in diagnosis_steps:
            text += (
                f"📌 <b>Bosqich {step['step']}: {step['name']}</b>\n"
                f"   📝 {step['description']}\n"
                f"   ❓ Savollar:\n"
            )
            
            for question in step['questions']:
                text += f"   • {question}\n"
            text += "\n"
        
        await message.answer(text)

    @router.message(F.text.in_(["📞 Texnik yordam", "📞 Техническая поддержка"]))
    async def technical_support(message: Message):
        """Show technical support"""
        # Mock technical support info
        support_info = {
            'phone': '+998 71 123 45 67',
            'email': 'support@example.com',
            'working_hours': '24/7',
            'response_time': '15 daqiqa',
            'languages': ['O\'zbekcha', 'Ruscha'],
            'services': [
                'Internet xizmati',
                'TV xizmati', 
                'Telefon xizmati',
                'Hisob ma\'lumotlari'
            ]
        }
        
        text = (
            f"📞 <b>Texnik yordam</b>\n\n"
            f"📱 <b>Telefon:</b> {support_info['phone']}\n"
            f"📧 <b>Email:</b> {support_info['email']}\n"
            f"⏰ <b>Ish vaqti:</b> {support_info['working_hours']}\n"
            f"⚡ <b>Javob vaqti:</b> {support_info['response_time']}\n"
            f"🌐 <b>Tillar:</b> {', '.join(support_info['languages'])}\n\n"
            f"📋 <b>Xizmatlar:</b>\n"
        )
        
        for service in support_info['services']:
            text += f"• {service}\n"
        
        await message.answer(text)

    @router.message(F.text.in_(["📊 Hal qilish statistikasi", "📊 Статистика решений"]))
    async def resolution_statistics(message: Message):
        """Show resolution statistics"""
        # Mock resolution statistics
        resolution_stats = {
            'total_problems': 1245,
            'resolved_problems': 1189,
            'resolution_rate': '95.5%',
            'avg_resolution_time': '2.3 soat',
            'by_category': {
                'internet': {'total': 560, 'resolved': 532, 'rate': '95.0%'},
                'tv': {'total': 312, 'resolved': 298, 'rate': '95.5%'},
                'phone': {'total': 187, 'resolved': 175, 'rate': '93.6%'},
                'billing': {'total': 186, 'resolved': 184, 'rate': '98.9%'}
            },
            'top_resolvers': [
                'Aziz Karimov - 156 ta',
                'Malika Yusupova - 142 ta',
                'Bekzod Toirov - 128 ta'
            ]
        }
        
        text = (
            f"📊 <b>Hal qilish statistikasi</b>\n\n"
            f"📈 <b>Umumiy ko'rsatkichlar:</b>\n"
            f"• Jami muammolar: {resolution_stats['total_problems']:,}\n"
            f"• Hal qilingan: {resolution_stats['resolved_problems']:,}\n"
            f"• Hal qilish darajasi: {resolution_stats['resolution_rate']}\n"
            f"• O'rtacha vaqt: {resolution_stats['avg_resolution_time']}\n\n"
            f"📋 <b>Kategoriya bo'yicha:</b>\n"
        )
        
        for category, data in resolution_stats['by_category'].items():
            category_names = {
                'internet': 'Internet xizmati',
                'tv': 'TV xizmati',
                'phone': 'Telefon xizmati',
                'billing': 'Hisob ma\'lumotlari'
            }
            category_name = category_names.get(category, category)
            text += f"• {category_name}: {data['resolved']}/{data['total']} ({data['rate']})\n"
        
        text += f"\n🏆 <b>Eng yaxshi hal qiluvchilar:</b>\n"
        for resolver in resolution_stats['top_resolvers']:
            text += f"• {resolver}\n"
        
        await message.answer(text)

    return router
