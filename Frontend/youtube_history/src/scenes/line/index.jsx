import { Box, Typography } from "@mui/material";
import Header from "../../components/Header";
import LineChart from "../../components/LineChart";
import React from "react";

const Line = () => {
  return (
    <Box m="20px" justifyItems='center' >
      <Header title="Line Chart" subtitle="Simple Line Chart" />
      <Box height="50vh" width="50vw">
        <LineChart />
      </Box>
    </Box>
  );
};

export default Line;