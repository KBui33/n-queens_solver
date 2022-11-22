import logo from "./logo.svg";
import { useState, useEffect } from "react";
import Card from "./components/Card";
import axios from "axios";
import "./App.css";

function App() {
  const [curCards, setCurCards] = useState([{ value: "0", suit: "test" }]);
  useEffect(() => {
    axios.get("/init_cards").then((res) => {
      let cardList = JSON.parse(res.data["cards"]);
      setCurCards(cardList);
    });
  }, []);
  return (
    <div>
      {(curCards || []).map((item) => (
        <Card key={JSON.stringify(item)} card={item} />
      ))}
    </div>
  );
}

export default App;
