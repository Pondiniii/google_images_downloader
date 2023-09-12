def search_query_gen(search_query: str):
    resolution = "6mp"  # Minimum resolution
    color = "trans"  # Transparent images

    # Replace space to "%20" in search_query
    search_query = search_query.replace(" ", "%20")

    url = f"https://www.google.com/search?tbm=isch&q={search_query}&tbs=isz:lt,islt:{resolution},ic:{color}"
    return url
