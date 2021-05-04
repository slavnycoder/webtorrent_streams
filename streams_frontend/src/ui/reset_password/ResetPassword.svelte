<script>
  import { onMount } from "svelte";
  import Textfield from "@smui/textfield";
  import Button, { Label } from "@smui/button";
  import HelperText from "@smui/textfield/helper-text/index";

  import { getToken, href, reset_password } from "utils.js";
  import { userProfile } from "stores.js";

  onMount(() => {
    if (getToken()) {
      href("/");
    }
  });

  let email = "";
  let email_valid = true;
  let email_sent = false;

  $: email => {
    email_valid = true;
  };

  function _reset_password() {
    if (!email) {
      email_valid = false;
    } else {
      reset_password(email);
      email_sent = true;
    }
  }
</script>

<style>
  #password-recovery {
    display: flex;
    width: 100%;
    height: 100%;
    justify-content: center;
    align-items: center;
  }

  #recovery-form {
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

  #email-sent {
    color: #388e3c;
  }
</style>

{#if !$userProfile.username}
  <div id="password-recovery">
    <div id="recovery-form">
      {#if !email_sent}
        Восстановление пароля
        <Textfield
          type="text"
          label="Email"
          bind:value={email}
          style="min-width: 250px"
          invalid={!email_valid}
          input$autocomplete="email" />
        <div class="separator" />
        <Button variant="raised" on:click={_reset_password}>
          <Label>Восстановить</Label>
        </Button>
      {:else}
        <div id="email-sent">инструкция по восстановлению отправлена</div>
      {/if}
    </div>
  </div>
{/if}
