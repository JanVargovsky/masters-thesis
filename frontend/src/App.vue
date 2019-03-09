<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" clipped fixed app>
      <v-list expand>
        <template v-for="item in items">
          <v-list-tile v-if="!item.items" :key="item.title" :to="item.link">
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          </v-list-tile>

          <v-list-group
            v-else
            :key="item.to"
            :prepend-icon="item.icon"
            no-action
          >
            <v-list-tile slot="activator">
              <v-list-tile-content>
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>

            <v-list-tile
              v-for="item in item.items"
              :key="item.to"
              :to="item.link"
            >
              <v-list-tile-action>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-tile-action>
              <v-list-tile-title>{{ item.title }}</v-list-tile-title>
            </v-list-tile>
          </v-list-group>
        </template>
      </v-list>
    </v-navigation-drawer>

    <v-toolbar color="primary" dark fixed clipped-left app>
      <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
      <router-link to="/">
        <v-icon class="ml-3">mdi-database-search</v-icon>
      </router-link>
      <v-toolbar-title> Dataset Analyser </v-toolbar-title>

      <v-spacer></v-spacer>

      <settings-modal />
    </v-toolbar>

    <v-content>
      <v-container fluid> <router-view></router-view> </v-container>
    </v-content>
  </v-app>
</template>

<script>
import SettingsModal from "./views/settings/SettingsModal";

export default {
  name: "App",
  components: {
    SettingsModal
  },
  data() {
    return {
      drawer: true,
      items: [
        { title: "Home", icon: "mdi-home", link: "/" },
        {
          title: "Datasets",
          icon: "mdi-database",
          items: [
            {
              title: "Upload",
              icon: "mdi-file-upload",
              link: "/datasets/upload"
            },
            {
              title: "Generate",
              icon: "mdi-database-plus",
              link: "/datasets/generate"
            },
            {
              title: "List",
              icon: "mdi-view-list",
              link: "/datasets/list"
            },
            {
              title: "Preprocessing",
              icon: "mdi-cogs",
              link: "/preprocessing"
            },
            {
              title: "Configurations",
              icon: "mdi-file-tree",
              link: "/datasets/configurations"
            },
            {
              title: "Statistics",
              icon: "mdi-chart-bar",
              link: "/statistics"
            }
          ]
        },
        {
          title: "Models",
          icon: "mdi-cube",
          items: [
            {
              title: "Create classification",
              icon: "mdi-shape-outline",
              link: "/models/create-classification"
            },
            {
              title: "Create clustering",
              icon: "mdi-chart-bubble",
              link: "/models/create-clustering"
            },
            { title: "List", icon: "mdi-view-list", link: "/models/list" }
          ]
        },
        // { title: "Experiments", icon: "mdi-view-list", link: "/experiments" },
        { title: "About", icon: "mdi-information", link: "/about" }
      ]
    };
  }
};
</script>
