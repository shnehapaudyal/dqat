import { DataGrid } from "@mui/x-data-grid";
import { useDatasetStat } from "api/query";
import { useEffect, useState } from "react";

const transposeObject = (data) => {
  if (!data) return [];

  // get keys from any one item in data
  const objectKeys = Object.keys(data);
  const keys = Object.keys(data[objectKeys[0]]);

  // Create an empty object to store the transposed data
  const result = [];

  objectKeys.forEach((objectKey) => {
    // console.log("transposed", { objectKey, objectKeys });
    const row = {};
    row.column = objectKey;
    keys.forEach((key) => {
      row[key] = data[objectKey][key];
    });
    result.push(row);
  });

  // Return the transposed data
  return [keys, result];
};

export const DatasetStats = ({ datasetId }) => {
  const [page, setPage] = useState(0);
  const { data, isLoading } = useDatasetStat(datasetId);

  const [headers, transposed] = transposeObject(data);

  useEffect(() => {
    console.log("transposed", { headers, transposed });
  }, [headers, transposed]);
  const coldef = transposed
    ? [
        {
          label: "Column",
          field: "column",
          flex: 3,
          fixed: true,
        },
        ...headers.map((key) => ({
          label: key,
          field: key,
          flex: 1,
          renderCell: (params) => +parseFloat(params.value).toFixed(2),
        })),
      ]
    : [];

  const rowDef = transposed ?? [];

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
      pagination={undefined}
    />
  );
};
