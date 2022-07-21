function buttons(id, user, posted_by, button){
    // Only do actions if the post is not posted by user logged in
    if(user===posted_by){
        alert(`You cannot ${button} your post!`)
    } else if(button==='like'){
        fetch('home', {
            method:'PUT',
            body:JSON.stringify({
                userlogged:user,
                post:id,
            })
        })
        .then(window.location.reload())
    };}



function submit_post(){
    const post_content = document.querySelector('#post_content').value;
    const user_username = JSON.parse(document.getElementById('user_username').textContent);
    if(post_content){
        fetch('home',{
            method:'POST',
            body: JSON.stringify({
                posted_by:user_username,
                content: post_content
            })
        })
    }
}

if(document.querySelector('#user_profile')){
    document.querySelector('#user_profile').addEventListener('click', ()=> {user_profile})
}
    


function user_profile(){
    const user_username = JSON.parse(document.getElementById('user_username').textContent);
    fetch(`user/${user_username}`)
    .then(response => response.json())
    .then(user => {
        document.querySelector('#user').innerText = user_username
        document.querySelector('#followers').innerText = user.followers
        document.querySelector('#following').innerText = user.following

    })
}