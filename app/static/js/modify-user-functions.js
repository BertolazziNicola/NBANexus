/**
 * @function passwordAndNewPassordCheck
 * @description
 * Validates the new password input field against specific requirements and optionally hides or shows error messages.
 * - Ensures the new password meets the following complexity criteria:
 *   - Length between 7 and 45 characters.
 *   - Contains at least one uppercase letter, one lowercase letter, and one special character.
 * - Handles cases where both fields (`password` and `new-password`) are empty, treating them as valid without error messages.
 * - Displays an error message if the new password does not meet the specified criteria and hides it otherwise.
 *
 * **Behavior:**
 * - If both fields are empty, validation is considered successful and no errors are shown.
 * - If the new password does not meet the criteria, an error message is displayed.
 * - Clears error messages for valid inputs.
 *
 * @param {HTMLElement} input - The input field triggering the validation, typically within a form.
 * @returns {boolean} - Returns `true` if validation passes or both fields are empty, otherwise `false`.
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
 * @function submitProperty
 * @description
 * Toggles the submit button's enabled state based on form validation results.
 * - Checks if the error element is hidden and that both `password` and `new-password` fields are populated.
 * - Enables the submit button if the form passes validation and disables it otherwise.
 *
 * **Behavior:**
 * - Requires both `password` and `new-password` fields to be non-empty for the submit button to be enabled.
 * - Disables the submit button if either field is empty or validation fails.
 *
 * @param {HTMLElement} input - The input field triggering the submit state check, typically within a form.
 * @returns {void}
 */
function submitProperty(input) {
    var form = $(input).closest('form');
    var password = form.find('input[name="password"]').val();
    var newPassword = form.find('input[name="new-password"]').val();

    if (form.find('#error').hasClass('d-none') && password.length > 0 && newPassword.length > 0) {
        form.find('button[type="submit"]').prop('disabled', false);
    } else {
        form.find('button[type="submit"]').prop('disabled', true);
    }
}