<template>
  <v-card>
    <v-toolbar color="deep-purple" dark flat dense card>
      <v-toolbar-title class="subheading">Model - {{ model }}</v-toolbar-title>
    </v-toolbar>
    <v-card-text>
      <v-layout row wrap>
        <v-flex xs12 v-if="details">
          <v-list subheader two-line>
            <v-subheader>General</v-subheader>
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>Dataset</v-list-tile-title>
                <v-list-tile-sub-title v-text="details.dataset" />
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile v-if="details.configuration">
              <v-list-tile-content>
                <v-list-tile-title>Configuration</v-list-tile-title>
                <v-list-tile-sub-title v-text="details.configuration" />
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>Label</v-list-tile-title>
                <v-list-tile-sub-title v-text="details.label" />
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>Input dimension</v-list-tile-title>
                <v-list-tile-sub-title v-text="details.inputDimension" />
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>Output dimension</v-list-tile-title>
                <v-list-tile-sub-title v-text="details.outputDimension" />
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>Train score</v-list-tile-title>
                <v-list-tile-sub-title>
                  {{ (details.score * 100) | round(2) }}%
                </v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>

          <v-divider />

          <v-list subheader two-line>
            <v-subheader>Hyperparameters</v-subheader>
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>Epochs</v-list-tile-title>
                <v-list-tile-sub-title v-text="details.epochs" />
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile>
              <v-list-tile-content>
                <v-list-tile-title>Layers</v-list-tile-title>
                <v-list-tile-sub-title>
                  {{ details.layers.join(" ") }}
                </v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>

          <v-divider />

          <v-layout row wrap>
            <v-flex v-for="(plot, i) in details.plots" :key="i" xs12 md6 lg4>
              <v-img :src="'data:image/jpeg;base64,' + plot" />
            </v-flex>
          </v-layout>
        </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    model: String
  },
  data() {
    return {
      details: undefined,

      loading: false,
      error: false
    };
  },
  async created() {
    await this.fetchDetails();
  },
  methods: {
    async fetchDetails() {
      try {
        this.error = false;
        this.loading = true;
        const response = await this.$http.get(
          `/api/v1/classification/${this.model}`
        );
        this.details = response.data;
      } catch {
        this.error = true;
      } finally {
        this.loading = false;
      }
    }
  },
  filters: {
    round: function(value, accuracy) {
      return +value.toFixed(accuracy);
    }
  }
};
</script>
