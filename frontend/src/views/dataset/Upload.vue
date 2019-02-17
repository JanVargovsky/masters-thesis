<template>
  <v-card>
    <v-toolbar color="indigo" dark flat dense card>
      <v-toolbar-title class="subheading">Dataset upload</v-toolbar-title>
    </v-toolbar>
    <v-card-text>
      <v-form>
        <v-layout row wrap>
          <v-flex xs12>
            <v-text-field
              label="Select dataset to upload"
              @click="$refs.dataset.click()"
              v-model="dataset"
              prepend-icon="mdi-database"
              clearable
            />
            <input type="file" hidden ref="dataset" accept=".csv, .xlsx, .xlsm" @change="onChange">
          </v-flex>
          <v-flex xs12>
            <v-alert :value="error" type="error" transition="scale-transition">Server error.</v-alert>
            <v-alert :value="done" type="success" transition="scale-transition">
              Dataset
              <strong>{{ dataset }}</strong> has been successfully uploaded.
            </v-alert>
          </v-flex>
          <v-flex xs12>
            <v-btn color="primary" :disabled="!dataset" :loading="loading" @click="submit">Upload</v-btn>
          </v-flex>
        </v-layout>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      dataset: undefined,
      datasetFile: undefined,

      loading: false,
      done: false,
      error: false
    };
  },
  methods: {
    onChange(e) {
      this.error = false;
      this.done = false;
      const files = e.target.files;
      if (files[0] !== undefined) {
        this.dataset = files[0].name;
        this.datasetFile = files[0];
      } else {
        this.dataset = undefined;
        this.datasetFile = undefined;
      }
    },
    async submit() {
      try {
        this.error = false;
        this.done = false;
        this.loading = true;

        // TODO: upload

        this.done = true;
      } catch (error) {
        this.error = true;
      }
      this.loading = false;
    }
  }
};
</script>
