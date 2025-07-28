import "./Button.css";

const Button = ({ link, description, filled }) => {
  return (
    <div className="button">
      <a className={filled ? "filled" : "transparent"} href={link}>
        {description}
      </a>
    </div>
  );
};

export default Button;
