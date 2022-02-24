<template>
  <div id="app">
    <TrafficChart :last_updated="last_updated" :data="data" :height="500" />
  </div>
</template>

<script>
import TrafficChart from "@/components/TrafficChart.vue";
import { rollup, sum } from "d3-array";
import { fetchData, fetchMetadata } from "@/utils";

export default {
  name: "App",
  components: {
    TrafficChart,
  },
  data() {
    return {
      data: null,
      last_updated: null,
    };
  },
  async created() {
    let meta = await fetchMetadata();
    this.last_updated = new Date(meta["committed_datetime"]);

    let data = await fetchData();
    let covid_traffic = Array.from(
      rollup(
        data,
        (v) => sum(v, (d) => d.covid_traffic),
        (d) => d.datetime
      ).entries()
    );
    let other_traffic = Array.from(
      rollup(
        data,
        (v) => sum(v, (d) => d.other_traffic),
        (d) => d.datetime
      ).entries()
    );

    this.data = { covid_traffic, other_traffic };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
