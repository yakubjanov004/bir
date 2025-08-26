"""
Call Center Supervisor Statistics Handler

This module implements statistics and reporting functionality for Call Center Supervisor role,
providing comprehensive analytics and performance metrics for call center operations.
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Keyboard imports
from keyboards.call_center_supervisor_buttons import (
    get_statistics_menu, get_analytics_dashboard_keyboard, 
    get_performance_dashboard_keyboard, get_analytics_menu,
    get_supervisor_statistics_keyboard
)

# States imports
from states.call_center_supervisor_states import CallCenterSupervisorStatisticsStates
from filters.role_filter import RoleFilter
from states.call_center_supervisor_states import CallCenterSupervisorMainMenuStates

def get_call_center_supervisor_statistics_router():
    """Get router for call center supervisor statistics handlers"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("call_center_supervisor")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text.in_(["📊 Statistikalar", "📊 Статистика"]))
    async def supervisor_statistics(message: Message, state: FSMContext):
        """Main statistics handler for call center supervisor"""
        lang = 'uz'  # Default language
        await state.set_state(CallCenterSupervisorStatisticsStates.statistics)
        
        # Mock dashboard statistics
        stats = {
            'orders': {
                'total_orders': 45,
                'new_orders': 12,
                'in_progress_orders': 8,
                'completed_orders': 25
            },
            'staff': {
                'total_supervised_staff': 15,
                'call_center_staff': 8,
                'technician_staff': 7
            }
        }
        
        text = (
            f"📊 Call Center Supervisor Statistikasi\n\n"
            f"📋 BUYURTMALAR:\n"
            f"• Jami: {stats['orders']['total_orders']}\n"
            f"• Yangi: {stats['orders']['new_orders']}\n"
            f"• Jarayonda: {stats['orders']['in_progress_orders']}\n"
            f"• Bajarilgan: {stats['orders']['completed_orders']}\n\n"
            f"👥 XODIMLAR:\n"
            f"• Jami nazorat ostida: {stats['staff']['total_supervised_staff']}\n"
            f"• Call center: {stats['staff']['call_center_staff']}\n"
            f"• Texniklar: {stats['staff']['technician_staff']}\n\n"
            f"Batafsil hisobotni tanlang:"
        )
        
        await message.answer(text, reply_markup=get_statistics_menu(lang))

    @router.callback_query(F.data.startswith("ccs_stats_"))
    async def handle_statistics_categories(callback: CallbackQuery, state: FSMContext):
        """Handle statistics category selection"""
        await callback.answer()
        
        lang = 'uz'  # Default language
        category = callback.data.split("_")[-1]
        
        if category == "daily":
            await _show_daily_statistics(callback, lang)
        elif category == "weekly":
            await _show_weekly_statistics(callback, lang)
        elif category == "monthly":
            await _show_monthly_statistics(callback, lang)
        elif category == "performance":
            await _show_staff_performance(callback, lang)
        elif category == "analysis":
            await _show_orders_analysis(callback, lang)
        else:
            await callback.answer("Noma'lum kategoriya", show_alert=True)

    @router.message(F.text.in_(["📊 Kunlik statistika", "📊 Дневная статистика"]))
    async def handle_daily_stats_quick(message: Message, state: FSMContext):
        """Quick access to daily statistics"""
        lang = 'uz'  # Default language
        await _show_daily_statistics_detailed(message, lang)

    @router.message(F.text.in_(["📈 Haftalik hisobot", "📈 Недельный отчет"]))
    async def handle_weekly_report_quick(message: Message, state: FSMContext):
        """Quick access to weekly report"""
        lang = 'uz'  # Default language
        await _show_weekly_report_detailed(message, lang)

    @router.message(F.text.in_(["📉 Oylik tahlil", "📉 Месячный анализ"]))
    async def handle_monthly_analysis_quick(message: Message, state: FSMContext):
        """Quick access to monthly analysis"""
        lang = 'uz'  # Default language
        await _show_monthly_analysis_detailed(message, lang)

    @router.message(F.text.in_(["👥 Jamoa samaradorligi", "👥 Производительность команды"]))
    async def handle_team_performance_quick(message: Message, state: FSMContext):
        """Quick access to team performance"""
        lang = 'uz'  # Default language
        await _show_team_performance_detailed(message, lang)

    @router.message(F.text.in_(["🎯 KPI dashboard", "🎯 KPI панель"]))
    async def handle_kpi_dashboard_quick(message: Message, state: FSMContext):
        """Quick access to KPI dashboard"""
        lang = 'uz'  # Default language
        await _show_kpi_dashboard_detailed(message, lang)

    @router.message(F.text.in_(["📤 Ma'lumot eksport", "📤 Экспорт данных"]))
    async def handle_data_export_quick(message: Message, state: FSMContext):
        """Quick access to data export"""
        lang = 'uz'  # Default language
        await _show_data_export_options(message, lang)

    @router.callback_query(F.data.in_(["back", "orqaga", "назад"]))
    async def supervisor_back(call: CallbackQuery, state: FSMContext):
        """Go back to supervisor main menu"""
        await call.answer()
        
        text = "Call Center Supervisor paneliga xush kelibsiz!"
        await call.message.edit_text(text)
        await state.clear()

    return router


