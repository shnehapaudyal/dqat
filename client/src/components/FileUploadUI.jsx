import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Card,
  CircularProgress,
  Grid,
  Typography,
} from "@mui/material";
import Add from "@mui/icons-material/Add";
import { DescriptionTwoTone, UploadFile } from "@mui/icons-material";
import { useDatasets, useUploadDataset } from "api/query";
import { red } from "@mui/material/colors";

export const FileUploadUI = () => {
  const [selectedFile, setSelectedFile] = React.useState();

  const handleFileChange = (event) => {
    if (event.target.files.length) setSelectedFile(event.target.files[0]);
  };

  const [width, height] = [64, 64];

  const startUpload = async () => {
    if (selectedFile) uploadDataset(selectedFile);
  };

  const { uploadDataset, isUploading } = useUploadDataset();

  useEffect(() => {
    if (selectedFile) console.log(selectedFile);
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
      <Grid container padding={4}>
        <Grid item flexGrow={10}>
          <input
            accept="*"
            type="file"
            id="contained-button-file"
            onChange={handleFileChange}
            hidden
          />
          <label htmlFor="contained-button-file">
            <Grid
              container
              spacing={2}
              padding={2}
              sx={{
                color: "primary.main",
                // borderColor: "primary.main",
                ":hover": {
                  // borderColor: "primary.light",
                  color: "primary.light",
                },
              }}
            >
              <Grid item xs={12}>
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
                  <Add sx={{ height: height / 2, width: width / 2 }} />
                </Box>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="h5">Select a file</Typography>
              </Grid>
            </Grid>
          </label>
        </Grid>
        {!!selectedFile && (
          <Grid item flexGrow={1}>
            <Card variant="outlined">
              <Grid
                container
                sx={{
                  color: "primary.main",
                  padding: 2,
                }}
                gap={1}
                direction="row"
                columns={12}
              >
                <Grid item container xs={6}>
                  <Grid item>
                    <DescriptionTwoTone sx={{ width: 56, height: 56 }} />
                  </Grid>
                  <Grid item container direction="column" xs={6}>
                    <Grid item>{selectedFile.name}</Grid>
                    <Grid
                      item
                    >{`${(selectedFile.size / (1024 * 1024 * 1024)).toFixed(2)} MB`}</Grid>
                    <Grid item>{selectedFile.type}</Grid>
                  </Grid>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    variant="contained"
                    startIcon={
                      isUploading ? (
                        <CircularProgress size="20px" />
                      ) : (
                        <UploadFile />
                      )
                    }
                    onClick={startUpload}
                    disabled={isUploading}
                  >
                    Upload
                  </Button>
                </Grid>
              </Grid>
            </Card>
          </Grid>
        )}
      </Grid>
    </Card>
  );
};
