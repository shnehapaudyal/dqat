import { snakeCaseToTitleCase } from "utils/strings";

import { DataGrid } from "@mui/x-data-grid";
import { useIssues } from "hooks/useIssues";
import { useMemo } from "react";

export const DatasetIssues = ({ datasetId }) => {
  const { headers, data: issues } = useIssues(datasetId);

  const colDef = useMemo(
    () =>
      headers.map((header) => ({
        field: header,
        headerName: snakeCaseToTitleCase(header),
        flex: 1,
      })),
    [headers],
  );

  const rowDef = useMemo(
    () =>
      Object.values(issues).map((issue) => ({ ...issue, id: issue.column })),
    [issues],
  );

  return <DataGrid columns={colDef} rows={rowDef} />;
};