async def _show_daily_statistics(callback: CallbackQuery, lang: str):
    """Show daily statistics"""
    today = datetime.now().date()
    
    # Mock today's orders
    today_orders = [
        {'status': 'new', 'created_at': datetime.now()},
        {'status': 'completed', 'created_at': datetime.now()},
        {'status': 'in_progress', 'created_at': datetime.now()},
        {'status': 'completed', 'created_at': datetime.now()},
        {'status': 'issue', 'created_at': datetime.now()}
    ]
    
    # Calculate statistics
    total_today = len(today_orders)
    completed_today = len([o for o in today_orders if o['status'] == 'completed'])
    new_today = len([o for o in today_orders if o['status'] == 'new'])
    in_progress_today = len([o for o in today_orders if o['status'] == 'in_progress'])
    issues_today = len([o for o in today_orders if o['status'] == 'issue'])
    
    completion_rate = (completed_today / total_today * 100) if total_today > 0 else 0
    
    text = (
        f"📊 Bugungi statistika ({today.strftime('%d.%m.%Y')})\n\n"
        f"📋 BUYURTMALAR:\n"
        f"• Jami: {total_today}\n"
        f"• Yangi: {new_today}\n"
        f"• Jarayonda: {in_progress_today}\n"
        f"• Bajarilgan: {completed_today}\n"
        f"• Muammoli: {issues_today}\n\n"
        f"📈 SAMARADORLIK:\n"
        f"• Bajarish foizi: {completion_rate:.1f}%\n"
        f"• O'rtacha vaqt: 2.3 soat\n\n"
        f"⏰ Soatlik taqsimot:\n"
    )
    
    # Add hourly distribution
    for hour in range(9, 19):  # Working hours 9-18
        count = 1 if hour in [10, 14, 16] else 0  # Mock data
        bar = "█" * min(count, 10)  # Visual bar
        text += f"{hour:02d}:00 - {count:2d} {bar}\n"
    
    await callback.message.edit_text(text, reply_markup=get_statistics_menu(lang))
    await callback.answer()


