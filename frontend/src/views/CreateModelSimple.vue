<template>
  <v-layout row wrap>
    <v-flex>
      <v-alert :value="done" type="success">
        Model
        <strong>{{ modelName }}</strong> has been successfully created.
      </v-alert>
      <v-stepper v-if="!done" vertical v-model="step">
        <v-stepper-step step="1" :complete="step > 1">
          Select model type
          <small>Classification, Clustering or Regression</small>
        </v-stepper-step>
        <v-stepper-content step="1">
          <v-btn
            v-for="item in availableModelTypes"
            :color="item == modelType ? 'primary': 'normal'"
            :key="item"
            @click="selectModelType(item)"
          >{{ item }}</v-btn>
        </v-stepper-content>

        <v-stepper-step step="2" :complete="step > 2">
          Select datasets
          <small>Training and test dataset</small>
        </v-stepper-step>
        <v-stepper-content step="2">
          <!--
        TODO: leave two options
        1) two files - verify same columns
        2) one file and split it internally
          -->
          <v-subheader>Training dataset</v-subheader>
          <v-overflow-btn
            v-model="trainingDataset"
            :items="availableTrainingDatasets"
            label="Select training dataset"
            editable
          ></v-overflow-btn>
          <v-subheader>Testing dataset</v-subheader>
          <v-overflow-btn
            v-model="testingDataset"
            :items="availableTestingDatasets"
            label="Select testing dataset"
            editable
          ></v-overflow-btn>

          <v-alert
            v-for="alert in datasetAlerts"
            :key="alert.message"
            :value="true"
            :type="alert.type"
            transition="scale-transition"
          >{{ alert.message }}</v-alert>

          <v-btn :disabled="!selectedDatasetsValid" @click="selectDatasets" color="primary">Next</v-btn>
        </v-stepper-content>

        <v-stepper-step step="3" :complete="step > 3">
          Select which column is label
          <small>Value to predict</small>
        </v-stepper-step>
        <v-stepper-content step="3">
          <p>Label column</p>
          <v-overflow-btn
            v-model="selectedDatasetColumn"
            :items="datasetsColumns"
            item-value="name"
            :item-text="datasetsColumnsText"
            label="Select column label"
            editable
          ></v-overflow-btn>

          <v-btn :disabled="!selectedDatasetColumn" @click="nextStep" color="primary">Next</v-btn>
        </v-stepper-content>

        <v-stepper-step step="4" :complete="step > 4">Summary</v-stepper-step>
        <v-stepper-content step="4">
          <v-text-field
            v-model="modelName"
            label="Model name"
            :placeholder="'My ' + modelType + ' model'"
            :error="modelName && modelName.length == 0"
          />

          <p>Review your inputs</p>
          <v-text-field readonly v-model="modelType" label="Model type"/>
          <v-text-field readonly v-model="trainingDataset" label="Training dataset"/>
          <v-text-field readonly v-model="testingDataset" label="Testing dataset"/>
          <v-text-field readonly v-model="selectedDatasetColumn" label="Column name to predict"/>

          <v-alert :value="true" type="info">This might take a while till processed.</v-alert>
          <v-alert :value="submitError" type="error">Server error.</v-alert>

          <v-btn
            :disabled="!modelName || modelName.length == 0"
            @click="submit"
            color="primary"
            :loading="submitLoading"
          >Submit</v-btn>
        </v-stepper-content>
      </v-stepper>
    </v-flex>
  </v-layout>
</template>

<script>
import store from "../store.js";

export default {
  data() {
    return {
      step: 0,
      done: false,

      availableModelTypes: ["Classification", "Clustering", "Regression"],
      modelType: undefined,

      availableDatasets: store.state.datasets,
      trainingDataset: undefined,
      testingDataset: undefined,
      selectedDatasetsValid: false,
      datasetAlerts: [],

      datasetsColumns: [],
      selectedDatasetColumn: undefined,

      modelName: undefined,

      submitLoading: false,
      submitError: false
    };
  },
  computed: {
    availableTrainingDatasets: function() {
      return this.availableDatasets.filter(t => this.testingDataset !== t);
    },
    availableTestingDatasets: function() {
      return this.availableDatasets.filter(t => this.trainingDataset !== t);
    }
  },
  methods: {
    nextStep() {
      this.step++;
    },
    selectModelType(modelType) {
      this.modelType = modelType;
      if (modelType === this.availableModelTypes[0]) this.nextStep();
    },
    async validateDatasets() {
      // query column types for dataset and if both are set then compare them
      this.datasetAlerts = [];
      if (!this.trainingDataset || !this.testingDataset) return false;
      try {
        const response = await this.$http.get(
          `/api/v1/model/validate/${this.trainingDataset}/${
            this.testingDataset
          }`
        );
        const data = response.data;
        if (!data.length)
          this.datasetAlerts.push({
            type: "error",
            message: "Count of columns is different."
          });
        else if (!data.types)
          this.datasetAlerts.push({
            type: "error",
            message: "Incompatible column types."
          });
        else if (!data.columns) {
          this.datasetAlerts.push({
            type: "warning",
            message: "Different column names."
          });
        }
        return data.length && data.types && data.columns;
      } catch {
        this.datasetAlerts.push({
          type: "error",
          message: "Server error."
        });
        return false;
      }
    },
    async selectDatasets() {
      const response = await this.$http.get(
        `/api/v1/dataset/${this.trainingDataset}`
      );
      const data = response.data;
      this.datasetsColumns = data.columns.map((name, index) => ({
        name,
        type: data.columnTypes[index]
      }));
      this.nextStep();
    },
    datasetsColumnsText(attribute) {
      return `${attribute.name} (${attribute.type})`;
    },
    async submit() {
      try {
        this.submitLoading = true;
        this.submitError = false;
        await this.$http.post("/api/v1/model/classification/simple", {
          name: this.modelName,
          trainingDataset: this.trainingDataset,
          testingDataset: this.testingDataset,
          labelColumnName: this.selectedDatasetColumn
        });
        this.done = true;
      } catch {
        this.submitError = true;
      }
      this.submitLoading = false;
    }
  },
  watch: {
    trainingDataset: async function() {
      this.selectedDatasetsValid = await this.validateDatasets();
    },
    testingDataset: async function() {
      this.selectedDatasetsValid = await this.validateDatasets();
    }
  }
};
</script>
