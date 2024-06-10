#!/usr/bin/env python3
import datetime
import os


def parse_gpu_data(file_path):
    """
    Parse GPU data from a file. Each line should be:
    GPU Name,Flop (TFlopS),Bandwidth (GB/s),TDP (W)
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

            name, flop, bandwidth, tdp = parts
            
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
                    "tdp": float(tdp),
                    "flop_per_watt": float(flop) / float(tdp),
                    "flop_per_bandwidth": float(flop) / float(bandwidth)*1000
                })
            except ValueError:
                print(f"Warning: Line {line_number}: Invalid numeric value, skipping.")

    return gpus

def rank_gpus(gpus):
    """
    Rank GPUs by Flop (primary), bandwidth (secondary), inverse TDP (tertiary).
    """
    return sorted(gpus, key=lambda x: (-x["flop"], -x["bandwidth"], 1/x["tdp"]))

def generate_gpu_table(gpus):
    """
    Generate a Markdown table of ranked GPUs with explanations.
    """

    today_date = datetime.datetime.now().strftime("%B %d, %Y")

    table = "### NVIDIA GPU Performance and Efficiency Comparison\n\n"
    table += f"**Last Updated**: `{today_date}`\n\n" 
    table += "||\n"
    table += "|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|\n"
    

    header1 = "|**Rank**|"
    header1 +="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Model**|"
    header1 +="**&nbsp;FP32 RPeak&nbsp;<br>(TFlops)**|"
    header1 += "**&nbsp;Mem Bdw&nbsp;<br>(GB/s)**|**&nbsp;TDP&nbsp;<br>(W)**|"
    header1 += "**&nbsp;TFlop/Watt&nbsp;**|**&nbsp;Flops/Bdw&nbsp;**|\n"
#    header1 += "|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|\n"

    table += header1

    header2 = "|**Rank**|"
    header2 +="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Model**|"
    header2 += "**&nbsp;FP32 RPeak&nbsp;**|"
    header2 += "**&nbsp;Mem Bdw&nbsp;**|**&nbsp;TDP&nbsp;**|"
    header2 += "**&nbsp;TFlop/Watt&nbsp;**|**&nbsp;Flops/Bdw&nbsp;**|\n"

    for rank, gpu in enumerate(gpus, 1):
        if rank % 10 == 1 and rank != 1: 
            table += header2
        table += f"| {rank} | {gpu['name']} | {gpu['flop']:.2f} | {gpu['bandwidth']:.0f}  | {gpu['tdp']:.0f} | {gpu['flop_per_watt']:.2f} | {gpu['flop_per_bandwidth']:.2f} |\n"

    table += "||\n\n### Understanding the Metrics\n\n"
    table += "- **Rank**: GPUs are ranked primarily by FP32 Flop, then by bandwidth, and finally by inverse of TDP.\n"
    table += "- **FP32 TFlops**: Single precision floating-point operations per second in teraflops.\n"
    table += "- **Bandwidth (GB/s)**: Memory bandwidth in GB/s.\n"
    table += "- **TDP (W)**: Thermal Design Power in watts.\n"
    table += "- **Flop/W**: TFlop per watt. Higher is better.\n"
    table += "- **Flop/Bdw**: Flop per unit of bandwidth. Lower is better\n"

    return table



def link_file(file):

    today_date = datetime.datetime.now().strftime("%Y-%m-%d")

    source_file = f'{file}.md'
    link_file = f'{today_date}-{file}.md'
    
    # Remove all existing symbolic links in the current directory
    for item in os.listdir('.'):
        if os.path.islink(item):
            os.unlink(item)
            print(f"Removed symbolic link: {item}")

    # Create the symbolic link
    try:
        os.symlink(source_file, link_file)
        print(f"Symbolic link created successfully: {link_file} -> {source_file}")
    except Exception as e:
        print(f"Failed to create symbolic link: {e}")


def main():
    gpus = parse_gpu_data("data.txt")
    ranked_gpus = rank_gpus(gpus)
    table = generate_gpu_table(ranked_gpus)
    link_file('gpu-ranking')
    
    # Write the table to the same directory as the blog post
    with open("gpu_table.md", "w") as f:
        f.write(table)
    print("\nTable saved to gpu_table.md")

if __name__ == "__main__":
    main()
