<script>
  export let channel_data;

  import Button, { Label, Icon } from "@smui/button";

  import Panel from "./Panel.svelte";
  import LoadingPage from "ui/LoadingPage.svelte";

  import { userProfile } from "stores.js";
  import { create_new_panel, delete_panel } from "utils.js";

  const MAX_PANELS_COUNT = 20;

  let edit_mode = false;

  let creating_panel = false;

  class PanelData {
    constructor(data) {
      let { id, title, sort, image_src, image_link, text } = data;
      this.id = id;
      this.sort = sort;
      this.title = title || "";
      this.image_src = image_src || "";
      this.image_link = image_link || "";
      this.text = text || "";
    }
  }

  let panels_data = Array.from(
    channel_data.panels,
    panel_data => new PanelData(panel_data)
  );

  async function add_empty_panel() {
    if (!creating_panel) {
      creating_panel = true;
      try {
        const response = await create_new_panel();
        const panel_data = await response.json();
        panels_data = [...panels_data, new PanelData(panel_data)];
      } catch (_) {}
      creating_panel = false;
    }
  }

  function remove_panel(idx) {
    const removed = panels_data.splice(idx, 1);
    delete_panel(removed[0].id);
    panels_data = [...panels_data];
  }
</script>

<style>
  #panels-edit-buttons {
    margin: 10px 15px;
  }

  #panels {
    display: grid;
    justify-content: center;
    grid-template-columns: repeat(auto-fit, 350px);
    grid-gap: 1.5rem;
  }

  #add-panel-div {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 350px;
    height: 485px;
    border: 1px solid #444;
  }

  #add-panel-div:hover {
    cursor: pointer;
    background-color: #222;
  }

  .add-panel-btn {
    font-size: 100px;
  }
</style>

<div id="panels-section">
  {#if $userProfile.username == channel_data.username}
    <div id="panels-edit-buttons">
      {#if !edit_mode}
        <Button
          color="secondary"
          variant="outlined"
          on:click={() => (edit_mode = true)}>
          <Label>редактировать</Label>
        </Button>
      {:else}
        <div>
          <Button
            color="secondary"
            variant="outlined"
            on:click={() => (edit_mode = false)}>
            <Label>просмотр</Label>
          </Button>
        </div>
      {/if}
    </div>
  {/if}
  <div id="panels">
    {#each panels_data as panel_data, idx}
      <Panel
        {...panel_data}
        {edit_mode}
        remove_panel={() => remove_panel(idx)} />
    {/each}
    {#if edit_mode && MAX_PANELS_COUNT > panels_data.length}
      <div id="add-panel-div" on:click={add_empty_panel}>
        {#if creating_panel}
          <LoadingPage />
        {:else}
          <div class="add-panel-btn">+</div>
        {/if}
      </div>
    {/if}
  </div>
</div>
