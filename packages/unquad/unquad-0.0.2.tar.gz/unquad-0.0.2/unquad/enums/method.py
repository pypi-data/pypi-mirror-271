from enum import Enum


class Method(Enum):
    """
    Enumerators of available conformal detection methods for uncertainty-quantified anomaly detection.
    """

    SPLIT_CONFORMAL: str = "SC"
    CV: str = "CV"
    CV_PLUS: str = "CV+"
    JACKKNIFE: str = "J"
    JACKKNIFE_PLUS: str = "J+"
    JACKKNIFE_AFTER_BOOTSTRAP: str = "JaB"
    JACKKNIFE_PLUS_AFTER_BOOTSTRAP: str = "J+aB"
