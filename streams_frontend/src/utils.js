import md5 from "md5";
import { https_host } from "host.js";
import { channelList, userProfile, UserProfile } from "stores.js";

// basic methods
function setToken(token) {
  localStorage.setItem('auth_token', token);
}

export function getToken() {
  const token = localStorage.getItem('auth_token');
  return token ? "Token " + token : undefined;
}

function handleErrors(response) {
  if (!response.ok) {
    if (response.status == 401) {
      userProfile.set({});
      localStorage.removeItem("auth_token");
      localStorage.removeItem("ws_token");
      location.reload();
    }
    throw response;
  }
  return response;
}

async function _get(endpoint, headers) {
  const token = getToken();
  const response = await fetch((https_host + endpoint), {
    method: 'GET',
    headers: {
      Authorization: token,
      ...headers,
    }
  });
  handleErrors(response);
  return response;
}

async function _post(endpoint, data, headers) {
  const token = getToken();
  const response = await fetch((https_host + endpoint), {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
      Authorization: token,
      ...headers,
    }
  });
  handleErrors(response);
  return response;
}

async function _patch(endpoint, data, headers) {
  const token = getToken();
  const response = await fetch((https_host + endpoint), {
    method: 'PATCH',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json',
      Authorization: token,
      ...headers,
    }
  });
  handleErrors(response);
  return response;
}

async function _upload_file(endpoint, body, headers, content_type) {
  const token = getToken();
  const response = await fetch((https_host + endpoint), {
    method: 'POST',
    body,
    headers: {
      'Content-Type': content_type,
      Authorization: token,
      ...headers,
    }
  });
  handleErrors(response);
  return response;
}

async function _delete(endpoint, headers) {
  const token = getToken();
  const response = await fetch((https_host + endpoint), {
    method: 'DELETE',
    headers: {
      Authorization: token,
      ...headers,
    }
  });
  handleErrors(response);
  return response;
}

export function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// api methods
export async function signUp(username, password, email, captcha) {
  const response = await _post("api/users/", {
    username,
    password,
    email,
    captcha
  });
  const profile_data = await response.json();
  localStorage.setItem("auth_token", profile_data.token);
  location.reload();
}

export async function login(username, password, captcha) {
  localStorage.removeItem("auth_token");
  localStorage.removeItem("ws_token");
  const response = await _post("api/auth/login/", {
    username,
    password,
    captcha
  });
  let jsonData = await response.json();
  setToken(jsonData.token);
  localStorage.setItem("ws_token", jsonData.user.ws_token);
  location.reload();
}

export async function auth() {
  const token = getToken();
  if (token) {
    try {
      const response = await _get("api/users/me/");
      const profile = await response.json();
      userProfile.set(new UserProfile(profile.username, profile.userpic_url, profile.display_name, profile.is_active));
    } catch (_) { }
  } else {
    userProfile.set({});
  }
}

export async function logout() {
  try {
    await _post("api/auth/logout/");
  } catch (_) { }
  localStorage.removeItem("auth_token");
  localStorage.removeItem("ws_token");
  userProfile.set({});
  location.reload();
}

export async function get_settings() {
  const settings_response = await _get("api/settings/");
  const settings = await settings_response.json();
  localStorage.setItem("ws_token", settings.ws_token);
  const emoticons_response = await fetch("https://storage.googleapis.com/streams/static/emoticons.json");
  const emoticons_data = await emoticons_response.text();
  localStorage.setItem("emoticons", emoticons_data);
}

export async function get_channels() {
  const response = await _get("api/channels/");
  channelList.set(await response.json());
}

export async function get_online_channels(page) {
  const response = await _get(`api/channels/online/?page=${page}`);
  return await response.json();
}

export async function get_stream(username) {
  const response = await _get(`api/channels/${username}/`);
  return await response.json();
}

export async function follow_channel(channel, to_follow) {
  return await _post(`api/channels/${channel}/follow/`, { to_follow });
}

