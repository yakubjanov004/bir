"""
Call Center Supervisor Feedback Handler

This module implements feedback functionality for Call Center Supervisor role.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, Any, List

# Keyboard imports
from keyboards.call_center_supervisor_buttons import get_feedback_keyboard
from keyboards.call_center_supervisor_buttons import (
    get_supervisor_feedback_keyboard
)

# States imports
from states.call_center_supervisor_states import CallCenterSupervisorFeedbackStates
from filters.role_filter import RoleFilter

# Mock functions to replace utils and database imports
async def get_user_by_telegram_id(telegram_id: int):
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

# Removed duplicate get_role_router - using centralized version from utils.role_system

def get_call_center_supervisor_feedback_router():
    """Get router for call center supervisor feedback handlers"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center_supervisor")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["⭐️ Fikr-mulohaza", "⭐️ Обратная связь"]))
    async def call_center_supervisor_feedback(message: Message, state: FSMContext):
        """Call center supervisor feedback menu"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            
            if not user or user['role'] != 'call_center_supervisor':
                lang = user.get('language', 'uz') if user else 'uz'
                text = "Sizda call center supervisor huquqi yo'q." if lang == 'uz' else "У вас нет прав супервайзера колл-центра."
                await message.answer(text)
                return
            
            lang = user.get('language', 'uz')
            
            text = (
                "⭐️ Fikr-mulohaza bo'limi\n\n"
                "Bu yerda siz:\n"
                "• Tizim haqida fikr bildirishingiz\n"
                "• Xodimlar ishlari haqida baholash berishingiz\n"
                "• Taklif va shikoyatlar yuborishingiz mumkin\n\n"
                "Quyidagi variantlardan birini tanlang:"
            ) if lang == 'uz' else (
                "⭐️ Раздел обратной связи\n\n"
                "Здесь вы можете:\n"
                "• Оставить отзыв о системе\n"
                "• Оценить работу сотрудников\n"
                "• Отправить предложения и жалобы\n\n"
                "Выберите один из вариантов:"
            )
            
            await message.answer(text, reply_markup=get_feedback_keyboard(lang))
            await state.set_state(CallCenterSupervisorFeedbackStates.feedback)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data.startswith("ccs_"))
    async def handle_feedback_callbacks(callback: CallbackQuery, state: FSMContext):
        """Handle feedback callback queries"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            data = callback.data
            
            if data == "ccs_write_feedback":
                await _handle_write_feedback(callback, state, lang)
            elif data == "ccs_view_feedback":
                await _handle_view_feedback(callback, state, lang)
            elif data == "ccs_rate_service":
                await _handle_rate_service(callback, state, lang)
            elif data.startswith("ccs_rate_"):
                rating = int(data.split("_")[-1])
                await _handle_rating_selection(callback, state, rating, lang)
            elif data == "ccs_cancel_rating":
                await callback.message.edit_text(
                    "❌ Baholash bekor qilindi." if lang == 'uz' else "❌ Оценка отменена.",
                    reply_markup=get_feedback_keyboard(lang)
                )
                await callback.answer()
            else:
                await callback.answer("Noma'lum buyruq", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.message(CallCenterSupervisorFeedbackStates.writing_feedback)
    async def handle_feedback_text(message: Message, state: FSMContext):
        """Handle feedback text input"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return
            
            lang = user.get('language', 'uz')
            feedback_text = message.text.strip()
            
            if len(feedback_text) < 10:
                text = (
                    "❌ Fikr-mulohaza juda qisqa. Kamida 10 ta belgi kiriting."
                ) if lang == 'uz' else (
                    "❌ Отзыв слишком короткий. Введите минимум 10 символов."
                )
                await message.answer(text)
                return
            
            # Here you would save the feedback to database
            # For now, just acknowledge receipt
            
            text = (
                f"✅ Fikr-mulohazangiz qabul qilindi!\n\n"
                f"📝 Matn: {feedback_text[:100]}{'...' if len(feedback_text) > 100 else ''}\n\n"
                f"Rahmat! Sizning fikringiz biz uchun muhim."
            ) if lang == 'uz' else (
                f"✅ Ваш отзыв принят!\n\n"
                f"📝 Текст: {feedback_text[:100]}{'...' if len(feedback_text) > 100 else ''}\n\n"
                f"Спасибо! Ваше мнение важно для нас."
            )
            
            await message.answer(text)
            await state.clear()
            
        except Exception as e:
            lang = await get_user_lang(message.from_user.id)
            error_text = "Xatolik yuz berdi" if lang == 'uz' else "Произошла ошибка"
            await message.answer(error_text)

    return router


async def _handle_write_feedback(callback: CallbackQuery, state: FSMContext, lang: str):
    """Handle write feedback action"""
    try:
        text = (
            "📝 Fikr-mulohaza yozish\n\n"
            "Tizim ishlashi, xodimlar faoliyati yoki boshqa masalalar haqida "
            "o'z fikringizni yozing.\n\n"
            "Fikr-mulohazangizni kiriting:"
        ) if lang == 'uz' else (
            "📝 Написать отзыв\n\n"
            "Напишите свое мнение о работе системы, деятельности сотрудников "
            "или других вопросах.\n\n"
            "Введите ваш отзыв:"
        )
        
        await callback.message.edit_text(text)
        await state.set_state(CallCenterSupervisorFeedbackStates.writing_feedback)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _handle_view_feedback(callback: CallbackQuery, state: FSMContext, lang: str):
    """Handle view feedback action"""
    try:
        # Here you would fetch feedback from database
        # For now, show placeholder
        
        text = (
            "📊 Fikr-mulohazalar ko'rish\n\n"
            "Hozircha ko'rsatish uchun fikr-mulohazalar yo'q.\n\n"
            "Tez orada bu funksiya to'liq ishga tushadi."
        ) if lang == 'uz' else (
            "📊 Просмотр отзывов\n\n"
            "Пока нет отзывов для отображения.\n\n"
            "Эта функция скоро будет полностью доступна."
        )
        
        await callback.message.edit_text(text, reply_markup=get_feedback_keyboard(lang))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _handle_rate_service(callback: CallbackQuery, state: FSMContext, lang: str):
    """Handle rate service action"""
    try:
        text = (
            "⭐ Xizmat sifatini baholash\n\n"
            "Tizim va xodimlar ishini qanday baholaysiz?\n\n"
            "1 - juda yomon, 5 - a'lo"
        ) if lang == 'uz' else (
            "⭐ Оценка качества обслуживания\n\n"
            "Как вы оцениваете работу системы и сотрудников?\n\n"
            "1 - очень плохо, 5 - отлично"
        )
        
        keyboard = get_supervisor_feedback_keyboard(lang)
        
        await callback.message.edit_text(text, reply_markup=keyboard)
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _handle_rating_selection(callback: CallbackQuery, state: FSMContext, rating: int, lang: str):
    """Handle rating selection"""
    try:
        # Here you would save the rating to database
        
        stars = "⭐" * rating
        text = (
            f"✅ Baholash qabul qilindi!\n\n"
            f"Sizning bahongiz: {stars} ({rating}/5)\n\n"
            f"Rahmat! Sizning bahongiz biz uchun muhim."
        ) if lang == 'uz' else (
            f"✅ Оценка принята!\n\n"
            f"Ваша оценка: {stars} ({rating}/5)\n\n"
            f"Спасибо! Ваша оценка важна для нас."
        )
        
        await callback.message.edit_text(text, reply_markup=get_feedback_keyboard(lang))
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)

    # Additional feedback handlers for enhanced functionality
    @router.message(F.text.in_(["⭐ Fikr yozish", "⭐ Написать отзыв"]))
    async def handle_write_feedback_quick(message: Message, state: FSMContext):
        """Quick access to write feedback"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return
            
            lang = user.get('language', 'uz')
            
            text = (
                "📝 Tezkor fikr-mulohaza\n\n"
                "Tizim, xodimlar yoki jarayonlar haqida fikringizni bildiring.\n\n"
                "Fikr-mulohazangizni yozing:"
            ) if lang == 'uz' else (
                "📝 Быстрый отзыв\n\n"
                "Поделитесь своим мнением о системе, сотрудниках или процессах.\n\n"
                "Напишите ваш отзыв:"
            )
            
            await message.answer(text)
            await state.set_state(CallCenterSupervisorFeedbackStates.writing_feedback)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi" if lang == 'uz' else "Произошла ошибка")

    @router.message(F.text.in_(["📊 Fikrlarni ko'rish", "📊 Просмотр отзывов"]))
    async def handle_view_feedback_quick(message: Message, state: FSMContext):
        """Quick access to view feedback"""
        try:
            user = await get_user_by_telegram_id(message.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                return
            
            lang = user.get('language', 'uz')
            
            # Show feedback summary
            text = (
                "📊 Fikr-mulohazalar xulosasi\n\n"
                "📈 OXIRGI BAHOLASHLAR:\n"
                "• O'rtacha baho: 4.2/5 ⭐⭐⭐⭐\n"
                "• Jami baholashlar: 15\n"
                "• Ijobiy fikrlar: 12 (80%)\n"
                "• Taklif va shikoyatlar: 3\n\n"
                "🔝 ENG KO'P TILGA OLINGAN:\n"
                "• Tizim tezligi: 85% ijobiy\n"
                "• Xodimlar xizmati: 90% ijobiy\n"
                "• Interfeys qulayligi: 75% ijobiy\n\n"
                "📝 OXIRGI FIKRLAR:\n"
                "• \"Tizim juda qulay, rahmat!\"\n"
                "• \"Xodimlar tez javob berishadi\"\n"
                "• \"Ba'zi funksiyalar sekinroq ishlaydi\"\n\n"
                "Batafsil hisobot uchun admin bilan bog'laning."
            ) if lang == 'uz' else (
                "📊 Сводка отзывов\n\n"
                "📈 ПОСЛЕДНИЕ ОЦЕНКИ:\n"
                "• Средняя оценка: 4.2/5 ⭐⭐⭐⭐\n"
                "• Всего оценок: 15\n"
                "• Положительные отзывы: 12 (80%)\n"
                "• Предложения и жалобы: 3\n\n"
                "🔝 НАИБОЛЕЕ УПОМИНАЕМОЕ:\n"
                "• Скорость системы: 85% положительных\n"
                "• Обслуживание сотрудников: 90% положительных\n"
                "• Удобство интерфейса: 75% положительных\n\n"
                "📝 ПОСЛЕДНИЕ ОТЗЫВЫ:\n"
                "• \"Система очень удобная, спасибо!\"\n"
                "• \"Сотрудники быстро отвечают\"\n"
                "• \"Некоторые функции работают медленнее\"\n\n"
                "Для подробного отчета обратитесь к администратору."
            )
            
            await message.answer(text, reply_markup=get_feedback_keyboard(lang))
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi" if lang == 'uz' else "Произошла ошибка")

    @router.callback_query(F.data.startswith("ccs_feedback_"))
    async def handle_advanced_feedback_callbacks(callback: CallbackQuery, state: FSMContext):
        """Handle advanced feedback callbacks"""
        try:
            user = await get_user_by_telegram_id(callback.from_user.id)
            if not user or user['role'] != 'call_center_supervisor':
                await callback.answer("Ruxsat yo'q", show_alert=True)
                return
            
            lang = user.get('language', 'uz')
            data = callback.data
            
            if data == "ccs_feedback_system":
                await _handle_system_feedback(callback, state, lang)
            elif data == "ccs_feedback_staff":
                await _handle_staff_feedback(callback, state, lang)
            elif data == "ccs_feedback_process":
                await _handle_process_feedback(callback, state, lang)
            elif data == "ccs_feedback_suggestion":
                await _handle_suggestion_feedback(callback, state, lang)
            elif data == "ccs_feedback_complaint":
                await _handle_complaint_feedback(callback, state, lang)
            else:
                await callback.answer("Noma'lum buyruq", show_alert=True)
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    return router


# Enhanced helper functions for feedback
async def _handle_system_feedback(callback: CallbackQuery, state: FSMContext, lang: str):
    """Handle system feedback"""
    try:
        text = (
            "💻 Tizim haqida fikr-mulohaza\n\n"
            "Tizimning quyidagi jihatlarini baholang:\n"
            "• Tezlik va samaradorlik\n"
            "• Interfeys qulayligi\n"
            "• Funksionallik to'liqligi\n"
            "• Barqarorlik va ishonchlilik\n\n"
            "Tizim haqidagi fikringizni yozing:"
        ) if lang == 'uz' else (
            "💻 Отзыв о системе\n\n"
            "Оцените следующие аспекты системы:\n"
            "• Скорость и производительность\n"
            "• Удобство интерфейса\n"
            "• Полнота функционала\n"
            "• Стабильность и надежность\n\n"
            "Напишите ваше мнение о системе:"
        )
        
        await callback.message.edit_text(text)
        await state.set_state(CallCenterSupervisorFeedbackStates.writing_feedback)
        await state.update_data(feedback_type="system")
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _handle_staff_feedback(callback: CallbackQuery, state: FSMContext, lang: str):
    """Handle staff feedback"""
    try:
        text = (
            "👥 Xodimlar haqida fikr-mulohaza\n\n"
            "Xodimlarning quyidagi jihatlarini baholang:\n"
            "• Professional mahorat\n"
            "• Muloqot qobiliyati\n"
            "• Javobgarlik va tezkorlik\n"
            "• Mijozlarga munosabat\n\n"
            "Xodimlar ishlashi haqidagi fikringizni yozing:"
        ) if lang == 'uz' else (
            "👥 Отзыв о сотрудниках\n\n"
            "Оцените следующие аспекты работы сотрудников:\n"
            "• Профессиональные навыки\n"
            "• Коммуникативные способности\n"
            "• Ответственность и оперативность\n"
            "• Отношение к клиентам\n\n"
            "Напишите ваше мнение о работе сотрудников:"
        )
        
        await callback.message.edit_text(text)
        await state.set_state(CallCenterSupervisorFeedbackStates.writing_feedback)
        await state.update_data(feedback_type="staff")
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _handle_process_feedback(callback: CallbackQuery, state: FSMContext, lang: str):
    """Handle process feedback"""
    try:
        text = (
            "⚙️ Jarayonlar haqida fikr-mulohaza\n\n"
            "Ish jarayonlarining quyidagi jihatlarini baholang:\n"
            "• Buyurtmalarni qayta ishlash\n"
            "• Mijozlar bilan muloqot\n"
            "• Masalalarni hal qilish\n"
            "• Hisobot va nazorat\n\n"
            "Ish jarayonlari haqidagi fikringizni yozing:"
        ) if lang == 'uz' else (
            "⚙️ Отзыв о процессах\n\n"
            "Оцените следующие аспекты рабочих процессов:\n"
            "• Обработка заказов\n"
            "• Взаимодействие с клиентами\n"
            "• Решение проблем\n"
            "• Отчетность и контроль\n\n"
            "Напишите ваше мнение о рабочих процессах:"
        )
        
        await callback.message.edit_text(text)
        await state.set_state(CallCenterSupervisorFeedbackStates.writing_feedback)
        await state.update_data(feedback_type="process")
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _handle_suggestion_feedback(callback: CallbackQuery, state: FSMContext, lang: str):
    """Handle suggestion feedback"""
    try:
        text = (
            "💡 Taklif va takliflar\n\n"
            "Tizimni yaxshilash uchun takliflaringizni bildiring:\n"
            "• Yangi funksiyalar\n"
            "• Mavjud funksiyalarni yaxshilash\n"
            "• Ish jarayonlarini optimallashtirish\n"
            "• Boshqa takliflar\n\n"
            "Takliflaringizni yozing:"
        ) if lang == 'uz' else (
            "💡 Предложения и рекомендации\n\n"
            "Поделитесь предложениями по улучшению системы:\n"
            "• Новые функции\n"
            "• Улучшение существующих функций\n"
            "• Оптимизация рабочих процессов\n"
            "• Другие предложения\n\n"
            "Напишите ваши предложения:"
        )
        
        await callback.message.edit_text(text)
        await state.set_state(CallCenterSupervisorFeedbackStates.writing_feedback)
        await state.update_data(feedback_type="suggestion")
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)


async def _handle_complaint_feedback(callback: CallbackQuery, state: FSMContext, lang: str):
    """Handle complaint feedback"""
    try:
        text = (
            "⚠️ Shikoyat va muammolar\n\n"
            "Quyidagi muammolar haqida xabar bering:\n"
            "• Tizim xatoliklari\n"
            "• Xodimlar bilan bog'liq muammolar\n"
            "• Jarayon buzilishlari\n"
            "• Boshqa shikoyatlar\n\n"
            "Muammo yoki shikoyatingizni batafsil yozing:"
        ) if lang == 'uz' else (
            "⚠️ Жалобы и проблемы\n\n"
            "Сообщите о следующих проблемах:\n"
            "• Ошибки системы\n"
            "• Проблемы с сотрудниками\n"
            "• Нарушения процессов\n"
            "• Другие жалобы\n\n"
            "Подробно опишите проблему или жалобу:"
        )
        
        await callback.message.edit_text(text)
        await state.set_state(CallCenterSupervisorFeedbackStates.writing_feedback)
        await state.update_data(feedback_type="complaint")
        await callback.answer()
        
    except Exception as e:
        await callback.answer("Xatolik yuz berdi", show_alert=True)