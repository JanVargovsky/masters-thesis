<template>
  <v-layout row wrap>
    <v-flex xs12>
      <v-layout row wrap>
        <v-text-field
          v-model="search"
          label="Search"
          single-line
          hide-details
          clearable
          prepend-icon="mdi-magnify"
        />
        <v-btn color="primary" class="mb-0" @click="refresh" :loading="loading">Refresh</v-btn>
      </v-layout>
    </v-flex>
    <v-flex xs12>
      <v-data-table
        :headers="headers"
        :items="datasets"
        :search="search"
        :loading="loading"
        :pagination.sync="pagination"
        :rows-per-page-items="[10, 25, 50, 100]"
      >
        <v-progress-linear slot="progress" color="blue" indeterminate></v-progress-linear>

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
              <v-btn
                slot="activator"
                fab
                icon
                small
                class="ma-0"
                :to="'/datasets/'+props.item.name"
              >
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
            <v-tooltip top>
              <v-btn
                slot="activator"
                fab
                icon
                small
                class="ma-0"
                @click="deleteDataset(props.item.name)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
              <span>Delete</span>
            </v-tooltip>
          </td>
        </template>

        <template slot="no-data">
          <v-alert :value="true && !loading" color="error" icon="mdi-alert">No data available.</v-alert>
        </template>
      </v-data-table>
    </v-flex>
  </v-layout>
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
      if (value === "excel") return "mdi-file-excel";
      if (value === "text") return "mdi-file-document";
      return "mdi-file";
    }
  },
  methods: {
    async refresh() {
      try {
        this.loading = true;
        this.datasets = [];
        const response = await this.$http.get("/api/v1/datasets");
        response.data.forEach(item => {
          item.createdAt = new Date(item.createdAt);
          item.lastModifiedAt = new Date(item.lastModifiedAt);
        });
        this.datasets = response.data;
      } catch (error) {
        this.error = true;
      }
      this.loading = false;
    },
    async deleteDataset(dataset) {
      if (confirm(`Are you sure you want to delete ${name}?`)) {
        try {
          const response = await this.$http.delete(
            `/api/v1/dataset/${dataset}`
          );
          this.datasets = this.datasets.filter(t => t.name !== dataset);
        } catch (error) {
          this.error = true;
        }
      }
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
