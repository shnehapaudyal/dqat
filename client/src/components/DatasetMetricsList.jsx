import { DatasetGauge } from "./DatasetGauge";
import { useDatasetMetricEstimation, useDatasetMetrics } from "api/query";
import { snakeCaseToTitleCase } from "utils/strings";
import { DataGrid } from "./DataGrid";
import {
  Box,
  CircularProgress,
  Grid,
  Tooltip,
  Typography,
} from "@mui/material";
import { common } from "@mui/material/colors";

export const DatasetMetricsList = ({ datasetId }) => {
  const { data: metrics, isLoading } = useDatasetMetrics(datasetId);

  const { data: estimation, isLoading: isLoadingEstimation } =
    useDatasetMetricEstimation(datasetId);

  // console.log(metrics, datasetId);

  const rows =
    metrics?.map(({ name, score }) => ({
      id: name,
      name: snakeCaseToTitleCase(name),
      score,
    })) ?? [];

  const columns = [
    {
      field: "score",
      headerName: "Score",
      width: 100,
      renderCell: (params) => {
        return (
          <Tooltip
            arrow
            placement="right"
            componentsProps={{
              arrow: {
                sx: {
                  color: ({ palette }) => palette.background.paper,
                },
              },
              tooltip: {
                sx: {
                  backgroundColor: ({ palette }) => palette.background.paper,
                  boxShadow: (theme) => theme.shadows[1],
                },
              },
            }}
            title={
              <Grid container sx={{ alignItems: "center" }} direction="column">
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="black">
                    Similar Dataset
                  </Typography>
                </Grid>
                {isLoadingEstimation || !estimation ? (
                  <Box margin={2}>
                    <CircularProgress size={16} />
                  </Box>
                ) : (
                  <DatasetGauge
                    height={48}
                    width={48}
                    value={estimation[params.id] ?? 0}
                    shortLabel
                    fontSize={10}
                    sx={{ color: common.white }}
                    textColor={common.white}
                  />
                )}
              </Grid>
            }
          >
            <Box width={56}>
              <DatasetGauge
                height={56}
                width={56}
                value={params.value}
                shortLabel
                fontSize={12}
              />
            </Box>
          </Tooltip>
        );
      },
    },
    { field: "name", headerName: "Metric", flex: 5 },
  ];

  return <DataGrid rows={rows} columns={columns} loading={isLoading} />;
};
