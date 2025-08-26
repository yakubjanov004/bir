"""
Admin Statistics Handler
Manages admin statistics and analytics
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
from keyboards.admin_buttons import get_statistics_keyboard

# States imports
from states.admin_states import AdminStatisticsStates, AdminMainMenuStates
from filters.role_filter import RoleFilter

def get_admin_statistics_router():
    """Get admin statistics router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("admin")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(StateFilter(AdminMainMenuStates.main_menu), F.text.in_(["📊 Statistika", "📊 Статистика"]))
    async def statistics_menu(message: Message, state: FSMContext):
        """Statistics main menu"""
        text = "📊 <b>Statistika bo'limi</b>\n\nTizim statistikalarini ko'rish uchun turini tanlang."
        
        sent_message = await message.answer(
            text,
            reply_markup=get_statistics_keyboard('uz')
        )
        await state.set_state(AdminStatisticsStates.statistics)

    @router.message(F.text.in_(["📈 Umumiy statistika", "📈 Общая статистика"]))
    async def general_statistics(message: Message):
        """Show general statistics"""
        # Mock general statistics
        stats = {
            'total_users': 1250,
            'active_users': 890,
            'total_orders': 3456,
            'completed_orders': 2890,
            'pending_orders': 566,
            'total_technicians': 45,
            'active_technicians': 38,
            'avg_response_time': '2.5 soat',
            'satisfaction_rate': '94.2%'
        }
        
        text = (
            f"📈 <b>Umumiy statistika</b>\n\n"
            f"👥 <b>Foydalanuvchilar:</b>\n"
            f"• Jami: {stats['total_users']:,}\n"
            f"• Faol: {stats['active_users']:,}\n"
            f"• Faollik: {stats['active_users']/stats['total_users']*100:.1f}%\n\n"
            f"📋 <b>Zayavkalar:</b>\n"
            f"• Jami: {stats['total_orders']:,}\n"
            f"• Bajarilgan: {stats['completed_orders']:,}\n"
            f"• Kutilmoqda: {stats['pending_orders']:,}\n"
            f"• Bajarilish: {stats['completed_orders']/stats['total_orders']*100:.1f}%\n\n"
            f"🔧 <b>Texniklar:</b>\n"
            f"• Jami: {stats['total_technicians']}\n"
            f"• Faol: {stats['active_technicians']}\n"
            f"• Faollik: {stats['active_technicians']/stats['total_technicians']*100:.1f}%\n\n"
            f"⏱ <b>Xizmat ko'rsatish:</b>\n"
            f"• O'rtacha javob vaqti: {stats['avg_response_time']}\n"
            f"• Mijoz mamnuniyati: {stats['satisfaction_rate']}\n\n"
            f"📅 Yangilangan: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Yangilash",
                    callback_data="refresh_general_stats"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Batafsil hisobot",
                    callback_data="detailed_report"
                )
            ]
        ])
        
        await message.answer(text, reply_markup=keyboard)
            
    @router.message(F.text.in_(["📊 Zayavkalar statistikasi", "📊 Статистика заявок"]))
    async def orders_statistics(message: Message):
        """Show orders statistics"""
        # Mock orders statistics
        orders_stats = {
            'today': {'created': 45, 'completed': 38, 'pending': 7},
            'week': {'created': 312, 'completed': 289, 'pending': 23},
            'month': {'created': 1245, 'completed': 1189, 'pending': 56},
            'by_status': {
                'Yangi': 23,
                'Jarayonda': 34,
                'Bajarilmoqda': 12,
                'Bajarildi': 2890,
                'Bekor qilindi': 45
            },
            'by_type': {
                'Internet': 1567,
                'Telefon': 890,
                'TV': 678,
                'Boshqa': 321
            }
        }
        
        text = (
            f"📊 <b>Zayavkalar statistikasi</b>\n\n"
            f"📅 <b>Bugun:</b>\n"
            f"• Yaratilgan: {orders_stats['today']['created']}\n"
            f"• Bajarilgan: {orders_stats['today']['completed']}\n"
            f"• Kutilmoqda: {orders_stats['today']['pending']}\n\n"
            f"📅 <b>Bu hafta:</b>\n"
            f"• Yaratilgan: {orders_stats['week']['created']}\n"
            f"• Bajarilgan: {orders_stats['week']['completed']}\n"
            f"• Kutilmoqda: {orders_stats['week']['pending']}\n\n"
            f"📅 <b>Bu oy:</b>\n"
            f"• Yaratilgan: {orders_stats['month']['created']}\n"
            f"• Bajarilgan: {orders_stats['month']['completed']}\n"
            f"• Kutilmoqda: {orders_stats['month']['pending']}\n\n"
            f"📋 <b>Holat bo'yicha:</b>\n"
        )
        
        for status, count in orders_stats['by_status'].items():
            text += f"• {status}: {count}\n"
        
        text += f"\n📋 <b>Turi bo'yicha:</b>\n"
        for order_type, count in orders_stats['by_type'].items():
            text += f"• {order_type}: {count}\n"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📈 Grafik ko'rinish",
                    callback_data="orders_chart"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Excel hisobot",
                    callback_data="export_orders_stats"
                )
            ]
        ])
        
        await message.answer(text, reply_markup=keyboard)

    @router.message(F.text.in_(["👥 Foydalanuvchilar statistikasi", "👥 Статистика пользователей"]))
    async def users_statistics(message: Message):
        """Show users statistics"""
        # Mock users statistics
        users_stats = {
            'total': 1250,
            'active_today': 234,
            'active_week': 567,
            'active_month': 890,
            'by_role': {
                'client': 980,
                'technician': 45,
                'manager': 23,
                'admin': 5,
                'call_center': 12,
                'controller': 8,
                'warehouse': 15,
                'junior_manager': 18
            },
            'by_region': {
                'Toshkent': 456,
                'Samarqand': 234,
                'Buxoro': 189,
                'Farg\'ona': 167,
                'Andijon': 145,
                'Boshqa': 59
            },
            'new_users': {
                'today': 12,
                'week': 67,
                'month': 234
            }
        }
        
        text = (
            f"👥 <b>Foydalanuvchilar statistikasi</b>\n\n"
            f"📊 <b>Umumiy:</b>\n"
            f"• Jami foydalanuvchilar: {users_stats['total']:,}\n"
            f"• Bugun faol: {users_stats['active_today']}\n"
            f"• Bu hafta faol: {users_stats['active_week']}\n"
            f"• Bu oy faol: {users_stats['active_month']}\n\n"
            f"👤 <b>Rol bo'yicha:</b>\n"
        )
        
        role_names = {
            'client': 'Mijozlar',
            'technician': 'Texniklar',
            'manager': 'Menejerlar',
            'admin': 'Adminlar',
            'call_center': 'Call Center',
            'controller': 'Kontrollerlar',
            'warehouse': 'Ombor',
            'junior_manager': 'Junior Menejerlar'
        }
        
        for role, count in users_stats['by_role'].items():
            role_name = role_names.get(role, role)
            text += f"• {role_name}: {count}\n"
        
        text += f"\n🌍 <b>Hudud bo'yicha:</b>\n"
        for region, count in users_stats['by_region'].items():
            text += f"• {region}: {count}\n"
        
        text += f"\n🆕 <b>Yangi foydalanuvchilar:</b>\n"
        text += f"• Bugun: {users_stats['new_users']['today']}\n"
        text += f"• Bu hafta: {users_stats['new_users']['week']}\n"
        text += f"• Bu oy: {users_stats['new_users']['month']}\n"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📈 Faollik grafigi",
                    callback_data="users_activity_chart"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Foydalanuvchilar ro'yxati",
                    callback_data="users_list"
                )
            ]
        ])
        
        await message.answer(text, reply_markup=keyboard)

    @router.message(F.text.in_(["🔧 Texniklar statistikasi", "🔧 Статистика техников"]))
    async def technicians_statistics(message: Message):
        """Show technicians statistics"""
        # Mock technicians statistics
        tech_stats = {
            'total': 45,
            'active': 38,
            'busy': 12,
            'available': 26,
            'performance': {
                'orders_completed_today': 89,
                'avg_completion_time': '3.2 soat',
                'satisfaction_rate': '96.8%',
                'response_time': '1.8 soat'
            },
            'by_region': {
                'Toshkent': 18,
                'Samarqand': 8,
                'Buxoro': 6,
                'Farg\'ona': 5,
                'Andijon': 4,
                'Boshqa': 4
            },
            'top_performers': [
                {'name': 'Aziz Karimov', 'orders': 156, 'rating': 4.9},
                {'name': 'Bekzod Toirov', 'orders': 142, 'rating': 4.8},
                {'name': 'Dilshod Rahimov', 'orders': 134, 'rating': 4.7}
            ]
        }
        
        text = (
            f"🔧 <b>Texniklar statistikasi</b>\n\n"
            f"👥 <b>Umumiy:</b>\n"
            f"• Jami texniklar: {tech_stats['total']}\n"
            f"• Faol: {tech_stats['active']}\n"
            f"• Band: {tech_stats['busy']}\n"
            f"• Bo'sh: {tech_stats['available']}\n\n"
            f"📊 <b>Bugungi faollik:</b>\n"
            f"• Bajarilgan zayavkalar: {tech_stats['performance']['orders_completed_today']}\n"
            f"• O'rtacha bajarish vaqti: {tech_stats['performance']['avg_completion_time']}\n"
            f"• Mijoz mamnuniyati: {tech_stats['performance']['satisfaction_rate']}\n"
            f"• O'rtacha javob vaqti: {tech_stats['performance']['response_time']}\n\n"
            f"🌍 <b>Hudud bo'yicha:</b>\n"
        )
        
        for region, count in tech_stats['by_region'].items():
            text += f"• {region}: {count} texnik\n"
        
        text += f"\n🏆 <b>Eng yaxshi texniklar:</b>\n"
        for i, tech in enumerate(tech_stats['top_performers'], 1):
            text += f"{i}. {tech['name']}: {tech['orders']} zayavka, ⭐ {tech['rating']}\n"
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📈 Faollik grafigi",
                    callback_data="technicians_activity_chart"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏆 Reyting jadvali",
                    callback_data="technicians_rating"
                )
            ]
        ])
        
        await message.answer(text, reply_markup=keyboard)
            
    @router.message(F.text.in_(["📈 KPI ko'rsatkichlari", "📈 KPI показатели"]))
    async def kpi_statistics(message: Message):
        """Show KPI statistics"""
        # Mock KPI statistics
        kpi_stats = {
            'response_time': {
                'target': '2 soat',
                'current': '1.8 soat',
                'achievement': '110%'
            },
            'completion_rate': {
                'target': '95%',
                'current': '96.2%',
                'achievement': '101%'
            },
            'satisfaction_rate': {
                'target': '90%',
                'current': '94.2%',
                'achievement': '105%'
            },
            'efficiency': {
                'target': '85%',
                'current': '88.5%',
                'achievement': '104%'
            },
            'cost_per_order': {
                'target': '50,000 so\'m',
                'current': '47,200 so\'m',
                'achievement': '106%'
            }
        }
        
        text = (
            f"📈 <b>KPI ko'rsatkichlari</b>\n\n"
            f"⏱ <b>Javob vaqti:</b>\n"
            f"• Maqsad: {kpi_stats['response_time']['target']}\n"
            f"• Joriy: {kpi_stats['response_time']['current']}\n"
            f"• Erishish: {kpi_stats['response_time']['achievement']}\n\n"
            f"✅ <b>Bajarilish darajasi:</b>\n"
            f"• Maqsad: {kpi_stats['completion_rate']['target']}\n"
            f"• Joriy: {kpi_stats['completion_rate']['current']}\n"
            f"• Erishish: {kpi_stats['completion_rate']['achievement']}\n\n"
            f"😊 <b>Mijoz mamnuniyati:</b>\n"
            f"• Maqsad: {kpi_stats['satisfaction_rate']['target']}\n"
            f"• Joriy: {kpi_stats['satisfaction_rate']['current']}\n"
            f"• Erishish: {kpi_stats['satisfaction_rate']['achievement']}\n\n"
            f"⚡ <b>Samaradorlik:</b>\n"
            f"• Maqsad: {kpi_stats['efficiency']['target']}\n"
            f"• Joriy: {kpi_stats['efficiency']['current']}\n"
            f"• Erishish: {kpi_stats['efficiency']['achievement']}\n\n"
            f"💰 <b>Zayavka narxi:</b>\n"
            f"• Maqsad: {kpi_stats['cost_per_order']['target']}\n"
            f"• Joriy: {kpi_stats['cost_per_order']['current']}\n"
            f"• Erishish: {kpi_stats['cost_per_order']['achievement']}\n\n"
            f"📊 <b>Umumiy natija:</b>\n"
            f"Barcha KPI ko'rsatkichlari maqsadlardan yuqori!"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📈 KPI grafigi",
                    callback_data="kpi_chart"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 KPI hisobot",
                    callback_data="kpi_report"
                )
            ]
        ])
        
        await message.answer(text, reply_markup=keyboard)

    @router.callback_query(F.data == "refresh_general_stats")
    async def refresh_general_stats(call: CallbackQuery):
        """Refresh general statistics"""
        await call.answer()
        
        # Mock updated statistics
        stats = {
            'total_users': 1253,
            'active_users': 895,
            'total_orders': 3467,
            'completed_orders': 2901,
            'pending_orders': 566,
            'total_technicians': 45,
            'active_technicians': 39,
            'avg_response_time': '2.3 soat',
            'satisfaction_rate': '94.5%'
        }
        
        text = (
            f"📈 <b>Yangilangan umumiy statistika</b>\n\n"
            f"👥 <b>Foydalanuvchilar:</b>\n"
            f"• Jami: {stats['total_users']:,}\n"
            f"• Faol: {stats['active_users']:,}\n"
            f"• Faollik: {stats['active_users']/stats['total_users']*100:.1f}%\n\n"
            f"📋 <b>Zayavkalar:</b>\n"
            f"• Jami: {stats['total_orders']:,}\n"
            f"• Bajarilgan: {stats['completed_orders']:,}\n"
            f"• Kutilmoqda: {stats['pending_orders']:,}\n"
            f"• Bajarilish: {stats['completed_orders']/stats['total_orders']*100:.1f}%\n\n"
            f"🔧 <b>Texniklar:</b>\n"
            f"• Jami: {stats['total_technicians']}\n"
            f"• Faol: {stats['active_technicians']}\n"
            f"• Faollik: {stats['active_technicians']/stats['total_technicians']*100:.1f}%\n\n"
            f"⏱ <b>Xizmat ko'rsatish:</b>\n"
            f"• O'rtacha javob vaqti: {stats['avg_response_time']}\n"
            f"• Mijoz mamnuniyati: {stats['satisfaction_rate']}\n\n"
            f"📅 Yangilangan: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Yangilash",
                    callback_data="refresh_general_stats"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Batafsil hisobot",
                    callback_data="detailed_report"
                )
            ]
        ])
        
        await call.message.edit_text(text, reply_markup=keyboard)
        await call.answer("Statistika yangilandi!")

    @router.callback_query(F.data == "detailed_report")
    async def detailed_report(call: CallbackQuery):
        """Show detailed report"""
        await call.answer()
        
        text = (
            f"📊 <b>Batafsil hisobot</b>\n\n"
            f"📈 <b>O'sish dinamikasi (oylik):</b>\n"
            f"• Foydalanuvchilar: +12.5%\n"
            f"• Zayavkalar: +8.3%\n"
            f"• Bajarilish: +2.1%\n\n"
            f"📊 <b>Eng ko'p so'raladigan xizmatlar:</b>\n"
            f"1. Internet ulanish - 45%\n"
            f"2. Internet tezligi - 23%\n"
            f"3. TV xizmati - 18%\n"
            f"4. Telefon xizmati - 14%\n\n"
            f"🌍 <b>Hududlar bo'yicha:</b>\n"
            f"• Toshkent: 35% zayavkalar\n"
            f"• Samarqand: 22% zayavkalar\n"
            f"• Buxoro: 18% zayavkalar\n"
            f"• Farg'ona: 15% zayavkalar\n"
            f"• Boshqa: 10% zayavkalar\n\n"
            f"⏰ <b>Eng faol vaqtlar:</b>\n"
            f"• 09:00-11:00: 25%\n"
            f"• 14:00-16:00: 30%\n"
            f"• 18:00-20:00: 35%\n"
            f"• Boshqa vaqtlar: 10%"
        )
        
        await call.message.edit_text(text)

    @router.callback_query(F.data == "orders_chart")
    async def orders_chart(call: CallbackQuery):
        """Show orders chart"""
        await call.answer()
        
        text = (
            f"📈 <b>Zayavkalar grafigi</b>\n\n"
            f"📊 <b>Haftalik dinamika:</b>\n"
            f"Dushanba: ████████ 45 zayavka\n"
            f"Seshanba: ██████████ 52 zayavka\n"
            f"Chorshanba: ████████████ 67 zayavka\n"
            f"Payshanba: ██████████████ 78 zayavka\n"
            f"Juma: ████████████████ 89 zayavka\n"
            f"Shanba: ██████████████████ 95 zayavka\n"
            f"Yakshanba: ████████████████████ 112 zayavka\n\n"
            f"📈 <b>O'sish tendentsiyasi:</b>\n"
            f"• O'tgan haftaga nisbatan: +15.3%\n"
            f"• O'tgan oyga nisbatan: +8.7%\n"
            f"• O'tgan yilga nisbatan: +23.1%"
        )
        
        await call.message.edit_text(text)

    @router.callback_query(F.data == "export_orders_stats")
    async def export_orders_stats(call: CallbackQuery):
        """Export orders statistics"""
        await call.answer()
        
        try:
            from utils.export_utils import create_export_file
            from aiogram.types import BufferedInputFile
            
            processing_text = "Zayavkalar statistikasi eksport qilinmoqda..."
            await call.message.edit_text(processing_text)
            
            # Create export file
            file_content, filename = create_export_file("statistics", "xlsx", "admin")
            
            # Get file size
            file_content.seek(0, 2)  # Move to end
            file_size = file_content.tell()
            file_content.seek(0)  # Reset to beginning
            
            # Delete processing message
            await call.message.delete()
            
            # Send only the file with all information in caption
            await call.message.answer_document(
                BufferedInputFile(
                    file_content.read(),
                    filename=filename
                ),
                caption=f"✅ Statistika export muvaffaqiyatli yakunlandi!\n\n"
                        f"📄 Fayl: {filename}\n"
                        f"📦 Hajm: {file_size:,} bayt\n"
                        f"📊 Format: XLSX\n"
                        f"📅 Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
            
        except Exception as e:
            await call.message.answer("❌ Export xatoligi yuz berdi")

    return router
