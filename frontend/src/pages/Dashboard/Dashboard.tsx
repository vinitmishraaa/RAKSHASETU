import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import FilterBar from "../../components/common/FilterBar";
import RiskMap from "../../components/map/RiskMap";
import SelectedAreaPanel from "../../components/risk/SelectedAreaPanel";
import PopulationProfile from "../../components/villages/PopulationProfile";
import HazardBars from "../../components/risk/HazardBars";
import HistoryTimeline from "../../components/charts/HistoryTimeline";
import RainfallTrendChart from "../../components/charts/RainfallTrendChart";
import RelocationBox from "../../components/relocation/RelocationBox";
import { api } from "../../services/api";
import type { Village, VillageDetail, RelocationPlan } from "../../types";

export default function Dashboard() {
  const navigate = useNavigate();
  const [villages, setVillages] = useState<Village[]>([]);
  const [district, setDistrict] = useState("");
  const [level, setLevel] = useState("");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<VillageDetail | null>(null);
  const [plan, setPlan] = useState<RelocationPlan | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.villages.list().then((data) => {
      setVillages(data);
      setLoading(false);
    });
  }, []);

  const filtered = useMemo(() => {
    return villages.filter((v) => {
      if (district && v.district !== district) return false;
      if (level && v.level !== level) return false;
      return true;
    });
  }, [villages, district, level]);

  const districts = useMemo(
    () => Array.from(new Set(villages.map((v) => v.district))),
    [villages]
  );

  async function handleSelect(v: Village) {
    setSelectedId(v.id);
    const [d, p] = await Promise.all([
      api.villages.get(v.id),
      api.relocation.plan(v.id),
    ]);
    setDetail(d);
    setPlan(p);
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", flex: 1, minHeight: 0 }}>
      <FilterBar
        districts={districts}
        district={district}
        setDistrict={setDistrict}
        level={level}
        setLevel={setLevel}
      />

      <div style={{ display: "flex", flex: 1, minHeight: 0 }}>
        <div style={{ flex: 3, position: "relative", borderRight: "1px solid var(--border-subtle)" }}>
          {loading ? (
            <div style={{ padding: 40, color: "var(--text-muted)" }}>Loading map data…</div>
          ) : (
            <RiskMap
              villages={filtered}
              selectedId={selectedId}
              onSelectVillage={handleSelect}
            />
          )}

          <div
            style={{
              position: "absolute",
              bottom: 16,
              left: 16,
              display: "flex",
              gap: 14,
              padding: "8px 14px",
              background: "rgba(16,28,43,0.9)",
              border: "1px solid var(--border-subtle)",
              borderRadius: 8,
              fontSize: 12,
              zIndex: 1000,
            }}
          >
            <Legend color="var(--risk-critical)" label="Critical" />
            <Legend color="var(--risk-high)" label="High" />
            <Legend color="var(--risk-moderate)" label="Moderate" />
            <Legend color="var(--risk-low)" label="Low" />
          </div>
        </div>

        <div style={{ flex: 1, padding: 16, minWidth: 320, maxWidth: 380 }}>
          <SelectedAreaPanel
            village={detail}
            onViewRelocation={() => detail && navigate(`/relocation?village=${detail.id}`)}
          />
        </div>
      </div>

      {detail && (
        <div className="scrollable" style={{ padding: 20, borderTop: "1px solid var(--border-subtle)" }}>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
              gap: 16,
            }}
          >
            <PopulationProfile village={detail} />
            <HazardBars village={detail} />
            <RainfallTrendChart village={detail} />
            <HistoryTimeline village={detail} />
            {plan && <RelocationBox plan={plan} onViewRoute={() => navigate(`/relocation?village=${detail.id}`)} />}
          </div>
        </div>
      )}
    </div>
  );
}

function Legend({ color, label }: { color: string; label: string }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
      <span style={{ width: 8, height: 8, borderRadius: "50%", background: color }} />
      <span style={{ color: "var(--text-secondary)" }}>{label}</span>
    </div>
  );
}
