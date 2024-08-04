import { getDatasetIssue } from "api/api";
import { useDatasetIssues } from "api/query";
import { useQueryClient } from "react-query";

const { useEffect, useState, useMemo } = require("react");

export const useIssues = (datasetId) => {
  // issues -> missingValue, inconsistency, typo, outlier

  const { data: issues, isLoading } = useDatasetIssues();
  const [isLoadingIssues, setLoadingIssues] = useState();
  const [data, setData] = useState({});

  const queryClient = useQueryClient();

  const headers = useMemo(
    () => (issues ? ["column", ...issues] : []),
    [issues],
  );

  useEffect(() => {
    const computeIssues = async () => {
      setLoadingIssues(true);
      const issuesData = {};

      console.log("issueData", "loading issue data", { issuesData });

      for (const issue of issues ?? []) {
        try {
          const issueData = await queryClient.fetchQuery({
            queryKey: ["dataset", datasetId, "issues", issue],
            queryFn: () => getDatasetIssue(datasetId, issue),
          });

          Object.keys(issueData).forEach((column) => {
            issuesData[column] ??= { column };
            issuesData[column][issue] = issueData[column];
          });
        } catch (error) {}
      }

      setData(issuesData);
      console.log("issueData", { issuesData });
      setLoadingIssues(false);
    };

    computeIssues();
  }, [datasetId, headers, issues, queryClient]);

  // const { data: missingValueData, isLoading: isLoadingMissingValue } =
  //   useMissingValue(datasetId);
  // const { data: inconsistencyData, isLoading: isLoadingInconcistency } =
  //   useInconsistency(datasetId, !!missingValueData);
  // const { data: outlierData, isLoading: isLoadingOutlier } = useOutlier(
  //   datasetId,
  //   !!missingValueData,
  // );
  // const { data: typoData, isLoading: isLoadingTypo } = useTypo(
  //   datasetId,
  //   !!missingValueData,
  // );

  // useEffect(() => {
  //   const columns = missingValueData ? Object.keys(missingValueData) : [];
  //   const result = {};
  //   columns.forEach((column) => {
  //     result[column] = {
  //       missingValue: (missingValueData ?? {})[column],
  //       inconsistency: (inconsistencyData ?? {})[column],
  //       outlier: (outlierData ?? {})[column],
  //       typo: (typoData ?? {})[column],
  //     };
  //   });

  //   setData((data) => ({ ...data, data: result }));
  // }, [inconsistencyData, missingValueData, outlierData, typoData]);

  return {
    headers,
    data,
    isLoading: isLoading || isLoadingIssues,
  };
};
