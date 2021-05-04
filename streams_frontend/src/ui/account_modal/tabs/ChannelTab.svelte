<script>
  import copy from "copy-to-clipboard";
  import { onMount } from "svelte";

  import Textfield from "@smui/textfield";
  import Button, { Label, Icon } from "@smui/button";
  import HelperText from "@smui/textfield/helper-text/index";
  import { userProfile } from "stores.js";

  import LoadingPage from "ui/LoadingPage.svelte";

  import {
    get_stream_settings,
    update_stream_description,
    reset_stream_key
  } from "utils.js";

  let stream_description = "";
  let stream_description_helper_text = "";
  let stream_description_max_length = 120;

  let stream_key = "";
  let show_key = false;
  let stream_key_helper_text = "";

  userProfile.subscribe(profile => {
    stream_key = profile.stream_key || "";
  });

  async function _update_stream_description() {
    const response = await update_stream_description(stream_description);
    stream_description_helper_text = "описание сохранено";
  }

  async function _get_stream_settings() {
    const response = await get_stream_settings();
    const json_data = await response.json();
    stream_description = json_data.stream_description;
    stream_key = json_data.stream_key;
  }

  async function _reset_stream_key() {
    stream_key_helper_text = "";
    const response = await reset_stream_key();
    const json_data = await response.json();
    stream_key = json_data.stream_key;
    stream_key_helper_text = "ключ обновлён";
  }

  function copy_key() {
    copy(stream_key);
    stream_key_helper_text = "ключ скопирован";
  }
</script>

<style>
  #channel-tab {
    display: flex;
    flex-direction: column;
  }

  .stream-settings-form {
    display: flex;
    flex-direction: column;
    width: 60%;
    padding: 15px;
    border-radius: 15px;
    background-color: #e0e0e0;
  }

  .stream-settings-section {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
  }

  #stream-key-field {
    display: flex;
    width: 100%;
    align-items: flex-end;
  }

  .separator {
    height: 1px;
    width: 100%;
    margin: 5px 0px;
  }
</style>

<div id="channel-tab">
  {#await _get_stream_settings()}
    <LoadingPage dark={true} />
  {:then _}
    <div class="stream-settings-form">
      <div class="stream-settings-section">
        <Textfield
          label="Описание стрима"
          style="width: 100%;"
          bind:value={stream_description}
          input$autocomplete="off" />
        <div
          id="char-counter"
          style="color:{stream_description.length > stream_description_max_length ? '#b71c1c' : '#000'}">
          {stream_description.length}/{stream_description_max_length}
        </div>
        <HelperText persistent>{stream_description_helper_text}</HelperText>
        <div class="separator" />
        <Button on:click={_update_stream_description} variant="raised">
          <Label>Сохранить</Label>
        </Button>
      </div>
    </div>
    <div class="separator" />
    <div class="stream-settings-form">
      <div class="stream-settings-section">
        <div id="stream-key-field">
          <Textfield
            label="Ключ"
            style="width: 100%;"
            bind:value={stream_key}
            input$style="-webkit-text-security:{!show_key ? 'disc' : 'none'}"
            input$autocomplete="off" />
          <Icon
            class="material-icons"
            role="button"
            style="cursor:pointer;padding:8px;"
            on:click={() => (show_key = !show_key)}>
            remove_red_eye
          </Icon>
        </div>
        <HelperText persistent>{stream_key_helper_text}</HelperText>
        <div class="separator" />
        <div>
          <Button on:click={_reset_stream_key} variant="outlined">
            <Label>Сгенерировать новый</Label>
          </Button>
          <Button on:click={copy_key} variant="raised">
            <Label>Скопировать</Label>
          </Button>
        </div>
      </div>
    </div>
  {:catch _}
    <div>Обратитесь к администрации, чтобы получить ключ для стрима.</div>
  {/await}

</div>
