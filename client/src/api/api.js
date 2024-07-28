import axios from "axios";

const httpclient = axios.create({
  baseURL: "http://localhost:5000", // replace with your server's address
  headers: {
    "Content-Type": "application/json",
  },
});

const cb = async (fc, ...args) => {
  try {
    const result = await httpclient[fc](...args);
    // console.log(fc, { args, result });
    return result;
  } catch (error) {
    console.error(fc, { args, error });
    throw error;
  }
};

const api = {
  post: (...args) => cb("post", ...args),
  get: (...args) => cb("get", ...args),
};

// Upload a dataset
export const uploadDataset = async (file) => {
  const formData = new FormData();
  formData.append("File", file);
  const response = await api.post("/home", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};

// Get all dataset records
export const getAllDatasetRecords = async (page = 0, perPage = 10) => {
  const response = await api.get(
    `/datasets?page=${page + 1}&per_page=${perPage}`,
  );
  return response.data;
};

// Get a single dataset record
export const getSingleDatasetRecord = async (datasetId) => {
  const response = await api.get(`/dataset/${datasetId}`);
  return response.data;
};

// Get dataset metrics
export const getDatasetMetrics = async (datasetId) => {
  const response = await api.get(`/dataset/${datasetId}/metrics`);
  return response.data;
};

export const getDatasetRating = async (datasetId) => {
  const response = await api.get(`/dataset/${datasetId}/overall_rating`);
  return response.data;
};

export const getDatasetData = async (datasetId, page, pageSize) => {
  const response = await api.get(
    `/dataset/${datasetId}/data?page=${page}&per_page=${pageSize}`,
  );
  return response.data;
};

export const getDatasetType = async (datasetId) => {
  const response = await api.get(`/dataset/${datasetId}/types`);
  return response.data;
};

export const getDatasetStats = async (datasetId) => {
  const response = await api.get(`/dataset/${datasetId}/stats`);
  return response.data;
};

export const getMissingValue = async (datasetId) => {
  const response = await api.get(`/dataset/${datasetId}/issues/missing`);
  return response.data;
};

export const getInconsistency = async (datasetId) => {
  const response = await api.get(`/dataset/${datasetId}/issues/inconsistency`);
  return response.data;
};

export const getOutlier = async (datasetId) => {
  const response = await api.get(`/dataset/${datasetId}/issues/outlier`);
  return response.data;
};

export const getTypo = async (datasetId) => {
  const response = await api.get(`/dataset/${datasetId}/issues/typo`);
  return response.data;
};
