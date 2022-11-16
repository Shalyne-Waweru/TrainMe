// Change Navbar Color when scroll value is greater than 100
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

// Tabs Navigation
let tabHeader = document.getElementsByClassName("tab-header")[0];
let tabIndicator = document.getElementsByClassName("tab-indicator")[0];
let tabBody = document.getElementsByClassName("tab-body")[0];

let tabsPane = tabHeader.getElementsByTagName("div");

for(let i=0; i<tabsPane.length; i++){
  tabsPane[i].addEventListener("click", function(){
    //Make The Headers Active On Click
    tabHeader.getElementsByClassName("active")[0].classList.remove("active");
    tabsPane[i].classList.add("active");

    //Add the Content Of The Specific Tabs
    tabBody.getElementsByClassName("active")[0].classList.remove("active");
    tabBody.getElementsByTagName("div")[i].classList.add("active");

    //Add the tab indicator
    tabIndicator.style.left = `calc(calc(100% / 3) * ${i})`;
  });
}

// When the user clicks on <div>, open the popup
// function openPopUp() {
//   let popup = document.getElementById("myPopup");
//   popup.classList.toggle("show");
// }

// function onButtonPress() {
//   // $('.alert').alert('close')
//   $('.alert').css("display", "none");
// }