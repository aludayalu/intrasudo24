import { Signal } from "/$.js";

const signupBtn = document.getElementById("signup")
const submitBtn = document.getElementById("submit")

const authTxt = document.getElementById("authTxt")

const signal = Signal("authstate", "signup")

signal.onChange = () => {
    const temp = authTxt.innerHTML;
    authTxt.innerHTML = temp === "Signup" ? "Login" : "Signup";
    signupBtn.innerHTML = temp !== "Signup" ? "Login" : "Signup"


    if (temp === "Login") {
        document.getElementById("name").style.transform = "scale(0)";
        document.getElementById("name").style.opacity = "0";

        setTimeout(() => {
            document.getElementById("name").style.transform = "scale(1)";
            document.getElementById("name").style.opacity = "1";
        }, 100);
    }
    if (temp === "Signup") {
        document.getElementById("name").style.transform = "scale(0)";
        document.getElementById("name").style.opacity = "0";
    }
}

signupBtn.addEventListener("click", () => {
    signal.setValue(signal.Value === "signup" ? "signin" : "signup")
})
