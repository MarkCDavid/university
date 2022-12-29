class KyberParametersBase:
    def __init__(self):
        self.seed_size = 32 # KYBER_SYM_BYTES
        # IMPORTANT(Aurimas): polynomial_coefficient_count indicated the size of vector required after
        #                     applying NTT. The maximum degree for polynomial is defined with parameter 
        #                     'n', which for given parameter sets is always 256. 
        # IMPORTANT(Aurimas): This might still be incorrect! NTT transformation leaves us with vector of
        #                     size 256.
        self.polynomial_coefficient_count = 384 
        self.montgomery = 2285
        self._static_seed = [68, 17, 101, 2, -4, -78, -21, 4, -72, 25, -39, 126, -58, -3, -94, 37, 126, -53, 37, 68, 77, -48, -74, -26, 86, -24, 36, -67, 16, -7, 123, -11]
        self._static = False


class KyberParameters512(KyberParametersBase):

    def __init__(self):
        super().__init__()
        self.n = 256 # KYBER_N, maximum degree of polynomials used
        self.k = 2 # number of polynomials per vector
        self.q = 3329 # KYBER_Q, modulus for numbers
        self.inverse_q = 62209 # KYBER_Q_INV

        # controlls how big coefficients for small vectors can be
        self.eta1 = 3
        self.eta2 = 2

        # controls how much (u,v) get compressed
        self.du = 10,
        self.dv = 4, 

class KyberParameters768(KyberParametersBase):

    def __init__(self):
        super().__init__()
        self.n = 256 # KYBER_N, maximum degree of polynomials used
        self.k = 3 # number of polynomials per vector
        self.q = 3329 # KYBER_Q, modulus for numbers
        self.inverse_q = 62209 # KYBER_Q_INV

        # controlls how big coefficients for small vectors can be
        self.eta1 = 2
        self.eta2 = 2

        # controls how much (u,v) get compressed
        self.du = 10,
        self.dv = 4, 

class KyberParameters1024(KyberParametersBase):

    def __init__(self):
        super().__init__()
        self.n = 256 # KYBER_N, maximum degree of polynomials used
        self.k = 4 # number of polynomials per vector
        self.q = 3329 # KYBER_Q, modulus for numbers
        self.inverse_q = 62209 # KYBER_Q_INV

        # controlls how big coefficients for small vectors can be
        self.eta1 = 2
        self.eta2 = 2

        # controls how much (u,v) get compressed
        self.du = 11,
        self.dv = 5, 



PARAMETERS_512 = KyberParameters512()
PARAMETERS_768 = KyberParameters768()
PARAMETERS_1024 = KyberParameters1024()


PARAMETERS = PARAMETERS_512
PARAMETERS._static = True