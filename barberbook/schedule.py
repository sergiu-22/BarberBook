def overlaps(start, end, other_start, other_end):
    return start < other_end and other_start < end

def is_available(barber_id, start, end, appointments, work_start, work_end, blocked=()):
    if start >= end or start < work_start or end > work_end:
        return False
    if any(overlaps(start, end, a, b) for a, b in blocked):
        return False
    return not any(a.barber_id == barber_id and a.state == 'confirmed'
        and overlaps(start, end, a.start, a.end) for a in appointments)
