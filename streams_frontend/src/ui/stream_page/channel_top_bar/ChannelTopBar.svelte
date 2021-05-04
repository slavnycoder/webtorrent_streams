<script>
  export let channel_data;
  export let channel_username;
  export let is_followed;

  import FollowBtn from "./FollowBtn.svelte";

  import { get_gravatar_link } from "utils.js";
  import { userProfile } from "stores.js";

  import { navbar_height } from "constants.js";
</script>

<style>
  #top-channel-bar {
    display: flex;
    height: var(--navbar_height);
    justify-content: space-between;
    align-items: center;
    background-color: #111;
  }

  #channel-info {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  #channel-avatar {
    width: 2em;
    height: 2em;
    border-radius: 50%;
    margin: 0px 10px;
  }

  #channel-display-name {
    color: #e0e0e0;
  }

  #follow-btn-wrap {
    margin-right: 50px;
  }
</style>

<div id="top-channel-bar" style="--navbar_height:{navbar_height + 'px'};">
  <div />
  <div id="channel-info">
    <img
      id="channel-avatar"
      src={channel_data.img_url || get_gravatar_link(channel_username)}
      alt="" />
    <h3 id="channel-display-name">{channel_data.display_name}</h3>
  </div>
  <div id="follow-btn-wrap">
    {#if $userProfile.username}
      <FollowBtn {channel_username} {is_followed} />
    {/if}
  </div>
</div>
