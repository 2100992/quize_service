<template>
  <b-comptainer>
    <b-row>
      <b-col cols="2">
        <Nav />
      </b-col>
      <b-col>
        <Collections :apiURL="apiURL" />
        <Pictures />
      </b-col>
    </b-row>
  </b-comptainer>
</template>

<script>
// @ is an alias to /src
import Collections from '@/components/gallery/collections/templates.vue';
import Pictures from '@/components/gallery/pictures/templates.vue';
import Nav from '@/components/gallery/nav/templates.vue';

// const apiURL = 'http://localhost:5000/api/v1/gallery/';

export default {
  props: [],
  data() {
    return {
      apiURL: 'http://localhost:5000/api/v1/gallery/collections/cats-210304232910/',
    };
  },
  components: {
    Collections,
    Pictures,
    Nav,
  },
};
</script>
