import React, { createContext, useContext, useState } from "react";

const InstrumentContext = createContext();

export const InstrumentProvider = ({ children }) => {
  const [selectedInstruments, setSelectedInstruments] = useState({});

  const handleInstrumentSelect = (index, instrument) => {
    setSelectedInstruments((prev) => {
      const currentInstruments = prev[index] || [];
      const newInstruments = Array.isArray(instrument)
        ? instrument
        : [instrument];
      const updatedInstruments = [...currentInstruments, ...newInstruments];

      // Use the updated state immediately
      console.log(
        `Updated instruments for artist ${index}:`,
        updatedInstruments
      );

      return {
        ...prev,
        [index]: updatedInstruments,
      };
    });
  };

  const removeInstrument = (index, instrumentId) => {
    setSelectedInstruments((prev) => ({
      ...prev,
      [index]: prev[index].filter((inst) => inst.id !== instrumentId),
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
