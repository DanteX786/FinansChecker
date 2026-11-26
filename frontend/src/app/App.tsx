import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { AlertsPage } from '../features/alerts/AlertsPage'
import { DashboardPage } from '../features/dashboard/DashboardPage'
import { SimulatorPage } from '../features/simulator/SimulatorPage'
import { TransactionDetailPage } from '../features/transactions/TransactionDetailPage'
import { TransactionsPage } from '../features/transactions/TransactionsPage'
import { Layout } from '../shared/components/Layout'
import { NotFoundPage } from './NotFoundPage'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'transactions', element: <TransactionsPage /> },
      { path: 'transactions/:id', element: <TransactionDetailPage /> },
      { path: 'simulator', element: <SimulatorPage /> },
      { path: 'alerts', element: <AlertsPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])

export function App() {
  return <RouterProvider router={router} />
}
