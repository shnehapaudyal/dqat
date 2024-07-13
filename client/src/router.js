import { createBrowserRouter } from "react-router-dom";
import { DatasetPage, MainPage } from "pages";
import { Box } from "@mui/material";

const PageWrapper = ({ children }) => (
  <Box sx={{ height: "100vh" }}>
    {children}
  </Box>
);

export const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <PageWrapper>
        <MainPage />
      </PageWrapper>
    ),
  },
  {
    path: "/dataset/:id",
    element: (
      <PageWrapper>
        <DatasetPage />
      </PageWrapper>
    ),
  },
]);
