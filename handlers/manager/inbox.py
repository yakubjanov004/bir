"""
Manager Inbox (QISQA KO'RINISH) — aiogram 3
- Har bir ariza uchun faqat quyidagi maydonlar chiqadi:
  ID, Tarif, Mijoz, Telefon, Manzil, Yaratilgan
- Inline tugmalar: ⬅️ Oldingi | Kichik menejerga yuborish | Keyingi ➡️
- "Kichik menejerga yuborish" bosilganda JM ro'yxati inline ochiladi
- JM tanlanganda "Kichik menejerga yuborildi ✅" xabari chiqadi va keyingi ariza ko'rsatiladi
"""

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
import asyncio

# Role filter import
from filters.role_filter import RoleFilter

# === MOCKLAR ===

async def get_user_by_telegram_id(telegram_id: int):
    return {
        "id": 1,
        "telegram_id": telegram_id,
        "role": "manager",
        "language": "uz",
        "full_name": "Test Manager",
        "phone_number": "+998901234567",
    }

async def get_users_by_role(role: str):
    if role != "junior_manager":
        return []
    return [
        {"id": 11, "full_name": "Ahmad Toshmatov"},
        {"id": 12, "full_name": "Malika Karimova"},
        {"id": 13, "full_name": "Jasur Rahimov"},
        {"id": 14, "full_name": "Dilfuza Abdullayeva"},
    ]

class MockWorkflowEngine:
    async def transition_workflow(self, request_id: str, action: str, role: str, data: dict):
        print(f"[MOCK] transition: {request_id=} {action=} {role=} {data=}")
        return True

# 4-5 ta QISQA mock arizalar
def _now():
    return datetime.now()

MOCK_REQUESTS = [
    {
        "id": "req_001_2025_08_26",
        "tariff": "Yangi",
        "client": "Aziz Karimov",
        "phone": "+998901234567",
        "address": "Tashkent, Chorsu tumani, 15-uy",
        "created_at": _now() - timedelta(minutes=30),
    },
    {
        "id": "req_002_2025_08_26",
        "tariff": "Standard",
        "client": "Malika Toshmatova",
        "phone": "+998901234568",
        "address": "Tashkent, Yunusabad tumani, 45-uy",
        "created_at": _now() - timedelta(hours=1, minutes=15),
    },
    {
        "id": "req_003_2025_08_25",
        "tariff": "Yangi",
        "client": "Jasur Rahimov",
        "phone": "+998901234569",
        "address": "Tashkent, Sergeli tumani, 78-uy",
        "created_at": _now() - timedelta(hours=5),
    },
    {
        "id": "req_004_2025_08_25",
        "tariff": "Yangi",
        "client": "Shahnoza Mirzayeva",
        "phone": "+998901234570",
        "address": "Tashkent, Yakkasaroy tumani, 89-uy",
        "created_at": _now() - timedelta(days=1, hours=2),
    },
    {
        "id": "req_005_2025_08_24",
        "tariff": "Standard",
        "client": "Zarina Usmanova",
        "phone": "+998901234571",
        "address": "Tashkent, Bektemir tumani, 12-uy",
        "created_at": _now() - timedelta(days=2),
    },
]

# === UTIL ===

def fmt_dt(dt: datetime) -> str:
    return dt.strftime("%d.%m.%Y %H:%M")

def short_view_text(item: dict) -> str:
    # ID formatini foydalanuvchidek ko'rsatamiz: req_001- _2024 (siz so'ragandek uslub)
    full_id = item["id"]
    short_id = f"{full_id.split('_')[0]}-{full_id.split('_')[1]}"
    created = fmt_dt(item["created_at"])
    return (
        "🔌 <b>Manager Inbox</b>\n"
        f"🆔 <b>ID:</b> {short_id}\n"
        f"📊 <b>Tarif:</b> {item['tariff']}\n"
        f"👤 <b>Mijoz:</b> {item['client']}\n"
        f"📞 <b>Telefon:</b> {item['phone']}\n"
        "📍 <b>Manzil:</b> {item['address']}\n"
        f"📅 <b>Yaratilgan:</b> {created}"
    )

def nav_keyboard(index: int, total: int, current_id: str) -> InlineKeyboardMarkup:
    rows = []
    # Prev
    if index > 0:
        rows.append([
            InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"mgr_inbox_prev_{index}")
        ])
    # Assign + Next
    row2 = [
        InlineKeyboardButton(text="📨 Kichik menejerga yuborish", callback_data=f"mgr_inbox_assign_{current_id}")
    ]
    if index < total - 1:
        row2.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"mgr_inbox_next_{index}"))
    rows.append(row2)
    return InlineKeyboardMarkup(inline_keyboard=rows)

def jm_list_keyboard(full_id: str, juniors: list) -> InlineKeyboardMarkup:
    rows = []
    for jm in juniors:
        rows.append([InlineKeyboardButton(text=f"👤 {jm['full_name']}", callback_data=f"mgr_inbox_pick_{full_id}_{jm['id']}")])
    rows.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"mgr_inbox_back_{full_id}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

# === ROUTER ===

