import random
from Crypto.Util import number


def gcd(a, b) -> int:
    '''
    Euclidean algorithm. 
    Method for computing the greatest common divisor  between two integers.
    For determining if two numbers are coprime.
    '''
    while b != 0:
        a, b = b, a % b
    return a


def extgcd(a, b):
    '''
    Extended Euclidean algorithm.
    Finding for finding the modular multiplicative inverse for RSA.
    '''
    if a == 0:
        return (b, 0, 1)
    gcd, x, y = extgcd(b % a, a)
    return (gcd, y - (b // a) * x, x)


class RSA_model:
    """
    NOTE this model uses a method of encrypting messages that is vulnerable 
    to frequency analysis. This method is used solely to demonstrate RSA encryption/decryption
    and is not recommended in real world applications.
    """

    def __init__(self):
        '''
        Initializing private, public key pairs used in RSA

        Private key consists of large prime numbers _q and _p, 
        and modular inverse of the totient and coprime.

        Public key consists of the RSA modulus (_q * _p), and 
        the number coprime to the totient.
        '''
        # "Large" private prime numbers
        # We can discard these numbers after computing the keys
        # Typical RSA uses much larger 1048 or longer numbers
        self._p = number.getPrime(32)
        self._q = number.getPrime(32)
        
        # RSA modulus
        self.n = self._p * self._q

        # Totient of the RSA modulus
        phi = (self._p - 1) * (self._q - 1)

        # Number coprime to totient 
        # Part of the public key
        self.e = random.randrange(2, phi)
        while gcd(self.e, phi) != 1:
            self.e = random.randrange(2, phi)

        # The modular inverse of phi and e
        # Part of the public key
        self._d = extgcd(phi, self.e)[2]

        # Positive modular inverse
        if self._d < 0:
            self._d += phi

    def encrypt(self, message, e, n):
        '''
        Encrypting each character utilizing the RSA public key.
        This is vulnerable to frequency analysis
        '''
        # cipher = [pow(ord(c), e, n) for c in message]
        cipher = []
        for c in message:
            # Encrypt character
            c0 = pow(ord(c), e, n)
            print("Encrypting char:", c, "to", c0)
            cipher.append(c0)
        return cipher

    def decrypt(self, cipher):
        '''
        Decrypting each character utilizing the RSA public key.
        '''
        # message = [chr(pow(c, self._d, self.n)) for c in cipher]
        message = []
        for c0 in cipher:
            c = chr(pow(c0, self._d, self.n))
            print("Decrypting:", c0, "to", c)
            message.append(c)
        return ''.join(message)


if __name__ == "__main__":
    print("Generating Alice's public and private RSA keys")
    alice = RSA_model()
    print("Alice's private keys are: ", alice._p, alice._q, alice._d)
    print("Alice's public keys are: ", alice.n, alice.e)
    print("Alice share's her public keys over the network with Bob.")
    bob_message = input("Bob wants to send Alice a message. What message does Bob send?: ")
    cipher = alice.encrypt(bob_message, alice.e, alice.n)
    print("Bob encrypts his message using the public key Alice provided\n", cipher, "\nand sends it to Alice over the network.")
    decrypted = alice.decrypt(cipher)
    print("Alice receives the message from Bob, decrypts it, and reads the following:\n")
    print(decrypted)