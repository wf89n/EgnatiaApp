(function($) {
    $(document).ready(function() {
        // Listen for changes in the Region field
        $('#id_region').change(function() {
            var regionId = $(this).val();
            var currentUrl = window.location.href.split('?')[0];
            if (regionId) {
                window.location.href = currentUrl + '?region=' + regionId;
            } else {
                window.location.href = currentUrl;
            }
        });

        // Listen for changes in the Group field
        $('#id_group').change(function() {
            var groupId = $(this).val();
            var currentUrl = window.location.href.split('?')[0];
            var queryString = new URLSearchParams(window.location.search);

            // Retain region selection
            if (queryString.get('region')) {
                currentUrl += '?region=' + queryString.get('region');
            }

            // Add group selection
            if (groupId) {
                currentUrl += '&group=' + groupId;
            }

            window.location.href = currentUrl;
        });

        // Listen for changes in the Department field
        $('#id_department').change(function() {
            var departmentId = $(this).val();
            var currentUrl = window.location.href.split('?')[0];
            var queryString = new URLSearchParams(window.location.search);

            // Retain region and group selection
            if (queryString.get('region')) {
                currentUrl += '?region=' + queryString.get('region');
            }
            if (queryString.get('group')) {
                currentUrl += '&group=' + queryString.get('group');
            }

            // Add department selection
            if (departmentId) {
                currentUrl += '&department=' + departmentId;
            }

            window.location.href = currentUrl;
        });
    });
})(django.jQuery);
