"""
Greedy Algorithms Assignment
Implement three greedy algorithms for delivery optimization.
"""

import json
import time


# ============================================================================
# PART 1: PACKAGE PRIORITIZATION (Activity Selection)
# ============================================================================

def maximize_deliveries(time_windows):
    """
    Schedule the maximum number of deliveries given time window constraints.
    
    This is the activity selection problem. Each delivery has a start and end time.
    You can only do one delivery at a time. A new delivery can start when the 
    previous one ends.
    
    Args:
        time_windows (list): List of dicts with 'delivery_id', 'start', 'end'
    
    Returns:
        list: List of delivery_ids that can be completed (maximum number possible)
    
    Example:
        time_windows = [
            {'delivery_id': 'A', 'start': 1, 'end': 3},
            {'delivery_id': 'B', 'start': 2, 'end': 5},
            {'delivery_id': 'C', 'start': 4, 'end': 7}
        ]
        maximize_deliveries(time_windows) returns ['A', 'C']
    """
    sorted_deliveries = sorted(time_windows, key=lambda x: x[1])
    
    selected_deliveries = []
    last_end_time = -1
    
    for delivery in sorted_deliveries:
        start, end = delivery
        if start >= last_end_time:
            selected_deliveries.append(delivery)
            last_end_time = end
            
    return selected_deliveries


# ============================================================================
# PART 2: TRUCK LOADING (Fractional Knapsack)
# ============================================================================

def optimize_truck_load(packages, weight_limit):
    """
    Maximize total priority value of packages loaded within weight constraint.
    
    This is the fractional knapsack problem. You can take fractions of packages
    (e.g., deliver part of a package). Goal is to maximize priority value while
    staying within the weight limit.
    
    Args:
        packages (list): List of dicts with 'package_id', 'weight', 'priority'
        weight_limit (int): Maximum weight the truck can carry
    
    Returns:
        dict: {
            'total_priority': float (total priority value loaded),
            'total_weight': float (total weight loaded),
            'packages': list of dicts with 'package_id' and 'fraction' (how much of package taken)
        }
    
    Example:
        packages = [
            {'package_id': 'A', 'weight': 10, 'priority': 60},
            {'package_id': 'B', 'weight': 20, 'priority': 100},
            {'package_id': 'C', 'weight': 30, 'priority': 120}
        ]
        weight_limit = 50
        optimize_truck_load(packages, 50) returns packages A (full), B (full), C (partial)
    """
    packages_with_ratio = []
    for p in packages:
        ratio = p['priority'] / p['weight']
        packages_with_ratio.append((p, ratio))
    
    packages_with_ratio.sort(key=lambda x: x[1], reverse=True)
    
    loaded_packages = []
    total_value = 0
    current_weight = 0
    
    for p, ratio in packages_with_ratio:
        if current_weight >= weight_limit:
            break
        
        space_remaining = weight_limit - current_weight
        
        if p['weight'] <= space_remaining:
            loaded_packages.append((p, 1.0))
            current_weight += p['weight']
            total_value += p['priority']
        else:
            fraction = space_remaining / p['weight']
            loaded_packages.append((p, fraction))
            current_weight += space_remaining
            total_value += p['priority'] * fraction
            break
            
    return loaded_packages, total_value

# ============================================================================
# PART 3: DRIVER ASSIGNMENT (Interval Scheduling)
# ============================================================================

def minimize_drivers(deliveries):
    """
    Assign deliveries to the minimum number of drivers needed.
    
    Each delivery has a start and end time. A driver can do a delivery if it 
    doesn't overlap with their other assigned deliveries. Goal is to use the
    fewest drivers possible.
    
    Args:
        deliveries (list): List of dicts with 'delivery_id', 'start', 'end'
    
    Returns:
        dict: {
            'num_drivers': int (minimum drivers needed),
            'assignments': list of lists (each sublist is one driver's deliveries)
        }
    
    Example:
        deliveries = [
            {'delivery_id': 'A', 'start': 1, 'end': 3},
            {'delivery_id': 'B', 'start': 2, 'end': 4},
            {'delivery_id': 'C', 'start': 5, 'end': 7}
        ]
        minimize_drivers(deliveries) returns 2 drivers: [[A, C], [B]]
    """
    sorted_deliveries = sorted(deliveries, key=lambda x: x[0])
    driver_schedules = [] 
    driver_availability = [] 
    
    for delivery in sorted_deliveries:
        start, end = delivery
        assigned = False
        
        for i in range(len(driver_availability)):
            if driver_availability[i] <= start:
                driver_schedules[i].append(delivery)
                driver_availability[i] = end
                assigned = True
                break
        
        if not assigned:
            driver_schedules.append([delivery])
            driver_availability.append(end)
            
    return driver_schedules


