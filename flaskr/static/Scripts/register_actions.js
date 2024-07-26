var lowercase = /[a-z]/g
var uppercase = /[A-Z]/g
var number = /[0-9]/g

document.addEventListener('DOMContentLoaded', function() {
    var pw_input = document.getElementById("password")
    var checklist = document.getElementById("requirements")
    var button = document.createElement("button")
    button.type = "submit"
    button.innerHTML = "Register"
    pw_input.onfocus = function() {
        checklist.style.display = "block"
        document.getElementById("msg").style.display = "none"
    }
    pw_input.onkeyup = function() {
        
        var low = document.getElementById("req-low")
        var upper = document.getElementById("req-upper")
        var num = document.getElementById("req-num")
        var len = document.getElementById("req-len")
        var passed = true
        if(pw_input.value.match(lowercase)) {
            low.innerHTML = "&#10003;" 
        } else {
            low.innerHTML = "&#10060;"
            passed = false
        }

        if(pw_input.value.match(uppercase)) {
            upper.innerHTML = "&#10003;" 
        } else {
            upper.innerHTML = "&#10060;"
            passed = false
        }

        if(pw_input.value.match(number)) {
            num.innerHTML = "&#10003;" 
        } else {
            num.innerHTML = "&#10060;"
            passed = false
        }

        if(pw_input.value.length >= 10) {
            len.innerHTML = "&#10003;" 
        } else {
            len.innerHTML = "&#10060;"
            passed = false
        }

        if (passed) {
            document.getElementById("requirements").style.display = "none"
            checklist.parentNode.insertBefore(button, checklist.nextSibling)
        } else {
            document.getElementById("requirements").style.display = "block"
            button.remove()
        }
    }   
})