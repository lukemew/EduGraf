import "./select.css";

const Select = ({ value }) => {
  return (
    <div>
      <select className="select" name="Seleção de polos">
        <option value="1">Polo 1</option>
        <option value="2">Polo 2</option>
        <option value="3">Polo 3</option>
        <option value="4">Polo 4</option>
        <option value="5">Polo 5</option>
        <option value="6">Polo 6</option>
        <option value="7">Polo 7</option>
        <option value="8">Polo 8</option>
        <option value="9">Polo 9</option>
        <option value="10">Polo 10</option>
        <option value="11">Polo 11</option>
        <option value="12">Polo 12</option>
        <option value="13">Polo 13</option>
        <option value="14">Polo 14 (Geral)</option>
      </select>
    </div>
  );
};

export default Select;
