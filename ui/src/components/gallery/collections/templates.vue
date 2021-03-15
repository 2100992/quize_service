<template>
  <div class="container-fluid">
    <b-container fluid class="p-4 bg-dark" v-if="pictures.length">
      <b-row>
        <b-col v-for="picture in pictures" :key="picture.name" cols="3">
          <b-img thumbnail fluid :src="picture.url" :alt="picture.name"></b-img>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script src="./index.js"></script>
<style lang="scss" scoped>
@import './styles.css';
</style>