def get_manager_inbox_router_min():
    router = Router()
    
    # Role filter qo'shamiz
    # Role guard - both manager and junior_manager can access
    router.message.filter(RoleFilter(["manager", "junior_manager"]))
    router.callback_query.filter(RoleFilter(["manager", "junior_manager"]))

    @router.message(F.text.in_(["📥 Inbox", "Inbox"]), flags={"block": False})
    async def open_inbox(message: Message, state: FSMContext):
        user = await get_user_by_telegram_id(message.from_user.id)
        if not user or user.get("role") != "manager":
            return
        await state.update_data(inbox=MOCK_REQUESTS.copy(), idx=0)
        items = MOCK_REQUESTS
        text = short_view_text(items[0])
        kb = nav_keyboard(0, len(items), items[0]["id"])
        await message.answer(text, reply_markup=kb, parse_mode="HTML")

    @router.callback_query(F.data.startswith("mgr_inbox_prev_"))
    async def prev_item(cb: CallbackQuery, state: FSMContext):
        await cb.answer()
        data = await state.get_data()
        items = data.get("inbox", [])
        idx = int(cb.data.replace("mgr_inbox_prev_", "")) - 1
        if idx < 0 or idx >= len(items):
            return
        await state.update_data(idx=idx)
        text = short_view_text(items[idx])
        kb = nav_keyboard(idx, len(items), items[idx]["id"])
        await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

    @router.callback_query(F.data.startswith("mgr_inbox_next_"))
    async def next_item(cb: CallbackQuery, state: FSMContext):
        await cb.answer()
        data = await state.get_data()
        items = data.get("inbox", [])
        idx = int(cb.data.replace("mgr_inbox_next_", "")) + 1
        if idx < 0 or idx >= len(items):
            return
        await state.update_data(idx=idx)
        text = short_view_text(items[idx])
        kb = nav_keyboard(idx, len(items), items[idx]["id"])
        await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

    @router.callback_query(F.data.startswith("mgr_inbox_assign_"))
    async def assign_open(cb: CallbackQuery, state: FSMContext):
        await cb.answer()
        full_id = cb.data.replace("mgr_inbox_assign_", "")
        # JM ro'yxatini chiqaramiz
        juniors = await get_users_by_role("junior_manager")
        if not juniors:
            await cb.message.edit_text("Kichik menejerlar topilmadi ❗")
            return
        text = f"👨‍💼 <b>Kichik menejer tanlang</b>\n🆔 {full_id}"
        kb = jm_list_keyboard(full_id, juniors)
        await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

    @router.callback_query(F.data.startswith("mgr_inbox_back_"))
    async def assign_back(cb: CallbackQuery, state: FSMContext):
        await cb.answer()
        data = await state.get_data()
        items = data.get("inbox", [])
        idx = data.get("idx", 0)
        if not items:
            await cb.message.edit_text("📭 Inbox bo'sh")
            return
        text = short_view_text(items[idx])
        kb = nav_keyboard(idx, len(items), items[idx]["id"])
        await cb.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

    @router.callback_query(F.data.startswith("mgr_inbox_pick_"))
    async def assign_pick(cb: CallbackQuery, state: FSMContext):
        await cb.answer()
        # Extract full_id and jm_id from callback data
        # Format: mgr_inbox_pick_{full_id}_{jm_id}
        parts = cb.data.split("_")
        if len(parts) < 5:
            await cb.answer("❌ Invalid callback data format", show_alert=True)
            return
        
        # Reconstruct full_id (everything between "mgr_inbox_pick" and the last part)
        full_id = "_".join(parts[3:-1])
        jm_id = parts[-1]
        
        try:
            jm_id = int(jm_id)
        except ValueError:
            await cb.answer("❌ Invalid junior manager ID", show_alert=True)
            return
        user = await get_user_by_telegram_id(cb.from_user.id)

        # Kichik menejer ma'lumotlarini olamiz
        juniors = await get_users_by_role("junior_manager")
        selected_jm = next((jm for jm in juniors if jm["id"] == jm_id), None)
        if not selected_jm:
            await cb.answer("❌ Kichik menejer topilmadi", show_alert=True)
            return

        # Workflow ni o'tkazamiz (mock)
        engine = MockWorkflowEngine()
        await engine.transition_workflow(
            request_id=full_id,
            action="assign_to_junior_manager",
            role="manager",
            data={"actor_id": user["id"], "junior_manager_id": jm_id, "assigned_at": datetime.now().isoformat()},
        )

        # Tasdiq xabarini ko'rsatamiz
        short_id = f"{full_id.split('_')[0]}-{full_id.split('_')[1]}"
        confirmation_text = (
            f"✅ <b>Ariza muvaffaqiyatli yuborildi!</b>\n\n"
            f"🆔 <b>Ariza ID:</b> {short_id}\n"
            f"👤 <b>Kichik menejer:</b> {selected_jm['full_name']}\n"
            f"📅 <b>Yuborilgan vaqt:</b> {fmt_dt(datetime.now())}\n"
            f"👨‍💼 <b>Yuboruvchi:</b> {user.get('full_name', 'Manager')}"
        )

        # Tasdiq xabarini ko'rsatamiz va qoldirib qo'yamiz
        await cb.message.edit_text(confirmation_text, parse_mode="HTML")

        # Ariza ro'yxatidan olib tashlaymiz (lekin xabarni o'zgartirmaymiz)
        data = await state.get_data()
        items = data.get("inbox", [])
        items = [it for it in items if it["id"] != full_id]
        await state.update_data(inbox=items)

    return router
