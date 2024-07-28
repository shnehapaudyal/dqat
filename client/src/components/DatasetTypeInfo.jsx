import { DataGrid } from "@mui/x-data-grid";
import { useDatasetTypes } from "api/query";
import { useState } from "react";

export const DatasetTypeInfo = ({ datasetId }) => {
  const [page, setPage] = useState(0);
  const { data, isLoading } = useDatasetTypes(datasetId);
  const coldef = [
    {
      label: "Column",
      field: "column",
      flex: 3,
    },
    {
      label: "Type",
      field: "type",
      flex: 2,
    },
  ];

  const rowDef = data
    ? Object.keys(data).map((key) => ({
        column: key,
        type: data[key],
      }))
    : [];

  return (
    <DataGrid
      loading={isLoading}
      density="compact"
      columns={coldef}
      rows={rowDef}
      pageSizeOptions={[10]}
      paginationModel={{ pageSize: 10, page }}
      onPaginationModelChange={(_, page) => setPage(page)}
      getRowId={(row) => row.column}
    />
  );
};
