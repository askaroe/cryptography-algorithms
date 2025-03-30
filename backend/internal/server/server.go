package server

import (
	"context"
	"github.com/askaroe/cryptography-algorithms/config"
	"github.com/askaroe/cryptography-algorithms/pkg/utils"
	"github.com/gin-gonic/gin"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

type Server struct {
	httpServer *http.Server
	logger     *utils.Logger
}

func New(cfg config.Config, router *gin.Engine, logger *utils.Logger) *Server {
	return &Server{
		httpServer: &http.Server{
			Addr:    ":" + cfg.Port,
			Handler: router,
		},
		logger: logger,
	}
}

func (s *Server) Start() {
	go func() {
		s.logger.Info("starting server")
		if err := s.httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			s.logger.Fatalf("failed to start server: %v", err)
		}
	}()
}

func (s *Server) HandleShutdown() {
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

	<-quit

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := s.httpServer.Shutdown(ctx); err != nil {
		s.logger.Fatalf("failed to shutdown server: %v", err)
	}

	s.logger.Info("shutting down")
}
