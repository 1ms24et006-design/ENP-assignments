#!/usr/bin/env python3

def verify_acceptance_filter(req_id, acr, amr):
    print("--- CAN Hardware Architecture Selection ---")
    print(
        "Hardware Architecture: Microcontroller -> SPI/Parallel Bus -> SJA1000 CAN Controller -> CAN Transceiver -> CAN Bus")
    print("Controller Mode: FULL CAN (SJA1000 PeliCAN mode) is suitable.")
    print("Reason: System handles 32 identifiers. Full CAN provides a larger 64-byte FIFO and offloads CPU overhead.")

    # Calculate bitwise filtering for top 8 bits
    top8_bits = req_id >> 3
    mask = ~amr & 0xFF
    match = (top8_bits & mask) == (acr & mask)

    print("\n--- Acceptance Filter Verification ---")
    print(f"Required CAN ID: {hex(req_id)}")
    print(f"ACR (Acceptance Code): {hex(acr)}")
    print(f"AMR (Acceptance Mask): {hex(amr)}")
    print(f"ID Top 8 Bits: {hex(top8_bits)}")

    if match:
        print(f"Verdict: MATCH. The CAN hardware will ACCEPT message ID {hex(req_id)}.")
    else:
        print(f"Verdict: NO MATCH. The CAN hardware will REJECT message ID {hex(req_id)}.")
    print("Data Length: 8 bytes is valid (Standard CAN supports up to 8 bytes).")


if __name__ == "__main__":
    verify_acceptance_filter(req_id=0x123, acr=0x24, amr=0x03)