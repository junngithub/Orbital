function get_checked() {
    var checked = document.querySelectorAll(".box:checked")
    var arr = []
    checked.forEach(element => {
        arr.push(element.getAttribute("id"))
    })
    send = document.getElementById("arr")
    send.value = arr
}

function check_all(e) {
    e.preventDefault()
    var boxes = document.querySelectorAll(".box")
    boxes.forEach(box => {
        box.checked = true
    })
}
