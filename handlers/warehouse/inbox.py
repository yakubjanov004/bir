import json
import html
from typing import List, Dict
from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from states.warehouse_states import WarehouseWorkflowStates
from filters.role_filter import RoleFilter
from keyboards.warehouse_buttons import (
    get_warehouse_inbox_navigation_keyboard,
    get_warehouse_request_actions_keyboard,
    get_warehouse_back_to_inbox_keyboard,
    get_warehouse_cancel_keyboard,
    get_warehouse_application_actions_keyboard
)

class WarehouseWorkflowFSM(StatesGroup):
    viewing_request = State()
    entering_return_reason = State()
    preparing_equipment = State()

def get_warehouse_inbox_router():
    """Warehouse inbox router"""
    router = Router()
    
    # Apply role filter
    role_filter = RoleFilter("warehouse")
    router.message.filter(role_filter)
    router.callback_query.filter(role_filter)
    
    @router.callback_query(F.data.startswith("open_inbox_"))
    async def handle_inbox_notification(callback: CallbackQuery, state: FSMContext):
        """Handle inbox notification button click"""
        try:
            await callback.answer()
            
            # Extract request ID
            request_id_short = callback.data.replace("open_inbox_", "")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz',
                'role': 'warehouse'
            }
            
            # Show inbox
            await show_warehouse_inbox_from_notification(callback.message, state, request_id_short)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi")
    
    async def show_warehouse_inbox_from_notification(message: Message, state: FSMContext, target_request_id: str = None):
        """Show warehouse inbox with focus on specific request"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz',
                'role': 'warehouse'
            }
            
            lang = user.get('language', 'uz')
            
            # Mock inbox messages (like other modules)
            inbox_messages = [
                {
                    'id': 1,
                    'application_id': 'WH001',
                    'message': 'Test message 1'
                },
                {
                    'id': 2,
                    'application_id': 'WH002',
                    'message': 'Test message 2'
                }
            ]
            
            if not inbox_messages:
                text = "📭 Inbox bo'sh"
                await message.answer(text)
                return
            
            # Find target request index if specified
            target_index = 0
            if target_request_id:
                for i, msg in enumerate(inbox_messages):
                    if msg['application_id'].startswith(target_request_id):
                        target_index = i
                        break
            
            # Mock requests data (like other modules)
            requests = [
                {
                    'id': 'WH001',
                    'client_name': 'Test Client 1',
                    'description': 'Test description 1',
                    'created_at': datetime.now(),
                    'materials': [
                        {'name': 'Cable', 'quantity': 2, 'unit': 'dona'},
                        {'name': 'Router', 'quantity': 1, 'unit': 'dona'}
                    ],
                    'inbox_message': inbox_messages[0]
                },
                {
                    'id': 'WH002',
                    'client_name': 'Test Client 2',
                    'description': 'Test description 2',
                    'created_at': datetime.now(),
                    'materials': [
                        {'name': 'Connector', 'quantity': 5, 'unit': 'dona'}
                    ],
                    'inbox_message': inbox_messages[1]
                }
            ]
            
            if not requests:
                text = "📭 Inbox bo'sh"
                await message.answer(text)
                return
            
            await state.update_data(
                warehouse_requests=requests,
                current_index=target_index
            )
            
            # Display the targeted request
            await display_warehouse_request(message, state, lang, requests, target_index)
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    @router.message(F.text == "📥 Inbox")
    async def show_warehouse_inbox(message: Message, state: FSMContext):
        """Show warehouse inbox with technician requests"""
        try:
            # Mock user data
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz',
                'role': 'warehouse'
            }
            
            lang = user.get('language', 'uz')
            
            # Get warehouse requests from technicians
            warehouse_requests = await get_warehouse_requests()
            
            if not warehouse_requests:
                no_requests_text = "📭 Texniklardan kelgan so'rovlar yo'q."
                await message.answer(no_requests_text)
                return

            await state.update_data(warehouse_requests=warehouse_requests, current_index=0)
            inbox_title = "📥 <b>Ombor Inbox - Texniklardan kelgan so'rovlar:</b>"
            
            # Send the title separately
            await message.answer(
                inbox_title,
                parse_mode='HTML'
            )
            
            # Display first request
            await display_warehouse_request(message, state, lang, warehouse_requests, 0)
            
        except Exception as e:
            print(f"Error in warehouse inbox handler: {str(e)}")
            await message.answer("Xatolik yuz berdi")

    async def display_application(message: Message, state: FSMContext, lang: str, applications: List[Dict], index: int):
        """Display a single application with pagination buttons - detailed view."""
        try:
            app = applications[index]
            app_id = app['id']
            app_details = app.get('application_details', {})
            
            # Get basic info
            client_name = app_details.get('client_name', 'N/A')
            created = app_details.get('created_at', '').strftime('%d.%m.%Y %H:%M') if app_details.get('created_at') else '-'
            description = app_details.get('description', 'Tavsif yo\'q')
            diagnosis = app_details.get('diagnosis', 'Diagnostika yo\'q')
            
            # Get materials info
            materials = app_details.get('materials', [])
            materials_text = ""
            if materials:
                try:
                    if isinstance(materials, str):
                        materials = json.loads(materials)
                    
                    materials_text = "\n"
                    for i, material in enumerate(materials, 1):
                        name = material.get('name', 'N/A')
                        quantity = material.get('quantity', 0)
                        unit = material.get('unit', 'dona')
                        materials_text += f"  {i}. {name} - {quantity} {unit}\n"
                except Exception as e:
                    materials_text = "\n❌ Materiallar ma'lumotida xatolik\n"
            else:
                materials_text = "\n❌ Materiallar ko'rsatilmagan\n"
            
            # Mock comments count (like other modules)
            comments_count = 2

            # More detailed text with better formatting
            text = (
                f"📦 <b>Zayavka #{app_id[:8]}</b>\n"
                f"👤 <b>Mijoz:</b> {client_name}\n"
                f"📅 <b>Sana:</b> {created}\n"
                f"📄 <b>Tavsif:</b> {description}\n"
                f"🔧 <b>Diagnostika:</b> {diagnosis}\n"
                f"💬 <b>Izohlar:</b> {comments_count} ta\n"
                f"📦 <b>Materiallar kerak:</b>{materials_text}"
            )
            
            # Create action buttons
            buttons = []
            
            # Add action buttons
            action_buttons = []
            
            # Add complete button
            action_buttons.append(InlineKeyboardButton(
                text="✅ Yakunlash",
                callback_data=f"wh_complete_{app_id}"
            ))
            
            # Add return to technician button
            action_buttons.append(InlineKeyboardButton(
                text="🔧 Texnikka qaytarish",
                callback_data=f"wh_return_tech_{app_id}"
            ))
            
            buttons.append(action_buttons)
            
            # Navigation buttons
            nav_buttons = []
            if index > 0:
                nav_buttons.append(InlineKeyboardButton(
                    text="⬅️ Oldingi",
                    callback_data="wh_prev"
                ))
            if index < len(applications) - 1:
                nav_buttons.append(InlineKeyboardButton(
                    text="Keyingisi ➡️",
                    callback_data="wh_next"
                ))
            
            if nav_buttons:
                buttons.append(nav_buttons)

            keyboard = get_warehouse_application_actions_keyboard(app_id, lang)
            # Add navigation buttons if needed
            if nav_buttons:
                keyboard.inline_keyboard.append(nav_buttons)
            
            await message.answer(
                text,
                parse_mode='HTML',
                reply_markup=keyboard
            )
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    async def display_application_edit(message: Message, state: FSMContext, lang: str, applications: List[Dict], index: int):
        """Display a single application by editing the current message."""
        try:
            app = applications[index]
            app_id = app['id']
            app_details = app.get('application_details', {})
            
            # Get basic info
            client_name = app_details.get('client_name', 'N/A')
            created = app_details.get('created_at', '').strftime('%d.%m.%Y %H:%M') if app_details.get('created_at') else '-'
            description = app_details.get('description', 'Tavsif yo\'q')
            diagnosis = app_details.get('diagnosis', 'Diagnostika yo\'q')
            
            # Get materials info
            materials = app_details.get('materials', [])
            materials_text = ""
            if materials:
                try:
                    if isinstance(materials, str):
                        materials = json.loads(materials)
                    
                    materials_text = "\n"
                    for i, material in enumerate(materials, 1):
                        name = material.get('name', 'N/A')
                        quantity = material.get('quantity', 0)
                        unit = material.get('unit', 'dona')
                        materials_text += f"  {i}. {name} - {quantity} {unit}\n"
                except Exception as e:
                    materials_text = "\n❌ Materiallar ma'lumotida xatolik\n"
            else:
                materials_text = "\n❌ Materiallar ko'rsatilmagan\n"
            
            # Mock comments count (like other modules)
            comments_count = 2

            # More detailed text with better formatting
            text = (
                f"📦 <b>Zayavka #{app_id[:8]}</b>\n"
                f"👤 <b>Mijoz:</b> {client_name}\n"
                f"📅 <b>Sana:</b> {created}\n"
                f"📄 <b>Tavsif:</b> {description}\n"
                f"🔧 <b>Diagnostika:</b> {diagnosis}\n"
                f"💬 <b>Izohlar:</b> {comments_count} ta\n"
                f"📦 <b>Materiallar kerak:</b>{materials_text}"
            )
            
            # Create action buttons
            buttons = []
            
            # Add action buttons
            action_buttons = []
            
            # Add complete button
            action_buttons.append(InlineKeyboardButton(
                text="✅ Yakunlash",
                callback_data=f"wh_complete_{app_id}"
            ))
            
            # Add return to technician button
            action_buttons.append(InlineKeyboardButton(
                text="🔧 Texnikka qaytarish",
                callback_data=f"wh_return_tech_{app_id}"
            ))
            
            buttons.append(action_buttons)
            
            # Navigation buttons
            nav_buttons = []
            if index > 0:
                nav_buttons.append(InlineKeyboardButton(
                    text="⬅️ Oldingi",
                    callback_data="wh_prev"
                ))
            if index < len(applications) - 1:
                nav_buttons.append(InlineKeyboardButton(
                    text="Keyingisi ➡️",
                    callback_data="wh_next"
                ))
            
            if nav_buttons:
                buttons.append(nav_buttons)

            keyboard = get_warehouse_application_actions_keyboard(app_id, lang)
            # Add navigation buttons if needed
            if nav_buttons:
                keyboard.inline_keyboard.append(nav_buttons)
            
            # Edit the current message instead of sending a new one
            await message.edit_text(text, parse_mode='HTML', reply_markup=keyboard)
            
        except Exception as e:
            await message.edit_text("Xatolik yuz berdi")

    @router.callback_query(F.data == "wh_next")
    async def warehouse_next(callback: CallbackQuery, state: FSMContext):
        """Navigate to next warehouse request"""
        try:
            data = await state.get_data()
            warehouse_requests = data.get('warehouse_requests', [])
            current_index = data.get('current_index', 0)
            
            if current_index < len(warehouse_requests) - 1:
                new_index = current_index + 1
                await state.update_data(current_index=new_index)
                
                # Mock user data
                user = {
                    'id': 1,
                    'full_name': 'Warehouse xodimi',
                    'language': 'uz'
                }
                lang = user.get('language', 'uz')
                
                await display_warehouse_request_edit(callback.message, state, lang, warehouse_requests, new_index)
            else:
                await callback.answer("Oxirgi so'rov")
            
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data == "wh_prev")
    async def warehouse_prev(callback: CallbackQuery, state: FSMContext):
        """Navigate to previous warehouse request"""
        try:
            data = await state.get_data()
            warehouse_requests = data.get('warehouse_requests', [])
            current_index = data.get('current_index', 0)
            
            if current_index > 0:
                new_index = current_index - 1
                await state.update_data(current_index=new_index)
                
                # Mock user data
                user = {
                    'id': 1,
                    'full_name': 'Warehouse xodimi',
                    'language': 'uz'
                }
                lang = user.get('language', 'uz')
                
                await display_warehouse_request_edit(callback.message, state, lang, warehouse_requests, new_index)
            else:
                await callback.answer("Birinchi so'rov")
            
            await callback.answer()
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("wh_prepare_"))
    async def prepare_equipment(callback: CallbackQuery, state: FSMContext):
        """Prepare equipment for warehouse"""
        try:
            request_id_short = callback.data.replace("wh_prepare_", "")
            
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            
            # Mock success response (like other modules)
            text = f"✅ Uskuna tayyorlandi! (Ariza: {request_id_short})"
            await callback.message.edit_text(text)
            await callback.answer()
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("wh_approve_"))
    async def approve_warehouse_request_handler(callback: CallbackQuery, state: FSMContext):
        """Approve warehouse request"""
        try:
            request_id = callback.data.replace("wh_approve_", "")
            
            # Get request data
            data = await state.get_data()
            warehouse_requests = data.get('warehouse_requests', [])
            current_index = data.get('current_index', 0)
            
            if current_index < len(warehouse_requests):
                request = warehouse_requests[current_index]
                
                # Mock approval
                success = await approve_warehouse_request(request_id)
                
                if success:
                    # Show approval confirmation
                    approval_text = (
                        f"✅ <b>Ombor so'rovi tasdiqlandi!</b>\n\n"
                        f"🆔 <b>So'rov ID:</b> {request['id']}\n"
                        f"🔧 <b>Texnik:</b> {request['technician_name']}\n"
                        f"👤 <b>Mijoz:</b> {request['client_name']}\n"
                        f"📍 <b>Manzil:</b> {request['location']}\n"
                        f"📦 <b>Tasdiqlangan mahsulot:</b>\n"
                        f"<i>{request['warehouse_item']}</i>\n\n"
                        f"✅ Mahsulot tayyorlanmoqda va texnikka yuboriladi."
                    )
                    
                    # Create back to inbox button
                    keyboard = get_warehouse_back_to_inbox_keyboard(lang)
                    
                    await callback.message.edit_text(
                        approval_text,
                        parse_mode='HTML',
                        reply_markup=keyboard
                    )
                    await callback.answer("✅ So'rov tasdiqlandi!")
                    
                    # Remove the request from the list
                    warehouse_requests.pop(current_index)
                    await state.update_data(warehouse_requests=warehouse_requests)
                    
                    if warehouse_requests:
                        # Show next request or previous if at end
                        new_index = min(current_index, len(warehouse_requests) - 1)
                        await state.update_data(current_index=new_index)
                        
                        # Show updated request list
                        await display_warehouse_request_edit(callback.message, state, 'uz', warehouse_requests, new_index)
                    else:
                        # No more requests
                        await callback.message.edit_text("📭 Barcha so'rovlar tasdiqlandi!")
                else:
                    await callback.answer("❌ Tasdiqlashda xatolik yuz berdi", show_alert=True)
            else:
                await callback.answer("❌ So'rov topilmadi", show_alert=True)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)

    @router.callback_query(F.data.startswith("wh_reject_"))
    async def reject_warehouse_request_handler(callback: CallbackQuery, state: FSMContext):
        """Reject warehouse request"""
        try:
            request_id = callback.data.replace("wh_reject_", "")
            
            # Get request data
            data = await state.get_data()
            warehouse_requests = data.get('warehouse_requests', [])
            current_index = data.get('current_index', 0)
            
            if current_index < len(warehouse_requests):
                request = warehouse_requests[current_index]
                
                # Show rejection reason input
                rejection_text = (
                    f"❌ <b>Ombor so'rovini rad etish</b>\n\n"
                    f"🆔 <b>So'rov ID:</b> {request['id']}\n"
                    f"🔧 <b>Texnik:</b> {request['technician_name']}\n"
                    f"👤 <b>Mijoz:</b> {request['client_name']}\n"
                    f"📍 <b>Manzil:</b> {request['location']}\n"
                    f"📦 <b>So'ralayotgan mahsulot:</b>\n"
                    f"<i>{request['warehouse_item']}</i>\n\n"
                    f"📝 Iltimos, rad etish sababini yozing:"
                )
                
                # Store request info in state
                await state.update_data(
                    current_reject_request_id=request_id,
                    current_reject_request_data=request
                )
                
                # Create cancel button
                keyboard = get_warehouse_cancel_keyboard(lang)
                
                await callback.message.edit_text(
                    rejection_text,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
                
                # Set state to wait for rejection reason
                await state.set_state(WarehouseWorkflowStates.entering_return_reason)
                
            else:
                await callback.answer("❌ So'rov topilmadi", show_alert=True)
            
        except Exception as e:
            await callback.answer("Xatolik yuz berdi", show_alert=True)





    @router.message(WarehouseWorkflowStates.entering_return_reason)
    async def handle_rejection_reason_input(message: Message, state: FSMContext):
        """Handle rejection reason input"""
        try:
            # Get the rejection reason
            rejection_reason = message.text.strip()
            
            if len(rejection_reason) < 5:
                await message.answer(
                    "⚠️ Iltimos, kamida 5 ta belgi kiriting. Rad etish sababini yozing."
                )
                return
            
            # Get request data from state
            data = await state.get_data()
            request_id = data.get('current_reject_request_id')
            request = data.get('current_reject_request_data')
            warehouse_requests = data.get('warehouse_requests', [])
            current_index = data.get('current_index', 0)
            
            if not request_id or not request:
                await message.answer("❌ So'rov ma'lumotlari topilmadi. Iltimos, qaytadan urinib ko'ring.")
                return
            
            # Mock rejection
            success = await reject_warehouse_request(request_id, rejection_reason)
            
            if success:
                # Show rejection confirmation
                rejection_text = (
                    f"❌ <b>Ombor so'rovi rad etildi!</b>\n\n"
                    f"🆔 <b>So'rov ID:</b> {request['id']}\n"
                    f"🔧 <b>Texnik:</b> {request['technician_name']}\n"
                    f"👤 <b>Mijoz:</b> {request['client_name']}\n"
                    f"📍 <b>Manzil:</b> {request['location']}\n"
                    f"📦 <b>Rad etilgan mahsulot:</b>\n"
                    f"<i>{request['warehouse_item']}</i>\n\n"
                    f"📝 <b>Rad etish sababi:</b>\n"
                    f"<i>{rejection_reason}</i>\n\n"
                    f"❌ Texnikka xabar yuborildi."
                )
                
                # Create back to inbox button
                keyboard = get_warehouse_back_to_inbox_keyboard(lang)
                
                await message.answer(
                    rejection_text,
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
                
                # Remove the request from the list
                if warehouse_requests and current_index < len(warehouse_requests):
                    warehouse_requests.pop(current_index)
                    await state.update_data(warehouse_requests=warehouse_requests)
                    
                    if warehouse_requests:
                        # Show next request or previous if at end
                        new_index = min(current_index, len(warehouse_requests) - 1)
                        await state.update_data(current_index=new_index)
                        
                        # Show updated request list
                        await display_warehouse_request_edit(message, state, 'uz', warehouse_requests, new_index)
                    else:
                        # No more requests
                        await message.answer("📭 Barcha so'rovlar ko'rib chiqildi!")
                
                # Clear the waiting state
                await state.clear()
                
            else:
                await message.answer("❌ Rad etishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
            
        except Exception as e:
            print(f"Error in handle_rejection_reason_input: {e}")
            await message.answer("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

    @router.callback_query(F.data == "wh_back_to_inbox")
    async def back_to_warehouse_inbox(callback: CallbackQuery, state: FSMContext):
        """Return to warehouse inbox"""
        try:
            # Mock user data
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz',
                'role': 'warehouse'
            }
            
            lang = user.get('language', 'uz')
            
            # Get warehouse requests
            warehouse_requests = await get_warehouse_requests()
            
            if not warehouse_requests:
                no_requests_text = "📭 Texniklardan kelgan so'rovlar yo'q."
                await callback.message.edit_text(no_requests_text)
                return

            await state.update_data(warehouse_requests=warehouse_requests, current_index=0)
            inbox_title = "📥 <b>Ombor Inbox - Texniklardan kelgan so'rovlar:</b>"
            
            # Display first request
            await display_warehouse_request_edit(callback.message, state, lang, warehouse_requests, 0)
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")

    @router.callback_query(F.data.startswith("wh_return_tech_"))
    async def return_to_technician(callback: CallbackQuery, state: FSMContext):
        """Return request to technician"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz'
            }
            lang = user.get('language', 'uz')
            request_id = callback.data.replace("wh_return_tech_", "")
            
            # Update message with return status
            text = (
                f"🔧 <b>Zayavka texnikka qaytarildi!</b>\n"
                f"📦 Ombor: ❌ Qaytarildi\n"
                f"🔧 Texnik: ⏳ Yangi vazifa\n"
                f"📝 Ariza ID: {request_id}\n"
                f"ℹ️ Texnik zayavkani qayta ko'rib chiqadi"
            )
            
            await callback.message.edit_text(text, parse_mode='HTML')
            await callback.answer("✅ Zayavka texnikka qaytarildi!")
            
            # Remove the application from the list and show next one
            data = await state.get_data()
            applications = data.get('application_list', [])
            current_index = data.get('current_index', 0)
            
            # Remove returned application
            if applications and current_index < len(applications):
                applications.pop(current_index)
                await state.update_data(application_list=applications)
                
                if applications:
                    # Show next application or previous if at end
                    new_index = min(current_index, len(applications) - 1)
                    await state.update_data(current_index=new_index)
                    
                    # Show updated application list
                    await display_application_edit(callback.message, state, lang, applications, new_index)
                else:
                    # No more applications
                    await callback.message.edit_text("📭 Barcha zayavkalar qaytarildi!")
                
        except Exception as e:
            await callback.answer("Xatolik yuz berdi!", show_alert=True)

    async def back_to_inbox(callback: CallbackQuery, state: FSMContext):
        """Return to warehouse inbox"""
        try:
            # Mock user data (like other modules)
            user = {
                'id': 1,
                'full_name': 'Warehouse xodimi',
                'language': 'uz',
                'role': 'warehouse'
            }
            
            lang = user.get('language', 'uz')
            
            # Mock applications data (like other modules)
            applications = [
                {
                    'id': 'WH001',
                    'application_details': {
                        'id': 'WH001',
                        'client_name': 'Test Client 1',
                        'description': 'Test description 1',
                        'created_at': datetime.now(),
                        'materials': [
                            {'name': 'Cable', 'quantity': 2, 'unit': 'dona'},
                            {'name': 'Router', 'quantity': 1, 'unit': 'dona'}
                        ]
                    }
                },
                {
                    'id': 'WH002',
                    'application_details': {
                        'id': 'WH002',
                        'client_name': 'Test Client 2',
                        'description': 'Test description 2',
                        'created_at': datetime.now(),
                        'materials': [
                            {'name': 'Connector', 'quantity': 5, 'unit': 'dona'}
                        ]
                    }
                }
            ]
            
            if not applications:
                no_requests_text = "📭 Sizga biriktirilgan zayavkalar yo'q."
                await callback.message.edit_text(no_requests_text)
                return

            await state.update_data(application_list=applications, current_index=0)
            inbox_title = "📥 <b>Ombor Inbox - Sizga biriktirilgan zayavkalar:</b>"
            
            # Display first request
            await display_application_edit(callback.message, state, lang, applications, 0)
            
        except Exception as e:
            await callback.message.edit_text("Xatolik yuz berdi")




    async def display_warehouse_request(message: Message, state: FSMContext, lang: str, requests: List[Dict], index: int):
        """Display warehouse request from technician"""
        try:
            if index >= len(requests):
                await message.answer("So'rov topilmadi")
                return
            
            request = requests[index]
            
            # Priority emoji
            priority_emoji = "🚨" if request.get('priority') == 'urgent' else "📋"
            priority_text = "Shoshilinch" if request.get('priority') == 'urgent' else "Oddiy"
            
            # Format created date
            created_date = request.get('created_at', datetime.now()).strftime('%d.%m.%Y %H:%M')
            
            text = (
                f"{priority_emoji} <b>Ombor so'rovi #{request['id'][:8]}</b>\n\n"
                f"🔧 <b>Texnik:</b> {request['technician_name']}\n"
                f"👤 <b>Mijoz:</b> {request['client_name']}\n"
                f"📞 <b>Telefon:</b> {request['client_phone']}\n"
                f"📍 <b>Manzil:</b> {request['location']}\n"
                f"📅 <b>Sana:</b> {created_date}\n"
                f"⚡ <b>Ustuvorlik:</b> {priority_text}\n\n"
                f"📦 <b>So'ralayotgan mahsulot:</b>\n"
                f"<i>{request['warehouse_item']}</i>\n\n"
                f"📝 <b>Texnik izohi:</b>\n"
                f"<i>{request['request_notes']}</i>"
            )
            
            # Create action buttons
            buttons = []
            
            # Add action buttons
            action_buttons = []
            
            # Add approve button
            action_buttons.append(InlineKeyboardButton(
                text="✅ Tasdiqlash",
                callback_data=f"wh_approve_{request['id']}"
            ))
            
            # Add reject button
            action_buttons.append(InlineKeyboardButton(
                text="❌ Rad etish",
                callback_data=f"wh_reject_{request['id']}"
            ))
            
            buttons.append(action_buttons)
            
            # Navigation buttons
            nav_buttons = []
            if index > 0:
                nav_buttons.append(InlineKeyboardButton(
                    text="⬅️ Oldingi",
                    callback_data="wh_prev"
                ))
            if index < len(requests) - 1:
                nav_buttons.append(InlineKeyboardButton(
                    text="Keyingisi ➡️",
                    callback_data="wh_next"
                ))
            
            if nav_buttons:
                buttons.append(nav_buttons)

            keyboard = get_warehouse_request_actions_keyboard(request['id'], lang)
            # Add navigation buttons if needed
            if nav_buttons:
                keyboard.inline_keyboard.append(nav_buttons)
            
            await message.answer(
                text,
                parse_mode='HTML',
                reply_markup=keyboard
            )
            
        except Exception as e:
            await message.answer("Xatolik yuz berdi")

    async def display_warehouse_request_edit(message: Message, state: FSMContext, lang: str, requests: List[Dict], index: int):
        """Display warehouse request by editing the current message"""
        try:
            if index >= len(requests):
                await message.edit_text("So'rov topilmadi")
                return
            
            request = requests[index]
            
            # Priority emoji
            priority_emoji = "🚨" if request.get('priority') == 'urgent' else "📋"
            priority_text = "Shoshilinch" if request.get('priority') == 'urgent' else "Oddiy"
            
            # Format created date
            created_date = request.get('created_at', datetime.now()).strftime('%d.%m.%Y %H:%M')
            
            text = (
                f"{priority_emoji} <b>Ombor so'rovi #{request['id'][:8]}</b>\n\n"
                f"🔧 <b>Texnik:</b> {request['technician_name']}\n"
                f"👤 <b>Mijoz:</b> {request['client_name']}\n"
                f"📞 <b>Telefon:</b> {request['client_phone']}\n"
                f"📍 <b>Manzil:</b> {request['location']}\n"
                f"📅 <b>Sana:</b> {created_date}\n"
                f"⚡ <b>Ustuvorlik:</b> {priority_text}\n\n"
                f"📦 <b>So'ralayotgan mahsulot:</b>\n"
                f"<i>{request['warehouse_item']}</i>\n\n"
                f"📝 <b>Texnik izohi:</b>\n"
                f"<i>{request['request_notes']}</i>"
            )
            
            # Create action buttons
            buttons = []
            
            # Add action buttons
            action_buttons = []
            
            # Add approve button
            action_buttons.append(InlineKeyboardButton(
                text="✅ Tasdiqlash",
                callback_data=f"wh_approve_{request['id']}"
            ))
            
            # Add reject button
            action_buttons.append(InlineKeyboardButton(
                text="❌ Rad etish",
                callback_data=f"wh_reject_{request['id']}"
            ))
            
            buttons.append(action_buttons)
            
            # Navigation buttons
            nav_buttons = []
            if index > 0:
                nav_buttons.append(InlineKeyboardButton(
                    text="⬅️ Oldingi",
                    callback_data="wh_prev"
                ))
            if index < len(requests) - 1:
                nav_buttons.append(InlineKeyboardButton(
                    text="Keyingisi ➡️",
                    callback_data="wh_next"
                ))
            
            if nav_buttons:
                buttons.append(nav_buttons)

            keyboard = get_warehouse_request_actions_keyboard(request['id'], lang)
            # Add navigation buttons if needed
            if nav_buttons:
                keyboard.inline_keyboard.append(nav_buttons)
            
            await message.edit_text(
                text,
                parse_mode='HTML',
                reply_markup=keyboard
            )
            
        except Exception as e:
            await message.edit_text("Xatolik yuz berdi")

    return router

