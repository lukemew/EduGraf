import "./Button.css";

const Button = ({ link, description, filled, onClick }) => {
  return (
    <div className="button">
      <a
        onClick={onClick}
        className={filled ? "filled" : "transparent"}
        href={link}
      >
        {description}
      </a>
    </div>
  );
};

export default Button;
