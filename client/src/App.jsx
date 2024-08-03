import { router } from "router";
import "./App.css";
import { RouterProvider, useLocation, Link } from "react-router-dom";
import { Box, AppBar, Toolbar, IconButton } from "@mui/material";
import { QueryClient, QueryClientProvider } from "react-query";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";

const queryCleint = new QueryClient({
  defaultOptions: { queries: { staleTime: 10 * 60 * 1000 } },
});

function App() {
  return (
    <QueryClientProvider client={queryCleint}>
      <Box>
        <RouterProvider router={router} />
      </Box>
    </QueryClientProvider>
  );
}

export default App;
