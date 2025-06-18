
"""
Colors are not numeric values, but wee can assign each color a numeric value as follows:
Create a color map dictionary.
"""
def distinct(data):
    distinct_colors = []
    for i in data:
        if i not in distinct_colors:
            distinct_colors.append(i)
        else:
            pass
    return distinct_colors

def create_map(data):
    distinct_colors = distinct(data)
    value = 1
    color_map = {}
    for i in distinct_colors:
        color_map[i] = value
        value+=1
    return color_map

"""key feature 1"""
def mean_color(data: list):
    # Create a dictionary color:value map
    color_map = create_map(data)
    
    # Convert all colors to numbers
    colors = data
    color_numbers = [color_map[i] for i in colors]

    # Mean color
    mean_value = sum(color_numbers)//len(color_numbers)
    for i in color_map:
        if color_map[i] == mean_value:
            color = i
            break
    return color


"""Key feature 2
The most worn feature takes in a list of colors or a list of color lists each list representing each day
"""
from collections import Counter

def most_worn(data):
    mode = lambda data: Counter(data).most_common(1)[0][0]
    modes = []

    if type(data[0]) is not list:
        return mode(data)
    
    elif type(data[0]) is list:
        increment = 1
        for i in data:
            print(f'Mode {increment}: {mode(i)}')
            modes.append(mode(i))
            increment += 1
        print("Overall Most worn: ",  mode(modes))

"""key feature 3"""
def median_color(data):
    median = lambda colors: sorted(colors)[len(sorted(colors))//2]
    medians = []
    if type(data[0]) == list:
        for i in data:
            if type(i) != list:
                raise Exception("All items must be of the same type")
                return
        increment = 1
        for i in data:
            print(f"Day {increment} Median: {median(i)}")
            medians.append(median(i))
            increment+=1
        print("Overall Median color: ", median(medians))
    else:
        return median(data)

"""key feature 4"""
import numpy as np

def variance(data):
    color_map = create_map(data)
    # Convert colors to numbers
    numbers = [color_map[i] for i in data]
    var = np.var(numbers)
    return var


"""key feature 5"""
def probability(color: str, colors: list):
    color_frequency = colors.count(color)
    prob = color_frequency/len(colors)
    return prob

"""key feature 6"""
import psycopg2

def database(data):
    #Get distinct colors
    distinct_colors = distinct(data)

    #Create color: frequecy map
    color_counts = {}
    for i in distinct_colors:
        color_counts[i] = data.count(i)

    # Connect to the database
    conn = psycopg2.connect(
        host="your-host",
        database="your-database",
        user="your-username",
        password="your-password"
    )

    # Create a cursor
    cur = conn.cursor()

    # Create a table
    cur.execute("""
        CREATE TABLE colors (
            id SERIAL PRIMARY KEY,
            color VARCHAR(255),
            frequency INTEGER
        );
    """)

    # Insert colors into the table
    for color, frequency in color_counts.items():
        cur.execute("""
            INSERT INTO colors (color, frequency)
            VALUES (%s, %s);
        """, (color, frequency))

    # Commit the changes
    conn.commit()
    # Close the cursor and connection
    cur.close()
    conn.close()

"""key feature 7"""
def number_search(numbers, target):
    if len(numbers) == 0:
        return False
    elif numbers[0] == target:
        return True
    else:
        return number_search(numbers[1:], target)


"""key feature 8"""
from random import choice

def random_bin_to_dec():
    bin=''
    for i in range(4):
        bin+=choice('01')

    # Convert binary to decimal
    dec = int(bin,2)
    return dec


"""key feature 9"""
def fibonacci(n):
    a = 0
    b = 1
    total = 0
    for _ in range(n):
        total += a
        a = b
        b = a + b
    return total


# Data

monday = 'GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, BLUE, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN'.split(', ')
tuesday = 'ARSH, BROWN, GREEN, BROWN, BLUE, BLUE, BLEW, PINK, PINK, ORANGE, ORANGE, RED, WHITE, BLUE, WHITE, WHITE, BLUE, BLUE, BLUE'.split(', ')
wednesday = 'GREEN, YELLOW, GREEN, BROWN, BLUE, PINK, RED, YELLOW, ORANGE, RED, ORANGE, RED, BLUE, BLUE, WHITE, BLUE, BLUE, WHITE, WHITE'.split(', ')
thursday = 'BLUE, BLUE, GREEN, WHITE, BLUE, BROWN, PINK, YELLOW, ORANGE, CREAM, ORANGE, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, GREEN'.split(', ')
friday = 'GREEN, WHITE, GREEN, BROWN, BLUE, BLUE, BLACK, WHITE, ORANGE, RED, RED, RED, WHITE, BLUE, WHITE, BLUE, BLUE, BLUE, WHITE'.split(', ')

data= monday+tuesday+wednesday+thursday+friday


# Print results
print("Mean Color:", mean_color(data))
print("Most Worn Color:", most_worn(data))
print("Median Color:", median_color(data))
print("Variance:", variance(data))
print("Random binary to base 10:", random_bin_to_dec() )
print("Sum of first 50 Fibonacci numbers:", fibonacci(50))
print("Probability of Red Color:", probability('RED',data))
