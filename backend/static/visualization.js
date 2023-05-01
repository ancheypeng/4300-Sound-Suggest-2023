function createTSNE(data) {
  function unpack(rows, key) {
    return rows.map(function (row) {
      return row[key];
    });
  }

  var suggestedSongs = {
    name: 'Suggested Songs',
    x: unpack(data['suggested_song_embeddings'], 0),
    y: unpack(data['suggested_song_embeddings'], 1),
    z: unpack(data['suggested_song_embeddings'], 2),
    text: unpack(data['spotify_data'], 'song'),
    hovertemplate: `%{text}`,
    mode: 'markers',
    marker: {
      color: '#1bb954',
      size: 8,
      line: {
        color: '#cccccc',
        width: 1,
      },
      opacity: 0.9,
    },
    type: 'scatter3d',
  };

  var albumSongs = {
    name: 'Album Songs',
    x: unpack(data['album_song_embeddings'], 0),
    y: unpack(data['album_song_embeddings'], 1),
    z: unpack(data['album_song_embeddings'], 2),
    text: data['album_song_names'],
    hovertemplate: `%{text}`,
    mode: 'markers',
    marker: {
      color: '#777777',
      size: 8,
      line: {
        width: 0.5,
      },
      opacity: 0.8,
    },
    type: 'scatter3d',
  };

  const average = (array) => array.reduce((a, b) => a + b) / array.length;

  var albumCentroid = {
    name: 'Album Centroid',
    x: [average(albumSongs.x)],
    y: [average(albumSongs.y)],
    z: [average(albumSongs.z)],
    mode: 'markers',
    marker: {
      color: 'white',
      size: 8,
      line: {
        width: 0.5,
      },
      opacity: 0.7,
    },
    type: 'scatter3d',
    hoverinfo: 'skip',
  };

  var randomSongs = {
    name: 'Other Songs',
    x: unpack(data['random_song_embeddings'], 0),
    y: unpack(data['random_song_embeddings'], 1),
    z: unpack(data['random_song_embeddings'], 2),
    mode: 'markers',
    marker: {
      color: '#151515',
      size: 8,
      line: {
        width: 0.5,
      },
      opacity: 0.5,
    },
    type: 'scatter3d',
    hoverinfo: 'skip',
  };

  var plotData = [suggestedSongs, albumSongs, albumCentroid, randomSongs];
  var layout = {
    height: 500,
    margin: {
      l: 20,
      r: 20,
      b: 20,
      t: 20,
    },
    font: {
      size: 10,
      color: '#aaaaaa',
      family: 'Figtree, sans-serif',
    },
    plot_bgcolor: '#202020',
    paper_bgcolor: '#202020',
    showlegend: true,
    legend: {
      x: 1,
      xanchor: 'right',
      y: 1,
      bgcolor: 'rgba(0,0,0,0)',
    },
    title: {
      text: 'Lyrical Similarity',
      font: {
        size: 24,
      },
      pad: {
        t: 15,
        b: 10,
      },
      xref: 'paper',
      yref: 'paper',
      automargin: true,
    },
    scene: {
      xaxis: {
        showticklabels: false,
        zeroline: false,
        title: '',
      },
      yaxis: {
        showticklabels: false,
        zeroline: false,
        title: '',
      },
      zaxis: {
        showticklabels: false,
        zeroline: false,
        title: '',
      },
    },
  };
  Plotly.newPlot('tsne', plotData, layout);
}

function truncate(str, n) {
  return str.length > n ? str.slice(0, n - 1) + '...' : str;
}

function createRadial(data) {
  // console.log(data['radial_data']);
  albumData = {
    name: 'Album Tags',
    type: 'scatterpolar',
    r: data['radial_data'].shift(),
    theta: data['radial_dimensions'],
    visible: true,
    hoverinfo: 'skip',
  };

  plotData = [albumData];

  for (let i = 0; i < data['radial_data'].length; i++) {
    let songData = { ...albumData };
    songData['r'] = data['radial_data'][i];
    songData['visible'] = i == 0 ? true : 'legendonly';
    songData['name'] = truncate(data['spotify_data'][i]['song'], 15);
    plotData.push(songData);
  }

  layout = {
    height: 500,
    margin: {
      b: 20,
      t: 20,
    },
    polar: {
      radialaxis: {
        visible: false,
      },
      bgcolor: '#202020',
    },
    showlegend: true,
    legend: {
      bgcolor: 'rgba(0,0,0,0)',
      xanchor: 'center',
      yanchor: 'top',
      y: -0.3, // play with it
      x: 0.5, // play with it
    },
    font: {
      size: 10,
      color: '#aaaaaa',
      family: 'Figtree, sans-serif',
    },
    paper_bgcolor: '#202020',
    title: {
      text: 'Tag Similarity',
      font: {
        size: 24,
      },
      pad: {
        t: 15,
        b: 30,
      },
      xref: 'paper',
      yref: 'paper',
      automargin: true,
    },
  };

  Plotly.newPlot('radial', plotData, layout);
}

// createRadial();
