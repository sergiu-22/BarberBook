from collections import Counter

def activity_report(admin, appointments, date_from, date_to, barber_id=None):
    if admin.role != 'admin':
        raise PermissionError('Administrator role required')
    selected = [a for a in appointments if date_from <= a.start.date() <= date_to
        and (barber_id is None or a.barber_id == barber_id)]
    return dict(Counter(a.state for a in selected))
