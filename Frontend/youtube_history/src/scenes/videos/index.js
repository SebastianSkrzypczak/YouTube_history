import { Box, Typography, useTheme } from "@mui/material";
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

    const columns = [
        {
            field: 'thumbnail',
            headerName: 'THUMBNAIL',
            renderCell: (params) => (
                <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', width: '100%' }}>
                <img 
                    src ={params.value}
                    alt={'Thumbnail ${params.row.id}'}
                    // style={{ width: '200px', height: '200px'}}
                />
                </div>
            ),
            cellClassName: "thumbnail-column--cell",
            flex: 1,
            headerAlign: "center",
            align: 'center'
        },
        {
            field: 'count',
            headerName: 'COUNT',
            type: 'number',
            headerAlign: "center",
            align: 'center'
        },
        {
            field: 'title',
            headerName: 'TITLE',
            flex: 1,
            cellClassName: "name-column--cell",
            headerAlign: "center",
            align: 'center'
        },
    ];

    const getRowHeight = () => 100; // Ustaw wysokość wiersza na 200px (dla przykładu)

    return (
        <Box>
            <Header title='Videos' subtitle='vidoes' />
            <Box style={{heigh: 500, width: '100%'}}>
                <DataGrid
                    rows = {mockVideosData}
                    columns ={columns}
                    autoHeight
                    getRowHeight={getRowHeight}
                />
            </Box>
        </Box>
    )
}

export default Videos;