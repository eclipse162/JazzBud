import React, { useEffect, useState, useRef } from "react";
import * as d3 from "d3";

const Waveform = ({
  artistIndex,
  sogments = [],
  songDuration,
  instruments,
  onAddSegment,
  onUpdateSegments,
}) => {
  const svgRef = useRef(null);
  const [colour, setColour] = useState("#D9D9D9");
  const [segments, setSegments] = useState([]);
  const [dragStart, setDragStart] = useState(null);

  const containerRef = useRef(null);

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const container = containerRef.current;
    if (instruments.length > 0) {
      setColour(instruments[0].colour);
    }

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
        .attr("fill", "#6c6c6c");

      segments.forEach((segment) => {
        svg
          .append("rect")
          .attr("x", xScale(segment.start))
          .attr("y", y - radius)
          .attr("width", xScale(segment.end) - xScale(segment.start))
          .attr("height", lineHeight)
          .attr("rx", radius)
          .attr("ry", radius)
          .attr("fill", colour);
      });

      const handleMouseDown = (event) => {
        const mouseX = d3.pointer(event, svgRef.current)[0];
        const startTime = xScale.invert(mouseX);
        setDragStart(startTime);
      };

      const handleMouseUp = (event) => {
        if (dragStart === null) return;
        const mouseX = d3.pointer(event)[0];
        const endTime = xScale.invert(mouseX);
        const start = Math.min(dragStart, endTime);
        const end = Math.max(dragStart, endTime);
        if (end - start > 0.5) {
          setSegments((prev) => [...prev, { start, end }]);
        }
        setDragStart(null);
      };

      svg.on("mousedown", handleMouseDown).on("mouseup", handleMouseUp);

      return () => {
        svg.on("mousedown", null).on("mouseup", null);
      };
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
  }, [songDuration, segments, colour, instruments, dragStart]);

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
