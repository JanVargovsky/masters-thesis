<template>
  <v-layout row wrap>
    <v-flex xs12>
      <v-card>
        <v-toolbar color="primary" dark flat dense cad>
          <v-toolbar-title class="subheading">Split dataset into train and test</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-form>
            <v-layout row wrap>
              <v-flex xs12>
                <v-subheader class="pa-0">Dataset</v-subheader>
                <v-overflow-btn
                  v-model="dataset"
                  :items="datasets"
                  label="Select dataset to split"
                  editable
                ></v-overflow-btn>
              </v-flex>
              <v-flex xs12 v-if="dataset">
                <v-subheader class="pa-0">{{ rows }} rows to split</v-subheader>
                <v-slider v-model="ratio" :min="min" :max="max" always-dirty></v-slider>
              </v-flex>
              <v-flex xs12 v-if="dataset">
                <v-subheader
                  class="pa-0"
                >Split ratio ({{ trainPercent | formatPercent }} vs {{ testPercent | formatPercent }})</v-subheader>
                <v-text-field v-model="train" readonly label="Train rows" :error="train == 0"></v-text-field>
                <v-text-field v-model="test" readonly label="Test rows" :error="test == 0"></v-text-field>
              </v-flex>
              <v-flex xs12 v-if="dataset">
                <v-subheader class="pa-0">Datasets names</v-subheader>
                <v-text-field v-model="trainDatasetName" label="Train dataset name"></v-text-field>
                <v-text-field v-model="testDatasetName" label="Test dataset name"></v-text-field>
              </v-flex>
              <v-flex xs12 v-if="dataset">
                <v-alert :value="done" type="success" transition="scale-transition">
                  Datasets
                  <strong>{{ trainDatasetName }}</strong> and
                  <strong>{{ testDatasetName }}</strong> has been successfully created.
                </v-alert>
                <v-alert
                  :value="submitError"
                  type="error"
                  transition="scale-transition"
                >Server error.</v-alert>
                <v-btn
                  color="primary"
                  :disabled="train === 0 || test === 0"
                  :loading="submitLoading"
                  @click="submit"
                >Split</v-btn>
              </v-flex>
            </v-layout>
          </v-form>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
const Units = 1000;

export default {
  data() {
    return {
      ratio: 0.5 * Units,
      min: 0.001 * Units,
      max: 0.999 * Units,

      datasets: [],
      dataset: undefined,
      rows: undefined,

      trainDatasetName: undefined,
      testDatasetName: undefined,

      submitLoading: false,
      submitError: false,
      done: false
    };
  },
  async created() {
    const response = await this.$http.get("/api/v1/datasets");
    this.datasets = response.data.map(t => t.name);
  },
  methods: {
    async submit() {
      try {
        this.done = false;
        this.submitLoading = true;
        this.submitError = false;
        await this.$http.put("api/v1/preprocessing/split", {
          dataset: this.dataset,
          ratio: this.ratio / Units,
          shuffle: true,
          trainDataset: this.trainDatasetName,
          testDataset: this.testDatasetName
        });
        this.done = true;
      } catch {
        this.submitError = true;
      }
      this.submitLoading = false;
    }
  },
  computed: {
    train() {
      return Math.ceil((this.rows * this.ratio) / Units);
    },
    test() {
      return Math.trunc(this.rows * (1 - this.ratio / Units));
    },
    trainPercent() {
      return (this.ratio / Units) * 100;
    },
    testPercent() {
      return (1 - this.ratio / Units) * 100;
    }
  },
  watch: {
    dataset: async function() {
      const response = await this.$http.get(
        `/api/v1/dataset/rows/${this.dataset}`
      );
      this.rows = response.data.rows;

      const index = this.dataset.lastIndexOf(".");
      if (index > 0) {
        const name = this.dataset.substr(0, index);
        const extension = this.dataset.substr(index);
        this.trainDatasetName = `${name}-train${extension}`;
        this.testDatasetName = `${name}-test${extension}`;
      }
    }
  },
  filters: {
    formatPercent(value) {
      return `${Math.round(value, 2)} %`;
    }
  }
};
</script>
