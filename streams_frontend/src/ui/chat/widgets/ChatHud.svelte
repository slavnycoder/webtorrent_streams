<script>
  export let chat_subscription;
  export let channel_username;

  import { onMount } from "svelte";
  import Button, { Label, Icon } from "@smui/button";

  import ReplySuggest from "ReplySuggest.svelte";
  import Emoticons from "Emoticons.svelte";

  import throttle from "just-throttle";
  import { userProfile } from "stores.js";
  import { send_chat_msg, is_key } from "utils.js";

  const USER_SUGGESTION_PATTERN = /(^|\s)\@([a-z0-9]+)?$/;
  const EMOTICONS_MAP = JSON.parse(localStorage.getItem("emoticons"));
  const MSG_MAX_LENGTH = 500;

  const WIDGET_TABS = {
    REPLY: "reply",
    EMOTICONS: "emoticons"
  };

  let msg_textarea;
  let msg_text = "";

  let widget_open = false;
  let current_widget_tab = WIDGET_TABS.REPLY;

  let textarea_focused = false;
  let selected_user = 0;
  let usernames = [];
  let filtered_usernames = [];
  let name_start = "";

  function filter_usernames(_usernames, _name_start) {
    let new_filtered_usernames = _usernames.filter(curr_username => {
      if (curr_username.length <= 16) {
        if (!name_start) {
          return true;
        } else if (curr_username.startsWith(_name_start)) {
          return true;
        }
      }
      return false;
    });
    new_filtered_usernames = [...new Set(new_filtered_usernames)];
    new_filtered_usernames.sort();
    return new_filtered_usernames.slice(0, 5);
  }

  $: filtered_usernames = filter_usernames(usernames, name_start);

  function replace_before_cursor(text, text_input, pattern, value) {
    let begining = text.slice(0, text_input.selectionEnd);
    const ending = text.slice(text_input.selectionEnd, -1);
    if (pattern && begining.match(pattern)) {
      begining = begining.replace(pattern, `$1${value} `);
    } else {
      begining += `${value} `;
    }
    msg_text = begining + ending;
    text_input.focus();
  }

  function submit_user_suggestion() {
    replace_before_cursor(
      msg_text,
      msg_textarea,
      USER_SUGGESTION_PATTERN,
      `@${filtered_usernames[selected_user]}`
    );
    widget_open = false;
  }

  function submit_emoticon(name) {
    replace_before_cursor(
      msg_text,
      msg_textarea,
      USER_SUGGESTION_PATTERN,
      ` ${name}`
    );
    widget_open = false;
  }

  async function send_message() {
    const curr_msg_text = msg_text;
    if (curr_msg_text.length > 0 && curr_msg_text.length <= MSG_MAX_LENGTH) {
      send_chat_msg(channel_username, curr_msg_text).catch(errResponse => {
        if (errResponse.status == 500) {
          messages = [
            ...messages,
            new Message({ type: "error", text: "чат недоступен" })
          ];
        }
        msg_text = curr_msg_text;
      });
      msg_text = "";
    }
  }

  const fetch_users = throttle(
    async () => {
      if (chat_subscription) {
        await chat_subscription.presence().then(function(response) {
          let fetched_usernames = [];
          for (let id in response.presence) {
            fetched_usernames.push(response.presence[id].user);
          }
          usernames = fetched_usernames;
        });
      }
    },
    5000,
    true
  );

  function open_hud_widget(tab) {
    if (!widget_open) {
      widget_open = true;
      switch (tab) {
        case WIDGET_TABS.REPLY:
          selected_user = 0;
          fetch_users();
          break;
        default:
          break;
      }
    }
    current_widget_tab = tab;
  }

  function close_hud_widget() {
    widget_open = false;
  }

  function onKeyUp(e) {
    const usernames_matches = msg_text
      .slice(0, msg_textarea.selectionEnd)
      .match(USER_SUGGESTION_PATTERN);
    if (usernames_matches) {
      open_hud_widget(WIDGET_TABS.REPLY);
      name_start = usernames_matches[usernames_matches.length - 1] || "";
    } else {
      close_hud_widget();
    }
    return true;
  }

  function onKeyDown(e) {
    if (widget_open) {
      switch (true) {
        case is_key(e, 38): //up arrow
          selected_user =
            (filtered_usernames.length + selected_user - 1) %
            filtered_usernames.length;
          return false;
        case is_key(e, 40): //down arrow
          selected_user = (selected_user + 1) % filtered_usernames.length;
          return false;
        case is_key(e, 9): //tab
        case is_key(e, 13): //enter
          submit_user_suggestion();
          return false;
        default:
          return true;
      }
    } else {
      switch (true) {
        case is_key(e, 13): //enter
          send_message();
          return false;
        default:
          return true;
      }
    }
  }

  onMount(() => {
    fetch_users();
  });
