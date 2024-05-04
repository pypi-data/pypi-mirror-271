<template>
    <div>
      <h1>Choose a Theme</h1>
      <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
      <select v-model="selectedTheme" @change="updateTheme">
        <option v-for="theme in themes" :key="theme.slug" :value="theme.slug">
          {{ theme.name }}
        </option>
      </select>
    </div>
  </template>

  <script lang="ts">
  import config from '../config';
  import { useDataStore } from '../stores/dataStore';
  import { Theme } from './types';
  export default {
    data(): { selectedTheme: string; themes: Theme[], errorMessage: string } {
      return {
        selectedTheme: "",
        themes: [],
        errorMessage: "",
      };
    },
    async mounted() {
        // Fetching the list of themes from the API
        const dataStore = useDataStore();
        const themeList = await dataStore.fetchJson(config.apiThemeListUrl);
        this.themes = themeList.items as Theme[];
        const selectedTheme = this.themes.find((theme) => theme.selected);
        if (selectedTheme) {
          this.selectedTheme = selectedTheme.slug;
        }
    },
    methods: {
      async updateTheme() {
        const response = await fetch(config.apiThemeUpdateUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": config.csrfToken,
          },
          body: JSON.stringify({ theme_slug: this.selectedTheme }),
        });

        if (response.ok) {
          // Reload the page to see the new theme
          window.location.reload();
        } else {
          console.log("theme error response: ", response);
          const result = await response.json();
          console.log("theme error result: ", result);
          this.errorMessage = `An error occurred: ${result.error}`;
        }
      },
    },
  };
  </script>
