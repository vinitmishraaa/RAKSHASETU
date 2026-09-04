import { Routes, Route } from "react-router-dom";
import TopRibbon from "./components/common/TopRibbon";
import Dashboard from "./pages/Dashboard/Dashboard";
import Villages from "./pages/Villages/Villages";
import SafeSites from "./pages/SafeSites/SafeSites";
import Relocation from "./pages/Relocation/Relocation";
import Alerts from "./pages/Alerts/Alerts";
import Analytics from "./pages/Analytics/Analytics";
import Assistant from "./pages/Assistant/Assistant";

export default function App() {
  return (
    <div className="app-shell">
      <TopRibbon />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/villages" element={<Villages />} />
        <Route path="/safe-sites" element={<SafeSites />} />
        <Route path="/relocation" element={<Relocation />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/assistant" element={<Assistant />} />
      </Routes>
    </div>
  );
}
