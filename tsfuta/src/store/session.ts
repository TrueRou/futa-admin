import { defineStore } from 'pinia';
import axios from 'axios';
import type { Page } from '@/types';

export const useSession = defineStore('session', {
    state: () => ({
        pages: [] as Page[],
    }),

    actions: {
        async ensurePages() {
            // Ensure that the pages are loaded, we don't consider pages updated.
            if (this.pages.length === 0) {
                const responses = await axios.get(`/pages`)
                this.pages = responses.data
            }
        }
    },
});