<template>
  <v-card>
    <v-toolbar color="brown" dark flat dense card>
      <v-toolbar-title class="subheading">Configurations</v-toolbar-title>
    </v-toolbar>
    <v-card-text>
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
            <v-overflow-btn
              v-model="configurationName"
              :items="configurations"
              label="Select configuration"
              editable
              class="pt-0 mt-0"
              :loading="loadingConfigurations"
            />
            <v-tooltip top>
              <v-btn
                slot="activator"
                fab
                icon
                small
                class="ma-0"
                @click="deleteConfiguration"
                :disabled="!configuration"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
              <span>Delete</span>
            </v-tooltip>
          </v-layout>
        </v-flex>
        <v-flex xs12 v-if="dataset">
          <v-progress-linear v-if="loadingConfiguration" indeterminate />
          <v-alert :value="error" type="error" transition="scale-transition"
            >Server error.</v-alert
          >
        </v-flex>
        <v-flex xs12 v-if="configuration">
          <pre>{{ JSON.stringify(configuration, null, 2) }}</pre>
        </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>
</template>

<script>
import store from "../../store.js";

export default {
  data() {
    return {
      datasets: store.state.datasets,
      dataset: undefined,

      configurations: [],
      useConfiguration: false,
      loadingConfigurations: false,
      configurationName: undefined,

      configuration: undefined,
      configurationTree: undefined,
      loadingConfiguration: false,

      error: false
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
    async deleteConfiguration() {
      if (
        confirm(`Are you sure you want to delete ${this.configurationName}?`)
      ) {
        try {
          await this.$http.delete(
            `/api/v1/dataset/${this.dataset}/configurations/${
              this.configurationName
            }`
          );
          this.configurations = this.configurations.filter(
            t => t !== this.configurationName
          );
          this.configurationName = undefined;
          this.configuration = undefined;
        } catch (error) {
          this.error = true;
        }
      }
    }
  },
  watch: {
    dataset: async function() {
      await this.loadConfigurations();
    },
    configurationName: async function() {
      if (!this.configurationName) return;

      this.loadingConfiguration = true;
      const response = await this.$http.get(
        `/api/v1/dataset/${this.dataset}/configurations/${
          this.configurationName
        }`
      );
      this.configuration = response.data;
      this.loadingConfiguration = false;
    }
  }
};
</script>
