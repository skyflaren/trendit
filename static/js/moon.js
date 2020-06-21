let submit = document.getElementById("submit");
let moon = document.getElementById("moon");

let enter, leave;
let moonStart = moon.style.marginRight;
let moonStartY = moon.style.marginTop;

var pos = moon.style.marginRight;
var posY = -30.095;


submit.addEventListener("mouseenter", function(){

    console.log("itworks");
    clearInterval(leave);
    clearInterval(enter);
    enter = setInterval(function(){
        console.log(moonStartY);
        if(pos>26){
            clearInterval(enter);
        }
        else{
            pos++;
            posY = (Math.sqrt(600-(pos-4)*(pos-4)));
            moon.style.marginRight = pos + 'vw';
            moon.style.marginTop = posY-11.80 - 27 + 'vw';
            moon.style.marginBottom = -posY-3.20 +27 + 'vw';
        }
    }, 15);
})


submit.addEventListener("mouseleave", function(){
    console.log("itLEAVES");
    clearInterval(leave);
    clearInterval(enter);
    leave = setInterval(function(){
        console.log(moonStartY);
        if(pos<=0){
            console.log("NIHAOMAT");
            clearInterval(leave);
        }
        else{
            pos-- ;
            posY = (Math.sqrt(600-(pos-4)*(pos-4)));
            moon.style.marginRight = pos + 'vw';
            moon.style.marginTop = posY-11.80 - 27 + 'vw';
            moon.style.marginBottom = -posY-3.20 +27 + 'vw';
        }
    }, 15);
})