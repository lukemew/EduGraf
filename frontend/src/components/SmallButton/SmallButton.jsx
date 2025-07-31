import "./SmallButton.css";

const SmallButton = ({ filled, description, onClick }) => {
  return (
    <div className="small_button">
      <a
        onClick={() => onClick()}
        className={filled ? "filled" : "transparent"}
      >
        {description}
      </a>
    </div>
  );
};

export default SmallButton;
