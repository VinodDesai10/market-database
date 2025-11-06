create database market;
use market;
show tables;
create table customers(
customer_id int not null,
customer_name varchar(50) ,
customer_address varchar(100),
primary key (customer_id));

create table orders(
order_id int not null,
customer_id int,
order_date date ,
order_item varchar(100),
primary key (order_id),
foreign key (customer_id) references customers(customer_id));

create table products(
product_id int not null,
product_name varchar(50) ,
category varchar(50),
product_quantity int ,
product_price int ,
primary key (product_id));

create table markets(
market_id int not null,
market_name varchar(50),
market_location varchar(50),
market_size int ,
primary key (market_id));

create table stall (
market_id int ,
stall_location int ,
stall_id int not null,
primary key (market_id,stall_id),
foreign key (market_id) references markets(market_id));

create table schedules(
market_id int ,
schedule_date date,
schedule_time time,
primary key (market_id),
foreign key (market_id) references markets(market_id));

create table farmers(
farmer_id int not null,
farmer_name varchar(50),
farmer_phone_number int ,
farmer_address varchar(100),
primary key (farmer_id));

create table vendors(
vendor_id int not null,
vendor_name varchar(50),
vendor_email varchar(50),
vendor_pancard varchar(20),
vendor_phone_number varchar(100),
primary key (vendor_id));

create table supply(
farmer_id int,
vendor_id int,
supply_quantity int ,
supply_date date,
primary key (farmer_id,vendor_id),
foreign key (farmer_id) references farmers(farmer_id),
foreign key (vendor_id) references vendors(vendor_id));

create table inventory(
vendor_id int ,
product_id int,
product_quantity int,
last_update datetime ,
primary key (vendor_id,product_id),
foreign key (vendor_id) references vendors(vendor_id),
foreign key (product_id) references products(product_id));

create table payment(
payment_id int not null,
order_id int ,
payment_amount int,
payment_date date,
primary key (payment_id),
foreign key (order_id) references orders(order_id));


alter table orders
add column vendor_id int ,
add constraint foreign key (vendor_id) references vendors(vendor_id);

alter table orders
add column order_amount int;

INSERT INTO customers (customer_id, customer_name, customer_address) VALUES
(1, 'Aarav Sharma', '123 MG Road, Bengaluru'),
(2, 'Vivaan Singh', '456 Koramangala, Bengaluru'),
(3, 'Aditya Gupta', '789 Indiranagar, Bengaluru'),
(4, 'Diya Patel', '101 Jayanagar, Bengaluru'),
(5, 'Ishaan Kumar', '212 Whitefield, Bengaluru'),
(6, 'Ananya Reddy', '333 HSR Layout, Bengaluru'),
(7, 'Rohan Mehta', '444 Electronic City, Bengaluru'),
(8, 'Saanvi Joshi', '555 Marathahalli, Bengaluru'),
(9, 'Kabir Verma', '666 BTM Layout, Bengaluru'),
(10, 'Myra Agarwal', '777 JP Nagar, Bengaluru'),
(11, 'Arjun Desai', '888 Malleswaram, Bengaluru'),
(12, 'Zoya Khan', '999 Fraser Town, Bengaluru'),
(13, 'Vihaan Iyer', '110 Rajajinagar, Bengaluru'),
(14, 'Kiara Rao', '121 Basavanagudi, Bengaluru'),
(15, 'Aryan Nair', '131 Cooke Town, Bengaluru'),
(16, 'Priya Murthy', '142 Ulsoor, Bengaluru'),
(17, 'Sai Prasad', '153 Richmond Town, Bengaluru'),
(18, 'Anika Hegde', '164 Cox Town, Bengaluru'),
(19, 'Reyansh Shenoy', '175 Yelahanka, Bengaluru'),
(20, 'Advait Pillai', '186 RT Nagar, Bengaluru');

