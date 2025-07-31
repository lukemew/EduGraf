import "./select.css";

const Select = ({ value, onChange, type }) => {
  return (
    <div>
      <select
        value={value}
        onChange={onChange}
        className="select"
        name="Seleção de polos"
      >
        {type === "polo"
          ? Array.from({ length: 14 }, (_, i) => {
              const number = i + 1;
              const label =
                number === 14 ? `Polo ${number} (Geral)` : `Polo ${number}`;
              return (
                <option key={i + 1} value={`Polo ${i + 1}`}>
                  {label}
                </option>
              );
            })
          : Array.from({ length: 2 }, (_, i) => (
              <option key={i + 1} value={`${i + 1}`}>
                {i + 1}
              </option>
            ))}
      </select>
    </div>
  );
};

export default Select;
