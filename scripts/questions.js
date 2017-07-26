current_question = 0;
document.getElementsByClassName('qna')[0].style.display = "block";
function advanceQuestion() {
    var questions = document.getElementsByClassName('qna');
    questions[current_question].style.display = 'none';
    current_question += 1;
    questions[current_question].style.display = 'block';
}

function changeScore() {
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
    $.post('/likes', {'photo_key': urlsafeKey}, function(response) {
      // Update the number in the "like" element.
      $(likes).text(response);
    });
  }

  $('.photo button').click(clickLike);
