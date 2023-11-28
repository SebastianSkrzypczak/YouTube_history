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
import SmartDisplayOutlinedIcon from '@mui/icons-material/SmartDisplayOutlined';



const Item = ({title, to, icon, selected, setSelected}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode)
    const [isHovered, setIsHovered] = useState(false)

  return (
    <MenuItem
      active={selected === title}
      style={{
        backgroundColor: isHovered ? colors.grey[700] : 'transparent',
        borderRadius: '10px',
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={() => setSelected(title)}
      icon={icon}
    >
      <Typography>{title}</Typography>
      <Link to={to} />
    </MenuItem>
  );
};

const Sidebar = ({isCollapsed, setIsCollapsed}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    //const [isCollapsed, setIsCollapsed] = useState(false);
    const [selected, setSelected] = useState('Dashboard');
    
    return (
        <Box
            sx = {{
                position: 'fixed',
                top: 0,
                left: 0,
                bottom: 0,
                zIndex: 1000,
                "& .pro-sidebar-inner": {
                    background: `${colors.grey[900]} !important`,
                },
                "& .pro-icon-wrapper": {
                    backgroundColor: 'transparent !important' 
                },
                
                "& .pro-menu-item.active": {
                    backgroundColor: `${colors.grey[800]} !important`
                }
            }}
        >
         <ProSidebar 
            collapsed = {isCollapsed}
            style = {{height: "100vh"}}
            >
            <Menu iconShape='square'>
                {/* LOGO AND MENU ICON */}
                <MenuItem
                    onClick={() => setIsCollapsed(!isCollapsed)}
                    icon={isCollapsed ? <MenuOutlinedIcon style = {{fontSize: '30'}}/> : undefined}    
                    style={{
                        margin: "10px 0 20px 0",
                        color: colors.grey[100]
                    }}
                >
                    {!isCollapsed && (
                        <Box 
                        display='flex'
                        justifyContent='space-evenly'
                        alignItems='center'
                        ml = '15px'
                        >
                            <IconButton onClick={() => setIsCollapsed(!isCollapsed) }>
                                <MenuOutlinedIcon style={{fontSize: '30'}}/>
                            </IconButton>
                            <img 
                            alt = 'profile-user'
                            width='50px'
                            height='50px'
                            src='https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/YouTube_social_white_squircle_%282017%29.svg/450px-YouTube_social_white_squircle_%282017%29.svg.png?20220808215450'
                            style={{borderRadius: '25'}}
                            />
                            <Typography variant="h3" fontStyle='italic' >
                                STATS
                            </Typography>
                        </Box>
                    )}
                </MenuItem>

            {/* MENU ITEMS */}
            <Box 
                paddingLeft={"5%"}
                paddingRight={"5%"}
            >
                <Item 
                    title="Dashboard"
                    to="/"
                    icon={<HomeOutlinedIcon style={{fontSize: '30', marginRight: '10px'}}/>}
                    selected={selected}
                    setSelected={setSelected}
                />
                <Item
                    title='TOP VIDEOS'
                    to='/videos'
                    icon={<SmartDisplayOutlinedIcon style = {{fontSize: '30', marginRight: '10px'}} />}
                    selected={selected}
                    setSelected={setSelected}
                />
                <Item 
                    title="Line Chart"
                    to="/line"
                    icon={<StackedLineChartIcon style={{fontSize: '30', marginRight: '10px'}} />}
                    selected={selected}
                    setSelected={setSelected}
                />
                <Item 
                    title="Pie"
                    to="/pie"
                    icon={<PieChartOutlineOutlinedIcon style={{fontSize: '30', marginRight: '10px'}} />}
                    selected={selected}
                    setSelected={setSelected}
                />
                <Item 
                    title="Bar"
                    to="/bar"
                    icon={<BarChartOutlinedIcon style={{fontSize: '30', marginRight: '10px'}} />}
                    selected={selected}
                    setSelected={setSelected}
                />
                <Item 
                    title="Help"
                    to="/help"
                    icon={<HelpOutlinedIcon style={{fontSize: '30', marginRight: '10px'}}/>}
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