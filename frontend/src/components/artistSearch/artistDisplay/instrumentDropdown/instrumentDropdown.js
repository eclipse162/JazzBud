import React from "react";

const InstrumentDropdown = ({ instruments, onSelect }) => {
  if (!instruments || instruments.length === 0) return null;

  return (
    <div className="dropdown-container-i">
      {instruments.map((instrument) => (
        <div
          key={instrument.id}
          className="dropdown-item-i"
          onClick={() => onSelect(instrument)}>
          {instrument.name}
        </div>
      ))}
    </div>
  );
};

export default InstrumentDropdown;
