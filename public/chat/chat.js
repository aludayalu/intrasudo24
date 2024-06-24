import { Signal } from "/$.js";

const chatToggleBtn = document.getElementById("chatToggleBtn")
const chatPopup = document.getElementById("chatPopup")

var notyf = new Notyf();
var position = { x: "center", y: "top" }

const chatSignal = Signal("chatOpenState", "close")

chatSignal.onChange = () => {
    if (chatSignal.Value() === "open") {
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
    chatSignal.setValue("open")
})

chatCloseBtn.addEventListener("click", (e) => {
    chatSignal.setValue("close")
})

chatMinimizeBtn.addEventListener("click", (e) => {
    chatSignal.setValue("close")
})

document.getElementById("chatSendButton").addEventListener("click", async (x)=>{
    var text=document.getElementById("chatInput").value.trim().trim("\n")
    if (text!="") {
        document.getElementById("chatInput").value=""
        document.getElementById("chatMsgLen").innerText = "0"
        var response=await (await fetch("/submit_message?content="+encodeURIComponent(text))).json()
        if (response.error!=undefined) {
            notyf.error({ position: position, message: response.error })
        } else {
            ignore=true
            checksum.onChange()
        }
    }
})

document.getElementById("chatInput").oninput = (e) => {
    if(e.target.value.trim().length >= 512){
        chatInput.value = e.target.value.trim().slice(0, 512)
    }
    if(e.target.value.trim().length >= 400){
        document.getElementById("chatMsgCharLimit").style.color = "#f87171"
    } else{
        document.getElementById("chatMsgCharLimit").style.color = "#fff"
    }

    document.getElementById("chatMsgLen").innerText = e.target.value.trim().length
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
var first=true
var checksum=Signal("checksum", getCookie("checksum"))

function cookie_set(key, val) {
    try {
        document.cookie = `${key}=${val};expires=Thu, 01 Jan 2049 00:00:00 UTC`
    } catch { }
}

checksum.onChange=async ()=>{
    if (!ignore && !first) {
        if (chatSignal.Value()!="open") {
            notyf.success({ position: position, message: "You have got a new message!" })
        }
    }
    if (ignore) {
        ignore=false
    }
    cookie_set("checksum", checksum.Value())
    var request=(await (await fetch("/chats")).json())
    var chats=request["chats"]
    var hints=request["hints"]
    var final=chats.concat(hints)
    final.sort((a, b)=>{
        return a["time"] > b["time"] ? 1 : -1
    })
    console.log(final)
    document.getElementById("messagecontainer").innerHTML=""
    final.forEach((x)=>{
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
first=false

setInterval(async ()=>{
    checksum.setValue((await (await fetch("/chats_checksum")).json())["checksum"])
}, 5000)