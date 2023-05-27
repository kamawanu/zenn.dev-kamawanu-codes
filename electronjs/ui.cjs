///const electron = require("electron");
const ipcRenderer = window.safeipc;
let button = document.querySelector("input#open");
button.addEventListener("click", opensenddir);

ipcRenderer.on("file:add", fileadd);
ipcRenderer.on("file:clear", fileclear);

function opensenddir(e) {
    let odir = document.querySelector("input#directory").value;
    console.log(odir);
    ipcRenderer.send("open:dir", odir);
}
function fileadd(e, n) {
    //console.log(e);
    //console.log(n);
    let _placement = document.querySelector("div#log");
    _placement.innerHTML += n + "<BR>";
}
function fileclear(e) {
    let _placement = document.querySelector("div#log");
    _placement.innerHTML = "";

}
