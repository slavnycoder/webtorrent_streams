import { writable } from 'svelte/store';

export class UserProfile {
    constructor(username, userpic_url, display_name, is_active) {
        this.username = username;
        this.userpic_url = userpic_url;
        this.display_name = display_name;
        this.is_active = is_active;
    }
}

const createUserStore = () => {
    const { set, subscribe, update } = writable({});
    return {
        subscribe,
        set,
        update,
        useLocalStorage: () => {
            try {
                const json = localStorage.getItem('profile');
                set(JSON.parse(json) || {});
            } catch {
                set({});
            }
            subscribe(current => {
                localStorage.setItem('profile', JSON.stringify(current));
            });
        }
    };
}

export const drawerOpen = writable(false);
export const centrifuge_cli = writable(undefined);
export const channelList = writable({ followed: [], online: [] });
export const userProfile = createUserStore();
