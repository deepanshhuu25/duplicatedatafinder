def read_entries(file_name):
    try:
        file = open(file_name, "r", encoding="utf-8")
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        return None
    except UnicodeDecodeError:
        try:
            file = open(file_name, "r", encoding="latin-1")
            lines = file.readlines()
            file.close()
        except Exception:
            return None

    entries = []
    for line in lines:
        text = line.strip()          
        if text != "":               
            entries.append(text)
    return entries


def clean_entry(text):
    """Ignore-case mode: make lowercase and remove extra spaces.
    Example: '  Apple   Pie ' -> 'apple pie'"""
    words = text.lower().split()    
    return " ".join(words)


def get_unique(entries):
    """Return unique entries as a list (keeps the original order).
    A set is used to remember what we have already seen."""
    seen = set()
    unique_list = []
    for item in entries:
        if item not in seen:
            seen.add(item)
            unique_list.append(item)
    return unique_list


def find_duplicates(entries, unique_list):
    """Use a loop to count each unique entry.
    Return a list of (entry, count) for entries repeated more than once."""
    duplicates = []
    for item in unique_list:
        count = 0
        for entry in entries:
            if entry == item:
                count = count + 1
        if count > 1:
            duplicates.append((item, count))
    return duplicates


def save_unique(unique_list, output_file):
    """Save the unique entries to a file, one per line."""
    file = open(output_file, "w", encoding="utf-8")
    for item in unique_list:
        file.write(item + "\n")
    file.close()


def show_report(entries, unique_list, duplicates):
    """Print the result in the required format."""
    print("Total items:", len(entries), "| Unique items:", len(unique_list))

    if len(duplicates) == 0:
        print("No duplicates found.")
    else:
        parts = []
        for item, count in duplicates:
            parts.append(item + " (" + str(count) + " times)")
        print("Duplicates: " + " | ".join(parts))


def process_entries(entries, ignore_case_and_spaces=False):
    """Process a list of entries and return (processed_entries, unique_list, duplicates)."""
    if ignore_case_and_spaces:
        cleaned = []
        for item in entries:
            cleaned.append(clean_entry(item))
        entries = cleaned

    unique_list = get_unique(entries)
    duplicates = find_duplicates(entries, unique_list)
    return entries, unique_list, duplicates


def main():
    print("=" * 40)
    print("      DUPLICATE DATA FINDER")
    print("=" * 40)

   
    while True:
        file_name = input("Enter file name (e.g. data.txt): ").strip()
        entries = read_entries(file_name)
        if entries is None:
            print("File '" + file_name + "' not found. Please enter a valid file name.")
        else:
            break

    
    if len(entries) == 0:
        print("File is empty. Nothing to check.")
        return

    
    print("\nMenu")
    print("1. Exact match")
    print("2. Ignore case and extra spaces")
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice == "1" or choice == "2":
            break
        print("Invalid choice. Please enter 1 or 2.")

    
    entries, unique_list, duplicates = process_entries(entries, ignore_case_and_spaces=(choice == "2"))

  
    print()
    show_report(entries, unique_list, duplicates)

    save_unique(unique_list, "unique.txt")
    print("Unique list saved to unique.txt")


if __name__ == "__main__":
    main()
