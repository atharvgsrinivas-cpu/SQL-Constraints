import sqlite3
import pandas as pd

conn = sqlite3.connect('city.db')
conn.execute("DROP TABLE IF EXISTS cities")
conn.execute("""
CREATE TABLE cities (
     City_ID INTEGER PRIMARY KEY,
      City_Name TEXT NOT NULL UNIQUE,
     Country TEXT NOT NULL, 
        Population INTEGER,
          Is_Capital TEXT DEFAULT 'No'
        );
        """)
conn.commit()
print("Table created successfully")

conn.execute(" INSERT INTO cities VALUES (1, 'New York', 'USA', 8419600, 'No')")
conn.execute(" INSERT INTO cities VALUES (2, 'Los Angeles', 'USA', 3980400, 'No')")
conn.execute(" INSERT INTO cities VALUES (3, 'Chicago', 'USA', 2716000, 'No')")
conn.execute(" INSERT INTO cities VALUES (4, 'Houston', 'USA', 2328000, 'No')")
conn.execute(" INSERT INTO cities VALUES (5, 'Phoenix', 'USA', 1690000, 'No')")
conn.execute(" INSERT INTO cities VALUES (6, 'Philadelphia', 'USA', 1584200, 'No')")
conn.execute(" INSERT INTO cities VALUES (7, 'San Antonio', 'USA', 1547200, 'No')")
conn.execute(" INSERT INTO cities VALUES (8, 'San Diego', 'USA', 1423800, 'Yes')")
conn.commit()
print("Data inserted successfully")
city = pd.read_sql("SELECT * FROM cities", conn)
print(city)

print("\n------ TESTING PRIMARY KEY CONSTRAINT ------")
try:
    conn.execute("INSERT INTO cities VALUES (1, 'Dallas', 'USA', 1341000, 'No')")
    conn.commit()
except Exception as e:
    conn.rollback()
    print("city_id is a primary key, so it must be unique. Error:", e)



print("\n------ TESTING NOT NULL CONSTRAINT ------")
try:
    conn.execute("INSERT INTO cities VALUES (9, NULL, 'USA', 1341000, 'No')")
    conn.commit()
except Exception as e:
    conn.rollback()
    print("Rejected:", e)
    print("city_name is NOT NULL, so it cannot be NULL. Error:", e)


print("\n------ TESTING UNIQUE CONSTRAINT ------") 
try:
    conn.execute("INSERT INTO cities VALUES (10, 'New York', 'USA', 1341000, 'No')")
    conn.commit()
except Exception as e:
    conn.rollback()
    print("Rejected:", e)
    print("city_name is UNIQUE, so it cannot be duplicated. Error:", e)


print("\n------ TESTING DEFAULT VALUE ------")
conn.execute("INSERT INTO cities (City_ID, City_Name, Country, Population) VALUES (9, 'Austin', 'USA', NULL)")
conn.commit()
Austin = pd.read_sql("SELECT * FROM cities WHERE City_Name='Austin'", conn)
print(Austin)
print("Austin is not in the database, so it will be inserted with default value for Is_Capital.")

print("\n------ NULL IN THE POPULATION COLUMN ------")
all_cities = pd.read_sql("""SELECT  City_Name, Population, Country FROM cities""", conn)
print(all_cities)


missing_population = pd.read_sql("""SELECT  City_Name, Population, Country FROM cities WHERE Population IS NULL""", conn)
print("missing_population:")
print(missing_population)

has_data = pd.read_sql("""SELECT  City_Name, Population, Country FROM cities WHERE Population IS NOT NULL""", conn)
print("cities with population data:")
print(has_data)

conn.close()