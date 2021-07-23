use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from test.product

-- 2. Выбрать названия всех автоматизированных складов
select name from test.store where is_automated = 1

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(total) from test.sale

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select distinct store_id from test.sale where quantity > 0


-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select distinct store_id from test.store natural left join test.sale where quantity is null

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select name, avg(total/quantity) from test.product join test.sale using(product_id) group by name

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select name from 
(select distinct name, store_id from test.product join test.sale using(product_id)) as t
group by name having count(name) = 1

-- 8. Получить названия всех складов, с которых продавался только один продукт
select distinct name from test.store where store_id = (
select store_id from 
(select distinct store_id, name from test.sale join test.product using(product_id)) as t
group by store_id having count(store_id) = 1)

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * from test.sale where total = (select max(total) from test.sale)

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date from 
(select date, sum(total) from test.sale group by date order by sum(total) desc, date) as t
limit 1
