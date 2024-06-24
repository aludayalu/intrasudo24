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
        chatToggleBtn.style.opacity = 1
        chatToggleBtn.style.transform = "scale(1)"
        setTimeout(() => {
            chatPopup.style.opacity = 0
            chatPopup.style.transform = "translateY(0px)"
            chatPopup.style.display = "none"
            chatToggleBtn.style.display = "block"
        }, 200);
    }
}

document.addEventListener("click", (e)=>{
    console.log("hi")
    if (document.getElementById("chatPopup").contains(e.target)) {
        console.log("inside")
    } else {
        if (document.getElementById("btn-message").contains(e.target)) {
            signal.setValue("open")
        } else {
            signal.setValue("close")
        }
    }
})