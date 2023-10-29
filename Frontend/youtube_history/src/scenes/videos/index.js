import { Box, Typography, useTheme,Grid, Card, CardMedia, CardContent } from "@mui/material";
import React from "react";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import mockVideosData   from "../../data/mockVideosData";
import { AdminPanelSettings } from "@mui/icons-material";
import { LocknPanelSettings } from "@mui/icons-material";
import { SecurityPanelSettings } from "@mui/icons-material";
import Header from "../../components/Header";

const Videos = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode)

    return (
            <Box sx={{
                padding: '20px',
            }}>
                <Grid container spacing={2}>
                {mockVideosData.map((video) => (
                    <Grid item key={video.id} xs={12} sm={6} md={4} lg={3} >
                    <Card style={{borderRadius: '25px'}}>
                        <CardMedia
                        component="img"
                        alt={video.title}
                        height="140"
                        image={video.thumbnail}
                        style={{
                            borderRadius: '25px',
                            padding: '10px'
                        }}
                        />
                        <CardContent>
                            <Typography variant="subtitle1">{video.title}</Typography>
                            <Typography variant='h6' color="text.secondary" align='right'>
                            Views: {video.count}
                            </Typography>
                        </CardContent>
                    </Card>
                    </Grid>
                ))}
                </Grid>
            </Box>
    )
}

export default Videos;