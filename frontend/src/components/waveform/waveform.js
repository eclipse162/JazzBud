import { useRef, useEffect, useState } from "react";
import * as d3 from "d3";

function Waveform({ artistId, duration, segments, onSegmentChange }) {
  const svgRef = useRef(null);
  const [localSegments, setLocalSegments] = useState(segments || []);

  // Scale for mapping time to pixel
  const [width, setWidth] = useState(1000);
  const timeScale = d3.scaleLinear().domain([0, duration]).range([0, width]);

  useEffect(() => {
    const handleResize = () => {
      const newWidth = svgRef.current?.getBoundingClientRect().width || 1000;
      setWidth(newWidth);
    };
    handleResize();
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove(); // Clear previous render

    // Draw baseline
    svg
      .append("line")
      .attr("x1", 0)
      .attr("x2", width)
      .attr("y1", 30)
      .attr("y2", 30)
      .attr("stroke", "#ccc")
      .attr("stroke-width", 4);

    // Draw timestamp labels every 10 seconds
    const labelInterval = 10; // seconds
    const times = d3.range(0, duration + 1, labelInterval);
    times.forEach((t) => {
      svg
        .append("text")
        .attr("x", timeScale(t))
        .attr("y", 55)
        .attr("text-anchor", "middle")
        .attr("font-size", "10px")
        .text(formatTime(t));

      svg
        .append("line")
        .attr("x1", timeScale(t))
        .attr("x2", timeScale(t))
        .attr("y1", 25)
        .attr("y2", 35)
        .attr("stroke", "#888")
        .attr("stroke-width", 1);
    });

    // Draw segments
    const segmentGroup = svg
      .selectAll(".segment")
      .data(localSegments)
      .enter()
      .append("g")
      .attr("class", "segment");

    segmentGroup
      .append("rect")
      .attr("x", (d) => timeScale(d.start))
      .attr("y", 15)
      .attr("width", (d) => timeScale(d.end) - timeScale(d.start))
      .attr("height", 30)
      .attr("fill", "rgba(255, 0, 0, 0.5)");

    // Add drag handles
    const dragHandleWidth = 6;

    segmentGroup
      .append("rect") // Start handle
      .attr("x", (d) => timeScale(d.start) - dragHandleWidth / 2)
      .attr("y", 15)
      .attr("width", dragHandleWidth)
      .attr("height", 30)
      .attr("fill", "darkred")
      .style("cursor", "ew-resize")
      .call(
        d3.drag().on("drag", function (event, d) {
          const newStart = Math.min(timeScale.invert(event.x), d.end - 0.1);
          d.start = Math.max(0, newStart);
          updateSegments();
        })
      );

    segmentGroup
      .append("rect") // End handle
      .attr("x", (d) => timeScale(d.end) - dragHandleWidth / 2)
      .attr("y", 15)
      .attr("width", dragHandleWidth)
      .attr("height", 30)
      .attr("fill", "darkred")
      .style("cursor", "ew-resize")
      .call(
        d3.drag().on("drag", function (event, d) {
          const newEnd = Math.max(timeScale.invert(event.x), d.start + 0.1);
          d.end = Math.min(duration, newEnd);
          updateSegments();
        })
      );

    // Click to create new segments
    let pendingStart = null;
    svg.on("click", function (event) {
      const [mouseX] = d3.pointer(event);
      const time = timeScale.invert(mouseX);

      if (pendingStart === null) {
        pendingStart = time;
      } else {
        const newSegment = {
          start: Math.min(pendingStart, time),
          end: Math.max(pendingStart, time),
        };
        const updated = [...localSegments, newSegment];
        setLocalSegments(updated);
        onSegmentChange(artistId, updated);
        pendingStart = null;
      }
    });

    function updateSegments() {
      const updated = [...localSegments];
      setLocalSegments(updated);
      onSegmentChange(artistId, updated);
    }
  }, [localSegments, duration, width]);

  // Format time as mm:ss
  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  return <svg ref={svgRef} width="100%" height={70}></svg>;
}
