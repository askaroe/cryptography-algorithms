package entity

const (
	P = 3
	Q = 5
)

type RsaEncryptRequest struct {
	Message string `json:"message"`
}

type RsaEncryptResponse struct {
	Cipher               string `json:"cipher"`
	PublicKey            int    `json:"publicKey"`
	PrivateKey           int    `json:"privateKey"`
	EulerTotientFunction int    `json:"eulerTotientFunction"`
}

type RsaDecryptRequest struct {
	Cipher string `json:"cipher"`
}

type RsaDecryptResponse struct {
	Cipher string `json:"cipher"`
}
