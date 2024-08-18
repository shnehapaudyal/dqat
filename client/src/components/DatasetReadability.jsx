import { useDatasetReadability } from "api/query";
import { DataGrid } from "./DataGrid";
import { useMemo } from "react";
import { Box } from "@mui/system";

export const DatasetReadability = ({ datasetId }) => {
  const { data: readability, isLoading } = useDatasetReadability(datasetId);

  const cols = [
    {
      headerName: "Column",
      field: "column",
      flex: 1,
    },
    {
      headerName: "Readability Score",
      field: "score",
      flex: 1,
    },
  ];

  const rows = useMemo(() => {
    console.log("readability", { readability });
    if (!readability) return [];

    return Object.keys(readability).map((key) => ({
      column: key,
      id: key,
      score: readability[key],
    }));
  }, [readability]);

  return rows.length ? (
    <DataGrid
      title="Readability Score"
      loading={isLoading}
      columns={cols}
      rows={rows}
    />
  ) : null;
};
