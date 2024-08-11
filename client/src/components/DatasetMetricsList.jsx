import { DatasetGauge } from "./DatasetGauge";
import { useDatasetMetrics } from "api/query";
import { snakeCaseToTitleCase } from "utils/strings";
import { DataGrid } from "./DataGrid";

export const DatasetMetricsList = ({ datasetId }) => {
  const { data: metrics, isLoading } = useDatasetMetrics(datasetId);

  // console.log(metrics, datasetId);

  const rows =
    metrics?.map(({ name, score }) => ({
      id: name,
      name: snakeCaseToTitleCase(name),
      score,
    })) ?? [];

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

  return <DataGrid rows={rows} columns={columns} loading={isLoading} />;
};
