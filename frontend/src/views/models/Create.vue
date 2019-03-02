<template>
  <v-card>
    <v-toolbar color="teal" dark flat dense card>
      <v-toolbar-title class="subheading">Model creation</v-toolbar-title>
    </v-toolbar>
    <v-card-text>
      <v-form>
        <v-layout row wrap>
          <v-flex xs12>
            <v-subheader class="pa-0">Dataset</v-subheader>
            <v-overflow-btn
              v-model="dataset"
              :items="datasets"
              label="Select dataset"
              editable
              class="pt-0 mt-0"
              hide-details
            />
          </v-flex>
          <v-flex xs12 v-if="dataset">
            <v-subheader class="pa-0">Configuration</v-subheader>
            <v-layout>
              <v-checkbox v-model="useConfiguration" hide-details class="shrink"/>
              <v-overflow-btn
                v-model="configuration"
                :items="configurations"
                :disabled="!useConfiguration"
                label="Select configuration"
                editable
                class="pt-0 mt-0"
                :loading="loadingConfigurations"
                hide-details
              />
            </v-layout>
          </v-flex>
          <v-flex xs12 v-if="dataset">
            <v-subheader class="pa-0">Label</v-subheader>
            <v-overflow-btn
              v-model="labelColumn"
              :items="datasetColumns"
              item-value="name"
              :item-text="datasetColumnText"
              label="Select column label"
              editable
              class="pt-0 mt-0"
            ></v-overflow-btn>
          </v-flex>
          <v-flex xs12 v-if="dataset">
            <v-layout>
              <v-btn @click="testRun" :loading="testRunLoading" color="green" dark>Test run</v-btn>
              <v-btn color="primary">Create</v-btn>
            </v-layout>
          </v-flex>
          <v-flex xs12>
            <v-alert :value="error" type="error" transition="scale-transition">Server error.</v-alert>
          </v-flex>
          <v-flex xs12>
            <v-layout row>
              <v-flex xs6>
                <v-img v-if="accuracy" :src="'data:image/jpeg;base64,' + accuracy"/>
              </v-flex>
              <v-flex xs6>
                <v-img v-if="loss" :src="'data:image/jpeg;base64,' + loss"/>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-layout>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import store from "../../store.js";

export default {
  data() {
    return {
      datasets: store.state.datasets,
      dataset: undefined,
      datasetColumns: [],
      labelColumn: undefined,

      configurations: [],
      useConfiguration: false,
      loadingConfigurations: false,
      configuration: undefined,

      error: false,
      testRunLoading: false,
      accuracy: undefined,
      loss: undefined
    };
  },
  methods: {
    async loadConfigurations() {
      this.loadingConfigurations = true;
      const response = await this.$http.get(
        `/api/v1/dataset/${this.dataset}/configurations`
      );
      this.configurations = response.data;
      this.loadingConfigurations = false;
    },
    async loadColumns() {
      const response = await this.$http.get(`/api/v1/dataset/${this.dataset}`);
      const data = response.data;
      this.datasetColumns = data.columns.map((name, index) => ({
        name,
        type: data.columnTypes[index]
      }));
      this.tryGuessLabelColumn();
    },
    datasetColumnText(attribute) {
      return `${attribute.name} (${attribute.type})`;
    },
    tryGuessLabelColumn() {
      const names = ["label", "class"];
      const guess = this.datasetColumns.find(c => {
        const name = c.name.toLowerCase();
        return names.some(guess => name.indexOf(guess) !== -1);
      });
      if (guess) this.labelColumn = guess.name;
    },
    async testRun() {
      try {
        this.error = false;
        this.testRunLoading = true;
        const payload = {
          dataset: this.dataset,
          labelColumn: this.labelColumn
        };
        if (this.useConfiguration && this.configuration)
          payload.configuration = this.configuration;
        const response = await this.$http.post(
          `/api/v1/classification/test-run`,
          payload
        );
        const data = response.data;
        this.accuracy = data.plotAccuracy;
        this.loss = data.plotLoss;
      } catch {
        this.error = true;
        this.accuracy = undefined;
        this.loss = undefined;
      }
      this.testRunLoading = false;
    }
  },
  watch: {
    dataset: async function() {
      this.configuration = undefined;
      this.labelColumn = undefined;
      await Promise.all([this.loadConfigurations(), this.loadColumns()]);
    }
  }
};
</script>