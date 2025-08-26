"""
Message builder functions for real-time monitoring.
"""

from datetime import datetime
from typing import List, Dict, Any

def calculate_time_duration(start_time: datetime, end_time: datetime = None) -> str:
    """Calculate time duration between start and end time"""
    if end_time is None:
        end_time = datetime.now()
    
    duration = end_time - start_time
    total_seconds = int(duration.total_seconds())
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def get_priority_emoji(priority: str) -> str:
    """Get priority emoji based on priority level"""
    priority_emojis = {
        'urgent': '🔴',
        'high': '🟠', 
        'normal': '🟡',
        'low': '🟢'
    }
    return priority_emojis.get(priority, '⚪')

def get_status_emoji(duration_minutes: int) -> str:
    """Get status emoji based on duration"""
    if duration_minutes <= 30:
        return '🟢'
    elif duration_minutes <= 60:
        return '🟡'
    else:
        return '🔴'

def build_main_dashboard_message(dashboard_data: Dict[str, Any], technicians_data: Dict[str, Any], lang: str, updated: bool = False) -> str:
    """Builds the main real-time monitoring dashboard message."""
    if lang == 'uz':
        header = "🔄 Ma'lumotlar yangilandi!" if updated else "🕐 Real vaqtda monitoring"
        text = f"""<b>{header}</b>

📊 <b>Umumiy ma'lumot:</b>
• Faol arizalar: {dashboard_data['total_active']}
• Shoshilinch: {dashboard_data['urgent_count']}
• Yuqori: {dashboard_data['normal_count']}
• Past: {dashboard_data['low_count']}

👨‍🔧 <b>Texniklar holati:</b>
• Band: {technicians_data['busy_count']}
• Bo'sh: {technicians_data['available_count']}
• Oflayn: {technicians_data['offline_count']}
• Jami: {technicians_data['total_technicians']}
"""
    else:
        header = "🔄 Данные обновлены!" if updated else "🕐 Мониторинг в реальном времени"
        text = f"""<b>{header}</b>

📊 <b>Общая информация:</b>
• Активные заявки: {dashboard_data['total_active']}
• Срочные: {dashboard_data['urgent_count']}
• Высокие: {dashboard_data['normal_count']}
• Низкие: {dashboard_data['low_count']}

👨‍🔧 <b>Статус техников:</b>
• Заняты: {technicians_data['busy_count']}
• Свободны: {technicians_data['available_count']}
• Офлайн: {technicians_data['offline_count']}
• Всего: {technicians_data['total_technicians']}
"""
    return text

def build_applications_list_message(applications: List[Dict[str, Any]], page: int, total_pages: int, lang: str) -> str:
    """Builds the message for a paginated list of applications."""
    if not applications:
        return "📭 Faol arizalar topilmadi" if lang == 'uz' else "📭 Активные заявки не найдены"

    header = f"📋 Arizalar (Sahifa {page}/{total_pages})" if lang == 'uz' else f"📋 Заявки (Страница {page}/{total_pages})"
    
    items = []
    for i, app in enumerate(applications):
        priority_emoji = get_priority_emoji(app['priority'])
        time_since_update = calculate_time_duration(app['updated_at'])
        client_name = app['client_name']
        assigned_to = app['assigned_to'] or ('Tayinlanmagan' if lang == 'uz' else 'Не назначен')

        if lang == 'uz':
            item_text = f"{i+1}. {priority_emoji} <b>{app['id']}</b> ({app['priority']}) - {time_since_update} avval\n   Mijoz: {client_name}\n   Tayinlangan: {assigned_to}"
        else:
            item_text = f"{i+1}. {priority_emoji} <b>{app['id']}</b> ({app['priority']}) - {time_since_update} назад\n   Клиент: {client_name}\n   Назначен: {assigned_to}"
        items.append(item_text)

    return f"<b>{header}</b>\n\n" + "\n\n".join(items)

def build_technicians_list_message(technicians: List[Dict[str, Any]], page: int, total_pages: int, lang: str) -> str:
    """Builds the message for a paginated list of technicians."""
    if not technicians:
        return "👨‍🔧 Texniklar topilmadi" if lang == 'uz' else "👨‍🔧 Техники не найдены"

    header = f"👨‍🔧 Texniklar (Sahifa {page}/{total_pages})" if lang == 'uz' else f"👨‍🔧 Техники (Страница {page}/{total_pages})"

    items = []
    for i, tech in enumerate(technicians):
        status_emoji = {
            'busy': '🔴',
            'available': '🟢',
            'offline': '⚫'
        }.get(tech['status'], '⚪')
        last_seen = calculate_time_duration(tech['last_seen'])
        name = tech['name']
        current_task = tech['current_task'] or ('Vazifa yo\'q' if lang == 'uz' else 'Нет задачи')

        if lang == 'uz':
            item_text = f"{i+1}. {status_emoji} <b>{name}</b> ({tech['status']})\n   Oxirgi ko'rinish: {last_seen} avval\n   Joriy vazifa: {current_task}"
        else:
            item_text = f"{i+1}. {status_emoji} <b>{name}</b> ({tech['status']})\n   Последний раз: {last_seen} назад\n   Текущая задача: {current_task}"
        items.append(item_text)

    return f"<b>{header}</b>\n\n" + "\n\n".join(items)
