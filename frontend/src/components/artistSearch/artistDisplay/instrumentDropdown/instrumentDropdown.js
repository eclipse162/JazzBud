import React from "react";
import PropTypes from "prop-types";
import { useInstrumentContext } from "../../../../components/InstrumentContext";
import styles from "../../artistDisplay/artistDisplay.module.css";

const InstrumentDropdown = ({ instruments, artistId }) => {
  const { addInstrument } = useInstrumentContext();

  if (!instruments || instruments.length === 0) return null;

  const handleSelect = (instrument) => {
    addInstrument(artistId, instrument); // Add the instrument to the context
  };

  return (
    <div className={styles.dropdownContainer} style={{ width: "150px" }}>
      {instruments.map((instrument) => (
        <div
          key={instrument.id}
          className={styles.dropdownItem}
          onClick={() => handleSelect(instrument)}
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
