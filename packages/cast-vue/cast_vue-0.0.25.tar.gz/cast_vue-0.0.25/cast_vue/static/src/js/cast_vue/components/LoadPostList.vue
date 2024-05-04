<template>
    <div>
        <p v-if="isLoading">Loading data...</p>
        <div v-else>
            <select-theme></select-theme>
            <filter-form
                @submit-filter-form="handleSubmitFilterForm"
                :form="form"
                :facetCounts="facetCounts"
            ></filter-form>
            <br />
            <pagination-buttons :currentPage="currentPage" :totalPages="totalPages" @change-page="changePage">
            </pagination-buttons>
            <post-list :blog="blog" :posts="postsFromApi" />
        </div>
    </div>
</template>

<script lang="ts">
import config from '../config';
import { FacetCounts, PostsFromApi } from './types';
import { ref, onMounted, computed, Ref } from 'vue';
import { LocationQueryRaw, useRoute, useRouter } from 'vue-router';
import FilterForm from './FilterForm.vue';
import PostList from './PostList.vue';
import PaginationButtons from './PaginationButtons.vue';
import SelectTheme from './SelectTheme.vue';
import { useDataStore } from '../stores/dataStore';
import { setUrlSearchParams, getUrlSearchParams } from '../helpers/url';
import { Form } from './types';


export default {
    components: {
        FilterForm,
        PostList,
        PaginationButtons,
        SelectTheme,
    },
    setup() {
        const route = useRoute();
        const router = useRouter();
        const isLoading = ref(true);
        const blog = ref({});
        const postsFromApi = ref({} as PostsFromApi);
        const facetCounts = ref({} as FacetCounts);
        const form = ref(getUrlSearchParams(route.query)) as unknown as Ref<Form>;
        const currentPage = ref(isNaN(Number(form.value.page)) ? 1 : Number(form.value.page));  // maybe page was already set in url
        const itemsPerPage = config.paginationPageSize;

        const updateSearchParams = (wagtailApiUrl: URL, data: any) => {
            const { page: _, ...params } = data;  // remove page from params
            setUrlSearchParams(wagtailApiUrl, params);
        };

        const calculateFirstOffset = (data: any) => {
            const { page: _, ...rest } = data;
            const params = { ...rest, offset: "0" };
            if (data.page) {
                params["offset"] = ((Number(data.page) - 1) * itemsPerPage).toString();
            }
            return params;
        };

        // init pages api url
        const wagtailApiUrl = new URL(config.postListUrl.toString()); // make a copy to not modify the original url
        wagtailApiUrl.searchParams.set("type", "cast.Post");
        wagtailApiUrl.searchParams.set("fields", "html_overview,html_detail,visible_date,podlove_players");
        wagtailApiUrl.searchParams.set("offset", "0");
        wagtailApiUrl.searchParams.set("limit", itemsPerPage.toString());
        wagtailApiUrl.searchParams.set("order", "-visible_date");
        wagtailApiUrl.searchParams.set("use_post_filter", "true");
        updateSearchParams(wagtailApiUrl, calculateFirstOffset(form.value));

        // init blog facet counts api url
        const facetCountsApiUrl = config.apiFacetCountsUrl;
        updateSearchParams(facetCountsApiUrl, calculateFirstOffset(form.value));

        const fetchData = async () => {
            try {
                const dataStore = useDataStore();
                blog.value = await dataStore.fetchJson(config.blogDetailUrl);
                const facetResult = await dataStore.fetchJson(facetCountsApiUrl);
                facetCounts.value = facetResult.facet_counts as FacetCounts;
                const posts = await dataStore.fetchJson(wagtailApiUrl) as unknown as PostsFromApi;
                dataStore.setSlugToId(posts);
                postsFromApi.value = posts;
            } catch (error) {
                console.error('Error fetching blog data from API: ', error);
            } finally {
                isLoading.value = false;
            }
        };

        const handleSubmitFilterForm = async (data: Form) => {
            currentPage.value = 1;
            updateSearchParams(wagtailApiUrl, data);
            updateSearchParams(facetCountsApiUrl, data);
            await fetchData();
            router.push({ query: data as unknown as LocationQueryRaw});
        };

        const changePage = async (delta: number) => {
            currentPage.value += delta;
            wagtailApiUrl.searchParams.set("offset", ((currentPage.value - 1) * itemsPerPage).toString());
            router.push({ query: { ...route.query, page: currentPage.value } });
            await fetchData();
        };

        const totalPages = computed(() => {
            return Math.ceil(postsFromApi.value.meta.total_count / itemsPerPage);
        });

        onMounted(fetchData);

        return {
            isLoading,
            currentPage,
            totalPages,
            blog,
            postsFromApi,
            facetCounts,
            form,
            handleSubmitFilterForm,
            changePage
        };
    }
};
</script>
