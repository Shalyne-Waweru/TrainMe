function changeBg(){
  let navbar = document.getElementById('navbar')
  let scrollValue = window.scrollY;

  if(scrollValue < 100){
    navbar.classList.remove('navColor')
  }
  else {
    navbar.classList.add('navColor')
  }
  
}

window.addEventListener('scroll', changeBg);

