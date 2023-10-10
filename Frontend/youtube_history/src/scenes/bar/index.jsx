import { Box, Typography } from "@mui/material";
import Header from "../../components/Header";
import BarChart from "../../components/BarChart";
import React from "react";

const Bar = () => {
  return (
    <Box m="20px" justifyItems='center' >
      <Header title="Bar Chart" subtitle="Simple Bar Chart" />
      <Box height="50vh" width="50vw">
        <BarChart />
      </Box>
    </Box>
  );
};

export default Bar;