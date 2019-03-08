const store = {
  state: {
    allDatasets: [],
    filter: false,
    datasets: []
  },
  setAllDatasets(datasets) {
    while (this.state.allDatasets.length > 0) this.state.allDatasets.pop();

    datasets.forEach(dataset => this.state.allDatasets.push(dataset));

    if (!this.state.filter) {
      this.setDatasets(datasets);
    }
  },
  setDatasets(datasets) {
    while (this.state.datasets.length > 0) this.state.datasets.pop();

    datasets.forEach(dataset => this.state.datasets.push(dataset));
  },
  setFilter(filter) {
    this.state.filter = filter;
  }
};

export default store;
