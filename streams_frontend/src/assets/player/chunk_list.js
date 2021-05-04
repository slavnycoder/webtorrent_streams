class Chunk {
  constructor(
    torrent_client,
    number,
    prob,
    duration,
    torrent_url,
    magnet_link
  ) {
    this.torrent_client = torrent_client;
    this.torrent = undefined;
    this.is_ready = false;
    this.update_timer = undefined;
    // chunk data
    this.number = number;
    this.prob = prob;
    this.duration = duration;
    this.torrent_url = torrent_url;
    this.magnet_link = magnet_link;
    this.blob_url = undefined;
  }

  init() {
    const curr_chunk = this;

    curr_chunk.torrent_client.torrents
      .filter(torrent => torrent.name == `${curr_chunk.number}.ts`)
      .forEach(torrent => torrent.destroy());

    const target_url =
      Math.random() < parseFloat(curr_chunk.prob) || !!curr_chunk.update_timer
        ? curr_chunk.torrent_url || curr_chunk.magnet_link
        : curr_chunk.magnet_link;
    curr_chunk.torrent_client.add(target_url, function (torrent) {
      curr_chunk.torrent = torrent;
      curr_chunk.torrent.files[0].getBlob(function (err, blob) {
        curr_chunk.blob_url = URL.createObjectURL(blob);
      });
    });

    curr_chunk.update_timer = setTimeout(() => {
      if (!curr_chunk.torrent || curr_chunk.torrent.progress == 0) {
        curr_chunk.init();
      }
    }, 1500);
  }

  to_worker() {
    return {
      number: this.number,
      duration: this.duration,
      blob_url: this.blob_url
    };
  }

  clear_update_timer() {
    if (this.update_timer) {
      clearTimeout(this.update_timer);
    }
  }

  destroy() {
    this.clear_update_timer();
    if (this.torrent) {
      this.torrent.destroy();
    }
  }
}

export class ChunkList {
  constructor() {
    this.max_number = 0;
    this.chunks = [];
  }

  add_new_chunk(chunk_data, torrent_client) {
    let curr_chunk_list = this;
    if (chunk_data.number > curr_chunk_list.max_number) {
      curr_chunk_list.max_number = chunk_data.number;
      const new_chunk = new Chunk(
        torrent_client,
        chunk_data.number,
        chunk_data.prob,
        chunk_data.duration,
        chunk_data.torrent_url,
        chunk_data.magnet_link
      );
      curr_chunk_list.chunks = [...curr_chunk_list.chunks, new_chunk];
      new_chunk.init();
    }
  }
}