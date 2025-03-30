package services

import (
	"github.com/askaroe/cryptography-algorithms/internal/entity"
	"math/big"
	"strconv"
	"strings"
)

func (s *service) EncryptMessageRSA(message string) (string, int, int, int) {
	s.logger.Infof("Encrypting message: %s", message)

	// Generate RSA Key Pair
	public, private, modulo := s.GenerateRsaKeyPair()

	// Encrypt message
	var cipherTextSlice []*big.Int
	var chars []int32

	for _, ch := range message {
		chars = append(chars, ch)
		// Convert character to big.Int
		charBig := big.NewInt(int64(ch))
		publicBig := big.NewInt(int64(public))
		moduloBig := big.NewInt(int64(modulo))

		// Encrypt: (ch^public) % modulo
		cipherBig := new(big.Int).Exp(charBig, publicBig, moduloBig)
		cipherTextSlice = append(cipherTextSlice, cipherBig)
	}

	// Convert cipher text to a comma-separated string
	cipherTextStrings := make([]string, len(cipherTextSlice))
	for i, num := range cipherTextSlice {
		cipherTextStrings[i] = num.String() // Convert big.Int to string
	}

	s.logger.Info(chars)

	result := strings.Join(cipherTextStrings, ",")
	s.logger.Infof("Encryption result: %s", result)

	// Return the cipher text along with the keys
	return result, public, private, modulo
}

func (s *service) DecryptMessageRSA(cipher string, private int, modulo int) string {
	s.logger.Infof("Decrypting cipher: %s", cipher)
	s.logger.Infof("Private key: %d, Modulo: %d", private, modulo)

	// Split the cipher text (comma-separated numbers)
	cipherParts := strings.Split(cipher, ",")
	var messageTextSlice []rune
	var chars []int64

	for _, part := range cipherParts {
		numberPart, _ := strconv.Atoi(part)

	}

	// Convert rune slice to string
	result := string(messageTextSlice)
	s.logger.Infof("Decryption result: %s", result)
	s.logger.Infof("Decrypted numbers: %v", chars)

	return result
}

func (s *service) GenerateRsaKeyPair() (int, int, int) {
	eulerTotientFunctionOfPandQ := s.EulerTotientFunction(entity.P-1, entity.Q-1)

	s.logger.Infof("modulo %d", eulerTotientFunctionOfPandQ)

	encryptionExponent := s.FindEncryptionExponent(eulerTotientFunctionOfPandQ)

	s.logger.Infof("encryption exponent or public key: %d", encryptionExponent)

	decryptionExponent := s.InverseModulo(encryptionExponent, eulerTotientFunctionOfPandQ)

	s.logger.Infof("decryption exponent or private key: %d", decryptionExponent)

	return encryptionExponent, decryptionExponent, eulerTotientFunctionOfPandQ
}

func (s *service) EulerTotientFunction(p, q int) int {
	return (entity.P - 1) * (entity.Q - 1)
}

func (s *service) FindEncryptionExponent(eulerTotientFunctionOfPandQ int) int {
	for i := 2; i < eulerTotientFunctionOfPandQ; i++ {
		if s.isCoprime(i, eulerTotientFunctionOfPandQ) {
			return i
		}
	}
	return -1
}

func (s *service) InverseModulo(encryptionExponent, eulerTotient int) int {
	i := 1
	for {
		if (i*encryptionExponent)%eulerTotient == 1 {
			return i
		}
		i++
	}

}
