import { router } from "router";
import "./App.css";
import { RouterProvider } from "react-router-dom";
import { Box } from "@mui/material";

function App() {
  return (
    <Box>
      <RouterProvider router={router} />
    </Box>
  );
}

export default App;
