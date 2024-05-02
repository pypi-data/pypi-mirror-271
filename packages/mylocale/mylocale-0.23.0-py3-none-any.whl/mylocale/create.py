def main():
    name = "localisation.csv"
    string = "stringname,en_EN\nHELLOWORLD,Hello World"
    with open(file=name, mode="w") as f:
        f.write(string)
    print(f"created {name} successfully")


if __name__ == "__main__":
    main()