async def _show_weekly_statistics(callback: CallbackQuery, lang: str):
    """Show weekly statistics"""
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    
    # Mock weekly data
    week_orders = [
        {'status': 'completed', 'created_at': datetime.now()},
        {'status': 'completed', 'created_at': datetime.now()},
        {'status': 'in_progress', 'created_at': datetime.now()},
        {'status': 'new', 'created_at': datetime.now()},
        {'status': 'completed', 'created_at': datetime.now()}
    ]
    
    # Calculate daily statistics for the week
    daily_stats = {
        week_start + timedelta(days=i): 1 for i in range(7)
    }
    
    total_week = len(week_orders)
    completed_week = len([o for o in week_orders if o['status'] == 'completed'])
    avg_daily = total_week / 7
    
    text = (
        f"📈 Haftalik hisobot ({week_start.strftime('%d.%m')} - {today.strftime('%d.%m.%Y')})\n\n"
        f"📊 UMUMIY:\n"
        f"• Jami buyurtmalar: {total_week}\n"
        f"• Bajarilgan: {completed_week}\n"
        f"• Kunlik o'rtacha: {avg_daily:.1f}\n\n"
        f"📅 KUNLIK TAQSIMOT:\n"
    )
    
    # Add daily breakdown
    weekdays = ['Душанба', 'Сешанба', 'Чоршанба', 'Пайшанба', 'Жума', 'Шанба', 'Якшанба']
    
    for i, (day, count) in enumerate(daily_stats.items()):
        weekday = weekdays[i]
        bar = "█" * min(count, 15)
        text += f"{weekday} {day.strftime('%d.%m')}: {count:2d} {bar}\n"
    
    await callback.message.edit_text(text, reply_markup=get_statistics_menu(lang))
    await callback.answer()


async def _show_monthly_statistics(callback: CallbackQuery, lang: str):
    """Show monthly statistics"""
    today = datetime.now().date()
    month_start = today.replace(day=1)
    
    # Mock monthly data
    month_orders = [
        {'status': 'completed', 'created_at': datetime.now()},
        {'status': 'in_progress', 'created_at': datetime.now()},
        {'status': 'new', 'created_at': datetime.now()},
        {'status': 'completed', 'created_at': datetime.now()},
        {'status': 'issue', 'created_at': datetime.now()}
    ]
    
    # Calculate statistics by status
    status_stats = {}
    for order in month_orders:
        status = order['status']
        status_stats[status] = status_stats.get(status, 0) + 1
    
    total_month = len(month_orders)
    days_in_month = (today - month_start).days + 1
    avg_daily = total_month / days_in_month if days_in_month > 0 else 0
    
    text = (
        f"📉 Oylik hisobot ({month_start.strftime('%B %Y')})\n\n"
        f"📊 UMUMIY:\n"
        f"• Jami buyurtmalar: {total_month}\n"
        f"• Kunlik o'rtacha: {avg_daily:.1f}\n"
        f"• Faol kunlar: {days_in_month}\n\n"
        f"📋 STATUS BO'YICHA:\n"
    )
    
    # Add status breakdown
    status_names = {
        'new': 'Yangi',
        'in_progress': 'Jarayonda',
        'completed': 'Bajarilgan',
        'cancelled': 'Bekor qilingan',
        'issue': 'Muammoli'
    }
    
    for status, count in status_stats.items():
        status_name = status_names.get(status, status)
        percentage = (count / total_month * 100) if total_month > 0 else 0
        bar = "█" * min(int(percentage / 5), 20)
        text += f"• {status_name}: {count} ({percentage:.1f}%) {bar}\n"
    
    await callback.message.edit_text(text, reply_markup=get_statistics_menu(lang))
    await callback.answer()


