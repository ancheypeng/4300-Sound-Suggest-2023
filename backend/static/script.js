// getting all required elements
const searchWrapper = document.querySelector('.search-input');
const inputBox = searchWrapper.querySelector('input');
const suggBox = searchWrapper.querySelector('.autocom-box');
const icon = searchWrapper.querySelector('.icon');
let linkTag = searchWrapper.querySelector('a');
let webLink;

// // global event listener for enter key
// document.addEventListener('keydown', (e) => {
//   if (e.key === 'Enter') {
//     searchWrapper.classList.remove('active');
//     query();
//     document.activeElement.blur();
//     return;
//   }
// });

// search icon onclick
icon.onclick = () => {
  searchWrapper.classList.remove('active');
  query();
  return;
};

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
      return data.toLocaleLowerCase().includes(userData.toLocaleLowerCase());
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
  $('.visualization').empty();
  //show spinner when query starts
  $('.results').append(
    `<div class="text-center"><div class='spinner-border text-primary m-5' role='status'></div></div>`
  );
  console.log('Querying...');

  let searchParams = new URLSearchParams();
  searchParams.append('album', inputBox.value);
  $('#social-tags')
    .select2('val')
    .forEach((tag) => searchParams.append('tags', tag.toLocaleLowerCase()));

  fetch('/songs?' + searchParams.toString())
    .then((response) => response.json())
    .then((data) => {
      // remove spinner
      $('.results').empty();

      //smooth scroll down
      setTimeout(
        () => $(window).scrollTo($('.results'), 500, { offset: { top: -20 } }),
        500
      );

      createTSNE(data);
      createRadial(data);

      suggested_songs = data['spotify_data'];
      suggested_songs.forEach((value, index) =>
        setTimeout(
          () =>
            $('.results').append(
              card(
                value['song'],
                value['link'],
                value['thumbnail'],
                value['artists'],
                value['score'].toFixed(2),
                index
              )
            ),
          index * 50
        )
      );

      setTrackList(data);
    })
    .catch((error) => {
      $('.results').empty();
      $('.results').append(`<h4 class="error">Invalid Input</h4>`);
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

function card(song, link, thumbnail, artists, score, index) {
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
        <p class="card-text">
        ${artistsHTML}
        </p>
        <p class="card-text">
        Similarity: ${score}%
        </p>
      </div>
    </div>
      <i class="fa fa-play-circle fa-4x play" onclick="loadAndPlayTrack(${index})"></i>
  </div>`;

  return temp;
}
