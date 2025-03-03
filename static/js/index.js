// Selects all tasks in the list of tasks
tasks = [...document.getElementsByClassName('task')]

tasks.forEach(task => {
    // Creates a click event listener for each task
    task.querySelector('.task-info').addEventListener('click', evt => {
        // Displays edit menu
        task.querySelector('.edit-task').style.display = 'block'
    })

    task.querySelector('.close').addEventListener('click', evt => {
        task.querySelector('.edit-task').style.display = 'none'
    })
})