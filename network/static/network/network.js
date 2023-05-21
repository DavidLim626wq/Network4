/*
function toggle_edit(id) {
    //toggles the appearance of the Edit Box;
    buttonString = document.querySelector(`#edit-button-${id}`).innerHTML;
    if (buttonString === "Edit Post") {
        document.querySelector(`#edit-button-${id}`).innerHTML = 'Cancel';
        document.querySelector(`#edit-container-${id}`).style.display = 'block';
        document.querySelector(`#post-body-${id}`).style.display = 'none';
    } else {
        document.querySelector(`#edit-button-${id}`).innerHTML = 'Edit Post';
        document.querySelector(`#edit-container-${id}`).style.display = 'none';
        document.querySelector(`#post-body-${id}`).style.display = 'block';
    }
}*/

function toggle_edit2(id) {
    //toggles the appearance of the Edit Box;
    buttonString = document.querySelector(`#edit-button-${id}`).innerHTML;
    editContainer = document.querySelector(`#edit-container-${id}`);
    currentText = document.querySelector(`#post-body-${id}`).innerText;
    const node = document.createElement("textarea");
            node.id = "edit-form";
            node.rows = "7";
            node.style = "resize: none;";
            node.innerHTML = currentText;

    var editExists = document.getElementById("edit-form");
    if (editExists === null){ //block two edit boxes from opening at the same time.
        if (buttonString === "Edit Post") {
            //opens an edit box if there are no other edit boxes
            document.querySelector(`#edit-button-${id}`).innerHTML = 'Cancel';
            editContainer.prepend(node);
            document.querySelector(`#edit-container-${id}`).style.display = 'block';
            document.querySelector(`#post-body-${id}`).style.display = 'none';
        } 
    } else { //if an edit form exists
        if (buttonString === "Cancel"){
            e = document.querySelector("#edit-form");
            e.remove();
            document.querySelector(`#edit-container-${id}`).style.display = 'none';
            document.querySelector(`#post-body-${id}`).style.display = 'block';
            document.querySelector(`#edit-button-${id}`).innerHTML = 'Edit Post';
        } else {
            alert("You are already editing another post");
        }
        
    }
}


function save_edit(id) {
    //toggles the appearance of the Edit Box
    e = document.querySelector("#edit-form");
    new_postBody = e.value;
    if (new_postBody.length === 0) {
        alert("Your post contains no text.");
    } else {
        fetch('/edit_post/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                post: e.value
            })
        });
        e = document.querySelector("#edit-form");
        e.remove();
        document.querySelector(`#post-body-${id}`).innerHTML = e.value;
        document.querySelector(`#edit-container-${id}`).style.display = 'none';
        document.querySelector(`#post-body-${id}`).style.display = 'block';
        document.querySelector(`#edit-button-${id}`).innerHTML = 'Edit Post';
        toggle_edit(id);
    }
}

function like(id) {

    fetch('/like/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                nlikes: document.querySelector(`#nlikes-${id}`).innerHTML
            })
        })
        .then(response => response.json())
        .then(x => {
            btnStr = x.btnState ? 'Like' : 'Unlike';
            document.querySelector(`#nlikes-${id}`).innerHTML = x.likes;
            document.querySelector(`#like-button-${id}`).innerHTML = btnStr;
        });
}

function get_like_button_state(id) {
    document.querySelector(`#like-button-${id}`).innerHTML = "BTZZT";
}

function follow(user) {

    fetch('/profile/' + user, {
        method: 'POST',
        body: JSON.stringify({
            user: user
        })
    });

    //handles some cosmetic changes when clicking on Follow/Unfollow
    button = document.querySelector(`#follow-button-${user}`);
    nFollowers = parseInt(document.querySelector("#nfollowers").textContent);
    newBtnLabel = (button.textContent === 'Unfollow') ? 'Follow' : 'Unfollow';
    if (button.textContent === 'Follow') {
        document.querySelector("#nfollowers").textContent = nFollowers + 1
    } else {
        document.querySelector("#nfollowers").textContent = nFollowers - 1
    }
    button.innerHTML = newBtnLabel;
}