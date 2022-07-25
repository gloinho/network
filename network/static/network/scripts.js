


document.querySelector('#allposts').addEventListener('click', ()=> {
    document.getElementById('posts').style.display = 'block'
    document.getElementById('title').style.display = 'block'
    document.getElementById('profile').style.display = 'none'
})




if(document.querySelector('#user_profile')){
    document.querySelector('#user_profile').addEventListener('click', ()=> {user_profile()})
}
    


function user_profile(){
    document.getElementById('posts').style.display = 'none'
    document.getElementById('title').style.display = 'none'
    document.getElementById('profile').style.display = 'block'
    const user_username = JSON.parse(document.getElementById('user_username').textContent);
    fetch(`user/${user_username}`)
    .then(response => response.json())
    .then(user => {
        console.log(user)

    })
}