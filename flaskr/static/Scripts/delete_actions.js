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
    var select_all = document.getElementById("select-all")
    var boxes = document.querySelectorAll(".box")
    if (select_all.innerHTML == "Select All") {
        boxes.forEach(box => {
            box.checked = true
        })
        select_all.innerHTML = "Unselect All"
    } else {
        boxes.forEach(box => {
            box.checked = false
        })
        select_all.innerHTML = "Select All"
    }

}
