<template>
  <v-card>
    <v-toolbar color="indigo" dark flat dense card>
      <v-toolbar-title class="subheading">Generate dataset</v-toolbar-title>
    </v-toolbar>
    <v-card-text>
      <v-layout row wrap>
        <v-flex xs12>
          <v-subheader class="pa-0">Dataset type</v-subheader>
          <v-overflow-btn
            v-model="typeName"
            :items="typeNames"
            label="Select dataset type"
            editable
            class="pt-0 mt-0"
          ></v-overflow-btn>
        </v-flex>
        <template v-if="typeName == 'Classification'">
          <v-flex xs12>
            <v-text-field
              v-model="type.params.rows"
              type="number"
              label="Number of rows"
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="type.params.features"
              type="number"
              label="Number of features"
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="type.params.classes"
              type="number"
              label="Number of classes"
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="type.params.informative"
              type="number"
              label="Number of informative features"
            />
          </v-flex>
        </template>
        <template v-else-if="typeName == 'Blobs'">
          <v-flex xs12>
            <v-text-field
              v-model="type.params.rows"
              type="number"
              label="Number of rows"
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="type.params.features"
              type="number"
              label="Number of features"
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="type.params.classes"
              type="number"
              label="Number of classes"
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="type.params.clusterStd"
              type="number"
              label="Standard deviation of each cluster"
            />
          </v-flex>
        </template>
        <template v-else-if="typeName == 'Circles' || typeName == 'Moons'">
          <v-flex xs12>
            <v-text-field
              v-model="type.params.rows"
              type="number"
              label="Number of rows"
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="type.params.noise"
              type="number"
              label="Noise"
            />
          </v-flex>
        </template>
        <template v-else-if="typeName == 'Gaussian quantiles'">
          <v-flex xs12>
            <v-text-field
              v-model="type.params.rows"
              type="number"
              label="Number of rows"
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="type.params.features"
              type="number"
              label="Number of features"
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="type.params.classes"
              type="number"
              label="Number of classes"
            />
          </v-flex>
        </template>
        <template v-else-if="typeName == 'S curve' || typeName == 'Swiss roll'">
          <v-flex xs12>
            <v-text-field
              v-model="type.params.rows"
              type="number"
              label="Number of rows"
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="type.params.noise"
              type="number"
              label="Noise"
            />
          </v-flex>
          <v-flex xs12>
            <v-text-field
              v-model="type.params.classes"
              type="number"
              label="Number of classes"
              hint="Leave 0 for continuous class (regression)"
              persistent-hint
            />
          </v-flex>
        </template>
        <v-flex xs12 v-if="typeName">
          <v-flex xs12>
            <v-text-field
              v-model="type.datasetName"
              label="Name of generated dataset"
            />
          </v-flex>
        </v-flex>
        <v-flex xs12 v-if="type">
          <v-layout>
            <v-btn @click="preview" :loading="previewLoading" color="green" dark
              >Preview</v-btn
            >
            <v-btn
              @click="save"
              :loading="saveLoading"
              :disabled="!isValidDatasetName"
              color="primary"
              >Save</v-btn
            >
          </v-layout>
        </v-flex>
        <v-flex xs12>
          <v-alert :value="error" type="error" transition="scale-transition"
            >Server error.</v-alert
          >
          <v-alert
            :value="type && type.preview.plot"
            type="info"
            transition="scale-transition"
            >Don't like it? <strong>Try it once more.</strong> Preview generates
            <strong>always new</strong> dataset.
          </v-alert>
          <v-alert
            :value="highDimension"
            type="info"
            transition="scale-transition"
            >Preview shows only first 3 features.</v-alert
          >
          <v-alert
            :value="createdDataset"
            type="success"
            transition="scale-transition"
            >Dataset <strong>{{ createdDataset }}</strong> has been successfully
            created.</v-alert
          >
        </v-flex>
        <v-flex xs12 md9 lg6 v-if="type && type.preview.plot">
          <v-img :src="'data:image/jpeg;base64,' + type.preview.plot" />
        </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>
</template>

