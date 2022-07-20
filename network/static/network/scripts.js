function buttons(id, user, posted_by, button){
    // Only do actions if the post is not posted by user logged in
    if(user===posted_by){
        alert(`You cannot ${button} your post!`)
    } else if(button==='like'){
        const likebutton = document.querySelectorAll('#like_button')
        fetch('home', {
            method:'PUT',
            body:JSON.stringify({
                userlogged:user,
                post:id,
            })
        })
        .then(response => response.json())
        .then(info => console.log(info))
    };}


