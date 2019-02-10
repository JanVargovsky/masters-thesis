<template>
  <v-card>
    <v-toolbar color="indigo" dark flat dense card>
      <v-toolbar-title class="subheading">Jobs</v-toolbar-title>
    </v-toolbar>
    <v-card-text>
      <v-layout row wrap>
        <v-flex xs12>
          <v-badge color="blue" v-model="newJobsCount" overlap class="ma-3">
            <span slot="badge">{{ newJobsCount }}</span>
            <v-checkbox v-model="showNew" color="blue" label="New"/>
          </v-badge>
          <v-badge color="orange" v-model="inProgressJobsCount" overlap>
            <span slot="badge">{{ inProgressJobsCount }}</span>
            <v-checkbox v-model="showInProgress" color="orange" label="In progress"/>
          </v-badge>
          <v-badge color="green" v-model="doneJobsCount" overlap>
            <span slot="badge">{{ doneJobsCount }}</span>
            <v-checkbox v-model="showDone" color="green" label="Done"/>
          </v-badge>
          <v-badge color="red" v-model="failedJobsCount" overlap>
            <span slot="badge">{{ failedJobsCount }}</span>
            <v-checkbox v-model="showFailed" color="red" label="Failed"/>
          </v-badge>
        </v-flex>

        <v-flex xs12>
          <v-data-table :headers="headers" :items="selectedItems">
            <template slot="items" slot-scope="props">
              <td>{{ props.item.name}}</td>
              <td>{{ props.item.state}}</td>
              <td>
                <v-icon>mdi-play</v-icon>
              </td>
            </template>
          </v-data-table>
        </v-flex>
      </v-layout>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      jobs: [],

      showNew: true,
      showInProgress: true,
      showDone: true,
      showFailed: true
    };
  },
  created() {
    this.jobs = [
      {
        name: "job1",
        state: "new"
      },
      {
        name: "job2",
        state: "new"
      },
      {
        name: "job3",
        state: "in progress"
      },
      {
        name: "job4",
        state: "done"
      },
      {
        name: "job5",
        state: "done"
      },
      {
        name: "job6",
        state: "done"
      },
      {
        name: "job7",
        state: "failed"
      },
      {
        name: "job8",
        state: "failed"
      }
    ];
  },
  methods: {
    filterJobs(states) {
      if (!Array.isArray(states)) states = [states];
      return this.jobs.filter(job => states.some(state => job.state == state));
    }
  },
  computed: {
    newJobsCount: function() {
      return this.filterJobs("new").length;
    },
    inProgressJobsCount: function() {
      return this.filterJobs("in progress").length;
    },
    doneJobsCount: function() {
      return this.filterJobs("done").length;
    },
    failedJobsCount: function() {
      return this.filterJobs("failed").length;
    },
    selectedItems: function() {
      const states = [
        this.showNew && "new",
        this.showInProgress && "in progress",
        this.showDone && "done",
        this.showFailed && "failed"
      ];
      console.log(states);
      return this.filterJobs(states);
    }
  }
};
</script>
