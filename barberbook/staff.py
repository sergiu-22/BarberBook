def calendar(barber, appointments):
    if barber.role != 'barber':
        raise PermissionError('Barber role required')
    return [a for a in appointments if a.barber_id == barber.id]

def mark_state(barber, appointment, state, now):
    if barber.role != 'barber' or appointment.barber_id != barber.id:
        raise PermissionError('Own calendar required')
    if state not in ('completed','no_show') or appointment.state != 'confirmed' or now < appointment.start:
        raise ValueError('Invalid state transition')
    appointment.state = state