# ============================================================================
# TESTING & BENCHMARKING
# ============================================================================

def load_scenario(filename):
    """Load a scenario from JSON file."""
    with open(f"scenarios/{filename}", "r") as f:
        return json.load(f)


def test_package_prioritization():
    """Test package prioritization with small known cases."""
    print("="*70)
    print("TESTING PACKAGE PRIORITIZATION")
    print("="*70 + "\n")
    
    # Test case 1: Non-overlapping deliveries (should select all)
    test1 = [
        {'delivery_id': 'A', 'start': 1, 'end': 2},
        {'delivery_id': 'B', 'start': 3, 'end': 4},
        {'delivery_id': 'C', 'start': 5, 'end': 6}
    ]
    result1 = maximize_deliveries(test1)
    print(f"Test 1: Non-overlapping")
    print(f"  Expected: 3 deliveries")
    print(f"  Got: {len(result1)} deliveries")
    print(f"  {'✓ PASS' if len(result1) == 3 else '✗ FAIL'}\n")
    
    # Test case 2: All overlapping (should select 1)
    test2 = [
        {'delivery_id': 'A', 'start': 1, 'end': 5},
        {'delivery_id': 'B', 'start': 2, 'end': 4},
        {'delivery_id': 'C', 'start': 3, 'end': 6}
    ]
    result2 = maximize_deliveries(test2)
    print(f"Test 2: All overlapping")
    print(f"  Expected: 1-2 deliveries (depends on greedy choice)")
    print(f"  Got: {len(result2)} deliveries")
    print(f"  Result: {result2}\n")
    
   # Test case 3: Mixed overlapping
    test3 = [
        {'delivery_id': 'A', 'start': 1, 'end': 3},
        {'delivery_id': 'B', 'start': 2, 'end': 5},
        {'delivery_id': 'C', 'start': 4, 'end': 7},
        {'delivery_id': 'D', 'start': 6, 'end': 9}
    ]
    result3 = maximize_deliveries(test3)
    print(f"Test 3: Mixed overlapping")
    print(f"  Expected: 2 deliveries (A ends at 3, C starts at 4)")
    print(f"  Got: {len(result3)} deliveries")
    print(f"  Result: {result3}")
    print(f"  {'✓ PASS' if len(result3) == 2 else '✗ FAIL'}\n")


def test_truck_loading():
    """Test truck loading with small known cases."""
    print("="*70)
    print("TESTING TRUCK LOADING")
    print("="*70 + "\n")
    
    # Test case 1: All packages fit
    packages1 = [
        {'package_id': 'A', 'weight': 10, 'priority': 60},
        {'package_id': 'B', 'weight': 20, 'priority': 100}
    ]
    result1 = optimize_truck_load(packages1, 50)
    print(f"Test 1: All packages fit")
    print(f"  Expected: Total priority = 160, weight = 30")
    print(f"  Got: Priority = {result1['total_priority']}, weight = {result1['total_weight']}")
    print(f"  {'✓ PASS' if result1['total_priority'] == 160 else '✗ FAIL'}\n")
    
    # Test case 2: Fractional required
    packages2 = [
        {'package_id': 'A', 'weight': 10, 'priority': 60},  # ratio = 6.0
        {'package_id': 'B', 'weight': 20, 'priority': 100}, # ratio = 5.0
        {'package_id': 'C', 'weight': 30, 'priority': 120}  # ratio = 4.0
    ]
    result2 = optimize_truck_load(packages2, 50)
    print(f"Test 2: Fractional knapsack")
    print(f"  Expected: Take A (full), B (full), C (partial)")
    print(f"  Expected priority: ~240 (60 + 100 + 80 from 2/3 of C)")
    print(f"  Got: Priority = {result2['total_priority']}, weight = {result2['total_weight']}")
    print(f"  Packages: {result2['packages']}\n")


