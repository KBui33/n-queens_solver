import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [size, setSize] = useState(0);
  const [board, setBoard] = useState([[]]);
  const [rightWall, setRightWall] = useState([]);
  const [bottomWall, setBottomWall] = useState([]);

  useEffect(() => {
    setSize(5);
  }, []);

  useEffect(() => {
    console.log(`chaning board size to ${size}`);

    let board = [];
    for (var i = 0; i < size; i++) {
      let temp = [];
      for (var j = 0; j < size; j++) {
        temp.push(" ");
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
    console.log(`Setting wall for ${row}:${col}`);
    console.log(rightWall);
    console.log(bottomWall);

    if (e.target.className == "wall-right") {
      console.log("right wall clicked");
      let newArr = [...rightWall];
      newArr[row][col] = newArr[row][col] == 1 ? 0 : 1;
      setRightWall(newArr);
    } else if (e.target.className == "wall-bottom") {
      let newArr = [...bottomWall];
      newArr[row][col] = newArr[row][col] == 1 ? 0 : 1;
      setBottomWall(newArr);
    }
  };

  const getCombos = async () => {
    await axios
      .post("http://localhost:5000/combo", {
        rightWall: rightWall,
        bottomWall: bottomWall,
        n: parseInt(size),
      })
      .then((res) => {
        console.log(res);
        setBoard(res.data);
      })
      .catch((err) => alert("an error occured"));
  };

  return (
    <div className="App">
      <div className="gridbox">
        {board.map((items, row) => {
          return (
            <div className="row">
              {items.map((subItem, col) => {
                return (
                  <div className="tile">
                    {col !== items.length - 1 ? (
                      <div
                        key={`${row}:${col}`}
                        style={{
                          backgroundColor:
                            rightWall[row][col] == 1 ? "black" : "",
                        }}
                        className="wall-right"
                        onClick={(e) => setWall(e, row, col)}
                      />
                    ) : (
                      <div />
                    )}
                    {row !== items.length - 1 ? (
                      <div
                        style={{
                          backgroundColor:
                            bottomWall[row][col] == 1 ? "black" : "",
                        }}
                        className="wall-bottom"
                        onClick={(e) => setWall(e, row, col)}
                      />
                    ) : (
                      <div />
                    )}
                    {subItem}
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
