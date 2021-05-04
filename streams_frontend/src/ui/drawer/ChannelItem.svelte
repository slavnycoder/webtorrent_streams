<script>
  export let channel;

  import { Item } from "@smui/list";
  import { Icon } from "@smui/button";
  import { kFormatter, get_gravatar_link, href } from "utils.js";
</script>

<style>
  .streamer-item {
    display: flex;
    align-items: center;
    width: 250px;
    padding: 5px 0px 5px 5px;
  }

  .streamer-item:hover {
    cursor: pointer;
    background-color: rgba(255, 255, 255, 0.05);
  }

  .streamer-avatar-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-right: 15px;
  }

  .streamer-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }

  .streamer-info {
    display: flex;
  }

  .streamer-metadata {
    display: flex;
    flex-direction: column;
    width: 135px;
  }

  .streamer-display-name {
    font-size: 1.2em;
  }

  .streamer-description {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: #e0e0e0;
  }

  .streamer-status {
    display: flex;
    justify-content: space-around;
    width: 55px;
  }

  .online-circle {
    margin: 4px;
    height: 1em;
    width: 1em;
    background-color: red;
    border-radius: 50%;
  }
</style>

<span on:click={() => href('/' + channel.username)} class="streamer-item">
  <span class="streamer-avatar-container">
    <img
      src={channel.img_url || get_gravatar_link(channel.username)}
      alt="channelpic"
      class="streamer-avatar" />
  </span>
  <span class="streamer-info">
    <span class="streamer-metadata">
      <span class="streamer-display-name">{channel.display_name}</span>
      <span class="streamer-description">
        {channel.stream ? channel.stream.description : ''}
      </span>
    </span>
    <span class="streamer-status">
      {#if channel.stream}
        <div class="online-circle" />
        <div>{kFormatter(channel.stream.viewers)}</div>
      {:else if channel.followers_count}
        <Icon class="material-icons">person</Icon>
        <div>{kFormatter(channel.followers_count)}</div>
      {:else}
        <div>Offline</div>
      {/if}
    </span>
  </span>
</span>
