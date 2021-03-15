import axios from 'axios';

export default {
  name: 'Collections',
  props: {
    apiURL: String,
  },
  data() {
    return {
      collections: [],
      collection: {},
      pics: true,
      pictures: [],
      meta: {},
      links: {},
    };
  },
  methods: {
    getData(URL) {
      axios.get(URL).then((response) => {
        this.collections = response.data.collections;
        this.collection = response.data.collection;
        this.pictures = response.data.pictures;
        // this.pictures.push(response.data.pictures);
        this.meta = response.data.meta;
        this.links = response.data.links;
      });
    },
  },

  created() {
    this.getData(this.apiURL);
  },
  setup() {},
};
