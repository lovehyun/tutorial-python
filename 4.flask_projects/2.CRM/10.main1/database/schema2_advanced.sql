CREATE TABLE IF NOT EXISTS "users"(
    "Id" TEXT PRIMARY KEY,
    "Name" TEXT NOT NULL,
    "Gender" TEXT,
    "Age" INTEGER,
    "Birthdate" DATETIME,
    "Address" TEXT
);

CREATE TABLE IF NOT EXISTS "stores"(
    "Id" TEXT PRIMARY KEY,
    "Name" TEXT NOT NULL,
    "Type" TEXT,
    "Address" TEXT
);

CREATE TABLE IF NOT EXISTS "orders"(
    "Id" TEXT PRIMARY KEY,
    "OrderAt" DATETIME NOT NULL,
    "StoreId" TEXT,
    "UserId" TEXT,
    FOREIGN KEY ("StoreId") REFERENCES "stores"("Id"),
    FOREIGN KEY ("UserId") REFERENCES "users"("Id")
);

CREATE TABLE IF NOT EXISTS "items"(
    "Id" TEXT PRIMARY KEY,
    "Name" TEXT NOT NULL,
    "Type" TEXT,
    "UnitPrice" INTEGER -- REAL 만약 달러면
);

CREATE TABLE IF NOT EXISTS "orderitems"(
    "Id" TEXT PRIMARY KEY,
    "OrderId" TEXT,
    "ItemId" TEXT,
    FOREIGN KEY ("OrderId") REFERENCES "orders"("Id"),
    FOREIGN KEY ("ItemId") REFERENCES "items"("Id")
);
