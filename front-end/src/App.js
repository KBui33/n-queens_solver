import "./App.css";
import WebSocketCall from "./components/WebSocketCall";
import Card from "./components/Card";
import axios from "axios";
import { io } from "socket.io-client";
import { useEffect, useState } from "react";

function App() {
  const [socketInstance, setSocketInstance] = useState("");
  // const [loading, setLoading] = useState(true);
  const [connecting, setConnecting] = useState(false);
  const [hand, setHand] = useState(null);
  const [numPlayers, setNumPlayers] = useState([]);
  const handleClick = () => {
    if (connecting === false) {
      setConnecting(true);
    } else {
      setConnecting(false);
    }
  };
  const highlight = (field, msg) => {
    field.className = "m-2 p-1 border-solid border-2 border-red";
    let m = document.createElement("p");
    m.setAttribute("id", `${field.getAttribute("id")}Msg`);
    m.innerHTML = msg;
    m.className = "text-red-600";
    field.parentElement.appendChild(m);
  };
  const removeHighlight = (field) => {
    field.className = "m-2 p-1 border-solid border-2 border-black";
    let m = document.getElementById(field.getAttribute("id") + "Msg");
    if (m === null) return;
    else m.remove();
  };

  const startGame = () => {
    // axios.get("/start_game").then((res) => {
    //   console.log(res);
    // });
    if (!socketInstance) {
      console.log("Please connect to the game first");
      return;
    }
    socketInstance.emit("start_game");
  };
  const check = () => {
    socketInstance.emit("check");
  };
  const raise = () => {
    let val = document.getElementById("raiseInput").value;
    console.log(val);
    if (val === "" || val === undefined || val === null || val <= 0) {
      alert("You must enter a numeric value >= 0");
      return;
    }
    socketInstance.emit("raise", val);
  };
  const fold = () => {
    socketInstance.emit("fold");
  };

  useEffect(() => {
    if (connecting === true) {
      /*
        Socket Function Definitions
      */
      const socket = io("localhost:5001/", {
        transports: ["websocket"],
        cors: {
          origin: "http://localhost:3000/",
        },
      });

      setSocketInstance(socket);

      socket.on("connect", (res) => {
        if (!res) return;
        // setNumPlayers(res.data.numPlayers);
      });

      // setLoading(false);

      socket.on("disconnect", (res) => {
        if (!res) return;
        setNumPlayers(res.data.numPlayers);
      });

      socket.on("output", (res) => {
        setHand(JSON.parse(res.cards));
      });

      socket.on("numPlayers", (res) => {
        setNumPlayers(res);
      });

      socket.on("notEnoughPlayers", (res) => {
        alert("Need at least 2 players to start the game");
      });

      /*
        User input logic
      */

      //make request asking for blind size

      let input = document.getElementById("wager"); /*eslint no-undef: "error"*/
      let name = document.getElementById("name"); /*eslint no-undef: "error"*/
      if (typeof input === "undefined") {
        //change wager's classname
        console.log("ERROR input not found");
        setConnecting(false);
        return;
      }
      if (typeof name === "undefined") {
        //change name's classname
        console.log("ERROR name not found");
        setConnecting(false);
        return;
      }
      let val = parseInt(input.value);
      if (val > 0) {
        axios.get("/blind").then((res) => {
          // setBlind(res);
          let data = res.data;
          if (data.error) {
            console.log("ERROR: game not initialized");
          }
          let blind = data.success;
          //if wager < blind, do not connect
          if (input.value < blind) {
            //highlight input value
            highlight(input, `must be bigger than ${blind}`);
            //change wager's className
            return;
          } else {
            //have this player join the game
            //remove highlight on all inputs
            removeHighlight(input);
            removeHighlight(name);
            let form = document.getElementById("form");
            form.className = "hidden";
            socket.emit("join", input.value, name.value);
            return;
          }
        });
      }
      if (val <= 0) {
        //highlight wager input
        highlight(input, `you must enter a value > 0`);
        setConnecting(false);
      }
      if (name.value == "") {
        //highlight name input
        highlight(name, `you must enter a name`);
        setConnecting(false);
      }

      return function cleanup() {
        socket.disconnect();
      };
    }
  }, [connecting]);

  return (
    <div className="App">
      <form id="form">
        <label htmlFor="wager" className="text-2xl text-black p-4">
          How much would you like to wager? Blind is $10
        </label>
        <input
          type="number"
          className="m-2 p-1 border-solid border-2 border-black"
          id="wager"
        ></input>
        <label htmlFor="name" className="text-2xl text-black p-4">
          What is your name?
        </label>
        <input
          type="text"
          className="m-2 p-1 border-solid border-2 border-black"
          id="name"
        ></input>
      </form>
      <div id="game">
        {connecting ? (
          <div>
            <p># of Players: {numPlayers}</p>
            {hand == null ? (
              <button onClick={startGame}>Start Game</button>
            ) : (
              <div></div>
            )}
            {hand != null ? (
              <div id="gameContent">
                <div id="river"></div>
                <div id="hand">
                  {hand.map((item) => {
                    return <Card key={JSON.stringify(item)} card={item} />;
                  })}
                </div>
                <button onClick={check}>Check</button>
                <form>
                  <input type="number" id="raiseInput"></input>
                  <button onClick={raise}>Raise</button>
                </form>
                <button onClick={fold}>Fold</button>
              </div>
            ) : (
              <div></div>
            )}
          </div>
        ) : (
          <button
            className="bg-slate-300 m-2 p-3 rounded"
            onClick={handleClick}
          >
            Connect to Game
          </button>
        )}
      </div>
      <div id="cardContent">
        {/* {connecting ? (
          hand.map(function (card, i) {
            return <Card card={card} key={i} />;
          })
        ) : (
          <div></div>
        )} */}
      </div>
    </div>
  );
}

export default App;
