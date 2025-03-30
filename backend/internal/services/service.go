package services

import "github.com/askaroe/cryptography-algorithms/pkg/utils"

type Service interface {
	EncryptMessageRSA(message string) (string, int, int, int)
	DecryptMessageRSA(cipher string, private int, modulo int) string
}

type service struct {
	logger *utils.Logger
}

func NewService(logger utils.Logger) Service {
	return &service{logger: &logger}
}
