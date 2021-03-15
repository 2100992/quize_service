<template>
  <div>
    <p>{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios';

const dataURL = 'http://localhost:5000/api/v1/gallery/collections/animals-210304232837';

export default {
  name: 'Fetch',
  data() {
    return {
      pictures: [],
    };
  },
  methods: {
    getPictures() {
      axios.get(dataURL).then((response) => {
        this.pictures = response.data.pictures;
      });
    },
  },
  created() {
    this.getPictures();
  },
  setup() {},
};
</script>
