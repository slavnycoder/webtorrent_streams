<script>
  import { onMount } from "svelte";

  import TabBar from "@smui/tab-bar";
  import Tab, { Icon, Label } from "@smui/tab";
  import Dialog, { Title as DialogTitle, Content } from "@smui/dialog";

  import ProfileTab from "./tabs/ProfileTab.svelte";
  import ChannelTab from "./tabs/ChannelTab.svelte";

  const tab_names = {
    profile: "Профиль",
    channel: "Канал"
  };
  let active_tab = "profile";

  onMount(() => {
    // TODO rm hack
    document.getElementById("account-dialog").parentNode.style["max-width"] =
      "none";
  });
</script>

<style>
  #account-dialog-wrap {
    width: 800px;
    height: 700px;
    background-color: #fff;
  }
</style>

<div id="account-dialog-wrap">
  <DialogTitle>Аккаунт</DialogTitle>
  <TabBar tabs={['profile', 'channel']} let:tab bind:active={active_tab}>
    <Tab {tab}>
      <Label>{tab_names[tab]}</Label>
    </Tab>
  </TabBar>
  <Content>
    {#if active_tab == 'profile'}
      <ProfileTab />
    {:else}
      <ChannelTab />
    {/if}
  </Content>
</div>
