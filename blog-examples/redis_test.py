# Connect to redis and execute test commands

import sys
import redis

def cmd_page_counts(redis_conn):
    # Just access the page counter item
    all_stats = redis_conn.hgetall('Richard#PAGES')

    pages_dict = {k.decode(): v.decode() for k, v in all_stats.items() if k.startswith(b'blog/articles')}
    pages_dict['Total'] = sum(map(int,pages_dict.values()))
    return pages_dict

def cmd_page_counts_full(redis_conn):
    # Perform traditional page count calculation

    # First get the index
    pages_set = redis_conn.smembers('Richard#INDEX')

    # Count the pages
    pages_dict = {page: len(redis_conn.keys(f"Richard#{page}*")) for page in map(bytes.decode, pages_set) if page.startswith('blog/articles')}
    pages_dict['Total'] = sum(map(int,pages_dict.values()))
    return pages_dict

def cmd_page_visits(redis_conn, page_id):
    # Just access the page and return the list
    return redis_conn.lrange(page_id, 0, -1)

def cmd_page_visits_full(redis_conn, page_id):
    # Get list of visits by querying partial index
    print(f"Querying {page_id}")

    key_list = redis_conn.keys(f'Richard#{page_id}*')

    return [k.split('#')[-1] for k in map(bytes.decode, key_list)]

if __name__ == "__main__":

    # Check the number of arguments
    if len(sys.argv) < 3:
        print("Error: Not enough arguments were provided")
        sys.exit()

    # Get the file name from the first argument
    remote = sys.argv[1]
    command = sys.argv[2]

    # Connect to redis
    r = redis.Redis(host=remote)
    try:
        r.ping()
    except Exception as e:
        print(f"Error: problem connecting to host: {remote}. Check it is the correct server address and redis is running.")
        sys.exit()

    # Make dictionary of all commands
    cmd_dict = {k[4:].replace('_', ''): v for k, v in locals().items() if k.startswith('cmd_')}
    # print(cmd_dict)

    # Run the command
    print(cmd_dict[command](r, *sys.argv[3:]))
