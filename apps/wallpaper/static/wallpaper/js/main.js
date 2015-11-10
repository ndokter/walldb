$(document).ready(function() {
    // Limit upload size of all file inputs with a data-max-file-size attribute.
    $('input[type=file][data-max-file-size]').bind('change', function() {
        var max_file_size = $(this).data('maxFileSize'),
            current_file_size = this.files[0].size/1024; // in KB's

        // Remove any existing file errors
        $('.help-block', parent).remove();

        if (current_file_size > max_file_size) {
            var parent = $(this).parent();

            parent.addClass('has-error');

            parent.append(
                $('<span/>')
                    .addClass('help-block max-file-size-error')
                    .html('Please limit the file size to under ' +
                          max_file_size + ' KB')
            );
        }
    });

    // Disable forms which have max-file-size errors.
    $('form').on('submit', function(e) {
        if ($('.max-file-size-error', this).length) {
            e.preventDefault();
        }
    });
});