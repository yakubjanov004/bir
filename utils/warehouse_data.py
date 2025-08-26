"""
Warehouse Data Models and Sample Data Generation

This module provides realistic warehouse data models and generates
sample data for export functionality.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Uzbek names for realistic data
UZBEK_NAMES = [
    "Abdullayev Abdulla", "Karimov Karim", "Rahimov Rahim", "Azizov Aziz",
    "Sobirov Sobir", "Umarov Umar", "Yusupov Yusup", "Aliyev Ali",
    "Xolmatov Xolmat", "Tursunov Tursun", "Ismoilov Ismoil", "Rustamov Rustam",
    "Ergashev Ergash", "Nurmatov Nurmat", "Qodirov Qodir", "Mirzayev Mirza",
    "Baxromov Baxrom", "Davlatov Davlat", "Shermatov Shermat", "Normatov Normat"
]

# Equipment and materials
EQUIPMENT_ITEMS = [
    {"name": "Router TP-Link Archer C6", "unit": "dona", "price": 280000, "category": "Tarmoq uskunalari"},
    {"name": "Router MikroTik hAP ac2", "unit": "dona", "price": 450000, "category": "Tarmoq uskunalari"},
    {"name": "Switch D-Link DGS-1008D", "unit": "dona", "price": 185000, "category": "Tarmoq uskunalari"},
    {"name": "Switch TP-Link TL-SG108", "unit": "dona", "price": 220000, "category": "Tarmoq uskunalari"},
    {"name": "Kabel UTP Cat6 (305m)", "unit": "rulon", "price": 850000, "category": "Kabellar"},
    {"name": "Kabel FTP Cat5e (305m)", "unit": "rulon", "price": 650000, "category": "Kabellar"},
    {"name": "RJ45 konnektori", "unit": "quti (100 dona)", "price": 45000, "category": "Kichik jihozlar"},
    {"name": "Optik kabel SM 4 core", "unit": "metr", "price": 8500, "category": "Optik kabellar"},
    {"name": "ONU GPON ZTE F660", "unit": "dona", "price": 380000, "category": "Optik uskunalar"},
    {"name": "WiFi adapter USB", "unit": "dona", "price": 65000, "category": "Kichik jihozlar"},
    {"name": "Antenna 2.4GHz 9dBi", "unit": "dona", "price": 95000, "category": "Antennalar"},
    {"name": "Antenna 5GHz 16dBi", "unit": "dona", "price": 145000, "category": "Antennalar"},
    {"name": "Crimping tool", "unit": "dona", "price": 125000, "category": "Asboblar"},
    {"name": "Cable tester", "unit": "dona", "price": 85000, "category": "Asboblar"},
    {"name": "Patch cord 1m", "unit": "dona", "price": 15000, "category": "Kichik jihozlar"},
    {"name": "Patch cord 3m", "unit": "dona", "price": 25000, "category": "Kichik jihozlar"},
    {"name": "TV Set-top box", "unit": "dona", "price": 320000, "category": "TV uskunalari"},
    {"name": "HDMI kabel 2m", "unit": "dona", "price": 35000, "category": "Kabellar"},
    {"name": "Power adapter 12V 2A", "unit": "dona", "price": 45000, "category": "Quvvat manbalari"},
    {"name": "UPS 650VA", "unit": "dona", "price": 580000, "category": "Quvvat manbalari"}
]

# Service types
SERVICE_TYPES = [
    "Internet ulanish (GPON)",
    "Internet ulanish (Ethernet)",
    "TV ulanish",
    "Internet + TV komplekt",
    "Internet tezligini oshirish",
    "Modem almashtirish",
    "Kabel o'tkazish",
    "Nosozlikni bartaraf etish"
]

# Districts in Tashkent
DISTRICTS = [
    "Yunusobod tumani", "Chilonzor tumani", "Mirzo Ulug'bek tumani",
    "Yakkasaroy tumani", "Shayxontohur tumani", "Olmazor tumani",
    "Uchtepa tumani", "Bektemir tumani", "Sergeli tumani",
    "Yashnobod tumani", "Mirobod tumani", "Hamza tumani"
]

def generate_inventory_data(count: int = 50) -> List[Dict[str, Any]]:
    """Generate realistic inventory data"""
    inventory = []
    
    for i in range(count):
        item = random.choice(EQUIPMENT_ITEMS)
        initial_quantity = random.randint(10, 200)
        used_quantity = random.randint(0, initial_quantity // 2)
        
        inventory_item = {
            "id": f"INV-{2024000 + i:06d}",
            "name": item["name"],
            "category": item["category"],
            "unit": item["unit"],
            "initial_quantity": initial_quantity,
            "current_quantity": initial_quantity - used_quantity,
            "reserved_quantity": random.randint(0, 10),
            "unit_price": item["price"],
            "total_value": (initial_quantity - used_quantity) * item["price"],
            "min_stock": random.randint(5, 20),
            "location": f"A{random.randint(1, 5)}-{random.randint(1, 10):02d}",
            "last_updated": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M"),
            "status": "Yetarli" if (initial_quantity - used_quantity) > 20 else "Kam qolgan"
        }
        inventory.append(inventory_item)
    
    return inventory

def generate_issued_items_data(count: int = 100) -> List[Dict[str, Any]]:
    """Generate realistic issued items data"""
    issued_items = []
    technicians = [f"Texnik-{i:02d}" for i in range(1, 11)]
    
    for i in range(count):
        item = random.choice(EQUIPMENT_ITEMS)
        quantity = random.randint(1, 10) if "dona" in item["unit"] else random.randint(10, 100)
        order_id = f"ORD-{2024000 + random.randint(1000, 9999):06d}"
        
        issued_item = {
            "id": f"ISS-{2024000 + i:06d}",
            "order_id": order_id,
            "item_name": item["name"],
            "category": item["category"],
            "quantity": f"{quantity} {item['unit']}",
            "unit_price": item["price"],
            "total_price": quantity * item["price"],
            "technician": random.choice(technicians),
            "client_name": random.choice(UZBEK_NAMES),
            "client_address": f"{random.choice(DISTRICTS)}, {random.randint(1, 200)}-uy",
            "service_type": random.choice(SERVICE_TYPES),
            "issued_date": (datetime.now() - timedelta(days=random.randint(0, 60))).strftime("%Y-%m-%d"),
            "issued_time": f"{random.randint(8, 18):02d}:{random.randint(0, 59):02d}",
            "return_status": random.choice(["Qaytarilmagan", "Qisman qaytarilgan", "To'liq qaytarilgan"]),
            "notes": random.choice(["", "Shoshilinch", "Mijoz kutmoqda", "Qo'shimcha material kerak"])
        }
        issued_items.append(issued_item)
    
    return issued_items

def generate_orders_data(count: int = 80) -> List[Dict[str, Any]]:
    """Generate realistic orders data"""
    orders = []
    statuses = ["Yangi", "Qabul qilingan", "Jarayonda", "Bajarilgan", "Bekor qilingan"]
    status_weights = [15, 20, 25, 35, 5]
    
    for i in range(count):
        order_date = datetime.now() - timedelta(days=random.randint(0, 90))
        status = random.choices(statuses, weights=status_weights)[0]
        
        order = {
            "id": f"ORD-{2024000 + i:06d}",
            "client_name": random.choice(UZBEK_NAMES),
            "phone": f"+99890{random.randint(1000000, 9999999)}",
            "address": f"{random.choice(DISTRICTS)}, {random.randint(1, 200)}-uy, {random.randint(1, 100)}-xonadon",
            "service_type": random.choice(SERVICE_TYPES),
            "status": status,
            "priority": random.choice(["Oddiy", "Muhim", "Shoshilinch"]),
            "created_date": order_date.strftime("%Y-%m-%d"),
            "created_time": f"{random.randint(8, 20):02d}:{random.randint(0, 59):02d}",
            "scheduled_date": (order_date + timedelta(days=random.randint(1, 3))).strftime("%Y-%m-%d"),
            "scheduled_time": f"{random.randint(9, 18):02d}:00",
            "technician": f"Texnik-{random.randint(1, 10):02d}" if status in ["Jarayonda", "Bajarilgan"] else "-",
            "completion_date": (order_date + timedelta(days=random.randint(1, 5))).strftime("%Y-%m-%d") if status == "Bajarilgan" else "-",
            "materials_used": "Router, Kabel 20m, RJ45 4 dona" if status == "Bajarilgan" else "-",
            "total_cost": random.randint(50000, 500000) if status == "Bajarilgan" else 0,
            "payment_status": "To'langan" if status == "Bajarilgan" else "Kutilmoqda",
            "notes": random.choice(["", "Mijoz uyda yo'q edi", "Qo'shimcha material kerak", "Texnik muammo"])
        }
        orders.append(order)
    
    return orders

def generate_statistics_data() -> Dict[str, Any]:
    """Generate realistic statistics data"""
    today = datetime.now()
    
    stats = {
        "period": f"{(today - timedelta(days=30)).strftime('%Y-%m-%d')} - {today.strftime('%Y-%m-%d')}",
        "general_stats": {
            "total_orders": random.randint(800, 1200),
            "completed_orders": random.randint(600, 900),
            "in_progress_orders": random.randint(50, 150),
            "new_orders": random.randint(20, 80),
            "cancelled_orders": random.randint(10, 50),
            "total_revenue": random.randint(50000000, 150000000),
            "average_order_value": random.randint(150000, 350000),
            "customer_satisfaction": f"{random.randint(85, 98)}%"
        },
        "inventory_stats": {
            "total_items": random.randint(40, 60),
            "low_stock_items": random.randint(5, 15),
            "out_of_stock_items": random.randint(0, 5),
            "total_inventory_value": random.randint(20000000, 50000000),
            "most_used_item": "Kabel UTP Cat6",
            "least_used_item": "UPS 650VA"
        },
        "technician_performance": [
            {
                "technician": f"Texnik-{i:02d}",
                "completed_orders": random.randint(40, 100),
                "average_time": f"{random.randint(1, 3)}s {random.randint(0, 59)}d",
                "customer_rating": f"{random.uniform(4.0, 5.0):.1f}",
                "materials_efficiency": f"{random.randint(85, 98)}%"
            }
            for i in range(1, 11)
        ],
        "daily_orders": [
            {
                "date": (today - timedelta(days=i)).strftime("%Y-%m-%d"),
                "new_orders": random.randint(20, 50),
                "completed_orders": random.randint(15, 45),
                "revenue": random.randint(1500000, 5000000)
            }
            for i in range(30)
        ],
        "service_distribution": {
            service: random.randint(50, 200)
            for service in SERVICE_TYPES
        }
    }
    
    return stats

def get_export_headers(export_type: str) -> List[str]:
    """Get headers for each export type"""
    headers = {
        "inventory": [
            "ID", "Mahsulot nomi", "Kategoriya", "O'lchov birligi",
            "Boshlang'ich miqdor", "Joriy miqdor", "Band qilingan",
            "Birlik narxi", "Umumiy qiymat", "Min. zaxira",
            "Joylashuv", "Oxirgi yangilanish", "Holat"
        ],
        "issued_items": [
            "ID", "Buyurtma ID", "Material nomi", "Kategoriya",
            "Miqdor", "Birlik narxi", "Umumiy narx", "Texnik",
            "Mijoz", "Manzil", "Xizmat turi", "Berilgan sana",
            "Berilgan vaqt", "Qaytarish holati", "Izoh"
        ],
        "orders": [
            "ID", "Mijoz", "Telefon", "Manzil", "Xizmat turi",
            "Holat", "Muhimlik", "Yaratilgan sana", "Yaratilgan vaqt",
            "Rejalashtirilgan sana", "Rejalashtirilgan vaqt", "Texnik",
            "Bajarilgan sana", "Ishlatilgan materiallar", "Umumiy narx",
            "To'lov holati", "Izohlar"
        ],
        "statistics": [
            "Ko'rsatkich", "Qiymat", "O'zgarish", "Tavsif"
        ]
    }
    return headers.get(export_type, [])