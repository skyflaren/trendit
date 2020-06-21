let searchBar = document.getElementById("example");
let moon = document.getElementById("moon");

let enter, leave;

searchBar.addEventListener("mouseenter", function(){
    console.log("itworks");
    var pos = moon.style.marginRight.replace('px', '');
    clearInterval(leave);
    clearInterval(enter);
    enter = setInterval(function(){
        if(pos>233){
            clearInterval(enter);
        }
        else{
            pos++;
            moon.style.marginRight = pos + 'px';
        }
    }, 20);
})


searchBar.addEventListener("mouseleave", function(){
    console.log("itLEAVES");
    var pos = moon.style.marginRight.replace('px', '');
    clearInterval(enter);
    clearInterval(leave);
    leave = setInterval(function(){
        if(pos<50){
            clearInterval(leave);
        }
        else{
            pos--;
            moon.style.marginRight = pos + 'px';
        }
    }, 20);
})