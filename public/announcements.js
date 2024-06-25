import { Signal } from "/$.js";

const announcementsToggleBtn = document.getElementById("announcementsToggleBtn")
const announcementsPopup = document.getElementById("announcementsPopup")
const announcementsContainer = document.getElementById("announcementsContainer")

const announcementsSignal = Signal("announcementsOpenState", "close")

announcementsSignal.onChange = () => {
    if (announcementsSignal.Value() === "open") {
        announcementsPopup.style.display = "block"

        setTimeout(() => {
            announcementsPopup.style.opacity = 1
            announcementsPopup.style.transform = "translateY(0px)"
        }, 10);
    }
    else {
        announcementsPopup.style.opacity = 0
        announcementsPopup.style.transform = "translateY(-500px)"

        setTimeout(() => {
            announcementsPopup.style.display = "none"
        }, 400);
    }
}

announcementsToggleBtn.addEventListener("click", (e) => {
    announcementsSignal.setValue(announcementsSignal.Value() === "open" ? "close" : "open")
})

window.addEventListener("click", (e) => {
    if(!Array.from(announcementsPopup.querySelectorAll("*")).includes(e.target)){
        if(!Array.from(announcementsToggleBtn.querySelectorAll("*")).includes(e.target)){
            announcementsSignal.setValue("close")
        }
    }
})

announcementsContainer.innerHTML = announcement_item