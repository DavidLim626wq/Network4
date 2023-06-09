function toggle_edit2(id) {
    //toggles the appearance of the Edit Box;
    buttonString = document.querySelector(`#edit-button-${id}`).innerHTML;
    editContainer = document.querySelector(`#edit-container-${id}`);
    currentText = document.querySelector(`#post-body-${id}`).innerText;
    //only a single TextArea can exist at a time, because only one post is edited at a time.
    const node = document.createElement("textarea");
            node.id = "edit-form";
            node.rows = "6";
            node.maxLength = "500";
            node.style = "resize: none;";
            node.innerHTML = currentText;

    var editExists = document.getElementById("edit-form");
    if (editExists === null){ //block two edit boxes from opening at the same time.
        if (buttonString === "Edit Post") {
            //opens an edit box if there are no other edit boxes
            document.querySelector(`#edit-button-${id}`).innerHTML = 'Cancel';
            document.querySelector(`#edit-icon-${id}`).setAttribute("src", "/static/images/cancel.png");
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
            document.querySelector(`#edit-icon-${id}`).setAttribute("src", "/static/images/edit.png");
        } else {
            displayAlert("You are already editing another post.");
        }
        
    }
}

function save_edit(id) {
    //toggles the appearance of the Edit Box
    e = document.querySelector("#edit-form");
    new_postBody = e.value;
    if (new_postBody.length === 0) {
        displayAlert("Your post contains no text.");;
    } else {
        fetch('/edit_post/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                post: e.value
            })
        });
        document.querySelector("#edit-form").remove;
        document.querySelector(`#post-body-${id}`).innerHTML = e.value;
        document.querySelector(`#edit-container-${id}`).style.display = 'none';
        document.querySelector(`#post-body-${id}`).style.display = 'block';
        document.querySelector(`#edit-button-${id}`).innerHTML = 'Edit Post';
        toggle_edit(id);
    }
}

function deletePost(id){
    e = document.querySelector(`#post-container-${id}`);
    console.log(e);
    fetch('/delete/' + id, {
        method: 'PUT',
        body: JSON.stringify({
            post: e.value
        })
    });
    //remove post container
    e.remove();
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
        const newFollowers = nFollowers + 1;
        document.querySelector("#nfollowers").textContent = nFollowers == 1 ? newFollowers + " people" : newFollowers + " person";
    } else {
        const newFollowers = nFollowers - 1;
        const newStr = nFollowers == 1 ? newFollowers + " people" : newFollowers + " person";
        document.querySelector("#nfollowers").textContent = nFollowers == 1 ? newFollowers + " people" : newFollowers + " person";
    }
    button.innerHTML = newBtnLabel;
}

function displayAlert(alertString){
    var x = document.getElementById("alertBox");
    x.className = "show";
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
    x.innerHTML = alertString;
}