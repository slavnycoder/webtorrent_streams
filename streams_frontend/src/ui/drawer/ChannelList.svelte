<script>
  import List, {
    Group,
    Item,
    Graphic,
    Meta,
    Label,
    Separator,
    Subheader,
    Text,
    PrimaryText,
    SecondaryText
  } from "@smui/list";
  import Button, {
    Group as BtnGroup,
    Label as BtnLabel,
    Icon
  } from "@smui/button";

  import ChannelItem from "ChannelItem.svelte";
  import { channelList } from "stores.js";
  import { get_channels } from "utils.js";

  const sections = ["followed", "online", "top"];
  const section_names = {
    followed: "Отслеживаемые",
    online: "Сейчас онлайн",
    top: "Топ стримеры"
  };
</script>

<style>
  .section-name {
    text-transform: uppercase;
    padding-left: 10px;
  }
</style>

<List avatarList dense>
  {#each sections as section}
    {#if $channelList[section] && $channelList[section].length}
      <span class="section-name">{section_names[section] || section}</span>
      {#each $channelList[section] as channel}
        <ChannelItem {channel} />
      {/each}
    {/if}
  {/each}
</List>
