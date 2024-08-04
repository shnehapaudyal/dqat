import { getDatasetIssue } from "api/api";
import {
  useDatasetIssues,
  useInconsistency,
  useMissingValue,
  useOutlier,
  useTypo,
} from "api/query";
import { useQuery, useQueryClient } from "react-query";

const { useEffect, useState, useMemo } = require("react");

export const useIssues = (datasetId) => {
  // issues -> missingValue, inconsistency, typo, outlier

  const { data: issues, isLoading: isLoadingIssues } = useDatasetIssues();
  const [data, setData] = useState({
    headers: [],
    data: {},
  });

  const queryClient = useQueryClient();

  const headers = useMemo(
    () => (issues ? ["column", ...issues] : []),
    [issues],
  );
  useEffect(() => {
    const issuesData = { headers };

    if (issues) {
      issues.forEach((issue) => {
        const issueData = queryClient.fetchQuery({
          queryKey: ["dataset", datasetId, "issues", issue],
          queryFn: () => getDatasetIssue(datasetId, issue),
        });

        console.log(issue);
      });
    }
  }, [datasetId, issues, queryClient]);

  const { data: missingValueData, isLoading: isLoadingMissingValue } =
    useMissingValue(datasetId);
  const { data: inconsistencyData, isLoading: isLoadingInconcistency } =
    useInconsistency(datasetId, !!missingValueData);
  const { data: outlierData, isLoading: isLoadingOutlier } = useOutlier(
    datasetId,
    !!missingValueData,
  );
  const { data: typoData, isLoading: isLoadingTypo } = useTypo(
    datasetId,
    !!missingValueData,
  );

  useEffect(() => {
    const columns = missingValueData ? Object.keys(missingValueData) : [];
    const result = {};
    columns.forEach((column) => {
      result[column] = {
        missingValue: (missingValueData ?? {})[column],
        inconsistency: (inconsistencyData ?? {})[column],
        outlier: (outlierData ?? {})[column],
        typo: (typoData ?? {})[column],
      };
    });

    setData((data) => ({ ...data, data: result }));
  }, [inconsistencyData, missingValueData, outlierData, typoData]);

  return {
    data,
    isLoading:
      isLoadingMissingValue ||
      isLoadingInconcistency ||
      isLoadingOutlier ||
      isLoadingTypo,
  };
};
