package handlers

import (
	"github.com/askaroe/cryptography-algorithms/internal/entity"
	"github.com/askaroe/cryptography-algorithms/internal/services"
	"github.com/gin-gonic/gin"
	"net/http"
)

type Handler struct {
	s services.Service
}

func NewHandler(s services.Service) *Handler {
	return &Handler{s: s}
}

func (h *Handler) EncryptMessageRSA(c *gin.Context) {
	var body entity.RsaEncryptRequest
	err := c.Bind(&body)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	result, public, private, modulo := h.s.EncryptMessageRSA(body.Message)
	c.JSON(http.StatusOK, entity.RsaEncryptResponse{Cipher: result, PublicKey: public, PrivateKey: private, EulerTotientFunction: modulo})
}

func (h *Handler) DecryptMessageRSA(c *gin.Context) {
	var body entity.RsaDecryptRequest
	err := c.Bind(&body)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	result := h.s.DecryptMessageRSA(body.Cipher, 317, 396)

	c.JSON(http.StatusOK, entity.RsaDecryptResponse{Cipher: result})
}
