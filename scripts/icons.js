var iconIndex = 1;
showIcons(iconIndex);

function plusIcons(n) {
  showIcons(iconIndex += n);
}

function currentIcon(n) {
  showIcons(iconIndex = n);
}

function showIcons(n) {
  var i;
  var icons = document.getElementsByClassName("userIcons");
  if (n > icons.length) {iconIndex = 1}
  if (n < 1) {iconIndex = icons.length}
  for (i = 0; i < icons.length; i++) {
      icons[i].style.display = "none";
  }
  icons[iconIndex-1].style.display = "block";
}
