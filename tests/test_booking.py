import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from barberbook.models import User, Service
from barberbook.bookings import BookingStore
from barberbook.services import active_services
from barberbook.staff import calendar, mark_state
from barberbook.reports import activity_report

class BookingTests(unittest.TestCase):
    def setUp(self):
        self.store=BookingStore(); self.client=User('c1'); self.service=Service('s1','Haircut',30,150)
        self.now=datetime(2026,10,6,8); self.start=datetime(2026,10,7,10)
        self.open=datetime(2026,10,7,9); self.close=datetime(2026,10,7,18)
    def book(self, start=None, client=None, service=None, blocked=()):
        return self.store.book(client or self.client,'b1',service or self.service,start or self.start,
            self.now,self.open,self.close,blocked)
    def test_booking_and_price_snapshot(self):
        a=self.book(); self.assertEqual((a.price,a.end-a.start),(150,timedelta(minutes=30)))
    def test_overlap_rejected(self):
        self.book()
        with self.assertRaises(ValueError): self.book(self.start+timedelta(minutes=15))
    def test_adjacent_slots_allowed(self):
        self.book(); self.assertEqual(self.book(self.start+timedelta(minutes=30)).id,'2')
    def test_outside_hours_and_blocked(self):
        with self.assertRaises(ValueError): self.book(self.close-timedelta(minutes=15))
        with self.assertRaises(ValueError): self.book(blocked=[(self.start,self.start+timedelta(hours=1))])
    def test_inactive_service(self):
        inactive=Service('s2','Inactive',30,100,False)
        self.assertEqual(active_services([self.service,inactive]),[self.service])
        with self.assertRaises(ValueError): self.book(service=inactive)
    def test_cancellation_frees_slot(self):
        a=self.book(); self.store.cancel(self.client,a,self.now); self.assertEqual(self.book().id,'2')
    def test_cancellation_ownership_and_time(self):
        a=self.book()
        with self.assertRaises(PermissionError): self.store.cancel(User('other'),a,self.now)
        with self.assertRaises(ValueError): self.store.cancel(self.client,a,self.start)
    def test_staff_calendar_and_transition(self):
        a=self.book(); barber=User('b1','barber')
        self.assertEqual(calendar(barber,self.store.appointments),[a])
        with self.assertRaises(ValueError): mark_state(barber,a,'completed',self.now)
        with self.assertRaises(PermissionError): mark_state(User('b2','barber'),a,'completed',a.end)
        mark_state(barber,a,'completed',a.end); self.assertEqual(a.state,'completed')
    def test_report_roles_and_filters(self):
        self.book(); d=self.start.date()
        self.assertEqual(activity_report(User('admin','admin'),self.store.appointments,d,d),{'confirmed':1})
        self.assertEqual(activity_report(User('admin','admin'),self.store.appointments,d,d,'other'),{})
        with self.assertRaises(PermissionError): activity_report(self.client,self.store.appointments,d,d)
    def test_concurrent_booking_only_one_success(self):
        def attempt(_):
            try: self.book(); return 1
            except ValueError: return 0
        with ThreadPoolExecutor(max_workers=2) as pool: self.assertEqual(sum(pool.map(attempt,range(2))),1)
        self.assertEqual(len(self.store.appointments),1)
if __name__ == '__main__': unittest.main()
