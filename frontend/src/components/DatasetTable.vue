<template>
  <v-card>
    <v-alert :value="error" type="error" transition="scale-transition">Server error.</v-alert>
    <v-card-title>
      <v-icon large>mdi-database</v-icon>
      {{ dataset }}
      <v-spacer/>
      <v-text-field v-model="search" label="Search" single-line hide-details clearable/>
    </v-card-title>

    <v-data-table :headers="headers" :items="rows" :search="search" :loading="loading">
      <v-progress-linear slot="progress" color="blue" indeterminate></v-progress-linear>

      <template slot="items" slot-scope="props">
        <td class="shrink">{{ props.item.id }}</td>
        <td
          v-for="(item, index) in props.item.values"
          :key="String(props.item.id) + String(index) + String(item)"
        >{{ item }}</td>
      </template>

      <template slot="no-data">
        <v-alert :value="true && !loading" color="error" icon="mdi-alert">No data available.</v-alert>
      </template>
    </v-data-table>
  </v-card>
</template>
 
<script>
export default {
  props: {
    dataset: String
  },
  data() {
    return {
      columns: [],
      rows: [],
      search: "",
      loading: false,
      error: false
    };
  },
  async created() {
    await this.initialize();
  },
  computed: {
    headers: function() {
      return [
        {
          text: "Row",
          value: "id",
          sortable: false
        },
        ...this.columns.map((value, index) => ({
          text: value,
          value: `values.${index}`,
          sortable: false
        }))
      ];
    }
  },
  watch: {
    dataset: async function() {
      await this.initialize();
    }
  },
  methods: {
    async initialize() {
      try {
        this.loading = true;
        this.data = [];
        var response = await this.$http.get(`/api/v1/dataset/${this.dataset}`);
        const data = response.data;
        this.columns = data.columns;
        this.rows = data.rows.map((value, index) => ({
          id: index,
          values: value
        }));
      } catch (error) {
        this.error = true;
      }
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
