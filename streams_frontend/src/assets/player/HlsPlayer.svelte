<script>
  export let channel_data;

  import { onMount, onDestroy } from "svelte";

  import LoadingPage from "ui/LoadingPage.svelte";

  import Hls from "hls.js";
  import Plyr from "plyr";

  import { ChunkList } from "./chunk_list.js";

  import styles from "plyr/dist/plyr.css";
  import { centrifuge_cli } from "stores.js";
  import { webtorrent_cli } from "../torrent_cli/torrent_manager.js";

  const hls_type = "application/vnd.apple.mpegURL";
  const source_url = "playlist.m3u8";

  let fullscreen = false;
  let chunk_list = new ChunkList();

  let stream_inited = false;

  async function fetch_playlist_json() {
    if (channel_data.stream) {
      const response = await fetch(channel_data.stream.playlist_json_url);
      const new_chunks = await response.json();
      new_chunks.sort((a, b) => a.number - b.number);
      new_chunks.forEach(data =>
        chunk_list.add_new_chunk(data, webtorrent_cli)
      );

      chunk_list.chunks.sort((a, b) => a.number - b.number);
      const old_chunks = chunk_list.chunks.splice(
        0,
        chunk_list.chunks.length - 3
      );
      old_chunks.forEach(chunk => chunk.destroy());
      const ready_chunks = chunk_list.chunks.filter(
        chunk => chunk.torrent && chunk.torrent.progress == 1
      );
      if (ready_chunks.length) {
        const serialized_ready_chunks = ready_chunks.map(chunk =>
          chunk.to_worker()
        );
        navigator.serviceWorker.controller.postMessage(
          JSON.stringify(serialized_ready_chunks)
        );
        if (!stream_inited) {
          init_stream();
        }
      }
    }
  }

  let playlist_update_timer = setInterval(fetch_playlist_json, 3000);

  function init_stream() {
    stream_inited = true;
    var video = document.getElementById("video");

    const player = new Plyr(video, {
      autoplay: true,
      disableContextMenu: true,
      controls: ["play-large", "play", "mute", "volume", "fullscreen"],
      fullscreen: { enabled: true, fallback: true, iosNative: true }
    });
    player.on("enterfullscreen", event => {
      fullscreen = true;
    });
    player.on("exitfullscreen", event => {
      fullscreen = false;
    });

    if (Hls.isSupported()) {
      const hls_config = {
        manifestLoadingMaxRetry: 3,
        startFragPrefetch: true,
        liveSyncDurationCount: 1
      };
      var hls = new Hls(hls_config);
      hls.loadSource(source_url);
      hls.attachMedia(video);
    } else if (video.canPlayType(hls_type)) {
      let newSource = document.createElement("source");
      newSource.src = source_url;
      newSource.type = hls_type;
      video.appendChild(newSource);
    }
  }

  onDestroy(() => {
    clearInterval(playlist_update_timer);
  });
</script>

<style>
  #stream {
    background: #000;
    height: 85vh;
  }

  #video {
    height: var(--video_height);
  }

  #stream-offline {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    color: #e0e0e0;
    background: black;
  }
</style>

<div id="stream" style="--video_height:{fullscreen ? '100vh' : '85vh'}">
  {#if channel_data.stream}
    <video
      id="video"
      hidden={!stream_inited}
      style="display:{stream_inited ? 'block' : 'none'}" />
    {#if !stream_inited}
      <LoadingPage />
    {/if}
  {:else}
    <div id="stream-offline">Стрим оффлайн.</div>
  {/if}
</div>
