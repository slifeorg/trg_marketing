#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime

class Appointment(Document):
    def validate(self):
        self.validate_time_slot()

    def validate_time_slot(self):
        """Validate that the time matches the selected time slot"""
        time_slots = {
            "9am - 12pm": "09:00:00",
            "10am - 1pm": "10:00:00",
            "11am - 2pm": "11:00:00",
            "12pm - 3pm": "12:00:00",
            "1pm - 4pm": "13:00:00",
            "2pm - 5pm": "14:00:00",
            "3pm - 6pm": "15:00:00",
            "4pm - 7pm": "16:00:00",
            "5pm - 8pm": "17:00:00",
            "6pm - 9pm": "18:00:00",
            "7pm - 10pm": "19:00:00"
        }

        if self.time_slot and self.time:
            expected_time = time_slots.get(self.time_slot)
            if expected_time and str(self.time) != expected_time:
                frappe.throw(f"Time {self.time} does not match the selected time slot {self.time_slot}")

    @frappe.whitelist()
    def get_events(start, end, filters=None):
        """Returns events for Gantt / Calendar view"""
        conditions = ["appointment_date between %(start)s and %(end)s"]

        if filters:
            if filters.get("status"):
                conditions.append("status = %(status)s")

        events = frappe.db.sql("""
            select
                name, customer_name, appointment_date, time,
                time_slot, status, lead
            from
                `tabAppointment`
            where
                {}""".format(" and ".join(conditions)),
            {
                "start": start,
                "end": end,
                "status": filters.get("status") if filters else None
            },
            as_dict=True
        )

        for event in events:
            event.all_day = 0
            # Combine date and time for proper calendar display
            if event.time:
                event.appointment_date = f"{event.appointment_date} {event.time}"

        return events
