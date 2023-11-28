import { Box, Typography, useTheme } from "@mui/material";
import { tokens } from "../theme";
import React from "react";

const StatBox = ( {title, subtitle, value, icon} ) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    return (
        <Box width='100%' m = '10px 10px'>
            <Box display='flex' justifyContent='space-evenly' flexDirection='column' alignItems='center'>
                <Box alignContent='center'>
                    {icon}
                </Box>
                <Box>
                    <Typography variant="h6" sx = {{ color: colors.primary[100]}}>
                        {title}
                    </Typography>
                </Box>
                <Box display='flex' justifyContent='space-between' >
                    <Typography variant="h6" fontWeight='italic' sx = {{ color: colors.primary[200]}}>
                        {value}
                    </Typography>
                </Box>
                <Box display='flex' justifyContent='space-between' >
                    <Typography variant="h5" sx = {{ color: colors.grey[400]}}>
                        {subtitle}
                    </Typography>
                </Box>
            </Box>
        </Box>
    );
};

export default StatBox;