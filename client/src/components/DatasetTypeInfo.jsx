import { useDatasetTypes } from "api/query";
import { useState } from "react";
import { DataGrid } from "./DataGrid";

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
      title="Dataset Types"
      loading={isLoading}
      density="compact"
      columns={coldef}
      rows={rowDef}
      itemsPerPage={10}
      getRowId={(row) => row.column}
    />
  );
};
