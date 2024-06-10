#!/usr/bin/env python3

def parse_gpu_data(file_path):
    """
    Parse GPU data from a file. Each line should be:
    GPU Name,FLOP (TFLOPS),Bandwidth (GB/s),VRAM (GB)
    Lines starting with '#' are comments and are ignored.
    """
    gpus = []
    seen = set()  # To keep track of unique GPUs

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Skip empty lines and comments

            parts = line.split(",")
            if len(parts) != 4:
                print(f"Warning: Line {line_number}: Invalid data format, skipping.")
                continue

            name, flop, bandwidth, vram = parts
            
            # Check for duplicates
            if name in seen:
                print(f"Warning: Line {line_number}: Duplicate GPU '{name}', skipping.")
                continue
            seen.add(name)

            try:
                gpus.append({
                    "name": name,
                    "flop": float(flop),
                    "bandwidth": float(bandwidth),
                    "vram": float(vram)
                })
            except ValueError:
                print(f"Warning: Line {line_number}: Invalid numeric value, skipping.")

    return gpus

def rank_gpus(gpus):
    """
    Rank GPUs by FLOP (primary), bandwidth (secondary), and VRAM (tertiary).
    """
    return sorted(gpus, key=lambda x: (-x["flop"], -x["bandwidth"], -x["vram"]))

def generate_gpu_table(gpus):
    """
    Generate a Markdown table of ranked GPUs with explanations.
    """
    table = "# NVIDIA GPU Performance Comparison\n\n"
    table += "| Rank  | Model | &nbsp;FP32 RPeak&nbsp;<br>(TFlops) | &nbsp;Mem Bdw&nbsp;<br>(GB/s) | &nbsp;VRam&nbsp;<br>(GB) | &nbsp;GFlops/bdw&nbsp; |\n"
    table += "|:---:|:---:|:---:|:---:|:---:|:---:|\n"

    for rank, gpu in enumerate(gpus, 1):
        flop_bw_ratio = gpu["flop"] / gpu["bandwidth"]*1000
        table += f"| {rank} | {gpu['name']} | {gpu['flop']:.2f} | {gpu['bandwidth']:.0f} | {gpu['vram']:.0f} | {flop_bw_ratio:.2f} |\n"

    table += "\n## Understanding the Metrics\n\n"
    table += "- **Rank**: GPUs are ranked primarily by FP32 FLOP, then by bandwidth, and finally by VRam.\n"
    table += "- **FP32 FLOP (TFLOPS)**: Single precision floating-point operations per second in teraflops.\n"
    table += "- **Bandwidth (GB/s)**: Memory bandwidth in GB/s.\n"
    table += "- **VRam (GB)**: GPU memory in GB.\n"
    table += "- **GFLOP/BW**: GFLOP per unit of bandwidth. Lower is better. \n"

    return table

def main():
    gpus = parse_gpu_data("data.txt")
    ranked_gpus = rank_gpus(gpus)
    table = generate_gpu_table(ranked_gpus)
    
    print(table)
    
    # Optionally, write to a file
    with open("gpu_table.md", "w") as f:
        f.write(table)
    print("\nTable saved to gpu_table.md")

if __name__ == "__main__":
    main()
