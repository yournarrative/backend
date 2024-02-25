
duration_hours = 1
duration_seconds = duration_hours * 3600

# Bitrates to test (in Mbps)
bitrates = [0.5, 1, 2, 4, 8]  # Example: 0.5 Mbps, 1 Mbps, 2 Mbps, 4 Mbps, 8 Mbps

# Resolution and frame rate
resolution = (320, 180)  # Full HD
frame_rate = 30  # fps

# Calculate file sizes for each bitrate
for bitrate in bitrates:
    # Calculate bitrate in kilobits per second (kbps)
    bitrate_kbps = bitrate * 1000

    # Calculate file size in bytes
    file_size_bytes = (bitrate_kbps * duration_seconds) / 8

    # Convert file size to megabytes (MB)
    file_size_MB = file_size_bytes / (1024 * 1024)

    print(f"At {bitrate} Mbps: Estimated file size is approximately {file_size_MB:.2f} MB")
