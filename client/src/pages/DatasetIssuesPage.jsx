import { DatasetIssues } from "components/DatasetIssues";

const { Grid, Typography } = require("@mui/material");

export const DatasetIssuesPage = ({ datasetId }) => {
  return (
    <Grid container>
      <Grid item container>
        <Grid item xs={12}>
          <DatasetIssues datasetId={datasetId} />
        </Grid>
      </Grid>
    </Grid>
  );
};
