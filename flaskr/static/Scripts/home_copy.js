document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll(".copy-button")
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const list = this.closest('li')
            text = list.dataset.pw
            copy(text)
        })
    })
})