class AIChipPowerAnalysis:
    """
    Analyze power consumption and thermal requirements for AI hardware.
    """

    def __init__(self, name, process_node_nm, frequency_ghz):
        self.name = name
        self.process_node = process_node_nm
        self.frequency = frequency_ghz

    def calculate_dynamic_power(self, num_operations, capacitance_pf, voltage):
        """
        Dynamic power = α * C * V² * f

        Args:
            num_operations: Operations per second
            capacitance_pf: Capacitance in picofarads
            voltage: Supply voltage
        """
        alpha = 0.5  # Activity factor (50% of circuits switching)
        C = capacitance_pf * 1e-12  # Convert to farads

        power = alpha * C * (voltage ** 2) * self.frequency * 1e9
        total_power = power * num_operations

        return total_power

    def analyze_ai_chip(self):
        """Full analysis of AI chip power and thermal."""

        print(f"\n{'='*70}")
        print(f"POWER ANALYSIS: {self.name}")
        print(f"{'='*70}")

        # Example: Small AI accelerator
        specs = {
            'mac_units': 128,  # Multiply-accumulate units
            'frequency': self.frequency,
            'voltage': 1.0,  # Volts
            'capacitance_per_mac': 10,  # pF
        }

        print(f"\nSpecifications:")
        print(f"  Process: {self.process_node}nm")
        print(f"  MAC Units: {specs['mac_units']}")
        print(f"  Frequency: {specs['frequency']} GHz")
        print(f"  Voltage: {specs['voltage']} V")

        # Calculate power
        power_per_mac = self.calculate_dynamic_power(
            1,
            specs['capacitance_per_mac'],
            specs['voltage']
        )

        total_power = power_per_mac * specs['mac_units']

        print(f"\nPower Analysis:")
        print(f"  Power per MAC unit: {power_per_mac*1000:.2f} mW")
        print(f"  Total dynamic power: {total_power:.2f} W")

        # Add static power (leakage)
        static_power = total_power * 0.3  # ~30% of dynamic
        total_chip_power = total_power + static_power

        print(f"  Static power (leakage): {static_power:.2f} W")
        print(f"  Total chip power: {total_chip_power:.2f} W")

        # Thermal analysis
        print(f"\nThermal Analysis:")

        # Typical cooling solutions
        cooling_solutions = [
            ("Passive heatsink", 10, 25, 100),  # θ, T_ambient, T_max
            ("Active cooling (fan)", 5, 25, 100),
            ("Liquid cooling", 1, 25, 100),
        ]

        for name, theta, t_amb, t_max in cooling_solutions:
            temp_rise = total_chip_power * theta
            chip_temp = t_amb + temp_rise

            margin = t_max - chip_temp

            status = "✓ OK" if chip_temp < t_max else "✗ OVERTEMP"
            print(f"  {name}:")
            print(f"    θ = {theta}°C/W")
            print(f"    Chip temp: {chip_temp:.1f}°C")
            print(f"    Margin: {margin:.1f}°C {status}")

        # Performance analysis
        print(f"\nPerformance:")
        ops_per_mac = specs['frequency'] * 1e9  # Operations/sec per MAC
        total_ops = ops_per_mac * specs['mac_units']

        print(f"  MACs/second: {total_ops/1e9:.1f} GMAC/s")
        print(f"  Operations/second: {total_ops/1e9:.1f} GFLOPS (approx)")

        # Efficiency
        efficiency = total_ops / (total_chip_power * 1e9)  # Ops/Watt
        print(f"  Power efficiency: {efficiency:.2f} GOPS/W")

        return total_chip_power, total_ops

# Compare different AI hardware architectures
def compare_ai_hardware():
    """Compare power/performance of different AI architectures."""

    print("\n" + "="*70)
    print("AI HARDWARE COMPARISON")
    print("="*70)

    architectures = [
        AIChipPowerAnalysis("Mobile AI Accelerator", 5, 1.0),
        AIChipPowerAnalysis("Desktop GPU", 7, 2.0),
        AIChipPowerAnalysis("Data Center TPU", 7, 1.5),
    ]

    results = []
    for arch in architectures:
        power, ops = arch.analyze_ai_chip()
        results.append((arch.name, power, ops, ops/power))

    print("\n" + "="*70)
    print("SUMMARY COMPARISON")
    print("="*70)
    print(f"{'Architecture':<25} {'Power (W)':<12} {'GOPS':<12} {'GOPS/W':<12}")
    print("-"*70)

    for name, power, ops, efficiency in results:
        print(f"{name:<25} {power:<12.1f} {ops/1e9:<12.1f} {efficiency:<12.2f}")

    print("\n" + "="*70)
    print("KEY INSIGHTS:")
    print("-"*70)
    print("1. Mobile chips prioritize efficiency (GOPS/W)")
    print("2. Desktop GPUs balance power and performance")
    print("3. Data center chips maximize throughput")
    print("4. Thermal management is critical for all")
    print("5. Process node affects both power and performance")

if __name__ == "__main__":
    compare_ai_hardware()
