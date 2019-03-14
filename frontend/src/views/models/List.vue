<template>
  <v-card>
    <v-toolbar color="deep-purple" dark flat dense card>
      <v-toolbar-title class="subheading">Models</v-toolbar-title>
    </v-toolbar>
    <v-card-text>
      <v-form>
        <v-layout row wrap>
          <v-flex xs12>
            <v-data-table
              :items="models"
              :loading="loadingModels"
              :rows-per-page-items="[10, 25, 50, 100]"
              hide-headers
            >
              <template slot="items" slot-scope="props">
                <tr>
                  <td class="shrink pr-0">
                    <v-tooltip top>
                      <v-icon slot="activator">mdi-shape-outline</v-icon>
                      <span>Classification</span>
                    </v-tooltip>
                  </td>
                  <td>{{ props.item }}</td>
                  <td class="shrink">
                    <v-tooltip top>
                      <v-btn
                        slot="activator"
                        fab
                        icon
                        small
                        class="ma-0"
                        :to="'/models/' + props.item"
                      >
                        <v-icon>mdi-file-find</v-icon>
                      </v-btn>
                      <span>Open</span>
                    </v-tooltip>
                    <v-tooltip top>
                      <v-btn
                        slot="activator"
                        fab
                        icon
                        small
                        class="ma-0"
                        @click="deleteModel(props.item)"
                      >
                        <v-icon>mdi-delete</v-icon>
                      </v-btn>
                      <span>Delete</span>
                    </v-tooltip>
                  </td>
                </tr>
              </template>
            </v-data-table>
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
      models: [],
      loadingModels: false,

      error: false
    };
  },
  async created() {
    await this.fetchModels();
  },
  methods: {
    async fetchModels() {
      try {
        this.error = false;
        this.loadingModels = true;
        const response = await this.$http.get(`/api/v1/classification`);
        this.models = response.data;
      } catch {
        this.error = true;
      } finally {
        this.loadingModels = false;
      }
    },
    async deleteModel(name) {
      if (confirm(`Are you sure you want to delete ${name}?`)) {
        try {
          await this.$http.delete(`/api/v1/classification/${name}`);
          this.models = this.models.filter(t => t !== name);
        } catch (error) {
          this.error = true;
        }
      }
    }
  }
};
</script>
