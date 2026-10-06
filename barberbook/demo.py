from datetime import datetime
from .models import User, Service
from .bookings import BookingStore
from .reports import activity_report

now=datetime(2026,10,6,8); start=datetime(2026,10,7,10)
store=BookingStore()
a=store.book(User('client-1'),'barber-1',Service('haircut','Haircut',30,150),start,now,
    datetime(2026,10,7,9),datetime(2026,10,7,18))
print(f'Booking {a.id}: {a.start} - {a.end}, price {a.price}, state {a.state}')
print(activity_report(User('admin','admin'),store.appointments,start.date(),start.date()))
