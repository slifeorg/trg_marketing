#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, get_time

class Appointment(Document):
    def validate(self):
        self.validate_time_slot()

    def validate_time_slot(self):
        """Validate that the time falls within the selected time slot range"""
        time_slots = {
            "9am - 12pm": ("09:00:00", "12:00:00"),
            "10am - 1pm": ("10:00:00", "13:00:00"),
            "11am - 2pm": ("11:00:00", "14:00:00"),
            "12pm - 3pm": ("12:00:00", "15:00:00"),
            "1pm - 4pm": ("13:00:00", "16:00:00"),
            "2pm - 5pm": ("14:00:00", "17:00:00"),
            "3pm - 6pm": ("15:00:00", "18:00:00"),
            "4pm - 7pm": ("16:00:00", "19:00:00"),
            "5pm - 8pm": ("17:00:00", "20:00:00"),
            "6pm - 9pm": ("18:00:00", "21:00:00"),
            "7pm - 10pm": ("19:00:00", "22:00:00")
        }

        if self.time_slot and self.time:
            start_time, end_time = time_slots.get(self.time_slot)
            current_time = get_time(self.time)
            slot_start = get_time(start_time)
            slot_end = get_time(end_time)

            if not (slot_start <= current_time <= slot_end):
                frappe.throw(f"Time {self.time} is not within the selected time slot {self.time_slot}")

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