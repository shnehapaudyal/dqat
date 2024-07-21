const { Gauge, gaugeClasses } = require("@mui/x-charts");

export const DatasetGauge = ({
  value,
  halfMode,
  shortLabel,
  fontSize = 20,
  ...sx
}) => {
  return (
    <Gauge
      value={value}
      {...(halfMode && { startAngle: -110, endAngle: 110 })}
      sx={{
        ...sx,
        [`& .${gaugeClasses.valueText}`]: {
          fontSize: fontSize,
          transform: "translate(0px, 0px)",
        },
      }}
      text={({ value, valueMax }) =>
        shortLabel ? `${value.toFixed(0)}` : `${value.toFixed(0)} / ${valueMax}`
      }
    />
  );
};
