<script>
  export let dialog;
  import { load } from "recaptcha-v3";

  import Dialog, { Title as DialogTitle, Content } from "@smui/dialog";
  import HelperText from "@smui/textfield/helper-text/index";
  import Button, { Label } from "@smui/button";
  import Textfield from "@smui/textfield";
  import LinearProgress from "@smui/linear-progress";

  import { UserProfile, userProfile } from "stores.js";
  import { login, sleep, href } from "utils.js";

  let loginInProgress = false;

  let username = "";
  let password = "";

  let creds_are_valid = true;
  let creds_err_text = "";

  let global_err = false;
  let global_err_text = "";

  $: (username, password) => {
    creds_are_valid = true;
  };

  function closeLoginDialog() {
    dialog.close();
    username = "";
    password = "";
  }

  async function submitLoginForm() {
    loginInProgress = true;

    creds_are_valid = true;
    global_err = false;
    await sleep(200);
    creds_are_valid = username && password;

    if (creds_are_valid) {
      try {
        const recaptcha = await load(
          "6LdhmLwUAAAAABK31j8H7JxR1DDh68xFKQoYePAa"
        );
        const token = await recaptcha.execute("login");
        await login(username, password, token);
      } catch (error_response) {
        try {
          const response_data = await error_response.json();
          if (response_data.non_field_errors) {
            creds_err_text = "неверный логин или пароль";
            creds_are_valid = false;
          } else if (response_data.captcha) {
            creds_err_text = "подозрительный запрос";
            creds_are_valid = false;
          } else {
            global_err = true;
          }
        } catch (_) {
          global_err = true;
        }
      }
    }
    loginInProgress = false;
  }

  function onKeyDown(e) {
    if (e.which == 13 || e.keyCode == 13) {
      e.preventDefault();
      submitLoginForm();
      return false;
    }
    return true;
  }
</script>

<style>
  #login-dialog {
    z-index: 99;
  }

  #login-form {
    display: flex;
    align-items: stretch;
    flex-wrap: wrap;
    flex-direction: column;
    max-height: 30%;
  }

  #login-actions {
    display: flex;
    position: relative;
    flex-shrink: 0;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-evenly;
    box-sizing: border-box;
    min-height: 52px;
    margin: 0;
    padding: 8px;
    border-top: 1px solid transparent;
  }
</style>

<div id="login-dialog">
  <DialogTitle>Вход</DialogTitle>
  <Content>
    <form id="login-form">
      <Textfield
        disabled={loginInProgress}
        type="text"
        label="Имя пользователя"
        bind:value={username}
        invalid={!creds_are_valid}
        on:keydown={onKeyDown}
        input$autocomplete="username" />
      <HelperText />
      <Textfield
        disabled={loginInProgress}
        type="password"
        label="Пароль"
        bind:value={password}
        invalid={!creds_are_valid}
        on:keydown={onKeyDown}
        input$autocomplete="current-password" />
      <HelperText validationMsg>{creds_err_text}</HelperText>
      <HelperText persistent={global_err}>{global_err_text}</HelperText>
    </form>
  </Content>
  <div id="login-actions">
    <Button
      on:click={() => href('/account/password/reset/')}
      variant="outlined">
      <Label>Забыл пароль</Label>
    </Button>
    <Button
      on:click={submitLoginForm}
      variant="raised"
      action="submit"
      disabled={loginInProgress}>
      <Label>Войти</Label>
    </Button>
  </div>
</div>
