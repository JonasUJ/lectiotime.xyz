const MDCRipple = mdc.ripple.MDCRipple;
const MDCTextField = mdc.textField.MDCTextField;
const MDCFormField = mdc.formField.MDCFormField;
const MDCCheckbox = mdc.checkbox.MDCCheckbox;
const MDCTextFieldIcon = mdc.textField.MDCTextFieldIcon;

function load_all(selector, MDCObj) {
    return [].map.call(document.querySelectorAll(selector), function(el) {
        return new MDCObj(el);
    });
}

function mdc_init() {
    load_all('.mdc-button', MDCRipple);
    load_all('.mdc-text-field', MDCTextField);
    load_all('.mdc-checkbox', MDCCheckbox);
    load_all('.mdc-form-field', MDCFormField);
    load_all('.mdc-text-field-icon', MDCTextFieldIcon);
}