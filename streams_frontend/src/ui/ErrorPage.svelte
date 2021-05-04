<script>
  export let error_status = 500;

  console.log(error_status);
</script>

<style>
  #error {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
  }
</style>

<div id="error">
  {#if error_status == 404}
    <h1>такого канала в помине не было</h1>
  {:else}
    <h1>что-то пошло не так</h1>
  {/if}
</div>
