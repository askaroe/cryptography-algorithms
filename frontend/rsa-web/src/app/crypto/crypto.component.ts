import { Component } from '@angular/core';
import { CryptoService } from '../services/cryptography.service';

@Component({
  selector: 'app-crypto',
  templateUrl: './crypto.component.html',
  styleUrls: ['./crypto.component.css']
})
export class CryptoComponent {
  selectedAlgorithm = 'rsa';
  rsa = {
    bits: 512,
    message: '',
    publicKey: [] as string[],
    privateKey: [] as string[],
    ciphertext: [] as string[],
    cipherInput: '',
    decrypted: '',
    signature: '',
    signatureInput: '',     // <--- user input
    publicKeyInput: '', 
    valid: false,
    hash: 'SHA-256'
  };

  elgamal = {
    bits: 256,
    message: '',
    publicKey: [] as string[],       // [p, g, y]
    privateKey: [] as string[],      // [x, p]
    a: '',                           // result of encryption
    bList: [] as string[],           // result of encryption
    cipherAInput: '',                // <-- user input
    cipherBInput: '',                // <-- user input
    decrypted: '',
    signature: [] as string[],
    signatureInput: '',             // <-- user input
    publicKeyInput: '',             // <-- user input
    valid: false,
    hash: 'SHA-256'
  };

  dsa = {
    L: 512,
    N: 160,
    message: '',
    publicKey: [] as string[],  // [p, q, g, y]
    privateKey: [] as string[], // [x, p, q]
    signature: [] as string[],
    valid: false,
    hash: 'SHA-256'
  };

  constructor(private crypto: CryptoService) {}

  // ========== RSA ==========
  generateRSAKeys() {
    this.crypto.generateRSAKeys(this.rsa.bits).subscribe(res => {
      this.rsa.publicKey = res.public_key;
      this.rsa.privateKey = res.private_key;
    });
  }

  rsaEncrypt() {
    this.crypto.rsaEncrypt(this.rsa.message, this.rsa.publicKey).subscribe(res => {
      this.rsa.ciphertext = res.ciphertext;
    });
  }

  rsaDecrypt() {
    const inputCipherArray = this.rsa.cipherInput
      .split(',')
      .map(c => c.trim())
      .filter(c => c !== '');
  
    this.crypto.rsaDecrypt(inputCipherArray, this.rsa.privateKey).subscribe(res => {
      this.rsa.decrypted = res.message;
    });
  }
  

  rsaSign() {
    this.crypto.rsaSign(this.rsa.message, this.rsa.privateKey, this.rsa.hash).subscribe(res => {
      this.rsa.signature = res.signature;
    });
  }

  rsaVerify() {
    const parsedPublicKey = this.rsa.publicKeyInput
      ? this.rsa.publicKeyInput.split(',').map(x => x.trim())
      : this.rsa.publicKey;
  
    const signature = this.rsa.signatureInput || this.rsa.signature;
  
    this.crypto.rsaVerify(this.rsa.message, signature, parsedPublicKey, this.rsa.hash).subscribe(res => {
      this.rsa.valid = res.valid;
    });
  }

  // ========== ElGamal ==========
  generateElGamalKeys() {
    this.crypto.generateElGamalKeys(this.elgamal.bits).subscribe(res => {
      this.elgamal.publicKey = res.public_key;
      this.elgamal.privateKey = res.private_key;
    });
  }

  elgamalEncrypt() {
    this.crypto.elgamalEncrypt(this.elgamal.message, this.elgamal.publicKey).subscribe(res => {
      this.elgamal.a = res.a;
      this.elgamal.bList = res.b_list;
    });
  }

  elgamalDecrypt() {
    const a = this.elgamal.cipherAInput || this.elgamal.a;
    const bList = this.elgamal.cipherBInput
      ? this.elgamal.cipherBInput.split(',').map(x => x.trim())
      : this.elgamal.bList;
  
    this.crypto.elgamalDecrypt(a, bList, this.elgamal.privateKey).subscribe(res => {
      this.elgamal.decrypted = res.message;
    });
  }

  elgamalSign() {
    this.crypto.elgamalSign(this.elgamal.message, this.elgamal.privateKey, this.elgamal.hash).subscribe(res => {
      this.elgamal.signature = res.signature;
    });
  }

  elgamalVerify() {
    const signature = this.elgamal.signatureInput
      ? this.elgamal.signatureInput.split(',').map(x => x.trim())
      : this.elgamal.signature;
  
    const publicKey = this.elgamal.publicKeyInput
      ? this.elgamal.publicKeyInput.split(',').map(x => x.trim())
      : this.elgamal.publicKey;
  
    this.crypto.elgamalVerify(this.elgamal.message, signature, publicKey, this.elgamal.hash)
      .subscribe(res => {
        this.elgamal.valid = res.valid;
      });
  }
  

  // ========== DSA ==========
  generateDSAKeys() {
    this.crypto.generateDSAKeys(this.dsa.L, this.dsa.N).subscribe(res => {
      this.dsa.publicKey = res.public_key;
      this.dsa.privateKey = res.private_key;
    });
  }

  dsaSign() {
    this.crypto.dsaSign(this.dsa.message, this.dsa.privateKey, this.dsa.hash).subscribe(res => {
      this.dsa.signature = res.signature;
    });
  }

  dsaVerify() {
    this.crypto.dsaVerify(this.dsa.message, this.dsa.signature, this.dsa.publicKey, this.dsa.hash)
      .subscribe(res => {
        this.dsa.valid = res.valid;
      });
  }

  saveToFile(filename: string, content: string) {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  }
  
}
