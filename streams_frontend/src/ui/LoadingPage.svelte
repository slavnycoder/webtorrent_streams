<script>
  export let dark = false;
</script>

<style>
  .loading {
    display: flex;
    flex-grow: 1 !important;
    min-height: 40px;
    height: 100%;
    width: 100%;
  }

  .light {
    background: url(static/grid-light.svg) no-repeat center center;
    background-size: 40px;
  }

  .dark {
    background: url(static/grid-dark.svg) no-repeat center center;
    background-size: 40px;
  }
</style>

<div class="loading {dark ? 'dark' : 'light'}" />
