import { NavLink } from "react-router-dom";

const LINKS = [
  { to: "/", label: "Command Center" },
  { to: "/villages", label: "Habitations" },
  { to: "/safe-sites", label: "Safe Sites" },
  { to: "/relocation", label: "Relocation Matrix" },
  { to: "/alerts", label: "Early Warnings" },
  { to: "/analytics", label: "Analytics" },
  { to: "/assistant", label: "AI Decision Desk" },
];

export default function TopRibbon() {
  return (
    <>
      {/* National Tricolor Accent Header Bar */}
      <div className="national-tricolor-bar" aria-hidden="true">
        <span className="tricolor-saffron" />
        <span className="tricolor-white" />
        <span className="tricolor-green" />
      </div>

      <header className="top-ribbon">
        <NavLink to="/" className="brand-lockup" title="RakshaSetu - National Multi-Hazard Decision Support System">
          {/* Government Emblem / Ashoka Stambha Crest */}
          <div className="gov-emblem-badge" aria-label="Government of India Emblem">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2L3 7v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-9-5z" />
              <path d="M12 7v10" />
              <path d="M8 12h8" />
              <circle cx="12" cy="12" r="2.5" />
            </svg>
          </div>
          <div className="gov-title-lockup">
            <span className="gov-apex-label">
              भारत सरकार · GOVT OF INDIA <b>|</b> गृह मंत्रालय · MHA
            </span>
            <div className="gov-main-title">
              <strong>RAKSHASETU</strong>
              <span className="gov-hindi-badge">रक्षासेतु</span>
            </div>
            <span className="gov-sub-label">National Multi-Hazard Red-Zone Decision Support System</span>
          </div>
        </NavLink>

        <nav className="top-nav" aria-label="Main Navigation">
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

        <div className="top-status-group">
          <span className="top-helpline-pill" title="National Disaster Response Force 24x7 Helpline">
            EMERGENCY: <b>1078</b>
          </span>
          <div className="top-live" title="Real-Time MHA/NDRF Telemetry Feed Active">
            <i />
            <span>MHA-NDRF · 24×7 CRISIS GATEWAY</span>
          </div>
        </div>
      </header>
    </>
  );
}
