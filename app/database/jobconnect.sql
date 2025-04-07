CREATE EXTENSION IF NOT EXISTS "postgis";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS admins (
    admin_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'),
    phone_number VARCHAR(10) NOT NULL UNIQUE CHECK (phone_number ~ '^[0-9]{10}$'),
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('super_admin', 'support_admin', 'content_admin')),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS clients (
    client_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'),
    phone_number VARCHAR(10) NOT NULL UNIQUE CHECK (phone_number ~ '^[0-9]{10}$'),
    password_hash TEXT NOT NULL,
    location_name TEXT NOT NULL,
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS technicians (
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
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS bookings (
    booking_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id uuid REFERENCES clients(client_id) ON DELETE CASCADE,
    technician_id uuid REFERENCES technicians(technician_id) ON DELETE CASCADE,
    service_type TEXT NOT NULL,
    description TEXT NOT NULL,
    price NUMERIC(10, 2),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'in_progress', 'completed', 'cancelled')),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS reviews (
    review_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_id uuid REFERENCES bookings(booking_id) ON DELETE CASCADE,
    client_id uuid REFERENCES clients(client_id) ON DELETE CASCADE,
    technician_id uuid REFERENCES technicians(technician_id) ON DELETE CASCADE,
    rating NUMERIC(3, 2) NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (booking_id, client_id)
);

CREATE TABLE IF NOT EXISTS payment (
    payment_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id uuid REFERENCES bookings(booking_id) ON DELETE CASCADE,
    client_id uuid REFERENCES clients(client_id) ON DELETE CASCADE,
    technician_id uuid REFERENCES technicians(technician_id) ON DELETE CASCADE,
    amount FLOAT NOT NULL,
    payment_method VARCHAR(50) CHECK (payment_method IN ('cash', 'card', 'banking')),
    payment_status VARCHAR(50) DEFAULT 'pending' CHECK (payment_method IN ('pending', 'completed', 'cancelled')),
    transaction_date TIMESTAMP DEFAULT NOW()
);

-- Will be used later
-- CREATE TABLE IF NOT EXISTS payments (
--     payment_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
--     booking_id uuid REFERENCES bookings(booking_id) ON DELETE CASCADE,
--     client_id uuid REFERENCES clients(client_id) ON DELETE CASCADE,
--     technician_id uuid REFERENCES technicians(technician_id) ON DELETE CASCADE,
--     amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
--     status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'escrow', 'released', 'cancelled')),
--     released_at TIMESTAMPTZ,
--     created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
-- );

CREATE TABLE IF NOT EXISTS notifications (
    notification_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    notification_type VARCHAR(20) NOT NULL CHECK (notification_type IN ('email', 'push', 'sms')),
    category VARCHAR(20) NOT NULL CHECK (category IN ('booking', 'payment', 'message', 'rating', 'system')),
    message TEXT NOT NULL,
    recipient_id uuid NOT NULL,
    sender_id uuid, -- This can be nulled in case the sender is the system 
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS favorite_technicians (
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id uuid REFERENCES clients(client_id) ON DELETE CASCADE,
    technician_id uuid REFERENCES technicians(technician_id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (client_id, technician_id)
);

CREATE TABLE IF NOT EXISTS technician_availability (
    availability_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    technician_id uuid REFERENCES technicians(technician_id) ON DELETE CASCADE,
    day_of_week SMALLINT NOT NULL CHECK (day_of_week BETWEEN 0 AND 6), -- 0=Sunday to 6=Saturday
    start_time TIME NOT NULL, -- Time the technician starts working (8:00)
    end_time TIME NOT NULL, -- time the technician stops working (16:00)
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Messaging system
CREATE TABLE IF NOT EXISTS conversations (
    conversation_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id uuid REFERENCES clients(client_id) ON DELETE CASCADE,
    technician_id uuid REFERENCES technicians(technician_id) ON DELETE CASCADE,
    booking_id uuid REFERENCES bookings(booking_id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (client_id, technician_id, booking_id)
);

CREATE TABLE IF NOT EXISTS messages (
    message_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id uuid REFERENCES conversations(conversation_id) ON DELETE CASCADE,
    sender_id uuid NOT NULL, -- Could be client_id or technician_id
    content TEXT NOT NULL,
    image_url TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Dispute resolution system
CREATE TABLE IF NOT EXISTS disputes (
    dispute_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_id uuid REFERENCES bookings(booking_id) ON DELETE CASCADE,
    initiator_id uuid NOT NULL, -- Could be client_id or technician_id
    initiator_role VARCHAR(10) NOT NULL CHECK (initiator_role IN ('client', 'technician')),
    reason TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_review', 'resolved', 'rejected')),
    resolution TEXT,
    resolved_by uuid REFERENCES admins(admin_id) ON DELETE SET NULL,
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dispute_attachments (
    attachment_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    dispute_id uuid REFERENCES disputes(dispute_id) ON DELETE CASCADE,
    file_url TEXT NOT NULL,
    file_type VARCHAR(20) NOT NULL,
    uploaded_by uuid NOT NULL, -- client_id or technician_id
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dispute_comments (
    comment_id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    dispute_id uuid REFERENCES disputes(dispute_id) ON DELETE CASCADE,
    author_id uuid NOT NULL, -- admin_id, client_id, or technician_id
    author_role VARCHAR(10) NOT NULL CHECK (author_role IN ('admin', 'client', 'technician')),
    content TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT FALSE, -- For admin-only notes
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS password_reset_tokens (
    email VARCHAR(255) PRIMARY KEY,
    token_hash TEXT NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
DO $$
BEGIN
    -- Technicians location index
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_technicians_location') THEN
        CREATE INDEX idx_technicians_location ON technicians USING GIST(location);
    END IF;
    
    -- Clients location index
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_clients_location') THEN
        CREATE INDEX idx_clients_location ON clients USING GIST(location);
    END IF;
    
    -- Technicians service types index
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_technicians_service_types') THEN
        CREATE INDEX idx_technicians_service_types ON technicians USING GIN(service_types);
    END IF;
    
    -- Ratings technician index
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_reviews_technician_id') THEN
        CREATE INDEX idx_reviews_technician_id ON reviews(technician_id);
    END IF;
    
    -- Bookings status index
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_bookings_status') THEN
        CREATE INDEX idx_bookings_status ON bookings(status);
    END IF;
    
    -- Bookings technician index
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_bookings_technician_id') THEN
        CREATE INDEX idx_bookings_technician_id ON bookings(technician_id);
    END IF;
    
    -- Bookings client index
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_bookings_client_id') THEN
        CREATE INDEX idx_bookings_client_id ON bookings(client_id);
    END IF;
    
    -- Dispute status index (for admin dashboard)
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_disputes_status') THEN
        CREATE INDEX idx_disputes_status ON disputes(status);
    END IF;
    
    -- Dispute booking index (for quick lookup)
    IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_disputes_booking_id') THEN
        CREATE INDEX idx_disputes_booking_id ON disputes(booking_id);
    END IF;

END $$;
