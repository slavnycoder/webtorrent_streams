<script>
  export let channel_username;

  import { onDestroy } from "svelte";

  import TabBar from "@smui/tab-bar";
  import Tab, { Label as TabLabel } from "@smui/tab";

  import HlsPlayer from "assets/player/HlsPlayer.svelte";
  import LoadingPage from "ui/LoadingPage.svelte";
  import ErrorPage from "ui/ErrorPage.svelte";

  import PanelSet from "panels/PanelSet.svelte";
  import Chat from "ui/chat/Chat.svelte";

  import { get_stream, get_gravatar_link } from "utils.js";
  import { userProfile, centrifuge_cli } from "stores.js";

  import {
    arrow_right,
    arrow_left,
    navbar_height,
    collapsed_chat_width,
    expanded_chat_width,
    chat_width
  } from "constants.js";

  let tabs = [{ k: 0, label: "Описание" }, { k: 1, label: "Чат" }];
  let active_tab = tabs[1];

  let ws_channel;
  let channel_data;
  let is_followed;

  $: if (channel_data) {
    is_followed = channel_data.is_followed;
  }

  onDestroy(() => {
    if (ws_channel) {
      ws_channel.unsubscribe();
    }
  });

  async function initStream() {
    channel_data = await get_stream(channel_username);
    centrifuge_cli.update(client => {
      if (client) {
        ws_channel = client.subscribe(channel_data.ws_channel, message => {
          if (message.data.type == "channel_updated") {
            channel_data = message.data.channel;
          } else if (message.data.type == "stream_started") {
            channel_data.stream = message.data.stream;
          }
        });
      }
      return client;
    });
  }

  let chat_shown = true;
  async function toggle_chat() {
    if (chat_shown) {
      chat_width.set(collapsed_chat_width);
    } else {
      chat_width.set(expanded_chat_width);
    }
    chat_shown = !chat_shown;
  }
</script>

<style>
  #player-and-chat {
    display: flex;
    width: 100%;
  }

  /* central */
  #central {
    overflow-y: scroll;
    height: 100%;
    width: 100%;
    -ms-overflow-style: none;
    scrollbar-width: none;
    background-color: #111;
  }

  /* chat */
  #mobile-chat-wrap {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
  }

  #upper-channel-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: fixed;
    top: var(--navbar_height);
    width: 100%;
    height: var(--navbar_height);
    background-color: #111;
    z-index: 2;
  }

  #bottom-channel-info {
    display: flex;
    flex-direction: column;
    padding: 0px;
  }

  #stream-description-and-info {
    display: flex;
    width: 100%;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
  }

  #stream-description {
    font-size: 1.5rem;
    color: #e0e0e0;
  }

  #stream-viewers-count {
    display: flex;
    align-items: center;
    color: #e0e0e0;
  }

  .online-circle {
    margin: 4px;
    height: 1em;
    width: 1em;
    background-color: red;
    border-radius: 50%;
  }

  #channel-info {
    display: flex;
    justify-content: center;
    align-items: center;
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

{#await initStream()}
  <LoadingPage />
{:then test}
  <div
    id="player-and-chat"
    style="--chat_width:{$chat_width + 'px'};--navbar_height:{navbar_height + 'px'}">
    <div id="central">
      <div id="upper-channel-bar">
        <div class="empty" />
        <div id="channel-info">
          <img
            id="channel-avatar"
            src={channel_data.img_url || get_gravatar_link(channel_username)}
            alt="" />
          <h3 id="channel-display-name">{channel_data.display_name}</h3>
        </div>
      </div>
      <HlsPlayer {channel_data} />
      <div id="bottom-channel-info">
        {#if channel_data.stream}
          <div id="stream-description-and-info">
            <div id="stream-description">{channel_data.stream.description}</div>
            <div id="stream-viewers-count">
              <div class="online-circle" />
              {channel_data.stream.viewers}
            </div>
          </div>
        {/if}
        <TabBar {tabs} let:tab key={tab => tab.k} bind:active={active_tab}>
          <Tab {tab}>
            <TabLabel style="color: #eee;">{tab.label}</TabLabel>
          </Tab>
        </TabBar>
        {#if active_tab.k == tabs[0].k}
          <PanelSet {channel_data} />
        {:else}
          <div id="mobile-chat-wrap">
            <Chat
              chat_channel={channel_data.ws_chat_channel}
              {channel_username}
              popup={false}
              mobile={true} />
          </div>
        {/if}
      </div>
    </div>
  </div>
{:catch error}
  <ErrorPage error_status={error.status} />
{/await}
