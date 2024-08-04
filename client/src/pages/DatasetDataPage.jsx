import { Box, Grid, Typography } from "@mui/material";
import { useDatasetData } from "api/query";
import { DatasetTypeInfo } from "components";
import { DataGrid } from "components/DataGrid";
import { DatasetStats } from "components/DatasetStats";
import React, { useMemo, useState } from "react";

export const DatasetDataPage = ({ datasetId }) => {
  const [currentPage, setCurrentPage] = useState(1);

  const pageSize = 25;

  const { data, isLoading } = useDatasetData(datasetId, currentPage, pageSize);

  const columns = useMemo(() => {
    const headers = data?.length ? Object.keys(data[0]) : [];
    return headers
      .filter((h) => h !== "id")
      .map((header) => ({
        field: header,
        headerName: header,
        flex: 1,
      }));
  }, [data]);

  const value = useMemo(
    () =>
      data?.map((row, index) => {
        row.id = index + 1;
        return row;
      }),
    [data],
  );

  // useEffect(
  //   () =>
  //     console.log({ headers: columns, value, data, total_items, datasetData }),
  //   [data, datasetData, columns, total_items, value],
  // );

  return (
    <Grid item container xs={12} rowGap={2}>
      <Grid item xs={12} sm={4}>
        <Box sx={{ marginRight: 1 }}>
          <DatasetTypeInfo datasetId={datasetId} />
        </Box>
      </Grid>
      <Grid item xs={12} sm={8}>
        <Box sx={{ marginLeft: 1 }}>
          <DatasetStats datasetId={datasetId} />
        </Box>
      </Grid>

      <Grid item xs={12} flexGrow>
        <DataGrid
          title="Data Sample"
          density="compact"
          loading={isLoading}
          rows={value ?? []}
          columnHeaderHeight={64}
          columns={columns}
          columnBufferPx={100}
          rowBufferPx={100}
          sx={{ minHeight: "500px" }}
          row
          pageSizeOptions={[pageSize]}
          paginationModel={{ page: currentPage, pageSize }}
          onPaginationModelChange={({ page }) => setCurrentPage(page)}
        />
      </Grid>
    </Grid>
  );
};
