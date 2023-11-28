import React from "react";
import { useTheme } from "@mui/material";
import { ResponsiveLine} from '@nivo/line';
import { tokens } from "../theme";
import mockLineData from "../data/mockLineData";


const LineChart = ({isDashboard = false}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);

    return (
        <ResponsiveLine 
        data={mockLineData}
        theme = {{
            axis:{
                domain:{
                    line: {
                        stroke: colors.grey[100]
                    }
                },
                legend: {
                    text: {
                        fill: colors.grey[100]
                    }
                },
                ticks: {
                    line: {
                        stroke: colors.grey[100],
                        strokeWidth: 1
                    },
                    text: {
                        fill: colors.grey[100]
                    }
                },
            }}}
        colors={isDashboard ? {datum: "color"} : {scheme: "nivo"}}
        margin={{ top: 80, right: 50, bottom: 40, left: 60 }}
        xScale={{ type: 'linear' }}
        yScale={{
            type: 'linear',
            min: 'auto',
            max: 'auto',
            stacked: true,
            reverse: false
        }}
        yFormat=" >-.2f"
        axisTop={null}
        axisRight={null}
        axisBottom={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: isDashboard ? undefined : 'hours',
            legendOffset: 36,
            legendPosition: 'middle'
        }}
        axisLeft={{
            tickValues: 5,
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend:  isDashboard ? undefined : 'count',
            legendOffset: -40,
            legendPosition: 'middle'
        }}
        pointSize={10}
        pointColor={{ theme: 'background' }}
        pointBorderWidth={2}
        pointBorderColor={{ from: 'serieColor' }}
        pointLabelYOffset={-12}
        useMesh={true}
        isInteractive={isDashboard ? false : true}
    />
    );
};

export default LineChart;
