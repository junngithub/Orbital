document.addEventListener('DOMContentLoaded', function() {
    var gen_button = document.getElementById("gen")
    if (gen_button.value == "Generate Again?") {
        gen_button.type = "submit"

        gen_button.onclick = function () {
            window.location.reload()
        }

        var copy_button = document.getElementById("copy")
        copy_button.style = 'display: "";'
        copy_button.onclick = function () { generate_copy() }
        add = document.createElement("input")
        add.type = "button"
        add.value = "Quick Add"
        add.onclick = function() { show() }
        add.id = "add"
        copy_button.parentNode.insertBefore(add, copy_button.nextSibling)
    }
})

function generate_copy() {
    // Get the text field
    var copyText = document.getElementById("generated-password").textContent
    copy(copyText)
}