import { blue } from "@mui/material/colors";

const { Grid, Collapse, Chip } = require("@mui/material");
const { useDatasetTags } = require("api/query");

export const DatasetTags = ({ datasetId }) => {
  const { data: tags, isLoading, isError } = useDatasetTags(datasetId);

  return (
    <Collapse collapsedSize={0} in={!(tags?.length && isError)}>
      <Grid container gap={1}>
        {tags?.map((tag) => (
          <Grid item>
            <Chip label={tag} size="small" color="primary" />
          </Grid>
        ))}
      </Grid>
    </Collapse>
  );
};