INSERT INTO products (product_id, product_name, category, product_quantity, product_price) VALUES
(301, 'Organic Apples', 'Fruits', 150, 180),
(302, 'Fresh Tomatoes', 'Vegetables', 200, 40),
(303, 'Basmati Rice', 'Grains', 500, 120),
(304, 'Whole Milk', 'Dairy', 100, 60),
(305, 'Brown Bread', 'Bakery', 80, 45),
(306, 'Carrots', 'Vegetables', 250, 50),
(307, 'Bananas', 'Fruits', 300, 40),
(308, 'Cheddar Cheese', 'Dairy', 60, 250),
(309, 'Onions', 'Vegetables', 400, 30),
(310, 'Potatoes', 'Vegetables', 500, 35),
(311, 'Almonds', 'Nuts', 120, 800),
(312, 'Organic Spinach', 'Vegetables', 90, 60),
(313, 'Chicken Breast', 'Meat', 70, 450),
(314, 'Olive Oil', 'Oils', 100, 700),
(315, 'Whole Wheat Flour', 'Grains', 300, 55),
(316, 'Lentils (Toor Dal)', 'Grains', 250, 140),
(317, 'Cucumbers', 'Vegetables', 180, 25),
(318, 'Mangoes', 'Fruits', 100, 100),
(319, 'Paneer', 'Dairy', 110, 350),
(320, 'Eggs (Dozen)', 'Poultry', 150, 75);

INSERT INTO markets (market_id, market_name, market_location, market_size) VALUES
(401, 'KR Market', 'Kalasipalyam', 15000),
(402, 'Malleshwaram Market', 'Malleshwaram', 8000),
(403, 'Jayanagar 4th Block Market', 'Jayanagar', 12000),
(404, 'Gandhi Bazaar', 'Basavanagudi', 9500),
(405, 'Indiranagar Market', 'Indiranagar', 7000),
(406, 'Whitefield Farmers Market', 'Whitefield', 11000),
(407, 'HSR Layout Organic Market', 'HSR Layout', 6500),
(408, 'Yelahanka Santhe', 'Yelahanka', 13000),
(409, 'Koramangala Weekly Market', 'Koramangala', 5000),
(410, 'Electronic City Market', 'Electronic City', 10000),
(411, 'RT Nagar Daily Market', 'RT Nagar', 7500),
(412, 'Marathahalli Market', 'Marathahalli', 14000),
(413, 'Hebbal Market', 'Hebbal', 8500),
(414, 'Yeshwantpur APMC Yard', 'Yeshwantpur', 25000),
(415, 'Shivajinagar Market', 'Shivajinagar', 16000);


alter table farmers
modify farmer_phone_number varchar(15);


INSERT INTO farmers (farmer_id, farmer_name, farmer_phone_number, farmer_address) VALUES
(201, 'Ramesh Gowda', '9876543210', 'Chikkaballapur, Karnataka'),
(202, 'Suresh Reddy', '9876543211', 'Kolar, Karnataka'),
(203, 'Manjunath Kumar', '9876543212', 'Doddaballapur, Karnataka'),
(204, 'Lakshmiamma', '9876543213', 'Ramanagara, Karnataka'),
(205, 'Ganeshappa', '9876543214', 'Magadi, Karnataka'),
(206, 'Kiran Patel', '9876543215', 'Hoskote, Karnataka'),
(207, 'Prakash Naidu', '9876543216', 'Devanahalli, Karnataka'),
(208, 'Savita Rao', '9876543217', 'Anekal, Karnataka'),
(209, 'Anand Murthy', '9876543218', 'Kanakapura, Karnataka'),
(210, 'Bhaskar Hegde', '9876543219', 'Nelamangala, Karnataka'),
(211, 'Chandrappa', '9876543220', 'Sidlaghatta, Karnataka'),
(212, 'Devraj Urs', '9876543221', 'Malur, Karnataka'),
(213, 'Eshwarappa', '9876543222', 'Gauribidanur, Karnataka'),	
(214, 'Farida Begum', '9876543223', 'Bagepalli, Karnataka'),
(215, 'Girish Sharma', '9876543224', 'Chintamani, Karnataka');