<script>
import { isDatasetNameValid } from "@/infrastructure/dataset";

export default {
  data() {
    return {
      typeName: undefined,
      types: {
        classification: {
          name: "Classification",
          url: "classification",
          preview: {
            randomState: undefined,
            plot: undefined,
            data: undefined
          },
          datasetName: undefined,
          params: {
            rows: 200,
            classes: 2,
            features: 2,
            informative: 2
          }
        },
        blobs: {
          name: "Blobs",
          url: "blobs",
          preview: {
            randomState: undefined,
            plot: undefined,
            data: undefined
          },
          datasetName: undefined,
          params: {
            rows: 200,
            features: 2,
            classes: 2,
            clusterStd: 0.08
          }
        },
        circles: {
          name: "Circles",
          url: "circles",
          preview: {
            randomState: undefined,
            plot: undefined,
            data: undefined
          },
          datasetName: undefined,
          params: {
            rows: 200,
            noise: 0.03
          }
        },
        moons: {
          name: "Moons",
          url: "moons",
          preview: {
            randomState: undefined,
            plot: undefined,
            data: undefined
          },
          datasetName: undefined,
          params: {
            rows: 200,
            noise: 0.1
          }
        },
        gaussianQuantiles: {
          name: "Gaussian quantiles",
          url: "gaussian-quantiles",
          preview: {
            randomState: undefined,
            plot: undefined,
            data: undefined
          },
          datasetName: undefined,
          params: {
            rows: 200,
            features: 2,
            classes: 2
          }
        },
        sCurve: {
          name: "S curve",
          url: "s-curve",
          preview: {
            randomState: undefined,
            plot: undefined,
            data: undefined
          },
          datasetName: undefined,
          params: {
            rows: 10000,
            noise: 0.01,
            classes: 3
          }
        },
        swissRoll: {
          name: "Swiss roll",
          url: "swiss-roll",
          preview: {
            randomState: undefined,
            plot: undefined,
            data: undefined
          },
          datasetName: undefined,
          params: {
            rows: 10000,
            noise: 0.01,
            classes: 3
          }
        }
      },

      previewLoading: false,
      highDimension: false,
      saveLoading: false,
      error: false,
      createdDataset: undefined
    };
  },
  methods: {
    async preview() {
      try {
        this.previewLoading = true;
        this.error = false;
        if (!this.highDimension) this.highDimension = false;
        const payload = this.getPayload(false);
        const response = await this.$http.post(
          `/api/v1/dataset-generator/${this.type.url}`,
          payload
        );
        this.highDimension = this.type.features && this.type.features > 3;
        const data = response.data;
        this.type.preview.randomState = data.randomState;
        this.type.preview.plot = data.plot;
      } catch (ex) {
        this.error = true;
      }
      this.previewLoading = false;
    },
    async save() {
      try {
        this.saveLoading = true;
        this.error = false;
        this.createdDataset = undefined;
        const payload = this.getPayload(true);
        await this.$http.put(
          `/api/v1/dataset-generator/${this.type.url}`,
          payload
        );
        this.createdDataset = payload.datasetName;
      } catch (ex) {
        this.error = true;
      }
      this.saveLoading = false;
    },
    getPayload(isSave) {
      const payload = { ...this.type.params };
      Object.keys(payload).map(t => (payload[t] = parseFloat(payload[t])));
      if (isSave) {
        payload.datasetName = this.type.datasetName;
        if (this.type.preview && this.type.preview.randomState)
          payload.randomState = this.type.preview.randomState;
      }
      return payload;
    }
  },
  watch: {
    type: {
      handler() {
        this.error = false;
        this.createdDataset = undefined;
      },
      deep: true
    }
  },
  computed: {
    typeNames: function() {
      return Object.values(this.types).map(t => t.name);
    },
    type: function() {
      return Object.values(this.types).find(t => t.name == this.typeName);
    },
    isValidDatasetName: function() {
      if (!this.type) return false;
      if (!isDatasetNameValid(this.type.datasetName)) return false;
      return true;
    }
  }
};
</script>
