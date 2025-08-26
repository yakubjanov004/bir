from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.warehouse_buttons import get_warehouse_main_keyboard, warehouse_statistics_menu, statistics_period_menu
from states.warehouse_states import WarehouseStatisticsStates
from filters.role_filter import RoleFilter

def get_warehouse_statistics_router():
    """Warehouse statistics router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("warehouse")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text == "📊 Statistikalar")
    async def statistics_handler(message: Message, state: FSMContext):
        """Handle statistics and reports"""
        try:
            # Debug logging
            print(f"Warehouse statistics handler called by user {message.from_user.id}")
            
            stats_text = "📊 Statistika va hisobotlar"
            
            await message.answer(
                stats_text,
                reply_markup=warehouse_statistics_menu('uz')
            )
            await state.set_state(WarehouseStatisticsStates.statistics_menu)
            
            print(f"Warehouse statistics handler completed successfully")
            
        except Exception as e:
            print(f"Error in warehouse statistics handler: {str(e)}")
            # await message.answer("Xatolik yuz berdi")
            pass

    @router.callback_query(F.data == "daily_statistics")
    async def daily_statistics_handler(callback: CallbackQuery, state: FSMContext):
        """Show daily statistics"""
        try:
            # Mock daily statistics data (like other modules)
            stats = {
                'items_added': 25,
                'items_issued': 18,
                'total_value': 1500000,
                'low_stock_count': 3,
                'turnover_rate': 85
            }
            
            text = "📊 Bugungi statistika:\n\n"
            text += f"📦 Qo'shilgan mahsulotlar: {stats.get('items_added', 0)}\n"
            text += f"📤 Chiqarilgan mahsulotlar: {stats.get('items_issued', 0)}\n"
            text += f"💰 Umumiy qiymat: {stats.get('total_value', 0):,.0f} so'm\n"
            text += f"⚠️ Kam zaxira: {stats.get('low_stock_count', 0)} ta\n"
            text += f"🔄 Aylanma tezligi: {stats.get('turnover_rate', 0)}%\n"
            
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            # await callback.message.edit_text("Statistikani olishda xatolik")
            # await callback.answer()
            pass

    @router.callback_query(F.data == "weekly_statistics")
    async def weekly_statistics_handler(callback: CallbackQuery, state: FSMContext):
        """Show weekly statistics"""
        try:
            # Mock weekly statistics data (like other modules)
            stats = {
                'items_added': 150,
                'items_issued': 120,
                'total_value': 8500000,
                'low_stock_count': 8,
                'turnover_rate': 78
            }
            
            text = "📊 Haftalik statistika:\n\n"
            text += f"📦 Qo'shilgan mahsulotlar: {stats.get('items_added', 0)}\n"
            text += f"📤 Chiqarilgan mahsulotlar: {stats.get('items_issued', 0)}\n"
            text += f"💰 Umumiy qiymat: {stats.get('total_value', 0):,.0f} so'm\n"
            text += f"⚠️ Kam zaxira: {stats.get('low_stock_count', 0)} ta\n"
            text += f"🔄 Aylanma tezligi: {stats.get('turnover_rate', 0)}%\n"
            
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            # await callback.message.edit_text("Statistikani olishda xatolik")
            # await callback.answer()
            pass

    @router.callback_query(F.data == "monthly_statistics")
    async def monthly_statistics_handler(callback: CallbackQuery, state: FSMContext):
        """Show monthly statistics"""
        try:
            # Mock monthly statistics data (like other modules)
            stats = {
                'items_added': 650,
                'items_issued': 580,
                'total_value': 35000000,
                'low_stock_count': 15,
                'turnover_rate': 82
            }
            
            text = "📊 Oylik statistika:\n\n"
            text += f"📦 Qo'shilgan mahsulotlar: {stats.get('items_added', 0)}\n"
            text += f"📤 Chiqarilgan mahsulotlar: {stats.get('items_issued', 0)}\n"
            text += f"💰 Umumiy qiymat: {stats.get('total_value', 0):,.0f} so'm\n"
            text += f"⚠️ Kam zaxira: {stats.get('low_stock_count', 0)} ta\n"
            text += f"🔄 Aylanma tezligi: {stats.get('turnover_rate', 0)}%\n"
            
            await callback.message.edit_text(text)
            await callback.answer()
            
        except Exception as e:
            # await callback.message.edit_text("Statistikani olishda xatolik")
            # await callback.answer()
            pass

    @router.callback_query(F.data == "turnover_statistics")
    async def turnover_statistics_handler(callback: CallbackQuery, state: FSMContext):
        """Show inventory turnover statistics"""
        try:
            # Mock turnover statistics data (like other modules)
            stats = {
                'turnover_rate': 75,
                'top_turnover_items': [
                    {'name': 'Cable', 'current_stock': 50, 'issued_quantity': 45, 'turnover_rate': 90},
                    {'name': 'Connector', 'current_stock': 100, 'issued_quantity': 85, 'turnover_rate': 85},
                    {'name': 'Router', 'current_stock': 10, 'issued_quantity': 8, 'turnover_rate': 80}
                ]
            }
            
            text = "🔄 Aylanma statistikasi:\n\n"
            text += f"📊 O'rtacha aylanma: {stats.get('turnover_rate', 0)}%\n\n"
            text += f"🔝 Eng ko'p aylangan mahsulotlar:\n"
            
            for i, item in enumerate(stats['top_turnover_items'][:5], 1):
                text += f"{i}. **{item['name']}**\n"
                text += f"   📦 Zaxira: {item['current_stock']}\n"
                text += f"   📤 Chiqarilgan: {item['issued_quantity']}\n"
                text += f"   🔄 Aylanma: {item['turnover_rate']}%\n\n"
            
            await callback.message.edit_text(text, parse_mode="Markdown")
            await callback.answer()
            
        except Exception as e:
            # await callback.message.edit_text("Statistikani olishda xatolik")
            # await callback.answer()
            pass

    @router.callback_query(F.data == "performance_report")
    async def performance_report_handler(callback: CallbackQuery, state: FSMContext):
        """Show performance report"""
        try:
            # Mock performance data (like other modules)
            daily_stats = {'items_added': 25, 'items_issued': 18, 'turnover_rate': 85}
            weekly_stats = {'items_added': 150, 'items_issued': 120, 'turnover_rate': 78}
            monthly_stats = {'items_added': 650, 'items_issued': 580, 'turnover_rate': 82, 'total_value': 35000000, 'low_stock_count': 15}
            
            text = "📈 Samaradorlik hisoboti:\n\n"
            
            # Daily performance
            text += f"📅 **Bugun:**\n"
            text += f"   📦 Qo'shilgan: {daily_stats.get('items_added', 0)}\n"
            text += f"   📤 Chiqarilgan: {daily_stats.get('items_issued', 0)}\n"
            text += f"   🔄 Aylanma: {daily_stats.get('turnover_rate', 0)}%\n\n"
            
            # Weekly performance
            text += f"📅 **Bu hafta:**\n"
            text += f"   📦 Qo'shilgan: {weekly_stats.get('items_added', 0)}\n"
            text += f"   📤 Chiqarilgan: {weekly_stats.get('items_issued', 0)}\n"
            text += f"   🔄 Aylanma: {weekly_stats.get('turnover_rate', 0)}%\n\n"
            
            # Monthly performance
            text += f"📅 **Bu oy:**\n"
            text += f"   📦 Qo'shilgan: {monthly_stats.get('items_added', 0)}\n"
            text += f"   📤 Chiqarilgan: {monthly_stats.get('items_issued', 0)}\n"
            text += f"   🔄 Aylanma: {monthly_stats.get('turnover_rate', 0)}%\n\n"
            
            # Overall status
            total_value = monthly_stats.get('total_value', 0)
            low_stock = monthly_stats.get('low_stock_count', 0)
            
            text += f"💰 **Umumiy qiymat:** {total_value:,.0f} so'm\n"
            text += f"⚠️ **Kam zaxira:** {low_stock} ta mahsulot\n"
            
            await callback.message.edit_text(text, parse_mode="Markdown")
            await callback.answer()
            
        except Exception as e:
            # await callback.message.edit_text("Hisobotni olishda xatolik")
            # await callback.answer()
            pass

    @router.message(F.text == "📦 Inventarizatsiya statistikasi")
    async def inventory_stats_reply_handler(message: Message, state: FSMContext):
        """Show inventory statistics"""
        try:
            # Mock inventory data (like other modules)
            stats = {
                'items_added': 25,
                'items_issued': 18,
                'total_value': 1500000,
                'low_stock_count': 3,
                'turnover_rate': 85
            }
            
            text = "📦 Inventarizatsiya statistikasi (bugun):\n\n"
            text += f"📦 Qo'shilgan mahsulotlar: {stats.get('items_added', 0)}\n"
            text += f"📤 Chiqarilgan mahsulotlar: {stats.get('items_issued', 0)}\n"
            text += f"💰 Umumiy qiymat: {stats.get('total_value', 0):,.0f} so'm\n"
            text += f"⚠️ Kam zaxira: {stats.get('low_stock_count', 0)} ta\n"
            text += f"🔄 Aylanma tezligi: {stats.get('turnover_rate', 0)}%\n"
            
            await message.answer(text, reply_markup=warehouse_statistics_menu('uz'))
            await state.set_state(WarehouseStatisticsStates.statistics_menu)
            
        except Exception as e:
            # await message.answer("Statistikani olishda xatolik")
            pass

    @router.message(F.text == "📋 Buyurtmalar statistikasi")
    async def orders_stats_reply_handler(message: Message, state: FSMContext):
        """Show orders statistics"""
        try:
            # Mock orders data (like other modules)
            stats = {
                'items_added': 150,
                'items_issued': 120,
                'total_value': 8500000,
                'low_stock_count': 8,
                'turnover_rate': 78
            }
            
            text = "📋 Buyurtmalar statistikasi (hafta):\n\n"
            text += f"📦 Qo'shilgan mahsulotlar: {stats.get('items_added', 0)}\n"
            text += f"📤 Chiqarilgan mahsulotlar: {stats.get('items_issued', 0)}\n"
            text += f"💰 Umumiy qiymat: {stats.get('total_value', 0):,.0f} so'm\n"
            text += f"⚠️ Kam zaxira: {stats.get('low_stock_count', 0)} ta\n"
            text += f"🔄 Aylanma tezligi: {stats.get('turnover_rate', 0)}%\n"
            
            await message.answer(text, reply_markup=warehouse_statistics_menu('uz'))
            await state.set_state(WarehouseStatisticsStates.statistics_menu)
            
        except Exception as e:
            # await message.answer("Statistikani olishda xatolik")
            pass

    @router.message(F.text == "⚠️ Kam zaxira statistikasi")
    async def low_stock_stats_reply_handler(message: Message, state: FSMContext):
        """Show low stock statistics"""
        try:
            # Mock low stock data (like other modules)
            items = [
                {'name': 'Cable', 'quantity': 5, 'min_quantity': 10},
                {'name': 'Connector', 'quantity': 8, 'min_quantity': 15},
                {'name': 'Router', 'quantity': 2, 'min_quantity': 5}
            ]
            
            if items:
                text = "⚠️ Kam zaxira statistikasi:\n\n"
                for i, item in enumerate(items, 1):
                    text += f"{i}. {item['name']} — {item['quantity']} dona (min: {item['min_quantity']})\n"
            else:
                text = "📦 Barcha mahsulotlar zaxirasi yetarli"
            
            await message.answer(text, reply_markup=warehouse_statistics_menu('uz'))
            await state.set_state(WarehouseStatisticsStates.statistics_menu)
            
        except Exception as e:
            # await message.answer("Statistikani olishda xatolik")
            pass

    @router.message(F.text == "💰 Moliyaviy hisobot")
    async def financial_stats_reply_handler(message: Message, state: FSMContext):
        """Show financial report"""
        try:
            # Mock financial data (like other modules)
            stats = {
                'items_added': 650,
                'items_issued': 580,
                'total_value': 35000000
            }
            
            text = "💰 Moliyaviy hisobot (oy):\n\n"
            text += f"📦 Omborga kiritilgan mahsulotlar: {stats.get('items_added', 0)} dona\n"
            text += f"📤 Ombordan chiqarilgan mahsulotlar: {stats.get('items_issued', 0)} dona\n"
            text += f"💰 Umumiy qiymat: {stats.get('total_value', 0):,.0f} so'm\n"
            
            await message.answer(text, reply_markup=warehouse_statistics_menu('uz'))
            await state.set_state(WarehouseStatisticsStates.statistics_menu)
            
        except Exception as e:
            # await message.answer("Statistikani olishda xatolik")
            pass

    @router.message(F.text == "📆 Vaqt oralig'idagi statistika")
    async def period_stats_reply_handler(message: Message, state: FSMContext):
        """Show period statistics menu"""
        try:
            await message.answer(
                "Qaysi davr uchun statistikani ko'rmoqchisiz?",
                reply_markup=statistics_period_menu('uz')
            )
            await state.set_state(WarehouseStatisticsStates.period_menu)
            
        except Exception as e:
            # await message.answer("Xatolik yuz berdi")
            pass

    @router.message(F.text == "📈 Oylik statistika")
    async def monthly_stats_reply_handler(message: Message, state: FSMContext):
        """Show monthly statistics"""
        try:
            # Mock monthly data (like other modules)
            stats = {
                'items_added': 650,
                'items_issued': 580,
                'total_value': 35000000,
                'low_stock_count': 15,
                'turnover_rate': 82
            }
            
            text = "📈 Oylik statistika:\n\n"
            text += f"📦 Qo'shilgan mahsulotlar: {stats.get('items_added', 0)}\n"
            text += f"📤 Chiqarilgan mahsulotlar: {stats.get('items_issued', 0)}\n"
            text += f"💰 Umumiy qiymat: {stats.get('total_value', 0):,.0f} so'm\n"
            text += f"⚠️ Kam zaxira: {stats.get('low_stock_count', 0)} ta\n"
            text += f"🔄 Aylanma tezligi: {stats.get('turnover_rate', 0)}%\n"
            
            await message.answer(text)
            
        except Exception as e:
            # await message.answer("Statistikani olishda xatolik")
            pass

    @router.message(F.text == "📅 Kunlik statistika")
    async def daily_stats_reply_handler(message: Message, state: FSMContext):
        """Show daily statistics"""
        try:
            # Mock daily data (like other modules)
            stats = {
                'items_added': 25,
                'items_issued': 18,
                'total_value': 1500000,
                'low_stock_count': 3,
                'turnover_rate': 85
            }
            
            text = "📅 Kunlik statistika:\n\n"
            text += f"📦 Qo'shilgan mahsulotlar: {stats.get('items_added', 0)}\n"
            text += f"📤 Chiqarilgan mahsulotlar: {stats.get('items_issued', 0)}\n"
            text += f"💰 Umumiy qiymat: {stats.get('total_value', 0):,.0f} so'm\n"
            text += f"⚠️ Kam zaxira: {stats.get('low_stock_count', 0)} ta\n"
            text += f"🔄 Aylanma tezligi: {stats.get('turnover_rate', 0)}%\n"
            
            await message.answer(text)
            
        except Exception as e:
            # await message.answer("Statistikani olishda xatolik")
            pass

    @router.message(F.text == "📊 Haftalik statistika")
    async def weekly_stats_reply_handler(message: Message, state: FSMContext):
        """Show weekly statistics"""
        try:
            # Mock weekly data (like other modules)
            stats = {
                'items_added': 150,
                'items_issued': 120,
                'total_value': 8500000,
                'low_stock_count': 8,
                'turnover_rate': 78
            }
            
            text = "📊 Haftalik statistika:\n\n"
            text += f"📦 Qo'shilgan mahsulotlar: {stats.get('items_added', 0)}\n"
            text += f"📤 Chiqarilgan mahsulotlar: {stats.get('items_issued', 0)}\n"
            text += f"💰 Umumiy qiymat: {stats.get('total_value', 0):,.0f} so'm\n"
            text += f"⚠️ Kam zaxira: {stats.get('low_stock_count', 0)} ta\n"
            text += f"🔄 Aylanma tezligi: {stats.get('turnover_rate', 0)}%\n"
            
            await message.answer(text)
            
        except Exception as e:
            # await message.answer("Statistikani olishda xatolik")
            pass

    @router.message(F.text == "🗓 Yillik statistika")
    async def yearly_stats_reply_handler(message: Message, state: FSMContext):
        """Show yearly statistics"""
        try:
            text = "🗓 Yillik statistika: tez orada to'liq statistikalar qo'shiladi."
            await message.answer(text)
            
        except Exception as e:
            #          await message.answer("Statistikani olishda xatolik")
            pass

    @router.callback_query(F.data == "back")
    async def statistics_back_reply_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back navigation"""
        try:
            current_state = await state.get_state()

            if current_state == WarehouseStatisticsStates.viewing_stats:
                # Go back to period menu
                await callback.message.edit_text(
                    "Qaysi davr uchun statistikani ko'rmoqchisiz?",
                    reply_markup=statistics_period_menu('uz')
                )
                await state.set_state(WarehouseStatisticsStates.period_menu)

            elif current_state == WarehouseStatisticsStates.period_menu:
                # Go back to statistics menu
                await callback.message.edit_text(
                    "Statistikalar menyusi",
                    reply_markup=warehouse_statistics_menu('uz')
                )
                await state.set_state(WarehouseStatisticsStates.statistics_menu)

            elif current_state == WarehouseStatisticsStates.statistics_menu:
                # Go back to main menu
                await callback.message.edit_text(
                    "Ombor bosh menyusi",
                    reply_markup=get_warehouse_main_keyboard('uz')
                )
                await state.set_state(WarehouseStatisticsStates.main_menu)

        except Exception as e:
            # await callback.answer("Xatolik yuz berdi")
            pass

    return router

