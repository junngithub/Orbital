document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll(".copy")
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const row = this.closest('tr')
            text = row.cells[2].textContent
            copy(text)
        })
    })
})