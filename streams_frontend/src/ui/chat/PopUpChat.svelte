<script>
  export let channel_username;

  import Chat from "Chat.svelte";
  import LoadingPage from "ui/LoadingPage.svelte";

  import { init_ws } from "assets/centrifuge_cli/client.js";
  import { get_stream } from "utils.js";

  async function initStream() {
    await init_ws();
    return await get_stream(channel_username);
  }
</script>

{#await initStream()}
  <LoadingPage />
{:then channel_data}
  <Chat
    chat_channel={channel_data.ws_chat_channel}
    {channel_username}
    popup={true} />
{/await}
