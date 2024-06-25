document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById("gen").value == "Generate Again?") {
        document.getElementById("gen").type = "reset"
        document.getElementById("gen").onclick = function () {
            location.replace(document.getElementById("form").dataset.defaultlocation)
        }
        document.getElementById("box").remove()
        document.getElementById("box_label").remove()
        document.getElementById("copy").style = 'display: "";'
        document.getElementById("copy").onclick = function () { generate_copy() }
        add = document.createElement("button")
        add.type = "button"
        add.innerHTML = "Quick Add"
        add.onclick = function() { show() }
        add.id = "add"
        document.body.appendChild(add)
    }
})

function generate_copy() {
    // Get the text field
    var copyText = document.getElementById("here").value
    document.getElementById("here").select()
    document.getElementById("here").setSelectionRange(0, 99999)
    copy(copyText)
}