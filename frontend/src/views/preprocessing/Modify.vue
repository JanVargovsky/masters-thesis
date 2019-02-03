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
                    <v-radio-group v-if="column.na" v-model="column.naSelected" row class="pl-3">
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
                      v-if="column.na && column.naSelected === 'custom'"
                      v-model="column.naCustomValue"
                      class="pl-3"
                      label="Custom value"
                      placeholder="Type here"
                      :type="isNumber(column) ? 'number' : 'text'"
                    />
                  </v-flex>
                </v-layout>
                <!-- Categorial -->
                <v-layout row v-if="!column.remove && isCategorical(column)">
                  <v-flex shrink>
                    <v-switch v-model="column.encode" label="Encode" color="blue"/>
                  </v-flex>
                  <v-flex shrink>
                    <v-radio-group
                      v-if="column.encode"
                      v-model="column.encodeType"
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
                <v-text-field v-model="newDatasetName" label="Modified dataset name"></v-text-field>
              </v-flex>
              <v-flex xs12 v-if="dataset">
                <v-alert :value="done" type="success" transition="scale-transition">
                  Dataset
                  <strong>{{ newDatasetName }}</strong>
                  has been successfully created.
                </v-alert>
                <v-alert
                  :value="submitError"
                  type="error"
                  transition="scale-transition"
                >Server error.</v-alert>
                <v-btn color="primary" :loading="submitLoading" @click="submit">Modify</v-btn>
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

      newDatasetName: undefined,

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
      return column.type === "int" || column.type === "float";
    },
    isCategorical(column) {
      return column.type === "object";
    },
    async submit() {
      try {
        this.done = false;
        this.submitLoading = true;
        this.submitError = false;
        await this.$http.put(`api/v1/preprocessing/modify/${this.dataset}`, {
          newDatasetName: this.newDatasetName,
        });
        this.done = true;
      } catch {
        this.submitError = true;
      }
      this.submitLoading = false;
    }
  },
  watch: {
    dataset: async function() {
      const response = await this.$http.get(`/api/v1/dataset/${this.dataset}`);
      const types = ["int", "float", "object"];
      this.columns = response.data.columns.map((name, index) => ({
        name: name,
        type: types[index % types.length],
        hasNA: index <= types.length,

        remove: false,

        normalize: false,
        normalizeRange: {
          min: 0,
          max: 1
        },

        na: false,
        naSelected: undefined,
        naCustomValue: undefined,

        encode: false,
        encodeType: undefined
      }));

      const index = this.dataset.lastIndexOf(".");
      if (index > 0) {
        const name = this.dataset.substr(0, index);
        const extension = this.dataset.substr(index);
        this.newDatasetName = `${name}-preprocessed${extension}`;
      }
    }
  }
};
</script>
