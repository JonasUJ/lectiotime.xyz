const url = "http://142.93.35.88:5500/today?school_id=680&elev_id=21640110194";
const offsetHours = 1;

let n = 0;
let modules = [];
let loop, par, bar, ulmod, modcont, hours, minutes, seconds, start, end;

function httpGetAsync(url, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", url, true);
    xmlHttp.send(null);
}

function offsetDate() {
    let dn = offsetDate();
    dn.setHours(dn.getHours() + offsetHours);
    return dn;
}

function calcTime(d1, d2) {
    let diff = d2 - d1;
    let h = Math.floor(diff / (1000 * 60 * 60));
    let m = Math.floor(diff / (1000 * 60)) - h * 60;
    let s = Math.floor(diff / 1000) - m * 60 - h * 60 * 60;
    return [h, m, s];
}

function calcTimeStr(d1, d2) {
    let times = calcTime(d1, d2);
    return `${times[0]}:${("0" + times[1]).substr(-2, 2)}:${("0" + times[2]).substr(-2, 2)}`;
}

function init(resp) {
    let today = JSON.parse(resp);
    start = new Date(today.start);
    end = new Date(today.end);

    let dn = offsetDate();
    modcont.setAttribute("title", "Skema: " + dn.toDateString());

    const amt_pieces = Object.keys(today).length - 3;
    for (let i = 0; i < amt_pieces; i++) {
        let mod = document.createElement("li");
        mod.className = "module";
        mod.style = "--progress: 0%"
        mod.setAttribute("title", today[i].Hold);
        mod.setAttribute("title-time", today[i].Hold + " " + calcTimeStr(dn, end));
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
        modul.setAttribute("title-time", modul.title + " " + (modul.end - dn >= 0 ? calcTimeStr(dn, modul.end) : "0:00:00"));
    })

    n = Math.floor(n * 10) / 10
    bar.style = "--progress: " + n + "%"
    par.setAttribute("data-percent", n);
}

function onload() {
    bar = document.getElementsByClassName("bar")[0];
    par = document.getElementsByClassName("percent")[0];
    ulmod = document.getElementsByTagName("ul")[0];
    modcont = document.getElementsByClassName("moduleContainer")[0];
    hours = document.getElementsByClassName("hours")[0];
    minutes = document.getElementsByClassName("minutes")[0];
    seconds = document.getElementsByClassName("seconds")[0];

    httpGetAsync(url, init)
}

window.addEventListener("load", onload);