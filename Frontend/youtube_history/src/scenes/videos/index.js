import { Box, Typography, useTheme,Grid, Card, CardMedia, CardContent } from "@mui/material";
import React from "react";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import mockVideosData   from "../../data/mockVideosData";
import { AdminPanelSettings } from "@mui/icons-material";
import { LocknPanelSettings } from "@mui/icons-material";
import { SecurityPanelSettings } from "@mui/icons-material";
import Header from "../../components/Header";
import VideosComp from "../../components/Videos";

const Videos = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode)

    return (
            <VideosComp/>
    )
}

export default Videos;