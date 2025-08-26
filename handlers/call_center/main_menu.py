"""
Call Center Main Menu Handler
Manages call center main menu and dashboard
"""

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.call_center_buttons import call_center_main_menu_reply

# States imports
from states.call_center import CallCenterMainMenuStates
from filters.role_filter import RoleFilter

# Mock functions to replace utils and database imports
async def get_user_language(user_id: int) -> str:
    """Mock user language"""
    return 'uz'

async def get_call_center_stats() -> Dict[str, Any]:
    """Mock call center statistics"""
    return {
        'calls_today': 45,
        'orders_today': 23,
        'pending_callbacks': 8,
        'active_chats': 12,
        'conversion_rate': 78
    }

def get_call_center_main_menu_router():
    """Get call center main menu router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["/start", "/callcenter", "📞 Call Center", " Колл-центр"]))
    async def call_center_start(message: Message, state: FSMContext):
        """Call center start"""
        lang = await get_user_language(message.from_user.id)
        
        # Mock dashboard stats
        stats = await get_call_center_stats()
        
        welcome_text = (
            f"📞 <b>{'Call Center Panel' if lang == 'uz' else 'Панель call-центра'}</b>\n\n"
            f"📊 <b>{'Bugungi holat' if lang == 'uz' else 'Состояние сегодня'}:</b>\n"
            f"📞 {'Bugungi qo\'ng\'iroqlar' if lang == 'uz' else 'Звонки сегодня'}: <b>{stats.get('calls_today', 0)}</b>\n"
            f"📋 {'Bugungi buyurtmalar' if lang == 'uz' else 'Заказы сегодня'}: <b>{stats.get('orders_today', 0)}</b>\n"
            f"⏳ {'Kutilayotgan' if lang == 'uz' else 'Ожидающие'}: <b>{stats.get('pending_callbacks', 0)}</b>\n"
            f"💬 {'Faol chatlar' if lang == 'uz' else 'Активные чаты'}: <b>{stats.get('active_chats', 0)}</b>\n"
            f"🎯 {'Konversiya' if lang == 'uz' else 'Конверсия'}: <b>{stats.get('conversion_rate', 0)}%</b>"
        )
        
        await state.set_state(CallCenterMainMenuStates.main_menu)
        await message.answer(
            welcome_text,
            reply_markup=call_center_main_menu_reply(lang)
        )

    @router.message(F.text.in_(['🏠 Bosh sahifa', '🏠 Главная']))
    async def call_center_home(message: Message, state: FSMContext):
        """Call center home"""
        lang = await get_user_language(message.from_user.id)
        
        # Mock dashboard stats
        stats = await get_call_center_stats()
        
        welcome_text = (
            f"📞 <b>{'Call Center Panel' if lang == 'uz' else 'Панель call-центра'}</b>\n\n"
            f"📊 <b>{'Bugungi holat' if lang == 'uz' else 'Состояние сегодня'}:</b>\n"
            f"📞 {'Bugungi qo\'ng\'iroqlar' if lang == 'uz' else 'Звонки сегодня'}: <b>{stats.get('calls_today', 0)}</b>\n"
            f"📋 {'Bugungi buyurtmalar' if lang == 'uz' else 'Заказы сегодня'}: <b>{stats.get('orders_today', 0)}</b>\n"
            f"⏳ {'Kutilayotgan' if lang == 'uz' else 'Ожидающие'}: <b>{stats.get('pending_callbacks', 0)}</b>\n"
            f"💬 {'Faol chatlar' if lang == 'uz' else 'Активные чаты'}: <b>{stats.get('active_chats', 0)}</b>\n"
            f"🎯 {'Konversiya' if lang == 'uz' else 'Конверсия'}: <b>{stats.get('conversion_rate', 0)}%</b>"
        )
        
        await state.set_state(CallCenterMainMenuStates.main_menu)
        await message.answer(
            welcome_text,
            reply_markup=call_center_main_menu_reply(lang)
        )

    @router.message(F.text.in_(['ℹ️ Yordam', 'ℹ️ Помощь']))
    async def call_center_help(message: Message, state: FSMContext):
        """Call center help"""
        lang = await get_user_language(message.from_user.id)
        
        if lang == 'uz':
            help_text = (
                "📞 <b>Call Center yordam</b>\n\n"
                "🔧 <b>Asosiy funksiyalar:</b>\n"
                "📞 Qo'ng'iroqlar boshqaruvi\n"
                "📋 Buyurtmalar yaratish\n"
                "🔍 Mijoz qidirish\n"
                "💬 Chat sessiyalari\n"
                "⭐️ Fikr-mulohaza\n"
                "📊 Statistika\n\n"
                "💡 Qo'shimcha ma'lumot uchun admin bilan bog'laning."
            )
        else:
            help_text = (
                "📞 <b>Помощь call-центра</b>\n\n"
                "🔧 <b>Основные функции:</b>\n"
                "📞 Управление звонками\n"
                "📋 Создание заказов\n"
                "🔍 Поиск клиентов\n"
                "💬 Сессии чата\n"
                "⭐️ Обратная связь\n"
                "📊 Статистика\n\n"
                "💡 Для дополнительной информации свяжитесь с администратором."
            )
        
        await message.answer(help_text, parse_mode='HTML')

    return router

async def show_call_center_main_menu(message: Message):
    """Show call center main menu"""
    lang = await get_user_language(message.from_user.id)
    
    # Mock dashboard stats
    stats = await get_call_center_stats()
    
    welcome_text = (
        f"📞 <b>{'Call Center Panel' if lang == 'uz' else 'Панель call-центра'}</b>\n\n"
        f"📊 <b>{'Bugungi holat' if lang == 'uz' else 'Состояние сегодня'}:</b>\n"
        f"📞 {'Bugungi qo\'ng\'iroqlar' if lang == 'uz' else 'Звонки сегодня'}: <b>{stats.get('calls_today', 0)}</b>\n"
        f"📋 {'Bugungi buyurtmalar' if lang == 'uz' else 'Заказы сегодня'}: <b>{stats.get('orders_today', 0)}</b>\n"
        f"⏳ {'Kutilayotgan' if lang == 'uz' else 'Ожидающие'}: <b>{stats.get('pending_callbacks', 0)}</b>\n"
        f"💬 {'Faol chatlar' if lang == 'uz' else 'Активные чаты'}: <b>{stats.get('active_chats', 0)}</b>\n"
        f"🎯 {'Konversiya' if lang == 'uz' else 'Конверсия'}: <b>{stats.get('conversion_rate', 0)}%</b>"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=call_center_main_menu_reply(lang)
    )