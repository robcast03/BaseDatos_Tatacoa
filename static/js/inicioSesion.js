const btnToggle =document.querySelector('.toggleButton')
console.log(btnToggle)

btnToggle.addEventListener('click', function(){
    document.getElementById('sidebar').classList.toggle('active');
})