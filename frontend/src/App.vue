<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" clipped fixed app>
      <v-list dense>
        <v-list-tile v-for="item in items" :key="item.to" :to="item.link">
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>

          <v-list-tile-content>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>

    <v-toolbar color="primary" dark fixed clipped-left app>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <v-icon class="ml-3">mdi-database-search</v-icon>
      <v-toolbar-title>Dataset Analyser</v-toolbar-title>
    </v-toolbar>

    <v-content>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      drawer: true,
      items: [
        { title: "Home", icon: "mdi-home", link: "/" },
        { title: "Datasets", icon: "mdi-database", link: "/datasets" },
        {
          title: "Preprocessing",
          icon: "mdi-settings-outline",
          link: "/preprocessing"
        },
        // { title: "Experiments", icon: "mdi-view-list", link: "/experiments" },
        {
          title: "Create model",
          icon: "mdi-cube-outline",
          link: "/create-model"
        },
        { title: "Models", icon: "mdi-cube", link: "/models" },
        { title: "About", icon: "mdi-information", link: "/about" }
      ]
    };
  }
};
</script>
