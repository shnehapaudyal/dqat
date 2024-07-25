import axios from "axios";

const httpclient = axios.create({
  baseURL: "http://localhost:5000", // replace with your server's address
  headers: {
    "Content-Type": "application/json",
  },
});

const api = {
  post: (...args) => {
    console.log("POST", { args })
    return httpclient.post(...args);
  },
  get: (...args) => {
    console.log("GET", { args })
    return httpclient.get(...args);
  }
}

// Upload a dataset
export const uploadDataset = async (file) => {
  const formData = new FormData();
  formData.append("File", file);

  try {
    const response = await api.post("/home", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error uploading dataset:", error);
    throw error;
  }
};

// Get all dataset records
export const getAllDatasetRecords = async (page = 0, perPage = 10) => {
  try {
    const response = await api.get(
      `/datasets?page=${page + 1}&per_page=${perPage}`,
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching dataset records:", error);
    throw error;
  }
};

// Get a single dataset record
export const getSingleDatasetRecord = async (datasetId) => {
  try {
    const response = await api.get(`/dataset/${datasetId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching dataset record:", error);
    throw error;
  }
};

// Get dataset metrics
export const getDatasetMetrics = async (datasetId) => {
  try {
    const response = await api.get(`/dataset/${datasetId}/metrics`);
    return response.data;
  } catch (error) {
    console.error("Error fetching dataset metrics:", error);
    throw error;
  }
};

export const getDatasetData = async (datasetId, page, pageSize) => {
  try {
    const response = await api.get(`/dataset/${datasetId}/data?page=${page}&per_page=${pageSize}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching dataset data:", error);
    throw error;
  }
};
