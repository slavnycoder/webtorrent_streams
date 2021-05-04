<script>
  export let chat_channel;
  export let channel_username;
  export let popup = false;
  export let mobile = false;

  import { onMount, onDestroy } from "svelte";

  import LoadingPage from "ui/LoadingPage.svelte";
  import ChatMessage from "widgets/ChatMessage.svelte";
  import ChatHud from "widgets/ChatHud.svelte";

  import {
    arrow_right,
    arrow_left,
    navbar_height,
    chat_toogle_duration,
    expanded_chat_width
  } from "constants.js";
  import { sleep } from "utils.js";
  import { centrifuge_cli } from "stores.js";

  class Message {
    constructor(data) {
      this.type = data.type;
      this.username = data.username;
      this.username_color = data.username_color;
      this.text = data.text;
    }
  }

  let chat_subscription;

  let autoscrollEnabled = true;
  let scrollOffset;
  let msg_list;
  let chat_bottom;

  let messages = [];

  let chat_scroll_timer;

  async function scrollDownChat(wait) {
    if (wait) await sleep(250);
    if (chat_bottom) chat_bottom.scrollIntoView();
  }

  function add_new_msg(msg_data) {
    messages = [...messages, new Message(msg_data)];
    if (autoscrollEnabled) scrollDownChat(true);
  }

  async function init_chat() {
    await sleep(chat_toogle_duration);
    centrifuge_cli.update(client => {
      if (client) {
        chat_subscription = client.subscribe(chat_channel, new_msg =>
          add_new_msg(new_msg.data)
        );
        chat_subscription
          .history()
          .then(response =>
            response.publications.forEach(new_msg => add_new_msg(new_msg.data))
          );
        add_new_msg({
          type: "service",
          text: "добро пожаловать"
        });
      }
      return client;
    });

    chat_scroll_timer = setInterval(() => {
      if (msg_list) {
        scrollOffset =
          (msg_list.scrollHeight - msg_list.scrollTop) / msg_list.offsetHeight;
        autoscrollEnabled = scrollOffset < 1.5;
      }
    }, 200);
  }

  onMount(() => {
    init_chat();
  });

  onDestroy(() => {
    clearInterval(chat_scroll_timer);
    if (chat_subscription) {
      chat_subscription.unsubscribe();
    }
  });
</script>

<style>
  #chat {
    display: grid;
    grid-template-rows: var(--navbar_height) auto 100px;
    height: 100%;
  }

  #header {
    display: flex;
    justify-content: center;
    align-items: center;
    color: #e0e0e0;
    background: #000;
    text-transform: uppercase;
    font-weight: bold;
    overflow: hidden;
  }
  
  #messages {
    display: flex;
    flex-grow: 1;
    overflow-y: scroll;
    background: #212121;
  }

  #msg-list {
    width: 100%;
  }

  #scroll-down-wrap {
    display: flex;
    justify-content: center;
    position: relative;
    align-self: center;
    width: 100%;
    height: 0px;
    float: both;
  }

  #scroll-down {
    display: flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: -150px;
    background-color: rgba(0, 0, 0, 0.7);
    color: #e0e0e0;
    width: 70%;
    min-height: 40px;
    border-radius: 15px;
    cursor: pointer;
  }
</style>

<div
  id="chat"
  style="--chat_width:{expanded_chat_width + 'px'}; --navbar_height:{navbar_height + 'px'}">
  {#if !mobile}
    <div id="header">ЧАТ</div>
  {:else}
    <div />
  {/if}
  <div bind:this={msg_list} id="messages">
    <div id="msg-list">
      {#each messages as msg}
        <ChatMessage {msg} />
      {/each}
      <div bind:this={chat_bottom} id="chat-bottom" />
    </div>
  </div>
  {#if !popup}
    <ChatHud {chat_subscription} {channel_username} />
    {#if !autoscrollEnabled}
      <div id="scroll-down-wrap">
        <div on:click={() => scrollDownChat(false)} id="scroll-down">
          сообщения ниже
        </div>
      </div>
    {/if}
  {/if}
</div>
