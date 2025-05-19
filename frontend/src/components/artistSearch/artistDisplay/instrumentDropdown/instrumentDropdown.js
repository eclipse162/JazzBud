import React from "react";
import PropTypes from "prop-types";
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

InstrumentDropdown.propTypes = {
  instruments: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
    })
  ).isRequired,
  artistId: PropTypes.number.isRequired, // Artist ID is required to associate instruments
};

export default InstrumentDropdown;
