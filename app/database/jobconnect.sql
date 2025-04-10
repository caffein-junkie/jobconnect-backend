CREATE EXTENSION IF NOT EXISTS "postgis";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS admin (
    admin_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'),
    phone_number VARCHAR(10) NOT NULL UNIQUE CHECK (phone_number ~ '^[0-9]{10}$'),
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK(role IN ('super_admin', 'support_admin', 'content_admin')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS client (
    client_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'),
    phone_number VARCHAR(10) NOT NULL UNIQUE CHECK (phone_number ~ '^[0-9]{10}$'),
    password_hash TEXT NOT NULL,
    location_name TEXT NOT NULL,
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS technician (
    technician_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'),
    phone_number VARCHAR(10) NOT NULL UNIQUE CHECK (phone_number ~ '^[0-9]{10}$'),
    password_hash TEXT NOT NULL,
    location_name TEXT NOT NULL,
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    service_types TEXT[] NOT NULL CHECK (array_length(service_types, 1) > 0),
    experience_years NUMERIC CHECK (experience_years >= 0),
    is_verified BOOLEAN DEFAULT FALSE,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS booking (
    booking_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id uuid REFERENCES client(client_id) ON DELETE CASCADE,
    technician_id uuid REFERENCES technician(technician_id) ON DELETE CASCADE,
    service_type TEXT NOT NULL,
    description TEXT NOT NULL,
    price NUMERIC(10, 2),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'in_progress', 'completed', 'cancelled')),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS review (
    review_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_id uuid REFERENCES booking(booking_id) ON DELETE CASCADE,
    client_id uuid REFERENCES client(client_id) ON DELETE CASCADE,
    technician_id uuid REFERENCES technician(technician_id) ON DELETE CASCADE,
    rating NUMERIC(3, 2) NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (booking_id, client_id)
);

CREATE TABLE IF NOT EXISTS payment (
    payment_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id uuid REFERENCES booking(booking_id) ON DELETE CASCADE,
    client_id uuid REFERENCES client(client_id) ON DELETE CASCADE,
    technician_id uuid REFERENCES technician(technician_id) ON DELETE CASCADE,
    amount FLOAT NOT NULL,
    payment_method VARCHAR(50) CHECK (payment_method IN ('card', 'banking')),
    payment_status VARCHAR(50) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'completed', 'cancelled')),
    transaction_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notification (
    notification_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    message TEXT NOT NULL,
    client_id uuid REFERENCES client(client_id),
    technician_id uuid REFERENCES technician(technician_id),
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT chk_recipient CHECK (
    (client_id IS NOT NULL AND technician_id IS NULL) OR
    (client_id IS NULL AND technician_id IS NOT NULL))
);

CREATE TABLE IF NOT EXISTS favorite_technician (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id uuid REFERENCES client(client_id) ON DELETE CASCADE,
    technician_id uuid REFERENCES technician(technician_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (client_id, technician_id)
);

-- Client indexes
CREATE INDEX IF NOT EXISTS idx_client_email ON client(email);
CREATE INDEX IF NOT EXISTS idx_client_phone ON client(phone_number);
CREATE INDEX IF NOT EXISTS idx_client_location ON client USING GIST(location);

-- Technician indexes
CREATE INDEX IF NOT EXISTS idx_technician_email ON technician(email);
CREATE INDEX IF NOT EXISTS idx_technician_phone ON technician(phone_number);
CREATE INDEX IF NOT EXISTS idx_technician_location ON technician USING GIST(location);
CREATE INDEX IF NOT EXISTS idx_technician_service_types ON technician USING GIN(service_types);
CREATE INDEX IF NOT EXISTS idx_technician_verified ON technician(is_verified);
CREATE INDEX IF NOT EXISTS idx_technician_available ON technician(is_available);

-- Booking indexes
CREATE INDEX IF NOT EXISTS idx_booking_client_id ON booking(client_id);
CREATE INDEX IF NOT EXISTS idx_booking_technician_id ON booking(technician_id);
CREATE INDEX IF NOT EXISTS idx_booking_status ON booking(status);
CREATE INDEX IF NOT EXISTS idx_booking_date_range ON booking(start_date, end_date);

-- Review indexes
CREATE INDEX IF NOT EXISTS idx_review_technician_id ON review(technician_id);
CREATE INDEX IF NOT EXISTS idx_review_booking_id ON review(booking_id);
CREATE INDEX IF NOT EXISTS idx_review_rating ON review(rating);

-- Payment indexes
CREATE INDEX IF NOT EXISTS idx_payment_booking_id ON payment(booking_id);
CREATE INDEX IF NOT EXISTS idx_payment_client_id ON payment(client_id);
CREATE INDEX IF NOT EXISTS idx_payment_technician_id ON payment(technician_id);
CREATE INDEX IF NOT EXISTS idx_payment_status ON payment(payment_status);

-- Notification indexes
CREATE INDEX IF NOT EXISTS idx_notification_client ON notification(client_id) WHERE client_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_notification_technician ON notification(technician_id) WHERE technician_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_notification_read_status ON notification(is_read);

-- Favorite technician indexes
CREATE INDEX IF NOT EXISTS idx_favorite_technician_client ON favorite_technician(client_id);