</script>

<style>
  #hud {
    display: flex;
    justify-content: flex-start;
    flex-direction: column;
    padding: 0px 6px 6px 6px;
    background-color: #111;
  }

  #chat-textarea {
    width: 100%;
    height: 25px;
    padding: 12px 10px 8px 10px;
    margin: 8px 0px;
    overflow: auto;
    resize: none;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
    color: #e0e0e0;
    background-color: #222;
    border: 2px solid transparent;
  }

  #chat-textarea:focus {
    outline: none !important;
    border: 2px solid #0077c7;
  }

  .chat-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  #char-counter {
    color: #bdbdbd;
  }

  #ask-auth {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    overflow: hidden;
  }

  #hud-widget-wrap {
    position: relative;
    height: 0px;
  }

  #hud-widget {
    position: relative;
    background-color: #111;
    width: 100%;
    transform: translate(0, -100%);
    z-index: 99;
  }

  #hud-widget-tab-bar {
    display: flex;
    border-top: 1px solid #757575;
  }

  .hud-widget-tab {
    color: #e0e0e0;
    font-weight: 700;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2px;
    width: 45px;
  }

  .hud-widget-tab.selected {
    background-color: #555;
  }

  .hud-widget-tab:hover {
    cursor: pointer;
    background-color: #757575;
  }

  #emoticon-btn {
    margin-right: 10px;
    color: #757575;
  }

  #emoticon-btn:hover {
    cursor: pointer;
    color: #e0e0e0;
  }

  .align-center {
    display: flex;
    align-items: center;
  }
</style>

<div id="hud">
  {#if $userProfile.username}
    {#if widget_open && textarea_focused}
      <div id="hud-widget-wrap">
        <div id="hud-widget">
          {#if current_widget_tab == WIDGET_TABS.REPLY}
            <ReplySuggest
              {filtered_usernames}
              {submit_user_suggestion}
              bind:selected_user />
          {:else if current_widget_tab == WIDGET_TABS.EMOTICONS}
            <Emoticons emoticons_map={EMOTICONS_MAP} {submit_emoticon} />
          {/if}
          <div id="hud-widget-tab-bar">
            <div
              on:mousedown={e => {
                e.preventDefault();
                current_widget_tab = WIDGET_TABS.REPLY;
              }}
              class="hud-widget-tab {current_widget_tab == WIDGET_TABS.REPLY ? 'selected' : ''}">
              @
            </div>
            <div
              on:mousedown={e => {
                e.preventDefault();
                current_widget_tab = WIDGET_TABS.EMOTICONS;
              }}
              class="hud-widget-tab {current_widget_tab == WIDGET_TABS.EMOTICONS ? 'selected' : ''}">
              <Icon class="material-icons">emoji_emotions</Icon>
            </div>
          </div>
        </div>
      </div>
    {/if}
    <div class="chat-controls">
      <textarea
        id="chat-textarea"
        bind:this={msg_textarea}
        bind:value={msg_text}
        on:focus={() => {
          textarea_focused = true;
        }}
        on:focusout={() => {
          textarea_focused = false;
        }}
        rows="1"
        on:keydown={onKeyDown}
        on:keyup={onKeyUp} />
    </div>
    <div class="chat-controls">
      <div
        id="char-counter"
        style="color:{msg_text.length > MSG_MAX_LENGTH ? '#b71c1c' : '#e0e0e0'}">
        {msg_text.length}/{MSG_MAX_LENGTH}
      </div>
      <div class="align-center">
        <div
          id="emoticon-btn"
          on:mousedown={e => {
            e.preventDefault();
            textarea_focused = true;
            open_hud_widget(WIDGET_TABS.EMOTICONS);
          }}>
          <Icon class="material-icons">emoji_emotions</Icon>
        </div>
        <Button on:click={send_message} variant="raised">
          <Label>Send</Label>
        </Button>
      </div>
    </div>
  {:else}
    <div id="ask-auth">
      Зарегистрируйтесь или войдите, чтобы отправлять сообщения.
    </div>
  {/if}
</div>
