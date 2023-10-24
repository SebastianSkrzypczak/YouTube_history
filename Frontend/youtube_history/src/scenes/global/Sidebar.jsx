import React from "react";
import { useState } from "react";
import { ProSidebar, Menu, MenuItem } from "react-pro-sidebar";
import { Box, IconButton, Typography, useTheme } from "@mui/material";
import { Link } from "react-router-dom";
import "react-pro-sidebar/dist/css/styles.css";
import { tokens } from "../../theme";
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined"; 
import HelpOutlinedIcon from "@mui/icons-material/HelpOutlined"; 
import PieChartOutlineOutlinedIcon from "@mui/icons-material/PieChartOutlineOutlined"; 
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined"; 
import BarChartOutlinedIcon from "@mui/icons-material/BarChartOutlined"; 
import StackedLineChartIcon from '@mui/icons-material/StackedLineChart';
import AccessTimeOutlinedIcon from '@mui/icons-material/AccessTimeOutlined';
import AssessmentOutlinedIcon from '@mui/icons-material/AssessmentOutlined';
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined';


const Item = ({title, to, icon, selected, setSelected}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode)

  return (
    <MenuItem
      active={selected === title}
      style={{
        color: colors.grey[100],
      }}
      onClick={() => setSelected(title)}
      icon={icon}
    >
      <Typography>{title}</Typography>
      <Link to={to} />
    </MenuItem>
  );
};

const Sidebar = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [isCollapsed, setIsCollapsed] = useState(false);
    const [selected, setSelected] = useState('Dashboard');
    
    return (
        <Box
            sx = {{
                position: 'flex',
                height: "100vh",
                "& .pro-sidebar-inner": {
                    background: `${colors.primary[400]} !important`
                },
                "& .pro-icon-wrapper": {
                    backgroundColor: 'transparent !important' 
                },
                "& .pro-inner-item": {
                    padding: "5px 35px 5px 20px !important"
                },
                "& .pro-inner-item:hover": {
                    color: "#868dfb !important"
                },
                "& .pro-menu-item.active": {
                    color: "#6870fa !important"
                }
            }}
        >
         <ProSidebar collapsed = {isCollapsed}>
            <Menu iconShape="sqaure">
                {/* LOGO AND MENU ICON */}
                <MenuItem
                    onClick={() => setIsCollapsed(!isCollapsed)}
                    icon={isCollapsed ? <MenuOutlinedIcon /> : undefined}    
                    style={{
                        margin: "10px 0 20px 0",
                        color: colors.grey[100]
                    }}
                >
                    {!isCollapsed && (
                        <Box 
                        display='flex'
                        justifyContent='space-between'
                        alignItems='center'
                        ml = '15px'
                        >
                            <img 
                            alt = 'profile-user'
                            width='50px'
                            height='50px'
                            src='https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/YouTube_social_white_squircle_%282017%29.svg/450px-YouTube_social_white_squircle_%282017%29.svg.png?20220808215450'
                            style={{borderRadius: '50%'}}
                            />
                            <Typography variant="h1" color={colors.grey[100]} margin={2}>
                                STATS
                            </Typography>
                            <IconButton onClick={() => setIsCollapsed(!isCollapsed)}>
                                <MenuOutlinedIcon />
                            </IconButton>
                        </Box>
                    )}
                </MenuItem>

                {/* USER */}
                {/* {!isCollapsed && (
                    <Box mb="25px">
                        <Box display='flex' justifyContent='center' alignItems='center'>
                            <img 
                            alt = 'profile-user'
                            width='100px'
                            height='100px'
                            src='https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/YouTube_social_white_squircle_%282017%29.svg/450px-YouTube_social_white_squircle_%282017%29.svg.png?20220808215450'
                            style={{cursor: 'pointer', borderRadius: '50%'}}
                            />
                        </Box>

                        <Box textAlign='center'>
                            <Typography variant="h2" color={colors.grey[100]} fontWeight='bold' sx={{m: "10px 0 0 0"}}>
                                USER
                            </Typography>
                            <Typography variant="h5" color={colors.greenAccent[500]}>
                                Admin
                            </Typography>
                        </Box>
                    </Box>
                )} */}

            {/* MENU ITEMS */}
            <Box paddingLeft={isCollapsed ? undefined: "10%"}>
                <Item 
                    title="Dashboard"
                    to="/"
                    icon={<HomeOutlinedIcon />}
                    selected={selected}
                    setSelected={setSelected}
                />
                <Item 
                    title="Line Chart"
                    to="/line"
                    icon={<StackedLineChartIcon />}
                    selected={selected}
                    setSelected={setSelected}
                />
                <Item 
                    title="Pie"
                    to="/pie"
                    icon={<PieChartOutlineOutlinedIcon />}
                    selected={selected}
                    setSelected={setSelected}
                />
                <Item 
                    title="Bar"
                    to="/bar"
                    icon={<BarChartOutlinedIcon />}
                    selected={selected}
                    setSelected={setSelected}
                />
                <Item 
                    title="Access"
                    to="/access"
                    icon={<AccessTimeOutlinedIcon />}
                    selected={selected}
                    setSelected={setSelected}
                />
                <Item 
                    title="Assessment"
                    to="/assessment"
                    icon={<AssessmentOutlinedIcon />}
                    selected={selected}
                    setSelected={setSelected}
                />
                <Item 
                    title="Calendar"
                    to="/calendar"
                    icon={<CalendarMonthOutlinedIcon />}
                    selected={selected}
                    setSelected={setSelected}
                />
                <Item 
                    title="Help"
                    to="/help"
                    icon={<HelpOutlinedIcon />}
                    selected={selected}
                    setSelected={setSelected}
                />
            </Box>
            </Menu>
         </ProSidebar>
        </Box>
    );
}

export default Sidebar;