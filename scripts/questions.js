current_question = 0;
document.getElementsByClassName('qna')[0].style.display = "block";
function advanceQuestion(buttonElement) {

      // TODO: Get all info needed from the button.dataset and button.innerText.
      console.log(buttonElement.dataset.questionKey);
      console.log(buttonElement.innerText);

      $.post('/score', {question_key: buttonElement.dataset.questionKey,
        answer: buttonElement.innerText});

    var questions = document.getElementsByClassName('qna');
    questions[current_question].style.display = 'none';
    current_question += 1;
    if(current_question == 11) {

    }
    questions[current_question].style.display = 'block';

}

  /*
  // Here, "this" is the button that the user clicked.
  var button = $(this);

  // Move through the DOM tree to find the "likes"
  // element that corresponds to the clicked button.

  // Look through parents of this to find .photo.
  var user = $(this).parents('.user');

  // Look inside photo to find .likes.
  var scores = $(user).find('.scores');

  // Get the URLsafe key from the button value.
  var urlsafeKey = $(button).val();

  // Send a POST request and handle the response.
    $.post('/scores', {'photo_key': urlsafeKey}, function(response) {
      // Update the number in the "like" element.
      $(likes).text(response);
    });
  }

  $('.photo button').click(clickLike); */
