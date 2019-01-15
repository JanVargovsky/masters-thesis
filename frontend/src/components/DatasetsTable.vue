<template>
  <v-card>
    <v-card-title>
      <v-icon large>mdi-database</v-icon>Datasets
      <v-spacer/>
      <v-text-field v-model="search" label="Search" single-line hide-details clearable/>
      <v-btn color="primary" class="mb-0" @click="refresh" :loading="loading">Refresh</v-btn>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="datasets"
      :search="search"
      :loading="loading"
      :pagination.sync="pagination"
      :rows-per-page-items="[10, 25, 50, 100]"
    >
      <v-progress-linear slot="progress" color="blue" indeterminate></v-progress-linear>

      <!-- TODO add basic info about dataset https://vuetifyjs.com/en/components/data-tables#example-expand -->
      <template slot="items" slot-scope="props">
        <td class="shrink">
          <v-tooltip top>
            <v-icon slot="activator">{{props.item.type | typeToIcon}}</v-icon>
            <span>{{props.item.type}}</span>
          </v-tooltip>
        </td>
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.size | formatSize }}</td>
        <td>{{ props.item.createdAt.toLocaleString() }}</td>
        <td>{{ props.item.lastModifiedAt.toLocaleString() }}</td>
        <td class="shrink">
          <v-tooltip top>
            <v-btn slot="activator" fab icon small class="ma-0" :to="'/dataset/'+props.item.name">
              <v-icon>mdi-file-find</v-icon>
            </v-btn>
            <span>Open</span>
          </v-tooltip>
          <v-tooltip top>
            <v-btn slot="activator" fab icon small class="ma-0">
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <span>Edit</span>
          </v-tooltip>
        </td>
      </template>

      <template slot="no-data">
        <v-alert :value="true && !loading" color="error" icon="mdi-alert">No data available.</v-alert>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      search: "",
      loading: false,
      pagination: {
        descending: false,
        // page: 1,
        // rowsPerPage: 10,
        sortBy: "name"
        // totalItems: 0
      },
      headers: [
        { text: "Type", value: "type" },
        { text: "Name", value: "name" },
        { text: "Size", value: "size" },
        { text: "Created at", value: "createdAt" },
        { text: "Last modified at", value: "lastModifiedAt" },
        { text: "Actions", value: "actions", sortable: false }
      ],
      datasets: []
    };
  },
  async created() {
    await this.refresh();
  },
  filters: {
    formatSize: function(value) {
      if (!value) value = 0;
      let unit = "B";
      if (value >= 1000) {
        value = Math.floor(value / 1000);
        unit = "kB";
      }
      if (value >= 1000) {
        value = Math.floor(value / 1000);
        unit = "MB";
      }
      return `${value} ${unit}`;
    },
    typeToIcon: function(value) {
      if (value === "csv") return "mdi-file-delimited";
      if (value === "txt") return "mdi-file-document";
      return "mdi-file";
    }
  },
  methods: {
    async refresh() {
      try {
        this.loading = true;
        this.datasets = [];
        var response = await this.$http.get("/api/v1/datasets");
        response.data.forEach(item => {
          item.createdAt = new Date(item.createdAt);
          item.lastModifiedAt = new Date(item.lastModifiedAt);
        });
        this.datasets = response.data;
      } catch (error) {}
      this.loading = false;
    }
  }
};
</script>

<style>
td.shrink {
  width: 0.1%;
  white-space: nowrap;
}
</style>