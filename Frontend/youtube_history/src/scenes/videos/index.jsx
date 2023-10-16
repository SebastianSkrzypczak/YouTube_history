import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import mockTableData from "../../data/mockTableData";
import { AdminPanelSettings } from "@mui/icons-material";
import Header from "../../components/Header";

const Table = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode)

    return(
        <Box>
            <Header title = 'Table' subtitle='table table'/>
            <Box>
                <DataGrid
                    rows={mockTableData}
                    columns={columns}

                />
            </Box>
        </Box>
    )
    
}

export default Table;