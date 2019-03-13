<template>
  <v-layout row wrap>
    <v-flex xs12>
      <v-timeline align-top class="pt-0">
        <v-timeline-item
          v-for="(item, i) in items"
          :key="i"
          :color="item.color"
          :icon="item.icon"
          fill-dot
        >
          <v-card :color="item.color" dark>
            <v-card-title class="title">{{ item.title }}</v-card-title>
            <v-card-text class="white text--primary">
              <p>{{ item.description }}</p>
              <v-btn
                v-for="(link, i) in item.links"
                :key="i"
                :color="item.color"
                :to="link.to"
                class="ml-0"
                outline
                >{{ link.name }}</v-btn
              >
            </v-card-text>
          </v-card>
        </v-timeline-item>
      </v-timeline>
    </v-flex>
  </v-layout>
</template>

<script>
export default {
  data() {
    return {
      items: [
        {
          title: "Dataset",
          description:
            "We need a data to operate on. Upload a new dataset with your data.",
          color: "indigo",
          icon: "mdi-database",
          links: [
            {
              to: "/datasets/upload",
              name: "Upload"
            },
            {
              to: "/datasets/import",
              name: "Import"
            },
            {
              to: "/datasets/generate",
              name: "Generate"
            }
          ]
        },
        {
          title: "Preprocess",
          description:
            "We need a clean data, without any missing values or outlayers. Use preprocessing to remove those defects.",
          color: "red",
          icon: "mdi-cogs",
          links: [
            {
              to: "/preprocessing/modify",
              name: "Modify"
            },
            {
              to: "/preprocessing/split",
              name: "Split"
            }
          ]
        },
        {
          title: "Review statistics",
          description:
            "Review exploration data analysis of a dataset. Apply your preprocess configurations.",
          color: "green",
          icon: "mdi-chart-bar",
          links: [
            {
              to: "/statistics",
              name: "Statistics"
            }
          ]
        },
        {
          title: "Create model",
          description: "Create a model for your data.",
          color: "teal",
          icon: "mdi-cube-outline",
          links: [
            {
              to: "/models/create-classification",
              name: "Classification"
            }
          ]
        },
        {
          title: "Make predictions",
          description:
            "Test your model against an unseen data and see how accurate it is.",
          color: "purple",
          icon: "mdi-flask-outline",
          links: [
            {
              to: "/models/predict",
              name: "Predict"
            }
          ]
        }
      ]
    };
  }
};
</script>