def test_driver_assignment():
    """Test driver assignment with small known cases."""
    print("="*70)
    print("TESTING DRIVER ASSIGNMENT")
    print("="*70 + "\n")
    
    # Test case 1: All non-overlapping (need 1 driver)
    deliveries1 = [
        {'delivery_id': 'A', 'start': 1, 'end': 2},
        {'delivery_id': 'B', 'start': 3, 'end': 4},
        {'delivery_id': 'C', 'start': 5, 'end': 6}
    ]
    result1 = minimize_drivers(deliveries1)
    print(f"Test 1: Non-overlapping")
    print(f"  Expected: 1 driver")
    print(f"  Got: {result1['num_drivers']} drivers")
    print(f"  {'✓ PASS' if result1['num_drivers'] == 1 else '✗ FAIL'}\n")
    
    # Test case 2: All overlapping (need 3 drivers)
    deliveries2 = [
        {'delivery_id': 'A', 'start': 1, 'end': 5},
        {'delivery_id': 'B', 'start': 2, 'end': 6},
        {'delivery_id': 'C', 'start': 3, 'end': 7}
    ]
    result2 = minimize_drivers(deliveries2)
    print(f"Test 2: All overlapping")
    print(f"  Expected: 3 drivers")
    print(f"  Got: {result2['num_drivers']} drivers")
    print(f"  {'✓ PASS' if result2['num_drivers'] == 3 else '✗ FAIL'}\n")
    
    # Test case 3: Mixed
    deliveries3 = [
        {'delivery_id': 'A', 'start': 1, 'end': 3},
        {'delivery_id': 'B', 'start': 2, 'end': 4},
        {'delivery_id': 'C', 'start': 4, 'end': 6},
        {'delivery_id': 'D', 'start': 5, 'end': 7}
    ]
    result3 = minimize_drivers(deliveries3)
    print(f"Test 3: Mixed overlapping")
    print(f"  Expected: 2 drivers")
    print(f"  Got: {result3['num_drivers']} drivers")
    print(f"  Assignments: {result3['assignments']}")
    print(f"  {'✓ PASS' if result3['num_drivers'] == 2 else '✗ FAIL'}\n")


def benchmark_scenarios():
    """Benchmark all algorithms on realistic scenarios."""
    print("\n" + "="*70)
    print("BENCHMARKING ON REALISTIC SCENARIOS")
    print("="*70 + "\n")
    
    # Benchmark package prioritization
    print("Scenario 1: Package Prioritization (50 deliveries)")
    print("-" * 70)
    data = load_scenario("package_prioritization.json")
    
    start = time.perf_counter()
    result = maximize_deliveries(data)
    elapsed = time.perf_counter() - start
    
    print(f"  Deliveries scheduled: {len(result)} out of {len(data)}")
    print(f"  Runtime: {elapsed*1000:.4f} ms\n")
    
    # Benchmark truck loading
    print("Scenario 2: Truck Loading (100 packages, 500 lb limit)")
    print("-" * 70)
    data = load_scenario("truck_loading.json")
    
    start = time.perf_counter()
    result = optimize_truck_load(data['packages'], data['truck_capacity'])
    elapsed = time.perf_counter() - start
    
    print(f"  Total priority loaded: {result['total_priority']:.2f}")
    print(f"  Total weight loaded: {result['total_weight']:.2f} lbs")
    print(f"  Packages used: {len(result['packages'])}")
    print(f"  Runtime: {elapsed*1000:.4f} ms\n")
    
    # Benchmark driver assignment
    print("Scenario 3: Driver Assignment (60 deliveries)")
    print("-" * 70)
    data = load_scenario("driver_assignment.json")
    
    start = time.perf_counter()
    result = minimize_drivers(data)
    elapsed = time.perf_counter() - start
    
    print(f"  Drivers needed: {result['num_drivers']}")
    print(f"  Runtime: {elapsed*1000:.4f} ms\n")


if __name__ == "__main__":
    print("GREEDY ALGORITHMS ASSIGNMENT - STARTER CODE")
    print("Implement the greedy functions above, then run tests.\n")
    
    # Uncomment these as you complete each part:
    
    # test_package_prioritization()
    # test_truck_loading()
    # test_driver_assignment()
    # benchmark_scenarios()
    
    print("\n⚠ Uncomment the test functions in the main block to run tests!")