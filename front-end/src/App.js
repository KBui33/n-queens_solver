import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [size, setSize] = useState(0);
  const [board, setBoard] = useState([[]]);
  const [rightWall, setRightWall] = useState([]);
  const [bottomWall, setBottomWall] = useState([]);
  const [clicked, setClicked] = useState(false);

  useEffect(() => {
    setSize(5);
  }, []);

  useEffect(() => {
    console.log(`chaning board size to ${size}`);

    let board = [];
    for (var i = 0; i < size; i++) {
      let temp = [];
      for (var j = 0; j < size; j++) {
        temp.push(0);
      }
      board.push(temp);
    }
    setBoard(board);

    // Init the rightWall Array
    board = [];
    for (var i = 0; i < size; i++) {
      let temp = [];
      for (var j = 0; j < size - 1; j++) {
        temp.push(0);
      }
      board.push(temp);
    }
    setRightWall(board);

    // Init the bottomWall Array
    board = [];
    for (var i = 0; i < size - 1; i++) {
      let temp = [];
      for (var j = 0; j < size; j++) {
        temp.push(0);
      }
      board.push(temp);
    }
    setBottomWall(board);
  }, [size]);

  // Makes sure that the input is an integer
  const test = (e) => {
    const re = /^[0-9\b]+$/;
    if (e.target.value === "" || re.test(e.target.value)) {
      setSize(e.target.value);
    }
  };

  const setWall = (e, row, col) => {
    console.log(`Setting all for ${row}:${col}`);
    setClicked((current) => !current);
    console.log(rightWall);
    console.log(bottomWall);

    if (e.target.className == "wall-right") {
      console.log("right wall clicked");
      rightWall[row][col] == 1
        ? (rightWall[row][col] = 0)
        : (rightWall[row][col] = 1);
    } else if (e.target.className == "wall-bottom") {
      bottomWall[row][col] == 1
        ? (bottomWall[row][col] = 0)
        : (bottomWall[row][col] = 1);
    }
  };

  const getCombos = async () => {
    await axios
      .get("/combo", { data: { rightWall, bottomWall } })
      .then((res) => {
        console.log(res);
      });
  };

  return (
    <div className="App">
      <div className="gridbox">
        {board.map((items, idx) => {
          return (
            <div className="row">
              {items.map((subItem, subIdx) => {
                return (
                  <div className="tile">
                    {subIdx !== items.length - 1 ? (
                      <div
                        key={`${idx}:${subIdx}`}
                        style={{
                          backgroundColor:
                            rightWall[idx][subIdx] == 1 ? "black" : "",
                        }}
                        className="wall-right"
                        onClick={(e) => setWall(e, idx, subIdx)}
                      />
                    ) : (
                      <div />
                    )}
                    {idx !== items.length - 1 ? (
                      <div
                        style={{
                          backgroundColor:
                            bottomWall[idx][subIdx] == 1 ? "black" : "",
                        }}
                        className="wall-bottom"
                        onClick={(e) => setWall(e, idx, subIdx)}
                      />
                    ) : (
                      <div />
                    )}
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>
      <div className="options">
        <input value={size} onChange={test}></input>
        <button className="start-btn" onClick={getCombos}>
          Get Combos
        </button>
      </div>
    </div>
  );
}

export default App;
