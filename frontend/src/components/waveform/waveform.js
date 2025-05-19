import React, { useEffect, useState, useRef } from "react";
import { formatTime } from "../../utils.js";
import * as d3 from "d3";

const Waveform = ({
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
  const [midDrag, setMidDrag] = useState(null);
  const [toolTip, setToolTip] = useState(null);

  const containerRef = useRef(null);

  useEffect(() => {
    console.log("Instruments passed to Waveform:", instruments);
  }, [instruments]);

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const container = containerRef.current;
    if (instruments.length > 0) {
      setColour(instruments[0].colour);
    }

    const renderWaveform = () => {
      const width = container.clientWidth;
      const height = 60;

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

      if (dragStart !== null && midDrag !== null) {
        const start = Math.max(0, Math.min(dragStart, midDrag));
        const end = Math.min(songDuration, Math.max(dragStart, midDrag));
        const previewWidth = xScale(end) - xScale(start);

        if (end - start > 0.1) {
          svg
            .append("rect")
            .attr("x", xScale(start))
            .attr("y", y - radius)
            .attr("width", previewWidth)
            .attr("height", lineHeight)
            .attr("rx", radius)
            .attr("ry", radius)
            .attr("fill", colour)
            .attr("opacity", 0.8);
        }

        if (toolTip && midDrag > dragStart) {
          svg
            .append("text")
            .attr("x", xScale(end) - 5)
            .attr("y", y - 10)
            .attr("text-anchor", "end")
            .attr("fill", "#D9D9D9")
            .attr("font-size", "13px")
            .attr("font-weight", "bold")
            .attr("z-index", 100)
            .attr("font-family", "sans-serif")
            .text(`${formatTime(start)} - ${formatTime(midDrag)}`);
        } else if (toolTip && midDrag < dragStart) {
          svg
            .append("text")
            .attr("x", xScale(start) + 5)
            .attr("y", y - 10)
            .attr("text-anchor", "start")
            .attr("fill", "#D9D9D9")
            .attr("font-size", "13px")
            .attr("font-weight", "bold")
            .attr("z-index", 100)
            .attr("font-family", "sans-serif")
            .text(`${formatTime(midDrag)} - ${formatTime(dragStart)}`);
        }
      }

      const handleMouseDown = (event) => {
        const mouseX = d3.pointer(event, svgRef.current)[0];
        const startTime = Math.max(
          0,
          Math.min(songDuration, xScale.invert(mouseX))
        );
        setDragStart(startTime);
        setMidDrag(startTime);
        setToolTip(true);
      };

      const handleMouseMove = (event) => {
        if (dragStart !== null) {
          const mouseX = d3.pointer(event, svgRef.current)[0];
          const time = Math.max(
            0,
            Math.min(songDuration, xScale.invert(mouseX))
          );
          setMidDrag(time);
        }
      };

      const handleMouseUp = () => {
        if (dragStart !== null && midDrag !== null) {
          const start = Math.max(0, Math.min(dragStart, midDrag));
          const end = Math.min(songDuration, Math.max(dragStart, midDrag));
          if (end - start > 0.5) {
            setSegments((prev) => [...prev, { start, end }]);
          }
          setDragStart(null);
          setMidDrag(null);
          setToolTip(false);
        }
      };

      svg
        .on("mousedown", handleMouseDown)
        .on("mousemove", handleMouseMove)
        .on("mouseup", handleMouseUp);

      return () => {
        svg.on("mousedown", null).on("mousemove", null).on("mouseup", null);
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
  }, [
    songDuration,
    segments,
    colour,
    instruments,
    dragStart,
    midDrag,
    toolTip,
  ]);

  return (
    <div ref={containerRef} style={{ width: "100%" }}>
      <svg
        ref={svgRef}
        style={{
          width: "100%",
          height: 60,
          display: "block",
          marginBottom: "16px",
          cursor: "pointer",
        }}
      />
    </div>
  );
};

export default Waveform;
