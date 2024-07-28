import { camelCaseToTitleCase, snakeCaseToTitleCase } from "utils/strings";

const { Grid, Typography } = require("@mui/material");
const { DataGrid } = require("@mui/x-data-grid");
const { useIssues } = require("hooks/useIssues");
const { useEffect, useState } = require("react");

export const DatasetIssues = ({ datasetId }) => {
  const { data: issues, isLoading } = useIssues(datasetId);

  const [tableData, setTableData] = useState({ colDef: [], rowDef: [] });

  useEffect(() => console.log({ issues }), [issues]);

  const result = {
    headers: [],
    data: {
      cases: {
        missingValue: 0,
        inconsistency: 0,
        outlier: 2.857142857142857,
        typo: 0,
      },
      monthId: {
        missingValue: 0,
        inconsistency: 0,
        outlier: 0,
        typo: 0,
      },
      quarantines: {
        missingValue: 0,
        inconsistency: 0,
        outlier: 0,
        typo: 0,
      },
      totalDrugDosage: {
        missingValue: 0,
        inconsistency: 0,
        outlier: 1.4285714285714286,
        typo: 0,
      },
      totalVaccines: {
        missingValue: 0,
        inconsistency: 0,
        outlier: 0,
        typo: 0,
      },
      vaccinationRate: {
        missingValue: 18.571428571428573,
        inconsistency: 0,
        outlier: 1.4285714285714286,
        typo: 0,
      },
      yearId: {
        missingValue: 0,
        inconsistency: 0,
        outlier: 0,
        typo: 0,
      },
    },
  };

  useEffect(() => {
    const colDef =
      issues?.headers?.map((header) => {
        return {
          field: header,
          headerName: camelCaseToTitleCase(header),
          flex: 1,
        };
      }) ?? [];

    const rowDef = !issues?.data
      ? []
      : Object.keys(issues.data).map((row) => ({
          id: row,
          column: row,
          ...Object.fromEntries(
            Object.entries(issues.data[row]).map(([key, value]) => [
              key,
              typeof value === "number"
                ? // value === 0
                  //   ? "-"
                  //   :
                  `${+value.toFixed(2)}%`
                : value,
            ]),
          ),
        }));

    setTableData({ colDef, rowDef });
  }, [issues]);

  useEffect(() => {
    console.log({ data: issues?.data });
  }, [issues?.data]);

  return <DataGrid columns={tableData.colDef} rows={tableData.rowDef} />;
};
