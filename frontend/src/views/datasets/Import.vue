<template>
  <v-card>
    <v-toolbar color="indigo" dark flat dense card>
      <v-toolbar-title class="subheading"
        >Import dataset from OpenML</v-toolbar-title
      >
    </v-toolbar>
    <v-card-text>
      <v-form>
        <v-layout row wrap>
          <v-flex xs12>
            <v-text-field
              v-model="dataId"
              label="Data id"
              prefix="https://www.openml.org/d/"
              hint="Tip: You can paste whole url"
              @input="dataIdChanged"
              persistent-hint
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field v-model="datasetName" label="Dataset name" />
          </v-flex>
          <v-flex xs12>
            <v-layout>
              <v-btn
                @click="fetchOpenMLDetails"
                :disabled="!canFetch"
                :loading="fetchLoading"
                color="success"
                >Details</v-btn
              >
              <v-btn
                @click="submitImport"
                :disabled="!canSubmit"
                :loading="importLoading"
                color="primary"
                >Import</v-btn
              >
            </v-layout>
          </v-flex>
          <v-flex xs12>
            <v-alert :value="error" type="error" transition="scale-transition"
              >Server error.</v-alert
            >
            <v-alert :value="done" type="success" transition="scale-transition">
              Dataset <strong>{{ importedDataset }}</strong> has been
              successfully uploaded.
            </v-alert>
          </v-flex>
          <v-flex xs12 v-if="datasetDetails">
            Raw details:
            <pre
              >{{ datasetDetails }}
              </pre
            >
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
      dataId: undefined,
      datasetName: undefined,

      datasetDetails: undefined,
      importedDataset: undefined,
      fetchLoading: false,
      importLoading: false,
      done: false,
      error: false
    };
  },
  methods: {
    dataIdChanged(value) {
      if (!value) return;

      // https://www.openml.org/d/
      const baseUrl = "openml.org/d/";
      const index = value.lastIndexOf(baseUrl);
      if (index == -1) return;

      const id = value.substring(index + baseUrl.length);
      if (parseInt(id) !== Math.NaN) this.$nextTick(() => (this.dataId = id));
    },
    async submitImport() {
      try {
        this.importLoading = true;
        this.done = false;
        await this.$http.post(`/api/v1/dataset-import/openml/${this.dataId}`, {
          datasetName: this.datasetName
        });
        this.done = true;
        this.importedDataset = this.datasetName;
      } catch {
        this.error = true;
      } finally {
        this.importLoading = false;
      }
    },
    async fetchOpenMLDetails() {
      try {
        this.fetchLoading = true;
        const response = await this.$http.get(
          `/api/v1/dataset-import/openml/${this.dataId}`
        );
        this.datasetDetails = response.data;

        this.datasetName =
          this.datasetDetails.data_set_description.name + ".csv";
      } catch {
        this.error = true;
        this.datasetDetails = undefined;
      } finally {
        this.fetchLoading = false;
      }
    }
  },
  computed: {
    canSubmit() {
      return this.dataId && this.datasetName && this.datasetName.length > 0;
    },
    canFetch() {
      return this.dataId && parseInt(this.dataId) !== Math.NaN;
    }
  }
};
</script>
