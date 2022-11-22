import logo from "./logo.svg";
import { useState, useEffect, useRef } from "react";
import Card from "./components/Card";
import axios from "axios";
import "./App.css";

function App() {
  const [curCards, setCurCards] = useState([{ value: "0", suit: "test" }]);
  const [inGame, setInGame] = useState(false);
  useEffect(() => {
    axios.get("/init").then((res) => console.log(res));
    if (!inGame) {
      axios.post("/leave_game/CDickie").then((res) => {
        console.log(res.data["success"]);
      });
    } else {
      axios.get("/init_cards").then((res) => {
        if (res.data["error"]) {
          console.log("cards already initialized");
        }
        axios.post("/join_game/CDickie").then((res) => {
          if (!res.data["success"]) {
            console.log("error joining game");
            return "";
          }
          axios.post("/draw/CDickie").then((res) => {
            if (!res.data["success"]) {
              console.log("error drawing hand");
              return "";
            }
            let cardList = JSON.parse(res.data["success"]);
            setCurCards(cardList);
          });
        });
      });
    }
  }, [inGame]);
  return (
    <div>
      <div>
        {((inGame && curCards) || []).map((item) => (
          <Card key={JSON.stringify(item)} card={item} />
        ))}
      </div>
      <button
        onClick={() => {
          setInGame(!inGame);
        }}
      >
        Join/Leave Game
      </button>
    </div>
  );
}

export default App;
