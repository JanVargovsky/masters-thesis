<template>
  <v-layout row wrap>
    <v-flex xs12>
      <v-alert :value="error" type="error" transition="scale-transition"
        >Server error.</v-alert
      >
    </v-flex>
    <v-flex xs12>
      <v-text-field
        v-model="search"
        label="Search"
        single-line
        hide-details
        clearable
        prepend-icon="mdi-database-search"
      />
    </v-flex>
    <v-flex xs12>
      <v-data-table
        :headers="headers"
        :items="rows"
        :search="search"
        :loading="loading"
        :rows-per-page-items="[10, 25, 50, 100]"
      >
        <v-progress-linear
          slot="progress"
          color="blue"
          indeterminate
        ></v-progress-linear>

        <template slot="items" slot-scope="props">
          <tr :class="{ 'red lighten-5': props.item.hasNA }">
            <td class="shrink">{{ props.item.id }}</td>
            <td
              v-for="(item, index) in props.item.values"
              :key="String(props.item.id) + String(index) + String(item)"
              :class="{ red: item === NA }"
            >
              <v-tooltip top v-if="item === NA">
                <span slot="activator">{{ item }}</span>
                <span>Missing value</span>
              </v-tooltip>
              <span v-else>{{ item }}</span>
            </td>
          </tr>
        </template>

        <template slot="no-data">
          <v-alert :value="true && !loading" color="error" icon="mdi-alert"
            >No data available.</v-alert
          >
        </template>
      </v-data-table>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  props: {
    dataset: String
  },
  data() {
    return {
      NA: "NA",
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
    },
    isNA(value) {
      return value === null;
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
        const response = await this.$http.get(
          `/api/v1/dataset/${this.dataset}`
        );
        const data = response.data;
        this.columns = data.columns;
        this.rows = data.rows.map((row, index) => ({
          id: index,
          hasNA: row.some(value => value === null),
          values: row.map(value => (value !== null ? value : this.NA))
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
