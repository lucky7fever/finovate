import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    """Defines the columns that will be displayed in the report."""
    return [
        {"label": _("Project"), "fieldname": "project", "fieldtype": "Link", "options": "Project", "width": 250},
        {"label": _("Customer"), "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": _("Total Billed (Income)"), "fieldname": "total_billed_amount", "fieldtype": "Currency", "width": 150},
        {"label": _("Total Cost"), "fieldname": "total_cost", "fieldtype": "Currency", "width": 150},
        {"label": _("Gross Margin (Profit)"), "fieldname": "gross_margin", "fieldtype": "Currency", "width": 150},
        {"label": _("Margin %"), "fieldname": "per_gross_margin", "fieldtype": "Percent", "width": 100},
    ]

def get_data(filters):
    """Fetches and processes project data to calculate profitability."""
    conditions = get_conditions(filters)
    
    # Fetch pre-calculated data directly from the Project doctype for efficiency
    projects = frappe.get_all(
        "Project",
        filters=conditions,
        fields=[
            "name as project",
            "customer",
            "status",
            "total_billed_amount",
            "total_costing_amount",      # Labor costs from timesheets
            "total_purchase_cost",       # Costs from Purchase Invoices
            "total_consumed_material_cost", # Costs from Stock Entries
            "gross_margin",
            "per_gross_margin"
        ]
    )

    # Process the data to create a  single "Total Cost" column
    for p in projects:
        p.total_cost = flt(p.total_costing_amount) + flt(p.total_purchase_cost) + flt(p.total_consumed_material_cost)

    return projects

def get_conditions(filters):
    """Builds a dictionary of filters for the frappe.get_all query."""
    conditions = {"company": filters.get("company")}

    if filters.get("customer"):
        conditions["customer"] = filters.get("customer")
        
    if filters.get("project_status"):
        conditions["status"] = filters.get("project_status")

    return conditions