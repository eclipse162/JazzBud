import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

const Waveform = ({
  artistIndex,
  segments,
  songDuration,
  instruments,
  onAddSegment,
  onUpdateSegments,
}) => {
  const svgRef = useRef(null);

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = 40;

    // Clear any previous render
    svg.selectAll("*").remove();

    // Time scale: maps time (sec) to pixel x-coordinate
    const xScale = d3.scaleLinear().domain([0, songDuration]).range([0, width]);

    // Draw baseline
    svg
      .append("line")
      .attr("x1", 0)
      .attr("y1", height / 2)
      .attr("x2", width)
      .attr("y2", height / 2)
      .attr("stroke", "black")
      .attr("stroke-width", 2);
  }, [songDuration, segments]);

  return (
    <svg
      ref={svgRef}
      style={{ width: "100%", height: 40, backgroundColor: "#f8f8f8" }}></svg>
  );
};

export default Waveform;
