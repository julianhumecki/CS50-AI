import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}





def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    naming = input("Name: ");
    source = person_id_for_name(naming)
    #print("Source == Sally Field")
    #print(naming == "Sally Field")
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        #print(path)
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

        


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    #queue
    frontier = QueueFrontier()

    #print(len(people))
    #print(people['102']['birth'])

    parent_id = None
    current_id = source

    current_node = None
    parent_node = None
    #print("Source: "+source)

    visited = set()

    #set up my frontier
    firstTime = True
    counter = 0
   
    finished = False
    end_node = None
    starting_node = None
    
    #first time through fill 
    while True:
        
        # print("New iteration: ")
        # print("First Time: ")
        # print(firstTime)
        # print("Frontier: ")
        # print(frontier.len())
        #if there's nothing left in our queue we are done        
        if frontier.empty() and not firstTime:
            return None

        #makes sure this happens every time after the initial run
        if not firstTime:
            # print("Not first time")
            parent_node = current_node
            #guarantees right starting node
            if(counter == 1):
                current_node = starting_node
            
            else:
                current_node = frontier.remove()

            current_id = current_node.state[1]
           
            #print("Parent Node: ")
            #print(parent_node.state)
            
            #add to visited
            visited.add(current_node.state)

        # print("Name: "+ people[current_id]["name"])
        # print("Tuple: ")

        # if not current_node == None: print(current_node.state)
        movies_of_current = people[str(current_id)]["movies"]

        for movie in movies_of_current:
            #print("Movie: " + movie)
            #get all our actors and actresses in this movie
            stars = movies[str(movie)]["stars"]
            for star in stars:
                # print("Movie: "+movies[movie]["title"] + " Star: "+people[star]["name"])
                node = Node(state=(movie, star), parent=current_node)
                # print(node.state)
                if star == target:
                    #done
                    #break and backtrack
                    end_node = node
                    finished = True
                    break
                else:
                    # print("node in frontier")
                    # print(frontier.contains_state(node.state))
                    # print("node in visited: ")
                    # print(node.state in visited)
                    if not frontier.contains_state(node.state):
                        if not node.state in visited:
                            if firstTime:
                                
                                if star == source:
                                    
                                    starting_node = node
                                else:
                                    #print("Added")
                                    frontier.add(node)
                            else:
                                #print("Added")
                                frontier.add(node)
                            
                    #otherwise node exists
            if finished:
                break

        
        firstTime = False
        if counter < 2:
            counter += 1;

        if finished:
            break
    

    #print("Done")
    ##print(end_node.state[1] == target)
    

    current_node = end_node
    path = []
    while not current_node.parent == None:
        temp = current_node.parent
        path.append(current_node.state)
        current_node = temp
    #add the last element    
    path.append(current_node.state)
    path.reverse()
    #print(path)
    return path
    # TODO
    #raise NotImplementedError

def initialize_visited(source):

    current_id = source

    movies_of_current = people[str(current_id)]["movies"]

    for movie in movies_of_current:
        #p_node = Node(state=(current_id, movie), parnet=parent_id)
        #get all our actors and actresses
        stars = movies[str(movie)]["stars"]
        for star in stars:
            node = (movie, star)
            if star == target:
                #done
                #break and backtrack
                break
            else:
                if not node in visited:
                    visited[node] = False



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
