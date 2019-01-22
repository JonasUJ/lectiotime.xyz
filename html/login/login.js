import * as util from '../util.js'

const re_skoleid = /lectio\/(\d+)\//;
const re_elevid = /elevid=(\d+)/;
let storage = window.localStorage;
let el_elevid, el_skoleid, el_husk_mig, el_btn_login, el_progress, el_skemaurl;

function onload() {
    el_elevid = document.getElementById('elevid');
    el_skoleid = document.getElementById('skoleid');
    el_skemaurl = document.getElementById('skemaurl');
    el_husk_mig = document.getElementById('husk-mig');
    el_btn_login = document.getElementById('btn-login');
    el_progress = document.querySelector('.mdc-linear-progress');
    el_progress.MDCLinearProgress.determinate = false;

    el_elevid.value = storage.getItem(el_elevid.id)
    el_skoleid.value = storage.getItem(el_skoleid.id)
    el_husk_mig.checked = storage.getItem(el_husk_mig.id) == "true" ? true : false;
    document.querySelector('.elevid label').classList.remove('mdc-floating-label--float-above');
    document.querySelector('.skoleid label').classList.remove('mdc-floating-label--float-above');
    if (el_elevid.value) {
        document.querySelector('.elevid label').classList.add('mdc-floating-label--float-above');
    }
    if (el_skoleid.value) {
        document.querySelector('.skoleid label').classList.add('mdc-floating-label--float-above');
    }
    el_btn_login.focus();
}

function login() {
    updateStorage();
    el_progress.MDCLinearProgress.open()
    util.httpGetAsync(`http://127.0.0.1:5000/exists?school_id=${el_skoleid.value}&elev_id=${el_elevid.value}`, finishExists);
}

function finishExists(exists) {
    exists = JSON.parse(exists).exists;
    if (exists) {
        window.location.assign('../index.html');
    } else {
        document.querySelector('.elevid').MDCTextField.valid = false;
        document.querySelector('.skoleid').MDCTextField.valid = false;
    }
    el_progress.MDCLinearProgress.close()
}

function onchangeHuskMig() {
    updateStorage();
}

function extract() {
    let url = el_skemaurl.value;
    let res_elevid = re_elevid.exec(url);
    let res_skoleid = re_skoleid.exec(url);

    if (!(res_elevid && res_skoleid)) {
        document.querySelector('.skemaurl').MDCTextField.valid = false;
    } else {
        el_skoleid.value = res_skoleid[1];
        el_elevid.value = res_elevid[1];
        document.querySelector('.elevid label').classList.add('mdc-floating-label--float-above');
        document.querySelector('.skoleid label').classList.add('mdc-floating-label--float-above');
        clickBack();
    }
}

function updateStorage() {
    if (el_husk_mig.checked) {
        storage.setItem(el_elevid.id, el_elevid.value);
        storage.setItem(el_skoleid.id, el_skoleid.value);
        storage.setItem(el_husk_mig.id, el_husk_mig.checked);
    } else {
        storage.clear();
        storage.setItem(el_husk_mig.id, el_husk_mig.checked);
    }
}

function clickHelp() {
    document.querySelector('.login-switch').style.transform = 'translate(-400px, 0px)';
}

function clickBack() {
    document.querySelector('.login-switch').style.transform = 'translate(0px, 0px)';
}

window.extract = extract;
window.clickBack = clickBack;
window.clickHelp = clickHelp;
window.login = login;
window.onchangeHuskMig = onchangeHuskMig;
util.AddOnload(onload);