
"""
Example: Custom SetLike Protocol Implementation (Infinite Sets)

This example demonstrates the flexibility of eule's `SetLike` protocol by
implementing a "ModuloSet" - a set representing infinite integers based on modular arithmetic.

A ModuloSet represents { x | x % modulus in residues }.
Example: 
  - Evens: modulus=2, residues={0}
  - Multiples of 3: modulus=3, residues={0}

These sets are infinite, yet closed under union, intersection, and difference.
Eule can compute the Euler diagram of these infinite sets!
"""

import math
from typing import Set, List, Iterator

# 1. Define the Custom SetLike Class
class ModuloSet:
    """
    Represents an infinite set of integers defined by modular arithmetic.
    Implements the SetLike protocol required by eule.
    """
    def __init__(self, modulus: int, residues: Set[int]):
        self.modulus = modulus
        # Normalize residues to be within [0, modulus)
        self.residues = {r % modulus for r in residues}
    
    @classmethod
    def from_string(cls, desc: str) -> 'ModuloSet':
        """Helper to create sets like '2n+1'"""
        # Simple parser for demo purposes
        # e.g. "mod 2 is 0" -> Evens
        pass 

    def _unify_bases(self, other: 'ModuloSet'):
        """Convert both sets to a common modulus (LCM)."""
        lcm = (self.modulus * other.modulus) // math.gcd(self.modulus, other.modulus)
        
        # Expand self to LCM
        multiplier_self = lcm // self.modulus
        new_residues_self = set()
        for r in self.residues:
            for k in range(multiplier_self):
                new_residues_self.add(r + k * self.modulus)
                
        # Expand other to LCM
        multiplier_other = lcm // other.modulus
        new_residues_other = set()
        for r in other.residues:
            for k in range(multiplier_other):
                new_residues_other.add(r + k * other.modulus)
                
        return lcm, new_residues_self, new_residues_other

    # --- SetLike Protocol Methods ---

    def union(self, other: 'ModuloSet') -> 'ModuloSet':
        if not isinstance(other, ModuloSet):
            return NotImplemented
        lcm, r1, r2 = self._unify_bases(other)
        return ModuloSet(lcm, r1 | r2)

    def intersection(self, other: 'ModuloSet') -> 'ModuloSet':
        if not isinstance(other, ModuloSet):
            return NotImplemented
        lcm, r1, r2 = self._unify_bases(other)
        return ModuloSet(lcm, r1 & r2)

    def difference(self, other: 'ModuloSet') -> 'ModuloSet':
        if not isinstance(other, ModuloSet):
            return NotImplemented
        lcm, r1, r2 = self._unify_bases(other)
        return ModuloSet(lcm, r1 - r2)

    def __bool__(self) -> bool:
        return bool(self.residues)

    def __iter__(self) -> Iterator[str]:
        """
        Since the set is infinite, we can't yield all integers.
        For eule, we just need to yield something representative or nothing if we don't convert to list.
        
        However, if eule tries to display elements, we should provide a string representation.
        We'll yield a single string description for now.
        """
        # Simplify residues if possible (e.g. all residues -> "Integers")
        if len(self.residues) == self.modulus:
            yield "Integers"
        elif not self.residues:
            return
        else:
            sorted_res = sorted(self.residues)
            yield f"{self.modulus}n + {sorted_res}"

    @classmethod
    def from_iterable(cls, iterable) -> 'ModuloSet':
        # Not used in this specific example flow, but required by protocol
        # Could construct from list of sample integers?
        return ModuloSet(1, set()) 

    def __repr__(self) -> str:
        r_str = ",".join(map(str, sorted(self.residues)))
        return f"{{x | x ≡ {{{r_str}}} (mod {self.modulus})}}"

    def __str__(self) -> str:
        return self.__repr__()
        
# 2. Run Example
from eule import euler

def main():
    print("=" * 60)
    print("♾️  Infinite Set Analysis (Modulo Arithmetic)")
    print("=" * 60)

    # Define sets:
    # A: Multiples of 2 (Evens)
    evens = ModuloSet(2, {0})
    
    # B: Multiples of 3
    threes = ModuloSet(3, {0})
    
    # C: Multiples of 4 (Subset of Evens)
    fours = ModuloSet(4, {0})
    
    # D: Numbers ending in 5 (x ≡ 5 mod 10)
    ends_in_5 = ModuloSet(10, {5})

    sets = {
        'Evens': evens,
        'Threes': threes,
        'Fours': fours,
        'Ends5': ends_in_5
    }

    print("\nDefintions:")
    for k, v in sets.items():
        print(f"  {k:8s}: {v}")
    
    print("\n🔍 Computing Euler Diagram of Infinite Sets...")
    diagram = euler(sets)
    
    print("\n📈 Disjoint Partitions (Residue Classes):")
    for keys, partition in sorted(diagram.items(), key=lambda x: str(x[0])):
        if partition:
            # partition is a ModuloSet
            print(f"\n  Region {keys}:")
            print(f"    {partition}")
            # print(f"    Example: {partition.modulus}n + {sorted(list(partition.residues))[:5]}...")

    print("\nNote: 'Fours' is strictly inside 'Evens'.")
    print("'Ends5' is disjoint from 'Evens' (Odd numbers).")
    print("\n" + "="*60)
    print("✅ Protocol demonstration complete")

if __name__ == "__main__":
    main()
