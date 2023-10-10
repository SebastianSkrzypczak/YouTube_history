import React from 'react'
import { ColorModeContext, useMode } from './theme';
import { CssBaseline, ThemeProvider } from '@mui/material';
import { Route, Routes } from 'react-router-dom';
import Topbar from './scenes/global/Topbar';
import Sidebar from './scenes/global/Sidebar';
import Dashboard from './scenes/dashboard/index';
import Bar from "./scenes/bar";
import Line from "./scenes/line";
// import Videos from "./scenes/videos";
// import Radar from "./scenes/radar";
import Pie from "./scenes/pie";
// import Calendar from "./scenes/calendar";
// import FAQ from "./scenes.faq"


function App() {
  const [theme, colorMode] = useMode();
  
  return (
  <ColorModeContext.Provider value={colorMode}>
    <ThemeProvider theme = {theme}>
      <CssBaseline />
      <div className="app">
      <Sidebar />
        <main className='content'>
          <Topbar />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/bar" element={<Bar />} />
            <Route path="/pie" element={<Pie />} />
            <Route path='/line' element={<Line />} />
            {/* <Route path="/videos" element={<Videos />} />
            <Route path="/radar" element={<Radar />} />
            <Route path="/pie" element={<Pie />} />
            <Route path="/calendar" element={<Calendar />} />
            <Route path="/faq" element={<FAQ />} />
          */}
          </Routes> 
        </main>
      </div>
    </ThemeProvider>
  </ColorModeContext.Provider>
  );
};

export default App;
