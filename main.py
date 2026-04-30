import random

def generate_sequence(length: int) -> str:
    return "".join(random.choice("ACGT") for _ in range(length))

def generate_sequence_with_distribution(length: int, distribution: dict) -> str:
    nucleotides = list(distribution.keys())
    weights = list(distribution.values())
    return "".join(random.choices(nucleotides, weights=weights, k=length))

def calculate_stats(sequence: str) -> dict:
    length = len(sequence)

    stats = {
        "A": sequence.count("A") / length * 100,
        "C": sequence.count("C") / length * 100,
        "G": sequence.count("G") / length * 100,
        "T": sequence.count("T") / length * 100,
    }

    stats["GC"] = stats["G"] + stats["C"]
    return stats

def insert_name(sequence: str, name: str) -> str:
    position = random.randint(0, len(sequence))
    return sequence[:position] + name.lower() + sequence[position:]

def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    header = f">{seq_id} {description}".rstrip()
    lines = [sequence[i:i + line_width] for i in range(0, len(sequence), line_width)]
    return header + "\n" + "\n".join(lines)

def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    while True:
        value = input(prompt)

        try:
            number = int(value)

            if min_val <= number <= max_val:
                return number

        except ValueError:
            pass

        print(f"Error: value must be an integer in the range [{min_val}, {max_val}].")

def validate_sequence_id(prompt: str) -> str:
    while True:
        seq_id = input(prompt)

        if seq_id and not any(char.isspace() for char in seq_id):
            return seq_id

        print("Error: sequence ID cannot be empty or contain whitespace.")

def get_distribution() -> dict:
    use_custom = input("Use custom nucleotide distribution? (yes/no): ").lower()

    if use_custom != "yes":
        return {"A": 25, "C": 25, "G": 25, "T": 25}

    while True:
        distribution = {}

        for nucleotide in "ACGT":
            distribution[nucleotide] = validate_positive_int(
                f"Enter percentage for {nucleotide}: ",
                min_val=0,
                max_val=100
            )

        if sum(distribution.values()) == 100:
            return distribution

        print("Error: percentages must sum to 100.")

def find_motif(sequence: str, motif: str) -> list:
    positions = []
    start = 0

    while True:
        index = sequence.find(motif, start)

        if index == -1:
            break

        positions.append(index + 1)
        start = index + 1

    return positions

def get_complement(sequence: str) -> str:
    table = str.maketrans("ACGT", "TGCA")
    return sequence.translate(table)


def get_reverse_complement(sequence: str) -> str:
    return get_complement(sequence)[::-1]


def save_single_fasta(seq_id: str, description: str, sequence: str, name: str) -> None:
    sequence_with_name = insert_name(sequence, name)

    complement = get_complement(sequence)
    reverse_complement = get_reverse_complement(sequence)

    fasta_records = [
        format_fasta(seq_id, description, sequence_with_name),
        format_fasta(seq_id + "_complement", "Complementary sequence", complement),
        format_fasta(seq_id + "_reverse_complement", "Reverse complementary sequence", reverse_complement)
    ]

    filename = f"{seq_id}.fasta"

    with open(filename, "w") as file:
        file.write("\n".join(fasta_records))

    print(f"\nSequence saved to file: {filename}")

def save_batch_fasta(base_id: str, description: str, sequences: list, name: str) -> None:
    filename = f"{base_id}_batch.fasta"
    records = []

    for index, sequence in enumerate(sequences, start=1):
        seq_id = f"{base_id}_{index:03d}"
        sequence_with_name = insert_name(sequence, name)

        records.append(format_fasta(seq_id, description, sequence_with_name))
        records.append(format_fasta(seq_id + "_complement", "Complementary sequence", get_complement(sequence)))
        records.append(format_fasta(seq_id + "_reverse_complement", "Reverse complementary sequence", get_reverse_complement(sequence)))

    with open(filename, "w") as file:
        file.write("\n".join(records))

    print(f"\nSequences saved to file: {filename}")

def print_statistics(sequence: str) -> None:
    stats = calculate_stats(sequence)

    print(f"\nSequence statistics (n={len(sequence)}):")
    print(f"A: {stats['A']:.2f}%")
    print(f"C: {stats['C']:.2f}%")
    print(f"G: {stats['G']:.2f}%")
    print(f"T: {stats['T']:.2f}%")
    print(f"GC-content : {stats['GC']:.2f}%")

def main():
    length = validate_positive_int("Enter sequence length: ")

    seq_id = validate_sequence_id("Enter sequence ID: ")
    description = input("Enter a description of the sequence: ")
    name = input("Enter your name: ")

    batch_count = validate_positive_int(
        "Enter number of sequences to generate: ",
        min_val=1,
        max_val=1000
    )

    distribution = get_distribution()

    sequences = []

    for _ in range(batch_count):
        sequence = generate_sequence_with_distribution(length, distribution)
        sequences.append(sequence)

    if batch_count == 1:
        save_single_fasta(seq_id, description, sequences[0], name)
    else:
        save_batch_fasta(seq_id, description, sequences, name)

    print_statistics(sequences[0])

    motif = input("\nEnter motif to search for, or press Enter to skip: ").upper()

    if motif:
        positions = find_motif(sequences[0], motif)

        if positions:
            print(f"Motif {motif} found at positions: {positions}")
        else:
            print(f"Motif {motif} was not found.")


if __name__ == "__main__":
    main()