var current_photo = 0;
document.getElementsByClassName('qna')[0].style.display = "block";
document.getElementsByClassName('scoreScreen')[0].style.display = "none";
function checkQuestion(buttonElement) {
      // TODO: Get all info needed from the button.dataset and button.innerText.
      console.log(buttonElement.dataset.photoKey);
      console.log(buttonElement.innerText);

      $.post('/score', {photo_key: buttonElement.dataset.photoKey,
        answer: buttonElement.innerText}, function(response){
          var values = JSON.parse(response);
          //Changes the text within the span id'd "score"
          $('#score').text(values.score);
          if (values.correct) {
            $(buttonElement).css({"background-color":"#009000"});
          }
          else {
            $(buttonElement).css({"background-color":"#ff0000"});
          }

          setTimeout(advanceQuestion, 1000);
        });
}

function advanceQuestion() {
    var photos = document.getElementsByClassName('qna');
    photos[current_photo].style.display = 'none';
    current_photo += 1;

    if(current_photo == 10) {
      //After 10 questions, the score will be displayed
      var scoreScreen = document.getElementsByClassName('scoreScreen')[0];
      scoreScreen.style.display = "block";
    }
    else {
      questions[current_question].style.display = 'block';
  }
}
