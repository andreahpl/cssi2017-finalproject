var current_question = 0;
document.getElementsByClassName('qna')[0].style.display = "block";
document.getElementsByClassName('scoreScreen')[0].style.display = "none";
function advanceQuestion(buttonElement) {
      // TODO: Get all info needed from the button.dataset and button.innerText.
      console.log(buttonElement.dataset.questionKey);
      console.log(buttonElement.innerText);

      $.post('/score', {question_key: buttonElement.dataset.questionKey,
        answer: buttonElement.innerText}, function(score){
          //Changes the text within the span id'd "score"
          $('#score').text(score);
        });

    var questions = document.getElementsByClassName('qna');
    questions[current_question].style.display = 'none';
    current_question += 1;

    if(current_question == 10) {
      //After 10 questions, the score will be displayed
      var scoreScreen = document.getElementsByClassName('scoreScreen')[0];
      scoreScreen.style.display = "block";
    }
    else {
      questions[current_question].style.display = 'block';
    }
}
