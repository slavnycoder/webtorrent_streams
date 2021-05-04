<script>
  import { Router, Route } from "svelte-routing";

  import TopBar from "ui/top_bar/TopBar.svelte";
  import StreamPage from "ui/stream_page/StreamPage.svelte";
  import MobileStreamPage from "ui/stream_page/MobileStreamPage.svelte";
  import PopUpChat from "ui/chat/PopUpChat.svelte";
  import Thumbnails from "ui/Thumbnails.svelte";
  import ResetPassword from "ui/reset_password/ResetPassword.svelte";
  import SetNewPassword from "ui/reset_password/SetNewPassword.svelte";
  import ConfirmEmail from "ui/ConfirmEmail.svelte";
  import ErrorPage from "ui/ErrorPage.svelte";

  let screenWidth = 0;

  $: mobile = screenWidth < 850;
</script>

<style>
  #app {
    height: 100vh;
  }
</style>

<div id="app" bind:clientWidth={screenWidth}>
  <Router>
    <Route path="/:channel_username/chat" let:params>
      <PopUpChat channel_username={params.channel_username} />
    </Route>
    <Route path="/:channel_username" let:params>
      <TopBar>
        <StreamPage channel_username={params.channel_username} {mobile} />
      </TopBar>
    </Route>
    <Route path="/account/activate/:uid/:token" let:params>
      <TopBar>
        <ConfirmEmail uid={params.uid} token={params.token} />
      </TopBar>
    </Route>
    <Route path="/account/password/reset/:uid/:token" let:params>
      <TopBar>
        <SetNewPassword uid={params.uid} token={params.token} />
      </TopBar>
    </Route>
    <Route path="/account/password/reset/">
      <TopBar>
        <ResetPassword />
      </TopBar>
    </Route>
    <Route path="/">
      <TopBar>
        <Thumbnails />
      </TopBar>
    </Route>
    <Route>
      <TopBar>
        <ErrorPage />
      </TopBar>
    </Route>
  </Router>
</div>
