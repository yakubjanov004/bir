from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards.warehouse_buttons import (
    get_warehouse_main_keyboard,
    get_warehouse_back_to_main_keyboard
)
from states.warehouse_states import WarehouseMainMenuStates
from filters.role_filter import RoleFilter

def get_get_warehouse_main_keyboard_router():
    """Warehouse main menu router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("warehouse")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)

    @router.message(F.text == "📦 Ombor")
    async def warehouse_start(message: Message, state: FSMContext):
        """Warehouse main menu handler"""
        try:
            # Debug logging
            print(f"Warehouse main menu handler called by user {message.from_user.id}")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            # Tex.txt bo'yicha warehouse vazifasi
            welcome_text = f"""
🏢 <b>Warehouse Panel - Ombor Boshqaruvi</b>

👋 Xush kelibsiz, {user.get('full_name', 'Warehouse xodimi')}!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Texnikdan kelgan zayavkalarni qabul qilish
• 📦 Kerakli jihozlarni tayyorlash va inventardan ajratish
• ✅ Jihozlar tayyor bo'lgach texnikka qaytarish
• 📝 Zayavkani yakunlash va mijozga xabar berish
• 📊 Inventar va statistikalarni boshqarish

<i>Tex.txt bo'yicha: Warehouse zayavka yakunida inventarni yangilaydi va mijozga bildirishnoma yuboradi.</i>
            """
            
            await message.answer(
                welcome_text.strip(),
                parse_mode='HTML',
                reply_markup=get_warehouse_main_keyboard('uz')
            )
            
            print(f"Warehouse main menu handler completed successfully")
            
        except Exception as e:
            print(f"Error in warehouse main menu handler: {str(e)}")
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "🏢 Warehouse")
    async def warehouse_alternative_start(message: Message, state: FSMContext):
        """Alternative warehouse main menu handler"""
        try:
            # Debug logging
            print(f"Warehouse alternative start handler called by user {message.from_user.id}")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            # Tex.txt bo'yicha warehouse vazifasi
            welcome_text = f"""
🏢 <b>Warehouse Panel - Ombor Boshqaruvi</b>

👋 Xush kelibsiz, {user.get('full_name', 'Warehouse xodimi')}!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Texnikdan kelgan zayavkalarni qabul qilish
• 📦 Kerakli jihozlarni tayyorlash va inventardan ajratish
• ✅ Jihozlar tayyor bo'lgach texnikka qaytarish
• 📝 Zayavkani yakunlash va mijozga xabar berish
• 📊 Inventar va statistikalarni boshqarish

<i>Tex.txt bo'yicha: Warehouse zayavka yakunida inventarni yangilaydi va mijozga bildirishnoma yuboradi.</i>
            """
            
            await message.answer(
                welcome_text.strip(),
                parse_mode='HTML',
                reply_markup=get_warehouse_main_keyboard('uz')
            )
            
            print(f"Warehouse alternative start handler completed successfully")
            
        except Exception as e:
            print(f"Error in warehouse alternative start handler: {str(e)}")
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "/start")
    async def warehouse_start_command(message: Message, state: FSMContext):
        """Warehouse start command handler"""
        try:
            # Debug logging
            print(f"Warehouse start command handler called by user {message.from_user.id}")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            welcome_text = f"""
🏢 <b>Warehouse Panel - Ombor Boshqaruvi</b>

👋 Xush kelibsiz, {user.get('full_name', 'Warehouse xodimi')}!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Texnikdan kelgan zayavkalarni qabul qilish
• 📦 Kerakli jihozlarni tayyorlash va inventardan ajratish
• ✅ Jihozlar tayyor bo'lgach texnikka qaytarish
• 📝 Zayavkani yakunlash va mijozga xabar berish
• 📊 Inventar va statistikalarni boshqarish

<i>Tex.txt bo'yicha: Warehouse zayavka yakunida inventarni yangilaydi va mijozga bildirishnoma yuboradi.</i>
            """
            
            await message.answer(
                welcome_text.strip(),
                parse_mode='HTML',
                reply_markup=get_warehouse_main_keyboard('uz')
            )
            
            print(f"Warehouse start command handler completed successfully")
            
        except Exception as e:
            print(f"Error in warehouse start command handler: {str(e)}")
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data == "get_warehouse_main_keyboard")
    async def get_warehouse_main_keyboard_callback(callback: CallbackQuery, state: FSMContext):
        """Return to warehouse main menu"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            welcome_text = f"""
