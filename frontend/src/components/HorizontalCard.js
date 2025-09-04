import {
  Box,
  Card,
  CardContent,
  Typography,
  Divider,
  Grid,
} from "@mui/material";
import { Link } from "react-router-dom";

export default function HorizontalCard({ data }) {
  return (
    <Card
      component={Link}
      to={`/issues/${data.id}`}
      sx={{
        display: "block",
        textDecoration: "none",
        color: "inherit",
        borderRadius: 2,
        border: "1px solid",
        borderColor: "divider",
        transition: "all 0.2s ease-in-out",
        "&:hover": {
          boxShadow: 4,
          transform: "translateY(-2px)",
        },
      }}
    >
      <Grid container>
        <Grid item xs={12}>
          <Box sx={{ display: "flex", flexDirection: "column" }}>
            <CardContent>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                {data.title}
              </Typography>

              <Divider sx={{ mb: 2 }} />

              <Typography
                variant="body2"
                color="text.secondary"
                sx={{ mb: 2 }}
              >
                {data.body}
              </Typography>

              <Typography variant="body2" color="text.secondary">
                Reported: {data.created_at}
                <br />
                Author: {data.author}
                <br />
                <em>Probability: {data.pred_confidence}</em>
                <br />
                <em>Predicted label: {data.prediction}</em>
                <br />
                <em>Actual label: {data.actual_label}</em>
              </Typography>
            </CardContent>
          </Box>
        </Grid>
      </Grid>
    </Card>
  );
}
