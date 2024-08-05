import { Card, Divider, Grid, Typography } from "@mui/material";
import { DataGrid as MUIDataGrid } from "@mui/x-data-grid";
import { useEffect } from "react";
export const DataGrid = ({ title, itemsPerPage = 50, ...props }) => {
  useEffect(
    () => console.log("DataGrid", title, { loading: props?.loading }),
    [props?.loading, title],
  );

  itemsPerPage = props?.rows?.length
    ? Math.min(props?.rows?.length, itemsPerPage)
    : itemsPerPage;

  const grid = (
    <MUIDataGrid
      {...props}
      {...(itemsPerPage && {
        pageSizeOptions: [itemsPerPage],
        initialState: {
          pagination: { paginationModel: { pageSize: itemsPerPage } },
        },
      })}
      sx={{
        minHeight: 300,
        ...props?.sx,
        ...(title && {
          border: 0,
        }),
      }}
    />
  );
  return !title ? (
    grid
  ) : (
    <Card variant="outlined">
      <Grid container direction={"column"}>
        <Grid item paddingX={2} paddingY={1}>
          <Typography variant="h6">{title}</Typography>
        </Grid>
        <Divider />
        {grid}
      </Grid>
    </Card>
  );
};
