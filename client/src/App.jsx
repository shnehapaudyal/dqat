import { router } from "router";
import "./App.css";
import { RouterProvider } from "react-router-dom";
import { Box } from "@mui/material";
import { QueryClient, QueryClientProvider } from "react-query";

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
