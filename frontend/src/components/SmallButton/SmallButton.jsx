import "./SmallButton.css";

const SmallButton = ({ filled, description }) => {
  function onPressed() {
    alert("Botão pressionado");
  }

  return (
    <div className="small_button">
      <a
        onClick={() => onPressed()}
        className={filled ? "filled" : "transparent"}
      >
        {description}
      </a>
    </div>
  );
};

export default SmallButton;
