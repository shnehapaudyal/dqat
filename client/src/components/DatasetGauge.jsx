import { blue, green, orange } from "@mui/material/colors";
import { Gauge, gaugeClasses } from "@mui/x-charts";
import React from "react";

export const DatasetGauge = ({
  value,
  halfMode,
  shortLabel,
  animate,
  fontSize = 20,
  ...sx
}) => {
  return (
    <Gauge
      value={value}
      valueMax={100}
      cornerRadius="50%"
      {...(halfMode && { startAngle: -110, endAngle: 110 })}
      sx={{
        ...sx,
        [`& .${gaugeClasses.valueText}`]: {
          fontSize: fontSize,
          transform: "translate(0px, 0px)",
        },
        [`& .${gaugeClasses.valueArc}`]: {
          fill: value > 80 ? green[700] : value > 50 ? blue[700] : orange[700],
        },
      }}
      text={() =>
        shortLabel ? `${value.toFixed(0)}` : `${value.toFixed(0)} / 100`
      }
    />
  );
};
