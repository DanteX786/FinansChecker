import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return (
    <div className="state">
      <h1>Página no encontrada</h1>
      <Link to="/" className="btn btn--primary">
        Ir al dashboard
      </Link>
    </div>
  )
}