export async function send_chat_msg(channel_username, text) {
  const response = await _post(`api/channels/${channel_username}/post_message/`, { text });
  return response;
}

export async function upload_userpic(body, content_type) {
  const response = await _upload_file("api/users/userpic/", body, { "Content-Disposition": "attachment; filename=userpic.png" }, content_type);
  return response;
}

export async function delete_userpic() {
  const response = await _delete("api/users/userpic/");
  return response;
}

export async function upload_display_name(display_name) {
  const response = await _post("api/users/display_name/", { display_name });
  return response;
}

export async function change_password(current_password, new_password, re_new_password) {
  const response = await _post("api/users/set_password/", { current_password, new_password, re_new_password });
  return response;
}

export async function get_stream_settings() {
  const response = await _get("api/users/stream_settings/");
  return response;
}

export async function update_stream_description(stream_description) {
  const response = await _post("api/users/stream_description/", { stream_description });
  return response;
}

export async function reset_stream_key() {
  const response = await _post("api/users/reset_stream_key/");
  return response;
}

export async function reset_password(email) {
  const response = await _post("api/users/reset_password/", { email });
  return response;
}

export async function set_new_password(uid, token, new_password) {
  const response = await _post("api/users/reset_password_confirm/", { uid, token, new_password });
  return response;
}

export async function confirm_email(uid, token) {
  const response = await _post("api/users/activation/", { uid, token });
  return response;
}

//channel panels
export async function create_new_panel() {
  const response = await _post("api/channel-panels/");
  return response;
}

export async function delete_panel(id) {
  const response = await _delete(`api/channel-panels/${id}/`);
  return response;
}

export async function set_panel_image(id, image) {
  let response;
  if (image) {
    response = await _upload_file(`api/channel-panels/${id}/image/`, image, { "Content-Disposition": "attachment; filename=panel_image.png" }, "image/png");
  } else {
    response = await _delete(`api/channel-panels/${id}/image/`);
  }
  return response;
}

export async function update_panel(data) {
  const response = await _patch(`api/channel-panels/${data.id}/`, data);
  return response;
}

// validation
export function validate_username(username) {
  if (username.length < 5) return [false, "не меньше 5 символов"]
  if (username.length > 16) return [false, "не больше 16 символов"]
  if (!username.match(/^[a-z0-9_]+$/)) return [false, "только [a-z, 0-9] и '_'"]
  if (username.match(/(_)\1/)) return [false, "не больше одного '_' подряд"]
  return [true, ''];
}

export function validate_password(password) {
  if (password.length < 7) return [false, "минимум 8 символов"];
  if (password.length > 127) return [false, "максимум 127 символов"];
  return [true, ''];
}

const emailRegexp = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
export function validate_email(email) {
  if (!email.match(emailRegexp)) return [false, 'вcратый email']
  return [true, ''];
}


// misc
export function href(path) {
  location.href = path;
}

export function strToRGB(my_string) {
  let hash = 0;
  for (let i = 0; i < my_string.length; i++) {
    hash = my_string.charCodeAt(i) + ((hash << 5) - hash);
  }
  let c = (hash & 0x00FFFFFF)
    .toString(16)
    .toUpperCase();

  return "00000".substring(0, 6 - c.length) + c;
}

export function kFormatter(num) {
  return Math.abs(num) > 999
    ? `${Math.sign(num) * (Math.abs(num) / 1000).toFixed(1)}k`
    : Math.sign(num) * Math.abs(num);
}

export function get_gravatar_link(name) {
  return `https://www.gravatar.com/avatar/${md5(name)}?s=50&d=identicon`;
}

export function is_key(e, keyCode, no_prevent) {
  const is_key = e.which == keyCode || e.keyCode == keyCode;
  if (is_key && !no_prevent) {
    e.preventDefault();
  }
  return is_key;
} 
