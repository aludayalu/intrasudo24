import { Signal } from "/$.js";

const signupBtn = document.getElementById("signup")
const submitBtn = document.getElementById("submit")

const authTxt = document.getElementById("authTxt")

const signal = Signal("authstate", "login")

function isValidEmail(email) {
    const pattern = /^[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)?@dpsrkp\.net$/;
    return pattern.test(email);
}

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
    signal.setValue(signal.Value() === "signup" ? "login" : "signup")
})

var notyf = new Notyf();
var position = { x: "center", y: "top" }

function cookie_get(key) {
    try {
        var cookies = {}
        for (var x in document.cookie.split("; ")) {
            var raw_data = document.cookie.split("; ")[x].split("=")
            cookies[raw_data[0]] = raw_data[1]
        }
        if (key in cookies) {
            return cookies[key]
        }
        return ""
    } catch {
        return ""
    }
}

function cookie_set(key, val) {
    try {
        document.cookie = `${key}=${val};expires=Thu, 01 Jan 2049 00:00:00 UTC`
    } catch { }
}

submitBtn.addEventListener("click", () => {
    var name = document.getElementById("name").value.trim()
    var email = document.getElementById("email").value.trim()
    var password = document.getElementById("password").value.trim()
    var otp = "1234"
    if (signal.Value() == "signup") {
        if (name.length == 0) {
            notyf.error({ position: position, message: "Name field is required" })
            return
        }
    }
    if (signal_otp.Value() == "otpscreen") {
        if (otp.length != 6 || Number(otp)==NaN) {
            notyf.error({ position: position, message: "OTP format is invalid" })
            return
        }
    }
    if (email.length == 0) {
        notyf.error({ position: position, message: "Email field is required" })
        return
    }
    if (!isValidEmail(email)) {
        notyf.error({ position: position, message: "Kindly login with valid dpsrkp.net accounts" })
        return
    }
    if (password.length == 0) {
        notyf.error({ position: position, message: "Password field is required" })
        return
    }
    if (signal_otp.Value()=="signup" && signal.Value()=="signup") {
        signal_otp.setValue("otpscreen")
        signupBtn.style.display="none"
        return
    }
    fetch("/api/auth?name=" + encodeURIComponent(name) + "&email=" + encodeURIComponent(email) + "&password=" + encodeURIComponent(password) + "&otp=" + otp).then(async (x) => {
        var out = await x.text()
        try {
            var json = JSON.parse(out)
        } catch {
            var json = false
        }
        if (json != false && json.success !== undefined) {
            notyf.success({ position: position, message: "Successfully Authenticated" })
            setTimeout(() => {
                cookie_set("email", email)
                cookie_set("password", password)
                window.location = "/"
            }, 1000)
        } else {
            notyf.error({ position: position, message: "Authentication Failed: " + out })
        }
    })
})



const otpform_container = document.getElementById("otpform_container");
const inputList = document.getElementById("inputList")


const signal_otp = Signal("otpScreen", "signup")

signal_otp.onChange = () => {
    if (signal_otp.Value() === "otpscreen") {
        otpform_container.style.display = "block"
        otpform_container.opacity = 0
        otpform_container.scale = 0
        inputList.style.display = "none"

        setTimeout(() => {
            otpform_container.opacity = 1
            otpform_container.scale = 1
        }, 400);
    }
}


const form = document.getElementById('otp-form')
const inputs = [...form.querySelectorAll('input[type=number]')]
const submit = form.querySelector('#submit')

const handleKeyDown = (e) => {
    if (
        !/^[0-9]{1}$/.test(e.key)
        && e.key !== 'Backspace'
        && e.key !== 'Delete'
        && e.key !== 'Tab'
        && !e.metaKey
    ) {
        e.preventDefault()
    }

    if (e.key === 'Delete' || e.key === 'Backspace') {
        const index = inputs.indexOf(e.target);
        inputs[index].value = '';
        if (index > 0) {
            setTimeout(() => {
                inputs[index - 1].focus();
            }, 100)
        }

    }
}

const handleInput = (e) => {
    const { target } = e
    const index = inputs.indexOf(target)
    if (e.key === 'Delete' || e.key === 'Backspace') {
        return
    }
    if (target.value) {
        if (index < inputs.length - 1) {
            inputs[index + 1].focus()
        } else {
            if (index === inputs.length - 1) {
                try {
                    e.target.value = e.target.value[0]
                }
                catch {
                }
            }
        }
    }
}

const handleFocus = (e) => {
    e.target.select()
}

const handlePaste = (e) => {
    e.preventDefault()
    const text = e.clipboardData.getData('text')
    if (!new RegExp(`^[0-9]{${inputs.length}}$`).test(text)) {
        return
    }
    const digits = text.split('')
    inputs.forEach((input, index) => input.value = digits[index])
    submit.focus()
}

inputs.forEach((input) => {
    input.addEventListener('input', handleInput)
    input.addEventListener('keydown', handleKeyDown)
    input.addEventListener('focus', handleFocus)
    input.addEventListener('paste', handlePaste)
})