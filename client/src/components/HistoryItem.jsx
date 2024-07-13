import { Box } from "@mui/material";
import { blue } from "@mui/material/colors";

export const HistoryItem = () => {
  return (
    <Box
      minHeight={100}
      sx={{
        ":hover": { backgroundColor: "action.hover" },
        borderRadius: 0,
      }}
    >
      Hello
    </Box>
  );
};
