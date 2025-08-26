"""
Call Center Statistics Handler
Manages call center statistics and reports
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.call_center_buttons import call_center_statistics_menu

# States imports
from states.call_center import CallCenterReportsStates
from filters.role_filter import RoleFilter

def get_call_center_statistics_router():
    """Get call center statistics router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text == "📊 Statistikalar")
    async def handle_statistics(message: Message, state: FSMContext):
        """Handle statistics menu"""
        text = "📊 <b>Call Center Statistikalar</b>\n\nStatistikalar va hisobotlarni ko'rish uchun turini tanlang."
        
        await message.answer(
            text,
            reply_markup=get_statistics_keyboard('uz')
        )
        await state.set_state(CallCenterReportsStates.statistics)

    @router.message(CallCenterReportsStates.statistics, F.text == "📅 Bugungi ko'rsatkichlar")
    async def handle_daily_stats(message: Message, state: FSMContext):
        """Handle daily statistics"""
        # Mock daily statistics
        daily_stats = {
            'total_calls': 45,
            'answered_calls': 42,
            'missed_calls': 3,
            'avg_call_duration': '8.5 daqiqa',
            'satisfaction_rate': '94.2%',
            'orders_created': 23,
            'issues_resolved': 38,
            'pending_issues': 7
        }
        
        text = (
            f"📅 <b>Bugungi ko'rsatkichlar</b>\n\n"
            f"📞 <b>Qo'ng'iroqlar:</b>\n"
            f"• Jami qo'ng'iroqlar: {daily_stats['total_calls']}\n"
            f"• Javob berilgan: {daily_stats['answered_calls']}\n"
            f"• O'tkazib yuborilgan: {daily_stats['missed_calls']}\n"
            f"• O'rtacha davomiyligi: {daily_stats['avg_call_duration']}\n\n"
            f"📊 <b>Natijalar:</b>\n"
            f"• Mamnuniyat darajasi: {daily_stats['satisfaction_rate']}\n"
            f"• Yaratilgan buyurtmalar: {daily_stats['orders_created']}\n"
            f"• Hal qilingan muammolar: {daily_stats['issues_resolved']}\n"
            f"• Kutilayotgan muammolar: {daily_stats['pending_issues']}"
        )
        
        await message.answer(text)

    @router.message(CallCenterReportsStates.statistics, F.text == "📊 Haftalik hisobot")
    async def handle_weekly_stats(message: Message, state: FSMContext):
        """Handle weekly statistics"""
        # Mock weekly statistics
        weekly_stats = {
            'total_calls': 312,
            'answered_calls': 298,
            'missed_calls': 14,
            'avg_call_duration': '9.2 daqiqa',
            'satisfaction_rate': '93.8%',
            'orders_created': 156,
            'issues_resolved': 245,
            'pending_issues': 23,
            'top_issues': [
                'Internet uzulish - 45 ta',
                'TV signal muammosi - 32 ta',
                'Telefon xizmati - 28 ta',
                'Hisob ma\'lumotlari - 15 ta'
            ]
        }
        
        text = (
            f"📊 <b>Haftalik hisobot</b>\n\n"
            f"📞 <b>Qo'ng'iroqlar:</b>\n"
            f"• Jami qo'ng'iroqlar: {weekly_stats['total_calls']}\n"
            f"• Javob berilgan: {weekly_stats['answered_calls']}\n"
            f"• O'tkazib yuborilgan: {weekly_stats['missed_calls']}\n"
            f"• O'rtacha davomiyligi: {weekly_stats['avg_call_duration']}\n\n"
            f"📊 <b>Natijalar:</b>\n"
            f"• Mamnuniyat darajasi: {weekly_stats['satisfaction_rate']}\n"
            f"• Yaratilgan buyurtmalar: {weekly_stats['orders_created']}\n"
            f"• Hal qilingan muammolar: {weekly_stats['issues_resolved']}\n"
            f"• Kutilayotgan muammolar: {weekly_stats['pending_issues']}\n\n"
            f"📋 <b>Eng ko'p muammolar:</b>\n"
        )
        
        for issue in weekly_stats['top_issues']:
            text += f"• {issue}\n"
        
        await message.answer(text)

    @router.message(CallCenterReportsStates.statistics, F.text == "📈 Oylik hisobot")
    async def handle_monthly_stats(message: Message, state: FSMContext):
        """Handle monthly statistics"""
        # Mock monthly statistics
        monthly_stats = {
            'total_calls': 1245,
            'answered_calls': 1189,
            'missed_calls': 56,
            'avg_call_duration': '8.8 daqiqa',
            'satisfaction_rate': '94.5%',
            'orders_created': 623,
            'issues_resolved': 987,
            'pending_issues': 89,
            'revenue_generated': '12,450,000 so\'m',
            'cost_saved': '2,340,000 so\'m'
        }
        
        text = (
            f"📈 <b>Oylik hisobot</b>\n\n"
            f"📞 <b>Qo'ng'iroqlar:</b>\n"
            f"• Jami qo'ng'iroqlar: {monthly_stats['total_calls']:,}\n"
            f"• Javob berilgan: {monthly_stats['answered_calls']:,}\n"
            f"• O'tkazib yuborilgan: {monthly_stats['missed_calls']:,}\n"
            f"• O'rtacha davomiyligi: {monthly_stats['avg_call_duration']}\n\n"
            f"📊 <b>Natijalar:</b>\n"
            f"• Mamnuniyat darajasi: {monthly_stats['satisfaction_rate']}\n"
            f"• Yaratilgan buyurtmalar: {monthly_stats['orders_created']:,}\n"
            f"• Hal qilingan muammolar: {monthly_stats['issues_resolved']:,}\n"
            f"• Kutilayotgan muammolar: {monthly_stats['pending_issues']:,}\n\n"
            f"💰 <b>Iqtisodiy natijalar:</b>\n"
            f"• Yaratilgan daromad: {monthly_stats['revenue_generated']}\n"
            f"• Tejab qolgan xarajatlar: {monthly_stats['cost_saved']}"
        )
        
        await message.answer(text)

    @router.message(CallCenterReportsStates.statistics, F.text == "🎯 Mening samaradorligim")
    async def handle_performance(message: Message, state: FSMContext):
        """Handle personal performance"""
        # Mock personal performance
        performance = {
            'calls_handled': 45,
            'avg_call_duration': '7.8 daqiqa',
            'satisfaction_rate': '96.2%',
            'orders_created': 23,
            'issues_resolved': 38,
            'response_time': '2.3 daqiqa',
            'ranking': '2-o\'rin',
            'achievements': [
                'Eng tez javob berish',
                'Eng yuqori mamnuniyat',
                'Eng ko\'p buyurtma yaratish'
            ]
        }
        
        text = (
            f"🎯 <b>Mening samaradorligim</b>\n\n"
            f"📞 <b>Qo'ng'iroqlar:</b>\n"
            f"• Boshqarilgan qo'ng'iroqlar: {performance['calls_handled']}\n"
            f"• O'rtacha davomiyligi: {performance['avg_call_duration']}\n"
            f"• Javob berish vaqti: {performance['response_time']}\n\n"
            f"📊 <b>Natijalar:</b>\n"
            f"• Mamnuniyat darajasi: {performance['satisfaction_rate']}\n"
            f"• Yaratilgan buyurtmalar: {performance['orders_created']}\n"
            f"• Hal qilingan muammolar: {performance['issues_resolved']}\n"
            f"• Reyting: {performance['ranking']}\n\n"
            f"🏆 <b>Yutuqlar:</b>\n"
        )
        
        for achievement in performance['achievements']:
            text += f"• {achievement}\n"
        
        await message.answer(text)

    @router.message(CallCenterReportsStates.statistics, F.text == "📈 Konversiya darajasi")
    async def handle_conversion(message: Message, state: FSMContext):
        """Handle conversion rate"""
        # Mock conversion statistics
        conversion_stats = {
            'total_contacts': 1245,
            'converted_contacts': 623,
            'conversion_rate': '50.0%',
            'by_channel': {
                'phone_calls': {'contacts': 890, 'converted': 456, 'rate': '51.2%'},
                'chat_support': {'contacts': 234, 'converted': 134, 'rate': '57.3%'},
                'email_support': {'contacts': 121, 'converted': 33, 'rate': '27.3%'}
            },
            'by_service': {
                'internet': {'contacts': 567, 'converted': 289, 'rate': '51.0%'},
                'tv': {'contacts': 345, 'converted': 178, 'rate': '51.6%'},
                'phone': {'contacts': 333, 'converted': 156, 'rate': '46.8%'}
            }
        }
        
        text = (
            f"📈 <b>Konversiya darajasi</b>\n\n"
            f"📊 <b>Umumiy ko'rsatkichlar:</b>\n"
            f"• Jami aloqalar: {conversion_stats['total_contacts']:,}\n"
            f"• Konvert qilingan: {conversion_stats['converted_contacts']:,}\n"
            f"• Konversiya darajasi: {conversion_stats['conversion_rate']}\n\n"
            f"📞 <b>Kanal bo'yicha:</b>\n"
        )
        
        for channel, data in conversion_stats['by_channel'].items():
            channel_names = {
                'phone_calls': 'Telefon qo\'ng\'iroqlari',
                'chat_support': 'Chat yordam',
                'email_support': 'Email yordam'
            }
            channel_name = channel_names.get(channel, channel)
            text += f"• {channel_name}: {data['contacts']} aloqa, {data['converted']} konvert, {data['rate']}\n"
        
        text += f"\n📋 <b>Xizmat bo'yicha:</b>\n"
        
        for service, data in conversion_stats['by_service'].items():
            service_names = {
                'internet': 'Internet xizmati',
                'tv': 'TV xizmati',
                'phone': 'Telefon xizmati'
            }
            service_name = service_names.get(service, service)
            text += f"• {service_name}: {data['contacts']} aloqa, {data['converted']} konvert, {data['rate']}\n"
        
        await message.answer(text)

    @router.message(CallCenterReportsStates.statistics, F.text == "🔄 Orqaga")
    async def handle_stats_back(message: Message, state: FSMContext):
        """Handle back to main menu"""
        lang = 'uz'  # Default language
        
        await message.answer(
            "🏠 Bosh sahifaga qaytdingiz" if lang == 'uz' else "🏠 Вернулись на главную страницу"
        )
        await state.clear()

    return router
