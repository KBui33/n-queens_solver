import "./MoveOptions.css";
import React from "react";

const MoveOptions = ({ check, raise, call, fold }) => {
  return (
    <div id="move-options">
      <button class="move-btn" role="button" onClick={check}>
        CHECK
      </button>
      <button class="move-btn" role="button" onClick={raise}>
        RAISE
      </button>
      <button class="move-btn" role="button" onClick={call}>
        CALL
      </button>
      <button class="move-btn" role="button" onClick={fold}>
        FOLD
      </button>
    </div>
  );
};

export default MoveOptions;
