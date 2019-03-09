<template>
  <v-tooltip bottom>
    <v-btn slot="activator" @click="refresh" :loading="loading" icon
      ><v-icon>mdi-database-refresh</v-icon></v-btn
    >
    <span>Refresh datasets</span>
  </v-tooltip>
</template>

<script>
import store from "../../store.js";

export default {
  data() {
    return {
      loading: false
    };
  },
  methods: {
    async refresh() {
      try {
        this.loading = true;
        const response = await this.$http.get("/api/v1/datasets");
        store.setAllDatasets(response.data.map(item => item.name));
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
