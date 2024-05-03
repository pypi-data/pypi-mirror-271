.. _sec-experiment_setup:

****************
Trial list file
****************

The trial list file is a CSV text file using a semicolon `;` as field separator. The first two lines contain directives regarding the randomization of the list and the presentation of feedback. In particular the first line must be either:

::
   
    Randomize: True

if you wish to present the list in random order, or:


::
   
    Randomize: False

if you wish to present the list in sequential order. The second line must be either:

::
   
    Feedback: True

if you wish to give feedback after each response:


::
   
    Feedback: False

if you do not wish to give feedback after each response. Each of the following lines set the parameters for a trial. The first column of these lines contains the path of the WAV file to be played. The second column contains the phrase spoken in the WAV file, so that it can be shown in written form to the participant during the trial. The third column indicates the emotion in which the phrase is spoken. Note that this must match the written form shown in the interface buttons (including letter case, accents, etc...). This also means that if you're using, for example, French as the language for the `emid` user interface, the emotion in the trial list must be also written in French. The final column indicates the RMS level, in dB SPL, at which the phrase will be played out (note that a calibration has to be performed for this to be accurate).

.. _fig-menu_bar:

.. figure:: Figures/example_trial_list.png
   :scale: 100%
   :alt: Example trial list

   Example trial list
