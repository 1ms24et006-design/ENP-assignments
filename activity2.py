#!/usr/bin/env python3

class Node:
    def __init__(self, name, cid, deadline, crit):
        self.name, self.id, self.dl, self.crit = name, cid, deadline, crit

veh_network = [
    Node("Steering cmd", 0x040, 5.0, True),
    Node("Brake cmd", 0x010, 5.0, True),
    Node("Wheel-speed", 0x050, 10.0, True),
    Node("Battery stat", 0x100, 100.0, False),
    Node("Infotainment", 0x200, 100.0, False)
]

def can_ft(): return 0.266  # ms at 500kbit/s
def fr_ft(): return 0.027   # ms at 5Mbit/s

def main():
    print("="*70 + "\nTASK 1 - Transmission time of one 8-byte frame\n" + "="*70)
    print(f" CAN @ 500 kbit/s: {can_ft():.3f} ms")
    print(f" FlexRay @ 5 Mbit/s: {fr_ft():.3f} ms (10x faster)")

    print("\n" + "="*70 + "\nTASK 2 - Busy CAN bus vs FlexRay Latency (ADAS Burst)\n" + "="*70)
    print(" ADAS frames | CAN steering | FlexRay steering")
    for adas_count in [0, 4, 8, 12, 15, 20]:
        # Latency approximation: ADAS frames + higher priority + own frame
        can_lat = (adas_count + 3) * can_ft()
        status = "MEETS" if can_lat <= 5.0 else "MISSES"
        print(f" {adas_count:>10}  | {can_lat:6.3f} ms {status:6} | {fr_ft():.3f} ms (always)")

    print("\n" + "="*70 + "\nTASK 6 - Hybrid architecture Recommendation\n" + "="*70)
    for n in veh_network:
        net = "FlexRay" if n.crit and n.dl <= 10.0 else "CAN Bus"
        reason = "Guaranteed slot needed" if net == "FlexRay" else "Relaxed / Event-driven"
        print(f" {n.name:15} -> {net:7} ({reason})")

    print("\n" + "="*70 + "\nQ3 - Fallback when a communication channel is lost\n" + "="*70)
    print(" Normal       : Steering & Brake on FlexRay A AND B (0.027 ms latency)")
    print(" Lose A       : B still delivers them, same latency (0.027 ms)")
    print(" Lose FlexRay : Fallback to CAN on reserved top IDs. Safe-stop mode initiated.")

if __name__ == "__main__":
    main()