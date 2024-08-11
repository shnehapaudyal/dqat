import { Grid, Typography } from "@mui/material";
import { useDatasets } from "api/query";
import { useNavigate } from "react-router-dom";
import { getFileSize } from "utils/files";
import { DataGrid } from "./DataGrid";

export const History = () => {
  const navigate = useNavigate();
  const { data, isLoading } = useDatasets();

  const columns = [
    { field: "dataset_id", headerName: "Id", flex: 1 },
    { field: "filename", headerName: "File Name", flex: 1 },
    { field: "created_at", headerName: "Uploaded at", flex: 1 },
    {
      field: "size",
      headerName: "File Size",
      flex: 1,
      renderCell: (params) => (params?.value ? getFileSize(params.value) : "-"),
    },
  ];

  const rows = data?.records ?? [];

  // navigate({ to: `/detail/233` });

  const openDetailPage = (datasetId) => {
    navigate(`dataset/${datasetId}?tab=data`);
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
