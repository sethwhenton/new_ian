import { Box, CircularProgress, Typography, Stack } from "@mui/material";

export default function DataLoading({ message = "Fetching data..." }) {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "40vh",
      }}
    >
      <Stack direction="row" spacing={2} alignItems="center">
        <CircularProgress size={48} thickness={5} color="primary" />
        <Typography variant="subtitle1" color="text.secondary">
          {message}
        </Typography>
      </Stack>
    </Box>
  );
}