async def _show_staff_performance(callback: CallbackQuery, lang: str):
    """Show staff performance statistics"""
    # Mock performance data
    performance = [
        {
            'full_name': 'Aziz Karimov',
            'role': 'call_center',
            'total_orders': 25,
            'completed_orders': 22,
            'cancelled_orders': 1
        },
        {
            'full_name': 'Malika Yusupova',
            'role': 'call_center',
            'total_orders': 20,
            'completed_orders': 18,
            'cancelled_orders': 0
        },
        {
            'full_name': 'Bekzod Toirov',
            'role': 'technician',
            'total_orders': 15,
            'completed_orders': 14,
            'cancelled_orders': 1
        }
    ]
    
    text = (
        f"👥 Xodimlar samaradorligi (30 kun)\n\n"
    )
    
    # Sort by completion rate
    for perf in sorted(performance, key=lambda x: x['completed_orders'], reverse=True):
        completion_rate = 0
        if perf['total_orders'] > 0:
            completion_rate = (perf['completed_orders'] / perf['total_orders']) * 100
        
        role_emoji = "📞" if perf['role'] == 'call_center' else "🔧"
        performance_emoji = "🟢" if completion_rate >= 80 else "🟡" if completion_rate >= 60 else "🔴"
        
        text += (
            f"{performance_emoji} {role_emoji} {perf['full_name']}\n"
            f"   📋 Jami: {perf['total_orders']}\n"
            f"   ✅ Bajarilgan: {perf['completed_orders']}\n"
            f"   ❌ Bekor: {perf['cancelled_orders']}\n"
            f"   📈 Samaradorlik: {completion_rate:.1f}%\n\n"
        )
    
    # Add performance summary
    total_staff = len(performance)
    high_performers = len([p for p in performance if (p['completed_orders'] / max(p['total_orders'], 1)) >= 0.8])
    
    text += (
        f"📊 XULOSA:\n"
        f"• Jami xodimlar: {total_staff}\n"
        f"• Yuqori samarali: {high_performers}\n"
        f"• Samaradorlik: {(high_performers/total_staff*100):.1f}%"
    )
    
    await callback.message.edit_text(text, reply_markup=get_statistics_menu(lang))
    await callback.answer()


async def _show_orders_analysis(callback: CallbackQuery, lang: str):
    """Show orders analysis"""
    # Mock orders data
    orders = [
        {'order_type': 'internet', 'priority': 'high'},
        {'order_type': 'tv', 'priority': 'medium'},
        {'order_type': 'internet', 'priority': 'low'},
        {'order_type': 'technical', 'priority': 'high'},
        {'order_type': 'internet', 'priority': 'medium'}
    ]
    
    # Analyze order types
    type_stats = {}
    priority_stats = {}
    
    for order in orders:
        order_type = order.get('order_type', 'unknown')
        priority = order.get('priority', 'medium')
        
        type_stats[order_type] = type_stats.get(order_type, 0) + 1
        priority_stats[priority] = priority_stats.get(priority, 0) + 1
    
    text = (
        f"📋 Buyurtmalar tahlili\n\n"
        f"📊 TUR BO'YICHA:\n"
    )
    
    # Add type analysis
    for order_type, count in sorted(type_stats.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(orders) * 100)
        bar = "█" * min(int(percentage / 5), 20)
        text += f"• {order_type}: {count} ({percentage:.1f}%) {bar}\n"
    
    text += (
        f"\n🎯 MUHIMLIK BO'YICHA:\n"
    )
    
    # Add priority analysis
    priority_names = {
        'high': 'Yuqori',
        'medium': 'O\'rta',
        'low': 'Past'
    }
    
    for priority, count in sorted(priority_stats.items(), key=lambda x: x[1], reverse=True):
        priority_name = priority_names.get(priority, priority)
        percentage = (count / len(orders) * 100)
        emoji = "🔴" if priority == 'high' else "🟡" if priority == 'medium' else "🟢"
        bar = "█" * min(int(percentage / 5), 20)
        text += f"{emoji} {priority_name}: {count} ({percentage:.1f}%) {bar}\n"
    
    await callback.message.edit_text(text, reply_markup=get_statistics_menu(lang))
    await callback.answer()


async def _show_daily_statistics_detailed(message: Message, lang: str):
    """Show detailed daily statistics"""
    text = (
        f"📊 Batafsil kunlik statistika\n"
        f"📅 {datetime.now().strftime('%d.%m.%Y')}\n\n"
        f"📋 BUYURTMALAR (bugun):\n"
        f"• Yangi: 5\n"
        f"• Jarayonda: 3\n"
        f"• Bajarilgan: 8\n"
        f"• Bekor qilingan: 1\n"
        f"• Muammoli: 1\n\n"
        f"⚡ SAMARADORLIK:\n"
        f"• Jami ishlov berilgan: 18\n"
        f"• O'rtacha vaqt: 2.3 soat\n"
        f"• Yuqori muhimlik: 3\n\n"
        f"📈 ENG FAOL VAQTLAR:\n"
        f"• 10:00 - 3 buyurtma\n"
        f"• 14:00 - 5 buyurtma\n"
        f"• 16:00 - 2 buyurtma\n"
    )
    
    await message.answer(text, reply_markup=get_analytics_dashboard_keyboard(lang))


