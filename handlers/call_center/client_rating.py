"""
Call Center Client Rating Handler
Manages call center client rating and feedback
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
from keyboards.call_center_buttons import rating_keyboard
from keyboards.call_center_buttons import (
    get_rating_statistics_keyboard,
    get_feedback_complaints_keyboard,
    get_top_operators_keyboard,
    get_rating_dynamics_keyboard,
    get_rating_settings_keyboard
)

# States imports
from states.call_center_states import CallCenterMainMenuStates
from filters.role_filter import RoleFilter

def get_call_center_client_rating_router():
    """Get call center client rating router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(StateFilter(CallCenterMainMenuStates.main_menu), F.text.in_(["⭐ Reyting", "⭐ Рейтинг"]))
    async def client_rating_menu(message: Message, state: FSMContext):
        """Client rating main menu"""
        text = "⭐ <b>Call Center Reyting</b>\n\nMijozlar reytingi va fikrlarini boshqarish uchun bo'limni tanlang."
        
        sent_message = await message.answer(
            text,
            reply_markup=rating_keyboard('uz')
        )
        await state.set_state(CallCenterMainMenuStates.main_menu)

    @router.message(F.text.in_(["📊 Reyting statistikasi", "📊 Статистика рейтинга"]))
    async def rating_statistics(message: Message):
        """Show rating statistics"""
        # Mock rating statistics
        rating_stats = {
            'total_ratings': 1250,
            'average_rating': 4.6,
            'excellent_ratings': 890,
            'good_ratings': 280,
            'average_ratings': 60,
            'poor_ratings': 15,
            'very_poor_ratings': 5,
            'satisfaction_rate': '94.8%',
            'response_rate': '87.2%'
        }
        
        text = (
            f"📊 <b>Reyting statistikasi</b>\n\n"
            f"⭐ <b>Umumiy reyting:</b> {rating_stats['average_rating']}/5\n"
            f"📈 <b>Mamnuniyat darajasi:</b> {rating_stats['satisfaction_rate']}\n"
            f"📊 <b>Javob berish darajasi:</b> {rating_stats['response_rate']}\n\n"
            f"📋 <b>Reyting taqsimoti:</b>\n"
            f"⭐⭐⭐⭐⭐ Yaxshi: {rating_stats['excellent_ratings']} ({rating_stats['excellent_ratings']/rating_stats['total_ratings']*100:.1f}%)\n"
            f"⭐⭐⭐ Yaxshi: {rating_stats['good_ratings']} ({rating_stats['good_ratings']/rating_stats['total_ratings']*100:.1f}%)\n"
            f"⭐⭐⭐ O'rtacha: {rating_stats['average_ratings']} ({rating_stats['average_ratings']/rating_stats['total_ratings']*100:.1f}%)\n"
            f"⭐⭐ Yomon: {rating_stats['poor_ratings']} ({rating_stats['poor_ratings']/rating_stats['total_ratings']*100:.1f}%)\n"
            f"⭐ Juda yomon: {rating_stats['very_poor_ratings']} ({rating_stats['very_poor_ratings']/rating_stats['total_ratings']*100:.1f}%)\n\n"
            f"📅 <b>Bugun:</b> 45 ta yangi reyting\n"
            f"📅 <b>Bu hafta:</b> 234 ta reyting\n"
            f"📅 <b>Bu oy:</b> 890 ta reyting"
        )
        
        keyboard = get_rating_statistics_keyboard(lang)
        
        await message.answer(text, reply_markup=keyboard)

    @router.message(F.text.in_(["📝 Fikrlar va shikoyatlar", "📝 Отзывы и жалобы"]))
    async def feedback_complaints(message: Message):
        """Show feedback and complaints"""
        # Mock feedback and complaints
        feedback_list = [
            {
                'id': 'FB001',
                'client_name': 'Bekzod Toirov',
                'rating': 5,
                'feedback': 'Ajoyib xizmat! Texnik juda tez va sifatli ishladi.',
                'date': '2024-08-05 14:30',
                'type': 'positive'
            },
            {
                'id': 'FB002',
                'client_name': 'Aziz Karimov',
                'rating': 4,
                'feedback': 'Yaxshi xizmat, lekin biroz kechikdi.',
                'date': '2024-08-05 13:45',
                'type': 'positive'
            },
            {
                'id': 'FB003',
                'client_name': 'Dilshod Rahimov',
                'rating': 2,
                'feedback': 'Texnik kech keldi va muammoni to\'liq hal qilmadi.',
                'date': '2024-08-05 12:20',
                'type': 'negative'
            }
        ]
        
        text = (
            f"📝 <b>Fikrlar va shikoyatlar</b>\n\n"
            f"📊 <b>Bugun:</b> {len(feedback_list)} ta fikr\n\n"
        )
        
        for i, feedback in enumerate(feedback_list, 1):
            rating_stars = "⭐" * feedback['rating']
            type_emoji = "✅" if feedback['type'] == 'positive' else "❌"
            
            text += (
                f"{i}. {type_emoji} <b>{feedback['client_name']}</b>\n"
                f"   {rating_stars}\n"
                f"   📝 {feedback['feedback']}\n"
                f"   📅 {feedback['date']}\n\n"
            )
        
        keyboard = get_feedback_complaints_keyboard(lang)
        
        await message.answer(text, reply_markup=keyboard)

    @router.message(F.text.in_(["🏆 Eng yaxshi operatorlar", "🏆 Лучшие операторы"]))
    async def top_operators(message: Message):
        """Show top operators"""
        # Mock top operators
        top_operators = [
            {
                'name': 'Aziz Karimov',
                'rating': 4.9,
                'total_chats': 156,
                'satisfaction_rate': '98.5%',
                'response_time': '1.2 daqiqa',
                'position': 1
            },
            {
                'name': 'Bekzod Toirov',
                'rating': 4.8,
                'total_chats': 142,
                'satisfaction_rate': '97.2%',
                'response_time': '1.5 daqiqa',
                'position': 2
            },
            {
                'name': 'Dilshod Rahimov',
                'rating': 4.7,
                'total_chats': 128,
                'satisfaction_rate': '96.8%',
                'response_time': '1.8 daqiqa',
                'position': 3
            }
        ]
        
        text = (
            f"🏆 <b>Eng yaxshi operatorlar</b>\n\n"
            f"📊 <b>Bu oy:</b> {len(top_operators)} ta eng yaxshi operator\n\n"
        )
        
        for operator in top_operators:
            medal_emoji = "🥇" if operator['position'] == 1 else "🥈" if operator['position'] == 2 else "🥉"
            
            text += (
                f"{medal_emoji} <b>{operator['name']}</b>\n"
                f"   ⭐ Reyting: {operator['rating']}/5\n"
                f"   💬 Chatlar: {operator['total_chats']}\n"
                f"   😊 Mamnuniyat: {operator['satisfaction_rate']}\n"
                f"   ⏱ Javob vaqti: {operator['response_time']}\n\n"
            )
        
        keyboard = get_top_operators_keyboard(lang)
        
        await message.answer(text, reply_markup=keyboard)

    @router.message(F.text.in_(["📈 Reyting dinamikasi", "📈 Динамика рейтинга"]))
    async def rating_dynamics(message: Message):
        """Show rating dynamics"""
        # Mock rating dynamics
        dynamics = {
            'current_month': 4.6,
            'previous_month': 4.4,
            'trend': '+0.2',
            'weekly_data': [
                {'week': '1-hafta', 'rating': 4.5},
                {'week': '2-hafta', 'rating': 4.6},
                {'week': '3-hafta', 'rating': 4.7},
                {'week': '4-hafta', 'rating': 4.6}
            ],
            'improvement_areas': [
                'Javob vaqtini qisqartirish',
                'Texnik xizmat sifatini oshirish',
                'Mijoz bilan aloqa sifatini yaxshilash'
            ]
        }
        
        text = (
            f"📈 <b>Reyting dinamikasi</b>\n\n"
            f"📊 <b>Joriy oy:</b> {dynamics['current_month']}/5\n"
            f"📊 <b>O'tgan oy:</b> {dynamics['previous_month']}/5\n"
            f"📈 <b>O'zgarish:</b> {dynamics['trend']}\n\n"
            f"📅 <b>Haftalik dinamika:</b>\n"
        )
        
        for week_data in dynamics['weekly_data']:
            text += f"• {week_data['week']}: {week_data['rating']}/5\n"
        
        text += f"\n🎯 <b>Yaxshilash yo'nalishlari:</b>\n"
        for area in dynamics['improvement_areas']:
            text += f"• {area}\n"
        
        keyboard = get_rating_dynamics_keyboard(lang)
        
        await message.answer(text, reply_markup=keyboard)

    @router.message(F.text.in_(["⚙️ Reyting sozlamalari", "⚙️ Настройки рейтинга"]))
    async def rating_settings(message: Message):
        """Show rating settings"""
        # Mock rating settings
        settings = {
            'auto_rating_enabled': True,
            'rating_reminder_enabled': True,
            'rating_reminder_delay': '24 soat',
            'minimum_rating_threshold': 3.5,
            'excellent_rating_threshold': 4.5,
            'feedback_required': True,
            'rating_expiry_days': 7
        }
        
        text = (
            f"⚙️ <b>Reyting sozlamalari</b>\n\n"
            f"🤖 <b>Avto-reyting:</b> {'Yoqilgan' if settings['auto_rating_enabled'] else 'O\'chirilgan'}\n"
            f"🔔 <b>Eslatma:</b> {'Yoqilgan' if settings['rating_reminder_enabled'] else 'O\'chirilgan'}\n"
            f"⏰ <b>Eslatma vaqti:</b> {settings['rating_reminder_delay']}\n"
            f"📊 <b>Minimal reyting:</b> {settings['minimum_rating_threshold']}/5\n"
            f"⭐ <b>Ajoyib reyting:</b> {settings['excellent_rating_threshold']}/5\n"
            f"📝 <b>Fikr majburiy:</b> {'Ha' if settings['feedback_required'] else 'Yo\'q'}\n"
            f"⏳ <b>Reyting muddati:</b> {settings['rating_expiry_days']} kun\n\n"
            f"💡 Sozlamalarni o'zgartirish uchun admin bilan bog'laning."
        )
        
        keyboard = get_rating_settings_keyboard(lang)
        
        await message.answer(text, reply_markup=keyboard)

    @router.callback_query(F.data == "detailed_rating_report")
    async def detailed_rating_report(call: CallbackQuery):
        """Show detailed rating report"""
        await call.answer()
        
        text = (
            f"📈 <b>Batafsil reyting hisoboti</b>\n\n"
            f"📊 <b>Umumiy ko'rsatkichlar:</b>\n"
            f"• Jami reytinglar: 1,250\n"
            f"• O'rtacha reyting: 4.6/5\n"
            f"• Mamnuniyat darajasi: 94.8%\n"
            f"• Javob berish darajasi: 87.2%\n\n"
            f"📅 <b>Vaqt bo'yicha:</b>\n"
            f"• Bugun: 45 ta reyting\n"
            f"• Bu hafta: 234 ta reyting\n"
            f"• Bu oy: 890 ta reyting\n"
            f"• O'tgan oy: 756 ta reyting\n\n"
            f"🌍 <b>Hudud bo'yicha:</b>\n"
            f"• Toshkent: 4.7/5\n"
            f"• Samarqand: 4.5/5\n"
            f"• Buxoro: 4.6/5\n"
            f"• Farg'ona: 4.4/5\n\n"
            f"📋 <b>Xizmat turi bo'yicha:</b>\n"
            f"• Internet: 4.7/5\n"
            f"• TV: 4.5/5\n"
            f"• Telefon: 4.6/5\n"
            f"• Texnik xizmat: 4.8/5"
        )
        
        await call.message.edit_text(text)

    @router.callback_query(F.data == "rating_chart")
    async def rating_chart(call: CallbackQuery):
        """Show rating chart"""
        await call.answer()
        
        text = (
            f"📊 <b>Reyting grafigi</b>\n\n"
            f"📈 <b>Oylik dinamika:</b>\n"
            f"Yanvar: ████████ 4.2/5\n"
            f"Fevral: █████████ 4.3/5\n"
            f"Mart: ██████████ 4.4/5\n"
            f"Aprel: ███████████ 4.5/5\n"
            f"May: ████████████ 4.6/5\n"
            f"Iyun: ████████████ 4.6/5\n"
            f"Iyul: ████████████ 4.6/5\n"
            f"Avgust: ████████████ 4.6/5\n\n"
            f"📈 <b>O'sish tendentsiyasi:</b>\n"
            f"• O'tgan oyga nisbatan: +0.2\n"
            f"• O'tgan yilga nisbatan: +0.4\n"
            f"• Umumiy tendentsiya: O'sish"
        )
        
        await call.message.edit_text(text)

    @router.callback_query(F.data == "view_all_feedback")
    async def view_all_feedback(call: CallbackQuery):
        """View all feedback"""
        await call.answer()
        
        text = (
            f"📝 <b>Barcha fikrlar</b>\n\n"
            f"📊 <b>Umumiy:</b> 1,250 ta fikr\n"
            f"✅ <b>Ijobiy:</b> 1,185 ta (94.8%)\n"
            f"❌ <b>Salbiy:</b> 65 ta (5.2%)\n\n"
            f"📅 <b>So'nggi fikrlar:</b>\n\n"
            f"1. ✅ Bekzod Toirov - ⭐⭐⭐⭐⭐\n"
            f"   Ajoyib xizmat! Texnik juda tez va sifatli ishladi.\n"
            f"   📅 2024-08-05 14:30\n\n"
            f"2. ✅ Aziz Karimov - ⭐⭐⭐⭐\n"
            f"   Yaxshi xizmat, lekin biroz kechikdi.\n"
            f"   📅 2024-08-05 13:45\n\n"
            f"3. ❌ Dilshod Rahimov - ⭐⭐\n"
            f"   Texnik kech keldi va muammoni to'liq hal qilmadi.\n"
            f"   📅 2024-08-05 12:20\n\n"
            f"... va 1,247 ta boshqa fikr"
        )
        
        await call.message.edit_text(text)

    @router.callback_query(F.data == "feedback_statistics")
    async def feedback_statistics(call: CallbackQuery):
        """Show feedback statistics"""
        await call.answer()
        
        text = (
            f"📊 <b>Fikrlar statistikasi</b>\n\n"
            f"📈 <b>Umumiy ko'rsatkichlar:</b>\n"
            f"• Jami fikrlar: 1,250\n"
            f"• Ijobiy fikrlar: 1,185 (94.8%)\n"
            f"• Salbiy fikrlar: 65 (5.2%)\n"
            f"• O'rtacha fikr uzunligi: 45 so'z\n\n"
            f"📅 <b>Vaqt bo'yicha:</b>\n"
            f"• Bugun: 45 ta fikr\n"
            f"• Bu hafta: 234 ta fikr\n"
            f"• Bu oy: 890 ta fikr\n\n"
            f"📋 <b>Eng ko'p so'raladigan mavzular:</b>\n"
            f"1. Texnik xizmat sifat (35%)\n"
            f"2. Javob vaqti (28%)\n"
            f"3. Operator malakasi (22%)\n"
            f"4. Xizmat narxi (15%)"
        )
        
        await call.message.edit_text(text)

    @router.callback_query(F.data == "detailed_operator_rating")
    async def detailed_operator_rating(call: CallbackQuery):
        """Show detailed operator rating"""
        await call.answer()
        
        text = (
            f"🏆 <b>Batafsil operator reytingi</b>\n\n"
            f"🥇 <b>1-o'rin: Aziz Karimov</b>\n"
            f"   ⭐ Reyting: 4.9/5\n"
            f"   💬 Chatlar: 156\n"
            f"   😊 Mamnuniyat: 98.5%\n"
            f"   ⏱ O'rtacha javob vaqti: 1.2 daqiqa\n"
            f"   📈 O'sish: +0.3\n\n"
            f"🥈 <b>2-o'rin: Bekzod Toirov</b>\n"
            f"   ⭐ Reyting: 4.8/5\n"
            f"   💬 Chatlar: 142\n"
            f"   😊 Mamnuniyat: 97.2%\n"
            f"   ⏱ O'rtacha javob vaqti: 1.5 daqiqa\n"
            f"   📈 O'sish: +0.2\n\n"
            f"🥉 <b>3-o'rin: Dilshod Rahimov</b>\n"
            f"   ⭐ Reyting: 4.7/5\n"
            f"   💬 Chatlar: 128\n"
            f"   😊 Mamnuniyat: 96.8%\n"
            f"   ⏱ O'rtacha javob vaqti: 1.8 daqiqa\n"
            f"   📈 O'sish: +0.1"
        )
        
        await call.message.edit_text(text)

    return router
