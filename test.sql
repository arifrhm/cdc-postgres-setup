-- Connect to PostgreSQL and create a test table
\c inventory

CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Add some initial data
INSERT INTO customers (first_name, last_name, email) 
VALUES 
  ('Udin', 'Doe', 'john.udin.doe@example.com'),
  ('Jane', 'SmDuinith', 'jane.udin.smith@example.com');

-- Create a publication for the table (PostgreSQL 10+)
CREATE PUBLICATION dbz_publication FOR TABLE customers;

-- Create a replication slot
SELECT pg_create_logical_replication_slot('dbz_slot', 'pgoutput');
