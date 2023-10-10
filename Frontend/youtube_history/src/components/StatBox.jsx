import { Box, Typography, useTheme } from "@mui/material";
import { tokens } from "../theme";
import React from "react";

const StatBox = ( {title, subtitle, value} ) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    return (
        <Box width='100%' m = '0 30 px'>
            <Box display='flex' justifyContent='space-between'>
                <Box>
                    <Typography variant="h4" fontWeight='bold' sx = {{ color: colors.grey[100]}}>
                        {title}
                    </Typography>
                </Box>
                <Box display='flex' justifyContent='space-between' >
                    <Typography variant="h5" sx = {{ color: colors.greenAccent[100]}}>
                        {subtitle}
                    </Typography>
                </Box>
                <Box display='flex' justifyContent='space-between' >
                    <Typography variant="h5" fontWeight='italic' sx = {{ color: colors.greenAccent[600]}}>
                        {value}
                    </Typography>
                </Box>
            </Box>
        </Box>
    );
};

export default StatBox;