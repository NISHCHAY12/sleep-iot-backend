import React, { useEffect, useState } from "react";
import { getStatus } from "../api/api";
import Controls from "./Controls";
import Charts from "./Charts";

function Dashboard() {
  const [data, setData] = useState({});
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      getStatus().then((res) => {
        const d = res.data;
        setData(d);

        setHistory((prev) => [
          ...prev.slice(-20),
          {
            time: new Date().toLocaleTimeString(),
            temp: d.temp || 0,
            light: d.light || 0,
            sleep_score: d.sleep_score || 0,
            sound: d.sound || 0,
          },
        ]);
      });
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard">

      <Controls />

      <div className="card">
        <h3>System Status</h3>
        <p>Power: {data.power ? "ON" : "OFF"}</p>
        <p>Mode: {data.mode}</p>
        <p>Sleep Score: {data.sleep_score || "--"}</p>
      </div>

      <div className="card">
        <h3>Live Sensor Data</h3>
        <p>Temp: {data.temp}</p>
        <p>Light: {data.light}</p>
        <p>Humidity: {data.humidity}</p>
        <p>Air: {data.air}</p>
      </div>

      <Charts history={history} />

    </div>
  );
}

export default Dashboard;