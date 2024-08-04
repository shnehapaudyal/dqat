import { mdiTableLarge } from "@mdi/js";
import Icon from "@mdi/react";
import { Card, Grid, Tab, Tabs, Typography } from "@mui/material";
import { useDataset } from "api/query";
import { CustomTabPanel } from "components/TabPanel";
import { useParams, useSearchParams } from "react-router-dom";
import { getFileSize } from "utils/files";
import { DatasetMetricsPage } from "./DatasetMetricsPage";
import { DatasetDataPage } from "./DatasetDataPage";
import { useEffect, useRef } from "react";
import { DatasetIssuesPage } from "./DatasetIssuesPage";
import { grey } from "@mui/material/colors";

export const DatasetPage = () => {
  const { id } = useParams("id");
  const [searchParams, setSearchParams] = useSearchParams();

  const { data: dataset } = useDataset(id);

  const selectedTab = searchParams.get("tab");

  // datetime in format 2024-07-21 14:56:17.030695
  const created = dataset?.created_at.split(".")[0];

  const filesize = getFileSize(dataset?.size);

  const tabsRef = useRef();

  useEffect(() => {
    console.log({ dataset, filesize });
  }, [dataset, filesize]);

  return (
    <Grid container justifyContent="space-around" padding={4}>
      <Grid item xs={12}>
        <Card sx={{ padding: 2 }} variant="outlined">
          <Grid container columnGap={2} alignItems="center">
            <Grid item flexShrink={1}>
              <Icon path={mdiTableLarge} size={1} />
            </Grid>
            <Grid item xs={11}>
              <Typography variant="h5">{dataset?.filename}</Typography>
            </Grid>
            <Grid item flexShrink={1}>
              <Icon size={1} />
            </Grid>
            <Typography variant="caption">
              {`${filesize} | ${dataset?.file_type} | ${created}`}
            </Typography>
          </Grid>
        </Card>
      </Grid>
      <Grid xs={12} item marginTop={2}>
        <Tabs
          value={selectedTab}
          onChange={(_, newTab) => {
            setSearchParams(`tab=${newTab}`);
            const tabs = tabsRef.current;
            const offset = tabsRef.current?.offsetTop;
            if (tabs) {
              tabsRef.current?.animate({
                scrollToTop: offset,
              });
            }
          }}
          ref={tabsRef}
        >
          <Tab label="Data" value="data" />
          <Tab label="Quality" value="quality" />
          <Tab label="Issues" value="issues" />
        </Tabs>
      </Grid>
      <Grid item xs={12}>
        <CustomTabPanel index="data" value={selectedTab}>
          <DatasetDataPage datasetId={id} />
        </CustomTabPanel>
        <CustomTabPanel index="quality" value={selectedTab}>
          <DatasetMetricsPage datasetId={id} />
        </CustomTabPanel>
        <CustomTabPanel index="issues" value={selectedTab}>
          <DatasetIssuesPage datasetId={id} />
        </CustomTabPanel>
      </Grid>
    </Grid>
  );
};
