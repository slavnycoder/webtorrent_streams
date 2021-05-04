<script>
  export let dialog;
  import { load } from "recaptcha-v3";

  import Dialog, { Title as DialogTitle, Content } from "@smui/dialog";
  import HelperText from "@smui/textfield/helper-text/index";
  import Button, { Label } from "@smui/button";
  import Textfield from "@smui/textfield";

  import { UserProfile, userProfile } from "stores.js";

  import {
    signUp,
    validate_username,
    validate_password,
    validate_email,
    sleep
  } from "utils.js";

  let signup_in_progress = false;

  let username = "";
  let email = "";
  let password = "";

  let username_is_valid = true;
  let email_is_valid = true;
  let password_is_valid = true;

  let global_err = false;
  let global_err_text = "ошибка сервера";

  $: username => {
    username_is_valid = true;
  };
  $: email => {
    email_is_valid = true;
  };
  $: password => {
    password_is_valid = true;
  };

  let username_err_text = "";
  let email_err_text = "";
  let password_err_text = "";

  function closeSignUpDialog() {
    dialog.close();
    username = "";
    password = "";
    email = "";
  }

  async function submit_signup_form() {
    signup_in_progress = true;

    username_is_valid = true;
    email_is_valid = true;
    password_is_valid = true;
    await sleep(200);
    [username_is_valid, username_err_text] = validate_username(username);
    [email_is_valid, email_err_text] = validate_email(email);
    [password_is_valid, password_err_text] = validate_password(password);

    if (username_is_valid & email_is_valid & password_is_valid) {
      try {
        const recaptcha = await load(
          "6LdhmLwUAAAAABK31j8H7JxR1DDh68xFKQoYePAa"
        );
        const token = await recaptcha.execute("signup");
        await signUp(username, password, email, token);
      } catch (error_response) {
        try {
          const response_data = await error_response.json();
          if (response_data.username == "unique_err") {
            username_is_valid = false;
            username_err_text = "имя пользователя занято";
          }
          if (response_data.email == "unique_err") {
            email_is_valid = false;
            email_err_text = "email уже зареган";
          }
          if (response_data.password) {
            password_is_valid = false;
            password_err_text = "какая-то хуйня с паролем";
          }
        } catch (_) {
          global_err = true;
        }
      }
    }
    signup_in_progress = false;
  }

  function on_keydown(e) {
    if (e.which == 13 || e.keyCode == 13) {
      e.preventDefault();
      submit_signup_form();
      return false;
    }
    return true;
  }
</script>

<style>
  #signup-dialog {
    z-index: 99;
  }

  #signup-form {
    display: flex;
    align-items: stretch;
    flex-wrap: wrap;
    flex-direction: column;
    max-height: 30%;
  }

  #signup-actions {
    display: flex;
    position: relative;
    flex-shrink: 0;
    flex-wrap: wrap;
    align-items: center;
    justify-content: flex-end;
    box-sizing: border-box;
    min-height: 52px;
    margin: 0;
    padding: 8px;
    border-top: 1px solid transparent;
  }
</style>

<div id="signup-dialog">
  <DialogTitle>Регистрация</DialogTitle>
  <Content>
    <form id="signup-form">
      <Textfield
        disabled={signup_in_progress}
        type="text"
        label="Имя пользователя"
        bind:value={username}
        invalid={!username_is_valid}
        on:keydown={on_keydown}
        input$autocomplete="username" />
      <HelperText validationMsg>{username_err_text}</HelperText>
      <Textfield
        class="email-field"
        disabled={signup_in_progress}
        type="email"
        label="Email"
        bind:value={email}
        invalid={!email_is_valid}
        on:keydown={on_keydown}
        input$autocomplete="email" />
      <HelperText validationMsg>{email_err_text}</HelperText>
      <Textfield
        disabled={signup_in_progress}
        type="password"
        label="Пароль"
        bind:value={password}
        invalid={!password_is_valid}
        on:keydown={on_keydown}
        input$autocomplete="new-password" />
      <HelperText validationMsg>{password_err_text}</HelperText>
      <HelperText persistent={global_err}>{global_err_text}</HelperText>
    </form>
  </Content>
  <div id="signup-actions">
    <Button
      on:click={submit_signup_form}
      variant="raised"
      disabled={signup_in_progress}>
      <Label>Зарегистрироваться</Label>
    </Button>
  </div>
</div>
