import { DataGrid } from "@mui/x-data-grid";

export const DatasetInfo = ({ datasetId }) => {
  const coldef = [
    {
      label: "Column",
      field: "column",
      flex: 1,
    },
    {
      label: "Type",
      field: "type",
      flex: 1,
    },
  ];

  const rowDef = [
    {
      column: "Value1",
      type: "String",
    },
    {
      column: "Value2",
      type: "Number",
    },
    {
      column: "Value3",
      type: "Boolean",
    },
    {
      column: "Value4",
      type: "Date",
    },
    {
      column: "Value5",
      type: "Object",
    },
    {
      column: "Value6",
      type: "Array",
    },
    {
      column: "Value7",
      type: "Function",
    },
  ];
  return (
    <DataGrid
      density="compact"
      columns={coldef}
      rows={rowDef}
      getRowId={(row) => row.column}
    />
  );
};
