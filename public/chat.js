import { Signal } from "/$.js";

const chatToggleBtn = document.getElementById("chatToggleBtn")
const chatPopup = document.getElementById("chatPopup")


const signal = Signal("chatOpenState", "close")

signal.onChange = () => {
    if (signal.Value() === "open") {
        chatPopup.style.display = "flex"

        chatToggleBtn.style.opacity = 0
        chatToggleBtn.style.transform = "scale(0)"

        setTimeout(() => {
            chatPopup.style.opacity = 1
            chatPopup.style.transform = "translateY(0px)"
            chatToggleBtn.style.display = "none"
        }, 10);

        const messagecontainer = document.getElementById("messagecontainer")
        setTimeout(() => {
            messagecontainer.scrollTop = messagecontainer.scrollHeight
        }, 200)
    }
    else {
        chatToggleBtn.style.display = "block"

        chatPopup.style.opacity = 0
        chatPopup.style.transform = "translateY(900px)"

        setTimeout(() => {
            chatPopup.style.display = "none"

            chatToggleBtn.style.opacity = 1
            chatToggleBtn.style.transform = "scale(1)"
        }, 400);
    }
}

chatToggleBtn.addEventListener("click", (e) => {
    signal.setValue("open")
})

chatCloseBtn.addEventListener("click", (e) => {
    signal.setValue("close")
})

chatMinimizeBtn.addEventListener("click", (e) => {
    signal.setValue("close")
})

document.getElementById("chatInput").oninput=(x)=>{
    if (x.target.value.includes("\n")) {
        console.log("hi")
    }
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return "";
}

var ignore=false
var checksum=Signal("checksum", getCookie("checksum"))

function cookie_set(key, val) {
    try {
        document.cookie = `${key}=${val};expires=Thu, 01 Jan 2049 00:00:00 UTC`
    } catch { }
}

checksum.onChange=async ()=>{
    if (ignore) {
        ignore=false
    }
    cookie_set("checksum", checksum.Value())
    var chats=(await (await fetch("/chats")).json())["chats"]
    document.getElementById("messagecontainer").innerHTML=""
    chats.forEach((x)=>{
        if (x["author"]=="Exun Clan") {
            document.getElementById("messagecontainer").innerHTML+=messageMe.replace("{content}", x["content"])
        } else {
            document.getElementById("messagecontainer").innerHTML+=messageYou.replace("{content}", x["content"])
        }
    })
    setTimeout(() => {
        messagecontainer.scrollTop = messagecontainer.scrollHeight
    }, 200)
}

checksum.setValue((await (await fetch("/chats_checksum")).json())["checksum"])
checksum.onChange()

setInterval(async ()=>{
    checksum.setValue((await (await fetch("/chats_checksum")).json())["checksum"])
}, 5000)