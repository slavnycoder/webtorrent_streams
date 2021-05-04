let chunks = [];
let cached_response;

self.addEventListener("fetch", event => {
  if (event.request.method === 'GET' && event.request.url.includes('.m3u8')) {
    if (!cached_response) {
      const sequence = Math.max(...Array.from(chunks, chunk => chunk.number));
      const max_duration = Math.max(...Array.from(chunks, chunk => parseFloat(chunk.duration)));
      const chunk_descriptions = Array.from(chunks, chunk => `#EXTINF:${parseFloat(chunk.duration)},\n${chunk.blob_url}`)
      const playlist_elements = [
        "#EXTM3U",
        "#EXT-X-VERSION:3",
        `#EXT-X-TARGETDURATION:${Math.ceil(max_duration)}`,
        `#EXT-X-MEDIA-SEQUENCE:${sequence}\n`,
        ...chunk_descriptions,
      ];
      cached_response = new Response(playlist_elements.join("\n"), {
        headers: {
          "Content-Type": "application/vnd.apple.mpegurl"
        }
      });
    }
    event.respondWith(cached_response.clone());
  }
});

self.addEventListener("message", function (event) {
  try {
    chunks = JSON.parse(event.data);
    cached_response = undefined;
  } catch (error) {
    console.log("SW err", err);
  }
});
