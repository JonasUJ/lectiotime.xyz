MDCRipple = mdc.ripple.MDCRipple;
MDCTextField = mdc.textField.MDCTextField;
MDCFormField = mdc.formField.MDCFormField;
MDCCheckBox = mdc.checkbox.MDCCheckBox;

function load_all(selector, mdcobj) {
    return [].map.call(document.querySelectorAll(selector), function(el) {
        return new mdcobj(el);
    });
}

function mdc_init() {
    load_all('.mdc-text-field', MDCTextField);
    load_all('.mdc-checkbox', MDCCheckBox);
    load_all('.mdc-form-field', MDCFormField);
    load_all('.mdc-button', MDCRipple);
}