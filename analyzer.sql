CREATE DATABASE IF NOT EXISTS analyzer;

USE analyzer;

CREATE TABLE IF NOT EXISTS ingredient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    cosmeticFunction VARCHAR(255),
    cir VARCHAR(255),
    ewg INT,
    goodDrySkin BOOLEAN,
    goodOilSkin BOOLEAN,
    goodSensitiveSkin BOOLEAN,
    notableEffects SET('ACNE_FIGHTING', 'BRIGHTENING', 'UV_PROTECTION', 'WOUND_HEALING', 'ANTI_AGING'),
    isParaben BOOLEAN,
    isSulfate BOOLEAN,
    isAlcohol BOOLEAN,
    isSilicone BOOLEAN,
    isEUAllergen BOOLEAN,
    isFungalAcneSafe BOOLEAN
);

CREATE TABLE IF NOT EXISTS product (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    barcode VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS product_ingredient (
    idProduct INT,
    idIngredient INT,
    PRIMARY KEY (idProduct, idIngredient),
    FOREIGN KEY (idProduct) REFERENCES product(Id),
    FOREIGN KEY (idIngredient) REFERENCES ingredient(Id)
);
