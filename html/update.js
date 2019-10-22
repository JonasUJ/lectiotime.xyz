let localStorage = window.localStorage;
let offsetMinutes = 0;
let offsetHours = 2;
let offsetDays = 0;
let n = 0;
let modules = [];
let loop, par, bar, barpro, ulmod, modcont, hours, minutes, seconds, start, end, schoolid, user, pwd;

function httpPostAsync(callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("POST", `https://api.lectiotime.xyz/today?schoolid=${schoolid.value}&user=${user.value}&pwd=${pwd.value}`, true);
    // xmlHttp.open("POST", `http://127.0.0.1:5000/today?schoolid=${schoolid.value}&user=${user.value}&pwd=${pwd.value}`, true);
    xmlHttp.send(null);
}

function offsetDate() {
    let dn = new Date();
    dn.setHours(dn.getHours() + offsetHours);
    dn.setDate(dn.getDate() + offsetDays);
    dn.setMinutes(dn.getMinutes() + offsetMinutes);
    return dn;
}

function calcTime(d1, d2) {
    let diff = d2 - d1;
    let h = Math.floor(diff / (1000 * 60 * 60));
    let m = Math.floor(diff / (1000 * 60)) - h * 60;
    let s = Math.floor(diff / 1000) - m * 60 - h * 60 * 60;
    return diff > 0 ? [h, m, s] : [0, 0, 0];
}

function calcTimeStr(d1, d2) {
    let times = calcTime(d1, d2);
    return `${times[0]}:${("0" + times[1]).substr(-2, 2)}:${("0" + times[2]).substr(-2, 2)}`;
}

function setTitle(per, dn) {
    document.title = `${per}% ${calcTimeStr(dn, end)}`;
}

function init(resp) {
    let today = JSON.parse(resp);
    start = new Date(today.start);
    end = new Date(today.end);

    let dn = offsetDate();
    modcont.setAttribute("data-title", "Skema: " + dn.toDateString());

    while (ulmod.firstChild) {
        ulmod.removeChild(ulmod.firstChild);
    }

    const amt_pieces = Object.keys(today).length - 4;
    for (let i = 0; i < amt_pieces; i++) {
        let mod = document.createElement("li");
        mod.className = "module";
        mod.style = "--progress: 0%"
        mod.setAttribute("data-title", today[i].Hold);
        mod.setAttribute("data-title-time", today[i].Hold + " " + calcTimeStr(dn, end));
        mod.setAttribute("data-progress", "0%");
        mod.start = new Date(today[i].start);
        mod.end = new Date(today[i].end);

        let room = document.createElement("div");
        room.innerText = "Lokale: " + (today[i].Lokaler != undefined ? today[i].Lokaler : today[i].Lokale)
        mod.appendChild(room);

        let teacher = document.createElement("div");
        teacher.innerText = "Lærer: " + today[i].Lærer
        mod.appendChild(teacher);

        modules.push(mod)
        ulmod.appendChild(mod);
    }

    update();
    loop = setInterval(update, 1000);
}

function updateTimer(hms) {
    hours.innerText = hms[0];
    minutes.innerText = ("0" + hms[1]).substr(-2, 2);
    seconds.innerText = ("0" + hms[2]).substr(-2, 2);
}

function percent(dstart, dnow, dend) {
    let passed = dnow - dstart;
    let total = dend - dstart;
    let p = (passed >= 0 ? passed : 0) / (total <= 0 ? 1 : total) * 100;
    return p > 100 ? 100 : p;
}

function update() {
    let dn = offsetDate();
    n = percent(start, dn, end);

    let hms = calcTime(dn, end);

    if (n >= 100) {
        n = 100;
        hms = [0, 0, 0];
        clearInterval(loop);
    }

    updateTimer(hms);

    modules.forEach((modul) => {
        let mn = percent(modul.start, dn, modul.end);
        mn = Math.floor(mn * 10) / 10
        modul.style = `--progress: ${mn >= 0 ? mn : 0}%`
        modul.setAttribute("data-progress", mn + "%");
        modul.setAttribute("data-title-time", modul.getAttribute("data-title") + " " + calcTimeStr(dn, modul.end));
    })

    n = Math.floor(n * 10) / 10
    bar.style = "--progress: " + n + "%"
    par.setAttribute("data-percent", n);
    barpro.style = `--percent: ${n}`;
    setTitle(n, dn);
}

function onload() {
    bar = document.getElementsByClassName("bar")[0];
    barpro = document.getElementsByClassName("barProgress")[0];
    par = document.getElementsByClassName("percent")[0];
    ulmod = document.getElementsByTagName("ul")[0];
    modcont = document.getElementsByClassName("moduleContainer")[0];
    hours = document.getElementsByClassName("hours")[0];
    minutes = document.getElementsByClassName("minutes")[0];
    seconds = document.getElementsByClassName("seconds")[0];
    schoolid = document.getElementsByClassName("schoolid")[0];
    user = document.getElementsByClassName("user")[0];
    pwd = document.getElementsByClassName("pwd")[0];
    let sid = Windows.localStorage.getItem("skoleid");
    if (sid) {
        schoolid.value = sid;
    }
}

function login() {
    Windows.localStorage.setItem("skoleid", schoolid.value);
    httpPostAsync(init)
}
