.. _sec-calibration:

************************
Sound Level Calibration
************************

Figure :ref:`fig-edit_transducers` shows a screenshot of the “Transducers” dialog which is used for setting calibration values.

.. _fig-edit_transducers:

.. figure:: Figures/edit_transducers.png
   :scale: 75%
   :alt: Transducers dialog

   Transducers dialog

Most of the fields should be pretty much self-explanatory. Using this
dialog you can add headphones/speakers models to the transducers database.
In the “Max Level” field you should enter the level in dB SPL that is output
by the transducer for a full amplitude sinusoid (a sinusoid with a peak amplitude of 1).
On the rightmost panel of the dialog you have facilities to play a sinusoid with a specified
level. You can use these facilities to check with a SPL meter (or a
voltmeter depending on how you’re doing it) that the actual output level
corresponds to the desired output level. Using these facilities you can
also play a full amplitude sinusoid: you need to set the level of the
sinuoid to the “Max Level” of the transducer in the dialog (whatever it is).
Be careful because it can be very loud! More detailed instructions on
the calibration procedure are provided below.

Calibrating Headphones
======================

Calibrating with an SPL meter
------------------------------

Open the "Transducers" dialog. Select the transducer for which you want to calibrate and note its
``MaxLevel`` (by default this is set to 100 dB SPL). Use the rightmost panel to play
a 1-kHz sinusoid at the ``MaxLevel`` (e.g. 100 dB), and read the measurement on the SPL
meter. Change the ``MaxLevel`` for the transducer to the measurement you just read on the SPL meter.

You don't actually need to play the sinusoid at the ``MaxLevel`` (and it may be better not to do so
because you may get distortions at very high levels). Instead, you could for example
play it at a level equal to ``MaxLevel`` - 20. The reading that you would obtain from the SPL meter
would then be 20 dB below the ``MaxLevel``. You would then simply add 20 to the SPL meter reading
and set ``MaxLevel`` to this value.

Calibrating with a voltmeter
-----------------------------

Open the "Transducers" dialog. Select the transducer for which you want to calibrate and note its
``MaxLevel`` (by default this is set to 100 dB SPL). Use the rightmost panel to play
a 1-kHz sinusoid at the ``MaxLevel`` (e.g. 100 dB), and note the RMS voltage reading from
a voltmeter connected to a cable receiving input from the soundcard.
Manufacturers of professional headphones usually provide datasheets indicating
what is the dB SPL level output by the transducer when it is driven by a 1-volt :sub:`RMS`
sinusoid at 1 kHz. You can use this figure to calculate what the dB SPL output is for the
1-kHz sinusoid. Suppose that the dB SPL output for a 1-volt :sub:`RMS` sinusoid at 1 kHz
is :math:`L_r`, and the voltage output for the sinusoid played at ``MaxLevel`` is :math:`V_x`,
the dB SPL output for the sinusoid (:math:`L_x`) will be:

.. math::
   
   L_x = L_r + 20 log10(V_x)

if the reference RMS voltage in the datasheet is not 1 but some other value :math:`V_r`,
:math:`L_x` can be calculated as:   

.. math::

   L_x = L_r + 20 log10(V_x/V_r)

Finally, set the ``MaxLevel`` for the transducer you're calibrating to :math:`L_x`.
As for the SPL meter calibration
you do not actually need to play the sinusoid at the ``MaxLevel`` (and it may be better not to do so
because you may get distortions at very high levels). Instead, you could for example
play it at a level equal to ``MaxLevel`` - 20. You would then add back the 20 dBs in the equation to
compute :math:`L_x`:

.. math::

   L_x = L_r + 20 log10(V_x) + 20



Calibrating Loudspeakers
=========================

Typically a noise is used for calibrating loudspeakers because it's difficult to get reliable readings with an SPL meter for a pure tone.

The procedure I normally use for calibrating loudspeakers is to save on disk a noise stimulus as a wav file. I filter the noise within the operating range of the SPL meter (usually around 0.05 to 8 kHz). The noise level needs to be reasonably loud as to avoid signal-to-noise ratio issues, but not too loud as to cause distortions or damage your hearing in the measurement process. Once I've found a reasonable level, by trial and error, I measure the actual level with an SPL meter held at the position where the listener head would be located relative to the loudspeaker during the experiment and note it down.

We can measure the RMS level of the WAV file with the noise used for calibration, let's call it :math:`rmsnoise`. A sinusoid at max amplitude (amplitude = 1, by convention) has a root-mean-square amplitude of 1/sqrt(2) = 0.707. The difference in dB between the level of a sinusoid at max amplitude and our calibration noise will be equal to:

.. math::

   dbdiff = 20*log10((1/sqrt(2))/rmsnoise)

Therefore, if our calibration noise had a level (measured with the SPL meter) or :math:`x` dB SPL, a sinusoid at max amplitude would have a level of:

.. math::

   maxlev = x + dbdiff

this is the value that you need to enter in the ``Max Level`` field of the transducers calibration table for the loudspeakers in question.
