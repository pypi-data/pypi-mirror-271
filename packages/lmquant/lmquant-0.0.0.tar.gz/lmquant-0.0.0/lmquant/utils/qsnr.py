# -*- coding: utf-8 -*-
"""Utility functions for Quantization Signal-to-Noise Ratio (QSNR)."""

import torch

__all__ = ["convert_to_dB", "convert_from_dB", "get_qsnr"]


def convert_to_dB(x: torch.Tensor, *, squared: bool = True) -> torch.Tensor:  # noqa: N802
    """Convert a linear value to dB.

    Args:
        x (torch.Tensor): Linear value.
        squared (bool, optional): Whether input is squared. Defaults to ``True``.

    Returns:
        torch.Tensor: dB value.
    """
    if squared:
        return 10 * torch.log10(x)
    else:
        return 20 * torch.log10(x)


def convert_from_dB(x: torch.Tensor, *, square: bool = True) -> torch.Tensor:  # noqa: N802
    """Convert a dB value to linear value.

    Args:
        x (torch.Tensor): dB value.
        square (bool, optional): Whether to square the output. Defaults to ``True``.

    Returns:
        torch.Tensor: Linear value.
    """
    if square:
        return 10 ** (x / 10)
    else:
        return 10 ** (x / 20)


def get_qsnr(*, x: torch.Tensor, q_x: torch.Tensor, dB: bool = True) -> torch.Tensor:  # noqa: N803
    """Compute QSNR (quantization signal-to-noise ratio) for input and quantized input.

    Args:
        x (torch.Tensor): Input.
        q_x (torch.Tensor): Quantized input.
        dB (bool, optional): Whether to return dB value. Defaults to ``True``.

    Returns:
        torch.Tensor: QSNR.
    """
    assert x.shape == q_x.shape
    x, q_x = x.float(), q_x.float()
    qsnr = x.norm() / (x - q_x).norm()
    if dB:
        return convert_to_dB(qsnr, squared=False)
    else:
        return qsnr**2


def get_qsnr_avg_std(qsnr: torch.Tensor, dB: bool = True) -> tuple[torch.Tensor, torch.Tensor]:  # noqa: N803
    """Compute average and standard deviation of QSNR (quantization signal-to-noise ratio).

    Args:
        qsnr (torch.Tensor): QSNR.

    Returns:
        tuple[torch.Tensor, torch.Tensor]: Average and standard deviation of QSNR.
    """
    if dB:
        qsnr = convert_from_dB(qsnr, square=True)
    avg = qsnr.mean()
    std = qsnr.std()
    if dB:
        avg = convert_to_dB(avg, squared=True)
        std = convert_to_dB(std, squared=True)
    return avg, std
