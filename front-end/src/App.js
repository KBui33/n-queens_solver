import React, { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [size, setSize] = useState(0);
  const [board, setBoard] = useState([[]]);

  const gridbox = {
    width: 50 * size,
  };

  useEffect(() => {
    setSize(5);
  }, []);

  useEffect(() => {
    console.log(`chaning board size to ${size}`);

    let board = [];
    for (var i = 1; i <= size; i++) {
      let temp = [];
      for (var j = 1; j <= size; j++) {
        temp.push(0);
      }
      board.push(temp);
    }
    setBoard(board);
  }, [size]);

  const test = (e) => {
    const re = /^[0-9\b]+$/;
    if (e.target.value === "" || re.test(e.target.value)) {
      setSize(e.target.value);
    }
  };

  return (
    <div className="App">
      <div>
        {board.map((items, idx) => {
          return (
            <div className="row">
              {items.map((subItem, subIdx) => {
                return <div className="tile"></div>;
              })}
            </div>
          );
        })}
      </div>
      <div className="options">
        <input value={size} onChange={test}></input>
        <button className="start-btn">Get Combos</button>
      </div>
    </div>
  );
}

export default App;
