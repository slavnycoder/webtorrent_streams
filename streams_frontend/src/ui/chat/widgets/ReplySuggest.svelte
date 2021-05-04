<script>
  export let filtered_usernames;
  export let selected_user;
  export let submit_user_suggestion;
</script>

<style>
  .suggested-user {
    cursor: pointer;
    background-color: #111;
    padding: 5px;
    color: #757575;
  }

  .suggested-user.selected {
    color: #e0e0e0;
    background-color: #333;
  }
</style>

{#each filtered_usernames as user, i}
  <div
    class="suggested-user {i == selected_user ? 'selected' : ''}"
    on:mouseover={() => {
      selected_user = i;
    }}
    on:mousedown={submit_user_suggestion}>
    {`@${user}`}
  </div>
{/each}
