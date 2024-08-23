import { router } from "router";
import "./App.css";
import { RouterProvider } from "react-router-dom";
import { Box } from "@mui/material";
import { QueryClient, QueryClientProvider } from "react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: 10 * 60 * 1000 } },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Box>
        <RouterProvider router={router} />
      </Box>
    </QueryClientProvider>
  );
}

export default App;
