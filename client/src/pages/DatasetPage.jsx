import { Grid, Typography } from "@mui/material";
import { useDataset } from "api/query";
import { DatasetGauge, DatasetMetricsList } from "components";
import { useParams } from "react-router-dom";

export const DatasetPage = () => {
  const { id } = useParams("id");

  const dataset = useDataset(id);

  console.log(dataset.data);

  return (
    <Grid container justifyContent="space-around" padding={4} gap={2}>
      <Grid item xs={12}>
        <Typography variant="h5">Dataset</Typography>
      </Grid>
      <Grid item flexShrink>
        <DatasetGauge value={25} width={200} halfMode />
      </Grid>
      <Grid item flexGrow>
        <Grid item container flexShrink direction="column">
          <Grid item>
            <Typography variant="h2">3</Typography>
          </Grid>
          <Grid item>
            <Typography variant="h3">Overall Score</Typography>
          </Grid>
        </Grid>
      </Grid>

      <Grid item container>
        <DatasetMetricsList datasetId={id} />
      </Grid>
    </Grid>
  );
};
