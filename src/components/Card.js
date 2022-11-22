import React from "react";

const spades = new Map([
  ["2", "🂢"],
  ["3", "🂣"],
  ["4", "🂤"],
  ["5", "🂥"],
  ["6", "🂦"],
  ["7", "🂧"],
  ["8", "🂨"],
  ["9", "🂩"],
  ["10", "🂪"],
  ["11", "🂫"],
  ["12", "🂭"],
  ["13", "🂮"],
  ["14", "🂡"],
]);

const clubs = new Map([
  ["2", "🃒"],
  ["3", "🃓"],
  ["4", "🃔"],
  ["5", "🃕"],
  ["6", "🃖"],
  ["7", "🃗"],
  ["8", "🃘"],
  ["9", "🃙"],
  ["10", "🃚"],
  ["11", "🃛"],
  ["12", "🃝"],
  ["13", "🃞"],
  ["14", "🃑"],
]);

const diamonds = new Map([
  ["2", "🃂"],
  ["3", "🃃"],
  ["4", "🃄"],
  ["5", "🃅"],
  ["6", "🃆"],
  ["7", "🃇"],
  ["8", "🃈"],
  ["9", "🃉"],
  ["10", "🃊"],
  ["11", "🃋"],
  ["12", "🃍"],
  ["13", "🃎"],
  ["14", "🃁"],
]);

const hearts = new Map([
  ["2", "🂲"],
  ["3", "🂳"],
  ["4", "🂴"],
  ["5", "🂵"],
  ["6", "🂶"],
  ["7", "🂷"],
  ["8", "🂸"],
  ["9", "🂹"],
  ["10", "🂺"],
  ["11", "🂻"],
  ["12", "🂽"],
  ["13", "🂾"],
  ["14", "🂱"],
]);

const CardBox = (props) => {
  let color = "";
  if (props.card.suit === "H" || props.card.suit === "D")
    color = "text-red-600";
  else color = "text-zinc-800";

  let curCard = "";
  if (props.card.suit === "S") {
    curCard = spades.get(props.card.value);
  } else if (props.card.suit === "C") {
    curCard = clubs.get(props.card.value);
  } else if (props.card.suit === "D") {
    curCard = diamonds.get(props.card.value);
  } else if (props.card.suit === "H") {
    curCard = hearts.get(props.card.value);
  } else {
    curCard = "";
    console.log("Error selecting suit");
  }
  return <div className={color}>{curCard}</div>;
};
const Card = (props) => {
  return (
    <div>
      <CardBox card={props.card} />
    </div>
  );
};

export default Card;
