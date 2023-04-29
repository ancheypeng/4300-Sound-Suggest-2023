function createVisualization(data) {
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
        color: '#1bb954',
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

  var data = [suggestedSongs, albumSongs, randomSongs];
  var layout = {
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
    plot_bgcolor: '#1a1a1a',
    paper_bgcolor: '#1a1a1a',
    showlegend: true,
    legend: {
      x: 1,
      xanchor: 'right',
      y: 1,
    },
    title: {
      text: 'Lyrical Similarity',
      font: {
        size: 24,
      },
      xref: 'paper',
      yref: 'paper',
      automargin: true,
    },
  };
  Plotly.newPlot('tsne', data, layout);
}

// createVisualization(0);
