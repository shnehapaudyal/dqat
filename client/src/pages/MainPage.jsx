import { Grid } from "@mui/material/index";
import React from "react";
import { FileUploadUI, History } from "../components";

export const MainPage = () => (
  <Grid
    container
    columns={1}
    flex={"1 1"}
    padding={4}
    sx={{ height: "100%" }}
    rowGap={4}
  >
    <Grid item xs={12} height={356}>
      <FileUploadUI />
    </Grid>
    <Grid item xs={12} flexGrow height={"50%"}>
      <History />
    </Grid>
  </Grid>
);
