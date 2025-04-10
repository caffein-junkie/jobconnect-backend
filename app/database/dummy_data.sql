-- Generate bcrypt hashes for the password (cost factor 12)
-- python123@#$.py becomes:
-- $2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O

-- Complete dummy data with UUID relationships
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DO $$
DECLARE
    -- Admin IDs
    admin1_id UUID := uuid_generate_v4();
    admin2_id UUID := uuid_generate_v4();
    admin3_id UUID := uuid_generate_v4();
    admin4_id UUID := uuid_generate_v4();
    admin5_id UUID := uuid_generate_v4();
    admin6_id UUID := uuid_generate_v4();
    admin7_id UUID := uuid_generate_v4();
    admin8_id UUID := uuid_generate_v4();
    admin9_id UUID := uuid_generate_v4();
    admin10_id UUID := uuid_generate_v4();
    
    -- Client IDs
    client1_id UUID := uuid_generate_v4();
    client2_id UUID := uuid_generate_v4();
    client3_id UUID := uuid_generate_v4();
    client4_id UUID := uuid_generate_v4();
    client5_id UUID := uuid_generate_v4();
    client6_id UUID := uuid_generate_v4();
    client7_id UUID := uuid_generate_v4();
    client8_id UUID := uuid_generate_v4();
    client9_id UUID := uuid_generate_v4();
    client10_id UUID := uuid_generate_v4();
    
    -- Technician IDs
    tech1_id UUID := uuid_generate_v4();
    tech2_id UUID := uuid_generate_v4();
    tech3_id UUID := uuid_generate_v4();
    tech4_id UUID := uuid_generate_v4();
    tech5_id UUID := uuid_generate_v4();
    tech6_id UUID := uuid_generate_v4();
    tech7_id UUID := uuid_generate_v4();
    tech8_id UUID := uuid_generate_v4();
    tech9_id UUID := uuid_generate_v4();
    tech10_id UUID := uuid_generate_v4();
    
    -- Booking IDs
    booking1_id UUID := uuid_generate_v4();
    booking2_id UUID := uuid_generate_v4();
    booking3_id UUID := uuid_generate_v4();
    booking4_id UUID := uuid_generate_v4();
    booking5_id UUID := uuid_generate_v4();
    booking6_id UUID := uuid_generate_v4();
    booking7_id UUID := uuid_generate_v4();
    booking8_id UUID := uuid_generate_v4();
    booking9_id UUID := uuid_generate_v4();
    booking10_id UUID := uuid_generate_v4();
    
    -- Other IDs
    fav1_id UUID := uuid_generate_v4();
    fav2_id UUID := uuid_generate_v4();
    fav3_id UUID := uuid_generate_v4();
    fav4_id UUID := uuid_generate_v4();
    fav5_id UUID := uuid_generate_v4();
    fav6_id UUID := uuid_generate_v4();
    fav7_id UUID := uuid_generate_v4();
    fav8_id UUID := uuid_generate_v4();
    fav9_id UUID := uuid_generate_v4();
    fav10_id UUID := uuid_generate_v4();
    
    review1_id UUID := uuid_generate_v4();
    review2_id UUID := uuid_generate_v4();
    review3_id UUID := uuid_generate_v4();
    
    payment1_id UUID := uuid_generate_v4();
    payment2_id UUID := uuid_generate_v4();
    payment3_id UUID := uuid_generate_v4();
    
    notif1_id UUID := uuid_generate_v4();
    notif2_id UUID := uuid_generate_v4();
    notif3_id UUID := uuid_generate_v4();
    notif4_id UUID := uuid_generate_v4();
    notif5_id UUID := uuid_generate_v4();
BEGIN

-- ADMIN DATA
INSERT INTO admin (admin_id, name, surname, email, phone_number, password_hash, role) VALUES
(admin1_id, 'Thabo', 'Mbeki', 'thabo.mbeki@jobconnect.co.za', '0821234567', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'super_admin'),
(admin2_id, 'Nkosazana', 'Dlamini', 'nkosazana.d@jobconnect.co.za', '0822345678', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'content_admin'),
(admin3_id, 'Cyril', 'Ramaphosa', 'cyril.r@jobconnect.co.za', '0823456789', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'support_admin'),
(admin4_id, 'Trevor', 'Noah', 'trevor.n@jobconnect.co.za', '0824567890', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'support_admin'),
(admin5_id, 'Charlize', 'Theron', 'charlize.t@jobconnect.co.za', '0825678901', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'content_admin'),
(admin6_id, 'Siya', 'Kolisi', 'siya.k@jobconnect.co.za', '0826789012', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'support_admin'),
(admin7_id, 'Bonang', 'Matheba', 'bonang.m@jobconnect.co.za', '0827890123', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'content_admin'),
(admin8_id, 'Kagiso', 'Rabada', 'kagiso.r@jobconnect.co.za', '0828901234', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'support_admin'),
(admin9_id, 'Nomzamo', 'Mbatha', 'nomzamo.m@jobconnect.co.za', '0829012345', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'content_admin'),
(admin10_id, 'Black', 'Coffee', 'black.c@jobconnect.co.za', '0820123456', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'support_admin');