INSERT INTO vendors (vendor_id, vendor_name, vendor_email, vendor_pancard, vendor_phone_number) VALUES
(101, 'Fresh Farms Co.', 'contact@freshfarms.com', 'AGBPC1234F', '9988776655'),
(102, 'GreenLeaf Organics', 'support@greenleaf.com', 'BJHPS5678G', '9988776654'),
(103, 'Daily Veggies', 'orders@dailyveggies.in', 'CKLPT9012H', '9988776653'),
(104, 'Natures Basket', 'help@naturesbasket.com', 'DMNQW3456J', '9988776652'),
(105, 'The Grain Store', 'info@grainstore.com', 'EORVX7890K', '9988776651'),
(106, 'Dairy Delights', 'dairy@delights.com', 'FPZAY1234L', '9988776650'),
(107, 'Healthy Harvest', 'healthy@harvest.co', 'GQBXC5678M', '9988776649'),
(108, 'City Grocers', 'city@grocers.in', 'HRDWE9012N', '9988776648'),
(109, 'Organic Roots', 'roots@organic.com', 'ISFVF3456P', '9988776647'),
(110, 'Sunrise Provisions', 'sunrise@provisions.com', 'JTGHG7890Q', '9988776646'),
(111, 'The Fruit Stall', 'fruits@stall.com', 'KUIHH1234R', '9988776645'),
(112, 'Village Farm Fresh', 'village@farm.com', 'LVJII5678S', '9988776644'),
(113, 'Prime Meats', 'prime@meats.com', 'MWKJJ9012T', '9988776643'),
(114, 'Artisan Bakes', 'artisan@bakes.co', 'NXLKK3456V', '9988776642'),
(115, 'Bangalore Organics', 'bangalore@organics.in', 'OYMLL7890W', '9988776641');

INSERT INTO orders (order_id, customer_id, order_date, order_item, vendor_id, order_amount) VALUES
(501, 1, '2025-10-01', 'Organic Apples, Brown Bread', 101, 225),
(502, 3, '2025-10-01', 'Fresh Tomatoes, Onions, Potatoes', 103, 105),
(503, 5, '2025-10-02', 'Basmati Rice', 105, 120),
(504, 2, '2025-10-02', 'Whole Milk, Cheddar Cheese', 106, 310),
(505, 4, '2025-10-03', 'Carrots, Organic Spinach', 102, 110),
(506, 7, '2025-10-03', 'Chicken Breast', 113, 450),
(507, 6, '2025-10-04', 'Bananas', 111, 40),
(508, 9, '2025-10-04', 'Almonds, Olive Oil', 104, 1500),
(509, 8, '2025-10-05', 'Paneer', 106, 350),
(510, 10, '2025-10-05', 'Whole Wheat Flour, Lentils', 105, 195),
(511, 12, '2025-10-06', 'Eggs (Dozen)', 112, 75),
(512, 11, '2025-10-06', 'Cucumbers, Tomatoes', 103, 65),
(513, 14, '2025-10-06', 'Mangoes', 111, 100),
(514, 15, '2025-10-07', 'Brown Bread', 114, 45),
(515, 13, '2025-10-07', 'Organic Apples', 107, 180),
(516, 1, '2025-10-07', 'Onions, Potatoes', 103, 65),
(517, 18, '2025-10-08', 'Olive Oil', 109, 700),
(518, 20, '2025-10-08', 'Chicken Breast, Eggs (Dozen)', 113, 525),
(519, 17, '2025-10-08', 'Basmati Rice, Lentils', 105, 260),
(520, 19, '2025-10-08', 'Whole Milk', 106, 60);

INSERT INTO payment (payment_id, order_id, payment_amount, payment_date) VALUES
(601, 501, 225, '2025-10-01'),
(602, 502, 105, '2025-10-01'),
(603, 503, 120, '2025-10-02'),
(604, 504, 310, '2025-10-02'),
(605, 505, 110, '2025-10-03'),
(606, 506, 450, '2025-10-03'),
(607, 507, 40, '2025-10-04'),
(608, 508, 1500, '2025-10-04'),
(609, 509, 350, '2025-10-05'),
(610, 510, 195, '2025-10-05'),
(611, 511, 75, '2025-10-06'),
(612, 512, 65, '2025-10-06'),
(613, 513, 100, '2025-10-06'),
(614, 514, 45, '2025-10-07'),
(615, 515, 180, '2025-10-07'),
(616, 516, 65, '2025-10-07'),
(617, 517, 700, '2025-10-08'),
(618, 518, 525, '2025-10-08'),
(619, 519, 260, '2025-10-08'),
(620, 520, 60, '2025-10-08');

