import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  CircularProgress,
  Grid,
  IconButton,
  Typography,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import Add from "@mui/icons-material/Add";
import {
  BorderColor,
  Description,
  DescriptionTwoTone,
  UploadFile,
} from "@mui/icons-material";
import { blue } from "@mui/material/colors";

export const FileUploadUI = () => {
  const [selectedFile, setSelectedFile] = React.useState();

  const handleFileChange = (event) => {
    if (event.target.files.length) setSelectedFile(event.target.files[0]);
  };

  const [width, height] = [64, 64];

  const startUpload = async () => {
    setUploading(true);
    await new Promise((resolve) => {
      setTimeout(resolve, 2000);
    });
    setUploading(false);
  };
  const [isUploading, setUploading] = useState(false);

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
    <Grid
      container
      rowGap={2}
      direction="row"
      sx={{
        borderWidth: 3,
        borderStyle: "dashed",
        borderColor: "primary.main",
        borderRadius: 2,
        height: "100%",
        padding: 4,
        gap: 4,
      }}
    >
      <Grid item xs={12} sx={{}}>
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
            sx={{
              color: "primary.main",
              borderColor: "primary.main",
              ":hover": {
                borderColor: "primary.light",
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

      {selectedFile && (
        <Grid
          container
          item
          sx={{
            color: "primary.main",
            borderWidth: "1px",
            borderColor: "primary.main",
            borderStyle: "solid",
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
                isUploading ? <CircularProgress size="20px" /> : <UploadFile />
              }
              onClick={startUpload}
              disabled={isUploading}
            >
              Upload
            </Button>
          </Grid>
        </Grid>
      )}
    </Grid>
  );
};
