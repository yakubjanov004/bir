"""
Call Center Supervisor Handler
Manages call center supervisor functions
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from typing import Optional, Dict, Any

# Keyboard imports
from keyboards.call_center_buttons import call_center_supervisor_main_menu

# States imports
from states.call_center import CallCenterSupervisorStates
from filters.role_filter import RoleFilter

def get_call_center_supervisor_router():
    """Get call center supervisor router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center_supervisor")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📞 Call Center Supervisor", "📞 Руководитель call-центра"]))
    async def call_center_supervisor_start(message: Message, state: FSMContext):
        """Call center supervisor start"""
        text = (
            "📞 <b>Call Center Supervisor</b>\n\n"
            "Call center operatorlarini boshqarish va nazorat qilish uchun bo'limni tanlang."
        )
        
        await message.answer(
            text,
            reply_markup=get_supervisor_keyboard('uz')
        )
        await state.set_state(CallCenterSupervisorStates.supervisor)

    @router.message(F.text.in_(["📋 So'rovlarni tayinlash", "📋 Назначить запросы"]))
    async def show_pending_assignments(message: Message, state: FSMContext):
        """Show pending call center direct resolution requests"""
        lang = 'uz'  # Default language
        
        # Mock pending requests
        pending_requests = [
            {
                'id': 'REQ001',
                'description': 'Internet uzulish muammosi',
                'priority': 'Yuqori',
                'created_at': '14:30'
            },
            {
                'id': 'REQ002',
                'description': 'TV signal yo\'q',
                'priority': 'O\'rta',
                'created_at': '14:25'
            },
            {
                'id': 'REQ003',
                'description': 'Telefon xizmati muammosi',
                'priority': 'Yuqori',
                'created_at': '14:20'
            }
        ]
        
        if pending_requests:
            await state.set_state(CallCenterSupervisorStates.assign_requests)
            
            pending_text = "📋 Tayinlash uchun so'rovlar:" if lang == 'uz' else "📋 Запросы для назначения:"
            text = f"{pending_text}\n\n"
            
            for request in pending_requests:
                text += f"🆔 ID: {request['id']}\n"
                text += f"📝 Tavsif: {request['description']}\n"
                text += f"🎯 Ustuvorlik: {request['priority']}\n"
                text += f"⏰ Yaratilgan: {request['created_at']}\n\n"
            
            # Mock available operators
            operators = [
                {'id': 1, 'name': 'Aziz Karimov'},
                {'id': 2, 'name': 'Malika Yusupova'},
                {'id': 3, 'name': 'Bekzod Toirov'}
            ]
            
            select_text = "Operator tanlang:" if lang == 'uz' else "Выберите оператора:"
            text += f"\n{select_text}"
            
            await message.answer(
                text,
                reply_markup=call_center_operator_selection_keyboard(operators, lang)
            )
        else:
            no_requests_text = "Tayinlash uchun so'rovlar yo'q." if lang == 'uz' else "Нет запросов для назначения."
            await message.answer(no_requests_text)

    @router.callback_query(F.data.startswith("assign_cc_operator_"))
    async def assign_to_operator(callback: CallbackQuery, state: FSMContext):
        """Assign request to operator"""
        await callback.answer()
        
        operator_id = callback.data.replace("assign_cc_operator_", "")
        
        # Mock assignment
        success_text = (
            f"✅ So'rov operator #{operator_id} ga tayinlandi!\n\n"
            f"📋 So'rov muvaffaqiyatli tayinlandi va operator xabardor qilindi."
        )
        
        await callback.message.edit_text(success_text)
        await state.clear()

    @router.callback_query(F.data == "cc_supervisor_back")
    async def supervisor_back(callback: CallbackQuery, state: FSMContext):
        """Handle back to supervisor main menu"""
        await callback.answer()
        
        lang = 'uz'  # Default language
        
        welcome_text = "📞 Call center supervisor paneliga xush kelibsiz!" if lang == 'uz' else "📞 Добро пожаловать в панель руководителя call-центра!"
        
        await callback.message.edit_text(
            welcome_text,
            reply_markup=call_center_supervisor_main_menu(lang)
        )
        await state.set_state(CallCenterSupervisorStates.main_menu)

    return router
