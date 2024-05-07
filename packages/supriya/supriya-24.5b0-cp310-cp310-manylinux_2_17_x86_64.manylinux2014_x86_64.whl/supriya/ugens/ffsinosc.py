from collections.abc import Sequence

from supriya import utils

from .core import UGen, param, ugen


@ugen(ar=True, kr=True)
class Blip(UGen):
    """
    A band limited impulse generator.

    ::

        >>> blip = supriya.ugens.Blip.ar(
        ...     frequency=440,
        ...     harmonic_count=200,
        ... )
        >>> blip
        <Blip.ar()[0]>
    """

    frequency = param(440.0)
    harmonic_count = param(200.0)


@ugen(ar=True, kr=True)
class FSinOsc(UGen):
    """
    Very fast sine wave generator (2 PowerPC instructions per output sample!) implemented using a ringing filter.

    ::

        >>> fsin_osc = supriya.ugens.FSinOsc.ar(
        ...     frequency=440,
        ...     initial_phase=0,
        ... )
        >>> fsin_osc
        <FSinOsc.ar()[0]>
    """

    frequency = param(440.0)
    initial_phase = param(0.0)


@ugen(ar=True)
class Klank(UGen):
    """
    A bank of resonators.

    ::

        >>> frequencies = [200, 671, 1153, 1723]
        >>> amplitudes = None
        >>> decay_times = [1, 1, 1, 1]
        >>> specifications = [frequencies, amplitudes, decay_times]
        >>> source = supriya.ugens.BrownNoise.ar() * 0.001
        >>> klank = supriya.ugens.Klank.ar(
        ...     decay_scale=1,
        ...     frequency_offset=0,
        ...     frequency_scale=1,
        ...     source=source,
        ...     specifications=specifications,
        ... )
        >>> klank
        <Klank.ar()[0]>
    """

    source = param()
    frequency_scale = param(1)
    frequency_offset = param(0)
    decay_scale = param(1)
    specifications = param(unexpanded=True)

    def __init__(
        self,
        calculation_rate=None,
        decay_scale=1,
        frequency_offset=0,
        frequency_scale=1,
        source=None,
        specifications=None,
    ):
        # TODO: Refactor this to not override __init__?
        frequencies, amplitudes, decay_times = specifications
        assert len(frequencies)
        if not amplitudes:
            amplitudes = [1.0] * len(frequencies)
        elif not isinstance(amplitudes, Sequence):
            amplitudes = [amplitudes] * len(frequencies)
        if not decay_times:
            decay_times = [1.0] * len(frequencies)
        elif not isinstance(decay_times, Sequence):
            decay_times = [decay_times] * len(frequencies)
        specifications = utils.zip_cycled(frequencies, amplitudes, decay_times)
        specifications = utils.flatten(specifications)
        specifications = tuple(specifications)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            decay_scale=decay_scale,
            frequency_offset=frequency_offset,
            frequency_scale=frequency_scale,
            source=source,
            specifications=specifications,
        )


@ugen(ar=True, kr=True)
class Pulse(UGen):
    """
    Band limited pulse wave generator with pulse width modulation.

    ::

        >>> pulse = supriya.ugens.Pulse.ar(
        ...     frequency=440,
        ...     width=0.5,
        ... )
        >>> pulse
        <Pulse.ar()[0]>
    """

    frequency = param(440.0)
    width = param(0.5)


@ugen(ar=True, kr=True, is_pure=True)
class Saw(UGen):
    """
    A band-limited sawtooth oscillator unit generator.

    ::

        >>> supriya.ugens.Saw.ar()
        <Saw.ar()[0]>
    """

    frequency = param(440.0)
