import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import RiskBadge from "../../components/common/RiskBadge";
import { api } from "../../services/api";
import type { Village } from "../../types";

export default function Villages() {
  const [villages, setVillages] = useState<Village[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    api.villages.list().then((data) =>
      setVillages([...data].sort((a, b) => b.risk_score - a.risk_score))
    );
  }, []);

  return (
    <div className="scrollable" style={{ padding: 24, flex: 1 }}>
      <h2 style={{ fontSize: 20, marginBottom: 4 }}>Villages &amp; Habitations</h2>
      <p style={{ marginBottom: 20 }}>Ranked by current risk score, highest first.</p>

      <div className="panel" style={{ overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13.5 }}>
          <thead>
            <tr style={{ textAlign: "left", background: "var(--bg-panel-raised)" }}>
              {["Village", "District", "Population", "Risk", "Level", ""].map((h) => (
                <th key={h} style={{ padding: "12px 16px", color: "var(--text-muted)", fontWeight: 600 }}>
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {villages.map((v) => (
              <tr key={v.id} style={{ borderTop: "1px solid var(--border-subtle)" }}>
                <td style={{ padding: "12px 16px", fontWeight: 600 }}>{v.name}</td>
                <td style={{ padding: "12px 16px", color: "var(--text-secondary)" }}>{v.district}</td>
                <td className="mono" style={{ padding: "12px 16px" }}>
                  {v.population.toLocaleString()}
                </td>
                <td className="mono" style={{ padding: "12px 16px", fontWeight: 700 }}>
                  {v.risk_score}
                </td>
                <td style={{ padding: "12px 16px" }}>
                  <RiskBadge level={v.level} />
                </td>
                <td style={{ padding: "12px 16px" }}>
                  <button className="btn" onClick={() => navigate(`/?village=${v.id}`)}>
                    View on map
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
