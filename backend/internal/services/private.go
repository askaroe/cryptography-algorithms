package services

import "math"

func (s *service) isPrime(num int) bool {
	if num < 2 {
		return false
	}
	for i := 2; i <= int(math.Sqrt(float64(num))); i++ {
		if num%i == 0 {
			return false
		}
	}
	return true
}

func (s *service) gcd(a, b int) int {
	if a == 0 || b == 0 {
		return 0
	}

	if a == b {
		return a
	}

	if a > b {
		return s.gcd(a-b, b)
	}
	return s.gcd(a, b-a)
}

func (s *service) isCoprime(a, b int) bool {
	if s.gcd(a, b) == 1 {
		return true
	}
	return false
}
