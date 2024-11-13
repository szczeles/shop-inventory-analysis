CREATE TABLE products (
  product_id SERIAL PRIMARY KEY,
  upc VARCHAR(14),
  name TEXT,
  item_number INT,
  price NUMERIC(18,2),
  supplier TEXT,
  inventory_level INT,
  inventory_updated_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  UNIQUE (upc)
);

CREATE TYPE alternate_type AS ENUM ('variant', 'case');

CREATE TABLE product_alternates (
  product_alternate_id SERIAL PRIMARY KEY,
  product_id INT,
  upc VARCHAR(14),
  alternate_type alternate_type,
  case_pack REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_product
      FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

COPY products(product_id,upc,name,item_number,price,supplier,inventory_level,inventory_updated_at)
FROM '/data/products.csv'
DELIMITER ',' CSV HEADER;

COPY product_alternates(product_alternate_id,product_id,upc,alternate_type,case_pack)
FROM '/data/product_alternates.csv'
DELIMITER ',' CSV HEADER;
