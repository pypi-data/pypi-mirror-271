import { PostsFromApi, Post } from './../components/types';
import { defineStore } from 'pinia';

// Define the store type
interface DataStoreState {
  jsonCache: Record<string, any>;
  slugToPost: Record<string, Post>;
}

// Define and export the store
export const useDataStore = defineStore({
  id: "main",
  state: (): DataStoreState => ({
    jsonCache: {},
    slugToPost: {},
  }),
  actions: {
    async fetchJson(url: URL, invalidateCache: boolean = false): Promise<Record<string, unknown>> {
      // Check if the URL is in the cache.
      const urlStr = url.toString();
      // console.log("fetchJson: ", urlStr)
      if (this.jsonCache[urlStr] && !invalidateCache) {
        return this.jsonCache[urlStr];
      }

      // Fetch the JSON if it's not in the cache.
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        // Store the result in the cache.
        this.jsonCache[urlStr] = data;
        return data;
      } catch (error) {
        console.error("Failed to fetch JSON", error);
        throw error;
      }
    },
    setSlugToId(posts: PostsFromApi) {
      for (const post of posts.items) {
        this.slugToPost[post.meta.slug] = post;
      }
    }
  },
});
