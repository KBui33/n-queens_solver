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
  const [scores, setScores] = useState([]);
  const [curPlayer, setCurplayer] = useState([]);

  const [start, setStart] = useState(false);

  const [playerStatus, setPlayerStatus] = useState("");
  const [playerName, setPlayerName] = useState("");

  /**
   *  When the player does the following:
   *  raise - Raise the amount and next person goes
   *  call - Make the bet equal to last person and next person goes
   *  fold - Throw away the cards and next person goes
   *  check - Go to next player turn (tell the socket to go next)
   */

  // const highlight = (field, msg) => {
  //   field.className = "m-2 p-1 border-solid border-2 border-red";
  //   let m = document.createElement("p");
  //   m.setAttribute("id", `${field.getAttribute("id")}Msg`);
  //   m.innerHTML = msg;
  //   m.className = "text-red-600";
  //   field.parentElement.appendChild(m);
  // };
  // const removeHighlight = (field) => {
  //   field.className = "m-2 p-1 border-solid border-2 border-black";
  //   let m = document.getElementById(field.getAttribute("id") + "Msg");
  //   if (m === null) return;
  //   else m.remove();
  // };

  const check = () => {
    socketInstance.emit("check");
  };

  const fold = () => {
    socketInstance.emit("fold");
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

  const blindAmount = () => {
    socketInstance.emit("blind", {});
  };

  // Set the player ready status
  useEffect(() => {
    console.log(playerStatus);
    if (socketInstance) {
      socketInstance.emit("ready_player", { playerName, status: playerStatus });
    }
  }, [playerStatus]);

  useEffect(() => {
    //highlight the current player in the list of players
    //unhighlight all other players
    //if it is not you, then make the buttons be deactivated
    //if it is you, then make buttons be activated
  }, [curPlayer]);

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
        socket.emit("set_name", playerName, (res) => {
          if (!res) return;
        });
      });

      socket.on("num_players", (res) => {
        console.log(res);
        setNumPlayers(res.data.numPlayers);
        if (!res) return;
        // setNumPlayers(res.data.numPlayers);
      });

      socket.on("disconnect", (res) => {
        if (!res) return;
        setNumPlayers(res.data.numPlayers);
        let name = res.data.name;
        alert(`${name} has been disconnected`);
        if (res.data.numPlayers < 2) {
          alert(`# of players is now less than 2. Ending the game`);
        }
      });

      socket.on("output", (res) => {
        setHand(JSON.parse(res.cards));
      });

      socket.on("notEnoughPlayers", (res) => {
        alert("Need at least 2 players to start the game");
      });

      socket.on("scoreboard", (data) => {
        //manage what the current scoreboard UI is
        let p = [];
        let pStrings = data.replaceAll("[", "").replaceAll("]", "").split(";");
        for (let i = 0; i < pStrings.length; i++) {
          p.push(JSON.parse(pStrings[i]));
        }
        //format and output scoreboard
        setScores(p);
        return;
      });

      socket.on("curPlayer", (res) => {
        //highlight on the scoreboard whichever player's turn it is
        setCurplayer(res.data.turn);
      });

      socket.on("game_start_status", (res) => {
        console.log(res);

        if (res.start) {
          // Change the view
          setStart((current) => !current);
        } else {
          console.log(res.start);
          alert(res.msg);
        }
      });

      socket.on("blind", (res) => {
        console.log(res);
      });

      /*
        User input logic
      */

      //make request asking for blind size

      // let input = document.getElementById("wager"); /*eslint no-undef: "error"*/
      // let name = document.getElementById("name"); /*eslint no-undef: "error"*/
      // if (typeof input === "undefined") {
      //   //change wager's classname
      //   console.log("ERROR input not found");
      //   setConnecting(false);
      //   return;
      // }
      // if (typeof name === "undefined") {
      //   //change name's classname
      //   console.log("ERROR name not found");
      //   setConnecting(false);
      //   return;
      // }
      // let val = parseInt(input.value);
      // if (val > 0) {
      //   axios.get("/blind").then((res) => {
      //     // setBlind(res);
      //     let data = res.data;
      //     if (data.error) {
      //       console.log("ERROR: game not initialized");
      //     }
      //     let blind = data.success;
      //     //if wager < blind, do not connect
      //     if (input.value < blind) {
      //       //highlight input value
      //       highlight(input, `must be bigger than ${blind}`);
      //       //change wager's className
      //       return;
      //     } else {
      //       //have this player join the game
      //       //remove highlight on all inputs
      //       removeHighlight(input);
      //       removeHighlight(name);
      //       let form = document.getElementById("form");
      //       form.className = "hidden";
      //       socket.emit("join", input.value, name.value);
      //       return;
      //     }
      //   });
      // }

      // if (val <= 0) {
      //   //highlight wager input
      //   highlight(input, `you must enter a value > 0`);
      //   setConnecting(false);
      // }
      // if (name.value == "") {
      //   //highlight name input
      //   highlight(name, `you must enter a name`);
      //   setConnecting(false);
      // }

      return function cleanup() {
        socket.disconnect();
      };
    }
  }, [connecting]);

  // Need to add some text to say that not all players are ready
  // Game starts and view changes
  return (
    <div className="App">
      {start ? (
        hand != null ? (
          <div id="gameContent">
            <div>Starting game</div>
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
        )
      ) : (
        <div id="game">
          {connecting ? (
            <div>
              <p># of Players: {numPlayers}</p>
              <button
                className={playerStatus ? "ready" : "not-ready"}
                onClick={() => setPlayerStatus((current) => !current)}
              >
                Ready
              </button>
            </div>
          ) : (
            <div id="join">
              <input
                style={{ border: "solid black" }}
                value={playerName}
                onChange={(e) => setPlayerName(e.target.value)}
              />
              <button onClick={() => setConnecting((current) => !current)}>
                Connect to Game
              </button>
            </div>
          )}
        </div>
      )}

      {/* <form id="form">
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
      </form> */}
    </div>
  );
}

export default App;
