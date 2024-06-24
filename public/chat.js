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