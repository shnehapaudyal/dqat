import { useDatasetStat } from "api/query";
import { useEffect, useMemo, useState } from "react";
import { DataGrid } from "./DataGrid";

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

  const [headers, transposed] = useMemo(() => transposeObject(data), [data]);

  useEffect(() => console.log("datastats", { data }), [data]);

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
          renderCell: (params) => {
            const floatValue = parseFloat(params.value);
            return Number.isNaN(floatValue) ? "-" : +floatValue.toFixed(2);
          },
        })),
      ]
    : [];

  const rowDef = transposed ?? [];

  return (
    <DataGrid
      loading={isLoading}
      title="Dataset Stats"
      density="compact"
      columns={coldef}
      rows={rowDef}
      getRowId={(row) => row.column}
      itemsPerPage={10}
    />
  );
};