async def _show_weekly_report_detailed(message: Message, lang: str):
    """Show detailed weekly report"""
    text = (
        f"📈 Batafsil haftalik hisobot\n"
        f"📅 Oxirgi 7 kun\n\n"
        f"👥 JAMOA SAMARADORLIGI:\n"
        f"• Jamoa hajmi: 8\n"
        f"• Jami buyurtmalar: 45\n"
        f"• Bajarilgan: 38\n"
        f"• O'rtacha bajarish vaqti: 2.1h\n"
        f"• Yuqori muhimlik: 12\n\n"
        f"👤 INDIVIDUAL SAMARADORLIK:\n"
        f"🟢 📞 Aziz Karimov (call_center)\n"
        f"   📋 Buyurtmalar: 12\n"
        f"   ✅ Bajarilgan: 11\n"
        f"   ⏱️ O'rtacha vaqt: 1.8h\n\n"
        f"🟡 📞 Malika Yusupova (call_center)\n"
        f"   📋 Buyurtmalar: 10\n"
        f"   ✅ Bajarilgan: 8\n"
        f"   ⏱️ O'rtacha vaqt: 2.3h\n\n"
    )
    
    await message.answer(text, reply_markup=get_performance_dashboard_keyboard(lang))


async def _show_monthly_analysis_detailed(message: Message, lang: str):
    """Show detailed monthly analysis"""
    text = (
        f"📉 Batafsil oylik tahlil\n"
        f"📅 Oxirgi 30 kun\n\n"
        f"📊 ASOSIY KO'RSATKICHLAR:\n"
        f"• Jami ishlov berilgan: 180\n"
        f"• Bajarilgan: 162\n"
        f"• Bekor qilingan: 8\n"
        f"• Muammoli: 10\n"
        f"• Umumiy samaradorlik: 90.0%\n\n"
        f"⏱️ VAQT TAHLILI:\n"
        f"• O'rtacha ishlov berish: 2.1 soat\n"
        f"• Yuqori muhimlik: 25\n\n"
        f"📈 TRENDLAR:\n"
        f"✅ Yuqori samaradorlik darajasi\n"
    )
    
    await message.answer(text, reply_markup=get_analytics_dashboard_keyboard(lang))


async def _show_team_performance_detailed(message: Message, lang: str):
    """Show detailed team performance"""
    text = (
        f"👥 Batafsil jamoa samaradorligi\n\n"
        f"📊 XODIMLAR HOLATI:\n"
        f"🟢 📞 Aziz Karimov\n"
        f"   📋 Joriy ish yuki: 5\n"
        f"   ⚡ Faol buyurtmalar: 3\n"
        f"   🔴 Yuqori muhimlik: 1\n"
        f"   ⏱️ O'rtacha vaqt: 1.8h\n\n"
        f"🟡 📞 Malika Yusupova\n"
        f"   📋 Joriy ish yuki: 8\n"
        f"   ⚡ Faol buyurtmalar: 4\n"
        f"   🔴 Yuqori muhimlik: 2\n"
        f"   ⏱️ O'rtacha vaqt: 2.3h\n\n"
        f"🚨 OGOHLANTIRISHLAR:\n"
        f"• Malika Yusupova yuqori ish yuki\n"
    )
    
    await message.answer(text, reply_markup=get_performance_dashboard_keyboard(lang))


