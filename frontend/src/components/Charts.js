import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Legend,
  Tooltip
} from "chart.js";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Legend,
  Tooltip
);

function Charts({ history }) {
  console.log("HISTORY DATA:", history);
  const data = {
    
    labels: history.map((d) => d.time || ""), // fallback if no time
    datasets: [
      {
        label: "Temperature",
        data: history.map((d) => d.temp),
        borderWidth: 2,
        borderColor: "red",  
        tension: 0.3,
      },
      {
        label: "Light",
        data: history.map((d) => d.light),
        borderWidth: 2,
        borderColor: "white",  
        tension: 0.3,
      },
      {
        label: "Sleep Score",
        data: history.map((d) => d.sleep_score),
        borderWidth: 4,           // 🔥 thicker line
        pointRadius: 3,
        borderColor: "blue",  
        tension: 0.3,
      },
      {
        label: "Sound",
        data: history.map((d) => d.sound),
        borderWidth: 4,           // 🔥 thicker line
        pointRadius: 3,
        borderColor: "green",  
        tension: 0.3,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false, // 🔥 allows custom height
    plugins: {
      legend: {
        labels: {
          font: {
            size: 14,
          },
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="card" style={{ height: "400px", width: "100%", padding: "20px" }}>
      <h3 style={{ marginBottom: "10px" }}>📊 Sleep Analytics</h3>

      <div style={{ height: "300px" }}>
        <Line data={data} options={options} />
      </div>
    </div>
  );
}

export default Charts;