🏢 <b>Warehouse Panel</b>

👤 {user.get('full_name', 'Warehouse xodimi')}
📊 Asosiy menyu

Kerakli bo'limni tanlang:
            """
            
            await callback.message.edit_text(
                welcome_text.strip(),
                parse_mode='HTML',
                reply_markup=get_warehouse_main_keyboard('uz')
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "warehouse_back")
    async def warehouse_back_handler(callback: CallbackQuery, state: FSMContext):
        """Go back to warehouse main menu"""
        try:
            # Debug logging
            print(f"Warehouse back callback handler called by user {callback.from_user.id}")
            
            await get_warehouse_main_keyboard_callback(callback, state)
            
        except Exception as e:
            print(f"Error in warehouse back callback handler: {str(e)}")
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(F.text == "◀️ Orqaga")
    async def warehouse_back_message_handler(message: Message, state: FSMContext):
        """Warehouse back message handler"""
        try:
            # Debug logging
            print(f"Warehouse back message handler called by user {message.from_user.id}")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            welcome_text = f"""
🏢 <b>Warehouse Panel - Ombor Boshqaruvi</b>

👋 Xush kelibsiz, {user.get('full_name', 'Warehouse xodimi')}!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Texnikdan kelgan zayavkalarni qabul qilish
• 📦 Kerakli jihozlarni tayyorlash va inventardan ajratish
• ✅ Jihozlar tayyor bo'lgach texnikka qaytarish
• 📝 Zayavkani yakunlash va mijozga xabar berish
• 📊 Inventar va statistikalarni boshqarish

<i>Tex.txt bo'yicha: Warehouse zayavka yakunida inventarni yangilaydi va mijozga bildirishnoma yuboradi.</i>
            """
            
            await message.answer(
                welcome_text.strip(),
                parse_mode='HTML',
                reply_markup=get_warehouse_main_keyboard('uz')
            )
            
            print(f"Warehouse back message handler completed successfully")
            
        except Exception as e:
            print(f"Error in warehouse back message handler: {str(e)}")
            await message.answer("Xatolik yuz berdi")

    # Language change handler
    @router.message(F.text == "🌐 Tilni o'zgartirish")
    async def change_language_handler(message: Message, state: FSMContext):
        """Language change handler for warehouse"""
        try:
            # Debug logging
            print(f"Warehouse language change handler called by user {message.from_user.id}")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            from keyboards.warehouse_buttons import language_selection_keyboard
            
            lang_text = "🌐 Tilni tanlang:"
            
            await message.answer(
                lang_text,
                reply_markup=language_selection_keyboard()
            )
            
            print(f"Warehouse language change handler completed successfully")
            
        except Exception as e:
            print(f"Error in warehouse language change handler: {str(e)}")
            await message.answer("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("set_language_"))
    async def set_language_callback(callback: CallbackQuery, state: FSMContext):
        """Set language callback"""
        try:
            new_lang = callback.data.split("_")[2]  # uz or ru
            
            # Mock success response (like other modules)
            success_text = "✅ Til muvaffaqiyatli o'zgartirildi!"
            
            # Create inline keyboard for back to main menu
            back_keyboard = get_warehouse_back_to_main_keyboard(lang)
            
            await callback.message.edit_text(
                text=success_text,
                reply_markup=back_keyboard
            )
            await callback.answer()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "warehouse_back_to_main")
    async def warehouse_back_to_main_handler(callback: CallbackQuery, state: FSMContext):
        """Handle back to main menu button for warehouse"""
        try:
            await callback.answer()
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            welcome_text = f"""
🏢 <b>Warehouse Panel - Ombor Boshqaruvi</b>

