import { Card, Grid, Skeleton, Typography } from "@mui/material";
import { useDatasetRating } from "api/query";
import { DatasetGauge, DatasetMetricsList } from "components";
import { DatasetReadability } from "components/DatasetReadability";

export const DatasetMetricsPage = ({ datasetId }) => {
  const { data, isLoading } = useDatasetRating(datasetId);

  return (
    <Grid container rowGap={2}>
      <Grid item xs={12}>
        <Card variant="outlined">
          <Grid container justifyContent="space-around" gap={2} margin={2}>
            <Grid item flexShrink>
              <DatasetGauge
                animate
                value={data?.rating ?? 0}
                width={200}
                halfMode
              />
            </Grid>
            <Grid item flexGrow>
              <Grid item container flexShrink direction="column">
                <Grid item>
                  {isLoading ? (
                    <Skeleton variant="text" width={120} height={72} />
                  ) : (
                    <Typography variant="h2">
                      {+data?.rating.toFixed(2) ?? ""}
                    </Typography>
                  )}
                </Grid>
                <Grid item>
                  {isLoading ? (
                    <Skeleton variant="text" width={294} height={56} />
                  ) : (
                    <Typography variant="h3">Overall Score</Typography>
                  )}
                </Grid>
              </Grid>
            </Grid>
          </Grid>
        </Card>
      </Grid>
      <Grid item xs={12}>
        <DatasetMetricsList datasetId={datasetId} />
      </Grid>
      <Grid item xs={12}>
        <DatasetReadability datasetId={datasetId} />
      </Grid>
    </Grid>
  );
};
