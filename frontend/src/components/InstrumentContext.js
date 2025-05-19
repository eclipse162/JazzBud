import React, { createContext, useContext, useState } from "react";

const InstrumentContext = createContext();

export const InstrumentProvider = ({ children }) => {
  const [selectedInstruments, setSelectedInstruments] = useState({});

  const addInstrument = (artistId, instrument) => {
    setSelectedInstruments((prev) => {
      const currentInstruments = prev[artistId] || [];
      const newInstruments = Array.isArray(instrument)
        ? instrument
        : [instrument];
      return {
        ...prev,
        [artistId]: [...currentInstruments, ...newInstruments], // Flatten the array
      };
    });
  };

  const removeInstrument = (artistId, instrumentId) => {
    setSelectedInstruments((prev) => ({
      ...prev,
      [artistId]: prev[artistId].filter((inst) => inst.id !== instrumentId),
    }));
  };

  return (
    <InstrumentContext.Provider
      value={{ selectedInstruments, addInstrument, removeInstrument }}>
      {children}
    </InstrumentContext.Provider>
  );
};

export const useInstrumentContext = () => useContext(InstrumentContext);
