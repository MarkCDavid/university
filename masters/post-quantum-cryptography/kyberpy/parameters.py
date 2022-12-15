class KyberParameters:

    def __init__(self):
        self.k = 2 # number of polynomials per vector
        self.n = 256 # KYBER_N, maximum degree of polynomials used
        self.q = 3329 # KYBER_Q, modulus for numbers
        self.inverse_q = 62209 # KYBER_Q_INV

        self.seed_size = 32 # KYBER_SYM_BYTES

        # controlls how big coefficients for small vectors can be
        self.eta1 = 3 # KYBER_ETAK512, KYBER_ETAK768_1024
        self.eta2 = 2 # KYBER_ETAK768_1024

        # controls how much (u,v) get compressed
        self.du = 10,
        self.dv = 4, 
        self.polynomial_coefficient_count = 384

        # Controls
        self._static_bytes = [68, 17, 101, 2, -4, -78, -21, 4, -72, 25, -39, 126, -58, -3, -94, 37, 126, -53, 37, 68, 77, -48, -74, -26, 86, -24, 36, -67, 16, -7, 123, -11]
        self._static = False

PARAMETERS = KyberParameters()
PARAMETERS._static = True