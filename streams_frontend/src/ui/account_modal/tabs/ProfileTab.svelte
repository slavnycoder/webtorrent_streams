<script>
  import Croppie from "croppie";
  import Button, { Label } from "@smui/button";
  import Textfield from "@smui/textfield";
  import HelperText from "@smui/textfield/helper-text/index";

  import {
    upload_userpic,
    delete_userpic,
    upload_display_name,
    change_password,
    validate_password
  } from "utils.js";
  import { userProfile } from "stores.js";

  //display name
  let current_username = "";
  let current_display_name = "";
  let display_name = "";
  let display_name_is_valid = true;
  let display_name_err_text = "можно менять только регистр букв";
  let submit_display_btn_disabled = true;

  userProfile.subscribe(profile => {
    current_username = profile.username;
    current_display_name = profile.display_name || profile.username;
    display_name = current_display_name;
  });

  $: submit_display_btn_disabled = display_name == current_display_name;
  $: display_name_is_valid =
    display_name.toLowerCase() == current_username.toLowerCase();

  function reset_display_name() {
    display_name = current_username;
  }

  async function submit_display_name() {
    if (display_name_is_valid) {
      userProfile.update(value => {
        value.display_name = display_name;
        return value;
      });
      await upload_display_name(display_name);
    }
  }

  //change password
  let current_password = "";
  let new_password = "";
  let re_new_password = "";
  let passwords_are_valid = true;
  let passwords_err_text = "";

  $: reset_password_change_form(
    current_password,
    new_password,
    re_new_password
  );

  function reset_password_change_form() {
    passwords_are_valid = true;
    passwords_err_text = "";
  }

  function validate_passwords_form() {
    [passwords_are_valid, passwords_err_text] = validate_password(new_password);
    if (passwords_are_valid) {
      if (new_password != re_new_password) {
        passwords_are_valid = false;
        passwords_err_text = "Пароли не совпадают";
      }
    }
  }

  async function submit_password_change(e) {
    try {
      validate_passwords_form();
      if (passwords_are_valid) {
        await change_password(current_password, new_password, re_new_password);
        location.reload();
      }
    } catch (errResponse) {
      const jsonData = await errResponse.json();
      if (jsonData.current_password == "Invalid password.") {
        passwords_are_valid = false;
        passwords_err_text = "Неверный текущий пароль";
      }
    }
  }

  //profile pic
  let image_editor;
  let cropper;
  let uploaded_files = [];
  let img_input;
  let current_userpic;

  userProfile.subscribe(profile => {
    current_userpic = profile.userpic_url;
  });

  $: uploaded_files.length && !current_userpic
    ? bind_cropper()
    : destroy_cropper();

  function bind_cropper() {
    if (!cropper) {
      cropper = new Croppie(image_editor, {
        showZoomer: false,
        viewport: {
          width: 200,
          height: 200,
          type: "circle"
        }
      });
    }
    cropper.bind({
      url: current_userpic || URL.createObjectURL(uploaded_files[0])
    });
  }

  function destroy_cropper() {
    if (img_input) {
      img_input.value = ""; //todo WTF?
    }
  }

  async function _upload_userpic() {
    if (cropper) {
      const blob = await cropper.result({
        type: "blob",
        size: "viewport",
        format: "png"
      });
      upload_userpic(blob, "image/png");
      userProfile.update(value => {
        value.userpic_url = URL.createObjectURL(blob);
        return value;
      });
    }
  }
  function delete_image() {
    userProfile.update(value => {
      value.userpic_url = undefined;
      return value;
    });
    uploaded_files = [];
    delete_userpic();
  }
</script>

<style>
  #profile-tab {
    display: flex;
    justify-content: space-between;
  }

  #profile-col {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }

  #avatar-form {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    padding: 15px;
    border-radius: 15px;
    background-color: #e0e0e0;
  }

  #display-name-form {
    display: flex;
    flex-direction: column;
    padding: 15px;
    border-radius: 15px;
    background-color: #e0e0e0;
    margin-bottom: 30px;
  }

  #change-password-form {
    display: flex;
    flex-direction: column;
    padding: 15px;
    border-radius: 15px;
    background-color: #e0e0e0;
  }

  #image-editor {
    width: 300px;
    height: 300px;
    margin-bottom: 30px;
  }

  #cropper-placeholder {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #757575;
    color: #eeeeee;
    width: 300px;
    height: 300px;
    margin-bottom: 30px;
  }

  .separator {
    height: 1px;
    width: 100%;
    margin: 5px 0px;
  }
</style>

<svelte:head>
  <link rel="stylesheet" href="/static/css/croppie.min.css" />
</svelte:head>
<div id="profile-tab">
  <div id="profile-col">
    Смена отображаемого имени
    <form id="display-name-form" autocomplete="off">
      <Textfield
        type="text"
        label="Отображаемое имя"
        bind:value={display_name}
        invalid={!display_name_is_valid} />
      <HelperText validationMsg>{display_name_err_text}</HelperText>
      <div class="separator" />
      <div>
        <Button type="button" on:click={reset_display_name} variant="outlined">
          <Label>Cброс</Label>
        </Button>
        <Button
          type="button"
          on:click={submit_display_name}
          variant="raised"
          disabled={submit_display_btn_disabled}>
          <Label>Сохранить</Label>
        </Button>
      </div>
    </form>
    Смена пароля
    <form id="change-password-form" autocomplete="off">
      <input type="text" autocomplete="username" hidden />
      <Textfield
        type="password"
        label="Текущий пароль"
        bind:value={current_password}
        invalid={!passwords_are_valid}
        input$autocomplete="current-password" />
      <Textfield
        type="password"
        label="Новый пароль"
        bind:value={new_password}
        invalid={!passwords_are_valid}
        input$autocomplete="new-password" />
      <Textfield
        type="password"
        label="Подтверждения пароля"
        bind:value={re_new_password}
        invalid={!passwords_are_valid}
        input$autocomplete="new-password" />
      <HelperText validationMsg>{passwords_err_text}</HelperText>
      <div class="separator" />
      <Button type="button" on:click={submit_password_change} variant="raised">
        <Label>Сменить</Label>
      </Button>
    </form>
  </div>
  <div id="profile-col">
    Смена аватарки
    <div id="avatar-form">
      {#if current_userpic || !uploaded_files.length}
        <div id="cropper-placeholder">
          {#if current_userpic}
            <img src={current_userpic} alt="userpic" />
          {:else}Нет аватарки{/if}
        </div>
      {/if}
      <div
        bind:this={image_editor}
        id="image-editor"
        style="display:{uploaded_files.length && !current_userpic ? 'block' : 'none'}" />
      <input
        bind:this={img_input}
        type="file"
        accept="image/*"
        bind:files={uploaded_files}
        hidden />
      <div>
        {#if !(uploaded_files.length || current_userpic)}
          <Button
            type="button"
            on:click={() => img_input.click()}
            variant="outlined">
            <Label>Загрузить</Label>
          </Button>
        {/if}
        {#if uploaded_files.length || current_userpic}
          <Button
            type="button"
            on:click={delete_image}
            color="error"
            variant="raised">
            <Label>Удалить</Label>
          </Button>
        {/if}
        {#if uploaded_files.length}
          <Button type="button" on:click={_upload_userpic} variant="raised">
            <Label>Сохранить</Label>
          </Button>
        {/if}
      </div>
    </div>
  </div>
</div>