👋 Xush kelibsiz, {user.get('full_name', 'Warehouse xodimi')}!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Texnikdan kelgan zayavkalarni qabul qilish
• 📦 Kerakli jihozlarni tayyorlash va inventardan ajratish
• ✅ Jihozlar tayyor bo'lgach texnikka qaytarish
• 📝 Zayavkani yakunlash va mijozga xabar berish
• 📊 Inventar va statistikalarni boshqarish

<i>Tex.txt bo'yicha: Warehouse zayavka yakunida inventarni yangilaydi va mijozga bildirishnoma yuboradi.</i>
            """
            
            # Send new message with main menu keyboard
            await callback.message.answer(
                welcome_text.strip(),
                parse_mode='HTML',
                reply_markup=get_warehouse_main_keyboard('uz')
            )
            
            # Delete the previous message
            await callback.message.delete()
            
        except Exception as e:
            await callback.answer("❌ Xatolik yuz berdi", show_alert=True)

    @router.message(F.text == "🏠 Bosh sahifa")
    async def warehouse_home_handler(message: Message, state: FSMContext):
        """Warehouse home handler"""
        try:
            # Debug logging
            print(f"Warehouse home handler called by user {message.from_user.id}")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            
            await state.set_state(WarehouseMainMenuStates.main_menu)
            
            welcome_text = f"""
🏢 <b>Warehouse Panel - Ombor Boshqaruvi</b>

👋 Xush kelibsiz, {user.get('full_name', 'Warehouse xodimi')}!

📋 <b>Sizning vazifalaringiz:</b>
• 📥 Texnikdan kelgan zayavkalarni qabul qilish
• 📦 Kerakli jihozlarni tayyorlash va inventardan ajratish
• ✅ Jihozlar tayyor bo'lgach texnikka qaytarish
• 📝 Zayavkani yakunlash va mijozga xabar berish
• 📊 Inventar va statistikalarni boshqarish

<i>Tex.txt bo'yicha: Warehouse zayavka yakunida inventarni yangilaydi va mijozga bildirishnoma yuboradi.</i>
            """
            
            await message.answer(
                welcome_text.strip(),
                parse_mode='HTML',
                reply_markup=get_warehouse_main_keyboard('uz')
            )
            
            print(f"Warehouse home handler completed successfully")
            
        except Exception as e:
            print(f"Error in warehouse home handler: {str(e)}")
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "ℹ️ Yordam")
    async def warehouse_help_handler(message: Message, state: FSMContext):
        """Warehouse help handler"""
        try:
            # Debug logging
            print(f"Warehouse help handler called by user {message.from_user.id}")
            
            help_text = """
ℹ️ <b>Warehouse Yordam</b>

📋 <b>Asosiy funksiyalar:</b>
• 📦 Inventar boshqaruvi
• 📋 Buyurtmalar ko'rish
• 📊 Statistika va hisobotlar
• 📥 Yangi so'rovlarni ko'rish
• ✅ Tayyor bo'lgan so'rovlarni yuborish

📞 <b>Qo'llab-quvvatlash:</b>
Agar muammo bo'lsa, administrator bilan bog'laning.

🔧 <b>Texnik yordam:</b>
Sistemada muammo bo'lsa, texnik xizmat bilan bog'laning.
            """
            
            await message.answer(
                help_text.strip(),
                parse_mode='HTML'
            )
            
            print(f"Warehouse help handler completed successfully")
            
        except Exception as e:
            print(f"Error in warehouse help handler: {str(e)}")
            await message.answer("Xatolik yuz berdi")

    return router

# Mock functions (like other modules)
async def get_warehouse_user_by_telegram_id(telegram_id: int):
    """Get warehouse user by telegram id (mock function like other modules)"""
    try:
        # Mock user data (like other modules)
        return {
            'id': 1,
            'telegram_id': telegram_id,
            'full_name': 'Warehouse xodimi',
            'role': 'warehouse',
            'language': 'uz'
        }
    except Exception as e:
        return None

async def update_warehouse_user_language(user_id: int, language: str):
    """Update warehouse user language (mock function like other modules)"""
    try:
        # Mock update (like other modules)
        return True
    except Exception as e:
        return False

async def get_user_lang(user_id: int):
    """Get user language (mock function like other modules)"""
    try:
        # Mock language (like other modules)
        return 'uz'
    except Exception as e:
        return 'uz'
