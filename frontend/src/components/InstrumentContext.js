import React, { createContext, useContext, useState } from "react";

const InstrumentContext = createContext();

export const InstrumentProvider = ({ children }) => {
  const [selectedInstruments, setSelectedInstruments] = useState({});

  const handleInstrumentSelect = (artistId, instrument) => {
    setSelectedInstruments((prev) => {
      const currentInstruments = prev[artistId] || [];
      const newInstruments = Array.isArray(instrument)
        ? instrument
        : [instrument];
      const updatedInstruments = [...currentInstruments, ...newInstruments];

      // Use the updated state immediately
      console.log(
        `Updated instruments for artist ${artistId}:`,
        updatedInstruments
      );

      return {
        ...prev,
        [artistId]: updatedInstruments,
      };
    });
  };

  const removeInstrument = (artistId, instrumentId) => {
    setSelectedInstruments((prev) => ({
      ...prev,
      [artistId]: prev[artistId].filter((inst) => inst.id !== instrumentId),
    }));
  };

  const contextValue = React.useMemo(
    () => ({
      selectedInstruments,
      addInstrument: handleInstrumentSelect,
      removeInstrument,
    }),
    [selectedInstruments]
  );

  return (
    <InstrumentContext.Provider value={contextValue}>
      {children}
    </InstrumentContext.Provider>
  );
};

export const useInstrumentContext = () => {
  const context = useContext(InstrumentContext);
  if (!context) {
    throw new Error(
      "useInstrumentContext must be used within an InstrumentProvider"
    );
  }
  return context;
};
