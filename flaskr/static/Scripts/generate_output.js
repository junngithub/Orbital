function output() {
    document.getElementById("txt").innerHTML = "Password Generated: "
    document.getElementById("here").value = JSON.parse(document.getElementById("form").dataset.pw)
    document.getElementById("gen").value = "Generate Again?"
    document.getElementById("gen").onclick = function () {
        window.location.reload()
    }
    document.getElementById("copy").style = 'display: "";'
    document.getElementById("copy").onclick = function () { generate_copy() }
    add = document.createElement("button")
    add.type = "button"
    add.innerHTML = "Quick Add"
    add.onclick = function() { show() }
    add.id = "add"
    document.body.appendChild(add)  
}

function generate_copy() {
    // Get the text field
    var copyText = document.getElementById("here").value
    document.getElementById("here").select()
    document.getElementById("here").setSelectionRange(0, 99999)
    copy(copyText)
}