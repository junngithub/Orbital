function copy(copyText) {
    navigator.clipboard.writeText(copyText)

    // Alert the copied text
    alert("Copied the text: " + copyText)
}