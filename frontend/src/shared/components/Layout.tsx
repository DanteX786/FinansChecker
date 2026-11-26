import { NavLink, Outlet } from 'react-router-dom'
import { Icon, type IconName } from './Icon'

const NAV_ITEMS: { to: string; label: string; icon: IconName }[] = [
  { to: '/', label: 'Dashboard', icon: 'dashboard' },
  { to: '/transactions', label: 'Transacciones', icon: 'list' },
  { to: '/simulator', label: 'Simulador', icon: 'play' },
  { to: '/alerts', label: 'Alertas', icon: 'bell' },
]

export function Layout() {
  return (
    <div className="layout">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand__logo">
            <Icon name="shield" size={22} />
          </span>
          <span className="brand__name">FinansChecker</span>
        </div>
        <nav aria-label="Navegación principal">
          <ul className="nav">
            {NAV_ITEMS.map((item) => (
              <li key={item.to}>
                <NavLink to={item.to} end={item.to === '/'} className="nav__link">
                  <Icon name={item.icon} size={18} />
                  <span className="nav__label">{item.label}</span>
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <p className="sidebar__note">Datos simulados con fines académicos</p>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  )
}
