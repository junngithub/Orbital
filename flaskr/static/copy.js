function copy() {
    // Get the text field
    var copyText = document.getElementById("here").value
    document.getElementById("here").select()
    document.getElementById("here").setSelectionRange(0, 99999)
    navigator.clipboard.writeText(copyText)

    // Alert the copied text
    alert("Copied the text: " + copyText)
}