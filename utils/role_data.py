"""
Role-specific Data Generation Module

This module provides data generation functions for each role's export functionality.
Each role has its own specific data structure and content.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from faker import Faker

fake = Faker(['uz_UZ', 'ru_RU'])

# Export limits for performance
MAX_EXPORT_ROWS = 1000  # Maximum rows for single export

# Common data pools
TECHNICIAN_NAMES = [
    "Sardor Rahimov", "Jasur Karimov", "Sherzod Toshmatov", "Dilshod Yuldashev",
    "Rustam Abdullayev", "Kamol Saidov", "Bahodir Nazarov", "Umid Qodirov",
    "Shohruh Mirzayev", "Farrux Rahmonov", "Aziz Ergashev", "Bobur Hasanov"
]

OPERATOR_NAMES = [
    "Malika Rahimova", "Gulnora Karimova", "Dilnoza Yuldasheva", "Shaxnoza Saidova",
    "Nodira Nazarova", "Umida Qodirova", "Zulfiya Mirzayeva", "Feruza Rahmonova"
]

SERVICE_TYPES = ["Internet", "TV", "Telefon", "Kompleks"]
PRIORITIES = ["Oddiy", "Muhim", "Shoshilinch"]
STATUSES = ["Yangi", "Jarayonda", "Bajarilgan", "Bekor qilingan", "Kutilmoqda"]

REGIONS = [
    "Toshkent shahri", "Toshkent viloyati", "Samarqand", "Buxoro", "Andijon",
    "Farg'ona", "Namangan", "Qashqadaryo", "Surxondaryo", "Xorazm", "Navoiy"
]

EQUIPMENT_TYPES = [
    "Router", "Modem", "TV Box", "Kabel (100m)", "Kabel (50m)", "Splitter",
    "Connector RJ45", "Connector F-type", "Switch", "Optical converter"
]

# Manager Role Data
def generate_manager_orders_data(count: int = 100) -> List[Dict[str, Any]]:
    """Generate orders data for Manager role"""
    orders = []
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(count):
        order_date = start_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        status = random.choice(STATUSES)
        
        order = {
            "id": f"Z-{1000 + i}",
            "client_name": fake.name(),
            "client_phone": f"+998{random.randint(90, 99)}{random.randint(1000000, 9999999)}",
            "address": f"{random.choice(REGIONS)}, {fake.street_address()}",
            "service_type": random.choice(SERVICE_TYPES),
            "priority": random.choice(PRIORITIES),
            "status": status,
            "technician": random.choice(TECHNICIAN_NAMES) if status != "Yangi" else "-",
            "created_date": order_date.strftime("%Y-%m-%d %H:%M"),
            "completed_date": (order_date + timedelta(hours=random.randint(2, 48))).strftime("%Y-%m-%d %H:%M") if status == "Bajarilgan" else "-",
            "comment": fake.sentence() if random.random() > 0.5 else "-",
            "amount": f"{random.randint(50, 500) * 1000:,} so'm" if status == "Bajarilgan" else "-"
        }
        orders.append(order)
    
    return sorted(orders, key=lambda x: x["created_date"], reverse=True)

def generate_manager_statistics_data() -> Dict[str, Any]:
    """Generate statistics data for Manager role"""
    return {
        "orders": {
            "total": 2547,
            "new": 156,
            "in_progress": 234,
            "completed": 1987,
            "cancelled": 170
        },
        "technicians": {
            "total": 45,
            "active": 38,
            "on_leave": 5,
            "inactive": 2,
            "average_orders_per_day": 12.5
        },
        "performance": {
            "completion_rate": "78.1%",
            "average_completion_time": "4.2 soat",
            "customer_satisfaction": "4.3/5.0",
            "on_time_completion": "82.5%"
        },
        "revenue": {
            "monthly_total": "245,678,000 so'm",
            "daily_average": "8,189,267 so'm",
            "per_order_average": "123,567 so'm",
            "growth_rate": "+15.3%"
        }
    }

def generate_manager_users_data(count: int = 50) -> List[Dict[str, Any]]:
    """Generate users/staff data for Manager role"""
    users = []
    roles = ["Texnik", "Operator", "Supervisor", "Koordinator"]
    
    for i in range(count):
        role = random.choice(roles)
        name = random.choice(TECHNICIAN_NAMES if role == "Texnik" else OPERATOR_NAMES)
        
        user = {
            "id": f"U-{100 + i}",
            "name": name,
            "role": role,
            "phone": f"+998{random.randint(90, 99)}{random.randint(1000000, 9999999)}",
            "region": random.choice(REGIONS),
            "status": random.choice(["Faol", "Band", "Ta'tilda"]),
            "orders_completed": random.randint(50, 500),
            "rating": f"{random.uniform(3.5, 5.0):.1f}",
            "joined_date": (datetime.now() - timedelta(days=random.randint(30, 730))).strftime("%Y-%m-%d"),
            "last_active": (datetime.now() - timedelta(hours=random.randint(0, 48))).strftime("%Y-%m-%d %H:%M")
        }
        users.append(user)
    
    return sorted(users, key=lambda x: x["name"])

def generate_manager_reports_data() -> Dict[str, Any]:
    """Generate reports data for Manager role"""
    return {
        "daily_report": {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "new_orders": 45,
            "completed_orders": 38,
            "cancelled_orders": 3,
            "revenue": "3,456,000 so'm",
            "active_technicians": 32,
            "average_completion_time": "3.8 soat"
        },
        "weekly_report": {
            "week": f"{datetime.now().isocalendar()[1]}-hafta",
            "total_orders": 312,
            "completion_rate": "81.4%",
            "top_technician": "Sardor Rahimov (45 buyurtma)",
            "top_region": "Toshkent shahri (125 buyurtma)",
            "total_revenue": "38,456,000 so'm"
        },
        "monthly_report": {
            "month": datetime.now().strftime("%B %Y"),
            "total_orders": 1245,
            "new_clients": 234,
            "returning_clients": 1011,
            "average_order_value": "145,000 so'm",
            "customer_complaints": 23,
            "resolved_complaints": 20
        }
    }

# Controller Role Data
def generate_controller_orders_data(count: int = 120) -> List[Dict[str, Any]]:
    """Generate orders data for Controller role with quality metrics"""
    orders = []
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(count):
        order_date = start_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        status = random.choice(STATUSES)
        
        order = {
            "id": f"Z-{2000 + i}",
            "client_name": fake.name(),
            "client_phone": f"+998{random.randint(90, 99)}{random.randint(1000000, 9999999)}",
            "address": f"{random.choice(REGIONS)}, {fake.street_address()}",
            "service_type": random.choice(SERVICE_TYPES),
            "priority": random.choice(PRIORITIES),
            "status": status,
            "technician": random.choice(TECHNICIAN_NAMES) if status != "Yangi" else "-",
            "created_date": order_date.strftime("%Y-%m-%d %H:%M"),
            "quality_score": f"{random.uniform(3.0, 5.0):.1f}" if status == "Bajarilgan" else "-",
            "completion_time": f"{random.uniform(1.5, 8.0):.1f} soat" if status == "Bajarilgan" else "-",
            "client_feedback": random.choice(["Juda yaxshi", "Yaxshi", "Qoniqarli", "Yomon"]) if status == "Bajarilgan" else "-",
            "issues_found": random.randint(0, 3) if status == "Bajarilgan" else 0
        }
        orders.append(order)
    
    return sorted(orders, key=lambda x: x["created_date"], reverse=True)

def generate_controller_quality_data() -> Dict[str, Any]:
    """Generate quality control data for Controller role"""
    return {
        "overall_metrics": {
            "average_quality_score": 4.2,
            "total_inspections": 456,
            "passed_inspections": 412,
            "failed_inspections": 44,
            "pass_rate": "90.4%"
        },
        "technician_performance": [
            {"name": name, "score": round(random.uniform(3.5, 5.0), 1), "orders": random.randint(20, 50)}
            for name in TECHNICIAN_NAMES[:10]
        ],
        "common_issues": [
            {"issue": "Kabel noto'g'ri o'rnatilgan", "count": 23, "percentage": "12.5%"},
            {"issue": "Router sozlamalari xato", "count": 18, "percentage": "9.8%"},
            {"issue": "Hujjatlar to'liq emas", "count": 15, "percentage": "8.2%"},
            {"issue": "Vaqtida bajarilmagan", "count": 12, "percentage": "6.5%"},
            {"issue": "Mijoz shikoyati", "count": 8, "percentage": "4.3%"}
        ],
        "regional_quality": [
            {"region": region, "score": round(random.uniform(3.8, 4.8), 1), "orders": random.randint(50, 200)}
            for region in REGIONS[:5]
        ]
    }

def generate_controller_technicians_data(count: int = 45) -> List[Dict[str, Any]]:
    """Generate technicians data for Controller role"""
    technicians = []
    
    for i, name in enumerate(TECHNICIAN_NAMES):
        if i >= count:
            break
            
        tech = {
            "id": f"T-{200 + i}",
            "name": name,
            "phone": f"+998{random.randint(90, 99)}{random.randint(1000000, 9999999)}",
            "region": random.choice(REGIONS),
            "specialization": random.choice(["Internet", "TV", "Universal"]),
            "status": random.choice(["Faol", "Band", "Ta'tilda", "Offline"]),
            "current_orders": random.randint(0, 5),
            "completed_today": random.randint(0, 8),
            "quality_score": f"{random.uniform(3.5, 5.0):.1f}",
            "efficiency_rate": f"{random.uniform(70, 95):.1f}%",
            "last_inspection": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
        }
        technicians.append(tech)
    
    return sorted(technicians, key=lambda x: float(x["quality_score"]), reverse=True)

# Call Center Supervisor Role Data
def generate_ccs_orders_data(count: int = 150) -> List[Dict[str, Any]]:
    """Generate orders data for Call Center Supervisor role"""
    orders = []
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(count):
        order_date = start_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        
        order = {
            "id": f"Z-{3000 + i}",
            "client_name": fake.name(),
            "client_phone": f"+998{random.randint(90, 99)}{random.randint(1000000, 9999999)}",
            "operator": random.choice(OPERATOR_NAMES),
            "service_type": random.choice(SERVICE_TYPES),
            "priority": random.choice(PRIORITIES),
            "status": random.choice(STATUSES),
            "created_date": order_date.strftime("%Y-%m-%d %H:%M"),
            "call_duration": f"{random.randint(30, 600)} sekund",
            "call_quality": random.choice(["A'lo", "Yaxshi", "O'rtacha", "Yomon"]),
            "client_mood": random.choice(["Juda mamnun", "Mamnun", "Neytral", "Norozi"]),
            "follow_up_required": random.choice(["Ha", "Yo'q"])
        }
        orders.append(order)
    
    return sorted(orders, key=lambda x: x["created_date"], reverse=True)

def generate_ccs_users_data(count: int = 30) -> List[Dict[str, Any]]:
    """Generate call center staff data for Call Center Supervisor role"""
    staff = []
    
    for i in range(count):
        operator = {
            "id": f"O-{300 + i}",
            "name": random.choice(OPERATOR_NAMES),
            "phone": f"+998{random.randint(90, 99)}{random.randint(1000000, 9999999)}",
            "shift": random.choice(["Ertalab", "Kunduz", "Kechqurun"]),
            "status": random.choice(["Online", "Tanaffus", "Offline", "Training"]),
            "calls_today": random.randint(20, 80),
            "avg_call_time": f"{random.randint(120, 300)} sekund",
            "satisfaction_rate": f"{random.uniform(3.5, 5.0):.1f}/5.0",
            "orders_created": random.randint(5, 25),
            "complaints_handled": random.randint(0, 5),
            "languages": random.choice(["O'zbek, Rus", "O'zbek", "O'zbek, Rus, Ingliz"])
        }
        staff.append(operator)
    
    return sorted(staff, key=lambda x: x["name"])

def generate_ccs_feedback_data(count: int = 50) -> List[Dict[str, Any]]:
    """Generate customer feedback data for Call Center Supervisor role"""
    feedback_list = []
    
    for i in range(count):
        feedback = {
            "id": f"F-{400 + i}",
            "client_name": fake.name(),
            "order_id": f"Z-{random.randint(1000, 3000)}",
            "operator": random.choice(OPERATOR_NAMES),
            "date": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M"),
            "rating": random.randint(1, 5),
            "category": random.choice(["Xizmat sifati", "Operator muomalasi", "Texnik masala", "Narx", "Boshqa"]),
            "comment": fake.sentence(),
            "status": random.choice(["Yangi", "Ko'rib chiqilmoqda", "Hal qilindi", "Yopildi"]),
            "response_time": f"{random.randint(5, 120)} daqiqa",
            "resolution": random.choice(["Mijoz qoniqdi", "Qisman hal qilindi", "Hal qilinmadi", "-"])
        }
        feedback_list.append(feedback)
    
    return sorted(feedback_list, key=lambda x: x["date"], reverse=True)

def generate_ccs_workflow_data() -> Dict[str, Any]:
    """Generate workflow data for Call Center Supervisor role"""
    return {
        "active_workflows": [
            {
                "id": f"W-{500 + i}",
                "name": f"Workflow {i+1}",
                "type": random.choice(["Yangi mijoz", "Texnik muammo", "Hisob-kitob", "Shikoyat"]),
                "status": "Faol",
                "assigned_operators": random.randint(2, 5),
                "daily_volume": random.randint(20, 100),
                "avg_handling_time": f"{random.randint(5, 30)} daqiqa",
                "sla_compliance": f"{random.uniform(85, 99):.1f}%"
            }
            for i in range(8)
        ],
        "workflow_statistics": {
            "total_active": 8,
            "total_paused": 2,
            "total_operators": 25,
            "average_efficiency": "87.3%",
            "bottlenecks_detected": 3
        }
    }

# Admin Role Data
def generate_admin_users_data(count: int = 100) -> List[Dict[str, Any]]:
    """Generate all system users data for Admin role"""
    users = []
    roles = ["Admin", "Manager", "Controller", "Call Center Supervisor", "Operator", "Texnik", "Warehouse"]
    
    for i in range(count):
        role = random.choice(roles)
        
        user = {
            "id": f"U-{1000 + i}",
            "username": f"user{1000 + i}",
            "full_name": fake.name(),
            "role": role,
            "phone": f"+998{random.randint(90, 99)}{random.randint(1000000, 9999999)}",
            "email": fake.email(),
            "region": random.choice(REGIONS),
            "status": random.choice(["Faol", "Bloklangan", "Ta'tilda"]),
            "created_date": (datetime.now() - timedelta(days=random.randint(30, 730))).strftime("%Y-%m-%d"),
            "last_login": (datetime.now() - timedelta(hours=random.randint(0, 168))).strftime("%Y-%m-%d %H:%M"),
            "permissions": random.choice(["To'liq", "Cheklangan", "Faqat ko'rish"])
        }
        users.append(user)
    
    return sorted(users, key=lambda x: x["created_date"], reverse=True)

def generate_admin_system_data() -> Dict[str, Any]:
    """Generate system settings and configuration data for Admin role"""
    return {
        "system_info": {
            "version": "2.5.1",
            "last_update": "2024-01-15",
            "database_size": "45.6 GB",
            "active_sessions": 234,
            "uptime": "45 kun 12 soat",
            "server_load": "34%"
        },
        "configurations": {
            "max_users": 500,
            "session_timeout": "30 daqiqa",
            "backup_frequency": "Kunlik",
            "last_backup": datetime.now().strftime("%Y-%m-%d 03:00"),
            "api_rate_limit": "1000 so'rov/soat",
            "maintenance_mode": "O'chirilgan"
        },
        "integrations": [
            {"name": "SMS Gateway", "status": "Faol", "requests_today": 4567},
            {"name": "Payment System", "status": "Faol", "transactions_today": 234},
            {"name": "Email Service", "status": "Faol", "emails_sent": 1234},
            {"name": "Backup Service", "status": "Faol", "last_run": "3 soat oldin"}
        ],
        "security_settings": {
            "two_factor_auth": "Majburiy",
            "password_policy": "Kuchli (8+ belgi)",
            "login_attempts": 3,
            "ip_whitelist": "Yoqilgan",
            "ssl_certificate": "Valid until 2025-03-15"
        }
    }

def generate_admin_logs_data(count: int = 200) -> List[Dict[str, Any]]:
    """Generate system logs data for Admin role"""
    logs = []
    log_types = ["Login", "Logout", "Error", "Warning", "Info", "Security", "API", "Database"]
    log_levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
    
    for i in range(count):
        log_time = datetime.now() - timedelta(minutes=random.randint(0, 10080))  # Last week
        
        log = {
            "id": f"L-{10000 + i}",
            "timestamp": log_time.strftime("%Y-%m-%d %H:%M:%S"),
            "type": random.choice(log_types),
            "level": random.choice(log_levels),
            "user": random.choice(["system", f"user{random.randint(1000, 2000)}"]),
            "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "action": fake.sentence(nb_words=6),
            "details": fake.sentence() if random.random() > 0.5 else "-",
            "duration": f"{random.randint(10, 5000)} ms"
        }
        logs.append(log)
    
    return sorted(logs, key=lambda x: x["timestamp"], reverse=True)

# Warehouse Role Data (keeping existing structure)
def generate_warehouse_inventory_data(count: int = 100) -> List[Dict[str, Any]]:
    """Generate inventory data for Warehouse role"""
    inventory = []
    
    for i in range(count):
        current_qty = random.randint(0, 1000)
        reserved_qty = random.randint(0, min(current_qty, 100))
        unit_price = random.randint(10000, 500000)
        
        item = {
            "id": f"INV-{5000 + i}",
            "name": random.choice(EQUIPMENT_TYPES),
            "category": random.choice(["Tarmoq uskunalari", "Kabellar", "Ulagichlar", "Yordamchi"]),
            "unit": random.choice(["dona", "metr", "komplekt"]),
            "initial_quantity": random.randint(100, 1500),
            "current_quantity": current_qty,
            "reserved_quantity": reserved_qty,
            "available_quantity": current_qty - reserved_qty,
            "unit_price": unit_price,
            "total_value": current_qty * unit_price,
            "min_stock": random.randint(10, 50),
            "location": f"{random.choice(['A', 'B', 'C'])}-{random.randint(1, 20)}",
            "last_updated": (datetime.now() - timedelta(days=random.randint(0, 7))).strftime("%Y-%m-%d"),
            "status": "Yetarli" if current_qty > 50 else "Kam" if current_qty > 10 else "Tugagan"
        }
        inventory.append(item)
    
    return sorted(inventory, key=lambda x: x["name"])

def generate_warehouse_issued_items_data(count: int = 150) -> List[Dict[str, Any]]:
    """Generate issued items data for Warehouse role"""
    issued_items = []
    
    for i in range(count):
        quantity = random.randint(1, 50)
        unit_price = random.randint(10000, 500000)
        
        item = {
            "id": f"ISS-{6000 + i}",
            "order_id": f"Z-{random.randint(1000, 5000)}",
            "item_name": random.choice(EQUIPMENT_TYPES),
            "category": random.choice(["Tarmoq uskunalari", "Kabellar", "Ulagichlar"]),
            "quantity": quantity,
            "unit_price": unit_price,
            "total_price": quantity * unit_price,
            "technician": random.choice(TECHNICIAN_NAMES),
            "client_name": fake.name(),
            "client_address": f"{random.choice(REGIONS)}, {fake.street_address()}",
            "issue_date": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M"),
            "return_date": "-",
            "status": random.choice(["Berildi", "Qaytarildi", "Yo'qolgan", "Shikastlangan"])
        }
        issued_items.append(item)
    
    return sorted(issued_items, key=lambda x: x["issue_date"], reverse=True)

def generate_warehouse_statistics_data() -> Dict[str, Any]:
    """Generate statistics data for Warehouse role"""
    return {
        "inventory_summary": {
            "total_items": 156,
            "total_value": "567,890,000 so'm",
            "low_stock_items": 23,
            "out_of_stock_items": 5,
            "categories": 8
        },
        "movement_statistics": {
            "items_received_today": 45,
            "items_issued_today": 67,
            "pending_orders": 12,
            "returns_today": 3,
            "damaged_items": 2
        },
        "top_items": [
            {"name": "Router TP-Link", "issued": 234, "remaining": 45},
            {"name": "Kabel UTP Cat6", "issued": 1200, "remaining": 300},
            {"name": "TV Box", "issued": 156, "remaining": 78},
            {"name": "Connector RJ45", "issued": 3456, "remaining": 1234},
            {"name": "Splitter 1:8", "issued": 89, "remaining": 23}
        ],
        "monthly_trends": {
            "total_issued": 4567,
            "total_received": 3456,
            "total_value_issued": "234,567,000 so'm",
            "efficiency_rate": "94.5%"
        }
    }

# Export headers for each data type
def get_export_headers(export_type: str, role: str = None) -> List[str]:
    """Get appropriate headers based on export type and role"""
    headers_map = {
        # Manager headers
        "manager_orders": ["ID", "Mijoz", "Telefon", "Manzil", "Xizmat turi", "Ustunlik", "Holat", "Texnik", "Yaratilgan", "Tugatilgan", "Izoh", "Summa"],
        "manager_statistics": ["Ko'rsatkich", "Qiymat", "O'zgarish", "Davr"],
        "manager_users": ["ID", "Ism", "Lavozim", "Telefon", "Hudud", "Holat", "Bajarilgan", "Reyting", "Qo'shilgan", "Oxirgi faollik"],
        "manager_reports": ["Hisobot turi", "Ko'rsatkich", "Qiymat", "Taqqoslash"],
        
        # Controller headers
        "controller_orders": ["ID", "Mijoz", "Telefon", "Manzil", "Xizmat", "Ustunlik", "Holat", "Texnik", "Yaratilgan", "Sifat", "Vaqt", "Fikr", "Muammolar"],
        "controller_quality": ["Ko'rsatkich", "Qiymat", "Foiz", "Trend"],
        "controller_users": ["ID", "Ism", "Telefon", "Hudud", "Mutaxassislik", "Holat", "Joriy", "Bugun", "Sifat", "Samaradorlik", "Oxirgi tekshiruv"],
        
        # Call Center Supervisor headers
        "ccs_orders": ["ID", "Mijoz", "Telefon", "Operator", "Xizmat", "Ustunlik", "Holat", "Yaratilgan", "Qo'ng'iroq vaqti", "Sifat", "Mijoz kayfiyati", "Kuzatish"],
        "ccs_users": ["ID", "Ism", "Telefon", "Smena", "Holat", "Bugungi qo'ng'iroqlar", "O'rtacha vaqt", "Qoniqish", "Buyurtmalar", "Shikoyatlar", "Tillar"],
        "ccs_feedback": ["ID", "Mijoz", "Buyurtma", "Operator", "Sana", "Reyting", "Kategoriya", "Izoh", "Holat", "Javob vaqti", "Yechim"],
        "ccs_workflow": ["ID", "Nomi", "Turi", "Holat", "Operatorlar", "Kunlik hajm", "O'rtacha vaqt", "SLA"],
        
        # Admin headers
        "admin_users": ["ID", "Username", "To'liq ism", "Lavozim", "Telefon", "Email", "Hudud", "Holat", "Yaratilgan", "Oxirgi kirish", "Ruxsatlar"],
        "admin_orders": ["ID", "Mijoz", "Telefon", "Manzil", "Xizmat", "Holat", "Yaratilgan", "Operator", "Texnik", "Summa"],
        "admin_system": ["Parametr", "Qiymat", "Holat", "Oxirgi yangilanish"],
        "admin_logs": ["ID", "Vaqt", "Turi", "Daraja", "Foydalanuvchi", "IP", "Harakat", "Tafsilotlar", "Davomiylik"],
        
        # Warehouse headers
        "warehouse_inventory": ["ID", "Nomi", "Kategoriya", "Birlik", "Boshlang'ich", "Joriy", "Band", "Mavjud", "Narx", "Umumiy qiymat", "Min zahira", "Joylashuv", "Yangilangan", "Holat"],
        "warehouse_issued": ["ID", "Buyurtma", "Nomi", "Kategoriya", "Miqdor", "Narx", "Umumiy", "Texnik", "Mijoz", "Manzil", "Berilgan", "Qaytarilgan", "Holat"],
        "warehouse_statistics": ["Ko'rsatkich", "Qiymat", "O'zgarish", "Davr"],
        
        # Default
        "orders": ["ID", "Mijoz", "Telefon", "Manzil", "Xizmat", "Holat", "Yaratilgan"],
        "statistics": ["Ko'rsatkich", "Qiymat", "O'zgarish", "Davr"],
        "users": ["ID", "Ism", "Lavozim", "Telefon", "Holat"]
    }
    
    # Build key based on role and export type
    if role:
        key = f"{role}_{export_type}"
        if key in headers_map:
            return headers_map[key]
    
    # Fallback to export type only
    return headers_map.get(export_type, headers_map.get("orders"))

# Main data generation function
def get_role_data(role: str, export_type: str) -> tuple:
    """Get data and headers for specific role and export type"""
    
    # Manager role
    if role == "manager":
        if export_type == "orders":
            return generate_manager_orders_data(), get_export_headers("manager_orders")
        elif export_type == "statistics":
            return generate_manager_statistics_data(), get_export_headers("manager_statistics")
        elif export_type == "users":
            return generate_manager_users_data(), get_export_headers("manager_users")
        elif export_type == "reports":
            return generate_manager_reports_data(), get_export_headers("manager_reports")
    
    # Controller role
    elif role == "controller":
        if export_type == "orders":
            return generate_controller_orders_data(), get_export_headers("controller_orders")
        elif export_type == "quality":
            return generate_controller_quality_data(), get_export_headers("controller_quality")
        elif export_type == "users" or export_type == "technicians":
            return generate_controller_technicians_data(), get_export_headers("controller_users")
        elif export_type == "statistics":
            return generate_controller_quality_data(), get_export_headers("controller_quality")
    
    # Call Center Supervisor role
    elif role == "call_center_supervisor":
        if export_type == "orders":
            return generate_ccs_orders_data(), get_export_headers("ccs_orders")
        elif export_type == "users":
            return generate_ccs_users_data(), get_export_headers("ccs_users")
        elif export_type == "feedback":
            return generate_ccs_feedback_data(), get_export_headers("ccs_feedback")
        elif export_type == "workflow":
            return generate_ccs_workflow_data(), get_export_headers("ccs_workflow")
        elif export_type == "statistics":
            return {
                "orders": generate_ccs_orders_data(20),
                "feedback": generate_ccs_feedback_data(10),
                "workflow": generate_ccs_workflow_data()
            }, get_export_headers("statistics")
    
    # Admin role
    elif role == "admin":
        if export_type == "users":
            return generate_admin_users_data(), get_export_headers("admin_users")
        elif export_type == "orders":
            return generate_manager_orders_data(200), get_export_headers("admin_orders")  # Reuse manager orders with more data
        elif export_type == "system":
            return generate_admin_system_data(), get_export_headers("admin_system")
        elif export_type == "logs":
            return generate_admin_logs_data(), get_export_headers("admin_logs")
        elif export_type == "statistics":
            return {
                "users": len(generate_admin_users_data(10)),
                "orders": len(generate_manager_orders_data(10)),
                "system": generate_admin_system_data(),
                "recent_logs": generate_admin_logs_data(5)
            }, get_export_headers("statistics")
    
    # Warehouse role
    elif role == "warehouse":
        if export_type == "inventory":
            return generate_warehouse_inventory_data(), get_export_headers("warehouse_inventory")
        elif export_type == "issued_items":
            return generate_warehouse_issued_items_data(), get_export_headers("warehouse_issued")
        elif export_type == "orders":
            return generate_warehouse_issued_items_data(), get_export_headers("warehouse_issued")
        elif export_type == "statistics":
            return generate_warehouse_statistics_data(), get_export_headers("warehouse_statistics")
    
    # Default fallback
    return generate_manager_orders_data(50), get_export_headers("orders")

def validate_export_data(data: Any, headers: List[str]) -> bool:
    """Validate export data before processing"""
    if not data:
        return False
    
    if isinstance(data, list):
        # Check if list is not empty and items are dictionaries
        if not data or not all(isinstance(item, dict) for item in data):
            return False
        # Check if all items have consistent keys
        if data:
            first_keys = set(data[0].keys())
            return all(set(item.keys()) == first_keys for item in data)
    
    elif isinstance(data, dict):
        # Check if dictionary is not empty
        return bool(data)
    
    return True