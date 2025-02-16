(function($){
    // This function will be triggered when Region field changes
    function updateFilterFields() {
        const regionId = $('#id_region').val();

        // Reset the fields to ensure they're refreshed after each region change
        $('#id_group').empty().append('<option value="">---------</option>');
        $('#id_department').empty().append('<option value="">---------</option>');
        $('#id_role').empty().append('<option value="">---------</option>');

        // If Region is selected, filter Groups based on the selected Region
        if (regionId) {
            $.ajax({
                url: '/admin/filter_groups/',  // Define the URL for fetching filtered groups
                data: {
                    'region_id': regionId,
                },
                success: function(data) {
                    // Populate the Group dropdown with the filtered results
                    if (data.groups.length) {
                        data.groups.forEach(function(group) {
                            $('#id_group').append(new Option(group.name, group.id));
                        });
                        $('#id_group').prop('disabled', false);  // Enable group select dropdown
                    }
                }
            });
        } else {
            $('#id_group').prop('disabled', true);
        }

        // Add similar logic for departments and roles
        const groupId = $('#id_group').val();
        if (groupId) {
            $.ajax({
                url: '/admin/filter_departments/',  // Define the URL for fetching filtered departments
                data: {
                    'group_id': groupId,
                },
                success: function(data) {
                    if (data.departments.length) {
                        data.departments.forEach(function(department) {
                            $('#id_department').append(new Option(department.name, department.id));
                        });
                        $('#id_department').prop('disabled', false);  // Enable department select dropdown
                    }
                }
            });
        } else {
            $('#id_department').prop('disabled', true);
        }

        const departmentId = $('#id_department').val();
        if (departmentId) {
            $.ajax({
                url: '/admin/filter_roles/',  // Define the URL for fetching filtered roles
                data: {
                    'department_id': departmentId,
                },
                success: function(data) {
                    if (data.roles.length) {
                        data.roles.forEach(function(role) {
                            $('#id_role').append(new Option(role.name, role.id));
                        });
                        $('#id_role').prop('disabled', false);  // Enable role select dropdown
                    }
                }
            });
        } else {
            $('#id_role').prop('disabled', true);
        }
    }

    // Trigger the updateFilterFields function when Region field changes
    $('#id_region').on('change', updateFilterFields);

})(django.jQuery);
