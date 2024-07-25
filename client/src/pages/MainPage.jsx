import { Grid } from "@mui/material/index";
import React from "react";
import { FileUploadUI, History } from "../components";

export const MainPage = () => (
  <Grid container direction="row" padding={4} rowGap={4}>
    <Grid item xs={12} flexShrink={1}>
      <FileUploadUI />
    </Grid>
    <Grid item xs={12} flexGrow={1}>
      <History />
    </Grid>
  </Grid>
);
