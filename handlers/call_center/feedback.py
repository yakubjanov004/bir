"""
Call Center Feedback Handler
Manages call center feedback collection and analysis
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.call_center_buttons import get_feedback_keyboard

# States imports
from states.call_center_states import CallCenterFeedbackStates, CallCenterMainMenuStates
from filters.role_filter import RoleFilter

def get_call_center_feedback_router():
    """Get call center feedback router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(StateFilter(CallCenterMainMenuStates.main_menu), F.text.in_(["📝 Fikrlar", "📝 Отзывы"]))
    async def feedback_menu(message: Message, state: FSMContext):
        """Feedback main menu"""
        text = "📝 <b>Call Center Fikrlar</b>\n\nMijozlar fikrlarini boshqarish va tahlil qilish uchun bo'limni tanlang."
        
        await message.answer(
            text,
            reply_markup=get_feedback_keyboard('uz')
        )
        await state.set_state(CallCenterFeedbackStates.feedback)

    @router.message(F.text.in_(["📊 Fikrlar statistikasi", "📊 Статистика отзывов"]))
    async def feedback_statistics(message: Message):
        """Show feedback statistics"""
        # Mock feedback statistics
        feedback_stats = {
            'total_feedback': 1250,
            'positive_feedback': 1185,
            'negative_feedback': 65,
            'satisfaction_rate': '94.8%',
            'response_rate': '87.2%',
            'avg_rating': 4.6,
            'by_category': {
                'service_quality': {'count': 450, 'avg_rating': 4.7},
                'response_time': {'count': 320, 'avg_rating': 4.3},
                'operator_skill': {'count': 280, 'avg_rating': 4.8},
                'problem_resolution': {'count': 200, 'avg_rating': 4.5}
            }
        }
            
        text = (
            f"📊 <b>Fikrlar statistikasi</b>\n\n"
            f"📈 <b>Umumiy ko'rsatkichlar:</b>\n"
            f"• Jami fikrlar: {feedback_stats['total_feedback']:,}\n"
            f"• Ijobiy fikrlar: {feedback_stats['positive_feedback']:,} ({feedback_stats['positive_feedback']/feedback_stats['total_feedback']*100:.1f}%)\n"
            f"• Salbiy fikrlar: {feedback_stats['negative_feedback']:,} ({feedback_stats['negative_feedback']/feedback_stats['total_feedback']*100:.1f}%)\n"
            f"• Mamnuniyat darajasi: {feedback_stats['satisfaction_rate']}\n"
            f"• Javob berish darajasi: {feedback_stats['response_rate']}\n"
            f"• O'rtacha reyting: ⭐ {feedback_stats['avg_rating']}/5\n\n"
            f"📋 <b>Kategoriya bo'yicha:</b>\n"
        )
        
        for category, data in feedback_stats['by_category'].items():
            category_names = {
                'service_quality': 'Xizmat sifat',
                'response_time': 'Javob vaqti',
                'operator_skill': 'Operator malakasi',
                'problem_resolution': 'Muammo hal qilish'
            }
            category_name = category_names.get(category, category)
            text += f"• {category_name}: {data['count']} fikr, ⭐ {data['avg_rating']}/5\n"
        
        await message.answer(text)

    @router.message(F.text.in_(["📝 Yangi fikr qo'shish", "📝 Добавить отзыв"]))
    async def add_feedback(message: Message, state: FSMContext):
        """Add new feedback"""
        text = (
            "📝 <b>Yangi fikr qo'shish</b>\n\n"
            "Yangi fikr ma'lumotlarini kiriting:\n\n"
            "👤 <b>Mijoz ismi:</b> Mijoz to'liq ismi\n"
            "📱 <b>Telefon:</b> +998 XX XXX XX XX\n"
            "⭐ <b>Reyting:</b> 1-5 yulduz\n"
            "📝 <b>Fikr:</b> Batafsil fikr\n"
            "📋 <b>Kategoriya:</b> Xizmat turi\n\n"
            "Ma'lumotlarni kiriting:"
        )
        
        await message.answer(text)
        await state.set_state(CallCenterFeedbackStates.waiting_for_feedback_data)

    @router.message(CallCenterFeedbackStates.waiting_for_feedback_data)
    async def process_feedback_data(message: Message, state: FSMContext):
        """Process feedback data"""
        feedback_data = message.text.strip()
        
        if not feedback_data:
            await message.answer("Iltimos, fikr ma'lumotlarini kiriting.")
            return
        
        # Mock feedback creation
        success_text = (
            "✅ Yangi fikr muvaffaqiyatli qo'shildi!\n\n"
            "📝 <b>Fikr ID:</b> FB123456\n"
            "📅 <b>Qo'shilgan sana:</b> 2024-01-15\n"
            "📊 <b>Status:</b> Faol"
        )
        
        await message.answer(success_text)
        await state.clear()

    @router.message(F.text.in_(["📋 Fikrlar ro'yxati", "📋 Список отзывов"]))
    async def feedback_list(message: Message):
        """Show feedback list"""
        # Mock feedback list
        feedback_list = [
            {
                'id': 'FB001',
                'client_name': 'Bekzod Toirov',
                'rating': 5,
                'category': 'Internet xizmati',
                'created_at': '2024-01-15',
                'status': 'positive'
            },
            {
                'id': 'FB002',
                'client_name': 'Aziz Karimov',
                'rating': 4,
                'category': 'TV xizmati',
                'created_at': '2024-01-14',
                'status': 'positive'
            },
            {
                'id': 'FB003',
                'client_name': 'Malika Yusupova',
                'rating': 2,
                'category': 'Texnik xizmat',
                'created_at': '2024-01-13',
                'status': 'negative'
            }
        ]
        
        text = f"📋 <b>Fikrlar ro'yxati ({len(feedback_list)})</b>\n\n"
        
        for i, feedback in enumerate(feedback_list, 1):
            rating_stars = "⭐" * feedback['rating']
            status_emoji = "✅" if feedback['status'] == 'positive' else "❌"
            text += (
                f"{i}. {status_emoji} <b>{feedback['client_name']}</b>\n"
                f"   🆔 {feedback['id']}\n"
                f"   {rating_stars}\n"
                f"   📋 {feedback['category']}\n"
                f"   📅 {feedback['created_at']}\n\n"
            )
        
        await message.answer(text)

    @router.message(F.text.in_(["🔍 Fikr qidirish", "🔍 Поиск отзывов"]))
    async def search_feedback(message: Message, state: FSMContext):
        """Search feedback"""
        text = (
            "🔍 <b>Fikr qidirish</b>\n\n"
            "Qidirish uchun quyidagi ma'lumotlardan birini kiriting:\n\n"
            "👤 <b>Mijoz ismi:</b>\n"
            "📱 <b>Telefon raqam:</b>\n"
            "🆔 <b>Fikr ID:</b>\n"
            "📋 <b>Kategoriya:</b>\n\n"
            "Qidirish ma'lumotini yuboring:"
        )
        
        await message.answer(text)
        await state.set_state(CallCenterFeedbackStates.waiting_for_search_query)

    @router.message(CallCenterFeedbackStates.waiting_for_search_query)
    async def process_search_query(message: Message, state: FSMContext):
        """Process search query"""
        search_query = message.text.strip()
        
        if not search_query:
            await message.answer("Iltimos, qidirish ma'lumotini kiriting.")
            return
        
        # Mock search results
        search_results = [
            {
                'id': 'FB001',
                'client_name': 'Bekzod Toirov',
                'phone': '+998 90 123 45 67',
                'rating': 5,
                'category': 'Internet xizmati',
                'feedback_text': 'Ajoyib xizmat! Internet juda tez ishlayapti.',
                'created_at': '2024-01-15',
                'status': 'positive'
            }
        ]
        
        if not search_results:
            text = f"❌ '{search_query}' bo'yicha fikr topilmadi."
            await message.answer(text)
            await state.clear()
            return
        
        text = f"🔍 <b>Qidirish natijalari</b>\n\n"
        text += f"'{search_query}' bo'yicha {len(search_results)} ta fikr topildi:\n\n"
        
        for i, feedback in enumerate(search_results, 1):
            rating_stars = "⭐" * feedback['rating']
            status_emoji = "✅" if feedback['status'] == 'positive' else "❌"
            text += (
                f"{i}. {status_emoji} <b>{feedback['client_name']}</b>\n"
                f"   📱 {feedback['phone']}\n"
                f"   🆔 {feedback['id']}\n"
                f"   {rating_stars}\n"
                f"   📋 {feedback['category']}\n"
                f"   📝 {feedback['feedback_text']}\n"
                f"   📅 {feedback['created_at']}\n\n"
            )
        
        await message.answer(text)
        await state.clear()

    return router
