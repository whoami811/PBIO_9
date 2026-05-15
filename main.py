import random
def validate_positive_int(prompt: str,
                          min_val: int = 1,
                          max_val: int = 100000) -> int:

    while True:

        value = input(prompt)

        if not value.isdigit():
            print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")
            continue

        number = int(value)

        if min_val <= number <= max_val:
            return number

        print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")

def validate_seq_id() -> str:

    while True:

        seq_id = input("Enter sequence ID: ").strip()

        if seq_id == "":
            print("Error: ID cannot be empty.")
            continue

        if " " in seq_id:
            print("Error: ID cannot contain whitespace.")
            continue

        return seq_id

def validate_distribution() -> tuple:
    while True:

        print("\nEnter nucleotide distribution:")

        a = validate_positive_int("A percentage: ", 0, 100)
        c = validate_positive_int("C percentage: ", 0, 100)
        g = validate_positive_int("G percentage: ", 0, 100)
        t = validate_positive_int("T percentage: ", 0, 100)

        total = a + c + g + t

        if total == 100:
            return a, c, g, t

        print("Error: percentages must sum to 100.")
def generate_sequence(length: int) -> str:
    sequence = ""
    for _ in range(length):
        sequence += random.choice("ACGT")

    return sequence
def generate_custom_sequence(length: int,
                             a_percent: int,
                             c_percent: int,
                             g_percent: int,
                             t_percent: int) -> str:
    nucleotides = (
        ["A"] * a_percent +
        ["C"] * c_percent +
        ["G"] * g_percent +
        ["T"] * t_percent
    )

    sequence = ""
    for _ in range(length):
        sequence += random.choice(nucleotides)

    return sequence
def calculate_stats(sequence: str) -> dict:
    stats = {}

    length = len(sequence)

    for nucleotide in "ACGT":

        count = sequence.count(nucleotide)

        stats[nucleotide] = round((count / length) * 100, 2)

    gc_count = sequence.count("G") + sequence.count("C")

    stats["GC"] = round((gc_count / length) * 100, 2)

    return stats
def insert_name(sequence: str, name: str) -> str:

    position = random.randint(0, len(sequence))

    modified_sequence = (
        sequence[:position]
        + name.lower()
        + sequence[position:]
    )

    return modified_sequence


def format_fasta(seq_id: str,
                 description: str,
                 sequence: str,
                 line_width: int = 80) -> str:

    if description.strip() == "":
        header = f">{seq_id}"
    else:
        header = f">{seq_id} {description}"

    fasta_text = header + "\n"

    for i in range(0, len(sequence), line_width):
        fasta_text += sequence[i:i + line_width] + "\n"

    return fasta_text


def save_fasta(filename: str, content: str):

    with open(filename, "w") as file:
        file.write(content)

def search_motif(sequence: str, motif: str) -> list:

    positions = []

    for i in range(len(sequence) - len(motif) + 1):

        fragment = sequence[i:i + len(motif)]

        if fragment == motif:
            positions.append(i + 1)

    return positions


def complementary_sequence(sequence: str) -> str:

    complement = ""

    for nucleotide in sequence:

        if nucleotide == "A":
            complement += "T"

        elif nucleotide == "T":
            complement += "A"

        elif nucleotide == "C":
            complement += "G"

        elif nucleotide == "G":
            complement += "C"

    return complement


def reverse_complement(sequence: str) -> str:

    complement = complementary_sequence(sequence)

    return complement[::-1]


def transcribe_dna(sequence: str) -> str:

    return sequence.replace("T", "U")

def main():

    print("=== DNA FASTA Generator ===")

    sequence_length = validate_positive_int(
        "Enter sequence length: "
    )

    seq_id = validate_seq_id()

    description = input(
        "Enter sequence description: "
    )

    user_name = input(
        "Enter your name: "
    )

    print("\nDo you want custom nucleotide distribution?")
    print("1 - Yes")
    print("2 - No")

    choice = input("Choose option: ")

    if choice == "1":

        a, c, g, t = validate_distribution()

        dna_sequence = generate_custom_sequence(
            sequence_length,
            a,
            c,
            g,
            t
        )

    else:

        dna_sequence = generate_sequence(
            sequence_length
        )

    sequence_with_name = insert_name(
        dna_sequence,
        user_name
    )

    fasta_content = format_fasta(
        seq_id,
        description,
        sequence_with_name
    )

    filename = f"{seq_id}.fasta"

    save_fasta(
        filename,
        fasta_content
    )

    print(f"\nSequence saved to file: {filename}")

    stats = calculate_stats(
        dna_sequence
    )

    print(f"\nSequence statistics (n={sequence_length}):")

    for nucleotide in "ACGT":
        print(f"{nucleotide}: {stats[nucleotide]:.2f}%")

    print(f"GC-content: {stats['GC']:.2f}%")

    motif = input("\nEnter motif to search: ").upper()

    if motif != "":

        motif_positions = search_motif(
            dna_sequence,
            motif
        )

        if len(motif_positions) > 0:
            print("Motif found at positions:", motif_positions)
        else:
            print("Motif not found.")

    complement = complementary_sequence(
        dna_sequence
    )

    reverse = reverse_complement(
        dna_sequence
    )

    print("\nComplementary strand:")
    print(complement)

    print("\nReverse complementary strand:")
    print(reverse)

    mrna = transcribe_dna(
        dna_sequence
    )

    print("\nmRNA sequence:")
    print(mrna)

    with open(filename, "a") as file:

        file.write("\n")

        file.write(
            format_fasta(
                seq_id + "_COMP",
                "Complementary strand",
                complement
            )
        )

        file.write("\n")

        file.write(
            format_fasta(
                seq_id + "_REVCOMP",
                "Reverse complementary strand",
                reverse
            )
        )

        file.write("\n")

        file.write(
            format_fasta(
                seq_id + "_MRNA",
                "mRNA sequence",
                mrna
            )
        )

    print("\nAdditional FASTA records added successfully.")

if __name__ == "__main__":
    main()