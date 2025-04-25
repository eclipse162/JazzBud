import React, { useEffect, useRef, useState } from "react";
import * as d3 from "d3";

const Waveform = ({
  artistIndex,
  instruments,
  segments,
  songDuration,
  onAddSegment,
  onUpdateSegments,
}) => {
  const [colour, setColour] = useState("#f7f7f7");

  useEffect(() => {
    if (instruments[0]) {
      setColour(instruments[0].color);
    }
  }, [instruments]);

  const svgRef = useRef();
  const ySpacing = 80;

  useEffect(() => {
    const svg = d3.select(svgRef.current);
    const timelineWidth = getTimelineWidth();

    const timeScale = d3
      .scaleLinear()
      .domain([0, songDuration])
      .range([0, timelineWidth]);

    // Render baseline
    svg
      .append("line")
      .attr("class", "baseline")
      .attr("x1", 5)
      .attr("x2", timelineWidth - 5)
      .attr("y1", artistIndex * ySpacing + 30)
      .attr("y2", artistIndex * ySpacing + 30)
      .attr("stroke", "#ccc")
      .attr("stroke-width", 12)
      .attr("stroke-linecap", "round");

    // Handle dragging to create segments
    let pendingStart = null;

    svg.on("mousedown", function (event) {
      const [mouseX] = d3.pointer(event);
      pendingStart = timeScale.invert(mouseX);

      svg.on("mousemove", function (event) {
        const [currentX] = d3.pointer(event);
        const currentEnd = timeScale.invert(currentX);

        svg.selectAll(".temp-segment").remove();
        svg
          .append("line")
          .attr("class", "temp-segment")
          .attr("x1", timeScale(pendingStart))
          .attr("x2", timeScale(currentEnd))
          .attr("y1", artistIndex * ySpacing + 30)
          .attr("y2", artistIndex * ySpacing + 30)
          .attr("stroke", "#212121")
          .attr("stroke-width", 10)
          .attr("stroke-linecap", "round");
      });

      svg.on("mouseup", function (event) {
        const [mouseX] = d3.pointer(event);
        const endTime = timeScale.invert(mouseX);

        if (pendingStart !== null && Math.abs(endTime - pendingStart) > 0.5) {
          onAddSegment({
            start: Math.max(0, pendingStart),
            end: Math.min(songDuration, endTime),
            artistIndex,
          });
        }

        svg.selectAll(".temp-segment").remove();
        pendingStart = null;
        svg.on("mousemove", null).on("mouseup", null);
      });
    });

    // Render segments
    const updateWaveforms = () => {
      const waveforms = svg
        .selectAll(`.waveform-group-${artistIndex}`)
        .data(segments, (d, i) => i);

      // Enter: Add new segments
      const newWaveforms = waveforms
        .enter()
        .append("g")
        .attr("class", `waveform-group-${artistIndex}`);

      newWaveforms
        .append("line")
        .attr("class", "segment-line")
        .attr("x1", (d) => timeScale(d.start))
        .attr("x2", (d) => timeScale(d.end))
        .attr("y1", artistIndex * ySpacing + 30)
        .attr("y2", artistIndex * ySpacing + 30)
        .attr("stroke", colour)
        .attr("stroke-width", 10)
        .attr("stroke-linecap", "round");

      // Exit: Remove old segments
      waveforms.exit().remove();
    };

    updateWaveforms();
  }, [artistIndex, colour, segments, songDuration, onAddSegment]);

  const getTimelineWidth = () => {
    return svgRef.current.getBoundingClientRect().width;
  };

  return <svg ref={svgRef} style={{ width: "100%", height: "80px" }} />;
};

export default Waveform;
