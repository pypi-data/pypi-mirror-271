<template>
  <div>
    <p v-if="isLoading">Loading data...</p>
    <div v-else>
      <router-link to="/">Back to Blog</router-link>
      <post-item :post="post" :detail="true" @comment-posted="handleCommentPosted"></post-item>
    </div>
  </div>
</template>

<script lang="ts">
import config from '../config';
import { useRoute } from 'vue-router';
import PostItem from './PostItem.vue';
import { useDataStore } from '../stores/dataStore';
import { Post, PostsFromApi } from './types';
import { ref, onMounted } from 'vue';

export default {
  name: "PostDetail",
  components: {
    PostItem,
  },
  methods: {
    async handleCommentPosted() {
      console.log("handleCommentPosted in PostDetail");
      await this.fetchPostFromAPI(true);
    }
  },
  setup() {
    const route = useRoute();
    const dataStore = useDataStore();
    const wagtailApiUrl = new URL(config.postListUrl.toString()); // make a copy to not modify the original url

    const isLoading = ref(true);
    const post = ref({} as Post);
    const visibleDateStr = ref("");

    const fetchPostFromAPI = async (invalidateCache: boolean = false) => {
      const postSlug = route.params.slug as string;
      // FIXME maybe use clean detail url? But then we need to have
      // the page id instead of the slug and and either modify the API
      // to accept slugs or do a second request to get the page id. :/
      const postDetailUrl = new URL(wagtailApiUrl.href);
      let pageType = config.pageType;
      if (postSlug in dataStore.slugToPost) {
        // FIXME we could also just use the post detail url?
        pageType = dataStore.slugToPost[postSlug].meta.type;
      }
      postDetailUrl.searchParams.set("type", pageType);
      postDetailUrl.searchParams.set("slug", postSlug);
      postDetailUrl.searchParams.set("fields", "html_detail,comments,comments_security_data,comments_are_enabled,podlove_players");

      try {
        const posts = await dataStore.fetchJson(postDetailUrl, invalidateCache) as unknown as PostsFromApi;
        post.value = posts.items[0];
      } catch (error) {
        console.error('Error fetching data from API: ', error);
      } finally {
        isLoading.value = false;
      }
    }

    onMounted(fetchPostFromAPI);
    return { dataStore, isLoading, post, visibleDate: visibleDateStr, fetchPostFromAPI };
  },
}
</script>
