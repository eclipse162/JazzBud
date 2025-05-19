import React from "react";
import styles from "../../artistDisplay/artistDisplay.module.css";

const InstrumentDropdown = ({ instruments, onSelect }) => {
  if (!instruments || instruments.length === 0) return null;

  return (
    <div className={styles.dropdownContainer} style={{ width: "150px" }}>
      {instruments.map((instrument) => (
        <div
          key={instrument.id}
          className={styles.dropdownItem}
          onClick={() => onSelect(instrument)}
          role="option"
          tabIndex={0}>
          {instrument.name}
        </div>
      ))}
    </div>
  );
};

export default InstrumentDropdown;
