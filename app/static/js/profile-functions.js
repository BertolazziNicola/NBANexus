/**
 * copyFromIcon - A function to handle the copying of input text to the clipboard when the user clicks an icon.
 *
 * @param {HTMLElement} icon - The icon element that was clicked.
 * @param {string} inputName - The name of the input field whose value is to be copied.
 *
 * Example Usage:
 * <svg onclick="copyFromIcon(this, 'api-key')" ...></svg>
 */
function copyFromIcon(icon, inputName) {
    var input = $(icon).closest('form').find('#api-key');

    // Select the input value
    input.select();
    input[0].setSelectionRange(0, 99999); // For mobile devices

    // Copy the selected text to the clipboard
    navigator.clipboard.writeText(input.val());

    var checkIcon = `
        <svg data-bs-toggle="tooltip" data-bs-placement="top" title="Copy" style="cursor: pointer;"
        xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
            fill="none" stroke="green" stroke-width="2" stroke-linecap="round"
            stroke-linejoin="round" class="feather feather-check">
            <polyline points="20 6 9 17 4 12">
            </polyline>
        </svg>
    `

    // Replace icon
    var container = $(icon).closest('div')
    // $(icon).replaceWith(checkIcon);
    $(container).html("<br><br>" + checkIcon);

    // Set normal icon (default)
    setTimeout(function() {
        var copyIcon = `
        <svg data-bs-toggle="tooltip" data-bs-placement="top" title="Copy"
            onclick="copyFromIcon(this, 'api-key')" style="cursor: pointer;"
            xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
            fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
            stroke-linejoin="round" class="feather feather-copy">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
        </svg>
        `

        $(container).find('svg').replaceWith(copyIcon);

        // Reset tooltip
        var tooltip = bootstrap.Tooltip.getInstance(icon);
        if (tooltip) {
            tooltip.dispose();
        }
        new bootstrap.Tooltip($(container).find('svg'));
    }, 2000); // 2 sec
}

/**
 * Validates the provided password and new password fields in a form.
 * 
 * This function checks if the "new-password" field meets a specific pattern:
 * - Must be between 7 and 45 characters long.
 * - Must contain at least one uppercase letter, one lowercase letter, and one symbol.
 * 
 * If both fields are empty, validation passes with no errors displayed.
 * If the new password does not meet the criteria, an error message is displayed.
 * If validation passes, any existing error messages are hidden.
 * 
 * @param {HTMLElement} input - The input field triggering the validation, typically part of a form.
 * @returns {boolean} - Returns `true` if validation passes, otherwise `false`.
 */
function passwordAndNewPassordCheck(input) {
    var form = $(input).closest('form');
    var password = form.find('input[name="password"]').val();
    var newPassword = form.find('input[name="new-password"]').val();

    var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{7,45}$/;

    if(password.length == 0 && newPassword.length == 0){
        form.find('#error').find('label').html("");
        form.find('#error').addClass('d-none'); // Hide error
        return true;
    }else if (!passwordRegex.test(newPassword)) {
        form.find('#error').find('label').html("The new password must be between 7 and 45 characters long, contain at least one uppercase letter, one lowercase letter, and one symbol.");
        form.find('#error').removeClass('d-none'); // Show error
        return false;
    } else {
        form.find('#error').find('label').html("");
        form.find('#error').addClass('d-none'); // Hide error
        return true;
    }
}

/**
 * Enables or disables the submit button in a form based on input validation.
 *
 * This function checks the closest form to the provided input element, ensuring
 * that both the "password" and "new-password" fields are filled and that no 
 * error messages are currently displayed. If the conditions are met, the submit
 * button is enabled; otherwise, it is disabled.
 *
 * @param {HTMLElement} input - The input element that triggered the function.
 */
function submitPropertyProfile(input) {
    var form = $(input).closest('form');
    var password = form.find('input[name="password"]').val();
    var newPassword = form.find('input[name="new-password"]').val();

    if (form.find('#error').hasClass('d-none') && password.length > 0 && newPassword.length > 0) {
        form.find('button[type="submit"]').prop('disabled', false);
    } else {
        form.find('button[type="submit"]').prop('disabled', true);
    }
}