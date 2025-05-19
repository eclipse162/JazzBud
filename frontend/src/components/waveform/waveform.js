import React, { useEffect, useState, useRef } from "react";
import styles from "./waveform.module.css";
import { formatTime } from "../../utils.js";
import * as d3 from "d3";
import { v4 as uuidv4 } from "uuid";

const Waveform = ({
  songDuration,
  instruments,
  artistSegments,
  addSegment,
  removeSegment,
}) => {
  const SOLO_HEIGHT = 20;
  const REGULAR_HEIGHT = 60;
  const SNAP_ANIMATION_DURATION = 300;

  const svgRef = useRef(null);
  const containerRef = useRef(null);

  const [midDrag, setMidDrag] = useState(null);
  const [toolTip, setToolTip] = useState(null);
  const [dragStart, setDragStart] = useState(null);
  const [colour, setColour] = useState("#D9D9D9");

  function animateSolo(selection, height) {
    selection
      .transition()
      .duration(SNAP_ANIMATION_DURATION)
      .attr("transform", `translate(0, ${height})`);
  }

  function getSoloPath(xStart, xEnd, yBase, height) {
    const width = xEnd - xStart;
    const mid = xStart + width / 2;

    const points = [
      [xStart, yBase],
      [mid, yBase + height],
      [xEnd, yBase],
    ];

    const lineGenerator = d3
      .line()
      .x((d) => d[0])
      .y((d) => d[1])
      .curve(d3.curveBasis); // smooth curve

    return lineGenerator(points);
  }

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

      artistSegments.forEach((segment) => {
        const group = svg
          .append("g")
          .attr("class", "segment")
          .call(
            d3.drag().on("drag", function (event) {
              const threshold = 5;

              if (!segment.isSolo && event.dy < -threshold) {
                segment.isSolo = true;
                animateSolo(d3.select(this), SOLO_HEIGHT);
                addSegment(segment);
              } else if (segment.isSolo && event.dy > threshold) {
                segment.isSolo = false;
                animateSolo(d3.select(this), 0);
                addSegment(segment);
              }
            })
          );
        if (segment.isSolo) {
          group
            .append("path")
            .attr(
              "d",
              getSoloPath(
                xScale(segment.start),
                xScale(segment.end),
                y,
                SOLO_HEIGHT
              )
            )
            .attr("fill", colour);
        } else {
          group
            .append("rect")
            .attr("x", xScale(segment.start))
            .attr("y", y - radius)
            .attr("width", xScale(segment.end) - xScale(segment.start))
            .attr("height", lineHeight)
            .attr("rx", radius)
            .attr("ry", radius)
            .attr("fill", colour)
            .on("dblclick", () => {
              removeSegment(segment);
            });
        }

        // Left Handle
        group
          .append("rect")
          .attr("x", xScale(segment.start) - 5)
          .attr("y", y - radius)
          .attr("width", 10)
          .attr("height", lineHeight + 5)
          .attr("fill", "transparent")
          .attr("cursor", "ew-resize")
          .call(
            d3.drag().on("drag", (event) => {
              const newStart = Math.max(
                0,
                Math.min(xScale.invert(event.x), segment.end - 0.1)
              );
              const newSegment = {
                ...segment,
                start: newStart,
              };
              addSegment(newSegment);
            })
          );

        // Right Handle
        group
          .append("rect")
          .attr("x", xScale(segment.end) - 4)
          .attr("y", y - radius - 2)
          .attr("width", 8)
          .attr("height", lineHeight + 4)
          .attr("fill", "transparent")
          .attr("cursor", "ew-resize")
          .call(
            d3.drag().on("drag", (event) => {
              const newEnd = Math.max(
                songDuration,
                Math.max(xScale.invert(event.x), segment.start + 0.1)
              );
              const newSegment = {
                ...segment,
                end: newEnd,
              };
              addSegment(newSegment);
            })
          );
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
            .text(`${formatTime(dragStart)} - ${formatTime(midDrag)}`);
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
          let id = uuidv4();
          const start = Math.max(0, Math.min(dragStart, midDrag));
          const end = Math.min(songDuration, Math.max(dragStart, midDrag));
          const segment = { id: id, start: start, end: end, isSolo: false };
          if (end - start > 0.5) {
            addSegment(segment);
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
    instruments,
    artistSegments,
    addSegment,
    removeSegment,
    colour,
    dragStart,
    midDrag,
    toolTip,
  ]);

  return (
    <div
      ref={containerRef}
      className={styles.noSelect}
      style={{ width: "100%" }}>
      <svg className={styles.waveform} ref={svgRef} />
    </div>
  );
};

export default Waveform;
