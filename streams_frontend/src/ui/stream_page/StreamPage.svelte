<script>
  export let channel_username;
  export let mobile;

  import HlsPlayer from "assets/player/HlsPlayer.svelte";
  import LoadingPage from "ui/LoadingPage.svelte";
  import ErrorPage from "ui/ErrorPage.svelte";
  import PanelSet from "panels/PanelSet.svelte";
  import ChannelTopBar from "channel_top_bar/ChannelTopBar.svelte";
  import Chat from "ui/chat/Chat.svelte";

  import TabBar from "@smui/tab-bar";
  import Tab, { Label as TabLabel } from "@smui/tab";

  import { get_stream } from "utils.js";
  import { centrifuge_cli } from "stores.js";
  import {
    arrow_right,
    arrow_left,
    navbar_height,
    collapsed_chat_width,
    expanded_chat_width
  } from "constants.js";

  let channel_data;
  let is_followed;
  let ws_channel;

  let tabs = [{ k: 0, label: "Описание" }, { k: 1, label: "Чат" }];
  let active_tab = tabs[1];

  $: if (channel_data) {
    is_followed = channel_data.is_followed;
  }

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

  $: chat_width =
    !mobile && chat_shown ? expanded_chat_width : collapsed_chat_width;

  let chat_shown = true;

  async function toggle_chat() {
    chat_shown = !chat_shown;
  }
</script>

<style>
  #stream-and-chat {
    display: grid;
    height: 100%;
    grid-template-columns: auto var(--chat_width);
    grid-template-rows: 100%;
    grid-column-gap: 0px;
    grid-row-gap: 0px;
    background: #111;
  }

  #stream-section {
    overflow-y: scroll;
  }

  #stream-description-and-info {
    display: flex;
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

  #chat-section {
    border-left: 1px solid #000;
    width: var(--chat_width);
  }

  #mobile-chat-wrap {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 450px;
  }

  #chat-toggle {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    right: 0;
    width: calc(var(--navbar_height) / 2);
    height: var(--navbar_height);
    background: #333;
    clear: both;
    z-index: 3;
  }

  #chat-toggle:hover {
    cursor: pointer;
    background: #444;
  }
</style>

{#await initStream()}
  <LoadingPage />
{:then _}
  <div
    id="stream-and-chat"
    style="--chat_width:{chat_width + 'px'}; --navbar_height:{navbar_height + 'px'};">
    <div id="stream-section">
      <ChannelTopBar {channel_data} {channel_username} {is_followed} />
      <HlsPlayer {channel_data} />
      <div id="stream-info">
        {#if channel_data.stream}
          <div id="stream-description-and-info">
            <div id="stream-description">{channel_data.stream.description}</div>
            <div id="stream-viewers-count">
              <div class="online-circle" />
              {channel_data.stream.viewers}
            </div>
          </div>
        {/if}
        {#if mobile}
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
        {:else}
          <PanelSet {channel_data} />
        {/if}
      </div>
    </div>
    {#if !mobile}
      <div id="chat-section">
        <div id="chat-toggle-wrap">
          <div id="chat-toggle" on:click={toggle_chat}>
            <img src={chat_shown ? arrow_right : arrow_left} alt="toggle" />
          </div>
        </div>
        {#if chat_shown}
          <Chat
            chat_channel={channel_data.ws_chat_channel}
            {channel_username}
            popup={false} />
        {/if}
      </div>
    {/if}
  </div>
{:catch error}
  <ErrorPage error_status={error} />
{/await}
