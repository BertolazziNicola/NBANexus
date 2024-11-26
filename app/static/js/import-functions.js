/**
 * @function seasonInputCheck
 * @description
 * Validates and formats a season input field to conform to the pattern `YYYY-YY`. 
 * - Allows only numeric input and automatically formats the value to include the calculated second year (YY).
 * - Handles user backspace or delete actions to remove the second part of the input.
 * - Automatically disables invalid operations such as copy-paste or drag-and-drop in the input field.
 * - Enables or disables the associated form submit button based on the validity of the input.
 *
 * **Behavior:**
 * - A dash (`-`) is added after the first four digits (`YYYY`) to separate the second part (`YY`).
 * - The second year (`YY`) is calculated as `YYYY + 1` and appended automatically when the first year is complete.
 * - If the user deletes part of the input, the second part (`YY`) is cleared.
 * - Ensures the input is restricted to 7 characters (`YYYY-YY`).
 *
 * @param {HTMLElement} input - The input field to be validated and formatted.
 */
function seasonInputCheck(input) {
    var $input = $(input);

    // Disable copy-paste and drag-drop actions
    $input.on('paste drop', function (e) {
        e.preventDefault();
    });

    // Handle input and format accordingly
    $input.on('input', function () {
        var value = $input.val();

        // Allow only numbers, remove all non-numeric characters
        value = value.replace(/[^0-9]/g, '');

        // If length is more than 4 characters, automatically append second part (YY)
        if (value.length >= 4) {
            var year = parseInt(value.substring(0, 4), 10);
            if (year >= 1000 && year <= 9999) {
                var nextYear = year + 1;  // Calculate next year
                var nextYearLastTwoDigits = nextYear.toString().slice(-2);  // Get last 2 digits of the next year
                value = value.substring(0, 4) + '-' + nextYearLastTwoDigits;
            }
        }

        // If the value is backspaced, remove the last part after the dash
        if (value.length < 7) {
            value = value.substring(0, 4); // Keep only the first 4 digits (YYYY)
        }

        // Restrict input to 7 characters (YYYY-YY)
        value = value.substring(0, 7);

        // Update the input value with the formatted version
        $input.val(value);

        // Set button property (import button)
        $button = $(input).closest('form').find('.submit-button');
        if (value.length === 7) {
            $button.prop('disabled', false);
        }else{
            $button.prop('disabled', true);
        }
    });

    // Detect backspace or delete keys explicitly
    $input.on('keydown', function (e) {
        var value = $input.val();

        // Check if the user presses the backspace key (keyCode 8) or delete key (keyCode 46)
        if (e.key === "Backspace" || e.key === "Delete") {
            // Check if there's a dash and remove the part after it if backspace or delete is pressed
            if (value.length === 7 && value.includes('-')) {
                // User is trying to delete the second part (YY), remove it
                $input.val(value.substring(0, 4)); // Remove '-YY' part
            }
        }
    });
}

/**
 * @function reimportSeason
 * @description
 * Automates the process of populating a form for season re-import and scrolling to the form section.
 * - Sets the season input field with a specified date.
 * - Ensures the overwrite checkbox is marked as checked.
 * - Scrolls smoothly to the form element to draw user attention.
 *
 * @param {string} date - The season value to be set in the input field.
 */
function reimportSeason(date){
    $form = $('#form-import');
    $form.find('input[type="checkbox"][name="overwrite"]').prop('checked');
    $form.find('#season-input').val(date);
    scrollToUser('form-import');
}

/**
 * @function scrollToUser
 * @description
 * Smoothly scrolls the browser window to an element identified by its ID. 
 * - Adjusts the scroll position to ensure the target element is in view, offset by 150px for better visibility.
 * - Animation duration is set to 250ms for a smooth user experience.
 *
 * @param {string} id - The ID of the target element to scroll to.
 */
function scrollToUser(id) {
    var element = $('#' + id);
    if (element.length) {
        $('html, body').animate({
            scrollTop: element.offset().top - 150
        }, 250);
    }
}