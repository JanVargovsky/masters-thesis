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
            <v-tabs v-model="tabs" grow slider-color="primary">
              <v-tab>Auto</v-tab>
              <v-tab-item></v-tab-item>

              <v-tab>Simple</v-tab>
              <v-tab-item></v-tab-item>

              <v-tab>Advanced</v-tab>
              <v-tab-item>
                <v-layout row wrap>
                  <v-flex xs12>
                    <v-text-field v-model="epochs" type="number" label="Epochs"/>
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field v-model="layers" label="Layers"/>
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field v-model="validationSplit" type="number" label="Validation split"/>
                  </v-flex>
                </v-layout>
              </v-tab-item>
            </v-tabs>
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
          <v-flex xs12 v-if="score">
            <v-layout justify-center column>
              <v-icon size="100">{{ scoreIcon }}</v-icon>
              <span class="text-xs-center">Accuracy: {{ score * 100 | round(2) }}%</span>
            </v-layout>
          </v-flex>
          <v-flex xs12>
            <v-layout row wrap>
              <v-flex v-for="(plot, i) in plots" :key="i" xs12 md6 lg4>
                <v-img :src="'data:image/jpeg;base64,' + plot"/>
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

      tabs: undefined,

      epochs: 100,
      layers: "32 32",
      validationSplit: 0.3,

      error: false,
      testRunLoading: false,
      score: undefined,
      plots: []
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
          labelColumn: this.labelColumn,
          epochs: parseInt(this.epochs),
          layers: this.layers.match(/\d+/g).map(t => parseInt(t))
        };

        if (this.useConfiguration && this.configuration)
          payload.configuration = this.configuration;

        const validationSplit = parseFloat(this.validationSplit);
        if (!isNaN(validationSplit)) payload.validationSplit = validationSplit;

        const response = await this.$http.post(
          `/api/v1/classification/test-run`,
          payload
        );
        const data = response.data;
        this.score = data.score;
        this.plots = data.plots;
      } catch {
        this.error = true;
        this.score = undefined;
        this.plots = [];
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
  },
  computed: {
    scoreIcon: function() {
      if (this.score < 0.3) return "mdi-emoticon-dead";
      if (this.score < 0.5) return "mdi-emoticon-sad";
      if (this.score < 0.7) return "mdi-emoticon-neutral";
      if (this.score < 0.9) return "mdi-emoticon-happy";
      return "mdi-emoticon-excited";
    }
  },
  filters: {
    round: function(value, accuracy) {
      return +value.toFixed(accuracy);
    }
  }
};
</script>
