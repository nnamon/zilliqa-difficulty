#!/usr/bin/env python


class DifficultySimulator:

    def __init__(self, global_hashrate, starting_diff, deviation=100, target=1810, guards=1200,
            pow_window=60, node_cap=None):
        """Create the DifficultySimulator object.

        Attributes:
            global_hashrate (int): the global hashrate in (H/s) to be used in the simulation.
            starting_diff (int): the starting difficulty.
            deviation (int): the number of nodes above or below the target to increment or decrement
                the difficulty by 1.
            target (int): the target number of nodes to reach.
            guards (int): the number of guard nodes.
            pow_window (int): the length of a proof-of-work window.
            node_cap (int): the maximum number of nodes running.
            current_n (int): the current iteration number of the simulation.
            current_diff (int): the current difficulty of the simulation.
        """

        # Parameters
        self.global_hashrate = global_hashrate
        self.starting_diff = starting_diff
        self.deviation = deviation
        self.target = target
        self.guards = guards
        self.pow_window = pow_window
        self.node_cap = node_cap

        # State
        self.set_state(0, self.starting_diff)


    def to_boundary(self, diff):
        """Converts a numerical difficulty to a boundary value.

        Args:
            diff (int): the Zilliqa difficulty (number of prefixed zeros).

        Returns:
            int: the target boundary to compare the solution to.
        """
        b = ["1"] * 256
        for i in range(int(diff)):
            b[i] = "0"
        return int("".join(b), 2)


    def to_hashes(self, diff):
        """Converts a numerical difficulty to the absolute expected number of hashes required.

        Args:
            diff (int): the Zilliqa difficulty (number of prefixed zeros).

        Returns:
            int: the absolute expected number of hashes required.
        """
        boundary = self.to_boundary(diff)
        result = pow(2, 256) / float(boundary)
        return result


    def to_hashrate(self, diff):
        """Converts a numerical difficulty to the hashrate (H/s) required to obtain a solution
        within the proof-of-work window.

        Args:
            diff (int): the Zilliqa difficulty (number of prefixed zeros).

        Returns:
            int: the hashrate (H/s) required to obtain a solution within the proof-of-work window.
        """
        return self.to_hashes(diff)/self.pow_window


    def set_state(self, current_n, current_diff):
        """Sets the current state of the simulation.

        Args:
            current_n (int): the current iteration number of the simulation.
            current_diff (int): the current difficulty of the simulation.
        """
        self.current_n = current_n
        self.current_diff = current_diff


    def set_global_hashrate(self, hashrate):
        """Sets the global hashrate of the simulation.

        Args:
            hashrate (int): the new global hashrate (H/s) to set.
        """
        self.global_hashrate = hashrate


    def step(self):
        """Advances the simulation by one DS epoch.

        Returns:
            (int, int, int, int): (the current n, the number of expected solutions submitted, the
                new difficulty, the difficulty adjustment)
        """
        expected_solutions = (self.global_hashrate/self.to_hashrate(self.current_diff))
        expected_solutions += self.guards
        if self.node_cap is not None:
            expected_solutions = min(expected_solutions, self.node_cap)
        difference = expected_solutions - self.target
        difficulty_adjustment = difference/self.deviation
        self.current_diff += difficulty_adjustment
        self.current_n += 1

        result = (self.current_n, expected_solutions, self.current_diff, difficulty_adjustment)
        return result


    def abbrev_hashrate(self, rate):
        quantifiers = (("Th", 1000000000000.0), ("Gh", 1000000000.0), ("Mh", 1000000.0),
                ("Kh", 1000.0))
        for quant, divisor in quantifiers:
            divided = rate/divisor
            if divided > 1:
                return "%.f %s" % (divided, quant)
        return "%d H" % rate


def show_required_global_hashrate_by_diff():
    """Display a table of required global hashrate.
    """
    simulator = DifficultySimulator(0, 0)

    print("Global hashrate required to maintain %d nodes:" % simulator.target)
    for i in range(50):
        hashrate_required_per_node = simulator.to_hashrate(i)
        hashrate_required_global = hashrate_required_per_node * (simulator.target - simulator.guards)
        hashrate_str = simulator.abbrev_hashrate(hashrate_required_global)
        print("Diff %02d = %10s/s" % (i, hashrate_str))

    print "--------------------------------------------------------\n\n"


def simulate_for_n(starting_diff, n, global_hashrate, node_cap, deviation=100):
    """Simulate the difficulty for n epochs with given starting difficulty, global hashrate, and the
    maximum number of nodes run.

    Args:
        starting_diff (int): the starting difficulty.
        n (int): the number of iterations to simulate.
        global_hashrate (int): the hashrate (H/s) to simulate.
    """
    simulator = DifficultySimulator(global_hashrate, starting_diff, node_cap=node_cap,
            deviation=deviation)
    print("Simulating for %d epochs:" % n)
    print("Starting Difficulty: %d" % starting_diff)
    print("Global Hashrate: %s/s" % simulator.abbrev_hashrate(global_hashrate))

    for i in range(n):
        iteration = simulator.step()
        print("n=%02d  solutions=%d  difficulty=%d  adjustment=%d" % iteration)

    print "--------------------------------------------------------\n\n"


def main():
    # Display the minimum required global hashrate to maintain a difficulty.
    show_required_global_hashrate_by_diff()

    # Simulate the difficulty adjustment diff=32, n=50, hashrate=58 Gh/s, node_cap=2100
    # Approximately in between difficulty 32 and 33.
    simulate_for_n(32, 50, 58 * 1000000000.0, 2100)

    # Simulate the difficulty adjustment diff=40, n=50, hashrate=15 Th/s, node_cap=2100
    # Approximately in between difficulty 40 and 41.
    simulate_for_n(40, 50, 15 * 1000000000000.0, 2100)

    # Simulate the difficulty adjustment diff=40, n=50, hashrate=15 Th/s, node_cap=2100 with a
    # higher deviation
    simulate_for_n(40, 50, 15 * 1000000000000.0, 2100, 200)

    # Simulate the difficulty adjustment diff=40, n=50, hashrate=15 Th/s, node_cap=4000 with a
    # higher deviation and higher max node cap
    simulate_for_n(40, 50, 15 * 1000000000000.0, 4000, 200)

    # Simulate the difficulty adjustment diff=40, n=50, hashrate=15 Th/s, node_cap=2100 with a
    # higher deviation and higher max node cap and a large hashrate.
    simulate_for_n(40, 50, 50 * 1000000000000.0, 4000, 200)


if __name__ == '__main__':
    main()
