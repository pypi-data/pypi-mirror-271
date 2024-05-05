# -*- coding: utf-8 -*-
"""Functions for calculating the number of gates in a MAC circuit."""

import math

__all__ = ["GateCount"]


class GateCount:
    """Gate count for various circuit components."""

    @staticmethod
    def NOT() -> int:
        """Inverter."""
        return 0

    @staticmethod
    def NAND() -> int:
        """NAND gate."""
        return 1

    @staticmethod
    def AND() -> int:
        """AND gate."""
        return 1

    @staticmethod
    def NOR() -> int:
        """NOR gate."""
        return 1

    @staticmethod
    def OR() -> int:
        """OR gate."""
        return 1

    @staticmethod
    def AOI21() -> int:
        """AND-OR-INVERT gate with 2 AND gates and 1 OR gate."""
        return 2

    @staticmethod
    def OAI21() -> int:
        """OR-AND-INVERT gate with 2 OR gates and 1 AND gate."""
        return 2

    @staticmethod
    def XOR() -> int:
        """Exclusive-OR gate."""
        return 3

    @staticmethod
    def XNOR() -> int:
        """Exclusive-NOR gate."""
        return 3

    @staticmethod
    def HA() -> int:  # Half Adder
        """Half Adder."""
        return 3

    @staticmethod
    def FA() -> int:  # Full Adder
        """Full Adder."""
        return 2 * GateCount.HA() + GateCount.OR()

    @staticmethod
    def FF() -> int:  # Flip-Flop
        """Flip-Flop."""
        return 2 * GateCount.Mux2()

    @staticmethod
    def Mux2(n: int = 1) -> int:
        """2-to-1 multiplexer."""
        return 3 * n

    @staticmethod
    def Mux4(n: int = 1) -> int:
        """4-to-1 multiplexer."""
        return 3 * GateCount.Mux2(n)

    @staticmethod
    def Reg(n: int) -> int:
        """Register."""
        return n * GateCount.FF()

    @staticmethod
    def Add(n: int) -> int:
        """Adder."""
        return (n - 1) * GateCount.FA() + GateCount.HA()

    @staticmethod
    def Inc(n: int) -> int:
        """Incrementer."""
        return n * GateCount.HA()

    @staticmethod
    def Mult(n: int, m: int = None) -> int:
        """Integer multiplier.

        Args:
            n (int): Number of bits in the multiplier.
            m (int, optional): Number of bits in the other multiplicand. Defaults to ``None``.
        """
        if m is None:
            m = n
        partial_products = n * m * GateCount.AND()
        partial_product_reduction = (m - 1) * GateCount.Add(n)
        return partial_products + partial_product_reduction

    @staticmethod
    def LeftShift(n: int, k: int, extend=False) -> int:
        """Left shifter.

        Args:
            n (int): Number of bits in the input.
            k (int): Number of bits to shift.
            extend (bool, optional): Whether to extend the input. Defaults to ``False``.
        """
        logk = int(math.log2(k))
        if extend:
            return (n - 2) * GateCount.Mux2(logk) + k * (GateCount.Mux2() + GateCount.AND())
        else:
            return n * GateCount.Mux2(logk) - k * (GateCount.Mux2() - GateCount.AND())

    @staticmethod
    def RightShift(n: int, k: int) -> int:
        """Right shifter.

        Args:
            n (int): Number of bits in the input.
            k (int): Number of bits to shift.
        """
        logk = int(math.log2(k))
        return (n - 1) * GateCount.Mux2(logk)

    @staticmethod
    def LeadingZeroDetect(n: int, m: int = 0) -> int:
        """Leading zero detector.

        Args:
            n (int): Number of bits in the input.
            m (int, optional): Number of bits in the output. Defaults to ``0``.

        Returns:
            int: Number of gates.
        """
        if n == 1:
            return 0
        if n == 2:
            return GateCount.NOT() + GateCount.Mux2(m)
        elif n <= 4:
            return 4 * GateCount.NAND() + 2 * GateCount.OR() + GateCount.Mux4(m)
        elif n <= 16:
            u = (n + 1) // 4
            v = (n - u * 4) > 0
            w = u + v
            return (
                GateCount.LeadingZeroDetect(2) * v
                + GateCount.LeadingZeroDetect(4) * u
                + GateCount.LeadingZeroDetect(w, 2)
            )
        elif n <= 32:
            return (
                GateCount.LeadingZeroDetect(16)
                + GateCount.LeadingZeroDetect(n - 16)
                + GateCount.LeadingZeroDetect(2, 4)
            )
        else:
            raise NotImplementedError(f"Leading zero detector for {n} bits is not implemented.")

    @staticmethod
    def IMA(mult_width: int, extra_accum_width: int = 1) -> tuple[int, int, int]:
        """Integer Multiplication and Addition.

        Args:
            mult_width (int): Width of the multiplier.
            extra_accum_width (int, optional): Extra width of the accumulator. Defaults to ``1``.

        Returns:
            tuple[int, int, int]: Number of gates for multiplication, addition, and normalization.
        """
        prod_n = 2 * mult_width
        accum_n = prod_n + extra_accum_width
        num_mult_gates = GateCount.Mult(mult_width) + GateCount.Reg(prod_n)
        num_add_gates = GateCount.Add(accum_n)
        num_norm_gates = GateCount.Reg(accum_n)
        return num_mult_gates, num_add_gates, num_norm_gates

    @staticmethod
    def FMA_Kulisch(mult_width: tuple[int, int], extra_accum_width: int) -> tuple[int, int, int]:
        """Floating-point Multiplication and Addition (Kulisch).

        Args:
            mult_width (tuple[int, int]): Width of the multiplier (mantissa width, exponent width).
            extra_accum_width (int): Extra width of the accumulator.

        Returns:
            tuple[int, int, int]: Number of gates for multiplication, addition, and normalization.
        """
        num_mult_gates, num_add_gates, num_norm_gates = 0, 0, 0
        # step 1: multiplication
        mult_e, mult_m = mult_width
        prod_e, prod_m = mult_e + 1, 2 * mult_m + 2
        prod_n = prod_m + 1
        num_mult_gates += GateCount.AND()  # sign mult
        num_mult_gates += GateCount.Add(mult_e)  # exponent add
        num_mult_gates += GateCount.Mult(mult_m + 1)  # mantissa mult
        num_mult_gates += GateCount.Reg(prod_e + prod_n)  # register
        # endstep
        # step 2: alignment and addition
        num_add_gates += GateCount.NOT() * prod_m + GateCount.Inc(prod_m)  # complement mantissa
        num_add_gates += GateCount.Mux2(prod_m)  # select mantissa
        shift_k = ((1 << mult_e) - 1) * 2
        num_add_gates += GateCount.LeftShift(prod_n, shift_k, extend=True)
        add_n = prod_m + shift_k + extra_accum_width
        num_add_gates += GateCount.Add(add_n)
        num_norm_gates += GateCount.Reg(add_n)
        # endstep
        return num_mult_gates, num_add_gates, num_norm_gates

    @staticmethod
    def FMA_Common(mult_width: tuple[int, int], accm_width: tuple[int, int]) -> tuple[int, int, int]:
        """Floating-point Multiplication and Addition (Common).

        Args:
            mult_width (tuple[int, int]): Width of the multiplier (mantissa width, exponent width).
            accm_width (tuple[int, int]): Width of the accumulator (mantissa width, exponent width).

        Returns:
            tuple[int, int, int]: Number of gates for multiplication, addition, and normalization.
        """
        num_mult_gates, num_add_gates, num_norm_gates = 0, 0, 0
        # step 1: multiplication
        mult_e, mult_m = mult_width
        prod_e, prod_m = mult_e + 1, 2 * mult_m + 2
        num_mult_gates += GateCount.AND()  # sign mult
        num_mult_gates += GateCount.Add(mult_e)  # exponent add
        num_mult_gates += GateCount.Mult(mult_m + 1)  # mantissa mult
        num_mult_gates += GateCount.Reg(prod_e + prod_m + 1)  # register
        # endstep
        # step 2: alignment and addition
        accum_e, accum_m = accm_width
        assert accum_e >= prod_e, "exponent width of adder must be greater than or equal to that of multiplier + 1"
        assert accum_m >= prod_m, "mantissa width of adder must be greater than or equal to that of multiplier + 2"
        num_add_gates += GateCount.Add(accum_e)  # exponent diff
        num_add_gates += GateCount.Mux2(accum_e)  # exponent select
        num_add_gates += GateCount.Mux2(accum_m)  # mantissa select max exp
        num_add_gates += GateCount.Mux2(accum_m)  # mantissa select min exp
        shift_k = (1 << accum_e) - 1
        num_add_gates += GateCount.RightShift(accum_m, shift_k)  # mantissa shift
        num_add_gates += (
            GateCount.XNOR() * accum_m + GateCount.Add(accum_m) - GateCount.HA() + GateCount.FA()
        )  # mantissa add/sub
        num_add_gates += GateCount.XNOR() * accum_m + GateCount.Inc(accum_m)
        # endstep
        # step 3: normalization
        num_norm_gates += GateCount.LeadingZeroDetect(accum_m)
        num_norm_gates += GateCount.Add(accum_e)  # exponent sub
        num_norm_gates += GateCount.LeftShift(accum_m, accum_m)  # mantissa shift
        num_norm_gates += GateCount.AND()  # sign
        num_norm_gates += GateCount.Reg(accum_e + accum_m)
        # endstep
        return num_mult_gates, num_add_gates, num_norm_gates
