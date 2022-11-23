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

  const startGame = () => {
    // axios.get("/start_game").then((res) => {
    //   console.log(res);
    // });
    if (!socketInstance) {
      console.log("Please connect to the game first");
      return;
    }
    socketInstance.emit("start_game", "");
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
      const socket = io("localhost:5001/", {
        transports: ["websocket"],
        cors: {
          origin: "http://localhost:3000/",
        },
      });

      setSocketInstance(socket);

      socket.on("connect", (res) => {
        if (!res) return;
        setNumPlayers(res.data.numPlayers);
      });

      // setLoading(false);

      socket.on("disconnect", (res) => {
        if (!res) return;
        setNumPlayers(res.data.numPlayers);
      });

      socket.on("output", (res) => {
        setHand(JSON.parse(res.cards));
        console.log(JSON.parse(res.cards));
      });

      return function cleanup() {
        socket.disconnect();
      };
    }
  }, [connecting]);

  return (
    <div className="App">
      <p className="text-2xl text-red-600">
        Hello I am a flask-react-socketio-app
      </p>
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
          <button onClick={handleClick}>Connect to Game</button>
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
