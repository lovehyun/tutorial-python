CREATE TABLE IF NOT EXISTS "users"(
    "Id" TEXT,
    "Name" TEXT,
    "Gender" TEXT,
    "Age" TEXT,
     "Birthdate" TEXT,
    "Address" TEXT
);

CREATE TABLE IF NOT EXISTS "stores"(
    "Id" TEXT,
    "Name" TEXT,
    "Type" TEXT,
    "Address" TEXT
);

CREATE TABLE IF NOT EXISTS "orders"(
    "Id" TEXT,
    "OrderAt" TEXT,
    "StoreId" TEXT,
    "UserId" TEXT
);

CREATE TABLE IF NOT EXISTS "items"(
    "Id" TEXT,
    "Name" TEXT,
    "Type" TEXT,
    "UnitPrice" TEXT
);

CREATE TABLE IF NOT EXISTS "orderitems"(
    "Id" TEXT,
    "OrderId" TEXT,
    "ItemId" TEXT
);
