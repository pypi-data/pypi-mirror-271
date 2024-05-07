"""Module for a pulse object representation"""
import os
import copy
import numpy as np
import lasertools_rffthelper as rfft
from lasertools_rffthelper.axes import Axes


class Pulse:
    """An object representing a pulse in time and frequency linked by RFFT

    Keyword arguments:
    - axes -- Object representing a signal and frequency axes linked by RFFT
    """

    def __init__(self, axes: Axes):
        self.axes = axes
        self.spectrum_complex = None

    def define_waveform(self, waveform: np.ndarray):
        """Calculate spectrum and phase from waveform

        Keyword arguments:
        - waveform -- Signal at each time"""

        self.spectrum_complex = rfft.complex_spectrum_from_signal(
            waveform, self.axes
        )

    def define_spectrum_complex(self, spectrum_complex: np.ndarray):
        """Define pulse based on complex spectrum

        Keyword arguments:
        - spectrum_complex -- Complex spectrum at each frequency
        """

        self.spectrum_complex = spectrum_complex

    def define_spectrum(
        self, spectrum_amplitude: np.ndarray, spectrum_phase: np.ndarray
    ):
        """Define pulse based on spectrum amplitude and phase

        Keyword arguments:
        - spectrum_amplitude -- Spectral amplitude at each frequency
        - spectrum_phase -- Spectral phase (radians) at each frequency
        """

        self.spectrum_complex = spectrum_amplitude * np.exp(
            1j * spectrum_phase
        )

    def recenter(self):
        """Recenters the peak of the waveform on the signal axis"""
        signal_center = (
            self.axes.signal_axis[-1] - self.axes.signal_axis[0]
        ) / 2
        signal_waveform_max = self.axes.signal_axis[
            np.argmax(self.envelope()[0])
        ]
        shift_amount = np.array([(signal_center - signal_waveform_max)])
        shifted_waveform = rfft.shift_signal(
            self.waveform(), shift_amount, self.axes, wrap=True
        )
        self.define_waveform(shifted_waveform)
        spectrum, spectrum_phase_centered = self.spectrum()
        index_weights = np.arange(len(spectrum))
        index_weighted = int(
            np.sum(index_weights * spectrum) / np.sum(spectrum)
        )
        self.define_spectrum(
            spectrum,
            spectrum_phase_centered - spectrum_phase_centered[index_weighted],
        )

    def waveform(self):
        """Returns: waveform of pulse"""

        return rfft.signal_from_complex_spectrum(
            self.spectrum_complex, self.axes
        )

    def spectrum(self):
        """Returns: spectral amplitude, spectral phase phase (radians)"""

        return np.abs(self.spectrum_complex), np.angle(self.spectrum_complex)

    def envelope(self, envelope_order: float = 1):
        """Returns: waveform envelope, instantaneous frequency"""

        (
            envelope,
            frequency,
            _,
            _,
        ) = rfft.envelope_frequency(
            self.waveform(), self.axes.axes_parameters.signal_step
        )
        return envelope**envelope_order, frequency

    def fwhm(self, envelope_order: float = 1):
        """Returns the full width at half max of the envelope

        Keyword arguments:
        - envelope_order (Optional) -- Exponent of envelope for FWHM calculation
        """

        envelope_raw, _ = self.envelope()
        envelope = envelope_raw**envelope_order
        envelope /= np.max(envelope)
        half_points = np.where(np.diff(np.sign(envelope - 0.5)))[0]
        return (
            self.axes.signal_axis[half_points[-1]]
            - self.axes.signal_axis[half_points[0]]
        )

    def fwhm_ftl(self, envelope_order: float = 1):
        """Returns the full width at half max of the transform limited envelope

        Keyword arguments:
        - envelope_order (Optional) -- Exponent of envelope for FWHM
        """

        pulse_ftl = copy.deepcopy(self)
        pulse_ftl.define_spectrum(
            pulse_ftl.spectrum()[0], np.zeros_like(pulse_ftl.spectrum()[0])
        )
        fwhm_ftl = pulse_ftl.fwhm(envelope_order=envelope_order)
        return fwhm_ftl

    def export(self, save_directory="", save_filename="pulse"):
        """A function to export the pulse to a csv file

        Keyword arguments:
        - save_directory (Optional) -- Directory of save location
        - save_filename (Optional) -- Filename for save
        """

        spectrum_amplitude, spectrum_phase = self.spectrum()

        np.savetxt(
            os.path.join(save_directory, save_filename + "_spectrum.csv"),
            np.transpose(
                np.vstack(
                    (
                        self.axes.frequency_axis,
                        spectrum_amplitude,
                        spectrum_phase,
                    )
                )
            ),
            delimiter=",",
        )
        np.savetxt(
            os.path.join(save_directory, save_filename + "_waveform.csv"),
            np.transpose(
                np.vstack(
                    (
                        self.axes.signal_axis,
                        self.waveform(),
                    )
                )
            ),
            delimiter=",",
        )


def import_pulse_data(save_directory="", save_filename="pulse"):
    """Import pulse from a csv file
    WARNING: Pulse must be defined by rffthelper Axes
    TIP: To interpolate, use an arbitrary pulse model

    Keyword arguments:
    - save_directory (Optional) -- Directory of save location
    - save_filename (Optional) -- Filename for save
    """

    data_spectrum = np.loadtxt(
        os.path.join(save_directory, save_filename + "_spectrum.csv"),
        delimiter=",",
    )

    data_waveform = np.loadtxt(
        os.path.join(save_directory, save_filename + "_waveform.csv"),
        delimiter=",",
    )

    axes = rfft.Axes(
        rfft.AxesParameters(
            signal_length=np.max(data_waveform[:, 0]),
            frequency_length=np.max(data_spectrum[:, 0]),
        )
    )

    pulse_instance = Pulse(axes)
    pulse_instance.define_spectrum(data_spectrum[:, 1], data_spectrum[:, 2])

    return pulse_instance
