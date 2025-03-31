import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RsaService {
  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  generateKeys(): Observable<any> {
    return this.http.post(`${this.apiUrl}/generate-keys`, {});
  }

  encryptMessage(message: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/encrypt`, { message });
  }

  decryptMessage(ciphertext: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/decrypt`, { ciphertext });
  }

  saveKeys(publicKey: string, privateKey: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/save-keys`, { publicKey, privateKey });
  }

  saveEncrypted(ciphertext: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/save-encrypted`, { ciphertext });
  }

  saveDecrypted(decryptedText: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/save-decrypted`, { decryptedText });
  }
}
