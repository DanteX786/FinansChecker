-- Esquema de la base de datos de FinansChecker (PostgreSQL en Neon)
-- Se ejecuta una sola vez en el editor SQL de Neon, si las tablas ya existen no hace nada

CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    city        VARCHAR(60)  NOT NULL,
    created_at  TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS transactions (
    id                   SERIAL PRIMARY KEY,
    user_id              INTEGER       NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    type                 VARCHAR(20)   NOT NULL CHECK (type IN ('transfer', 'payment', 'withdrawal', 'online_purchase')),
    amount               NUMERIC(14,2) NOT NULL CHECK (amount >= 1 AND amount <= 50000000),
    destination_account  VARCHAR(30)   NOT NULL,
    city                 VARCHAR(60)   NOT NULL,
    channel              VARCHAR(20)   NOT NULL CHECK (channel IN ('app', 'web', 'atm')),
    created_at           TIMESTAMP     NOT NULL,
    risk_score           SMALLINT      NOT NULL CHECK (risk_score BETWEEN 0 AND 100),
    status               VARCHAR(20)   NOT NULL CHECK (status IN ('approved', 'review', 'suspicious'))
);

CREATE TABLE IF NOT EXISTS alerts (
    id              SERIAL PRIMARY KEY,
    transaction_id  INTEGER     NOT NULL UNIQUE REFERENCES transactions (id) ON DELETE CASCADE,
    level           VARCHAR(20) NOT NULL CHECK (level IN ('review', 'suspicious')),
    -- RN-02: toda alerta debe tener al menos un motivo
    reasons         TEXT[]      NOT NULL CHECK (cardinality(reasons) >= 1),
    created_at      TIMESTAMP   NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_transactions_user_date ON transactions (user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions (status);
CREATE INDEX IF NOT EXISTS idx_alerts_date ON alerts (created_at DESC);
