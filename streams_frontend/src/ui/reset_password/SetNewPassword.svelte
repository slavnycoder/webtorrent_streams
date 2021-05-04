<script>
  export let uid = undefined;
  export let token = undefined;

  import { onMount } from "svelte";

  import Textfield from "@smui/textfield";
  import Button, { Label } from "@smui/button";
  import HelperText from "@smui/textfield/helper-text/index";
  import { userProfile } from "stores.js";

  import {
    getToken,
    href,
    set_new_password,
    validate_password
  } from "utils.js";

  onMount(() => {
    if (getToken()) {
      href("/");
    }
  });

  let new_password = "";
  let new_password_is_valid = true;
  let password_err_text = "";
  let new_password_set = false;

  $: new_password => {
    new_password_is_valid = true;
    password_err_text = "";
  };

  async function _set_new_password() {
    [new_password_is_valid, password_err_text] = validate_password(
      new_password
    );
    if (new_password_is_valid) {
      try {
        await set_new_password(uid, token, new_password);
        new_password_set = true;
      } catch (_) {
        new_password_is_valid = false;
        password_err_text = "ошибка сервера";
      }
    }
  }
</script>

<style>
  #set-new-password {
    display: flex;
    width: 100%;
    height: 100%;
    justify-content: center;
    align-items: center;
  }

  #set-password-form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    background-color: #e0e0e0;
    padding: 15px;
    margin: 30px;
    border-radius: 15px;
    min-width: 250px;
    min-height: 100px;
  }

  .separator {
    height: 1px;
    width: 100%;
    margin: 5px 0px;
  }

  #password-set {
    color: #d32f2f;
  }
</style>

{#if !$userProfile.username}
  <div id="set-new-password">
    <div id="set-password-form">
      {#if !new_password_set}
        Придумай новый пароль
        <Textfield
          type="password"
          label="Новый пароль"
          bind:value={new_password}
          style="min-width: 250px"
          invalid={!new_password_is_valid}
          input$autocomplete="new-password" />
        <HelperText validationMsg>{password_err_text}</HelperText>
        <div class="separator" />
        <Button variant="raised" on:click={_set_new_password}>
          <Label>Сменить</Label>
        </Button>
      {:else}
        <div id="password-set">пароль изменён. на этот раз не проеби</div>
      {/if}
    </div>
  </div>
{/if}
