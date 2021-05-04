<script>
  export let files;

  import Dialog, {
    Title as DialogTitle,
    Content as DialogContent,
    Actions as DialogActions
  } from "@smui/dialog";
  import Button, { Label, Icon } from "@smui/button";

  $: img_src = files.length ? URL.createObjectURL(files[0]) : "";
</script>

<style>
  .img-dialog-wrap {
    background-color: #eeeeee;
  }

  .img-wrap {
    display: flex;
    flex-direction: column;
  }
</style>

<div class="img-dialog-wrap">
  <DialogTitle>Изображение панели</DialogTitle>
  <DialogContent>
    <div class="img-wrap">
      {#if files.length}
        <img src={img_src} alt="panel image" width="350px" />
      {/if}
    </div>
  </DialogContent>
  <DialogActions>
    <Button variant="outlined" action="cancel">
      <Label>Отмена</Label>
    </Button>
    <Button variant="raised" action="submit">
      <Label>Ок</Label>
    </Button>
  </DialogActions>
</div>
