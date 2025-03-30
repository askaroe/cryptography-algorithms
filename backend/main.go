package main

import (
	"github.com/askaroe/cryptography-algorithms/config"
	"github.com/askaroe/cryptography-algorithms/internal/handlers"
	"github.com/askaroe/cryptography-algorithms/internal/router"
	"github.com/askaroe/cryptography-algorithms/internal/server"
	"github.com/askaroe/cryptography-algorithms/internal/services"
	"github.com/askaroe/cryptography-algorithms/pkg/utils"
)

func main() {
	logger := utils.NewLogger("")
	cfg, err := config.GetConfig()

	if err != nil {
		logger.Fatalf("failed to get config: %v", err)
	}

	svc := services.NewService(logger)
	if err != nil {
		logger.Fatalf("failed to create service: %v", err)
		return
	}

	handler := handlers.NewHandler(svc)

	r := router.New(handler)

	srv := server.New(*cfg, r, &logger)
	srv.Start()
	srv.HandleShutdown()

}
