#!/usr/bin/env python3
import math


class Msg:
    def __init__(self, name, cid, dlc, period, crit):
        self.name, self.id, self.dlc, self.p, self.crit = name, cid, dlc, period, crit
        self.deadline = 2.0 if crit else period


msgs = [
    Msg("Airbag", 0x040, 8, 20.0, True),
    Msg("ABS", 0x080, 8, 10.0, True),
    Msg("Engine", 0x180, 8, 10.0, False),
    Msg("Dashboard", 0x300, 8, 50.0, False)
]


def frame_time(dlc, rate_kbit):
    return (47 + 8 * dlc) * 1.2 / (rate_kbit * 1000) * 1000  # returns ms


def main():
    print("=" * 70 + "\nTASK 1 - CAN arbitration\n" + "=" * 70)
    sorted_msgs = sorted(msgs, key=lambda m: m.id)
    print(" Transmission order: " + " -> ".join(f"{m.name} (0x{m.id:03X})" for m in sorted_msgs))

    print("\n" + "=" * 70 + "\nTASKS 2 & 3 - Timing at 500 kbit/s, error-free\n" + "=" * 70)
    ft, t = frame_time(8, 500), 0.0
    for i, m in enumerate(sorted_msgs, 1):
        finish = t + ft
        status = "MEETS (critical)" if m.crit and finish <= m.deadline else "MEETS"
        print(
            f" {i} {m.name:15} (0x{m.id:03X}) Tx: {ft:.1f}us Wait: {t * 1000:.1f}us Finish: {finish * 1000:.1f}us DL: {m.deadline}ms {status}")
        t = finish

    print("\n" + "=" * 70 + "\nTASK 4 - ABS frame corrupted once (Retransmission)\n" + "=" * 70)
    t = 0.0
    for m in sorted_msgs:
        retries = 2 if m.name == "ABS" else 1
        cost = ft + (23 / 500) if retries > 1 else ft  # Includes error frame
        finish = t + cost + (ft if retries > 1 else 0)
        print(f" {m.name:15} finish: {finish * 1000:.1f}us (attempts: {retries})")
        t = finish

    print("\n" + "=" * 70 + "\nTASK 5 - Is a higher bit rate always better?\n" + "=" * 70)
    for r in [125, 250, 500, 1000]:
        max_len = max(0, (0.7 / (r * 1000) - 300e-9) / 10e-9)
        print(
            f" {r:4} kbit/s | Lmax margin: {max_len:4.0f} m | Verdict: {'OK' if r >= 500 else 'Misses worst-case deadline'}")


if __name__ == "__main__":
    main()