import React, { useEffect } from "react";
import {
  Box,
  Button,
  Card,
  CircularProgress,
  Grid,
  Typography,
} from "@mui/material";
import { FileOpen, UploadOutlined } from "@mui/icons-material";
import { useUploadDataset } from "api/query";
import { grey } from "@mui/material/colors";
import Dropzone from "react-dropzone";
import { getFileSize } from "utils/files";

import { get, set } from "https://unpkg.com/idb-keyval@5.0.2/dist/esm/index.js";

export const FileUploadUI = () => {
  const [selectedFile, setSelectedFile] = React.useState();

  const handleFileChange = (event) => {
    if (event.target.files.length) setSelectedFile(event.target.files[0]);
  };

  const [width, height] = [64, 64];

  const startUpload = () => {
    if (selectedFile) uploadDataset(selectedFile);
  };

  const { uploadDataset, isUploading, isUploadSuccess } = useUploadDataset();

  useEffect(() => {
    if (isUploadSuccess) setSelectedFile();
  }, [isUploadSuccess]);

  useEffect(() => {
    if (selectedFile) console.log({ selectedFile });
  }, [selectedFile]);
  // const handleFileUpload = () => {
  //   console.log(selectedFile);
  //   // Implement file upload logic here
  //   // Example:
  //   // const formData = new FormData();
  //   // formData.append('file', selectedFile);
  //   // fetch('/api/upload', { method: 'POST', body: formData })
  //   //   .then(response => response.json())
  //   //   .then(data => console.log(data))
  //   //   .catch(error => console.error(error));
  // };

  return (
    <Card variant="outlined">
      <Grid container padding={4} rowGap={3}>
        <Grid item xs={12}>
          <Typography variant="h6">Upload dataset</Typography>
          <Typography variant="caption">
            Select a csv file to analyse
          </Typography>
        </Grid>
        <Grid item xs={12} sx={{ display: "block" }}>
          <Dropzone
            disabled={isUploading}
            accept={{
              "text/csv": [".csv"],
            }}
            multiple={false}
            onDrop={([file]) => {
              setSelectedFile(file);
            }}
          >
            {({ getRootProps, getInputProps }) => (
              <section {...getRootProps()}>
                <input {...getInputProps()} />

                <Grid
                  container
                  gap={2}
                  padding={2}
                  alignItems={"center"}
                  direction={"row"}
                  sx={{
                    borderWidth: 1,
                    borderColor: (!selectedFile ? grey : grey)[300],
                    borderStyle: "dashed",
                    backgroundColor: (!selectedFile ? grey : grey)[100],
                    borderRadius: 1,
                  }}
                >
                  <Grid item>
                    <Box
                      width={width}
                      height={height}
                      display={"flex"}
                      border="solid"
                      borderRadius={1}
                      sx={{
                        justifyContent: "center",
                        alignItems: "center",
                      }}
                    >
                      {isUploading ? (
                        <CircularProgress size={24} />
                      ) : !selectedFile ? (
                        <FileOpen />
                      ) : (
                        <UploadOutlined />
                      )}
                    </Box>
                  </Grid>
                  <Grid item flexGrow={1}>
                    {!selectedFile ? (
                      <Typography variant="subtitle2">Select a file</Typography>
                    ) : (
                      <Grid container direction="column" gap={0}>
                        <Typography variant="caption">
                          {selectedFile?.name ?? "File Name"}
                        </Typography>
                        <Typography variant="caption">
                          {getFileSize(selectedFile?.size)}
                        </Typography>
                        <Grid item flexShrink={1}>
                          <Button
                            variant="contained"
                            size="small"
                            disabled={isUploading}
                            onClick={(event) => {
                              startUpload();
                              event.stopPropagation();
                            }}
                          >
                            <Typography variant="caption">Upload</Typography>
                          </Button>
                        </Grid>
                      </Grid>
                    )}
                  </Grid>
                </Grid>
              </section>
            )}
          </Dropzone>
        </Grid>
      </Grid>
    </Card>
  );
};
