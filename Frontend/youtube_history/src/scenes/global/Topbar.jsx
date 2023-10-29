import React, { useEffect, useState } from "react";
import {Box, Icon, IconButton, Input, colors, useTheme} from "@mui/material";
import { useContext } from "react";
import { ColorModeContext, tokens } from "../../theme";
import InputBase from "@mui/material/InputBase";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined"; 
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined"; 
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined"; 
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import SearchIcon from "@mui/icons-material/Search"; 
import secondsToDhms from "../../data/conversions";
import StatBox from "../../components/StatBox";
import AccessTimeOutlined from "@mui/icons-material/AccessTimeOutlined";


const Topbar = ({isCollapsed}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const colorMode = useContext(ColorModeContext);

    const [total, setTotal] = useState(null);
    const [average, setAverage] = useState(null);
    const [count, setCount] = useState(null);


    useEffect(() => {
        fetch('http://localhost:8000/total')
            .then(response => response.json())
            .then(data => {
                const totalValue = data['total_watch_time'];
                setTotal(totalValue);
            })
            .catch(error => console.error('Error:', error));
    }, []);


    useEffect(() => {
        fetch('http://localhost:8000/average')
            .then(response => response.json())
            .then(data => {
                
                const averageValue = data['average']['average_video_duration'];
                setAverage(averageValue);
            })
            .catch(error => console.error('Error: ', error));
            }, []);
    
    useEffect(() => {
        const countValue = total/average;
        setCount(countValue);
    }, []);

    return (
    <Box
        sx={{
        //width: isCollapsed ? '100%' : 'calc(100% - 250px)',
        width: '100%',
        display: 'flex',
        position: 'fixed',
        top: 0,
        left: 0,
        zIndex: 999, 
        paddingLeft: isCollapsed ? '100px' : '300px',
        transition: 'padding-left 0.3s ease',
        }} 
        flexDirection='row'
        justifyContent='space-between'>
        <Box display = "flex" justifyContent='flex-start' p={2}>
        {/* { COUNT  */}
            <Box 
            display="flex"
            backgroundColor={colors.grey[800]}
            borderRadius="10px"
            justifyContent='left'
            marginRight={2}
            width= '22vw'
            >
                <StatBox
                    title = 'Number of watched videos!'
                    value={Math.floor(total/average)}
                />
            </Box>

        {/* { TOTAL WATCH  */}
            <Box 
            display="flex"
            backgroundColor={colors.grey[800]}
            borderRadius="10px"
            justifyContent='left'
            marginRight={2}
            width= '20vw'
            >
                <StatBox
                    title = 'Total time spend on watching!'
                    value={secondsToDhms(parseFloat(total))}
                />
            </Box>

        {/* { AVERAGE  */}
            <Box 
            display="flex"
            backgroundColor={colors.grey[800]}
            borderRadius="10px"
            justifyContent='left'
            marginRight={2}
            width= '15vw'
            >
                <StatBox
                    title = 'Duration of an average vidoe!'
                    value={secondsToDhms(parseFloat(average))}
                />
            </Box>
        </Box>

        <Box display = "flex" justifyContent="flex-end" p={2}>
        
            {/* ICONS */}
            <Box display="flex">
                <IconButton onClick={colorMode.toggleColorMode}>
                    { theme.palette.mode === 'dark' ? (
                        <DarkModeOutlinedIcon />
                    ) : (
                        <LightModeOutlinedIcon />
                    )}
                </IconButton>
                <IconButton>
                    <SettingsOutlinedIcon />
                </IconButton>
                <IconButton>
                    <PersonOutlinedIcon />
                </IconButton>
            </Box>
        </Box>
    </Box>);
};

export default Topbar;