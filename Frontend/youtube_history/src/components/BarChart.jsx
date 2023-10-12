import React from "react";
import { useTheme } from "@mui/material";
import { ResponsiveBar } from '@nivo/bar';
import { tokens } from "../theme";
import mockBarData from "../data/mockBarData";


const BarChart = ({isDashboard = false}) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode)

    return (
        <ResponsiveBar
        data={mockBarData}
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
                }
            },
            legends: {
                text: {
                    fill: colors.grey[100]
                }
            }
        }}
        keys={['count of videos']}
        indexBy="hour"
        margin={{ top: 80, right: 50, bottom: 40, left: 60 }}
        padding={0.3}
        valueScale={{ type: 'linear' }}
        indexScale={{ type: 'band', round: true }}
        colors={{ scheme: 'blues' }}
        colorBy="indexValue"
        borderWidth={2}
        borderColor={{
            from: 'color',
            modifiers: [
                [
                    'darker',
                    1.6
                ]
            ]
        }}
        enableLabel= {false}
        enableGridX ={false}
        enableGridY={false}
        axisTop={null}
        axisRight={null}
        axisBottom= {{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: isDashboard ? undefined : 'HOUR OF A DAY',
            legendPosition: 'middle',
            legendOffset: 32,
            format: value => {
            return value % 2 === 0 ? value : '';
    }
        }}
        axisLeft={{
            tickSize: 5,
            tickPadding: 5,
            tickRotation: 0,
            legend: isDashboard ? undefined : 'VIDEOS WATCHED',
            legendPosition: 'middle',
            legendOffset: -40
        }}
        labelSkipWidth={12}
        labelSkipHeight={12}
        labelTextColor={{
            from: 'color',
            modifiers: [
                [
                    'darker',
                    1.6
                ]
            ]
        }}
        legends={[]}
        role="application"
        ariaLabel="Nivo bar chart demo"
        barAriaLabel={e=>e.id+": "+e.formattedValue+" in country: "+e.indexValue}
        isInteractive={isDashboard ? false : true}
    />
    )
}

export default BarChart;