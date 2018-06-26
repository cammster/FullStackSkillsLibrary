/*SQL Homework Week 10 Andrea Karaffa*/
/*Perform queries on the Sakila database*/
/*1a. Display first and last name of all actors from actor table*/
USE sakila;
SELECT first_name,last_name
FROM actor;

/*1b. Display first and last name together in upper case letters, name column Actor Name*/
SELECT UPPER(CONCAT_WS(' ',first_name,last_name)) Actor_Name
FROM actor;

/*2a. You need to find the ID number, first name, and last name of an actor, 
of whom you know only the first name, "Joe." */
SELECT actor_id, first_name,last_name
FROM actor
WHERE first_name="JOE";

/*2b. Find all actors whose last name contain the letters GEN:*/
SELECT actor_id, first_name,last_name
FROM actor
WHERE last_name LIKE "%GEN%";

/*2c. Find all actors whose last names contain the letters LI. 
This time, order the rows by last name and first name, in that order:*/
SELECT actor_id, first_name,last_name
FROM actor
WHERE last_name LIKE "%LI%"
ORDER BY last_name, first_name ASC;

/*2d. Using IN, display the country_id and country columns of the following countries:
 Afghanistan, Bangladesh, and China: */
 SELECT country_id,country
 FROM country
 WHERE country IN ("Afghanistan","Bangladesh","China");
 
 /*3a. Add a middle_name column to the table actor. Position it between first_name and last_name. Hint: you will need to specify the data type.*/
 SHOW COLUMNS FROM actor;
 ALTER TABLE actor
 ADD middle_name varchar(45) AFTER first_name;
 SHOW COLUMNS FROM actor;
  
 /*3b. You realize that some of these actors have tremendously long last names. Change the data type of the middle_name column to blobs.*/
 ALTER TABLE actor
 MODIFY COLUMN middle_name blob;
 SHOW COLUMNS FROM actor;
 
 /*3c. Now delete the middle_name column.*/
 ALTER TABLE actor
 DROP COLUMN middle_name;
 SHOW COLUMNS FROM actor;
 
 /*4a. List the last names of actors, as well as how many actors have that last name.*/
SELECT last_name,COUNT(*) FROM actor
GROUP BY last_name;

/*4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors*/
SELECT last_name,COUNT(*) FROM actor
GROUP BY last_name
HAVING COUNT(*)>1;

/*4c. Oh, no! The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. 
 Write a query to fix the record.*/
SHOW COLUMNS FROM actor;
SELECT * FROM actor
	WHERE last_name="Williams" AND first_name="GROUCHO";
UPDATE actor
	SET first_name="HARPO" 
	WHERE last_name="Williams" AND first_name="GROUCHO";
SELECT * FROM actor
		WHERE actor_id=172;

/*4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! 
In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO. Otherwise, change the first name to MUCHO GROUCHO, as that is exactly what the actor will be with the grievous error. 
BE CAREFUL NOT TO CHANGE THE FIRST NAME OF EVERY ACTOR TO MUCHO GROUCHO, HOWEVER! (Hint: update the record using a unique identifier.)*/
UPDATE actor
SET first_name= CASE
	WHEN first_name="HARPO" THEN "GROUCHO"
	ELSE "MUCHO GROUCHO"
	END 
WHERE actor_id=172;
SELECT * FROM actor
	WHERE actor_id=172;

/*5a. You cannot locate the schema of the address table. Which query would you use to re-create it?*/
SHOW CREATE TABLE address;

/*6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:*/
SELECT staff.first_name,staff.last_name,address.address FROM staff
	INNER JOIN address
	ON address.address_id=staff.address_id;

/*6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.*/
SELECT payment.staff_id,staff.first_name,staff.last_name,EXTRACT(YEAR_MONTH FROM payment.payment_date) AS DATE,SUM(payment.amount) AS Aug_2005_Total FROM payment
JOIN staff USING (staff_id)
	WHERE payment_date LIKE "2005-08%"
GROUP BY staff_id;

/*6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.*/
SELECT film.film_id,film.title,COUNT(film_actor.actor_id) AS actor_count FROM film
	INNER JOIN film_actor USING (film_id)
GROUP BY film_id;

