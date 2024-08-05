import { snakeCaseToTitleCase } from "utils/strings";

import { useIssues } from "hooks/useIssues";
import { useMemo } from "react";
import { DataGrid } from "./DataGrid";

export const DatasetIssues = ({ datasetId }) => {
  const { headers, data: issues, isLoading } = useIssues(datasetId);

  const colDef = useMemo(
    () =>
      headers.map((header) => ({
        field: header,
        headerName: snakeCaseToTitleCase(header),
        flex: 1,
        renderCell: ({ value }) => {
          if (Number.isNaN(value) || Number.isFinite(value)) {
            const floatValue = parseFloat(value);
            return Number.isNaN(floatValue) ? "-" : +floatValue.toFixed(2);
          } else {
            return value;
          }
        },
      })),
    [headers],
  );

  const rowDef = useMemo(
    () =>
      Object.values(issues).map((issue) => ({ ...issue, id: issue.column })),
    [issues],
  );

  return <DataGrid columns={colDef} rows={rowDef} loading={isLoading} />;
};