async def _show_kpi_dashboard_detailed(message: Message, lang: str):
    """Show detailed KPI dashboard"""
    text = (
        f"🎯 KPI Dashboard\n"
        f"📅 Oxirgi 7 kun\n\n"
        f"📊 ASOSIY KPI'LAR:\n"
        f"• Bajarish darajasi: 84.4%\n"
        f"• O'rtacha ishlov berish vaqti: 2.1h\n"
        f"• Xodim samaradorligi: 5.6 buyurtma/xodim\n"
        f"• Jamoa hajmi: 8\n\n"
        f"📈 SAMARADORLIK KO'RSATKICHLARI:\n"
        f"• Jami ishlov berilgan: 45\n"
        f"• Bajarilgan: 38\n"
        f"• Muammoli: 3\n"
        f"• Yuqori muhimlik: 12\n\n"
        f"🎯 MAQSADLAR:\n"
        f"✅ Bajarish darajasi: 84.4% (maqsad: 85%)\n"
        f"✅ Ishlov berish vaqti: 2.1h (maqsad: 4h)\n"
        f"❌ Xodim samaradorligi: 5.6 (maqsad: 10)\n"
    )
    
    await message.answer(text, reply_markup=get_analytics_dashboard_keyboard(lang))


async def _show_data_export_options(message: Message, lang: str):
    """Show data export options"""
    text = (
        f"📤 Ma'lumot eksport\n\n"
        f"Quyidagi ma'lumotlarni eksport qilishingiz mumkin:\n\n"
        f"📋 BUYURTMALAR:\n"
        f"• Barcha buyurtmalar (CSV)\n"
        f"• Status bo'yicha filtrlangan\n"
        f"• Sana oralig'i bo'yicha\n\n"
        f"👥 XODIMLAR:\n"
        f"• Xodimlar samaradorligi\n"
        f"• Ish yuki taqsimoti\n"
        f"• KPI hisobotlari\n\n"
        f"📊 STATISTIKALAR:\n"
        f"• Kunlik hisobotlar\n"
        f"• Haftalik tahlillar\n"
        f"• Oylik xulosalar\n\n"
        f"Eksport qilish uchun tegishli tugmani bosing:"
    )
    
    keyboard = get_supervisor_statistics_keyboard(lang)
    
    await message.answer(text, reply_markup=keyboard)

    # Export handlers
    @router.callback_query(F.data.startswith("ccs_export_"))
    async def handle_export_requests(callback: CallbackQuery, state: FSMContext):
        """Handle export requests"""
        await callback.answer()
        
        try:
            from utils.export_utils import create_export_file
            from aiogram.types import BufferedInputFile
            
            export_type = callback.data.replace("ccs_export_", "").split("_")[0]
            format_type = callback.data.split("_")[-1]
            
            # Map export types
            export_mapping = {
                "orders": "orders",
                "staff": "users", 
                "stats": "statistics",
                "kpi": "statistics"
            }
            
            actual_export_type = export_mapping.get(export_type, "statistics")
            
            # Create export file
            file_content, filename = create_export_file(actual_export_type, format_type, "call_center_supervisor")
            
            # Get file size
            file_content.seek(0, 2)  # Move to end
            file_size = file_content.tell()
            file_content.seek(0)  # Reset to beginning
            
            # Send only the file with all information in caption
            await callback.message.answer_document(
                BufferedInputFile(
                    file_content.read(),
                    filename=filename
                ),
                caption=f"✅ {export_type.title()} export muvaffaqiyatli yakunlandi!\n\n"
                        f"📄 Fayl: {filename}\n"
                        f"📦 Hajm: {file_size:,} bayt\n"
                        f"📊 Format: {format_type.upper()}\n"
                        f"📅 Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
            
        except Exception as e:
            await callback.message.answer("❌ Export xatoligi yuz berdi")

    @router.callback_query(F.data == "ccs_close_menu")
    async def close_export_menu(callback: CallbackQuery, state: FSMContext):
        """Close export menu"""
        await callback.answer()
        await callback.message.delete()