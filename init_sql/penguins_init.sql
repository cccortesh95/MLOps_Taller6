CREATE TABLE IF NOT EXISTS penguins_raw (
    id SERIAL PRIMARY KEY,
    species VARCHAR(50),
    island VARCHAR(50),
    bill_length_mm FLOAT,
    bill_depth_mm FLOAT,
    flipper_length_mm FLOAT,
    body_mass_g FLOAT,
    sex VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS penguins_processed (
    id SERIAL PRIMARY KEY,
    species VARCHAR(50),
    island VARCHAR(50),
    bill_length_mm FLOAT,
    bill_depth_mm FLOAT,
    flipper_length_mm FLOAT,
    body_mass_g FLOAT,
    sex VARCHAR(20),
    species_encoded INT,
    island_encoded INT,
    sex_encoded INT
);