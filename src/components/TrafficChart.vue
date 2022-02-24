<template>
  <div>
    <div class="title-wrapper">
      <h1 class="title">
        Hourly Traffic on Government Websites for COVID-19 Tests
      </h1>
      <h2>
        Last updated at
        <span v-if="last_updated">{{ formatTime(last_updated) }}</span>
      </h2>
      <hr class="my-hr" />
    </div>

    <div class="chart-wrapper">
      <!-- The chart -->
      <apexchart
        v-if="data !== null"
        :height="height"
        type="line"
        :series="series"
        :options="chartOptions"
      ></apexchart>
    </div>

    <div class="footnote">
      <div>
        <span class="bold">Note</span>: Traffic related to COVID-19 tests
        includes the following domains:
        <a href="https://www.COVIDtests.gov">COVIDtests.gov</a>
        and
        <a href="https://www.special.usps.com/testkits"
          >special.usps.com/testkits</a
        >
      </div>
      <div>
        <span class="bold">Source</span>:
        <a href="https://analytics.usa.gov">analytics.usa.gov</a>; scraped data
        available on
        <a href="https://github.com/nickhand/covid-tests-traffic">Github</a>
      </div>

      <div>Made by <a href="https://www.github.com/nickhand">@nickhand</a></div>
    </div>
  </div>
</template>

<script>
import { timeFormat } from "d3-time-format";
import { format } from "d3-format";
import VueApexCharts from "vue-apexcharts";

export default {
  name: "TrafficChart",
  props: ["last_updated", "data", "height"],
  components: { apexchart: VueApexCharts },
  methods: {
    formatTime(date) {
      let TZ = timeFormat("%Z")(date) == "-0500" ? "EST" : "EDT";
      const format1 = timeFormat("%I:%M %p");
      const format2 = timeFormat("%A, %B %-d, %Y");
      return `${format1(date)} ${TZ} on ${format2(date)}`;
    },
  },
  computed: {
    series() {
      if (!this.data) return [];
      return [
        {
          name: "All Other Domains",
          data: this.data.other_traffic,
        },
        {
          name: "COVID-19 Tests",
          data: this.data.covid_traffic,
        },
      ];
    },
    chartOptions() {
      return {
        grid: { padding: { left: 50, right: 50, top: 30 } },
        stroke: { width: 2.5, curve: "straight" },
        annotations: {
          xaxis: [
            {
              x: new Date().getTime(),
              strokeDashArray: 0,
              borderColor: "#000",
              label: {
                borderWidth: 0,
                style: {
                  fontSize: "18px",
                },
                text: "Now",
              },
            },
            {
              x: new Date("01/18/2022 12:00:00").getTime(),
              strokeDashArray: 0,
              borderColor: "#000",
              label: {
                borderWidth: 0,
                style: {
                  fontSize: "18px",
                },
                text: "Soft Launch",
              },
            },
          ],
        },
        chart: {
          animations: {
            enabled: false,
          },
        },
        tooltip: {
          x: {
            formatter(d) {
              let dt = new Date(d);
              const f = timeFormat("%b %-d %Y, %-I %p");
              return f(dt);
            },
          },
          style: {
            fontSize: "16px",
          },
        },
        colors: ["#a1a1a1", "#ff3b22"],
        xaxis: {
          type: "datetime",
          labels: {
            style: {
              fontSize: "16px",
            },
          },
        },
        yaxis: {
          labels: {
            show: true,
            style: {
              fontSize: "16px",
            },
            formatter: (val) => {
              return format(",.0f")(val);
            },
          },
        },
        legend: { position: "top", fontSize: "18px", offsetY: 40 },
        responsive: [
          {
            breakpoint: 768,
            options: {
              yaxis: {
                labels: {
                  show: false,
                },
              },
            },
          },
        ],
      };
    },
  },
};
</script>

<style>
h1 {
  font-size: 3rem;
  margin-bottom: 0rem;
}
h2 {
  font-size: 1.5rem;
  font-weight: 500;
  margin-top: 0rem;
}
.chart-wrapper {
  margin-top: 3rem;
}
.footnote {
  margin-top: 3rem;
  font-style: italic;
  font-size: 1.1rem;
  text-align: left;
}
.title {
  max-width: 1000px;
  text-align: center;
}
.title-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.my-hr {
  border-top: 1px solid #000;
  width: 80%;
}
.footnote div {
  margin-top: 0.5rem;
}
.bold {
  font-weight: 700;
}
</style>
