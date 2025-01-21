const contextMenuButton = document.querySelector("#context-menu-button")
document.body.addEventListener("click", (event) =>
{
    const contextMenu = document.querySelector("#context-menu")
    if (contextMenu)
    {
        const targetIsContextMenuButton = contextMenuButton === event.target
        const contextMenuButtonIncludesTarget = Array
            .from(contextMenuButton.children)
            .includes(event.target)
        if (targetIsContextMenuButton || contextMenuButtonIncludesTarget)
        {
            contextMenu.hidden = !contextMenu.hidden
        }
        else
        {
            contextMenu.hidden = true
        }
    }
})

const showEventDialog = document.querySelector("#show-event-dialog")
function showEvent() { showEventDialog.showModal() }

const eventListDialog = document.querySelector("#event-list-dialog")
function showEventList() { eventListDialog.showModal() }