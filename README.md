# light_pulse_modelling
What it does:
> has two user inputs (from cmd line): pulse_qidth and time_delay. Pulse_width will be the FWHM and time_delay will be the time after which the pulse shall be played.

Key features:
> given the FWHM it calculates the sigma value for the Gauss distribution;
> calculates the delay accordingly, with a certain error estimation eps (modifiable);

Future improvements:
> at the moment, th epeak is normalized, so it reaches the maximum voltage the modulator has been set to. Rather than doing so, given a constant parameter with the maximum voltage, to modelate the pulse in such way that it only reaches the amount desired by the user