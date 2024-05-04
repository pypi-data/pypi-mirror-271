<template>
    <form @submit.prevent="submitForm">
      <p>
        <label for="id_search">Search:</label>
        <input v-model="form.search" id="id_search" />
      </p>
      <p>
        <label>Date:</label>
        <input type="date" v-model="form.date_after" placeholder="YYYY/MM/DD" id="id_date_0">
        -
        <input type="date" v-model="form.date_before" placeholder="YYYY/MM/DD" id="id_date_1">
      </p>
      <p>
        <label for="id_date_facets">Date Facets:</label>
        <input v-model="form.date_facets" id="id_date_facets" />
        <div class="cast-date-facet-container" id="id_date_facets">
          <div class="cast-date-facet-item">
            <a class="selected" href="#" @click.prevent="selectFacet('date_facets', '')">All</a>
          </div>
          <div v-for="facet in facetCounts.date_facets" :key="facet.slug" class="cast-date-facet-item">
            <a href="#" @click.prevent="selectFacet('date_facets', facet.slug)">{{ facet.name }} ({{ facet.count }})</a>
          </div>
        </div>
      </p>
      <p>
        <label for="id_category_facets">Category Facets:</label>
        <input v-model="form.category_facets" id="id_category_facets" />
        <div class="cast-category-facet-container" id="id_category_facets">
          <div class="cast-date-facet-item">
            <a class="selected" href="#" @click.prevent="selectFacet('category_facets', '')">All</a>
          </div>
          <div v-for="facet in facetCounts.category_facets" :key="facet.slug" class="cast-date-facet-item">
            <a href="#" @click.prevent="selectFacet('category_facets', facet.slug)">{{ facet.name }} ({{ facet.count }})</a>
          </div>
        </div>
      </p>
      <p>
        <label for="id_tag_facets">Tag Facets:</label>
        <input v-model="form.tag_facets" id="id_tag_facets" />
        <div class="cast-tag-facet-container" id="id_tag_facets">
          <div class="cast-date-facet-item">
            <a class="selected" href="#" @click.prevent="selectFacet('tag_facets', '')">All</a>
          </div>
          <div v-for="facet in facetCounts.tag_facets" :key="facet.slug" class="cast-date-facet-item">
            <a href="#" @click.prevent="selectFacet('tag_facets', facet.slug)">{{ facet.name }} ({{ facet.count }})</a>
          </div>
        </div>
      </p>
      <p>
        <label for="id_o">Ordering:</label>
        <select v-model="form.order" name="order" id="id_o">
          <option value="">---------</option>
          <option value="visible_date">Date</option>
          <option value="-visible_date">Date (descending)</option>
        </select>
      </p>
      <button type="submit">Filter</button>
    </form>
  </template>

  <script lang="ts">
  import { ref, watchEffect } from 'vue';
  import { Form, FacetCounts } from './types';


  export default {
    props: {
      form: {
        type: Object as () => Form,
        default: () => ({}),
      },
      facetCounts: {
        type: Object as () => FacetCounts,
        default: () => ({}),
      },
    },
    setup(props, context) {
      const form = ref<Form>(props.form);

      watchEffect(() => {
        // Update the ref whenever the prop changes
        form.value = props.form;
      });

      const submitForm = () => {
        // handle form submission here
        console.log("form value: ", form.value);
        context.emit("submitFilterForm", form.value);
      };

      type FacetType = 'date_facets' | 'category_facets' | 'tag_facets';
      const selectFacet = (type: FacetType, value: string) => {
        form.value[type] = value;
        console.log(`select ${type} - form value: `, form.value);
        context.emit("submitFilterForm", form.value);
      };

      return { form, submitForm, selectFacet };
    },
    emits: ["submitFilterForm"],
  };
  </script>
