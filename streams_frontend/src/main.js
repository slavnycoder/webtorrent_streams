import App from './App.svelte';
import { userProfile } from "stores.js";

userProfile.useLocalStorage();

if ("serviceWorker" in navigator) {
	navigator.serviceWorker.register('./sw.js').catch((error) => console.log('Service worker registration failed:', error));
} else {
	console.log("No SW");
}

const app = new App({
	target: document.body,
});

export default app;
