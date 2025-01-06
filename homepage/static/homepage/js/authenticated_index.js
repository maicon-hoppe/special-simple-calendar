const contextMenuButton = document.querySelector("#context-menu-button")
document.body.addEventListener("click", (event) =>
{
    const contextMenu = document.querySelector("#context-menu")
    if (contextMenu)
    {
        const targetIsContextMenuButton = contextMenuButton === event.target
        const contextMenuButtonIncludesTarget = Array.from(contextMenuButton.children).includes(event.target)

        if ( targetIsContextMenuButton || contextMenuButtonIncludesTarget )
        {
            contextMenu.hidden = !contextMenu.hidden
        }
        else
        {
            contextMenu.hidden = true
        }
    }
})

function createCalendarEvent(calendarTile)
{
    console.log(calendarTile.innerText, 
                calendarTile.dataset.month,
                calendarTile.dataset.year)

    const eventDialog = document.querySelector("#event-dialog")
    if (!eventDialog)
    {
        htmx.on("htmx:load", (event) => event.target.showModal())
    }
    else
    {
        eventDialog.showModal()
    }
}