# Mock functions for warehouse inbox
async def get_warehouse_requests():
    """Get warehouse requests from technicians (mock function)"""
    try:
        return [
            {
                'id': 'req_001_2024_01_15',
                'technician_name': 'Aziz Karimov',
                'client_name': 'Jasur Rahimov',
                'client_phone': '+998 90 123 45 67',
                'location': 'Tashkent, Shayxontohur tumani, 67-uy',
                'created_at': datetime.now(),
                'warehouse_item': 'Router TP-Link Archer C6 - 2',
                'request_notes': 'Yangi router o\'rnatish uchun kerak',
                'status': 'pending_warehouse',
                'priority': 'normal'
            },
            {
                'id': 'req_002_2024_01_15',
                'technician_name': 'Dilfuza Abdullayeva',
                'client_name': 'Malika Karimova',
                'client_phone': '+998 91 234 56 78',
                'location': 'Tashkent, Chilonzor tumani, 45-uy',
                'created_at': datetime.now(),
                'warehouse_item': 'Network Cable Cat6 - 50 metr',
                'request_notes': 'Internet kabelini almashtirish uchun',
                'status': 'pending_warehouse',
                'priority': 'urgent'
            },
            {
                'id': 'req_003_2024_01_15',
                'technician_name': 'Bobur Toshmatov',
                'client_name': 'Olimjon Safarov',
                'client_phone': '+998 92 345 67 89',
                'location': 'Tashkent, Sergeli tumani, 23-uy',
                'created_at': datetime.now(),
                'warehouse_item': 'WiFi Adapter USB - 1 dona',
                'request_notes': 'Kompyuter uchun WiFi adapter kerak',
                'status': 'pending_warehouse',
                'priority': 'normal'
            },
            {
                'id': 'req_004_2024_01_15',
                'technician_name': 'Aziza Karimova',
                'client_name': 'Fazliddin Rahimov',
                'client_phone': '+998 93 456 78 90',
                'location': 'Tashkent, Yashnobod tumani, 89-uy',
                'created_at': datetime.now(),
                'warehouse_item': 'Power Supply 12V - 2 dona',
                'request_notes': 'Kamera tizimi uchun quvvat manbai',
                'status': 'pending_warehouse',
                'priority': 'urgent'
            },
            {
                'id': 'req_005_2024_01_15',
                'technician_name': 'Jahongir Toshmatov',
                'client_name': 'Nilufar Karimova',
                'client_phone': '+998 94 567 89 01',
                'location': 'Tashkent, Mirzo Ulug\'bek tumani, 12-uy',
                'created_at': datetime.now(),
                'warehouse_item': 'Switch 8-port - 1 dona',
                'request_notes': 'Ofis tarmog\'i uchun switch kerak',
                'status': 'pending_warehouse',
                'priority': 'normal'
            }
        ]
    except Exception as e:
        return []

async def approve_warehouse_request(request_id: str, warehouse_notes: str = ""):
    """Approve warehouse request (mock function)"""
    try:
        # Mock approval
        return True
    except Exception as e:
        return False

async def reject_warehouse_request(request_id: str, rejection_reason: str):
    """Reject warehouse request (mock function)"""
    try:
        # Mock rejection
        return True
    except Exception as e:
        return False