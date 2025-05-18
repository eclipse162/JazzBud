import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

const Waveform = ({
  artistIndex,
  segments = [],
  songDuration,
  instruments,
  onAddSegment,
  onUpdateSegments,
}) => {
  const svgRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const container = containerRef.current;

    const renderWaveform = () => {
      const width = container.clientWidth;
      const height = 30;

      // Clear previous render
      svg.selectAll("*").remove();

      // Time scale
      const xScale = d3
        .scaleLinear()
        .domain([0, songDuration])
        .range([0, width]);

      // --- Draw GRAY BASELINE (represents full duration) ---
      const y = height / 2;
      const lineHeight = 8;
      const radius = lineHeight / 2;

      svg
        .append("rect")
        .attr("x", 0)
        .attr("y", y - radius)
        .attr("width", width)
        .attr("height", lineHeight)
        .attr("rx", radius)
        .attr("ry", radius)
        .attr("fill", "#4e4e4e"); // gray like your mockup
    };

    // Initial render
    renderWaveform();

    // Use ResizeObserver to re-render on container resize
    const resizeObserver = new ResizeObserver(() => {
      renderWaveform();
    });

    resizeObserver.observe(container);

    // Cleanup observer on unmount
    return () => {
      resizeObserver.disconnect();
    };
  }, [songDuration, segments]);

  return (
    <div ref={containerRef} style={{ width: "100%" }}>
      <svg
        ref={svgRef}
        style={{
          width: "100%",
          height: 30,
          display: "block",
          marginBottom: "16px",
        }}
      />
    </div>
  );
};

export default Waveform;
