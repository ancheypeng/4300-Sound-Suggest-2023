let track_art = document.querySelector('.track-art');
let track_name = document.querySelector('.track-name');
let track_artist = document.querySelector('.track-artist');

let playpause_btn = document.querySelector('.playpause-track');
let next_btn = document.querySelector('.next-track');
let prev_btn = document.querySelector('.prev-track');

let seek_slider = document.querySelector('.seek-slider');
let volume_slider = document.querySelector('.volume-slider');
let curr_time = document.querySelector('.current-time');
let total_duration = document.querySelector('.total-duration');

let track_index = 0;
let isPlaying = false;
let updateTimer;

// Create new audio element
let curr_track = document.createElement('audio');

// Define the tracks that have to be played
let track_list = [
  // {
  //   name: '1234567891011121314',
  //   artist: '1234567891011121314',
  //   image:
  //     'https://images.pexels.com/photos/2264753/pexels-photo-2264753.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=250&w=250',
  //   path: 'https://files.freemusicarchive.org/storage-freemusicarchive-org/music/WFMU/Broke_For_Free/Directionless_EP/Broke_For_Free_-_01_-_Night_Owl.mp3',
  // },
  // {
  //   name: 'Enthusiast',
  //   artist: 'Tours',
  //   image:
  //     'https://images.pexels.com/photos/3100835/pexels-photo-3100835.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=250&w=250',
  //   path: 'https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/Tours/Enthusiast/Tours_-_01_-_Enthusiast.mp3',
  // },
  // {
  //   name: 'Shipping Lanes',
  //   artist: 'Chad Crouch',
  //   image:
  //     'https://images.pexels.com/photos/1717969/pexels-photo-1717969.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=250&w=250',
  //   path: 'https://files.freemusicarchive.org/storage-freemusicarchive-org/music/ccCommunity/Chad_Crouch/Arps/Chad_Crouch_-_Shipping_Lanes.mp3',
  // },
];

function setTrackList(data) {
  if (isPlaying) pauseTrack();

  track_list = [];

  spotifyData = data['spotify_data'];

  spotifyData.forEach((value) => {
    artistString = '';
    value['artists'].forEach((artist, i) => {
      if (i > 0) {
        artistString = artistString.concat(', ');
      }
      let name = artist['name'];
      artistString = artistString.concat(name);
    });

    track_list.push({
      name: truncate(value['song'], 15),
      artist: truncate(artistString, 23),
      image: value['thumbnail'],
      path: value['preview'],
    });
  });
}

function loadTrack(track_index) {
  clearInterval(updateTimer);
  resetValues();

  // Load a new track
  curr_track.src = track_list[track_index].path;
  curr_track.load();

  // Update details of the track
  track_art.style.backgroundImage =
    'url(' + track_list[track_index].image + ')';
  track_name.textContent = track_list[track_index].name;
  track_artist.textContent = track_list[track_index].artist;

  // Set an interval of 1000 milliseconds for updating the seek slider
  updateTimer = setInterval(seekUpdate, 1000);

  // Move to the next track if the current one finishes playing
  curr_track.addEventListener('ended', nextTrack);
}

// Reset Values
function resetValues() {
  curr_time.textContent = '00:00';
  total_duration.textContent = '00:00';
  seek_slider.value = 0;
}

function playpauseTrack() {
  if (!isPlaying && curr_track.readyState != 0) playTrack();
  else pauseTrack();
}

function playTrack() {
  curr_track.play();
  isPlaying = true;

  // Replace icon with the pause icon
  playpause_btn.innerHTML = '<i class="fa fa-pause-circle fa-3x"></i>';
}

function loadAndPlayTrack(track_index) {
  loadTrack(track_index);
  playTrack();
}

function pauseTrack() {
  curr_track.pause();
  isPlaying = false;

  // Replace icon with the play icon
  playpause_btn.innerHTML = '<i class="fa fa-play-circle fa-3x"></i>';
}

function nextTrack() {
  if (track_index < track_list.length - 1) track_index += 1;
  else track_index = 0;
  loadTrack(track_index);
  playTrack();
}

function prevTrack() {
  if (track_index > 0) track_index -= 1;
  else track_index = track_list.length;
  loadTrack(track_index);
  playTrack();
}

function seekTo() {
  seekto = curr_track.duration * (seek_slider.value / 100);
  curr_track.currentTime = seekto;
}

function setVolume() {
  curr_track.volume = volume_slider.value / 100;
  console.log(curr_track.volume);
  curr_track.muted = curr_track.volume == 0;
}

function seekUpdate() {
  let seekPosition = 0;

  // Check if the current track duration is a legible number
  if (!isNaN(curr_track.duration)) {
    seekPosition = curr_track.currentTime * (100 / curr_track.duration);
    seek_slider.value = seekPosition;

    // Calculate the time left and the total duration
    let currentMinutes = Math.floor(curr_track.currentTime / 60);
    let currentSeconds = Math.floor(
      curr_track.currentTime - currentMinutes * 60
    );
    let durationMinutes = Math.floor(curr_track.duration / 60);
    let durationSeconds = Math.floor(
      curr_track.duration - durationMinutes * 60
    );

    // Adding a zero to the single digit time values
    if (currentSeconds < 10) {
      currentSeconds = '0' + currentSeconds;
    }
    if (durationSeconds < 10) {
      durationSeconds = '0' + durationSeconds;
    }
    if (currentMinutes < 10) {
      currentMinutes = '0' + currentMinutes;
    }
    if (durationMinutes < 10) {
      durationMinutes = '0' + durationMinutes;
    }

    curr_time.textContent = currentMinutes + ':' + currentSeconds;
    total_duration.textContent = durationMinutes + ':' + durationSeconds;
  }
}

// Load the first track in the tracklist
// loadTrack(track_index);
