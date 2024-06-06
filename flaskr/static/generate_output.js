function output() {
    document.getElementById("txt").innerHTML = "Password Generated: "
    document.getElementById("here").value = JSON.parse(document.getElementById("form").dataset.pw)
    document.getElementById("gen").value = "Generate Again?"
    document.getElementById("gen").onclick = function () {
        window.location.reload()
    }
    document.getElementById("copy").style = 'display: "";'
    document.getElementById("copy").onclick = function () { copy() }
    add = document.createElement("button")
    add.type = "button"
    add.innerHTML = "Quick Add"
    add.onclick = function() { show() }
    add.id = "add"
    document.body.appendChild(add)  
}