INSERT INTO stall (market_id, stall_location, stall_id) VALUES
(401, 10, 1), 
(401, 12, 2), 
(401, 25, 3),
(402, 5, 4), 
(402, 15, 5),
(403, 1, 6), 
(403, 2, 7), 
(403, 22, 8),
(404, 18, 9), 
(404, 30, 10),
(405, 7, 11),
(406, 9, 12), 
(406, 11, 13),
(407, 4, 14),
(408, 45, 15),
(414, 101, 16), 
(414, 102, 17), 
(414, 250, 18);

INSERT INTO schedules (market_id, schedule_date, schedule_time) VALUES
(401, '2025-10-10', '06:00:00'),
(402, '2025-10-11', '07:00:00'),
(403, '2025-10-11', '08:00:00'),
(404, '2025-10-12', '06:30:00'),
(405, '2025-10-12', '09:00:00'),
(406, '2025-10-12', '10:00:00'),
(407, '2025-10-13', '08:30:00'),
(408, '2025-10-13', '05:00:00'),
(409, '2025-10-14', '16:00:00'),
(410, '2025-10-14', '07:00:00'),
(411, '2025-10-10', '07:30:00'),
(412, '2025-10-11', '06:00:00'),
(413, '2025-10-12', '08:00:00'),
(414, '2025-10-13', '04:00:00'),
(415, '2025-10-13', '05:30:00');

INSERT INTO supply (farmer_id, vendor_id, supply_quantity, supply_date) VALUES
(201, 101, 100, '2025-09-28'),
(201, 111, 150, '2025-09-28'),
(202, 103, 250, '2025-09-29'), 
(202, 107, 300, '2025-09-29'),
(203, 108, 400, '2025-09-29'),
(204, 102, 150, '2025-09-30'), 
(204, 109, 120, '2025-09-30'),
(205, 105, 500, '2025-10-01'),
(206, 106, 80, '2025-10-01'), 
(206, 112, 100, '2025-10-01'),
(207, 113, 75, '2025-10-02'),
(208, 114, 50, '2025-10-03'),
(209, 104, 200, '2025-10-03'),
(210, 110, 300, '2025-10-04'),
(211, 101, 120, '2025-10-05');

INSERT INTO inventory (vendor_id, product_id, product_quantity, last_update) VALUES
(101, 301, 90, '2025-10-07 11:00:00'),
(103, 302, 150, '2025-10-06 09:30:00'),
(105, 303, 400, '2025-10-05 14:00:00'),
(106, 304, 70, '2025-10-08 10:00:00'),
(114, 305, 60, '2025-10-07 08:00:00'),
(102, 306, 200, '2025-10-03 12:00:00'),
(111, 307, 250, '2025-10-04 11:30:00'),
(106, 308, 45, '2025-10-02 15:00:00'),
(103, 309, 320, '2025-10-07 11:15:00'),
(108, 310, 450, '2025-10-07 11:15:00'),
(104, 311, 100, '2025-10-04 18:00:00'),
(102, 312, 75, '2025-10-03 12:00:00'),
(113, 313, 50, '2025-10-08 13:00:00'),
(109, 314, 80, '2025-10-08 14:00:00'),
(105, 316, 200, '2025-10-08 15:00:00');


DELIMITER //

create function total_expenditure(cust_id int)
returns int 
deterministic 
begin 
	declare am int default 0;
    select sum(o.order_amount) into am from customers c
    join orders o on c.customer_id=o.customer_id
    where o.customer_id=cust_id;
    return am;
end //
DELIMITER ;   


DELIMITER //

create function total_stock(prdt_name varchar(50))
returns int
deterministic
begin
	declare quant int;
    select i.product_quantity into  quant 
    from products p 
    join
    inventory i
    on p.product_id=i.product_id 
    where p.product_name=prdt_name;
    return quant;
end //

DELIMITER ;    

DELIMITER //

