<script>
  export let uid = undefined;
  export let token = undefined;

  import LoadingPage from "ui/LoadingPage.svelte";

  import { confirm_email } from "utils.js";

  async function _confirm_email() {
    await confirm_email(uid, token);
  }
</script>

<style>
  #confirm-email {
    display: flex;
    width: 100%;
    height: 100%;
    justify-content: center;
    align-items: center;
  }

  #email-confirmed {
    color: #388e3c;
  }

  #email-confirm-err {
    color: #d32f2f;
  }
</style>

<div id="confirm-email">
  {#await _confirm_email()}
    <LoadingPage />
  {:then _}
    <div id="email-confirmed">Email подтверждён.</div>
  {:catch error}
    <div id="email-confirm-err">Email уже подтверждён.</div>
  {/await}
</div>
