import { Grid, Typography } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useDatasets } from "api/query";
import { useNavigate } from "react-router-dom";

export const History = () => {
  const navigate = useNavigate();
  const { data, isLoading } = useDatasets();

  const columns = [
    { field: "dataset_id", headerName: "Id" },
    { field: "filename", headerName: "File Name" },
    { field: "uploaded", headerName: "Uploaded at" },
  ];

  const rows = data?.records?.map((item) => ({
    dataset_id: item.dataset_id,
    filename: item.filename,
    uploaded: item.uploaded,
  }));

  // navigate({ to: `/detail/233` });

  const openDetailPage = (datasetId) => {
    navigate(`dataset/${datasetId}`);
  };

  return (
    <Grid container rowGap={2}>
      <Grid item xs={12}>
        <Typography variant="h5">History</Typography>
      </Grid>
      <Grid item xs={12}>
        <DataGrid
          rows={rows || []} // Ensure rows is not undefined
          columns={columns}
          getRowId={(row) => row.dataset_id}
          loading={isLoading}
          sx={{ minHeight: "200px" }}
          onRowClick={({ row }) => openDetailPage(row.dataset_id)}
        />
      </Grid>
    </Grid>
  );
};
