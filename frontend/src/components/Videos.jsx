import { Box, Typography, useTheme,Grid, Card, CardMedia, CardContent,IconButton } from "@mui/material";
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import React, { useState } from "react";
import mockVideosData   from "../data/mockVideosData";
import { tokens } from "../theme";

const VideosComp = ({isDashboard = false}) => {
    const maxCards = isDashboard ? 10 : 10000;
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    return (
        <Box sx={{
            padding: '20px',
            overflow: 'auto',
            scrollPaddingBlockStart: '10px',
            scrollbarWidth: 'thin',  
            scrollbarTrackColor: 'transparent', 
            '&::-webkit-scrollbar': {
            width: '12px', 
            height: '12px',  
            },
            '&::-webkit-scrollbar-thumb': {
            background: '#888', 
            
            },
        }}>
            <Grid
            container spacing={2}
            sx={
                isDashboard ? {
                display: 'flex',
                flexWrap: 'nowrap',
                height: 'auto'
                } : {}
            }
            >
            {mockVideosData.slice(0, maxCards).map((video) => (
                <Grid item key={video.id} xs={12} sm={6} md={4} lg={3}>
                <Card style={{borderRadius: '25px', backgroundColor: colors.grey[900],}}>
                    <CardMedia
                    component="img"
                    alt={video.title}
                    height="140"
                    image={video.thumbnail}
                    style={{
                        borderRadius: '25px',
                        padding: '10px',
                        width: isDashboard ? '200px' : undefined
                    }}
                    />
                    <CardContent>
                    <div style={{overflow: 'hidden', textOverflow: 'ellipsis', height: '50px'}}>
                        <Typography variant="subtitle1">
                            {video.title}
                        </Typography>
                    </div>
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
};

export default VideosComp;