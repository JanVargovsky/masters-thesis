<template>
  <v-card>
    <v-toolbar color="teal" dark flat dense card>
      <v-toolbar-title class="subheading"
        >Classification model creation</v-toolbar-title
      >
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
              <v-checkbox
                v-model="useConfiguration"
                hide-details
                class="shrink"
              />
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
            <v-text-field v-model="modelName" label="Model name" />
          </v-flex>
          <v-flex xs12 v-if="dataset">
            <v-tabs v-model="tabs" grow slider-color="primary">
              <v-tab>Simple</v-tab>
              <v-tab-item>
                <v-layout row wrap>
                  <v-flex xs12>
                    <v-subheader class="pa-0">Time</v-subheader>
                    <v-tooltip top>
                      <v-btn
                        slot="activator"
                        @click="removeTime"
                        flat
                        icon
                        color="red"
                      >
                        <v-icon large>mdi-minus-box</v-icon>
                      </v-btn>
                      <span>Train less</span>
                    </v-tooltip>
                    <v-tooltip top>
                      <v-btn
                        slot="activator"
                        @click="addTime"
                        flat
                        icon
                        color="green"
                      >
                        <v-icon large>mdi-plus-box</v-icon>
                      </v-btn>
                      <span>Train more</span>
                    </v-tooltip>
                    {{ epochs }}
                  </v-flex>
                  <v-flex xs12>
                    <v-subheader class="pa-0">Size</v-subheader>
                    <v-tooltip top>
                      <v-btn
                        slot="activator"
                        @click="removeLastLayer"
                        flat
                        icon
                        color="red"
                      >
                        <v-icon large>mdi-collapse-all</v-icon>
                      </v-btn>
                      <span>Remove layer</span>
                    </v-tooltip>
                    <v-tooltip top>
                      <v-btn
                        slot="activator"
                        @click="addLayer"
                        flat
                        icon
                        color="green"
                      >
                        <v-icon large>mdi-expand-all</v-icon>
                      </v-btn>
                      <span>Add layer</span>
                    </v-tooltip>

                    <v-tooltip top>
                      <v-btn
                        slot="activator"
                        @click="autoShrinkLayer"
                        flat
                        icon
                        color="red"
                      >
                        <v-icon large>mdi-layers-minus</v-icon>
                      </v-btn>
                      <span>Shrink layer</span>
                    </v-tooltip>
                    <v-tooltip top>
                      <v-btn
                        slot="activator"
                        @click="autoExpandLayer"
                        flat
                        icon
                        color="green"
                      >
                        <v-icon large>mdi-layers-plus</v-icon>
                      </v-btn>
                      <span>Expand layer</span>
                    </v-tooltip>
                    {{ layersDisplay }}
                  </v-flex>
                </v-layout>
              </v-tab-item>

              <v-tab>Advanced</v-tab>
              <v-tab-item>
                <v-layout row wrap>
                  <v-flex xs12>
                    <v-text-field
                      v-model.number="epochs"
                      type="number"
                      label="Epochs"
                    />
                  </v-flex>
                  <v-flex xs12>
                    <v-text-field
                      v-model.number="validationSplit"
                      type="number"
                      label="Validation split"
                      hide-details
                    />
                  </v-flex>
                  <v-flex xs12>
                    <v-subheader class="pa-0">Layers</v-subheader>
                    <v-layout>
                      <v-flex shrink>
                        <v-tooltip top>
                          <v-btn
                            slot="activator"
                            @click="addLayerStart"
                            flat
                            icon
                          >
                            <v-icon class="mdi-rotate-180"
                              >mdi-expand-all-outline</v-icon
                            >
                          </v-btn>
                          <span>Add new layer to start</span>
                        </v-tooltip>
                      </v-flex>
                      <v-flex shrink>
                        <v-tooltip top>
                          <v-btn
                            slot="activator"
                            @click="addLayerEnd"
                            flat
                            icon
                          >
                            <v-icon>mdi-expand-all</v-icon>
                          </v-btn>
                          <span>Add new layer to end</span>
                        </v-tooltip>
                      </v-flex>
                    </v-layout>
                    <v-layout v-for="(layer, index) in layers" :key="index">
                      <v-flex shrink>
                        <v-tooltip top>
                          <v-btn
                            slot="activator"
                            @click="shrinkLayer(index)"
                            flat
                            icon
                            color="red"
                          >
                            <v-icon>mdi-layers-minus</v-icon>
                          </v-btn>
                          <span>Shrink layer</span>
                        </v-tooltip>
                      </v-flex>
                      <v-flex shrink>
                        <v-text-field
                          v-model.number="layers[index]"
                          type="number"
                          :label="'Dense layer ' + (index + 1)"
                          flat
                          hide-details
                        ></v-text-field>
                      </v-flex>
                      <v-flex shrink>
                        <v-tooltip top>
                          <v-btn
                            slot="activator"
                            @click="expandLayer(index)"
                            flat
                            icon
                            color="green"
                          >
                            <v-icon>mdi-layers-plus</v-icon>
                          </v-btn>
                          <span>Expand layer</span>
                        </v-tooltip>
                      </v-flex>
                      <v-flex shrink>
                        <v-tooltip top>
                          <v-btn
                            slot="activator"
                            @click="removeLayer(index)"
                            flat
                            icon
                          >
                            <v-icon>mdi-layers-remove</v-icon>
                          </v-btn>
                          <span>Delete layer</span>
                        </v-tooltip>
                      </v-flex>
                    </v-layout>
                  </v-flex>
                </v-layout>
              </v-tab-item>
            </v-tabs>
          </v-flex>
          <v-flex xs12 v-if="dataset" class="pt-3">
            <v-layout>
              <v-btn
                @click="testRun"
                :loading="testRunLoading"
                color="green"
                dark
                >Test run</v-btn
              >
              <v-menu offset-y>
                <template slot="activator">
                  <v-btn :loading="crossValidationLoading" color="green" dark>
                    Cross validate
                  </v-btn>
                </template>
                <v-list>
                  <v-list-tile
                    v-for="(item, index) in [3, 4, 5, 10]"
                    :key="index"
                    @click="crossValidate(item)"
                  >
                    <v-list-tile-title>{{ item }}-fold</v-list-tile-title>
                  </v-list-tile>
                </v-list>
              </v-menu>
              <v-btn
                @click="create"
                :loading="createLoading"
                :disabled="!modelName"
                color="primary"
                >Create</v-btn
              >
            </v-layout>
          </v-flex>
          <v-flex xs12>
            <v-alert :value="error" type="error" transition="scale-transition"
              >Server error.</v-alert
            >
            <v-alert
              :value="createdModel"
              type="success"
              transition="scale-transition"
              >Model <strong>{{ createdModel }}</strong> has been successfully
              created.</v-alert
            >
          </v-flex>
          <v-flex xs12 v-if="crossValidationScore">
            <v-layout justify-center column>
              <v-icon size="100">{{ scoreIcon }}</v-icon>
              <span class="text-xs-center body-2"
                >Cross-validation accuracy:
                {{ (crossValidationScore * 100) | round(2) }}%</span
              >
            </v-layout>
          </v-flex>
          <v-flex xs12 v-if="score">
            <v-layout justify-center column>
              <v-icon size="100">{{ scoreIcon }}</v-icon>
              <span class="text-xs-center body-2"
                >Accuracy: {{ (score * 100) | round(2) }}%</span
              >
            </v-layout>
          </v-flex>
          <v-flex xs12>
            <v-layout row wrap>
              <v-flex v-for="(plot, i) in plots" :key="i" xs12 md6 lg4>
                <v-img :src="'data:image/jpeg;base64,' + plot" />
              </v-flex>
            </v-layout>
          </v-flex>
          <v-flex xs12 v-if="confusionMatrix && confusionMatrix.length > 0">
            <v-subheader class="pa-0">Confusion matrix</v-subheader>
            <confusion-matrix :matrix="confusionMatrix" />
          </v-flex>
        </v-layout>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import store from "../../store.js";
