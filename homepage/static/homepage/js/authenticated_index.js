const contextMenuButton = document.querySelector("#context-menu-button")
document.body.addEventListener("click", (event) =>
{
    const contextMenu = document.querySelector("#context-menu")
    if (contextMenu)
    {
        const targetIsContextMenuButton = contextMenuButton === event.target
        const contextMenuButtonIncludesTarget = Array.from(contextMenuButton.children).includes(event.target)

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

const calendarTiles = document.querySelectorAll(".calendar-tile")
const createEventDialog = document.querySelector("#create-event-dialog")
for (const tile of calendarTiles)
{
    tile.addEventListener("click", event =>
    {
        if (!event.target.classList.contains("event-tile"))
        {
            console.log(tile.innerText,
                tile.dataset.month,
                tile.dataset.year
            )

            // if createEventDialog
            createEventDialog.showModal()
            // else
            // htmx.onLoad((_) => createEventDialog.showModal())
        }
    })
}

const showEventDialog = document.querySelector("#show-event-dialog")
function showEvent(eventTile)
{
    // if showEventDialog
    showEventDialog.showModal()
    // else
    // htmx.onLoad((_) => showEventDialog.showModal())
}