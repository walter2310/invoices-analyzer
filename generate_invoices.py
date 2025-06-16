from fpdf import FPDF
import random
from datetime import datetime, timedelta
import os
from calendar import month_name

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'INVOICE', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_monthly_invoices():
    if not os.path.exists('invoices'):
        os.makedirs('invoices')

    vendors = {
        "AWS": "Amazon Web Services",
        "Google_Cloud": "Google Cloud Platform",
        "Microsoft": "Microsoft Azure",
        "Stripe": "Payment processing",
        "ADP": "Payroll services",
        "Gusto": "Payroll services",
        "Starbucks": "Coffee supplies",
        "OfficeMax": "Office supplies",
        "Zoom": "Zoom Pro subscription",
        "Slack": "Slack subscription",
        "Telmex": "Internet service",
        "CFE": "Electricity service",
        "WeWork": "Coworking space",
    }

    concepts_by_vendor = {
        "AWS": ["Cloud computing services", "S3 Storage", "EC2 Instances"],
        "Google_Cloud": ["GCP services", "BigQuery", "Cloud Storage"],
        "Microsoft": ["Office 365 licenses", "Azure services"],
        "Stripe": ["Payment processing", "Transaction fees"],
        "ADP": ["Payroll processing", "Payroll taxes"],
        "Gusto": ["Payroll services", "Employee benefits"],
        "Starbucks": ["Coffee supplies", "Office coffee"],
        "OfficeMax": ["Office materials", "Printer toner"],
        "Zoom": ["Monthly subscription", "Zoom licenses"],
        "Slack": ["Business plan", "Workspace licenses"],
        "Telmex": ["Business internet", "Phone package"],
        "CFE": ["Electricity consumption", "Power service"],
        "WeWork": ["Space rental", "Monthly membership"],
    }

    # Generate invoices from January 2024 to May 2025
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 5, 31)

    current_date = start_date
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        month_name_str = month_name[month]

        # Create year-month directory
        month_dir = os.path.join('invoices', f"{year}_{month_name_str}")
        if not os.path.exists(month_dir):
            os.makedirs(month_dir)

        for i in range(3):
            vendor_name, vendor_desc = random.choice(list(vendors.items()))

            pdf = PDF()
            pdf.add_page()

            # Generate a random day in this month
            last_day = 28 if month == 2 else 31 if month in [1,3,5,7,8,10,12] else 30
            day = random.randint(1, last_day)
            invoice_date = datetime(year, month, day)

            available_concepts = concepts_by_vendor[vendor_name]
            concept = random.choice(available_concepts)
            amount = round(random.uniform(100, 1000), 2)
            currency = "USD"
            invoice_number = f"INV-{year%100:02d}{month:02d}{i+1:02d}"
            tax = round(amount * 0.16, 2)
            total = round(amount + tax, 2)

            # Invoice information
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, f'Invoice Number: {invoice_number}', 0, 1)
            pdf.cell(0, 10, f'Date: {invoice_date.strftime("%m/%d/%Y")}', 0, 1)
            pdf.cell(0, 10, f'Vendor: {vendor_desc}', 0, 1)
            pdf.ln(10)

            # Items table
            pdf.set_font('Arial', 'B', 12)
            with pdf.table() as table:
                row = table.row()
                row.cell("Description", align="C")
                row.cell("Quantity", align="C")
                row.cell("Unit Price", align="C")
                row.cell("Amount", align="C")

                pdf.set_font('Arial', '', 12)
                row = table.row()
                row.cell(concept)
                row.cell("1", align="C")
                row.cell(f"{amount} {currency}", align="C")
                row.cell(f"{amount} {currency}", align="C")

            pdf.ln(10)
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, f"Subtotal: {amount} {currency}", 0, 1, 'R')
            pdf.cell(0, 10, f"Tax (16%): {tax} {currency}", 0, 1, 'R')

            pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, f"TOTAL: {total} {currency}", 0, 1, 'R')

            filename = f"{month_name_str}_{vendor_name.replace(' ', '_')}.pdf"
            filepath = os.path.join(month_dir, filename)
            pdf.output(filepath)
            print(f"Invoice generated: {filepath}")

        # Move to next month
        if current_date.month == 12:
            current_date = datetime(current_date.year + 1, 1, 1)
        else:
            current_date = datetime(current_date.year, current_date.month + 1, 1)


generate_monthly_invoices()