document.addEventListener('DOMContentLoaded', function() {       
    const editButtons = document.querySelectorAll('.edit-button');
    editButtons.forEach(button => {
        const postId = button.getAttribute('id').split('-')[2];
        button.addEventListener('click', () => editPost(postId));
    });
  
    const saveButtons = document.querySelectorAll('.save-button');
    saveButtons.forEach(button => {
        const postId = button.getAttribute('id').split('-')[2];
        button.addEventListener('click', () => savePost(postId));
    });

    const likeButtons = document.querySelectorAll('.like-button');
    likeButtons.forEach(button => {
        const postID = button.getAttribute('id').split('-')[2];
        button.addEventListener('click', () => likePost(postID));
    })

    const dislikeButtons = document.querySelectorAll('.dislike-button');
    dislikeButtons.forEach(button => {
        const postID = button.getAttribute('id').split('-')[2];
        button.addEventListener('click', () => dislikePost(postID));
    })
});


function editPost(postId) {
    const postContentElement = document.querySelector(`#post-content-${postId}`);
    const editContentElement = document.querySelector(`#edit-content-${postId}`);
    const editButton = document.querySelector(`#edit-button-${postId}`);
    const saveButton = document.querySelector(`#save-button-${postId}`);
    const edited = document.querySelector(`#edited-${postId}`);

    postContentElement.style.display = 'none';
    editContentElement.style.display = 'block';
    editContentElement.value = postContentElement.innerText;
    editButton.style.display = 'none';
    saveButton.style.display = 'block';
    edited.style.display = 'none';
}

  
function savePost(postId) {
    const editContentElement = document.querySelector(`#edit-content-${postId}`);
    const postContentElement = document.querySelector(`#post-content-${postId}`);
    const editButton = document.querySelector(`#edit-button-${postId}`);
    const saveButton = document.querySelector(`#save-button-${postId}`);
    const edited = document.querySelector(`#edited-${postId}`);

    const updatedContent = editContentElement.value;      
    
    fetch(`/update_post/${postId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'       
        },
        body: JSON.stringify({
            post_content: updatedContent              
        })
    })
    .then(response => {
    if (response.ok) {
        return response.json();
    } else {
        throw new Error('Failed to update post');
    }
    })
    .then(result => {        
    postContentElement.innerText = updatedContent;  
    
    postContentElement.style.display = 'block';
    editContentElement.style.display = 'none';
    editButton.style.display = 'block';
    saveButton.style.display = 'none';
    edited.style.display = 'block';
    
    })
    .catch(error => {
    console.error(error);
    });
}


function likePost(postId) {      
    fetch(`/like_post/${postId}`, {
        method: 'POST',
        body: JSON.stringify({})
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to like post');
        }
    })
    .then(result => {            
        const likeCountElement = document.querySelector(`#like-count-${postId}`);
        likeCountElement.textContent = result.likecount;

    })
    .catch(error => {
        console.error(error);
    });
} 

         
function dislikePost(postId) {         
    fetch(`/dislike_post/${postId}`, {
        method: 'POST',
        body: JSON.stringify({})
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to dislike post');
        }
    })
    .then(result => {        
        const likeCountElement = document.querySelector(`#like-count-${postId}`);
        likeCountElement.textContent = result.likecount;      
    })
    .catch(error => {
        console.error(error);
    });
}
               
// test

// fetch(`/get_post/15`)
// .then(response => response.json())
// .then(result => {
//     console.log(result);
// })
// .catch(error => {
//     console.log('Error:', error);
// });

