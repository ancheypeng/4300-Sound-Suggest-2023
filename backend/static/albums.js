let albums = [];

fetch('/albums')
  .then((response) => response.json())
  .then((data) => (albums = data));
