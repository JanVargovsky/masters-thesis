<template>
  <v-layout row wrap>
    <v-flex xs12>
      <v-card>
        <v-toolbar color="red" dark flat dense card>
          <v-toolbar-title
            class="subheading"
          >Modify dataset - remove, fix missing, normalize or encode values</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-form>
            <v-layout row wrap>
              <v-flex xs12>
                <v-subheader class="pa-0">Dataset</v-subheader>
                <v-overflow-btn
                  v-model="dataset"
                  :items="datasets"
                  label="Select dataset to modify"
                  editable
                  class="pt-0 mt-0"
                />
              </v-flex>
              <v-flex xs12 row v-for="(column) in columns" :key="column.name">
                <v-subheader class="pa-0">{{ column.name }} ({{ column.type }})</v-subheader>
                <!-- Remove -->
                <v-switch v-model="column.remove" label="Remove" color="red"/>
                <!-- Normalize -->
                <v-layout row v-if="!column.remove && isNumber(column)">
                  <v-flex shrink>
                    <v-switch v-model="column.normalize" label="Normalize" color="orange"/>
                  </v-flex>
                  <v-flex shrink>
                    <v-text-field
                      v-if="column.normalize"
                      v-model="column.normalizeRange.min"
                      class="pl-3"
                      label="Min"
                      type="number"
                    />
                  </v-flex>
                  <v-flex shrink>
                    <v-text-field
                      v-if="column.normalize"
                      v-model="column.normalizeRange.max"
                      class="pl-3"
                      label="Max"
                      type="number"
                    />
                  </v-flex>
                </v-layout>
                <!-- Missing values -->
                <v-layout row v-if="!column.remove && column.hasNA">
                  <v-flex shrink>
                    <v-switch v-model="column.na" label="Fix missing values" color="green"/>
                  </v-flex>
                  <v-flex shrink>
                    <v-radio-group v-if="column.na" v-model="column.naMethod" row class="pl-3">
                      <v-radio v-if="isNumber(column)" label="Using 0" value="zero" color="green"/>
                      <v-radio
                        v-if="isNumber(column)"
                        label="Using average"
                        value="average"
                        color="green"
                      />
                      <v-radio label="Using the most common" value="common" color="green"/>
                      <v-radio label="Custom" value="custom" color="green"/>
                    </v-radio-group>
                  </v-flex>
                  <v-flex shrink>
                    <v-text-field
                      v-if="column.na && column.naMethod === 'custom'"
                      v-model="column.naCustomValue"
                      class="pl-3"
                      label="Custom value"
                      placeholder="Type here"
                      :type="isNumber(column) ? 'number' : 'text'"
                    />
                  </v-flex>
                </v-layout>
                <!-- Categorical -->
                <v-layout row v-if="!column.remove && isCategorical(column)">
                  <v-flex shrink>
                    <v-switch v-model="column.encode" label="Encode" color="blue"/>
                  </v-flex>
                  <v-flex shrink>
                    <v-radio-group
                      v-if="column.encode"
                      v-model="column.encodeMethod"
                      row
                      class="pl-3"
                    >
                      <v-radio label="Label/Integer encoding" value="label" color="blue"/>
                      <v-radio label="One-Hot encoding" value="oneHot" color="blue"/>
                    </v-radio-group>
                  </v-flex>
                </v-layout>
              </v-flex>
              <v-flex xs12 v-if="dataset">
                <v-layout>
                  <v-checkbox v-model="useNewDatasetName" hide-details class="shrink"/>
                  <v-text-field
                    v-model="newDatasetName"
                    :disabled="!useNewDatasetName"
                    label="New modified dataset name"
                  />
                </v-layout>
                <v-layout>
                  <v-checkbox v-model="useConfigurationName" hide-details class="shrink"/>
                  <v-text-field
                    v-model="configurationName"
                    :disabled="!useConfigurationName"
                    label="Configuration name"
                  />
                </v-layout>
              </v-flex>
              <v-flex xs12 v-if="dataset">
                <v-alert
                  :value="done && useNewDatasetName && this.newDatasetName.length !== 0"
                  type="success"
                  transition="scale-transition"
                >
                  Dataset
                  <strong>{{ newDatasetName }}</strong>
                  has been successfully created.
                </v-alert>
                <v-alert
                  :value="done && useConfigurationName && this.configurationName.length !== 0"
                  type="success"
                  transition="scale-transition"
                >
                  Configuration
                  <strong>{{ configurationName }}</strong>
                  has been successfully created.
                </v-alert>
                <v-alert
                  :value="submitError"
                  type="error"
                  transition="scale-transition"
                >Server error.</v-alert>
                <v-btn
                  :disabled="disableSubmit"
                  :loading="submitLoading"
                  @click="submit"
                  color="primary"
                >Submit</v-btn>
              </v-flex>
            </v-layout>
          </v-form>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {
      datasets: [],
      dataset: undefined,

      columns: [],

      useNewDatasetName: false,
      newDatasetName: undefined,
      useConfigurationName: false,
      configurationName: undefined,

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
    isNumber(column) {
      return column.type === "int64" || column.type === "float64";
    },
    isCategorical(column) {
      return column.type === "object";
    },
    async submit() {
      try {
        this.done = false;
        this.submitLoading = true;
        this.submitError = false;
        let payload = {
          columns: this.columns.map(column => ({
            name: column.name,
            remove: column.remove,
            normalize: column.normalize,
            normalizeRange: {
              min: parseFloat(column.normalizeRange.min),
              max: parseFloat(column.normalizeRange.max)
            },
            na: column.na,
            naMethod: column.naMethod,
            naCustomValue: column.naCustomValue,
            encode: column.encode,
            encodeMethod: column.encodeMethod
          }))
        };
        if (this.useNewDatasetName && this.newDatasetName.length !== 0)
          payload.newDatasetName = this.newDatasetName;
        if (this.useConfigurationName && this.configurationName.length !== 0)
          payload.configurationName = this.configurationName;

        await this.$http.put(
          `api/v1/preprocessing/modify/${this.dataset}`,
          payload
        );

        this.done = true;
      } catch {
        this.submitError = true;
      }
      this.submitLoading = false;
    },
    reset() {
      this.done = false;
      this.submitError = false;
    }
  },
  watch: {
    dataset: async function() {
      const response = await this.$http.get(
        `/api/v1/preprocessing/modify/${this.dataset}`
      );
      this.columns = response.data.columns.map(column => ({
        name: column.name,
        type: column.type,
        hasNA: column.hasNA,

        remove: false,

        normalize: false,
        normalizeRange: {
          min: 0,
          max: 1
        },

        na: false,
        naMethod: undefined,
        naCustomValue: undefined,

        encode: false,
        encodeMethod: undefined
      }));

      const index = this.dataset.lastIndexOf(".");
      if (index > 0) {
        const name = this.dataset.substr(0, index);
        const extension = this.dataset.substr(index);
        this.newDatasetName = `${name}-preprocessed${extension}`;
        this.configurationName = `${name}-configuration`;
      }
    },
    useNewDatasetName() {
      this.reset();
    },
    newDatasetName() {
      this.reset();
    },
    useConfigurationName() {
      this.reset();
    },
    configurationName() {
      this.reset();
    },
    columns: {
      handler: function() {
        this.reset();
      },
      deep: true
    }
  },
  computed: {
    disableSubmit() {
      if (!this.useNewDatasetName && !this.useConfigurationName) return true;
      if (this.useNewDatasetName && this.newDatasetName.length === 0)
        return true;
      if (this.useConfigurationName && this.configurationName.length === 0)
        return true;
      return false;
    }
  }
};
</script>
