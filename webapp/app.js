function hideAll(){

document.querySelectorAll(".page")
.forEach(
page=>page.classList.add("hidden")
)

}



function home(){

hideAll()

document
.getElementById("home")
.classList.remove("hidden")

}



function markets(){

hideAll()

document
.getElementById("markets")
.classList.remove("hidden")

}



function commodities(){

hideAll()

document
.getElementById("commodities")
.classList.remove("hidden")

}



function crypto(){

alert("🪙 بخش کریپتو")

}