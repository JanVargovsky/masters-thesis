<template>
  <v-dialog v-model="show" max-width="600px">
    <v-btn slot="activator" icon>
      <v-icon>mdi-settings</v-icon>
    </v-btn>
    <v-card>
      <v-card-title class="headline">Settings</v-card-title>
      <v-card-text>
        <v-container fluid>
          <v-layout wrap>
            <v-flex xs12>
              <v-switch v-model="filter" label="Select datasets you are working with" hide-details/>
              <v-combobox
                v-model="datasets"
                :items="allDatasets"
                :label="filter ? 'Datasets' : 'All datasets'"
                multiple
                chips
                clearable
                small-chips
                deletable-chips
                prepend-icon="mdi-database"
                :disabled="!filter"
              />
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" flat @click="close">Close</v-btn>
        <v-btn color="primary" flat @click="save">Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import store from "../../store.js";

export default {
  data() {
    return {
      show: false,
      filter: false,
      datasets: [],
      allDatasets: store.state.allDatasets
    };
  },
  async created() {
    const response = await this.$http.get("/api/v1/datasets");
    store.setAllDatasets(response.data.map(item => item.name));
    store.setDatasets(response.data.map(item => item.name));
  },
  methods: {
    close() {
      this.show = false;
    },
    save() {
      if (this.filter) {
        store.setDatasets(this.datasets);
      } else {
        store.setDatasets(this.allDatasets);
      }
      store.setFilter(this.filter);
      this.show = false;
    }
  },
  watch: {
    show(value) {
      if (value) {
        this.filter = store.state.filter;
        this.datasets = this.filter ? store.state.datasets : [];
      }
    },
    filter(value) {
      if (!value) this.datasets = [];
    }
  }
};
</script>
