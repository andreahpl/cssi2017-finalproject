current_question = 0;
document.getElementsByClassName('qna')[0].style.display = "block";
function advanceQuestion() {
    var questions = document.getElementsByClassName('qna');
    questions[current_question].style.display = 'none';
    current_question += 1;
    questions[current_question].style.display = 'block';
}
