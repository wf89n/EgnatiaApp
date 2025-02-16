(function($) {
    $(document).ready(function() {
        // Listen for changes in the Region field
        $('#id_region').change(function() {
            var regionId = $(this).val();
            var currentUrl = window.location.href.split('?')[0]; // Get the base URL
            if (regionId) {
                window.location.href = currentUrl + '?region=' + regionId;  // Redirect with region ID
            } else {
                window.location.href = currentUrl;  // Just reload if no region is selected
            }
        });

        // Listen for changes in the Group field
        $('#id_group').change(function() {
            var groupId = $(this).val();
            var currentUrl = window.location.href.split('?')[0];  // Get the base URL
            var queryString = new URLSearchParams(window.location.search); // Retain existing query parameters

            // Retain region selection if it's present
            if (queryString.get('region')) {
                currentUrl += '?region=' + queryString.get('region');
            }

            // Add group selection to the URL
            if (groupId) {
                currentUrl += '&group=' + groupId;
            }

            window.location.href = currentUrl;  // Redirect to the new URL
        });

        // Listen for changes in the Department field
        $('#id_department').change(function() {
            var departmentId = $(this).val();
            var currentUrl = window.location.href.split('?')[0];  // Get the base URL
            var queryString = new URLSearchParams(window.location.search); // Retain existing query parameters

            // Retain region and group selections if they're present
            if (queryString.get('region')) {
                currentUrl += '?region=' + queryString.get('region');
            }
            if (queryString.get('group')) {
                currentUrl += '&group=' + queryString.get('group');
            }

            // Add department selection to the URL
            if (departmentId) {
                currentUrl += '&department=' + departmentId;
            }

            window.location.href = currentUrl;  // Redirect to the new URL
        });
    });
})(django.jQuery);
