import { useQuery, useMutation, queryCache } from "react-query";
import * as api from "./api";

export const useUploadDataset = () => {
  const {
    mutate: uploadDataset,
    isLoading: isUploading,
    isSuccess: isUploadSuccess,
  } = useMutation(api.uploadDataset, {
    onSuccess: (result) => {
      // Invalidate the 'datasets' query key after successful upload
      queryCache.invalidateQueries(["datasets"]);
      queryCache.invalidateQueries(["dataset", result.data.dataset_id]);
    },
  });

  return { uploadDataset, isLoading: isUploading, isSuccess: isUploadSuccess };
};

export const useDatasets = () =>
  useQuery(["datasets"], () => api.getAllDatasetRecords());

export const useDataset = (datasetId) =>
  useQuery(["dataset", datasetId, "detail"], () =>
    api.getSingleDatasetRecord(datasetId),
  );

export const useDatasetMetrics = (datasetId) =>
  useQuery(["dataset", datasetId, "metric"], () =>
    api.getDatasetMetrics(datasetId),
  );

export const useDatasetData = (datasetId, page, pageSize) =>
  useQuery(["dataset", datasetId, "data"], () =>
    api.getDatasetData(datasetId, page, pageSize),
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
