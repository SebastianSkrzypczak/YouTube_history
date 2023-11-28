import { Box, Typography } from "@mui/material";
import Header from "../../components/Header";
import PieChart from "../../components/PieChart";
import React from "react";

const Pie = () => {
  return (
    <Box m="20px" justifyItems='center' >
      <Header title="Pie Chart" subtitle="Simple Pie Chart" />
      <Box height="50vh" width="50vw">
        <PieChart />
      </Box>
    </Box>
  );
};

export default Pie;