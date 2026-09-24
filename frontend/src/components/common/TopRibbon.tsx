import { NavLink } from "react-router-dom";

const LINKS = [
  { to: "/", label: "Command Center" },
  { to: "/villages", label: "Villages" },
  { to: "/safe-sites", label: "Safe Sites" },
  { to: "/relocation", label: "Relocation" },
  { to: "/alerts", label: "Alerts" },
  { to: "/analytics", label: "Analytics" },
  { to: "/assistant", label: "AI Assistant" },
];

export default function TopRibbon() {
  return (
    <header className="top-ribbon">
      <NavLink to="/" className="brand-lockup">
        <span className="brand-mark"><span /></span>
        <span><strong>RakshaSetu</strong><small>MHA · NDRF | PS-26191</small></span>
      </NavLink>
      <nav className="top-nav">
        {LINKS.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === "/"}
            className={({ isActive }) => `top-nav-link ${isActive ? "active" : ""}`}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
      <div className="top-live" title="Smart India Hackathon 2026 - Problem Statement 26191"><i />SIH-26191 · GIS DECISION SUPPORT</div>
    </header>
  );
}
