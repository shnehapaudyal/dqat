import { DataGrid } from "@mui/x-data-grid";
import { DatasetGauge } from "./DatasetGauge";
import { useDatasetMetrics } from "api/query";
import { snakeCaseToTitleCase } from "utils/strings";

export const DatasetMetricsList = ({ datasetId }) => {
  const metrics = useDatasetMetrics(datasetId);

  // console.log(metrics.data, datasetId);

  const rows = metrics.data
    ? Object.keys(metrics.data).map((key) => ({
        id: key,
        name: snakeCaseToTitleCase(key),
        score: metrics.data[key],
      }))
    : [];

  const columns = [
    {
      field: "score",
      headerName: "Score",
      flex: 1,
      renderCell: (params) => (
        <DatasetGauge
          height={56}
          width={56}
          value={params.value}
          shortLabel
          fontSize={12}
        />
      ),
    },
    { field: "name", headerName: "Metric", flex: 3 },
  ];

  return <DataGrid rows={rows} columns={columns} />;
};
