<template>
  <v-card>
    <v-toolbar color="indigo" dark flat dense card>
      <v-toolbar-title class="subheading">Datasets</v-toolbar-title>
    </v-toolbar>
    <v-card-text> <datasets-table /> </v-card-text>
  </v-card>
</template>

<script>
import DatasetsTable from "../../components/DatasetsTable";

export default {
  components: {
    DatasetsTable
  }
};
</script>
