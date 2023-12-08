/*
SELECT *
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_type = 'BASE TABLE';
*/


CREATE TABLE icd10_categories (
    id VARCHAR(10) PRIMARY KEY NOT NULL,
    category_name VARCHAR(255)
);

CREATE TABLE icd10_sub_categories (
	id SERIAL PRIMARY KEY NOT NULL,
    code VARCHAR(10),
    sub_category_name VARCHAR(255),
    parent_code VARCHAR(10) REFERENCES icd10_categories(id)
);

CREATE TABLE icd10_classification (
    icd_code VARCHAR(10) PRIMARY KEY NOT NULL,
    icd_name VARCHAR(255),
    parent_code VARCHAR(10) REFERENCES icd10_classification(icd_code),
    sub_category INTEGER REFERENCES icd10_sub_categories(id)
);

CREATE TABLE atc_classification (
    atc_code VARCHAR(10) PRIMARY KEY NOT NULL,
    atc_name VARCHAR(255),
    parent_code VARCHAR(10) REFERENCES atc_classification(atc_code)
);

CREATE TABLE medicines (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    atc_code VARCHAR REFERENCES atc_classification(atc_code)
);




