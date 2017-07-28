var current_photo = 0;
document.getElementsByClassName('qna')[0].style.display = "block";
document.getElementsByClassName('scoreScreen')[0].style.display = "none";
var image = document.getElementsByClassName('picture-question')[0];
document.getElementsByClassName('picture-question')[0].style.transform = "scale(8)";
function checkQuestion(buttonElement) {
      // TODO: Get all info needed from the button.dataset and button.innerText.
      console.log(buttonElement.dataset.photoKey);
      console.log(buttonElement.innerText);

      $.post('/image-score', {photo_key: buttonElement.dataset.photoKey,
        answer: buttonElement.innerText}, function(response2){
          var values = JSON.parse(response2);
          //Changes the text within the span id'd "score"
          $('#score').text(values.score);
          if (values.correct) {
            $(buttonElement).css({"background-color":"#009000"});
            $('.picture-question').css({"transform" : "scale(1)"});
          }
          else {
            $(buttonElement).css({"background-color":"#ff0000"});
            $('.picture-question').css({"transform" : "scale(1)"});
          }
          setTimeout(advanceQuestion, 1000);

        });
}

function advanceQuestion() {
    var photos = document.getElementsByClassName('qna');
    photos[current_photo].style.display = 'none';
    $('.picture-question').css({"transform":"scale(8)"});
    current_photo += 1;

    if(current_photo == 10) {
      //After 10 questions, the score will be displayed
      var scoreScreen = document.getElementsByClassName('scoreScreen')[0];
      scoreScreen.style.display = "block";
    }
    else {
      photos[current_photo].style.display = 'block';
  }
}
