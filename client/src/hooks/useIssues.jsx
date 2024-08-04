import {
  useInconsistency,
  useMissingValue,
  useOutlier,
  useTypo,
} from "api/query";

const { useEffect, useState } = require("react");

export const useIssues = (datasetId) => {
  // issues -> missingValue, inconsistency, typo, outlier

  const [data, setData] = useState({
    headers: ["column", "missingValue", "inconsistency", "typo", "outliers"],
    data: {},
  });

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
    console.log("issues", { outlierData });
  }, [outlierData]);

  useEffect(() => {
    const columns = missingValueData ? Object.keys(missingValueData) : [];
    const result = {};
    columns.forEach((column) => {
      result[column] = {
        missingValue: (missingValueData ?? {})[column],
        inconsistency: (inconsistencyData ?? {})[column],
        outliers: (outlierData ?? {})[column],
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
