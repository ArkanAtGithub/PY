def search_symbol():
    # http://www.aprs.org/symbols/symbolsX.txt
    symbol = {
        "house": "/ -",
        "car": "/ >",
        "human": "/ [",
        "phone": "/ $"
    }

    a = input("Symbol name: ")

    if a in symbol:
        table, sub = symbol[a].split()
    else:
        table, sub = None, None
        print("Not found")
        exit()

    print(f"Table: {table}, Sub: {sub}")

search_symbol()