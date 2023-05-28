///const electron = require("electron");
///const window.safeipc = window.safeipc;
let button = document.querySelector("input#open");
button.addEventListener("click", opensenddir);

window.safeipc.on("file:add", fileadd);
window.safeipc.on("file:clear", fileclear);

function opensenddir(e) {
    let odir = document.querySelector("input#directory").value;
    console.log(odir);
    window.safeipc.send("open:dir", odir);
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
