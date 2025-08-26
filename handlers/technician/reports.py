from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.technician_buttons import get_reports_back_keyboard
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from keyboards.technician_buttons import get_reports_keyboard
from filters.role_filter import RoleFilter

def get_reports_router():
    """Technician reports router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("technician")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text == "📊 Hisobotlar")
    async def show_reports_menu(message: Message, state: FSMContext):
        """Show reports menu handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            
            lang = user.get('language', 'uz')
            
            text = f"""
📊 <b>Hisobotlar</b>

📈 Kunlik hisobot
📊 Haftalik hisobot
📋 Oylik hisobot
📋 Ish natijalari

Kerakli hisobotni tanlang:
            """
            
            await message.answer(
                text.strip(),
                parse_mode='HTML',
                reply_markup=get_reports_keyboard(lang)
            )
            
        except Exception as e:
            await message.answer("❌ Xatolik yuz berdi")

    @router.callback_query(F.data == "tech_daily_report")
    async def daily_report(callback: CallbackQuery, state: FSMContext):
        """Daily report handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            lang = user.get('language', 'uz')
            
            # Mock stats data (like other modules)
            stats = {
                'total': 15,
                'completed': 12,
                'in_progress': 2,
                'new': 1,
                'completion_rate': 80,
                'avg_time': 2.5
            }
            
            text = f"""
📈 <b>Kunlik hisobot</b>
📅 {datetime.now().strftime('%d.%m.%Y')}

📊 <b>Statistika:</b>
• Jami vazifalar: {stats.get('total', 0)}
• Bajarilgan: {stats.get('completed', 0)}
• Jarayonda: {stats.get('in_progress', 0)}
• Yangi: {stats.get('new', 0)}

