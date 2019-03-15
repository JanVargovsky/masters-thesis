<template>
  <v-card>
    <v-toolbar color="indigo" dark flat dense card>
      <v-toolbar-title class="subheading">Upload dataset</v-toolbar-title>
    </v-toolbar>
    <v-card-text>
      <v-form>
        <v-layout row wrap>
          <v-flex xs12>
            <v-text-field
              label="Select dataset(s) to upload"
              @click="$refs.dataset.click()"
              :value="datasetFileNames"
              prepend-icon="mdi-database"
              clearable
              @click:clear="reset"
            />
            <input
              type="file"
              hidden
              ref="dataset"
              :accept="acceptedDatasetExtensions"
              @change="onChange"
              multiple
            />
          </v-flex>
          <v-flex xs12>
            <v-alert :value="error" type="error" transition="scale-transition"
              >Server error.</v-alert
            >
            <v-alert
              :value="uploadedDatasets"
              type="success"
              transition="scale-transition"
            >
              Dataset <strong>{{ uploadedDatasets }}</strong> has been
              successfully uploaded.
            </v-alert>
          </v-flex>
          <v-flex xs12>
            <v-btn
              color="primary"
              :disabled="!datasetFiles"
              :loading="loading"
              @click="submit"
              >Upload</v-btn
            >
          </v-flex>
        </v-layout>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import { extensions } from "@/infrastructure/dataset";

export default {
  data() {
    return {
      datasetFiles: undefined,

      loading: false,
      uploadedDatasets: undefined,
      error: false
    };
  },
  methods: {
    onChange(e) {
      this.error = false;
      this.uploadedDatasets = undefined;
      this.datasetFiles = Array.from(e.target.files);
    },
    async submit() {
      try {
        this.error = false;
        this.uploadedDatasets = undefined;
        this.loading = true;

        let formData = new FormData();
        this.datasetFiles.forEach(f => formData.append("datasets", f));
        await this.$http.post(`/api/v1/dataset`, formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        });
        this.uploadedDatasets = this.datasetFileNames;
      } catch (error) {
        this.error = true;
      }
      this.loading = false;
    },
    reset() {
      this.error = false;
      this.uploadedDatasets = undefined;
    }
  },
  computed: {
    acceptedDatasetExtensions: function() {
      return extensions.join(",");
    },
    datasetFileNames: function() {
      if (!this.datasetFiles) return "";
      return this.datasetFiles.map(t => t.name).join(", ");
    }
  }
};
</script>
