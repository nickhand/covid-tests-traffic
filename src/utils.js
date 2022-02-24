import { csv, json } from "d3-fetch"
import { timeHour } from "d3-time";

function getDownloadURL(filename) {
  return `https://raw.githubusercontent.com/nickhand/covid-tests-traffic/main/processed/${filename}`;
}

async function fetchData() {

  let url = getDownloadURL("data-covid-tests-traffic.csv")
  
  try {

    const data = await csv(url, (d) => {
      return {
        covid_traffic: +d.covid_traffic,
        other_traffic: +d.other_traffic,
        datetime: timeHour.floor(new Date(d.datetime)).getTime()
      };
    });
    return data;
  } catch (e) {
    console.error(e);
  }
}

async function fetchMetadata() {

  let url = getDownloadURL("meta.json")
  try {
    const data = await json(url);
    return data
  } catch (e) {
    console.error(e);
  }
}

export { fetchData, fetchMetadata };