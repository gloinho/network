document.querySelector('#allposts').addEventListener('click', ()=> {
    document.getElementById('posts').style.display = 'block'
    document.getElementById('title').style.display = 'block'
    document.getElementById('profile').style.display = 'none'
})

if(document.querySelector('#user_profile')){
    document.querySelector('#user_profile').addEventListener('click', ()=> user_profile(JSON.parse(document.getElementById('user_username').textContent)))
}
    
function user_profile(user){
    document.getElementById('posts').style.display = 'none'
    document.getElementById('title').style.display = 'none'
    document.getElementById('profile').style.display = 'block'
    const userlogged = JSON.parse(document.getElementById('user_username').textContent)
    const follow_button = document.getElementById('followbutton')
    if(userlogged != user){
        follow_button.style.display='block'
    }else{follow_button.style.display = 'none'}
    
    if(typeof(user)==='object'){
        user = user.posted_by
    }
    fetch(`user/${user}`)
    .then(response => response.json())
    .then(infos => {
        infos.map(info => {
            document.getElementById('user').innerText = user
            document.getElementById('followers').innerText = `Followers: ${info.followers.length}`
            document.getElementById('following').innerText = `Following: ${info.following.length}`
            document.getElementById('postings').innerText = `Postings: ${info.posts.length}`    
        })
        if(infos[0].followers.includes(userlogged)){
            document.getElementById('followbutton').innerText = 'Unfollow'
        } else{
            document.getElementById('followbutton').innerText = 'Follow'
        }
    })
}

