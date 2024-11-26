/**
 * @function inputsCheck
 * @description
 * Validates form inputs for email, password, and password confirmation. The function performs the following checks:
 * - Ensures the email field is not empty and matches a valid email format.
 * - Ensures the password and re-password fields are not empty and match each other.
 * - Ensures the password meets complexity requirements (length 7-45, contains at least one uppercase letter, one lowercase letter, and one special symbol).
 * 
 * If any validation fails, an error message is displayed in the form's designated error element.
 *
 * @param {HTMLElement} input - The input element triggering the validation, typically within a form.
 * @returns {boolean} - Returns `true` if all inputs are valid, otherwise `false`.
 */
function inputsCheck(input) {
    var form = $(input).closest('form');
    var email = form.find('input[name="email"]').val();
    var password = form.find('input[name="password"]').val();
    var rePassword = form.find('input[name="re-password"]').val();

    var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{7,45}$/;
    var emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    if (email.length == 0) {
        form.find('#error').find('label').html("Email is required.");
        form.find('#error').removeClass('d-none');
        return false;
    } else if (!emailRegex.test(email)) {
        form.find('#error').find('label').html("Please enter a valid email address.");
        form.find('#error').removeClass('d-none');
        return false;
    } else if (password.length == 0 || rePassword.length == 0) {
        form.find('#error').find('label').html("Password and re-password cannot be empty.");
        form.find('#error').removeClass('d-none');
        return false;
    } else if (password !== rePassword) {
        form.find('#error').find('label').html("Passwords do not match.");
        form.find('#error').removeClass('d-none');
        return false;
    } else if (!passwordRegex.test(password)) {
        form.find('#error').find('label').html("The password must be between 7 and 45 characters long, contain at least one uppercase letter, one lowercase letter, and one symbol.");
        form.find('#error').removeClass('d-none');
        return false;
    } else {
        form.find('#error').find('label').html("");
        form.find('#error').addClass('d-none');
        return true;
    }
}

/**
 * @function submitPropertyCreate
 * @description
 * Handles the state of the form's submit button based on the validation status of the form inputs.
 * - Ensures the submit button is only enabled if there are no validation errors and all required fields are populated.
 * - Disables the submit button if any validation errors exist or required fields are empty.
 *
 * @param {HTMLElement} input - The input element triggering the submit state check, typically within a form.
 * @returns {void}
 */
function submitPropertyCreate(input) {
    var form = $(input).closest('form');
    var email = form.find('input[name="email"]').val();
    var password = form.find('input[name="password"]').val();
    var rePassword = form.find('input[name="re-password"]').val();

    if (form.find('#error').hasClass('d-none') && email.length > 0 && password.length > 0 && rePassword.length > 0) {
        form.find('button[type="submit"]').prop('disabled', false);
    } else {
        form.find('button[type="submit"]').prop('disabled', true);
    }
}