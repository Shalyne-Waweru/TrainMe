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

// Messages Alert
function closeBtn(){
  document.querySelector(".alert").style.display = "none"
}

// Tabs Navigation
let tabHeader = document.getElementsByClassName("tab-header")[0];
let tabIndicator = document.getElementsByClassName("tab-indicator")[0];
let tabBody = document.getElementsByClassName("tab-body")[0];

let tabsPane = tabHeader.getElementsByTagName("section");

for(let i=0; i<tabsPane.length; i++){
  tabsPane[i].addEventListener("click", function(){
    //Make The Headers Active On Click
    tabHeader.getElementsByClassName("active")[0].classList.remove("active");
    tabsPane[i].classList.add("active");

    //Add the Content Of The Specific Tabs
    tabBody.getElementsByClassName("active")[0].classList.remove("active");
    tabBody.getElementsByTagName("section")[i].classList.add("active");

    //Add the tab indicator
    tabIndicator.style.left = `calc(calc(100% / 3) * ${i})`;
  });
}

// Toggle Clinic Form
function showClinicForm(){
  let form = document.querySelector(".clinic-form");

  if(form.style.display === "none"){
    form.style.display = "block";
  }

  else {
    form.style.display = "none";
  }
}

// Hide Clinic Form After Save
function hideClinicForm(){
  document.querySelector(".clinic-form").style.display = "none";
}

// Toggle Business Hours Form
function showHoursForm(){
  let form = document.querySelector(".hours-form");

  if(form.style.display === "none"){
    form.style.display = "block";
  }

  else {
    form.style.display = "none";
  }
}

// Hide Hours Form After Save
function hideHoursForm(){
  document.querySelector(".hours-form").style.display = "none";
}

// Opening Status
function checkStatus(){
  let checkBox = document.querySelector("#open_closed")

  if(checkBox.checked){
    document.querySelector(".status-title").innerHTML = "Open"
  }
  else{
    document.querySelector(".status-title").innerHTML = "Closed"
  }
}
