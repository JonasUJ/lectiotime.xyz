storage = window.localStorage;
let el_elevid, el_skoleid, el_husk_mig

function onload() {
    el_elevid = document.getElementById('elevid');
    el_skoleid = document.getElementById('skoleid');
    el_husk_mig = document.getElementById('husk-mig');

    el_elevid.value = storage.getItem(el_elevid.id)
    el_skoleid.value = storage.getItem(el_skoleid.id)
    el_husk_mig.check = storage.getItem(el_husk_mig.id)
}

function login() {
    updateStorage();
    window.location = "../index.html";
}

function onchangeHuskMig() {
    updateStorage();
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