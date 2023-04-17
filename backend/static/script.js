// getting all required elements
const searchWrapper = document.querySelector('.search-input');
const inputBox = searchWrapper.querySelector('input');
const suggBox = searchWrapper.querySelector('.autocom-box');
const icon = searchWrapper.querySelector('.icon');
let linkTag = searchWrapper.querySelector('a');
let webLink;

// if user press any key and release
inputBox.onkeyup = (e) => {
  if (e.keyCode === 13) {
    searchWrapper.classList.remove('active');
    query();
    return;
  }

  let userData = e.target.value; //user enetered data

  let emptyArray = [];
  if (userData) {
    emptyArray = albums.filter((data) => {
      //filtering array value and user characters to lowercase and return only those words which are start with user enetered chars
      return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
    });
    emptyArray = emptyArray.map((data) => {
      // passing return data inside li tag
      return (data = `<li>${data}</li>`);
    });
    searchWrapper.classList.add('active'); //show autocomplete box
    showSuggestions(emptyArray);
    let allList = suggBox.querySelectorAll('li');
    for (let i = 0; i < allList.length; i++) {
      //adding onclick attribute in all li tag
      allList[i].setAttribute('onclick', 'select(this)');
    }
  } else {
    searchWrapper.classList.remove('active'); //hide autocomplete box
  }
};

function select(element) {
  let selectData = element.textContent;
  inputBox.value = selectData;
  searchWrapper.classList.remove('active');
  inputBox.focus();
}

function showSuggestions(list) {
  let listData;
  if (!list.length) {
    userValue = inputBox.value;
    listData = `<li>${userValue}</li>`;
  } else {
    listData = list.join('');
  }
  suggBox.innerHTML = listData;
}

// if user unfocuses from search box
inputBox.addEventListener('focusout', (e) =>
  setTimeout(() => searchWrapper.classList.remove('active'), 200)
);

function query() {
  searchWrapper.classList.remove('active');
  $('.content').addClass('active-state');
  $('.results').empty();
  console.log('Querying...');
  // song = 'Life Is Good (feat. Drake)';
  // link = 'https://open.spotify.com/track/5yY9lUy8nbvjM1Uyo1Uqoc';
  // thumbnail =
  //   'https://i.scdn.co/image/ab67616d0000b2738a01c7b77a34378a62f46402';
  // artists = [
  //   {
  //     name: 'Future',
  //     link: 'https://open.spotify.com/artist/1RyvyyTE3xzB2ZywiAwp0i',
  //   },
  //   {
  //     name: 'Drake',
  //     link: 'https://open.spotify.com/artist/3TVXtAsR1Inumwj472S9r4',
  //   },
  // ];

  // for (let i = 0; i < 5; i++) {
  //   setTimeout(
  //     () => $('.results').append(card(song, link, thumbnail, artists)),
  //     i * 150
  //   );
  // }

  let searchParams = new URLSearchParams();
  searchParams.append('album', inputBox.value);
  $('#social-tags')
    .select2('val')
    .forEach((tag) => searchParams.append('tags', tag.toLocaleLowerCase()));

  fetch('/songs?' + searchParams.toString())
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      data.forEach((value, index) =>
        setTimeout(
          () =>
            $('.results').append(
              card(
                value['song'],
                value['link'],
                value['thumbnail'],
                value['artists']
              )
            ),
          index * 150
        )
      );
    });
}

$('#social-tags').select2({
  theme: 'bootstrap-5',
  width: $(this).data('width')
    ? $(this).data('width')
    : $(this).hasClass('w-100')
    ? '100%'
    : 'style',
  placeholder: $(this).data('placeholder'),
  closeOnSelect: false,
});

//populate tags
fetch('/tags')
  .then((response) => response.json())
  .then((data) =>
    data.forEach((good_tag) =>
      $('#social-tags').append(`<option>${good_tag}</option>`)
    )
  );

// suggestions.forEach((song) => {
//   let tempOption = document.createElement('option');
//   tempOption.innerHTML = song;
//   $('#search').append(tempOption);
// });

function artistContent(artists) {
  let artistDiv = $(document.createElement('div'));
  artists.forEach((artist, i) => {
    if (i > 0) {
      artistDiv.html(artistDiv.html() + ', ');
    }
    let name = artist['name'];
    let link = artist['link'];
    let linkAnchor = $('<a></a>')
      .attr('href', link)
      .attr('target', '_blank')
      .append(`<span class="artist-name">${name}</span>`);
    artistDiv.append(linkAnchor);
  });

  return artistDiv.html();
}

function card(song, link, thumbnail, artists) {
  let artistsHTML = artistContent(artists);
  let temp = `
  <div class="card">
    <div class="row g-0">
      <div class="col col-md-4">
        <img
          class="cover-art"
          src="${thumbnail}"
          alt="Cover Art"
        />
      </div>
      <div class="col col-md-8">
        <h5 class="song-title">${song}</h5>
        <p class="artists">
        ${artistsHTML}
        </p>
      </div>
    </div>
    <a
      href="${link}"
      target="_blank"
      class="stretched-link"
    >
      <img class="play" src="static/images/play.svg" alt="Play Button" />
    </a>
  </div>`;

  return temp;
}
