import { Box, Button, IconButton, Typography, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import { useNavigate } from "react-router-dom";
import Header from '../../components/Header';
import React, { useEffect } from "react";
import LineChart from "../../components/LineChart";
import PieChart from "../../components/PieChart";
import StatBox from "../../components/StatBox";
import DownloadSharpIcon from '@mui/icons-material/DownloadSharp';
import AccessTimeOutlinedIcon from '@mui/icons-material/AccessTimeOutlined';
import TimerOutlinedIcon from '@mui/icons-material/TimerOutlined';
import OndemandVideoOutlinedIcon from '@mui/icons-material/OndemandVideoOutlined';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import BarChart from "../../components/BarChart";
import secondsToDhms from "../../data/conversions"
import { useState } from "react";


const Dashboard = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    const [total, setTotal] = useState(null);
    const [average, setAverage] = useState(null);
    const [videosCount, setVideosCount] = useState(null);

    const navigate = useNavigate();

    const handleButtonClick = (path) => {
        navigate(path);
    }

    useEffect(() => {
        fetch('http://localhost:8000/default')
            .then(response => response.json())
            .then(data => {
                const totalValue = secondsToDhms(parseFloat(data['total']['total_watch_time']));
                setTotal(totalValue);
                const averageValue = secondsToDhms(parseFloat(data['average']['average_video_duration']));
                setAverage(averageValue);
                const videosCountValue = Math.floor(parseFloat(data['total']['total_watch_time']) / data['average']['average_video_duration'])
                setVideosCount(videosCountValue)
            })
            .catch(error => console.error('Error:', error));
    }, []);

    return (
        <Box m="20px">
            {/* <Box display='flex' justifyContent='space-between' alignItems='center' marginBottom="20px" >
                <Header title="DASHBOARD" subtitle="Welcome to your dashboard" />
                <Button
                    sx = {{ 
                        backgroundColor: colors.blueAccent[700],
                        color: colors.grey[100],
                        fontSize: "14px",
                        fontWeight: "bold",
                        padding: "10px 20px",
                        marginBottom: "20px"
                        }}
                >
                <DownloadSharpIcon sx={{mr: "10px"}} />
                    Download Raport
                </Button>
            </Box> */}

            {/* GRID  */}
            <Box
                display="grid"
                gridTemplateColumns="repeat(12, 1fr)"
                gridAutoRows="140px"
                gap="15px"
            >

                {/* ROW 1 */}
                <Box gridColumn="span 4"
                backgroundColor={colors.primary[400]}
                display="flex"
                alignItems="center"
                justifyContent="center"
                borderRadius='20px'
                >
                    <StatBox
                        title = "Total watch time"
                        subtitle = "total time spent watching"
                        value = {total}
                        icon = {
                            <AccessTimeOutlinedIcon/>
                        }
                    />
                </Box>
                <Box gridColumn="span 4"
                backgroundColor={colors.primary[400]}
                display="flex"
                alignItems="center"
                justifyContent="center"
                borderRadius='20px'
                >
                    <StatBox
                        title = "Average watch time"
                        subtitle = "average video duration"
                        value = {average}
                        icon = {
                            <TimerOutlinedIcon/>
                        }
                    />
                </Box>
                <Box gridColumn="span 4"
                backgroundColor={colors.primary[400]}
                display="flex"
                alignItems="center"
                justifyContent="center"
                borderRadius='20px'
                >
                    <StatBox
                        title = "Watched Videos"
                        subtitle = "total count of vidoes"
                        value = {videosCount}
                        icon = {
                            <OndemandVideoOutlinedIcon/>
                        }
                    />
                </Box>

                {/* ROW 2 */}
                <Box 
                    gridColumn='span 6'
                    gridRow='span 2'
                    backgroundColor={colors.primary[400]}
                    display='flex'
                    flexDirection='column'
                    alignContent='center'
                    alignItems='center'
                    justifyContent='center'
                    borderRadius='20px'
                >
                    <LineChart isDashboard={true}/>
                    <Button variant="outlined" startIcon={<InfoOutlinedIcon />}
                        sx= {{
                        marginBottom: "50px",
                        backgroundColor: colors.blueAccent[700],
                        color: colors.grey[100]}}
                        onClick={() => handleButtonClick('/line')}>
                        More details
                    </Button>
                </Box>
                <Box 
                    gridColumn='span 6'
                    gridRow='span 2'
                    backgroundColor={colors.primary[400]}
                    display='flex'
                    flexDirection='column'
                    alignContent='center'
                    alignItems='center'
                    justifyContent='center'
                    borderRadius='20px'
                >
                    <BarChart isDashboard = {true}/>
                    <Button variant="outlined" startIcon={<InfoOutlinedIcon />}
                        sx= {{
                        marginBottom: "50px",
                        backgroundColor: colors.blueAccent[700],
                        color: colors.grey[100]}}
                        onClick={() => handleButtonClick('/bar')}>
                        More details
                    </Button>
                </Box>
            </Box>
        </Box>
    );
}

export default Dashboard;