import { DataGrid } from "@mui/x-data-grid";
import { DatasetGauge } from "./DatasetGauge";

export const DatasetMetricsList = () => {
  const rows = [
    { id: 1, score: 24, name: "Completeness", uploaded: new Date().getTime() },
    { id: 2, score: 56, name: "Reliability", uploaded: new Date().getTime() },
    { id: 3, score: 97, name: "Normality", uploaded: new Date().getTime() },
  ];

  const columns = [
    {
      field: "score",
      headerName: "Score",
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
    { field: "name", headerName: "Metric" },
  ];

  return <DataGrid rows={rows} columns={columns} />;
};
