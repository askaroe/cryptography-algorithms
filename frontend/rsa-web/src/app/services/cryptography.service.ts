import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class CryptoService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  // --- RSA ---
  generateRSAKeys(bits: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/rsa/generate-keys`, { bits });
  }

  rsaEncrypt(message: string, public_key: string[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/rsa/encrypt`, { message, public_key });
  }

  rsaDecrypt(ciphertext: string[], private_key: string[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/rsa/decrypt`, { ciphertext, private_key });
  }

  rsaSign(message: string, private_key: string[], hash_algorithm: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/rsa/sign`, { message, private_key, hash_algorithm });
  }

  rsaVerify(message: string, signature: string, public_key: string[], hash_algorithm: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/rsa/verify`, { message, signature, public_key, hash_algorithm });
  }

  // --- ElGamal ---
  generateElGamalKeys(bits: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/elgamal/generate-keys`, { bits });
  }

  elgamalEncrypt(message: string, public_key: string[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/elgamal/encrypt`, { message, public_key });
  }

  elgamalDecrypt(a: string, b_list: string[], private_key: string[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/elgamal/decrypt`, { a, b_list, private_key });
  }

  elgamalSign(message: string, private_key: string[], hash_algorithm: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/elgamal/sign`, { message, private_key, hash_algorithm });
  }

  elgamalVerify(message: string, signature: string[], public_key: string[], hash_algorithm: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/elgamal/verify`, { message, signature, public_key, hash_algorithm });
  }

  // --- DSA ---
  generateDSAKeys(L: number, N: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/dsa/generate-keys`, { L, N });
  }

  dsaSign(message: string, private_key: string[], hash_algorithm: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/dsa/sign`, { message, private_key, hash_algorithm });
  }

  dsaVerify(message: string, signature: string[], public_key: string[], hash_algorithm: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/dsa/verify`, { message, signature, public_key, hash_algorithm });
  }
}
