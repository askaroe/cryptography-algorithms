package router

import (
	"github.com/askaroe/cryptography-algorithms/internal/handlers"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func New(handler *handlers.Handler) *gin.Engine {
	r := gin.New()
	r.Use(gin.Logger())
	r.Use(gin.Recovery())

	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"}, // Replace with specific origins if needed
		AllowMethods:     []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"*"}, // Replace with specific headers if needed
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           300, // Maximum cache age in seconds
	}))

	r.Use(SetJSONContentType())

	api := r.Group("api/v1")
	{
		rsa := api.Group("/rsa")
		{
			rsa.POST("/encrypt", handler.EncryptMessageRSA)
			rsa.POST("/decrypt", handler.DecryptMessageRSA)
		}
	}

	return r
}

func SetJSONContentType() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Content-Type", "application/json")
		c.Next()
	}
}
