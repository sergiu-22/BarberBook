from datetime import timedelta
from threading import RLock
from .models import Appointment
from .services import validate_service
from .schedule import is_available

class BookingStore:
    def __init__(self):
        self.appointments = []
        self.lock = RLock()

    def book(self, client, barber_id, service, start, now, work_start, work_end, blocked=()):
        if client.role != 'client':
            raise PermissionError('Client role required')
        validate_service(service)
        if start <= now:
            raise ValueError('Booking must be in the future')
        end = start + timedelta(minutes=service.minutes)
        with self.lock:
            if not is_available(barber_id, start, end, self.appointments, work_start, work_end, blocked):
                raise ValueError('Slot unavailable')
            a = Appointment(str(len(self.appointments)+1), client.id, barber_id,
                service.id, start, end, service.price)
            self.appointments.append(a)
            return a

    def cancel(self, client, appointment, now):
        with self.lock:
            if client.role != 'client' or appointment.client_id != client.id:
                raise PermissionError('Own booking required')
            if appointment.state != 'confirmed' or now >= appointment.start:
                raise ValueError('Cancellation is not allowed')
            appointment.state = 'cancelled'
