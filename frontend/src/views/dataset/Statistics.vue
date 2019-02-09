<template>
  <v-card>
    <v-toolbar color="green" dark flat dense card>
      <v-toolbar-title
        class="subheading"
      >Analyse your dataset - descriptive statistics and histograms</v-toolbar-title>
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
            :loading="loadingDatasets"
          />
        </v-flex>
        <v-flex xs12>
          <v-progress-linear v-if="loadingDatasetDetails" indeterminate/>
          <v-alert
            :value="datasetDetailsError"
            type="error"
            transition="scale-transition"
          >Server error.</v-alert>
        </v-flex>

        <v-container fluid grid-list-md>
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

                <v-divider/>

                <v-list dense v-if="props.item.numeric">
                  <v-list-tile>
                    <v-list-tile-content>Count:</v-list-tile-content>
                    <v-list-tile-content
                      class="align-end"
                    >{{ props.item.descriptiveStatistics.count }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Mean:</v-list-tile-content>
                    <v-list-tile-content
                      class="align-end"
                    >{{ props.item.descriptiveStatistics.mean }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Std:</v-list-tile-content>
                    <v-list-tile-content
                      class="align-end"
                    >{{ props.item.descriptiveStatistics.std }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Min:</v-list-tile-content>
                    <v-list-tile-content
                      class="align-end"
                    >{{ props.item.descriptiveStatistics.min }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Q1, 25%:</v-list-tile-content>
                    <v-list-tile-content
                      class="align-end"
                    >{{ props.item.descriptiveStatistics.p25 }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Q2, Median, 50%:</v-list-tile-content>
                    <v-list-tile-content
                      class="align-end"
                    >{{ props.item.descriptiveStatistics.p50 }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Q3, 75%:</v-list-tile-content>
                    <v-list-tile-content
                      class="align-end"
                    >{{ props.item.descriptiveStatistics.p75 }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Max:</v-list-tile-content>
                    <v-list-tile-content
                      class="align-end"
                    >{{ props.item.descriptiveStatistics.max }}</v-list-tile-content>
                  </v-list-tile>
                </v-list>
                <v-list dense v-else>
                  <v-list-tile>
                    <v-list-tile-content>Count:</v-list-tile-content>
                    <v-list-tile-content
                      class="align-end"
                    >{{ props.item.descriptiveStatistics.count }}</v-list-tile-content>
                  </v-list-tile>
                  <v-list-tile>
                    <v-list-tile-content>Unique:</v-list-tile-content>
                    <v-list-tile-content
                      class="align-end"
                    >{{ props.item.descriptiveStatistics.unique }}</v-list-tile-content>
                  </v-list-tile>
                </v-list>

                <v-divider/>
                
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
export default {
  data() {
    return {
      datasets: [],
      loadingDatasets: false,
      dataset: undefined,

      loadingDatasetDetails: false,
      datasetDetailsError: false,
      columns: []
    };
  },
  async created() {
    this.loadingDatasets = true;
    const response = await this.$http.get("/api/v1/datasets");
    this.datasets = response.data.map(t => t.name);
    this.loadingDatasets = false;
  },
  methods: {},
  watch: {
    dataset: async function() {
      try {
        this.loadingDatasetDetails = true;
        this.datasetDetailsError = false;
        const response = await this.$http.get(
          `/api/v1/dataset/statistics/${this.dataset}`
        );
        this.columns = response.data.columns;
      } catch {
        this.datasetDetailsError = true;
        this.columns = []
      } finally {
        this.loadingDatasetDetails = false;
      }
    }
  }
};
</script>

