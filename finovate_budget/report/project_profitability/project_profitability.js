
/**
 * Frappe Query Report configuration  for "Project Profitability"
 *
 * Defines the filters available for  the report :
 * - Company:  Required, linked to the "Company" doctype, defaults to user's default company.
 * - Customer : Optional, linked to the "Customer" doctype
 * - Project Status:  Optional, select field with options "Open", "Completed",  "Cancelled", defaults to "Open".
 */
frappe.query_reports["Project Profitability"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
        {
			"fieldname":"project_status",
			"label": __("Project Status"),
			"fieldtype": "Select",
			"options": "\nOpen\nCompleted\nCancelled",
            "default": "Open"
		}
	]
};