import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from "chart.js";

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement);

function Charts({ history }) {
  const data = {
    labels: history.map((d) => d.time),
    datasets: [
      {
        label: "Temperature",
        data: history.map((d) => d.temp),
      },
      {
        label: "Light",
        data: history.map((d) => d.light),
      },
    ],
  };

  return (
    <div className="card">
      <h3>Live Graph</h3>
      <Line data={data} />
    </div> 
  );
}

export default Charts;