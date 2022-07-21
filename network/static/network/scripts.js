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
    const user_id = JSON.parse(document.getElementById('user_id').textContent);
    if(post_content){
        fetch('home',{
            method:'POST',
            body: JSON.stringify({
                posted_by:user_id,
                content: post_content
            })
        })
    }
}


