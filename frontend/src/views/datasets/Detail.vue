<template>
  <v-card>
    <v-toolbar color="indigo" dark flat dense card>
      <v-toolbar-title class="subheading"
        >Dataset - {{ dataset }}</v-toolbar-title
      >
    </v-toolbar>
    <v-card-text> <dataset-table :dataset="dataset" /> </v-card-text>
  </v-card>
</template>

<script>
import DatasetTable from "../../components/DatasetTable";

export default {
  props: {
    dataset: String
  },
  components: {
    DatasetTable
  }
};
</script>
