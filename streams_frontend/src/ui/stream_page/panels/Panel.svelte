<script>
  export let edit_mode;
  export let remove_panel;

  export let id;
  export let sort;
  export let title;
  export let image_src;
  export let image_link;
  export let text;

  import showdown from "showdown";

  import { onMount } from "svelte";
  import Button, { Label, Icon } from "@smui/button";
  import Dialog from "@smui/dialog";

  import ImageDialog from "ImageDialog.svelte";
  import { update_panel, set_panel_image } from "utils.js";

  let converter = new showdown.Converter();

  let img_dialog;
  let img_input;
  let files = [];
  let submit_btn_disabled = false;

  $: files.length ? img_dialog.open() : void 0;

  function enable_submit_btn() {
    submit_btn_disabled = false;
  }

  $: title || image_link || text ? enable_submit_btn() : enable_submit_btn();

  function image_dialog_close_handler(e) {
    switch (e.detail.action) {
      case "submit":
        image_src = URL.createObjectURL(files[0]);
        set_panel_image(id, files[0]);
        break;
      default:
        break;
    }
    img_input.value = "";
    files = [];
  }

  async function submit_panel() {
    submit_btn_disabled = true;
    const response = await update_panel({
      id,
      sort,
      title,
      image_src,
      image_link,
      text
    });
    const response_data = await response.json();
    title = response_data.title;
    image_link = response_data.image_link;
    text = response_data.text;
    image_src = response_data.image_src;
  }
</script>

<style>
  .panel {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: stretch;
    width: 350px;
    color: #e0e0e0;
  }

  .edit-panel {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    padding: 10px;
    width: 330px;
    background-color: #333;
    border: 1px solid #444;
  }

  .edit-panel-section {
    display: flex;
    flex-direction: column;
    margin: 5px 0px;
    width: 100%;
  }

  .panel-img-section {
    display: flex;
    justify-content: space-between;
  }

  .section-title {
    margin: 5px 0px;
    color: #e0e0e0;
    font-size: 0.9rem;
    font-weight: 500;
    align-items: center;
  }

  .text-input {
    padding: 12px 10px 8px 10px;
    overflow: auto;
    resize: none;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
    color: #e0e0e0;
    background-color: #222;
    border: 2px solid transparent;
  }

  .text-input:focus {
    outline: none !important;
    border: 2px solid #0077c7;
  }

  .panel-title {
    font-size: 18px;
    font-weight: 500;
    padding: 8px 0px;
  }

  .panel-image {
    width: 100%;
    height: auto;
  }

  .panel-text {
  }

  .edit-panel-title {
    padding: 4px 4px 4px 8px;
  }

  .edit-image-link {
    padding: 4px 4px 4px 8px;
  }

  .edit-panel-text {
    height: 150px;
  }

  .panel-buttons-section {
    display: flex;
    justify-content: flex-end;
  }
</style>

{#if !edit_mode}
  <div class="panel">
    {#if title}
      <div class="panel-title">{title}</div>
    {/if}
    {#if image_src}
      {#if image_link}
        <a href={image_link} target="_blank">
          <img class="panel-image" src={image_src} alt={title} />
        </a>
      {:else}
        <img class="panel-image" src={image_src} alt={title} />
      {/if}
    {/if}
    {#if text}
      <div class="panel-text">
        {@html converter.makeHtml(text)}
      </div>
    {/if}
  </div>
{:else}
  <div class="edit-panel">
    <div class="edit-panel-section">
      <div class="section-title">Название панели:</div>
      <input
        class="text-input edit-panel-title"
        type="text"
        bind:value={title} />
    </div>
    <div class="edit-panel-section">
      <input
        bind:this={img_input}
        type="file"
        accept="image/png"
        bind:files
        hidden />
      <div class="panel-img-section">
        <div>
          <Button
            variant="raised"
            on:click={() => {
              img_input.click();
            }}
            dense>
            <Icon class="material-icons" style="margin: 0px;">image</Icon>
          </Button>
          {#if image_src}
            <Button
              color="secondary"
              variant="outlined"
              on:click={() => {
                set_panel_image(id);
                image_src = '';
              }}
              dense>
              <Icon class="material-icons" style="margin: 0px;">clear</Icon>
            </Button>
          {/if}
        </div>
        <div>
          {#if image_src}
            <img src={image_src} alt="panel image" height="32" />
          {/if}
        </div>
      </div>
    </div>
    <Dialog
      bind:this={img_dialog}
      on:MDCDialog:closed={image_dialog_close_handler}>
      <ImageDialog bind:files />
    </Dialog>
    <div class="edit-panel-section">
      <div class="section-title">Ссылка изображения:</div>
      <input
        class="text-input edit-image-link"
        type="text"
        bind:value={image_link} />
    </div>
    <div class="edit-panel-section">
      <div class="section-title">Текст панели:</div>
      <textarea class="text-input edit-panel-text" bind:value={text} />
    </div>
    <div class="edit-panel-section">
      <div class="panel-buttons-section">
        <Button
          color="secondary"
          on:click={remove_panel}
          style="text-decoration: underline !important;margin: 5px;"
          dense>
          <Label>Удалить</Label>
        </Button>
        <Button
          variant="raised"
          style="margin: 5px;"
          on:click={submit_panel}
          disabled={submit_btn_disabled}
          dense>
          <Label>Сохранить</Label>
        </Button>
      </div>
    </div>
  </div>
{/if}
