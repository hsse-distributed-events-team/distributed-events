function deleteStage(stage) {
    console.log("WHERE BANANA")
    fetch(document.URL + "delete",
         {
             method: "POST",
             body: JSON.stringify({
                stage_id: stage,
             }),
             headers: { "X-CSRFToken": getCookie("csrftoken") }
         }
    )
}

function createStage(next_stage) {
    fetch(document.URL + "create",
         {
             method: "POST",
             body: JSON.stringify({
                next_stage_id: next_stage,
             }),
             headers: { "X-CSRFToken": getCookie("csrftoken") }
         }
    )
}
const add_buttons = document.querySelectorAll(".stage__button_type_add")
const delete_buttons = document.querySelectorAll(".stage__button_type_delete")


for (const btn of add_buttons) {
    btn.addEventListener("click", () => {
        createStage(btn.getAttribute("stage_id"));
    })
}
for (const btn of delete_buttons) {
    btn.addEventListener("click", () => {
        deleteStage(btn.getAttribute("stage_id"));
    })
}

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}
