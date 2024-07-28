import argparse

parser = argparse.ArgumentParser()

# 1 
parser.add_argument("-column", "-col", type = str, choices = ["director", "cast"], 
                    help = "Choose a column between director and cast")
parser.add_argument("-topN", "-n", type = int, choices = range(1,11), default = 5, 
                    help = "Choose a number for top N directors or actors or stay with default 5")

# 2 
parser.add_argument("-interval", "-i", type = str, choices= ["year", "month"],
                    help= "Choose interval for grouping")

# 3 
parser.add_argument("-type","-tp", type=str, choices=["Movie", "TV"],
                    help= "Choose type - TV or Movie")

# 4 
parser.add_argument("-rating", "-r", action='store_true', 
                    help= "Choose for age group viz")
parser.add_argument("-total_counts", "-tc", type = int, choices = range(50,1000, 50), default = 100, 
                    help = "Choose a number for total counts to filter countries or stay with default 100")


args = parser.parse_args()

