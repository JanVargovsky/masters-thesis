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
            <v-btn
              @click="submitImport"
              :disabled="!canSubmit"
              :loading="importLoading"
              color="primary"
              >Import</v-btn
            >
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
          <v-progress-linear
            v-if="fetchLoading"
            slot="progress"
            color="blue"
          ></v-progress-linear>
          <v-flex xs12 v-if="datasetDetails">
            <v-list subheader>
              <v-subheader>Details</v-subheader>
              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title>Name</v-list-tile-title>
                  <v-list-tile-sub-title v-text="datasetDetails.name" />
                </v-list-tile-content>
              </v-list-tile>

              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title>Id</v-list-tile-title>
                  <v-list-tile-sub-title v-text="datasetDetails.id" />
                </v-list-tile-content>
              </v-list-tile>

              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title>Version</v-list-tile-title>
                  <v-list-tile-sub-title v-text="datasetDetails.version" />
                </v-list-tile-content>
              </v-list-tile>

              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title>Licence</v-list-tile-title>
                  <v-list-tile-sub-title v-text="datasetDetails.licence" />
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-flex>
        </v-layout>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import { isDatasetNameValid, defaultExtension } from "@/infrastructure/dataset";

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
      if (Number.isInteger(Number(id)))
        this.$nextTick(() => (this.dataId = id));
    },
    async submitImport() {
      this.error = false;
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
      this.error = false;
      if (!this.canFetch) return;
      try {
        this.fetchLoading = true;
        const response = await this.$http.get(
          `/api/v1/dataset-import/openml/${this.dataId}`
        );
        this.datasetDetails = response.data.data_set_description;
        this.datasetName = this.datasetDetails.name + defaultExtension;
      } catch {
        this.error = true;
        this.datasetDetails = undefined;
      } finally {
        this.fetchLoading = false;
      }
    }
  },
  computed: {
    canSubmit: function() {
      return this.dataId && isDatasetNameValid(this.datasetName);
    },
    canFetch: function() {
      return this.dataId && Number.isInteger(Number(this.dataId));
    }
  },
  created: function() {
    this.debouncedFetchOpenMLDetails = this.$_.debounce(
      this.fetchOpenMLDetails,
      1000
    );
  },
  watch: {
    dataId: function() {
      this.debouncedFetchOpenMLDetails();
    }
  }
};
</script>
