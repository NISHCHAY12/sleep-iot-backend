import React, { useState } from "react";
import { sendFeedback } from "../api/api";

function FeedbackSlider() {
  const [value, setValue] = useState(0);

  const handleChange = (e) => {
    const val = Number(e.target.value);
    setValue(val);
    sendFeedback(val);
  };

  return (
    <div>
      <h4>Feedback: {value}</h4>
      <input
        type="range"
        min="-5"
        max="5"
        value={value}
        onChange={handleChange}
      />
    </div>
  );
}

export default FeedbackSlider;