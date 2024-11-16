import pymem
import pymem.process

def scan_memory(pm, value_to_find, start_address=0x00000000, end_address=0x7FFFFFFF):
    """Scan memory for a specific value."""
    try:
        if isinstance(value_to_find, str):
            value_bytes = value_to_find.encode('utf-8')  # Convert string to bytes
        else:
            value_bytes = value_to_find.to_bytes(4, byteorder='little')  # Integer to bytes

        address = start_address

        while address < end_address:
            try:
                # Query memory region information
                region = pymem.memory.virtual_query(pm.process_handle, address)

                # Skip inaccessible or protected regions
                if not (region.Protect & 0x04):  # PAGE_READWRITE
                    address += region.RegionSize
                    continue

                # Read the memory region
                data = pm.read_bytes(address, region.RegionSize)

                # Search for the value
                index = data.find(value_bytes)
                while index != -1:
                    found_address = address + index
                    print(f"Value found at: {hex(found_address)}")
                    index = data.find(value_bytes, index + 1)

                address += region.RegionSize  # Move to next region
            except pymem.exception.MemoryReadError:
                address += 0x1000  # Skip unreadable section
    except Exception as e:
        print(f"Error scanning memory: {e}")

def main():
    process_name = "Drill Core.exe"  # Replace with your process name
    pm = pymem.Pymem(process_name)
    print(f"Attached to process: {pm.process_id}")

    # Example: Scan for the string "recycle"
    scan_memory(pm, "recycle")

if __name__ == "__main__":
    main()
