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
  const [playerName, setPlayerName] = useState("");
  const [playerStatus, setPlayerStatus] = useState(false);

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

  // Set the player ready status
  useEffect(() => {
    console.log(playerStatus);
    if (socketInstance) {
      socketInstance.emit("ready_player", { playerName, status: playerStatus });
    }
  }, [playerStatus]);

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
        socket.emit("set_name", playerName, (res) => {
          if (!res) return;
        });
      });

      socket.on("num_players", (res) => {
        console.log(res);
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
            <button
              className={playerStatus ? "ready" : "not-ready"}
              onClick={() => setPlayerStatus((current) => !current)}
            >
              Ready
            </button>
            {hand != null ? (
              <div>
                {hand.map((item) => {
                  return <Card key={JSON.stringify(item)} card={item} />;
                })}
              </div>
            ) : (
              <div></div>
            )}
          </div>
        ) : (
          <div id="join">
            <input
              style={{ border: "solid black" }}
              value={playerName}
              onChange={(e) => setPlayerName(e.target.value)}
            />
            <button onClick={handleClick}>Connect to Game</button>
          </div>
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
