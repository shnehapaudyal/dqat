import { Grid, Pagination } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { useDatasetData } from "api/query";
import React, { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";

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
    <Grid item container xs={12}>
      <Grid item xs={12} flexGrow>
        <DataGrid
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