/*6d. How many copies of the film Hunchback Impossible exist in the inventory system?*/
SELECT COUNT(inventory_id),film_id FROM inventory
	WHERE film_id IN 
    (
		SELECT film_id FROM film
		WHERE title="Hunchback Impossible"
    )
    ;
/*6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. 
List the customers alphabetically by last name:*/
SELECT customer.customer_id,customer.first_name,customer.last_name,SUM(payment.amount) AS customer_total FROM customer
	INNER JOIN payment USING (customer_id)
GROUP BY customer_id
ORDER BY customer.last_name;

/*7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. 
As an unintended consequence, films starting with the letters K and Q have also soared in popularity. 
Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.*/
SELECT title FROM film
	WHERE 
		title LIKE "K%" OR title LIKE "Q%" 
		AND 
        language_id IN (
			SELECT language_id FROM language 
			WHERE name="English"
						)
        ;
        
/*7b. Use subqueries to display all actors who appear in the film Alone Trip.*/
SELECT actor_id,first_name,last_name FROM actor
	WHERE actor_id IN 
		(SELECT actor_id from film_actor
			WHERE film_id IN
				(SELECT film_id FROM film
					WHERE title="Alone Trip"
                    )
		);
        
/*7c. You want to run an email marketing campaign in Canada, 
for which you will need the names and email addresses of all Canadian customers. 
Use joins to retrieve this information.*/ 
SELECT customer_id as canadian_customers,first_name,last_name,email FROM customer
	INNER JOIN address USING (address_id)
	INNER JOIN city USING (city_id)
	INNER JOIN country USING (country_id)
WHERE country.country="Canada";

/*7d. Sales have been lagging among young families,and you wish to target all family movies for a promotion.
 Identify all movies categorized as family films.*/ 
 SELECT title as family_movies FROM film
	WHERE film_id IN 
		(SELECT film_id FROM film_category
        WHERE category_id IN
			(SELECT category_id FROM category
            WHERE name="Family"
            )
         )
         ;
         
/*7e. Display the most frequently rented movies in descending order.*/
SELECT film.title,COUNT(rental.rental_id) AS rental_count FROM film
	INNER JOIN inventory USING (film_id)
	INNER JOIN rental USING (inventory_id)
GROUP BY film.title
HAVING rental_count>30
ORDER BY rental_count DESC
LIMIT 10
;

/*7f. Write a query to display how much business, in dollars, each store brought in.*/
SELECT store.store_id,SUM(payment.amount) AS store_total from payment
	INNER JOIN staff USING (staff_id)
	INNER JOIN store USING(store_id)
GROUP BY store_id
ORDER BY store_total DESC;

/*7g. Write a query to display for each store its store ID, city, and country.*/
SELECT store.store_id,city.city,country.country FROM store
	INNER JOIN address USING (address_id)
	INNER JOIN city USING (city_id)
	INNER JOIN country USING (country_id);

/*7h. List the top five genres in gross revenue in descending order. 
(Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)*/
SELECT category.name,SUM(payment.amount) AS genre_gross_revenue FROM payment
	INNER JOIN rental USING (rental_id)
	INNER JOIN inventory USING (inventory_id)
	INNER JOIN film_category USING (film_id)
	INNER JOIN category USING (category_id)
GROUP BY category.name
ORDER BY genre_gross_revenue DESC
LIMIT 5
;

/*8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. 
Use the solution from the problem above to create a view. 
If you haven't solved 7h, you can substitute another query to create a view.*/
CREATE VIEW TOP_5_GENRES AS
	SELECT category.name,SUM(payment.amount) AS genre_gross_revenue FROM payment
		INNER JOIN rental USING (rental_id)
		INNER JOIN inventory USING (inventory_id)
		INNER JOIN film_category USING (film_id)
		INNER JOIN category USING (category_id)
	GROUP BY category.name
	ORDER BY genre_gross_revenue DESC
	LIMIT 5
;

/*8b. How would you display the view that you created in 8a?*/
SELECT * FROM TOP_5_GENRES;

/*8c. You find that you no longer need the view top_five_genres. Write a query to delete it.*/
DROP VIEW TOP_5_GENRES;




    
	