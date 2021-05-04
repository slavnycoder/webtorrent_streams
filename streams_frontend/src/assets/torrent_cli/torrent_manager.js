import WebTorrent from 'webtorrent/webtorrent.min';

WebTorrent.prototype.cleanup_torrents = function () {
  if (this.torrents.length < 5) return;
  const oldTorrent = this.torrents.shift();
  oldTorrent.destroy();
};

export const webtorrent_cli = new WebTorrent();

if (false) {
  setInterval(() => {
    sendMessage("test");
  }, 2000);
}
