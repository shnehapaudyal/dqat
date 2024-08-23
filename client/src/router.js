import { createBrowserRouter, Link, useLocation } from "react-router-dom";
import { DatasetPage, MainPage } from "pages";
import { AppBar, Box, IconButton, Toolbar, Typography } from "@mui/material";
import { ArrowBack, Home } from "@mui/icons-material";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

const MyToolbar = ({ title}) => {
  const location = useLocation();

  return (
    <AppBar position="static">
      <Toolbar>
        {location.pathname !== "/" ? (
          <IconButton
            edge="start"
            color="inherit"
            aria-label="back"
            component={Link}
            to="/"
          >
            <ArrowBack />
          </IconButton>
        ) : (
          <IconButton
            edge="start"
            color="inherit"
            aria-label="back"
            component={Link}
          >
            <Home />
          </IconButton>
        )}
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          {title}
        </Typography>
        {/* Add your toolbar content here */}
      </Toolbar>
    </AppBar>
  );
}

const PageWrapper = ({ title, children }) => (
  <Box sx={{ height: "100vh" }}>
    <MyToolbar title={title}/>
    <Box>{children}</Box>
  </Box>
);

export const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <PageWrapper title="DQAT">
        <MainPage />
      </PageWrapper>
    ),
  },
  {
    path: "/dataset/:id",
    element: (
      <PageWrapper title="Dataset">
        <DatasetPage />
      </PageWrapper>
    ),
  },
]);
