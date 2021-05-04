<script>
  export let channel_username;
  export let is_followed;

  import { onDestroy } from "svelte";
  import debounce from "just-debounce-it";

  import Button, { Icon } from "@smui/button";
  import { follow_channel, get_channels } from "utils.js";

  let hovered = false;

  function enter() {
    hovered = true;
  }

  function leave() {
    hovered = false;
  }

  const sendFollowQuery = debounce(() => {
    follow_channel(channel_username, is_followed).then(() => {
      get_channels();
    });
  }, 300);

  function toggleFollow() {
    is_followed = !is_followed;
    hovered = false;
    sendFollowQuery();
  }
</script>

<div on:mouseenter={enter} on:mouseleave={leave}>
  <Button
    on:click={toggleFollow}
    variant={is_followed != hovered ? 'raised' : 'outlined'}
    style="padding: 0; min-width: 36px;">
    <Icon class="material-icons" style="margin: 0;">star</Icon> 
    <!-- todo fix margin:0 -->
  </Button>
</div>
