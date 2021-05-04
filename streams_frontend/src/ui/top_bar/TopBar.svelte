<script>
  import NavBar from "ui/top_bar/NavBar.svelte";
  import Drawer from "ui/drawer/Drawer.svelte";
  import LoadingPage from "ui/LoadingPage.svelte";
  import ErrorPage from "ui/ErrorPage.svelte";

  import { drawerOpen } from "stores.js";
  import { navbar_height } from "constants.js";
  import { get_settings, auth, get_channels } from "utils.js";
  import { init_ws } from "assets/centrifuge_cli/client.js";

  async function init_main() {
    await get_settings();
    await auth();
  }

  async function init_content() {
    await init_ws();
    await get_channels();
  }

  let drawerToggle = () => {
    drawerOpen.update(n => !n);
  };
</script>

<style>
  #content {
    height: calc(100% - var(--navbar_height));
  }
</style>

{#await init_main()}
  <LoadingPage />
{:then _}
  <Drawer {drawerToggle} />
  <NavBar {drawerToggle} />
  {#await init_content()}
    <LoadingPage />
  {:then _}
    <div id="content" style="--navbar_height:{navbar_height + 'px'};">
      <slot />
    </div>
  {:catch error}
    <ErrorPage />
  {/await}
{:catch error}
  <ErrorPage />
{/await}
