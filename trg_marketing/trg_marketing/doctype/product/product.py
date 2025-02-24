#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import cint

class Product(Document):
    def validate(self):
        self.validate_rank()
        self.update_top_10_status()
        self.validate_product_code()
        self.validate_prices()

    def validate_rank(self):
        """Validate that rank is between 1 and 10 if set"""
        if self.rank:
            if not (1 <= cint(self.rank) <= 10):
                frappe.throw("Rank must be between 1 and 10")

            # Check for duplicate ranks in top 10
            existing = frappe.get_all(
                "Product",
                filters={
                    "rank": self.rank,
                    "name": ["!=", self.name]
                }
            )
            if existing:
                frappe.throw(f"Rank {self.rank} is already assigned to another product")

    def update_top_10_status(self):
        """Automatically update is_top_10 based on rank"""
        self.is_top_10 = 1 if self.rank and 1 <= cint(self.rank) <= 10 else 0

    def validate_product_code(self):
        """Validate product code format and uniqueness"""
        if self.product_code:
            # Convert to uppercase
            self.product_code = self.product_code.upper()

            # Check uniqueness
            existing = frappe.db.exists("Product", {
                "product_code": self.product_code,
                "name": ["!=", self.name]
            })
            if existing:
                frappe.throw(f"Product Code {self.product_code} already exists")

    def validate_prices(self):
        """Validate price values"""
        if self.base_price and self.base_price < 0:
            frappe.throw("Base Price cannot be negative")

    def before_save(self):
        """Actions before saving"""
        self.update_availability()

    def update_availability(self):
        """Update availability status based on conditions"""
        if not self.enabled:
            self.availability_status = "Discontinued"

    def on_trash(self):
        """Before deletion checks"""
        self.check_dependencies()

    def check_dependencies(self):
        """Check if product can be deleted"""
        # Add checks for related records (orders, quotes etc.)
        pass

    @frappe.whitelist()
    def copy_product(self):
        """Create a copy of the product"""
        new_product = frappe.copy_doc(self)
        new_product.product_name = f"Copy of {self.product_name}"
        new_product.product_code = None
        new_product.rank = None
        new_product.is_top_10 = 0
        return new_product

    @frappe.whitelist()
    def update_rank(self, new_rank):
        """Update product rank with validation"""
        if not new_rank:
            self.rank = None
            self.save()
            return

        new_rank = cint(new_rank)
        if not (1 <= new_rank <= 10):
            frappe.throw("Rank must be between 1 and 10")

        # Check for existing product with new rank
        existing = frappe.get_all(
            "Product",
            filters={
                "rank": new_rank,
                "name": ["!=", self.name]
            }
        )

        if existing:
            # Swap ranks
            existing_product = frappe.get_doc("Product", existing[0].name)
            old_rank = self.rank

            # Update existing product
            existing_product.rank = old_rank
            existing_product.save()

            # Update current product
            self.rank = new_rank
            self.save()
        else:
            self.rank = new_rank
            self.save()
