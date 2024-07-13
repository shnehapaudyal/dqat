import { Box } from "@mui/material";
import { ArcElement, Chart } from "chart.js";
import { useEffect, useRef } from "react";
import { Doughnut as DoughnutChart } from "react-chartjs-2";

Chart.register(ArcElement);

export const Doughnut = ({ sx }) => {
  const data = {
    labels: ["Label 1", "Label 2", "Label 3"],
    datasets: [
      {
        data: [300, 50, 100],
        backgroundColor: ["#ff6384", "#36a2eb", "#ffce56"],
        hoverBackgroundColor: ["#ff6384", "#36a2eb", "#ffce56"],
      },
    ],
  };

  const ref = useRef(null);

  useEffect(() => {
    const comp = ref.current;

    return () => {
      comp?.chart?.destroy();
    };
  }, [ref]);

  return (
    <Box sx={sx}>
      <DoughnutChart ref={ref} data={data} />
    </Box>
  );
};
