import { Grid, Typography } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";

const rows = [
  { datasetId: 1, filename: "mpox.csv", uploaded: new Date().getTime() },
  { datasetId: 1, filename: "mpox.csv", uploaded: new Date().getTime() },
  { datasetId: 1, filename: "mpox.csv", uploaded: new Date().getTime() },
];

const columns = [
  { field: "datasetId", headerName: "Id" },
  { field: "filename", headerName: "File Name" },
  { field: "uploaded", headerName: "Uploaded at" },
];

export const History = () => (
  <Grid container rowGap={2}>
    <Grid item xs={12}>
      <Typography variant="h5">History</Typography>
    </Grid>
    <DataGrid rows={rows} columns={columns} getRowId={(row) => row.datasetId} />
  </Grid>
);
