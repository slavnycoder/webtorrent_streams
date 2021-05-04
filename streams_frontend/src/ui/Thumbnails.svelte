<script>
  import { onMount } from "svelte";
  import { Icon } from "@smui/button";

  import Button, { Label } from "@smui/button";

  import LoadingPage from "ui/LoadingPage.svelte";
  import ErrorPage from "ui/ErrorPage.svelte";

  import { get_online_channels, kFormatter, href } from "utils.js";

  let loadingInProgress = false;
  let channels = [];
  let page = 1;
  let has_next_page = false;
  let has_error = false;
  let channel_id = "test";

  async function load_more_channels() {
    if (loadingInProgress) return;
    try {
      has_error = false;
      loadingInProgress = true;
      const responseData = await get_online_channels(page);
      page += 1;
      has_next_page = responseData.next_page;
      channels = responseData.channels;
    } catch (err) {
      has_error = true;
      loadingInProgress = false;
      throw err;
    }
    loadingInProgress = false;
  }
</script>

<style>
  #main-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-grow: 1 !important;
    width: 100%;
    overflow-y: scroll;
  }

  #stream-list {
    display: grid;
    justify-content: center;
    grid-template-columns: repeat(auto-fit, 320px);
    grid-template-rows: repeat(auto-fit, 180px);
    grid-gap: 2rem;
    width: 80%;
    margin: 35px 0px;
  }

  #stream-list > li {
    padding: 5px;
    height: 180px;
    width: 320px;
    color: #fff;
    list-style-type: none;
    cursor: pointer;
  }

  .thumbnail {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    justify-content: space-between;
    background-size: cover;
    background-color: #000;
  }

  .thumbnail:hover {
    background-color: #212121;
    background-blend-mode: screen;
  }

  .top-row {
    display: flex;
    justify-content: space-between;
  }

  .dark-background {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 5px;
    border-radius: 5px;
    background-color: rgba(0, 0, 0, 0.7);
  }

  .streamer-name {
    display: block;
  }

  .red-circle {
    height: 0.8em;
    width: 0.8em;
    border-radius: 50%;
    margin-right: 5px;
    background-color: #d32f2f;
  }

  .bottom-row {
    display: flex;
    flex-direction: column;
    align-content: flex-start;
  }

  .stream-description {
    justify-content: flex-start;
    font-weight: 200;
  }

  .load-more {
    display: flex;
    justify-content: center;
    align-items: center;
    color: #000 !important;
    background-color: #424242;
  }

  .load-more:hover {
    background-color: #9e9e9e;
  }

  #no-streams {
    display: flex;
    justify-content: center;
    color: #e0e0e0;
  }

  #no-streams-wrap {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: stretch;
    align-self: center;
    padding: 15px;
  }

  #no-streams-img {
    background: url(static/png/no_streams.png);
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    height: 300px;
    max-width: 100vw;
  }

  a#tlg-link {
    color: inherit;
    text-decoration: none;
  }
</style>

{#await load_more_channels()}
  <LoadingPage />
{:then _}
  <div id="main-page">
    {#if channels.length}
      <div id="stream-list">
        {#each channels as channel}
          <li
            on:click={() => href('/' + channel.username)}
            class="thumbnail"
            style="background-image:url('{channel.stream.thumbnail_url}')">
            <div class="top-row">
              <div
                class="dark-background streamer-name"
                style="color:{channel.username_color}">
                {channel.display_name}
              </div>
              <div class="dark-background">
                <div class="red-circle" />
                {kFormatter(channel.stream.viewers)}
              </div>
            </div>
            <div class="bottom-row">
              <div class="dark-background stream-description">
                {channel.stream.description}
              </div>
            </div>
          </li>
        {/each}
        {#if channels.next_page}
          <li on:click={load_more_channels} class="load-more">
            {#if loadingInProgress}
              <LoadingPage dark={true} />
            {:else if has_error}
              <Icon class="material-icons" style="font-size: 75px !important;">
                refresh
              </Icon>
            {:else}
              <Icon class="material-icons" style="font-size: 75px !important;">
                chevron_right
              </Icon>
            {/if}
          </li>
        {/if}
      </div>
    {:else}
      <div id="no-streams-wrap">
        <h2 id="no-streams">Никто не стримит</h2>
        <Button variant="outlined" color="secondary">
          <a id="tlg-link" href="https://t.me/{channel_id}" target="_blank">
            <Label>Телеграм канал @{channel_id}</Label>
          </a>
        </Button>
        <div id="no-streams-img" />
      </div>
    {/if}
  </div>
{:catch error}
  <ErrorPage />
{/await}
