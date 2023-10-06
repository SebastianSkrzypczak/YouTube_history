import { Typography, Box, useTheme } from "@mui/material/styles/createTypography";
import { tokens } from "../theme";
import { Typography, Typography } from "@mui/material";

const Header = ({ title, subtitle}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode)

    return (<Box mb = "30px">
        <Typography 
        variant='h2'
        color = {colors.gray[100]}
        fontWeight = 'bold '
        sx = {{mb: "5"}}
        >{title}</Typography>
        <Typography variant='h5' color = {colors.greenAccent[400]}>
        {subtitle}
        </Typography>
    </Box>
    );
};