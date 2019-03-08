<template>
  <v-card>
    <v-toolbar color="green" dark flat dense card>
      <v-toolbar-title class="subheading"
        >Analyse your dataset - descriptive statistics and
        histograms</v-toolbar-title
      >
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
            />
          </v-layout>
        </v-flex>
        <v-flex xs12>
          <v-progress-linear v-if="loadingDatasetDetails" indeterminate />
          <v-alert
            :value="datasetDetailsError"
            type="error"
            transition="scale-transition"
            >Server error.</v-alert
          >
        </v-flex>

        <v-container fluid grid-list-md class="pa-0">
          <v-data-iterator
            :items="columns"
            content-tag="v-layout"
            hide-actions
            no-data-text
            row
            wrap
          >
            <v-flex slot="item" slot-scope="props" xs12 sm6 md4>
              <v-card>
                <v-card-title>
                  <h4>{{ props.item.name }} ({{ props.item.type }})</h4>
                </v-card-title>

                <v-divider />

                <v-list dense v-if="props.item.numeric">
                  <v-list-tile>
                    <v-list-tile-content>Count:</v-list-tile-content>
                    <v-list-tile-content class="align-end">{{
                      props.item.descriptiveStatistics.count
                    }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Mean:</v-list-tile-content>
                    <v-list-tile-content class="align-end">{{
                      props.item.descriptiveStatistics.mean
                    }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Std:</v-list-tile-content>
                    <v-list-tile-content class="align-end">{{
                      props.item.descriptiveStatistics.std
                    }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Min:</v-list-tile-content>
                    <v-list-tile-content class="align-end">{{
                      props.item.descriptiveStatistics.min
                    }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Q1, 25%:</v-list-tile-content>
                    <v-list-tile-content class="align-end">{{
                      props.item.descriptiveStatistics.p25
                    }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Q2, Median, 50%:</v-list-tile-content>
                    <v-list-tile-content class="align-end">{{
                      props.item.descriptiveStatistics.p50
                    }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Q3, 75%:</v-list-tile-content>
                    <v-list-tile-content class="align-end">{{
                      props.item.descriptiveStatistics.p75
                    }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Max:</v-list-tile-content>
                    <v-list-tile-content class="align-end">{{
                      props.item.descriptiveStatistics.max
                    }}</v-list-tile-content>
                  </v-list-tile>
                </v-list>
                <v-list dense v-else>
                  <v-list-tile>
                    <v-list-tile-content>Count:</v-list-tile-content>
                    <v-list-tile-content class="align-end">{{
                      props.item.descriptiveStatistics.count
                    }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Unique:</v-list-tile-content>
                    <v-list-tile-content class="align-end">{{
                      props.item.descriptiveStatistics.unique
                    }}</v-list-tile-content>
                  </v-list-tile>
                </v-list>

                <v-divider />

                <v-img
                  v-if="props.item.histogramType === 'base64'"
                  :src="'data:image/jpeg;base64,' + props.item.histogram"
                />
              </v-card>
            </v-flex>
          </v-data-iterator>
        </v-container>
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
      configuration: undefined,

      loadingDatasetDetails: false,
      datasetDetailsError: false,
      columns: []
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
    async loadView() {
      try {
        this.loadingDatasetDetails = true;
        this.datasetDetailsError = false;
        let url = `/api/v1/dataset/${this.dataset}/statistics`;
        if (this.useConfiguration && this.configuration)
          url += `/${this.configuration}`;
        const response = await this.$http.get(url);
        this.columns = response.data.columns;
      } catch {
        this.datasetDetailsError = true;
        this.columns = [];
      } finally {
        this.loadingDatasetDetails = false;
      }
    }
  },
  watch: {
    dataset: async function() {
      this.configuration = undefined;
      await this.loadConfigurations();
      await this.loadView();
    },
    useConfiguration: async function() {
      if (this.configuration && this.configuration.length > 0)
        await this.loadView();
    },
    configuration: async function() {
      if (this.configuration && this.configuration.length > 0)
        await this.loadView();
    }
  }
};
</script>
