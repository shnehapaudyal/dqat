import { useQuery as useApi, useMutation, useQueryClient } from "react-query";
import * as api from "./api";

// const useApi = (...args) => useQuery(...args);

export const useUploadDataset = () => {
  const client = useQueryClient();

  const {
    mutate: uploadDataset,
    isLoading: isUploading,
    isSuccess: isUploadSuccess,
    isError: isUploadError,
  } = useMutation(api.uploadDataset, {
    onSuccess: () => {
      // Invalidate the 'datasets' query key after successful upload
      client.invalidateQueries(["datasets"], { refetchActive: true, refetchInactive: true });
    },
  });

  return { uploadDataset, isUploading, isUploadSuccess, isUploadError };
};

export const useDatasets = () =>
  useApi(["datasets"], () => api.getAllDatasetRecords());

export const useDatasetTags = (datasetId) => useApi(["dataset", datasetId, "tags"], () => api.getDatasetTags(datasetId))

export const useDatasetMetricEstimation = (datasetId) => useApi(["dataset", datasetId, "metric", "estimation"], () => api.getDatasetMetricsEstimation(datasetId))

export const useDatasetReadability = (datasetId) => useApi(["dataset", datasetId, "metric", "readability"], () => api.getDatasetReadability(datasetId))

export const useDataset = (datasetId) =>
  useApi(["dataset", datasetId, "detail"], () =>
    api.getSingleDatasetRecord(datasetId),
  );

export const useDatasetRating = (datasetId) =>
  useApi(["dataset", datasetId, "rating"], () =>
    api.getDatasetRating(datasetId),
  );

export const useDatasetMetrics = (datasetId) =>
  useApi(["dataset", datasetId, "metric"], () =>
    api.getDatasetMetrics(datasetId),
  );

export const useDatasetData = (datasetId) =>
  useApi(["dataset", datasetId, "data"], () =>
    api.getDatasetData(datasetId),
  );

export const useDatasetTypes = (datasetId) =>
  useApi(["dataset", datasetId, "types"], () => api.getDatasetType(datasetId));

export const useDatasetStat = (datasetId) =>
  useApi(["dataset", datasetId, "stats"], () => api.getDatasetStats(datasetId));
export const useDatasetIssues = () =>
  useApi(["issues"], () => api.getDatasetIssues());

export const useMissingValue = (datasetId, enabled) =>
  useApi(
    ["dataset", datasetId, "issues", "missingValue"],
    () => api.getMissingValue(datasetId),
    { enabled },
  );
export const useInconsistency = (datasetId, enabled) =>
  useApi(
    ["dataset", datasetId, "issues", "inconsistency"],
    () => api.getInconsistency(datasetId),
    { enabled },
  );
export const useOutlier = (datasetId, enabled) =>
  useApi(
    ["dataset", datasetId, "issues", "outlier"],
    () => api.getOutlier(datasetId),
    { enabled },
  );
export const useTypo = (datasetId, enabled) =>
  useApi(
    ["dataset", datasetId, "issues", "typo"],
    () => api.getTypo(datasetId),
    { enabled },
  );

// Example of using custom fetcher for API requests

// export const useDatasets = () => {
//   // Upload dataset mutation
//   const { mutate: uploadDataset, isLoading: isUploading, isSuccess: isUploadSuccess } = useMutation(api.uploadDataset, {
//     onSuccess: () => {
//       // Invalidate the 'datasets' query key after successful upload
//       queryCache.invalidateQueries(["datasets"]);
//     },
//   });

//   // Get all dataset records query
//   const {
//     data: allDatasetsData,
//     isLoading: allDatasetsLoading,
//     isError: allDatasetsError,
//   } = useQuery(["datasets"], api.getAllDatasetRecords, {
//     keepPreviousData: true, // Keep previous data when refetching
//   });

//   // Get single dataset record query
//   const getSingleDatasetRecordQuery = async (datasetId) => {
//     const response = await api.getSingleDatasetRecord(datasetId);
//     return response.data;
//   };

//   // Get dataset metrics query
//   const getDatasetMetricsQuery = async (datasetId) => {
//     const response = await api.getDatasetMetrics(datasetId);
//     return response.data;
//   };

//   return {
//     uploadDataset,
//     isUploading,
//     isUploadSuccess,
//     allDatasetsData,
//     allDatasetsLoading,
//     allDatasetsError,
//     getSingleDatasetRecordQuery,
//     getDatasetMetricsQuery,
//   };
// };
