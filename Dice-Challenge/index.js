var randomNumber1 = Math.floor(Math.random() * 6) +1;

randomDiceImage = "dice" + randomNumber1 + ".png";
var randomImageSource = "images/" + randomDiceImage;
var img1 = document.querySelectorAll("img")[0];
img1.setAttribute("src", randomImageSource)


var randomNumber2 = Math.floor(Math.random() * 6) +1;

randomDiceImage2 = "dice" + randomNumber2 + ".png";
var randomImageSource2 = "images/" + randomDiceImage2;
var img2 =document.querySelectorAll("img")[1];
img2.setAttribute("src", randomImageSource2)

if (randomNumber1 === randomNumber2){
    document.querySelectorAll("h1")[0].innerHTML = "🏳️DRAW"
}else if(randomNumber1 > randomNumber2){
    document.querySelectorAll("h1")[0].innerHTML = "🚩Player 1 wins"
}else{
    document.querySelectorAll("h1")[0].innerHTML = "🏴Player 2 wins"
}