# Mock functions (like other modules)
async def get_warehouse_daily_statistics():
    """Get daily warehouse statistics (mock function like other modules)"""
    try:
        return {
            'items_added': 25,
            'items_issued': 18,
            'total_value': 1500000,
            'low_stock_count': 3,
            'turnover_rate': 85
        }
    except Exception as e:
        return None

async def get_warehouse_weekly_statistics():
    """Get weekly warehouse statistics (mock function like other modules)"""
    try:
        return {
            'items_added': 150,
            'items_issued': 120,
            'total_value': 8500000,
            'low_stock_count': 8,
            'turnover_rate': 78
        }
    except Exception as e:
        return None

async def get_warehouse_monthly_statistics():
    """Get monthly warehouse statistics (mock function like other modules)"""
    try:
        return {
            'items_added': 650,
            'items_issued': 580,
            'total_value': 35000000,
            'low_stock_count': 15,
            'turnover_rate': 82
        }
    except Exception as e:
        return None

async def get_inventory_turnover_statistics():
    """Get inventory turnover statistics (mock function like other modules)"""
    try:
        return {
            'turnover_rate': 75,
            'top_turnover_items': [
                {'name': 'Cable', 'current_stock': 50, 'issued_quantity': 45, 'turnover_rate': 90},
                {'name': 'Connector', 'current_stock': 100, 'issued_quantity': 85, 'turnover_rate': 85},
                {'name': 'Router', 'current_stock': 10, 'issued_quantity': 8, 'turnover_rate': 80}
            ]
        }
    except Exception as e:
        return None

async def get_low_stock_inventory_items():
    """Get low stock inventory items (mock function like other modules)"""
    try:
        return [
            {'name': 'Cable', 'quantity': 5, 'min_quantity': 10},
            {'name': 'Connector', 'quantity': 8, 'min_quantity': 15},
            {'name': 'Router', 'quantity': 2, 'min_quantity': 5}
        ]
    except Exception as e:
        return []
