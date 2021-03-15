<template>
  <div class="container">
    <p :title="message">Experiments</p>
    <p>{{ message }}</p>
  </div>
</template>

<script>
export default {
  name: 'Experiments',
  setup() {},
  data() {
    return {
      message: 'title',
    };
  },
};
</script>
