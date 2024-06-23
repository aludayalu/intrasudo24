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

    }
}

chatToggleBtn.addEventListener("click", () => {
    signal.setValue(signal.Value() === "close" ? "open" : "close")
})