-- CLIENT DATA
INSERT INTO client (client_id, name, surname, email, phone_number, password_hash, location_name, location) VALUES
(client1_id, 'Lerato', 'Moloi', 'lerato.m@gmail.com', '0711234567', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Hatfield', ST_GeographyFromText('POINT(28.2293 -25.7479)')),
(client2_id, 'Sipho', 'Ndlovu', 'sipho.n@yahoo.com', '0712345678', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Centurion', ST_GeographyFromText('POINT(28.1684 -25.8606)')),
(client3_id, 'Nandi', 'Khumalo', 'nandi.k@outlook.com', '0713456789', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Brooklyn', ST_GeographyFromText('POINT(28.2419 -25.7656)')),
(client4_id, 'Tumi', 'Van der Merwe', 'tumi.v@hotmail.com', '0714567890', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Menlyn', ST_GeographyFromText('POINT(28.2746 -25.7835)')),
(client5_id, 'Kagiso', 'Botha', 'kagiso.b@gmail.com', '0715678901', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Sunnyside', ST_GeographyFromText('POINT(28.2086 -25.7547)')),
(client6_id, 'Amahle', 'Mokoena', 'amahle.m@yahoo.com', '0716789012', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Arcadia', ST_GeographyFromText('POINT(28.2167 -25.7479)')),
(client7_id, 'Mandla', 'Sithole', 'mandla.s@outlook.com', '0717890123', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Waterkloof', ST_GeographyFromText('POINT(28.2805 -25.7994)')),
(client8_id, 'Zanele', 'Pretorius', 'zanele.p@hotmail.com', '0718901234', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Garsfontein', ST_GeographyFromText('POINT(28.3184 -25.7932)')),
(client9_id, 'Bongani', 'Van Wyk', 'bongani.v@gmail.com', '0719012345', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Muckleneuk', ST_GeographyFromText('POINT(28.2219 -25.7612)')),
(client10_id, 'Nomsa', 'De Jager', 'nomsa.d@yahoo.com', '0710123456', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Lynnwood', ST_GeographyFromText('POINT(28.2538 -25.7694)'));

-- TECHNICIAN DATA
INSERT INTO technician (technician_id, name, surname, email, phone_number, password_hash, location_name, location, service_types, experience_years, is_verified, is_available) VALUES
(tech1_id, 'Jacob', 'Zuma', 'jacob.z@handyman.co.za', '0721234567', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Soshanguve', ST_GeographyFromText('POINT(28.0945 -25.5146)'), '{"Plumbing", "Electrical"}', 8, TRUE, TRUE),
(tech2_id, 'Julius', 'Malema', 'julius.m@fixit.co.za', '0722345678', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Mamelodi', ST_GeographyFromText('POINT(28.3333 -25.7000)'), '{"Painting", "Carpentry"}', 5, TRUE, TRUE),
(tech3_id, 'Patrice', 'Motsepe', 'patrice.m@repairs.co.za', '0723456789', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Atteridgeville', ST_GeographyFromText('POINT(28.1167 -25.7667)'), '{"Appliance Repair", "Aircon"}', 10, TRUE, FALSE),
(tech4_id, 'Tokyo', 'Sexwale', 'tokyo.s@services.co.za', '0724567890', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Silverton', ST_GeographyFromText('POINT(28.2667 -25.7333)'), '{"Tiling", "Paving"}', 7, TRUE, TRUE),
(tech5_id, 'Fikile', 'Mbalula', 'fikile.m@buildit.co.za', '0725678901', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Eersterust', ST_GeographyFromText('POINT(28.3000 -25.7167)'), '{"Bricklaying", "Roofing"}', 12, FALSE, TRUE),
(tech6_id, 'Naledi', 'Pandor', 'naledi.p@tech.co.za', '0726789012', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Laudium', ST_GeographyFromText('POINT(28.1000 -25.7833)'), '{"Computer Repair", "Networking"}', 6, TRUE, TRUE),
(tech7_id, 'Blade', 'Nzimande', 'blade.n@install.co.za', '0727890123', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Irene', ST_GeographyFromText('POINT(28.2167 -25.8667)'), '{"Satellite TV", "Security Systems"}', 9, TRUE, FALSE),
(tech8_id, 'Lindiwe', 'Sisulu', 'lindiwe.s@clean.co.za', '0728901234', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Olifantsfontein', ST_GeographyFromText('POINT(28.2667 -25.9667)'), '{"Cleaning", "Gardening"}', 4, FALSE, TRUE),
(tech9_id, 'Pravin', 'Gordhan', 'pravin.g@electro.co.za', '0729012345', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Wierdapark', ST_GeographyFromText('POINT(28.2833 -25.8167)'), '{"Solar Installation", "Inverter Repair"}', 15, TRUE, TRUE),
(tech10_id, 'Baleka', 'Mbete', 'baleka.m@decor.co.za', '0720123456', '$2b$12$E9Q3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5OeQ3bX5Z5O3Z5O3Z5O3Z5O', 'Faerie Glen', ST_GeographyFromText('POINT(28.3000 -25.7833)'), '{"Interior Design", "Furniture Assembly"}', 11, TRUE, TRUE);

-- BOOKING DATA
INSERT INTO booking (booking_id, client_id, technician_id, service_type, description, price, status, start_date, end_date) VALUES
(booking1_id, client1_id, tech1_id, 'Plumbing', 'Kitchen sink leaking', 450.00, 'completed', '2023-05-15 09:00:00', '2023-05-15 11:30:00'),
(booking2_id, client2_id, tech2_id, 'Painting', 'Living room walls need repainting', 1200.00, 'confirmed', '2023-06-20 08:00:00', '2023-06-20 16:00:00'),
(booking3_id, client3_id, tech3_id, 'Appliance Repair', 'Fridge not cooling properly', 600.00, 'in_progress', '2023-07-10 10:00:00', '2023-07-10 12:00:00'),
(booking4_id, client4_id, tech4_id, 'Tiling', 'Bathroom floor tiles cracked', 850.00, 'pending', '2023-08-05 07:30:00', '2023-08-05 15:00:00'),
(booking5_id, client5_id, tech5_id, 'Bricklaying', 'Garden wall needs rebuilding', 2200.00, 'completed', '2023-09-12 08:00:00', '2023-09-14 17:00:00'),
(booking6_id, client6_id, tech6_id, 'Computer Repair', 'Laptop screen replacement', 950.00, 'cancelled', '2023-10-18 11:00:00', '2023-10-18 13:00:00'),
(booking7_id, client7_id, tech7_id, 'Satellite TV', 'New DStv installation', 300.00, 'completed', '2023-11-22 09:30:00', '2023-11-22 11:00:00'),
(booking8_id, client8_id, tech8_id, 'Cleaning', 'Deep clean after renovation', 500.00, 'confirmed', '2023-12-05 08:00:00', '2023-12-05 12:00:00'),
(booking9_id, client9_id, tech9_id, 'Solar Installation', 'Install 5kVA solar system', 18500.00, 'in_progress', '2024-01-15 07:00:00', '2024-01-17 17:00:00'),
(booking10_id, client10_id, tech10_id, 'Interior Design', 'Consultation for new apartment', 800.00, 'pending', '2024-02-20 10:00:00', '2024-02-20 12:00:00');

-- FAVORITE TECHNICIAN DATA
INSERT INTO favorite_technician (id, client_id, technician_id, created_at) VALUES
(fav1_id, client1_id, tech1_id, NOW()),
(fav2_id, client1_id, tech3_id, NOW()),
(fav3_id, client2_id, tech2_id, NOW()),
(fav4_id, client3_id, tech5_id, NOW()),
(fav5_id, client4_id, tech4_id, NOW()),
(fav6_id, client5_id, tech10_id, NOW()),
(fav7_id, client6_id, tech6_id, NOW()),
(fav8_id, client7_id, tech7_id, NOW()),
(fav9_id, client8_id, tech8_id, NOW()),
(fav10_id, client9_id, tech9_id, NOW());

-- REVIEW DATA
INSERT INTO review (review_id, booking_id, client_id, technician_id, rating, comment, created_at) VALUES
(review1_id, booking1_id, client1_id, tech1_id, 4.5, 'Fixed the leak quickly but was 15 minutes late', NOW()),
(review2_id, booking5_id, client5_id, tech5_id, 3.0, 'Wall was built well but took longer than estimated', NOW()),
(review3_id, booking7_id, client7_id, tech7_id, 5.0, 'Perfect installation and very professional', NOW());

-- PAYMENT DATA
INSERT INTO payment (payment_id, booking_id, client_id, technician_id, amount, payment_method, payment_status, transaction_date) VALUES
(payment1_id, booking1_id, client1_id, tech1_id, 450.00, 'card', 'completed', '2023-05-15 12:00:00'),
(payment2_id, booking5_id, client5_id, tech5_id, 2200.00, 'banking', 'completed', '2023-09-14 17:30:00'),
(payment3_id, booking7_id, client7_id, tech7_id, 300.00, 'card', 'completed', '2023-11-22 11:30:00');

-- NOTIFICATION DATA
INSERT INTO notification (notification_id, message, recipient_id, is_read, created_at) VALUES
(notif1_id, 'Your booking with Jacob Zuma has been confirmed', client1_id, TRUE, NOW()),
(notif2_id, 'Payment of R450.00 received for your plumbing service', client1_id, FALSE, NOW()),
(notif3_id, 'Reminder: Your painting appointment starts in 2 hours', client2_id, FALSE, NOW()),
(notif4_id, 'Please rate your recent service with Tokyo Sexwale', client5_id, TRUE, NOW()),
(notif5_id, 'New technician available in your area: Baleka Mbete', client3_id, FALSE, NOW());

END $$;
