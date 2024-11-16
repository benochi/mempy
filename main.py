import pymem
import pymem.process

def scan_memory(pm, value_to_find, start_address=0x00000000, end_address=0x7FFFFFFF):
    """Scan memory for a specific value and return all matching addresses."""
    addresses = []
    try:
        value_bytes = value_to_find.to_bytes(4, byteorder='little')  # Convert to bytes
        address = start_address

        while address < end_address:
            try:
                region = pymem.memory.virtual_query(pm.process_handle, address)

                if not (region.Protect & 0x04):  # PAGE_READWRITE
                    address += region.RegionSize
                    continue

                data = pm.read_bytes(address, region.RegionSize)
                index = data.find(value_bytes)
                while index != -1:
                    found_address = address + index
                    addresses.append(found_address)
                    index = data.find(value_bytes, index + 1)

                address += region.RegionSize
            except pymem.exception.MemoryReadError:
                address += 0x1000
    except Exception as e:
        print(f"Error scanning memory: {e}")
    return addresses

def find_pointers(pm, target_address, start_address=0x00000000, end_address=0x7FFFFFFF):
    """Search memory for pointers referencing the target address."""
    pointers = []
    target_bytes = target_address.to_bytes(4, byteorder='little')

    address = start_address
    while address < end_address:
        try:
            region = pymem.memory.virtual_query(pm.process_handle, address)

            if not (region.Protect & 0x04):  # PAGE_READWRITE
                address += region.RegionSize
                continue

            data = pm.read_bytes(address, region.RegionSize)
            index = data.find(target_bytes)
            while index != -1:
                found_pointer = address + index
                pointers.append(found_pointer)
                print(f"Pointer to {hex(target_address)} found at: {hex(found_pointer)}")
                index = data.find(target_bytes, index + 1)

            address += region.RegionSize
        except pymem.exception.MemoryReadError:
            address += 0x1000

    return pointers

def main():
    process_name = "Drill Core.exe"  # Replace with your process name
    pm = pymem.Pymem(process_name)
    print(f"Attached to process: {pm.process_id}")

    # Step 1: Scan for the initial value (e.g., 18)
    target_value = 18
    print(f"Scanning for value: {target_value}")
    candidate_addresses = scan_memory(pm, target_value)
    print(f"Found {len(candidate_addresses)} matching addresses.")

    # Step 2: Perform pointer scan for each candidate address
    for addr in candidate_addresses:
        print(f"\nSearching for pointers to: {hex(addr)}")
        pointers = find_pointers(pm, addr)
        if pointers:
            print(f"Pointers for {hex(addr)}:")
            for pointer in pointers:
                print(f"  - {hex(pointer)}")

if __name__ == "__main__":
    main()
