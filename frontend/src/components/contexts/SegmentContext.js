import React, { createContext, useContext, useState, useMemo } from "react";

const SegmentContext = createContext();

export const SegmentProvider = ({ children }) => {
  const [artistSegments, setArtistSegments] = useState({});

  const addSegment = (index, segment) => {
    if (!segment || !segment.id) return;
    setArtistSegments((prev) => {
      const existingSegments = prev[index] || [];
      const segmentExists = existingSegments.some(
        (seg) => seg.id === segment.id
      );

      // If the segment exists, update it; otherwise, add it
      const updatedSegments = segmentExists
        ? existingSegments.map((seg) =>
            seg.id === segment.id ? { ...seg, ...segment } : seg
          )
        : [...existingSegments, segment];

      return {
        ...prev,
        [index]: updatedSegments,
      };
    });
  };

  const removeSegment = (index, segmentId) => {
    setArtistSegments((prev) => {
      const filteredSegments = (prev[index] || []).filter(
        (segment) => segment.id !== segmentId
      );
      return {
        ...prev,
        [index]: filteredSegments,
      };
    });
  };

  const contextValue = useMemo(
    () => ({
      artistSegments,
      addSegment,
      removeSegment,
    }),
    [artistSegments]
  );

  return (
    <SegmentContext.Provider value={contextValue}>
      {children}
    </SegmentContext.Provider>
  );
};

export const useSegmentContext = () => {
  const context = useContext(SegmentContext);
  if (!context) {
    throw new Error("useSegmentContext must be used within an SegmentContext");
  }
  return context;
};
