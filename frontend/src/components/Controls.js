import React from "react";
import { toggleSystem, setMode } from "../api/api";
import FeedbackSlider from "./FeedbackSlider";

function Controls() {
  return (
    <div className="card">
      <h3>Controls</h3>

      <button onClick={toggleSystem}>
        Toggle Power
      </button>

      <div>
        <button onClick={() => setMode("manual")}>
          Manual Mode
        </button>

        <button onClick={() => setMode("dynamic")}>
          Dynamic Mode
        </button>
      </div>

      <FeedbackSlider />
    </div>
  );
}

export default Controls;