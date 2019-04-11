<template>
  <v-data-table :headers="headers" :items="matrix" hide-actions no-data-text>
    <template slot="items" slot-scope="props">
      <tr>
        <td>{{ props.index }}</td>
        <td
          v-for="(item, index) in props.item"
          :key="String(props.item) + String(index) + String(item)"
          :class="toColor(item, props.index, index)"
        >
          <span> {{ item }} </span>
        </td>
      </tr>
    </template>
  </v-data-table>
</template>

<script>
export default {
  props: ["matrix"],
  methods: {
    toColor(value, row, col) {
      if (row === col) return "green accent-4";
      if (value !== 0) return "red lighten-1";
      return "";
    }
  },
  computed: {
    headers: function() {
      if (
        !this.matrix ||
        this.matrix.length === 0 ||
        this.matrix[0].length === 0
      )
        return [];

      return [
        {
          text: "",
          sortable: false
        },
        ...this.matrix[0].map((_, index) => ({
          text: index.toString(),
          sortable: false
        }))
      ];
    }
  }
};
</script>
