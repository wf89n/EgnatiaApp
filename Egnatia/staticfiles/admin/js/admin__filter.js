(function($){
    // This function will be triggered when Region field changes
    function updateFilterFields() {
        const regionId = $('#id_region').val();

        // Reset the fields to make sure they're refreshed after each region change
        $('#id_group').empty().append('<option value="">---------</option>');
        $('#id_department').empty().append('<option value="">---------</option>');
        $('#id_role').empty().append('<option value="">---------</option>');

        // If Region is selected, filter Groups based on the selected Region
        if (regionId) {
            $.ajax({
                url: '/admin/filter_groups/', // Define the URL for fetching filtered groups
                data: {
                    'region_id': regionId,
                },
                success: function(data) {
                    // Populate the Group dropdown with the filtered results
                    data.groups.forEach(function(group) {
                        $('#id_group').append(new Option(group.name, group.id));
                    });
                    $('#id_group').prop('disabled', false);  // Enable group select dropdown
                }
            });
        }

        // Add similar logic for departments and roles if needed
    }

    // Trigger the updateFilterFields function when Region field changes
    $('#id_region').on('change', updateFilterFields);
})(django.jQuery);