CREATE PROCEDURE PlaceNewOrder(
    IN p_order_id INT,          
    IN p_customer_id INT,       
    IN p_vendor_id INT,         
    IN p_product_id INT,        
    IN p_order_quantity INT     
)
BEGIN
    
    DECLARE v_current_stock INT;
    DECLARE v_product_price INT;
    DECLARE v_product_name VARCHAR(50);
    DECLARE v_total_amount INT;

    
    SELECT product_quantity INTO v_current_stock
    FROM inventory
    WHERE vendor_id = p_vendor_id AND product_id = p_product_id;

    SELECT product_name, product_price INTO v_product_name, v_product_price
    FROM products
    WHERE product_id = p_product_id;


    IF v_current_stock IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Vendor does not stock this product.';
    ELSEIF p_order_quantity > v_current_stock THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Error: Insufficient stock for the quantity requested.';
    ELSE
        
        START TRANSACTION;

        
        SET v_total_amount = v_product_price * p_order_quantity;

        
        INSERT INTO orders (order_id, customer_id, order_date, order_item, vendor_id, order_amount)
        VALUES (p_order_id, p_customer_id, CURDATE(), v_product_name, p_vendor_id, v_total_amount);

        
        UPDATE inventory
        SET product_quantity = product_quantity - p_order_quantity,
            last_update = NOW()
        WHERE vendor_id = p_vendor_id AND product_id = p_product_id;

        COMMIT;

        
        SELECT 'Order placed successfully!' AS result;

    END IF;
END //

DELIMITER ;

-- show procedure status where db='market';

DELIMITER //

CREATE PROCEDURE ProcessSupplyDelivery(
    IN p_farmer_id INT,           
    IN p_vendor_id INT,           
    IN p_product_id INT,          
    IN p_supplied_quantity INT    
)
BEGIN
    
    START TRANSACTION;

    
    INSERT INTO supply (farmer_id, vendor_id, supply_quantity, supply_date)
    VALUES (p_farmer_id, p_vendor_id, p_supplied_quantity, CURDATE());

    
    INSERT INTO inventory (vendor_id, product_id, product_quantity, last_update)
    VALUES (p_vendor_id, p_product_id, p_supplied_quantity, NOW())
    ON DUPLICATE KEY UPDATE
        product_quantity = product_quantity + VALUES(product_quantity),
        last_update = NOW();

    COMMIT;

    
    SELECT 'Inventory successfully updated.' AS result;

END //

DELIMITER ;

-- show procedure status where db='market'; 


DELIMITER //

CREATE TRIGGER before_payment_insert
BEFORE INSERT ON payment
FOR EACH ROW
BEGIN
    DECLARE correct_amount INT;
    SELECT order_amount INTO correct_amount FROM orders WHERE order_id = NEW.order_id;
    IF NEW.payment_amount != correct_amount THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Payment amount does not match the order amount.';
    END IF;
END //

DELIMITER ;

-- 1. Drop the foreign keys using the names you found
ALTER TABLE supply DROP FOREIGN KEY supply_ibfk_1;
ALTER TABLE supply DROP FOREIGN KEY supply_ibfk_2;

-- 2. Drop the old primary key (This will work now)
ALTER TABLE supply DROP PRIMARY KEY;

-- 3. Add the new supply_id primary key
ALTER TABLE supply ADD COLUMN supply_id INT AUTO_INCREMENT PRIMARY KEY FIRST;

-- 4. Add the foreign keys back (We give them new, clear names)
ALTER TABLE supply ADD CONSTRAINT fk_supply_farmer
FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id);
ALTER TABLE supply ADD CONSTRAINT fk_supply_vendor
FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id);

ALTER TABLE payment DROP PRIMARY KEY;

ALTER TABLE payment MODIFY payment_id INT AUTO_INCREMENT PRIMARY KEY;

ALTER TABLE orders DROP PRIMARY KEY;

ALTER TABLE orders
MODIFY COLUMN order_id INT NOT NULL AUTO_INCREMENT,
ADD PRIMARY KEY (order_id);

ALTER TABLE payment
ADD CONSTRAINT fk_payment_order
FOREIGN KEY (order_id) REFERENCES orders(order_id)
ON DELETE CASCADE ON UPDATE CASCADE;