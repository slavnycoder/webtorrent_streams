import { cubicOut } from "svelte/easing";
import { tweened } from "svelte/motion";

export const host = "API_HOST";

export const arrow_right = "/static/icons/arrow_right.svg";
export const arrow_left = "/static/icons/arrow_left.svg";
export const navbar_height = 48;

export const collapsed_chat_width = 0;
export const expanded_chat_width = 400;
export const chat_toogle_duration = 400;

export const chat_width = tweened(
  expanded_chat_width,
  {
    duration: chat_toogle_duration,
    easing: cubicOut
  }
);
