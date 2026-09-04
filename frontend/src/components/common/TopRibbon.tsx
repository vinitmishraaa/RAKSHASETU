import { NavLink } from "react-router-dom";

const LINKS = [
  { to: "/", label: "Dashboard" },
  { to: "/villages", label: "Villages" },
  { to: "/safe-sites", label: "Safe Sites" },
  { to: "/relocation", label: "Relocation" },
  { to: "/alerts", label: "Alerts" },
  { to: "/analytics", label: "Analytics" },
  { to: "/assistant", label: "AI Assistant" },
];

export default function TopRibbon() {
  return (
    <header
      style={{
        display: "flex",
        alignItems: "center",
        gap: 28,
        padding: "0 20px",
        height: 56,
        borderBottom: "1px solid var(--border-subtle)",
        background: "var(--bg-panel)",
        flexShrink: 0,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
          <path
            d="M12 2 L21 6 V12 C21 17 17 20.5 12 22 C7 20.5 3 17 3 12 V6 Z"
            stroke="var(--brand)"
            strokeWidth="1.6"
            fill="rgba(211,150,60,0.08)"
          />
          <circle cx="12" cy="12" r="3" fill="var(--brand)" />
        </svg>
        <span style={{ fontWeight: 800, fontSize: 15, letterSpacing: "0.01em" }}>
          RakshaSetu
        </span>
      </div>

      <nav style={{ display: "flex", gap: 4, flex: 1 }}>
        {LINKS.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === "/"}
            style={({ isActive }) => ({
              padding: "8px 12px",
              borderRadius: 6,
              fontSize: 13.5,
              fontWeight: 600,
              color: isActive ? "var(--text-primary)" : "var(--text-secondary)",
              background: isActive ? "var(--bg-panel-raised)" : "transparent",
            })}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>

      <div
        style={{
          fontSize: 12,
          color: "var(--text-muted)",
          fontFamily: "var(--font-data)",
        }}
      >
        South &amp; North 24 Parganas · West Bengal
      </div>
    </header>
  );
}
