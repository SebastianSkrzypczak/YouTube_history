import { Box, Button, IconButton, Typography, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import Header from '../../components/Header';
import React from "react";
import LineChart from "../../components/LineChart"
import BarChartChart from "../../components/BarChart"
import PieChart from "../../components/PieChart"
import StatBox from "../../components/StatBox"
import EmailIcon from "@mui/icons-material/"

const Dashboard = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    return (
    <Box m="20px">
        <Box display='flex' justifyContent='space-between' alignItems='center'  >
            <Header title="DASHBOARD" subtitle="Welcome to your dashboard" />
        </Box>
        <Box>
            <Button
                sx = {{ backgroundColor: colors.blueAccent[700], color: colors.grey[100], fontSize: "14px", fontWeight: "bold"}}
            >
                Download Raports
            </Button>
        </Box>

        {/* GRID  */}
        <Box
            display="grid"
            gridTemplateColumns="repeat(12, 1fr)"
            gridAutoRows="140px"
            gap="20px"
        >
        {/* ROW 1 */}
            <Box gridColumn="span 3"
            backgroundColor={colors.primary[400]}
            display="flex"
            alignItems="center"
            justifyContent="center"
            >
                <StatBox
                    title = "title"
                    subtitle = "subtitle"
                    value = "value"
                    icon = {
                        <EmailIcon/>
                    }
                />
            </Box>

        </Box>
    </Box>
    );
}

export default Dashboard;