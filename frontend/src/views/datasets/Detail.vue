<template>
  <dataset-table :dataset="dataset"/>
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
