import "./SmallButton.css";

const SmallButton = ({ filled, description, onClick, disabled, isLoading }) => {
  return (
    <div className="small_button">
      <button
        onClick={onClick}
        className={filled ? "filled" : "transparent"}
        disabled={disabled || isLoading}
      >
        {isLoading ? (
          <>
            <span className="spinner"></span>
            Gerando...
          </>
        ) : (
          description
        )}
      </button>
    </div>
  );
};

export default SmallButton;
