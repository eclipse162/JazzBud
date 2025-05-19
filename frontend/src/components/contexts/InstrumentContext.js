import React, { createContext, useContext, useState, useMemo } from "react";

const InstrumentContext = createContext();

export const InstrumentProvider = ({ children }) => {
  const [selectedInstruments, setSelectedInstruments] = useState({});

  const handleInstrumentSelect = (index, instrument) => {
    setSelectedInstruments((prev) => {
      const currentInstruments = prev[index] ? [...prev[index]] : [];
      const newInstruments = Array.isArray(instrument)
        ? instrument
        : [instrument];

      const updatedInstruments = [
        ...currentInstruments,
        ...newInstruments.filter(
          (newInst) =>
            !currentInstruments.some((inst) => inst.id === newInst.id)
        ),
      ];

      return {
        ...prev,
        [index]: updatedInstruments,
      };
    });
  };

  const removeInstrument = (index, instrumentId) => {
    setSelectedInstruments((prev) => {
      const currentInstruments = prev[index] || [];
      const updatedInstruments = currentInstruments.filter(
        (inst) => inst.id !== instrumentId
      );

      return {
        ...prev,
        [index]: updatedInstruments,
      };
    });
  };

  const contextValue = useMemo(
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