import { scoreToIcon } from "@/infrastructure/model";
import ConfusionMatrix from "@/components/ConfusionMatrix";

export default {
  components: {
    ConfusionMatrix
  },
  data() {
    return {
      datasets: store.state.datasets,
      dataset: undefined,
      datasetColumns: [],
      labelColumn: undefined,
      modelName: undefined,

      configurations: [],
      useConfiguration: false,
      loadingConfigurations: false,
      configuration: undefined,

      tabs: undefined,

      epochs: 100,
      layers: [32, 32],
      validationSplit: 0.3,

      error: false,
      testRunLoading: false,
      crossValidationLoading: false,
      createLoading: false,
      crossValidationScore: undefined,
      createdModel: undefined,
      score: undefined,
      plots: [],
      confusionMatrix: []
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
      const response = await this.$http.get(
        `/api/v1/dataset/${this.dataset}/5`
      );
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
    calculateTimeDiff() {
      if (this.epochs > 1000) return 100;
      if (this.epochs > 100) return Math.floor(this.epochs / 100) * 10;
      if (this.epochs > 10) return 10;
      return 1;
    },
    addTime() {
      this.epochs += this.calculateTimeDiff();
    },
    removeTime() {
      this.epochs -= this.calculateTimeDiff();
      if (this.epochs < 1) this.epochs = 1;
    },
    addLayer() {
      this.layers.push(1);
    },
    addLayerStart() {
      this.layers.unshift(1);
    },
    addLayerEnd() {
      this.layers.push(1);
    },
    removeLastLayer() {
      this.layers.pop();
    },
    removeLayer(index) {
      this.layers.splice(index, 1);
    },
    autoExpandLayer() {
      const indexOfSmallest = this.layers.reduce(
        (lowest, next, index) => (next < this.layers[lowest] ? index : lowest),
        0
      );

      this.expandLayer(indexOfSmallest);
    },
    autoShrinkLayer() {
      const indexOfLargest = this.layers.reduceRight(
        (largest, next, index) =>
          next > this.layers[largest] ? index : largest,
        this.layers.length - 1
      );

      this.shrinkLayer(indexOfLargest);
    },
    expandLayer(index) {
      if (index < this.layers.length)
        this.$set(this.layers, index, this.layers[index] * 2);
    },
    shrinkLayer(index) {
      if (index < this.layers.length)
        this.$set(this.layers, index, Math.ceil(this.layers[index] / 2));
    },
    async testRun() {
      try {
        this.error = false;
        this.createdModel = undefined;
        this.testRunLoading = true;
        const payload = this.getPayload();

        const response = await this.$http.post(
          `/api/v1/classification/test-run`,
          payload
        );
        const data = response.data;
        this.resetResults();
        this.score = data.score;
        this.plots = data.plots;
        this.confusionMatrix = data.confusionMatrix;
      } catch {
        this.error = true;
        this.resetResults();
      }
      this.testRunLoading = false;
    },
    async crossValidate(kfolds) {
      try {
        this.error = false;
        this.createdModel = undefined;
        this.crossValidationLoading = true;
        const payload = this.getPayload(false);
        payload.kfolds = kfolds;

        const response = await this.$http.post(
          `/api/v1/classification/cross-validation`,
          payload
        );
        const data = response.data;
        this.resetResults();
        this.crossValidationScore = this.$_.mean(data.testScores);
        this.plots = data.plots;
      } catch {
        this.error = true;
        this.resetResults();
      }
      this.crossValidationLoading = false;
    },
    async create() {
      try {
        this.error = false;
        this.createdModel = undefined;
        this.createLoading = true;
        const payload = this.getPayload();

        const response = await this.$http.post(
          `/api/v1/classification/${this.modelName}`,
          payload
        );
        const data = response.data;
        this.resetResults();
        this.createdModel = this.modelName;
        this.score = data.score;
        this.plots = data.plots;
        this.confusionMatrix = data.confusionMatrix;
      } catch {
        this.error = true;
        this.resetResults();
      }
      this.createLoading = false;
    },
    getPayload(appendValidationSplit = true) {
      const payload = {
        dataset: this.dataset,
        labelColumn: this.labelColumn,
        epochs: this.epochs,
        layers: this.layers
      };

      if (this.useConfiguration && this.configuration)
        payload.configuration = this.configuration;

      if (appendValidationSplit && this.validationSplit)
        payload.validationSplit = this.validationSplit;
      return payload;
    },
    resetResults() {
      this.createdModel = undefined;
      this.score = undefined;
      this.crossValidationScore = undefined;
      this.plots = [];
      this.confusionMatrix = [];
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
      return scoreToIcon(this.score);
    },
    layersDisplay: function() {
      if (this.layers.length == 0) return "No layers!";
      return this.layers.join(" - ");
    }
  },
  filters: {
    round: function(value, accuracy) {
      return +value.toFixed(accuracy);
    }
  }
};
</script>