📈 <b>Samaradorlik:</b>
• Bajarish foizi: {stats.get('completion_rate', 0)}%
• O'rtacha vaqt: {stats.get('avg_time', 0)} soat
            """
            
            keyboard = get_reports_back_keyboard('uz')
            await callback.message.edit_text(
                text.strip(),
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_weekly_report")
    async def weekly_report(callback: CallbackQuery, state: FSMContext):
        """Weekly report handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            lang = user.get('language', 'uz')
            
            # Mock stats data (like other modules)
            stats = {
                'total': 85,
                'completed': 72,
                'in_progress': 8,
                'new': 5,
                'completion_rate': 85,
                'avg_time': 2.3
            }
            
            text = f"""
📊 <b>Haftalik hisobot</b>
📅 {datetime.now().strftime('%d.%m.%Y')}

📊 <b>Statistika:</b>
• Jami vazifalar: {stats.get('total', 0)}
• Bajarilgan: {stats.get('completed', 0)}
• Jarayonda: {stats.get('in_progress', 0)}
• Yangi: {stats.get('new', 0)}

📈 <b>Samaradorlik:</b>
• Bajarish foizi: {stats.get('completion_rate', 0)}%
• O'rtacha vaqt: {stats.get('avg_time', 0)} soat
            """
            
            keyboard = get_reports_back_keyboard('uz')
            await callback.message.edit_text(
                text.strip(),
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_monthly_report")
    async def monthly_report(callback: CallbackQuery, state: FSMContext):
        """Monthly report handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            lang = user.get('language', 'uz')
            
            # Mock stats data (like other modules)
            stats = {
                'total': 320,
                'completed': 285,
                'in_progress': 25,
                'new': 10,
                'completion_rate': 89,
                'avg_time': 2.1
            }
            
            text = f"""
📋 <b>Oylik hisobot</b>
📅 {datetime.now().strftime('%d.%m.%Y')}

📊 <b>Statistika:</b>
• Jami vazifalar: {stats.get('total', 0)}
• Bajarilgan: {stats.get('completed', 0)}
• Jarayonda: {stats.get('in_progress', 0)}
• Yangi: {stats.get('new', 0)}

📈 <b>Samaradorlik:</b>
• Bajarish foizi: {stats.get('completion_rate', 0)}%
• O'rtacha vaqt: {stats.get('avg_time', 0)} soat
            """
            
            buttons = [[
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="tech_back_to_reports"
                )
            ]]
            
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            await callback.message.edit_text(
                text.strip(),
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_performance_report")
    async def performance_report(callback: CallbackQuery, state: FSMContext):
        """Performance report handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            lang = user.get('language', 'uz')
            
            # Mock performance data (like other modules)
            performance = {
                'total_orders': 150,
                'completed_orders': 135,
                'avg_completion_time': 2.5,
                'customer_satisfaction': 4.8,
                'quality_score': 95,
                'efficiency_rating': 92
            }
            
            text = f"""
📋 <b>Ish natijalari</b>
📅 {datetime.now().strftime('%d.%m.%Y')}

📊 <b>Umumiy ko'rsatkichlar:</b>
• Jami buyurtmalar: {performance.get('total_orders', 0)}
• Bajarilgan: {performance.get('completed_orders', 0)}
• O'rtacha vaqt: {performance.get('avg_completion_time', 0)} soat

📈 <b>Baholash:</b>
• Mijozlar mamnuniyati: {performance.get('customer_satisfaction', 0)}/5
• Sifat ko'rsatkichi: {performance.get('quality_score', 0)}%
• Samaradorlik: {performance.get('efficiency_rating', 0)}%
            """
            
            keyboard = get_reports_back_keyboard('uz')
            await callback.message.edit_text(
                text.strip(),
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "tech_back_to_reports")
    async def back_to_reports(callback: CallbackQuery, state: FSMContext):
        """Back to reports handler"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Technician xodimi',
                'language': 'uz',
                'role': 'technician'
            }
            lang = user.get('language', 'uz')
            
            text = f"""
📊 <b>Hisobotlar</b>

📈 Kunlik hisobot
📊 Haftalik hisobot
📋 Oylik hisobot
📋 Ish natijalari

Kerakli hisobotni tanlang:
            """
            
            await callback.message.edit_text(
                text.strip(),
                parse_mode='HTML',
                reply_markup=get_reports_keyboard(lang)
            )
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    return router

# Mock functions (like other modules)
async def get_technician_stats(technician_id: int, period: str):
    """Get technician stats (mock function like other modules)"""
    try:
        if period == 'daily':
            return {
                'total': 15,
                'completed': 12,
                'in_progress': 2,
                'new': 1,
                'completion_rate': 80,
                'avg_time': 2.5
            }
        elif period == 'weekly':
            return {
                'total': 85,
                'completed': 72,
                'in_progress': 8,
                'new': 5,
                'completion_rate': 85,
                'avg_time': 2.3
            }
        elif period == 'monthly':
            return {
                'total': 320,
                'completed': 285,
                'in_progress': 25,
                'new': 10,
                'completion_rate': 89,
                'avg_time': 2.1
            }
        else:
            return {
                'total': 0,
                'completed': 0,
                'in_progress': 0,
                'new': 0,
                'completion_rate': 0,
                'avg_time': 0
            }
    except Exception as e:
        return {
            'total': 0,
            'completed': 0,
            'in_progress': 0,
            'new': 0,
            'completion_rate': 0,
            'avg_time': 0
        }

async def get_technician_performance(technician_id: int):
    """Get technician performance (mock function like other modules)"""
    try:
        return {
            'total_orders': 150,
            'completed_orders': 135,
            'avg_completion_time': 2.5,
            'customer_satisfaction': 4.8,
            'quality_score': 95,
            'efficiency_rating': 92
        }
    except Exception as e:
        return {
            'total_orders': 0,
            'completed_orders': 0,
            'avg_completion_time': 0,
            'customer_satisfaction': 0,
            'quality_score': 0,
            'efficiency_rating': 0
        }
