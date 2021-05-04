<script>
  export let drawerToggle;

  import { fade as fadeTransition } from "svelte/transition";

  import TopAppBar, {
    Row,
    Section,
    Title as AppBarTitle
  } from "@smui/top-app-bar";
  import IconButton from "@smui/icon-button";
  import Button, { Group, GroupItem, Label, Icon } from "@smui/button";
  import Dialog from "@smui/dialog";
  import Textfield, { Input, Textarea } from "@smui/textfield";
  import { Anchor } from "@smui/menu-surface";
  import Menu, { SelectionGroup, SelectionGroupIcon } from "@smui/menu";
  import List, { Item, Separator, Text, Graphic } from "@smui/list";

  import LoginDialog from "ui/auth_modals/LoginDialog.svelte";
  import SignUpDialog from "ui/auth_modals/SignUpDialog.svelte";
  import AccountDialog from "ui/account_modal/AccountDialog.svelte";

  import { host } from "constants.js";
  import { get_gravatar_link, logout, href } from "utils.js";
  import { userProfile } from "stores.js";

  let userMenuAnchor;
  let userMenu;
  const userMenuOpen = () => userMenu.setOpen(true);

  let loginDialog;
  const loginOpen = () => loginDialog.open();

  let registrationDialog;
  const registrationOpen = () => registrationDialog.open();

  let accountDialog;
  const accountOpen = () => accountDialog.open();
</script>

<style>
  .logo {
    cursor: pointer;
  }

  .logo:hover {
    color: red;
  }

  .auth-dialog {
    background-color: #e0e0e0;
  }

  .account-dialog {
    background-color: #e0e0e0;
  }

  #user-avatar {
    width: 2.5em;
    height: 2.5em;
    border-radius: 50%;
    margin-left: 10px;
  }

  .user-menu {
    background-color: #e0e0e0;
  }
</style>

<TopAppBar variant="static" color="primary" dense>
  <Row>
    <Section>
      <IconButton class="material-icons" on:click={drawerToggle}>
        menu
      </IconButton>
      <div class="logo" on:click={() => href('/')}>
        <AppBarTitle>KRINGE.TV</AppBarTitle>
      </div>
    </Section>
    <Section toolbar align="end" style="z-index: 999;">
      {#if !$userProfile.username}
        <Button on:click={loginOpen} color="secondary">
          <Label>Вход</Label>
        </Button>
        <Button on:click={registrationOpen} color="secondary">
          <Label>Регистрация</Label>
        </Button>
        <Dialog bind:this={loginDialog}>
          <div class="auth-dialog">
            <LoginDialog dialog={loginDialog} />
          </div>
        </Dialog>
        <Dialog bind:this={registrationDialog}>
          <div class="auth-dialog">
            <SignUpDialog dialog={registrationDialog} />
          </div>
        </Dialog>
      {:else}
        <div use:Anchor bind:this={userMenuAnchor}>
          <Button on:click={userMenuOpen} color="secondary">
            <Label>{$userProfile.username}</Label>
            <img
              id="user-avatar"
              src={$userProfile.userpic_url || get_gravatar_link($userProfile.username)}
              alt="" />
          </Button>
          <Dialog bind:this={accountDialog}>
            <div class="account-dialog" id="account-dialog">
              <AccountDialog dialog={accountDialog} />
            </div>
          </Dialog>
          <Menu
            bind:this={userMenu}
            bind:anchorElement={userMenuAnchor}
            anchorCorner="BOTTOM_START">
            <div class="user-menu">
              <List>
                <Item on:SMUI:action={accountOpen}>
                  <Graphic class="material-icons">account_circle</Graphic>
                  <Text>Аккаунт</Text>
                </Item>
                <Separator style="border-bottom-color: #000;" />
                <Item on:SMUI:action={logout}>
                  <Graphic class="material-icons">exit_to_app</Graphic>
                  <Text>Выход</Text>
                </Item>
              </List>
            </div>
          </Menu>
        </div>
      {/if}
    </Section>
  </Row>
</TopAppBar>
