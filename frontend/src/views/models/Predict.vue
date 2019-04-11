<template>
  <v-card>
    <v-toolbar color="purple" dark flat dense card>
      <v-toolbar-title class="subheading">Make predictions</v-toolbar-title>
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
          <v-flex xs12>
            <v-subheader class="pa-0">Model</v-subheader>
            <v-overflow-btn
              v-model="model"
              :items="models"
              label="Select model"
              editable
              class="pt-0 mt-0"
              :loading="loadingModels"
            />
          </v-flex>
          <v-flex xs12>
            <v-btn
              @click="predict"
              :disabled="!dataset || !model"
              :loading="predictLoading"
              color="primary"
              >Predict</v-btn
            >
          </v-flex>
          <v-flex xs12>
            <v-alert :value="error" type="error" transition="scale-transition"
              >Server error.</v-alert
            >
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
import store from "@/store";
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

      models: [],
      model: undefined,
      loadingModels: false,

      predictLoading: false,
      score: undefined,
      plots: [],
      confusionMatrix: [],

      error: false
    };
  },
  async created() {
    await this.fetchModels();
  },
  methods: {
    async fetchModels() {
      try {
        this.error = false;
        this.loadingModels = true;
        const response = await this.$http.get(`/api/v1/classification`);
        this.models = response.data;
      } catch {
        this.error = true;
      } finally {
        this.loadingModels = false;
      }
    },
    async predict() {
      try {
        this.error = false;
        this.predictLoading = true;
        const response = await this.$http.get(
          `/api/v1/classification/${this.model}/predict/${this.dataset}`
        );
        const data = response.data;
        this.score = data.score;
        this.plots = data.plots;
        this.confusionMatrix = data.confusionMatrix;
      } catch {
        this.error = true;
      } finally {
        this.predictLoading = false;
      }
    }
  },
  computed: {
    scoreIcon: function() {
      return scoreToIcon(this.score);
    }
  },
  filters: {
    round: function(value, accuracy) {
      return +value.toFixed(accuracy);
    }
  }
};
</script>
