import { Card, Grid, Typography } from "@mui/material";
import { useDataset, useDatasetRating } from "api/query";
import { DatasetGauge, DatasetMetricsList } from "components";
import { useParams } from "react-router-dom";

export const DatasetMetricsPage = ({ datasetId }) => {
  const { data } = useDatasetRating(datasetId);

  return (
    <Grid container rowGap={2}>
      <Grid item xs={12}>
        <Card variant="outlined">
          <Grid container justifyContent="space-around" gap={2} margin={2}>
            <Grid item flexShrink>
              <DatasetGauge value={data?.rating ?? 0} width={200} halfMode />
            </Grid>
            <Grid item flexGrow>
              <Grid item container flexShrink direction="column">
                <Grid item>
                  <Typography variant="h2">
                    {+data?.rating.toFixed(2) ?? ""}
                  </Typography>
                </Grid>
                <Grid item>
                  <Typography variant="h3">Overall Score</Typography>
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Card>
      </Grid>
      <Grid container item>
        <DatasetMetricsList datasetId={datasetId} />
      </Grid>
    </Grid>
  );
};
