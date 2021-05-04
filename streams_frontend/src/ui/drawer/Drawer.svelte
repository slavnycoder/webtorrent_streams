<script>
  export let drawerToggle;

  import { tweened } from "svelte/motion";
  import { cubicOut } from "svelte/easing";
  import IconButton from "@smui/icon-button";
  import { Title as AppBarTitle } from "@smui/top-app-bar";

  import { Separator } from "@smui/list";

  import Drawer, {
    AppContent,
    Content,
    Header,
    Title,
    Subtitle,
    Scrim
  } from "@smui/drawer";

  import ChannelList from "ChannelList.svelte";
  import { arrow_right, arrow_left } from "constants.js";
  import { drawerOpen } from "stores.js";

  let subscriptions_shown = false;
  const collapsed_subs_width = 70;
  const expanded_subs_width = 240;

  const list_width = tweened(
    subscriptions_shown ? expanded_subs_width : collapsed_subs_width,
    {
      duration: 400,
      easing: cubicOut
    }
  );

  function toggle_subscriptions() {
    if (subscriptions_shown) {
      list_width.set(collapsed_subs_width);
    } else {
      list_width.set(expanded_subs_width);
    }
    subscriptions_shown = !subscriptions_shown;
  }
</script>

<style>
  #drawer-header {
    display: flex;
    justify-content: flex-end;
    padding-top: 12px;
    padding-bottom: 12px;
  }
</style>

<Drawer class="drawer-space" variant="modal" bind:open={$drawerOpen}>
  <Header>
    <div id="drawer-header">
      <IconButton class="material-icons" on:click={drawerToggle}>
        close
      </IconButton>
    </div>
  </Header>
  <Content>
    <ChannelList />
  </Content>
</Drawer>
<Scrim />
