import { useDatasetStat } from "api/query";
import { useEffect, useMemo, useState } from "react";
import { DataGrid } from "./DataGrid";
import { camelCaseToTitleCase } from "utils/strings";

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
  const { data, isLoading } = useDatasetStat(datasetId);

  const [[headers, transposed], setTransposed] = useState([]);

  useEffect(() => {
    if (data) {
      new Promise((resolve) => resolve(transposeObject(data))).then(
        setTransposed,
      );
    }
  }, [data, isLoading]);

  useEffect(() => {
    console.log("transposed", { headers, transposed });
  }, [headers, transposed]);

  const coldef = transposed
    ? [
        {
          headerName: "Column",
          field: "column",
          flex: 3,
          fixed: true,
        },
        ...headers.map((key) => ({
          headerName: camelCaseToTitleCase(key),
          field: key,
          flex: 1,
          renderCell: ({ value }) => {
            if (value === undefined || value === null || Number.isNaN(value))
              return "-";
            if (Number.isFinite(value)) return +parseFloat(value).toFixed(2);
            return value;
          },
        })),
      ]
    : [];

  const rowDef = transposed ?? [];

  return (
    <DataGrid
      loading={isLoading}
      title="Dataset Statistics"
      density="compact"
      columns={coldef}
      rows={rowDef}
      getRowId={(row) => row.column}
      itemsPerPage={10}
    />
  );
};
