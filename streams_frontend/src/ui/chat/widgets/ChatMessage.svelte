<script>
  export let msg;

  import { onMount } from "svelte";
  import { userProfile } from "stores.js";

  class TextSpan {
    constructor(span_class, text, url) {
      this.span_class = span_class;
      this.text = text;
      this.url = url;
    }
  }

  let curr_username = "";

  userProfile.update(profile => {
    curr_username = profile.username;
    return profile;
  });

  const REPLY_PATTERN = new RegExp("^@" + curr_username + "$");
  const EMOTICON_CLASS = "emoticon";
  const REPLY_CLASS = "reply";
  const TEXT_CLASS = "text";

  const EMOTICONS_MAP = JSON.parse(localStorage.getItem("emoticons"));

  function render_msg(msg) {
    const ret = [];

    const spans = msg.text.split(" ").map(span_text => {
      const emoticon = EMOTICONS_MAP[span_text];
      if (span_text.match(REPLY_PATTERN)) {
        return new TextSpan(REPLY_CLASS, span_text);
      } else if (emoticon) {
        return new TextSpan(
          EMOTICON_CLASS,
          span_text,
          `https://cdn.frankerfacez.com/${emoticon.url}`
        );
      } else {
        return new TextSpan(TEXT_CLASS, span_text);
      }
    });

    let current_span;
    spans.forEach(new_span => {
      if (!current_span) {
        current_span = new_span;
      } else if (
        current_span.span_class == new_span.span_class &&
        current_span.span_class == TEXT_CLASS
      ) {
        current_span.text = [current_span.text, new_span.text].join(" ");
      } else {
        ret.push(current_span);
        ret.push(new TextSpan("", " "));
        current_span = new_span;
      }
    });
    if (current_span) {
      ret.push(current_span);
    }
    return ret;
  }
</script>

<style>
  .username {
    font-weight: 500;
  }
  .msg {
    padding: 5px;
    font-size: 0.9em;
    color: #e0e0e0;
    word-wrap: break-word;
  }

  .reply {
    color: black;
    background-color: #e0e0e0;
  }
</style>

<div class="msg">
  {#if msg.type == 'user'}
    <span class="username" style="color:{msg.username_color}">
      {msg.username + ':'}
    </span>
    {#each render_msg(msg) as span}
      {#if span.span_class == EMOTICON_CLASS}
        <img class={span.span_class} src={span.url} alt={span.text} />
      {:else}
        <span class={span.span_class}>{span.text}</span>
      {/if}
    {/each}
  {:else if msg.type == 'error'}
    <span style="color:#b00020">{'Ошибка: ' + msg.text}</span>
  {:else}
    <span style="color:#bdbdbd">{msg.text}</span>
  {/if}
</div>
