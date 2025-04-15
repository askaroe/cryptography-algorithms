import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CryptographyService {

  private apiUrl = 'http://localhost:8000'; // FastAPI server URL

  constructor(private http: HttpClient) { }

  // RSA key generation
  generateRSAKeys(bits: number) {
    return this.http.post(`${this.apiUrl}/rsa/generate-keys`, { bits });
  }

  // RSA encryption
  encryptRSA(message: string, publicKey: number[]) {
    return this.http.post(`${this.apiUrl}/rsa/encrypt`, { message, public_key: publicKey });
  }

  // RSA decryption
  decryptRSA(ciphertext: number[], privateKey: number[]) {
    return this.http.post(`${this.apiUrl}/rsa/decrypt`, { ciphertext, private_key: privateKey });
  }

  // RSA signature creation
  signRSA(message: string, privateKey: number[], hashAlgorithm: string) {
    return this.http.post(`${this.apiUrl}/rsa/sign`, { message, private_key: privateKey, hash_algorithm: hashAlgorithm });
  }

  // RSA signature verification
  verifyRSA(message: string, signature: string, publicKey: number[], hashAlgorithm: string) {
    return this.http.post(`${this.apiUrl}/rsa/verify`, { message, signature, public_key: publicKey, hash_algorithm: hashAlgorithm });
  }

  // ElGamal key generation
  generateElGamalKeys(bits: number) {
    return this.http.post(`${this.apiUrl}/elgamal/generate-keys`, { bits });
  }

  // ElGamal encryption
  encryptElGamal(message: string, publicKey: number[]) {
    return this.http.post(`${this.apiUrl}/elgamal/encrypt`, { message, public_key: publicKey });
  }

  // ElGamal decryption
  decryptElGamal(a: string, bList: string[], privateKey: number[]) {
    return this.http.post(`${this.apiUrl}/elgamal/decrypt`, { a, b_list: bList, private_key: privateKey });
  }

  // ElGamal signature creation
  signElGamal(message: string, privateKey: number[], hashAlgorithm: string) {
    return this.http.post(`${this.apiUrl}/elgamal/sign`, { message, private_key: privateKey, hash_algorithm: hashAlgorithm });
  }

  // ElGamal signature verification
  verifyElGamal(message: string, signature: string[], publicKey: number[], hashAlgorithm: string) {
    return this.http.post(`${this.apiUrl}/elgamal/verify`, { message, signature, public_key: publicKey, hash_algorithm: hashAlgorithm });
  }

  // DSA key generation
  generateDSAKeys(L: number, N: number) {
    return this.http.post(`${this.apiUrl}/dsa/generate-keys`, { L, N });
  }

  // DSA signature creation
  signDSA(message: string, privateKey: number[], hashAlgorithm: string) {
    return this.http.post(`${this.apiUrl}/dsa/sign`, { message, private_key: privateKey, hash_algorithm: hashAlgorithm });
  }

  // DSA signature verification
  verifyDSA(message: string, signature: string[], publicKey: string[], hashAlgorithm: string) {
    return this.http.post(`${this.apiUrl}/dsa/verify`, { message, signature, public_key: publicKey, hash_algorithm: hashAlgorithm });
  }
}
