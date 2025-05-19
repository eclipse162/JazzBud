import React, { createContext, useContext, useState } from "react";

const InstrumentContext = createContext();

export const InstrumentProvider = ({ children }) => {
  const [selectedInstruments, setSelectedInstruments] = useState({});

  const handleInstrumentSelect = (index, instrument) => {
    setSelectedInstruments((prev) => {
      // Ensure the current instruments for the artist index are isolated
      const currentInstruments = prev[index] ? [...prev[index]] : [];
      const newInstruments = Array.isArray(instrument)
        ? instrument
        : [instrument];

      // Avoid adding duplicate instruments
      const updatedInstruments = [
        ...currentInstruments,
        ...newInstruments.filter(
          (newInst) =>
            !currentInstruments.some((inst) => inst.id === newInst.id)
        ),
      ];

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
    setSelectedInstruments((prev) => {
      const currentInstruments = prev[index] || [];
      const updatedInstruments = currentInstruments.filter(
        (inst) => inst.id !== instrumentId
      );

      console.log(
        `Removed instrument ${instrumentId} for artist ${index}:`,
        updatedInstruments
      );

      return {
        ...prev,
        [index]: updatedInstruments,
      };
    });
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
