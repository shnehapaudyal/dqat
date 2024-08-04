import { camelCaseToTitleCase, snakeCaseToTitleCase } from "utils/strings";

const { Grid, Typography } = require("@mui/material");
const { DataGrid } = require("@mui/x-data-grid");
const { useIssues } = require("hooks/useIssues");
const { useEffect, useState, useMemo } = require("react");

export const DatasetIssues = ({ datasetId }) => {
  const { headers, data: issues, isLoading } = useIssues(datasetId);

  // const result = {
  //   headers: [],
  //   data: {
  //     cases: {
  //       missingValue: 0,
  //       inconsistency: 0,
  //       outlier: 2.857142857142857,
  //       typo: 0,
  //     },
  //     monthId: {
  //       missingValue: 0,
  //       inconsistency: 0,
  //       outlier: 0,
  //       typo: 0,
  //     },
  //     quarantines: {
  //       missingValue: 0,
  //       inconsistency: 0,
  //       outlier: 0,
  //       typo: 0,
  //     },
  //     totalDrugDosage: {
  //       missingValue: 0,
  //       inconsistency: 0,
  //       outlier: 1.4285714285714286,
  //       typo: 0,
  //     },
  //     totalVaccines: {
  //       missingValue: 0,
  //       inconsistency: 0,
  //       outlier: 0,
  //       typo: 0,
  //     },
  //     vaccinationRate: {
  //       missingValue: 18.571428571428573,
  //       inconsistency: 0,
  //       outlier: 1.4285714285714286,
  //       typo: 0,
  //     },
  //     yearId: {
  //       missingValue: 0,
  //       inconsistency: 0,
  //       outlier: 0,
  //       typo: 0,
  //     },
  //   },
  // };

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
