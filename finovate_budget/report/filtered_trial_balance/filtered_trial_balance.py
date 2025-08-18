import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    """Defines the columns for the report."""
    return [
        {"label": _("Account"), "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 300},
        {"label": _("Debit"), "fieldname": "debit", "fieldtype": "Currency", "width": 150},
        {"label": _("Credit"), "fieldname": "credit", "fieldtype": "Currency", "width": 150},
        {"label": _("Balance"), "fieldname": "balance", "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    """Fetches and processes the general ledger data based on filters."""
    conditions = get_conditions(filters)
    
    # SQL query to get debit/credit  sums for each account
    gl_entries = frappe.db.sql(f"""
        SELECT
            account,
            SUM(debit) as debit,
            SUM(credit) as credit
        FROM `tabGL Entry`
        WHERE {conditions}
        GROUP BY account
        ORDER BY account
    """, filters, as_dict=True)

    # Process data to calculate  balance
    data = []
    for entry in gl_entries:
        balance = entry.debit - entry.credit
        data.append({
            "account": entry.account,
            "debit": entry.debit,
            "credit": entry.credit,
            "balance": balance
        })
        
    return data

def get_conditions(filters):
    """Builds the WHERE clause for the SQL query."""
    conditions = "company = %(company)s AND fiscal_year = %(fiscal_year)s AND docstatus = 1"

    # Add the cost_center filter condition  ONLY if a value is provided by the user.
    if filters.get("cost_center"):
        conditions += " AND cost_center = %(cost_center)s"

    return conditions