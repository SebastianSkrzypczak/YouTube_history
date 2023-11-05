import { Box, Button, IconButton, Typography, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import { useNavigate } from "react-router-dom";
import React, { useEffect } from "react";
import LineChart from "../../components/LineChart";
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import BarChart from "../../components/BarChart";
import secondsToDhms from "../../data/conversions"
import { useState } from "react";
import VideosComp from "../../components/Videos";


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
            <Box
                display="grid"
                gridTemplateColumns="repeat(12, 1fr)"
                gridAutoRows="150px"
                gap="25px"
            >

                {/* ROW 2 */}
                <Box 
                    gridColumn='span 12'
                    gridRow='span 2'
                    //backgroundColor={colors.primary[400]}
                    display='block'
                    //flexDirection='column'
                    justifyContent='center'
                    alignContent='center'
                    alignItems='center'
                    borderRadius='20px'
                >
                    <VideosComp isDashboard={true}/>
                    {/* <Button variant="outlined" startIcon={<InfoOutlinedIcon />}
                        sx= {{
                        marginBottom: "50px",
                        backgroundColor: colors.grey[700],
                        color: colors.grey[100],
                        padding: '10px'}}
                        onClick={() => handleButtonClick('/videos')}>
                        More details
                    </Button> */}
                </Box>
                
                {/* ROW 3 */}
                <Box 
                    gridColumn='span 6'
                    gridRow='span 2'
                    backgroundColor={colors.grey[800]}
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
                        backgroundColor: colors.grey[700],
                        color: colors.grey[100]}}
                        onClick={() => handleButtonClick('/line')}>
                        More details
                    </Button>
                </Box>
                <Box 
                    gridColumn='span 6'
                    gridRow='span 2'
                    backgroundColor={colors.grey[800]}
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
                        backgroundColor: colors.grey[700],
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