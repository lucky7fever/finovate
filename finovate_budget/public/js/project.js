frappe.ui.form.on('Project', {
    /**
     * Set default values for new projects to align with Finovate's tracking methodology
     * This runs when a new Project form is loaded
     */
    onload: function(frm) {
        if (frm.is_new()) {
            // Set '% Complete Method' to 'Task Completion'
            frm.set_value('percent_complete_method', 'Task Completion');

            // Set 'Collect Progress' to 'Yes' (checked)
            frm.set_value('collect_progress', 1);

            frm.refresh_field('percent_complete_method');
            frm.refresh_field('collect_progress');
        }
    }
});