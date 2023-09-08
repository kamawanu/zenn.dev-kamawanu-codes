///const electron = require("electron");
///const window.safeipc = window.safeipc;
const button = document.querySelector("input#open");
button.addEventListener("click", opensenddir);

window.safeipc.on("add", fileadd);
window.safeipc.on("clear", fileclear);

function opensenddir(e) {
    const odir = document.querySelector("input#directory").value;
    console.log(odir);
    window.safeipc.send("dir", odir);
}
function fileadd(e, n) {
    //console.log(e);
    //console.log(n);
    const _placement = document.querySelector("div#log");
    _placement.innerHTML += n + "<BR>";
}
function fileclear(e) {
    const _placement = document.querySelector("div#log");
    _placement.innerHTML = "";

}
