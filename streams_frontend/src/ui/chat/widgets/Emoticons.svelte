<script>
  export let emoticons_map;
  export let submit_emoticon;

  class Emoticon {
    constructor(name, count, url) {
      this.name = name;
      this.count = count;
      this.url = url;
    }
  }

  function process_emoticons(map) {
    let _emoticons = [];
    for (let emo_name in map) {
      _emoticons.push(
        new Emoticon(
          emo_name,
          map[emo_name].count,
          `https://cdn.frankerfacez.com/${map[emo_name].url}`
        )
      );
    }
    _emoticons.sort((a, b) => b.count - a.count);
    return _emoticons;
  }

  const sorted_emoticons = process_emoticons(emoticons_map);
</script>

<style>
  #emoticon-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    max-height: 300px;
    overflow: scroll;
  }

  .emoticon {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
    padding: 10px 0px;
    color: #e0e0e0;
    font-size: 12px;
  }

  .emoticon:hover {
    cursor: pointer;
    background-color: #444;
  }
</style>

<div id="emoticon-grid">
  {#each sorted_emoticons as emoticon}
    <div class="emoticon" on:mousedown={(e) => {
      e.preventDefault();
      submit_emoticon(emoticon.name)
    }}>
      <img src={emoticon.url} alt={emoticon.name} />
      {emoticon.name.length < 15 ? emoticon.name : emoticon.name.slice(0, 12) + '...'}
    </div>
  {/each}
</div>
