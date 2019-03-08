<template>
  <v-card>
    <v-toolbar color="primary" dark flat dense card>
      <v-toolbar-title class="subheading"
        >Select preprocessing type</v-toolbar-title
      >
    </v-toolbar>
    <v-card-text>
      <v-btn dark color="red" to="modify" append>Modify</v-btn>
      <v-btn dark color="amber darken-3" to="split" append>Split</v-btn>
    </v-card-text>
  </v-card>
</template>
